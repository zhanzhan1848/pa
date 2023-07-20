import requests
from bs4 import BeautifulSoup
import os
from requests.adapters import HTTPAdapter
import pandas as pd
import json

sess = requests.Session()
sess.mount('http://', HTTPAdapter(max_retries=3))
sess.mount('https://', HTTPAdapter(max_retries=3))

header = {
       'User-Agent':
       'Mozilla/5.0 (Windows NT 6.1; Win64; WOW64) AppleWebKit/537.36'
       '(KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

df_ret = pd.DataFrame(columns= ['日文名', '系列名', '卡牌编号', '种类', '费用', '能力', '力量', '任务', '特征', '账号', '罕见度', '效果', '台词', '画师'])

df_ret_row = { '日文名' :'', '系列名' :'', '卡牌编号' :'', '种类' :'', '费用' :'', '能力' :'', '力量' :'', '任务' :'', '特征' :'', '账号' :'', '罕见度' : '', '效果' : '', '台词' : '', '画师' : ''}

uid = 1

for i in range(1, 24):
    url1 = "https://vividztcg.com/card/?pg={}&search=1".format(i)
    try:
        r1 = sess.get(url1, headers=header, timeout=10)
        soup = BeautifulSoup(r1.text, 'html.parser')

        card_nums = soup.find('ul', attrs={'class':'list'}).find_all('img')
        for card_num in card_nums:
            url2 = "https://vividztcg.com/assets/inc/card.php?no={}".format(card_num['data-modal-card'])
            r2 = sess.get(url2, headers=header, timeout=10)
            soup1 = BeautifulSoup(r2.text, 'html.parser')
            df_ret_row['卡牌编号'] = soup1.find('li', attrs={'class':'no'}).get_text().strip()
            df_ret_row['系列名'] = soup1.find('li', attrs={'class':'no'}).get_text().split('-')[0].strip()
            df_ret_row['种类'] = soup1.find('li', attrs={'class':'type'}).get_text().strip()
            df_ret_row['罕见度'] = soup1.find('li', attrs={'class':'rarity'}).get_text().strip()
            df_ret_row['日文名'] = soup1.find('h1').get_text().strip()
            df_ret_row['特征'] =  soup1.find('ul',attrs={'class':'icons'}).find_all('li')[0].find('img')['alt']
            df_ret_row['账号'] =  soup1.find('ul',attrs={'class':'icons'}).find_all('li')[1].find('img')['alt']
            df_ret_row['能力'] =  soup1.find('ul',attrs={'class':'icons'}).find_all('li')[2].find('img')['alt']
            df_ret_row['任务'] = soup1.find('ul',attrs={'class':'infos'}).find_all('p', attrs={'class':'data'})[0].get_text().strip()
            df_ret_row['费用'] = soup1.find('ul',attrs={'class':'infos'}).find_all('p', attrs={'class':'data'})[1].get_text().strip()
            df_ret_row['力量'] = soup1.find('ul',attrs={'class':'infos'}).find_all('p', attrs={'class':'data'})[1].get_text().strip()
            df_ret_row['效果'] = soup1.find('p',attrs={'class':'text'}).get_text().strip()
            df_ret_row['台词'] = soup1.find('p',attrs={'class':'text emColor02'}).get_text().strip()
            df_ret_row['画师'] = soup1.find('span',attrs={'class':'iblock'}).get_text().strip()
            df_ret = df_ret.append(df_ret_row, ignore_index=True)
            print(df_ret)
            df_ret_row.clear()
            uid += 1
            if uid % 5 == 0:
                df_ret.to_excel(os.getcwd() + "/vividz_detail.xlsx", index=False)
            img_url = soup1.find('div', attrs={'class':'pic'}).find('img')['src']
            try:
                r2 = sess.get(img_url, headers = header, stream = True, timeout=5)
                print(r2.status_code)
                if r2.status_code == 200:
                    filename = os.path.join(os.getcwd() + '/Pic/vividz_image/', img_url.split('/')[-1])
                    open(filename, 'wb').write(r2.content)
                    print(filename)
                    print('done')
                del r2
            except requests.exceptions.RequestException as e:
                print(e)
    except Exception as e:
        print(e)
        uid += 1
        df_ret.to_excel(os.getcwd() + "/vividz_detail.xlsx", index=False)