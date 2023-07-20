import requests
import os
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
import time
import random
import re
import pandas as pd

df_row = pd.DataFrame(columns=['name', 'cardnumber', 'package', 'ip', 'cost', 'atk', 'def', 'type', 'attribute', 'rarity', 'effect', 'line'])

df_row_now = {'name' : '', 'cardnumber' : '', 'package' : '', 'ip' : '', 'cost' : '', 'atk' : '', 'def' : '', 'type' : '', 'attribute' : '', 'rarity' : '', 'effect' : '', 'line' : ''}

sess = requests.Session()
sess.mount('http://', HTTPAdapter(max_retries=3))
sess.mount('https://', HTTPAdapter(max_retries=3))

header = {
       'User-Agent':
       'Mozilla/5.0 (Windows NT 6.1; Win64; WOW64) AppleWebKit/537.36'
       '(KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

url1 = "https://rebirth-fy.com/cardlist/cardsearch?keyword=&keyword_type[]=all&search_type[]=and&expansion=&title=&card_kind=&cost_s=&cost_e=&atk_s=&atk_e=&def_s=&def_e="

r = sess.get(url1, headers=header, timeout=5)
#print(re.findall( r"var max_page = [0-9]{3};", r.content.decode('utf-8')))
max_page = re.sub("\D", "", str(re.findall( r"var max_page = [0-9]{3};", r.content.decode('utf-8'))))

uuid = 0

for i in range(1, int(max_page) + 1):
    url2 = "https://rebirth-fy.com/cardlist/cardsearch_ex?keyword=&keyword_type[0]=all&search_type[0]=and&expansion=&title=&card_kind=&cost_s=&cost_e=&atk_s=&atk_e=&def_s=&def_e=&page={}".format(str(i))
    r1 = sess.get(url2, headers=header, timeout=5)
    soup = BeautifulSoup(r1.content, "html.parser")

    href = soup.find_all(name='a')
    for link in href:
        url3 = "https://rebirth-fy.com" + link['href']
        try:
            r2 = sess.get(url3, headers=header, timeout=5)
            soup2 = BeautifulSoup(r2.content, "html.parser")
            card_info = soup2.find(name='div', attrs={'class': 'cardlist-texts'})
            df_row_now['name'] = card_info.find(name='h2', attrs={'class':'cardlist-title'}).get_text().strip()
            df_row_now['cardnumber'] = card_info.find(name='p', attrs={'class':'cardlist-number'}).get_text().strip()
            text = []
            for a in card_info.find_all(lambda x: x.name == 'dl' and x.get('class') == ['cardlist-text']):
                for b in a.find_all('dd'):
                    text.append(b)
            df_row_now['package'] = text[0].get_text().strip()
            df_row_now['ip'] = text[1].get_text().strip()
            df_row_now['cost'] = text[2].get_text().strip()
            df_row_now['rarity'] = text[3].get_text().strip()
            df_row_now['type'] = text[4].get_text().strip()
            df_row_now['attribute'] = text[5].get_text().strip()
            df_row_now['atk'] = text[6].get_text().strip()
            df_row_now['def'] = text[7].get_text().strip()
            df_row_now['line'] = card_info.find('p', attrs={'class' : 'cardlist-flavor'}).get_text().strip()
            df_row_now['effect'] = card_info.find('div', attrs={'class' : 'cardlist-free'}).get_text().strip()
            df_row = df_row.append(df_row_now, ignore_index=True)
            df_row_now.clear()
            print(df_row)
            uuid += 1
            if uuid % 5 == 0:
                df_row.to_excel(os.getcwd() + '/RBF_detail_download.xlsx', index=False)
            image_url = str(card_info.find(name='img')['src']).replace("s3-ap-northeast-1.amazonaws.com/", "")
            try:
                r = sess.get(image_url, headers = header, stream = True, timeout=5)
                img_name = str(image_url).split('/')[-1]
                print(r.status_code)
                if r.status_code == 200:
                    filename = os.path.join(r'C:\Users\27042\Desktop\pa\Pic\rbf_image', img_name)
                    open(filename, 'wb').write(r.content)
                    print(filename)
                    print('done')
                del r
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)
            df_row.to_excel(os.getcwd() + '/RBF_detail_download.xlsx', index=False)
    df_row.to_excel(os.getcwd() + '/RBF_detail_download.xlsx', index=False)
df_row.to_excel(os.getcwd() + '/RBF_detail_download.xlsx', index=False)
            
