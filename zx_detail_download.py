import requests
from bs4 import BeautifulSoup
import pandas as pd
from requests.adapters import HTTPAdapter
import os, time, random, re

package_dist = { 'B' : {'min' : 31, 'max' : 44}, 'E' : {'min' : 20, 'max' : 38}, 'SD' : {'min' : 4, 'max' : 6}, 'CS' : {'min':1, 'max':2}, 'P' : {'min' : 31, 'max' : 44}, 'G' : {'min' : 5, 'max' : 24}} #'SD' : 5, 'LTD' : 1, 'TD' : 3, 'C' : {'min' : }

s = requests.Session()

s.mount('http://', HTTPAdapter(max_retries=3))
s.mount('https://', HTTPAdapter(max_retries=3))

df_ret = pd.DataFrame(columns= ['中文名', '日文名', '系列编号', '卡牌编号', '罕贵度', '费用', '颜色', '种族', '力量', '效果'])

df_ret_row = {'中文名' : '', '日文名' : '', '系列编号' : '', '卡牌编号' : '', '罕贵度' : '', '费用' : '', '颜色' : '', '种族' : '', '力量' : '', '效果' : ''}

def download_img(img_url, img_name):
    print(img_url)
    header = {
       'User-Agent':
       'Mozilla/5.0 (Windows NT 6.1; Win64; WOW64) AppleWebKit/537.36'
       '(KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    try:
        r = s.get(img_url, headers = header, stream = True, timeout=5)
        print(r.status_code)
        if r.status_code == 200:
            filename = os.path.join(os.getcwd() + '/Pic/zx_image/', img_name)
            open(filename, 'wb').write(r.content)
            print(filename)
            print('done')
            time.sleep(int(format(random.randint(1, 2))))
        del r
    except requests.exceptions.RequestException as e:
        print(e)

def down_detail(url):
    global df_ret
    global df_ret_row
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'}
    # ret = Request(url, headers = headers)
    # res = urlopen(ret)
    # constents = res.read()
    try:
        r = s.get(url, headers=headers, timeout=5)
        if(r.status_code==200):
            constents = r.text

            soup = BeautifulSoup(constents, "html.parser")

            all_card_detail = soup.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['card-item'])
            for tag in all_card_detail:
                df_ret_row['中文名'] = tag.find(name='h2').find(name='a').get_text().strip()
                df_ret_row['日文名'] = tag.find(name='h3').get_text().strip()
                #print(tag.find(name='div', attrs={'class' : 'meta head clearfix'}).get_text().splitlines())
                df_ret_row['系列编号'] = url.split('/')[-1]
                df_ret_row['卡牌编号'] = tag.find(name='div', attrs={'class' : 'meta head clearfix'}).get_text().splitlines()[1].strip().split(' ')[0].strip()
                df_ret_row['罕贵度'] = tag.find(name='div', attrs={'class' : 'meta head clearfix'}).get_text().splitlines()[1].strip().split(' ')[1].strip()
                df_ret_row['颜色'] = tag.find(name='div', attrs={'class' : 'meta head clearfix'}).get_text().splitlines()[0].strip()
                try:
                    df_ret_row['效果'] = tag.find(name='p', attrs= {'class' : 'effect'}).get_text().strip()
                except:
                    df_ret_row['效果'] = '-'
                sec_tag = tag.find(lambda tag: tag.name == 'div' and tag.get('class') == ['meta'])
                #print(sec_tag.find_all(name='div', attrs={'class' : 'value'})[0].get_text())
                df_ret_row['费用'] = sec_tag.find_all(name='div', attrs={'class' : 'value'})[0].get_text()
                df_ret_row['力量'] = sec_tag.find_all(name='div', attrs={'class' : 'value'})[1].get_text()
                df_ret_row['种族'] = sec_tag.find_all(name='div', attrs={'class' : 'value'})[2].get_text()
                df_ret = df_ret.append(df_ret_row, ignore_index=True)
                image_url = 'http://zximg-cdn.yimieji.com/card/{}/{}.png'.format(df_ret_row['系列编号'], df_ret_row['卡牌编号'])
                #print(image_url)
                image_name = df_ret_row['卡牌编号'] + '.png'
                #print(image_name)
                download_img(image_url, image_name)
                df_ret_row.clear()
                print(df_ret)
        if(r.status_code==404):
            print(df_ret)
    except requests.exceptions.RequestException as e:
        print(e)


if __name__ == '__main__':
    n = 0
    for key, value in package_dist.items():
        for i in range(int(value['min']), int(value['max']) + 1):
            if n < 0:
                n += 1
                continue
            url = 'http://zxcard.yimieji.com/Package/{}{}'.format(key, str(i).zfill(2))
            print(url)
            down_detail(url)
            if n % 5 == 0:
                df_ret.to_excel(os.getcwd() + '/zx_detail.xlsx', index = False)
            time.sleep(int(format(random.randint(1, 2))))
            n += 1
        df_ret.to_excel(os.getcwd() + '/zx_detail.xlsx', index = False)
    df_ret.to_excel(os.getcwd() + '/zx_detail.xlsx', index = False)
    
    