from bs4 import BeautifulSoup
import pandas as pd
import requests
import time, os
import random
from requests.adapters import HTTPAdapter

energy_dist = {'energy energy-grass' : '草', 'energy energy-fire' : '火', 'energy energy-water' : '水', 'energy energy-lightning' : '光', 'energy energy-psychic' : '超能力', 'energy energy-fighting' : '格斗',
                'energy energy-darkness' : '暗', 'energy energy-metal' : '金属', 'energy energy-colorless' : '无属性', 'energy energy-fairy' : '妖精', 'energy energy-dragon' : '龙'}

series = [ 'SM', 'XY', 'BW', 'HGSS', 'PL', 'DP', 'EX']#'SWSH',

packages = { 'HSP' : 25} #'SM12' : 236, 'SMA' : 50, 'SM115' : 69, 'SM11' : 236, 'SM10' : 234, 'det' : 196, 'SM9' : 181, 'SMP' : 244, 'g1' : 83, 'XY9' : 122, 'XY8' : 162, 'XY7' : 98,
            #'XY6' : 108, 'XY10' : 124, 'XY5' : 160, 'XY4' : 119, 'XY3' : 111, 'XY2' : 106, 'XY1' : 146, 'XYP' : 178, 'BW11' : 113, 'BW10' : 101, 'BW9' : 116, 'BW8' : 135,
            #'BW7' : 149, 'DV1' : 20, 'BW6' : 124, 'BW5' : 108, 'BW4' : 99, 'BW3' : 101, 'BW2' : 98, 'BW1' : 114, 'BWP' : 101, 'HGSS4' : 103, 'HGSS3' : 91, 'HGSS2' : 96, 'PL4' : 111, 'PL3' : 153, 'PL2' : 120, 'PL1' : 133, 'DP7' : 106, 'DP6' : 146, 'DP5' : 100, 'DP4' : 106, 'DP3' : 132, 'DP2' : 124, 'DP1' : 130,
            #'EX16' : 108, 'EX15' : 101, 'EX14' : 100, 'EX13' : 111, 'EX12' : 93, 'EX11' : 114, 'EX10' : 144, 'EX9' : 106, 'EX8' : 106, 'EX7' : 109, 'EX6' : 112, 'EX5' : 101, 'EX4' : 95,
            #'EX3' : 97, 'EX2' : 100, 'EX1' : 109'SM8' : 214, 'SM75' : 78, 'SM7' : 168, 'SM6' : 131, 'SM5' : 138, 'XY0' : 39,
            #'SM4' : 111, 'SM35' : 73, 'SM3' : 147, 'SM2' : 145, 'SM' : 149,'COL' : 95, 'XY12' : 108, 'XY11' : 114, 'DC' : 34, 'DV1' : 20,
            #'HGSS1' : 123,

df_ret = pd.DataFrame(columns = ["卡名", "系列编号", "卡牌编号", "罕贵度",
                                 "基础类型", "基础类型补充",
                                  "生命", "属性", 
                                  "特殊类型1", "特殊类型1描述", "特殊类型2", "特殊类型2描述",
                                   "特性", "特性描述",
                                    "技能名1", "技能1费用", "技能描述1", "技能伤害1", "技能名2", "技能2费用", "技能描述2", "技能伤害2",
                                    "弱点", "抗性", "撤退"])

df_ret_row = {"卡名" : "", "系列编号" : "", "卡牌编号" : "", "罕贵度" : "",
                                 "基础类型" : "", "基础类型补充" : "",
                                  "生命" : "", "属性" : "", 
                                  "特殊类型1" : "", "特殊类型1描述" : "", "特殊类型2" : "", "特殊类型2描述" : "",
                                   "特性" : "", "特性描述" : "",
                                    "技能名1" : "", "技能1费用" : '', "技能描述1" : "", "技能伤害1" : "", "技能名2" : "", "技能2费用" : '', "技能描述2" : "", "技能伤害2" : "",
                                    "弱点" : "", "抗性" : "", "撤退" : ""}

sess = requests.Session()

sess.mount("http://", HTTPAdapter(max_retries=5))
sess.mount("https://", HTTPAdapter(max_retries=5))

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'}

