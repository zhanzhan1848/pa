import requests
import os
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
import time
import random
import re
import pandas as pd

df_row = pd.DataFrame(columns=['name', 'cardnumber', 'package', 'ip', 'level', 'cost', 'power', 'soul', 'trigger', 'type', 'attribute', 'color', 'rarity', 'effect', 'line'])

df_row_now = {'name':'', 'cardnumber':'', 'package':'', 'ip':'', 'level':'', 'cost':'', 'power':'', 'soul':'', 'trigger':'', 'type':'', 
              'attribute':'', 'color':'', 'rarity':'', 'effect':'', 'line':''}

sess = requests.Session()
sess.mount('http://', HTTPAdapter(max_retries=3))
sess.mount('https://', HTTPAdapter(max_retries=3))

header = {
       'User-Agent':
       'Mozilla/5.0 (Windows NT 6.1; Win64; WOW64) AppleWebKit/537.36'
       '(KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

url_main = "https://ws-blau.com"

url1 = "https://ws-blau.com/cardlist/cardsearch?expansion=BLK%2F01S"

r = sess.get(url1, headers=header, timeout=5)
#print(re.findall( r"var max_page = [0-9]{3};", r.content.decode('utf-8')))
max_page = re.sub("\D", "", str(re.findall( r"var max_page = [0-9]{1};", r.content.decode('utf-8'))))
print(max_page)

uuid = 0

for i in range(1, int(max_page) + 1):
    url2 = "https://ws-blau.com/cardlist/cardsearch_ex?expansion=BLK%2F01S&view=image&page={}".format(i)
    r2 = sess.get(url2, headers=header, timeout=5)
    soup = BeautifulSoup(r2.content, "html.parser")
    
    for tag in soup.find_all('a'):
        url3 = url_main + tag['href']
        print(url3)
        try:
            r3 = sess.get(url3, headers=header, timeout=5)
            soup2 = BeautifulSoup(r3.content, "html.parser")
            card_info = soup2.find('div', attrs={'class' : 'cardlist-Detail_Box'})
            df_row_now['name'] = card_info.find('h1', attrs={'class' : 'ttl'}).get_text().strip()
            df_row_now['cardnumber'] = card_info.find('div', attrs={'class':'sup'}).find_all('p')[0].get_text().strip()
            df_row_now['line'] = card_info.find('div', attrs={'class':'sup'}).find_all('p')[1].get_text().strip()
            card_info1 = card_info.find('div',attrs={'class':'info'})
            df_row_now['package'] = card_info1.find_all('dl')[0].find('dd').get_text().strip()
            df_row_now['ip'] = card_info1.find_all('dl')[1].find('dd').get_text().strip()
            df_row_now['type'] = card_info1.find_all('dl')[2].find('dd').get_text().strip()
            df_row_now['rarity'] = card_info1.find_all('dl')[3].find('dd').get_text().strip()
            df_row_now['color'] = card_info1.find_all('dl')[4].find('img')['alt']
            try:
                df_row_now['attribute'] = card_info1.find_all('dl')[5].find('dd').get_text().strip()
            except:
                print("No attribute")
                df_row_now['attribute'] = "-"
            card_info2 = card_info.find('div', attrs={'class':'status'})
            df_row_now['level'] = re.sub("レベル", "", card_info2.find_all('span')[0].get_text().strip())   #[text.strip() for text in card_info2.find_all('span', text=True)[0] if text.parent.name != 'span' and text.strip()]
            df_row_now['cost'] = re.sub("コスト", "", card_info2.find_all('span')[2].get_text().strip())
            df_row_now['power'] = re.sub("パワー", "", card_info2.find_all('span')[4].get_text().strip())
            df_row_now['soul'] = re.sub("ソウル", "", card_info2.find_all('span')[6].get_text().strip())
            try:
                df_row_now['trigger'] = str(len(card_info2.find_all('span')[8].find_all('img'))) + card_info2.find_all('span')[8].find_all('img')[0]['ソウル']
            except:
                df_row_now['trigger'] = "-"
            try:
                df_row_now['effect'] = card_info.find('div',attrs={'class':'detail'}).get_text().strip()
            except:
                print("No effect")
                df_row_now['effect'] = "-"
            df_row = df_row.append(df_row_now, ignore_index=True)
            print(df_row)
            df_row_now.clear()
            uuid += 1
            if uuid % 5 == 0:
                df_row.to_excel(os.getcwd() + '/wsb_blk01s_detail.xlsx', index=False)
            img_url = url_main + card_info.find('div', attrs={'class':'img_Box'}).find('img')['src']
            img_name = str(img_url).split('/')[-1]
            try:
                r = sess.get(img_url, headers = header, stream = True, timeout=5)
                print(r.status_code)
                if r.status_code == 200:
                    filename = os.path.join(r'C:\Users\zy\Desktop\pa\pa\Pic\wsb_image', img_name)
                    open(filename, 'wb').write(r.content)
                    print(filename)
                    print('done')
                del r
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)
            df_row.to_excel(os.getcwd() + '/wsb_blk01s_detail.xlsx', index=False)
    df_row.to_excel(os.getcwd() + '/wsb_blk01s_detail.xlsx', index=False)
df_row.to_excel(os.getcwd() + '/wsb_blk01s_detail.xlsx', index=False)
    
