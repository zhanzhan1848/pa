import requests
from bs4 import BeautifulSoup
import pandas as pd
from requests.adapters import HTTPAdapter
import os, time, random, re

package_dist = { 'BT' : 7, 'LBT' : 3, 'TTD' : 5, 'TB' : 6, 'SS' : 2}#'SD' : 5, 'LTD' : 1, 'TD' : 3,

s = requests.Session()

s.mount('http://', HTTPAdapter(max_retries=3))
s.mount('https://', HTTPAdapter(max_retries=3))

df_ret = pd.DataFrame(columns= ['中文名', '日文名', '系列编号', '卡牌编号', '罕贵度', '种类', '国家', '种族', '等级', '力量', '护盾', '效果'])

df_ret_row = {'中文名' : '', '日文名' : '', '系列编号' : '', '卡牌编号' : '', '罕贵度' : '', '种类' : '', '国家' : '', '种族' : '', '等级' : '', '力量' : '', '护盾' : '', '效果' : ''}

def download_img(img_url, img_name):
    print(img_url)
    header = {
       'User-Agent':
       'Mozilla/5.0 (Windows NT 6.1; Win64; WOW64) AppleWebKit/537.36'
       '(KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    try:
        r = s.get(img_url, headers = header, stream = True)
        print(r.status_code)
        if r.status_code == 200:
            filename = os.path.join(r'C:\Users\27042\Desktop\pa\Pic\vg_image', img_name)
            open(filename, 'wb').write(r.content)
            print(filename)
            print('done')
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
        r = s.get(url, headers=headers)
        if(r.status_code==200):
            constents = r.text

            soup = BeautifulSoup(constents, "html.parser")

            all_card_detail = soup.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['card-item'])
            for tag in all_card_detail:
                df_ret_row['中文名'] = tag.find(name='h2').find(name='a').get_text().strip()
                df_ret_row['日文名'] = tag.find(name='h3').get_text().strip()
                #print(tag.find(name='div', attrs={'class' : 'meta head clearfix'}).get_text().splitlines())
                df_ret_row['系列编号'] = tag.find(name='div', attrs={'class' : 'meta head clearfix'}).get_text().split('/')[0].strip()
                df_ret_row['卡牌编号'] = tag.find(name='div', attrs={'class' : 'meta head clearfix'}).get_text().splitlines()[1].strip().split(' ')[0].strip()
                df_ret_row['罕贵度'] = tag.find(name='div', attrs={'class' : 'meta head clearfix'}).get_text().splitlines()[1].strip().split(' ')[1].strip()
                df_ret_row['种类'] = tag.find(name='div', attrs={'class' : 'meta head clearfix'}).get_text().splitlines()[3].strip().split(' ')[1].strip()
                df_ret_row['效果'] = tag.find(name='p', attrs= {'class' : 'effect'}).get_text().strip()
                sec_tag = tag.find(lambda tag: tag.name == 'div' and tag.get('class') == ['meta'])
                df_ret_row['国家'] = sec_tag.find_all(name='div', attrs={'class' : 'value'})[0].get_text()
                df_ret_row['种族'] = sec_tag.find_all(name='div', attrs={'class' : 'value'})[1].get_text()
                df_ret_row['等级'] = sec_tag.find_all(name='div', attrs={'class' : 'value'})[2].get_text()
                df_ret_row['力量'] = sec_tag.find_all(name='div', attrs={'class' : 'value'})[3].get_text()
                df_ret_row['护盾'] = sec_tag.find_all(name='div', attrs={'class' : 'value'})[4].get_text()
                df_ret = df_ret.append(df_ret_row, ignore_index=True)
                image_url = tag.find(name = 'div', attrs= {'class' : 'card-image'}).find(name='img')['data-src']
                image_name = tag.find(name='div', attrs={'class' : 'meta head clearfix'}).get_text().splitlines()[1].strip().split(' ')[0].strip().replace('/', '-') + '.jpg'
                download_img(image_url, image_name)
                df_ret_row.clear()
                print(df_ret)
        if(r.status_code==404):
            print(df_ret)
    except requests.exceptions.RequestException as e:
        print(e)


if __name__ == '__main__':
    for key, value in package_dist.items():
        for i in range(1, int(value) + 1):
            url = 'https://vgcard.yimieji.com/Package/D-{}{:02d}'.format(key, i)
            print(url)
            down_detail(url)
            df_ret.to_excel(r'C:\Users\27042\Desktop\pa\vg_detail.xlsx', index = False)
            time.sleep(int(format(random.randint(1, 3))))
    