def down_detail(url):
    global df_ret
    global df_ret_row
    
    print(url)
    try:
        res = requests.get(url, headers = headers)
    except requests.exceptions.RequestException as e:
        print(e)

    constents = res.text

    soup = BeautifulSoup(constents, "html.parser")

    try:
        df_ret_row["卡名"] = soup.find(name='div', attrs={'class' : 'card-header'}).get_text().strip() if 'energy' not in soup.find(name='div', attrs={'class' : 'card-header'}) else '基本' + energy_dist[str(soup.find(name='div', attrs={'class' : 'card-header'}).find(name='i')['class'])] + '能量'
        df_ret_row["系列编号"] = url.split('/')[-1].split('_')[0].strip()
        df_ret_row["卡牌编号"] = url.split('/')[-1].strip()
        df_ret_row["罕贵度"] = soup.find(name="p", attrs={'class' : 'rarity'}).get_text().split('/')[1].strip()
        df_ret_row["基础类型"] = soup.find(name='div', attrs={'class' : 'card-content'}).find(name='div', attrs={'class' : 'left'}).find(name='label').get_text().strip()
        df_ret_row["基础类型补充"] = soup.find(name='div', attrs={'class' : 'card-content'}).find(name='div', attrs={'class' : 'left'}).find(name='div').get_text().strip() if soup.find(name='div', attrs={'class' : 'card-content'}).find(name='div', attrs={'class' : 'left'}).find(name='div') is not None else '-'
        df_ret_row['生命'] = soup.find(name='span', attrs={'class' : 'hp'}).get_text().strip() if soup.find(name='span', attrs={'class' : 'hp'}) in soup else '-' 
        df_ret_row['属性'] = energy_dist[soup.find(name='div', attrs={'class' : 'card-content'}).find(name='span', attrs={'class' : 'right'}).find(name='div', attrs={'class' : 'float-right'}).find(name='i')['class']] if soup.find(name='div', attrs={'class' : 'card-content'}).find(name='span', attrs={'class' : 'right'}).find(name='div', attrs={'class' : 'float-right'}) in soup else  '-'
        
        df_ret_row['特殊类型1'] = '-'
        df_ret_row['特殊类型1描述'] = '-'
        df_ret_row['特殊类型2'] = '-'
        df_ret_row['特殊类型2描述'] = '-'

        df_ret_row['特性'] = '-'
        df_ret_row['特性描述'] = '-'

        df_ret_row['技能名1'] = '-'
        df_ret_row['技能1费用'] = '-'
        df_ret_row['技能描述1'] = '-'
        df_ret_row['技能伤害1'] = '-'
        df_ret_row['技能名2'] = '-'
        df_ret_row['技能2费用'] = '-'
        df_ret_row['技能描述2'] = '-'
        df_ret_row['技能伤害2'] = '-'

        df_ret_row['弱点'] = '-'
        df_ret_row['抗性'] = '-'
        df_ret_row['撤退'] = '-'
    except:
        df_ret_row["卡名"] = '-' #soup.find(name='div', attrs={'class' : 'card-header'}).get_text().strip() if 'energy' not in soup.find(name='div', attrs={'class' : 'card-header'}) else '基本' + energy_dist[str(soup.find(name='div', attrs={'class' : 'card-header'}).find(name='i')['class'])] + '能量'
        df_ret_row["系列编号"] = '-' #url.split('/')[-1].split('_')[0].strip()
        df_ret_row["卡牌编号"] = '-' #url.split('/')[-1].strip()
        df_ret_row["罕贵度"] = '-' #soup.find(name="p", attrs={'class' : 'rarity'}).get_text().split('/')[1].strip()
        df_ret_row["基础类型"] = '-' #soup.find(name='div', attrs={'class' : 'card-content'}).find(name='div', attrs={'class' : 'left'}).find(name='label').get_text().strip()
        df_ret_row["基础类型补充"] = '-' #soup.find(name='div', attrs={'class' : 'card-content'}).find(name='div', attrs={'class' : 'left'}).find(name='div').get_text().strip() if soup.find(name='div', attrs={'class' : 'card-content'}).find(name='div', attrs={'class' : 'left'}).find(name='div') is not None else '-'
        df_ret_row['生命'] = '-' #soup.find(name='span', attrs={'class' : 'hp'}).get_text().strip() if soup.find(name='span', attrs={'class' : 'hp'}) in soup else '-' 
        df_ret_row['属性'] = '-' #energy_dist[soup.find(name='div', attrs={'class' : 'card-content'}).find(name='span', attrs={'class' : 'right'}).find(name='div', attrs={'class' : 'float-right'}).find(name='i')['class']] if soup.find(name='div', attrs={'class' : 'card-content'}).find(name='span', attrs={'class' : 'right'}).find(name='div', attrs={'class' : 'float-right'}) in soup else  '-'
        
        df_ret_row['特殊类型1'] = '-'
        df_ret_row['特殊类型1描述'] = '-'
        df_ret_row['特殊类型2'] = '-'
        df_ret_row['特殊类型2描述'] = '-'

        df_ret_row['特性'] = '-'
        df_ret_row['特性描述'] = '-'

        df_ret_row['技能名1'] = '-'
        df_ret_row['技能1费用'] = '-'
        df_ret_row['技能描述1'] = '-'
        df_ret_row['技能伤害1'] = '-'
        df_ret_row['技能名2'] = '-'
        df_ret_row['技能2费用'] = '-'
        df_ret_row['技能描述2'] = '-'
        df_ret_row['技能伤害2'] = '-'

        df_ret_row['弱点'] = '-'
        df_ret_row['抗性'] = '-'
        df_ret_row['撤退'] = '-'

    # if soup.find(name='div', attrs={'class' : 'r1'}) in soup:
    #     df_ret_row['特殊类型1'] = soup.find_all(name='div', attrs={'class' : 'r1'})[0].find(name='span', attrs={'class' : 'addon'}).get_text().strip()
    #     df_ret_row['特殊类型1描述'] = soup.find_all(name='div', attrs={'class' : 'r1'})[0].find(name='p').get_text().strip()
    #     df_ret_row['特殊类型2'] = soup.find_all(name='div', attrs={'class' : 'r1'})[1].find(name='span', attrs={'class' : 'addon'}).get_text().strip() if len(soup.find_all(name='div', attrs={'class' : 'r1'})) > 1 else '-'
    #     df_ret_row['特殊类型2描述'] = soup.find_all(name='div', attrs={'class' : 'r1'})[1].find(name='p').get_text().strip() if len(soup.find_all(name='div', attrs={'class' : 'r1'})) > 1 else '-'
    # else:
    #     df_ret_row['特殊类型1'] = '-'
    #     df_ret_row['特殊类型1描述'] = '-'
    #     df_ret_row['特殊类型2'] = '-'
    #     df_ret_row['特殊类型2描述'] = '-'
    
    # try:
    #     soup.find(name='div', attrs={'class' : 'abilitys'})
    #     soup.find(name='div', attrs={'class' : 'abilitys'}).find(name='div', attrs={'class':'card'})
    # except:
    #     df_ret_row['特性'] = '-'
    #     df_ret_row['特性描述'] = '-'
    # else:
    #     df_ret_row['特性'] = soup.find(name='div', attrs={'class' : 'abilitys'}).find(name='span',attrs={'class' : 'label'}).get_text().strip()
    #     df_ret_row['特性描述'] = soup.find(name='div', attrs={'class' : 'abilitys'}).find(name='div', attrs={'class' : 'card-body'}).get_text().strip()

    # try:
    #     soup.find(name='div', attrs={'class' : 'power'})
    #     soup.find(name='div', attrs={'class' : 'power'}).find(name='div', attrs={'class' : 'card'})
    # except:
    #     df_ret_row['技能名1'] = '-'
    #     df_ret_row['技能1费用'] = '-'
    #     df_ret_row['技能描述1'] = '-'
    #     df_ret_row['技能伤害1'] = '-'
    #     df_ret_row['技能名2'] = '-'
    #     df_ret_row['技能2费用'] = '-'
    #     df_ret_row['技能描述2'] = '-'
    #     df_ret_row['技能伤害2'] = '-'
    # else:
    #     #print(soup.find(name='div', attrs={'class' : 'power'}).find_all(name='div', attrs={'class' : 'card'})[0].find(name='h3',attrs={'class':'card-header'}).text)
    #     df_ret_row['技能名1'] = soup.find(name='div', attrs={'class' : 'power'}).find_all(name='div', attrs={'class' : 'card'})[0].find(name='h3',attrs={'class':'card-header'}).text[2].strip()
    #     df_ret_row['技能1费用'] = '-' if soup.find(name='div', attrs={'class' : 'power'}).find_all(name='div', attrs={'class' : 'card'})[0].find(name='span', attrs={'class' : 'cost'}) not in soup.find(name='div', attrs={'class' : 'power'}).find_all(name='div', attrs={'class' : 'card'})[0] else energy_dist[soup.find(name='div', attrs={'class' : 'power'}).find_all(name='div', attrs={'class' : 'card'})[0].find_all(name='i')[0]['class']] + energy_dist[soup.find(name='div', attrs={'class' : 'power'}).find_all(name='div', attrs={'class' : 'card'})[0].find_all(name='i')[1]['class']]
    #     df_ret_row['技能伤害1'] = '-' if soup.find(name='div', attrs={'class' : 'power'}).find_all(name='div', attrs={'class' : 'card'})[0].find(name='span', attrs={'class' : 'float-right'}) not in soup.find(name='div', attrs={'class' : 'power'}).find_all(name='div', attrs={'class' : 'card'})[0] else soup.find(name='div', attrs={'class' : 'power'}).find_all(name='div', attrs={'class' : 'card'})[0].find(name='span', attrs={'class' : 'float-right'}).get_text()
    #     df_ret_row['技能描述1'] = '-' if soup.find(name='div', attrs={'class' : 'power'}).find_all(name='div', attrs={'class' : 'card'})[0].find(name='div', attrs={'class' : 'card-body'}).get_text().strip() == '' else soup.find(name='div', attrs={'class' : 'power'}).find_all(name='div', attrs={'class' : 'card'})[0].find(name='div', attrs={'class' : 'card-body'}).get_text().strip()
    #     df_ret_row['技能名2'] = '-' if len(soup.find(name='div', attrs={'class' : 'power'}).find_all(name='div', attrs={'class' : 'card'})) <= 1 else soup.find(name='div', attrs={'class' : 'power'}).find_all(name='div', attrs={'class' : 'card'})[1].find(name='h3',attrs={'class':'card-header'}, text=True).text[2].strip()
    #     df_ret_row['技能2费用'] = '-' if len(soup.find(name='div', attrs={'class' : 'power'}).find_all(name='div', attrs={'class' : 'card'})) <= 1 else energy_dist[soup.find(name='div', attrs={'class' : 'power'}).find_all(name='div', attrs={'class' : 'card'})[1].find_all(name='i')[0]['class']] + energy_dist[soup.find(name='div', attrs={'class' : 'power'}).find_all(name='div', attrs={'class' : 'card'})[1].find_all(name='i')[1]['class']]
    #     df_ret_row['技能伤害2'] = '-' if len(soup.find(name='div', attrs={'class' : 'power'}).find_all(name='div', attrs={'class' : 'card'})) <= 1 or soup.find(name='div', attrs={'class' : 'power'}).find_all(name='div', attrs={'class' : 'card'})[1].find(name='span', attrs={'class' : 'float-right'}) not in soup.find(name='div', attrs={'class' : 'power'}).find_all(name='div', attrs={'class' : 'card'})[1] else soup.find(name='div', attrs={'class' : 'power'}).find_all(name='div', attrs={'class' : 'card'})[1].find(name='span', attrs={'class' : 'float-right'}).get_text()
    #     df_ret_row['技能描述2'] = '-' if len(soup.find(name='div', attrs={'class' : 'power'}).find_all(name='div', attrs={'class' : 'card'})) <= 1 or soup.find(name='div', attrs={'class' : 'power'}).find_all(name='div', attrs={'class' : 'card'})[1].find(name='div', attrs={'class' : 'card-body'}).get_text().strip() == ''  else soup.find(name='div', attrs={'class' : 'power'}).find_all(name='div', attrs={'class' : 'card'})[1].find(name='div', attrs={'class' : 'card-body'}).get_text().strip()

    # if soup.find(name='div', attrs={'class' : 'jumbotron'}) not in soup:
    #     df_ret_row['弱点'] = '-'
    #     df_ret_row['抗性'] = '-'
    #     df_ret_row['撤退'] = '-'
    # else:
    #     df_ret_row['弱点'] = '-' if soup.find_all(name='div', attrs={'class':'col-4'})[0].children.children is not None else energy_dist[soup.find_all(name='div', attrs={'class':'col-4'})[0].find_all(name="i")[0]['class']] if len(soup.find_all(name='div', attrs={'class':'col-4'})[0].find_all(name="i")) <= 1 else energy_dist[soup.find_all(name='div', attrs={'class':'col-4'})[0].find_all(name="i")[0]['class']] + energy_dist[soup.find_all(name='div', attrs={'class':'col-4'})[0].find_all(name="i")[1]['class']]
    #     df_ret_row['抗性'] = '-' if soup.find_all(name='div', attrs={'class':'col-4'})[1].children.children is not None else energy_dist[soup.find_all(name='div', attrs={'class':'col-4'})[1].find_all(name="i")[0]['class']] + soup.find_all(name='div', attrs={'class':'col-4'})[1].find(name='div', attrs={'class' : 'rwbox'}, text=True).get_text()
    #     df_ret_row['撤退'] = '-' if soup.find_all(name='div', attrs={'class':'col-4'})[2].children.children is not None else energy_dist[soup.find_all(name='div', attrs={'class':'col-4'})[2].find_all(name="i")[0]['class']] if len(soup.find_all(name='div', attrs={'class':'col-4'})[2].find_all(name="i")) <= 1 else energy_dist[soup.find_all(name='div', attrs={'class':'col-4'})[2].find_all(name="i")[0]['class']] + energy_dist[soup.find_all(name='div', attrs={'class':'col-4'})[2].find_all(name="i")[1]['class']]
    df_ret = df_ret.append(df_ret_row, ignore_index=True)

    # image_url = soup.find(name='div', attrs={'class' : 'card-image text-center'}).find(name='img')['src']
    # image_name = image_url.split('/')[-1]
    # download_img(image_url, image_name)
    df_ret_row.clear()
    print(df_ret)


def download_img(img_url, img_name):
    print(img_url)
    header = {
       'User-Agent':
       'Mozilla/5.0 (Windows NT 6.1; Win64; WOW64) AppleWebKit/537.36'
       '(KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    try:
        r = sess.get(img_url, headers = header, stream = True)
        print(r.status_code)
        if r.status_code == 200:
            filename = os.path.join(r'C:\Users\27042\Desktop\pa\Pic\ptcg_image', img_name)
            open(filename, 'wb').write(r.content)
            print(filename)
            print('done')
        del r
    except requests.exceptions.RequestException as e:
        print(e)


if __name__ == '__main__':
    #url1 = 'http://www.pmtcgo.com/'
    # try:
    #     res1 = sess.get(url=url1, headers=headers).text
    # except requests.exceptions.RequestException as e:
    #     print(e)
    # soup1 = BeautifulSoup(res1, "html.parser")
    # hrefs = soup1.find_all(name="a", attrs={"class" : "col-6 col-lg-4 col-xl-3"})
    n = 0
    for key, value in packages.items():
        if n < 0:
            n += 1
            continue
        packageName = key
        max_card = value
        for i in range(1, int(max_card) + 1):
            if packageName == 'SWSHP':
                url = 'http://www.pmtcgo.com/card/{}_{}'.format(packageName, 'SWSH' + str(i))
            elif packageName == 'SMA':
                url = 'http://www.pmtcgo.com/card/{}_{}'.format(packageName, 'SV' + str(i))
            elif packageName == 'SMP':
                url = 'http://www.pmtcgo.com/card/{}_{}'.format(packageName, 'SM' + str(i).zfill(2))
            elif packageName == 'XYP':
                url = 'http://www.pmtcgo.com/card/{}_{}'.format(packageName, 'XY' + str(i).zfill(2))
            elif packageName == 'BWP':
                url = 'http://www.pmtcgo.com/card/{}_{}'.format(packageName, 'BW' + str(i).zfill(2))
            elif packageName == 'HSP':
                url = 'http://www.pmtcgo.com/card/{}_{}'.format(packageName, 'HGSS' + str(i).zfill(2))
            elif packageName == 'SM':
                url = 'http://www.pmtcgo.com/card/{}_{}'.format(packageName + '1', str(i))
            elif packageName == 'COL':
                url = 'http://www.pmtcgo.com/card/{}_{}'.format(packageName + '1', str(i))
            elif packageName == 'DC':
                url = 'http://www.pmtcgo.com/card/{}_{}'.format(packageName + '1', str(i))
            elif packageName == 'HSP':
                url = 'http://www.pmtcgo.com/card/{}_{}'.format(packageName, 'HGSS' + str(i).zfill(2))
            else:
                url = 'http://www.pmtcgo.com/card/{}_{}'.format(packageName, str(i))

            if packageName == 'SMP' and (i == 4 or i == 148 or i == 170 or i == 190 or i == 194):
                continue
            down_detail(url)
            time.sleep(int(format(random.randint(1, 3))))
            if i % 10 == 1:
                df_ret.to_excel(r'C:\Users\27042\Desktop\pa\ptcg_detail.xlsx', index = False)
        n += 1
        df_ret.to_excel(r'C:\Users\27042\Desktop\pa\ptcg_detail.xlsx', index = False)
    df_ret.to_excel(r'C:\Users\27042\Desktop\pa\ptcg_detail.xlsx', index = False)

#7767