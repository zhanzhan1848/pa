from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
import time
import random
import requests
import os
import re
import pandas as pd

sess = requests.Session()
sess.mount('http://', HTTPAdapter(max_retries=3))
sess.mount('https://', HTTPAdapter(max_retries=3))

df_ret = pd.DataFrame(columns = ["卡名", "クラス", "カード種類", "タイプ", "レアリティ", "収録商品", "COST", "攻击力", "HP", "效果", "台词", "画师", "卡片编号"])

df_ret_row = {"卡名" : "", "クラス" : "", "カード種類" : "", "タイプ" : "", "レアリティ" : "", "収録商品" : "", "COST" : "", "攻击力" : "", "HP" : "", 
              "效果" : "", "台词" : "", "画师" : "", "卡片编号" : ""}

header = {
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0'}

def download_detail(url):
    global df_ret
    global df_ret_row
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'}
    try:
        ret = sess.get(url, headers = headers, timeout=5)

        soup = BeautifulSoup(ret.content, "html.parser")

        main_tag = soup.find(name = "div", attrs = {"class" : "txt"})
        c_name = str(main_tag.find(name = "h1", attrs = {"class" : "ttl Sans"}).get_text())
        c_info = main_tag.find(name = "div", attrs = {"class" : "info"})
        c_1 = str(c_info.find_all(name = "dd")[0].get_text())
        c_2 = str(c_info.find_all(name = "dd")[1].get_text())
        c_3 = str(c_info.find_all(name = "dd")[2].get_text())
        c_4 = str(c_info.find_all(name = "dd")[3].get_text())
        c_5 = str(c_info.find_all(name = "dd")[4].get_text())
        c_status = main_tag.find(name = "div", attrs = {"class" : "status"})
        c_cost = str(c_status.find(name = "span", attrs = {"class" : "status-Item status-Item-Cost"}).get_text()[3])
        c_power = str(c_status.find(name = "span", attrs = {"class" : "status-Item status-Item-Power"}).get_text()[3])
        c_hp = str(c_status.find(name = "span", attrs = {"class" : "status-Item status-Item-Hp"}).get_text()[2])
        n1 = len(main_tag.find_all(name = "div", attrs = {"class" : "detail"}))
        if(n1==0):
            c_detail = "-"
        else:
            c_detail = str(main_tag.find(name = "div", attrs = {"class" : "detail"}).find(name = "p"))

        n2 = len(main_tag.find_all(name = "div", attrs = {"class" : "speech"}))
        if(n2 == 0):
            c_speech = "-"
        else:
            c_speech = str(main_tag.find(name = "div", attrs = {"class" : "speech"}).get_text())

        c_ill = main_tag.find(name = "div", attrs = {"class" : "illustrator"})
        painters = len(c_ill.find_all(name = "span", attrs = {"class" : "name"}))
        if(painters == 0):
            c_painter = "-"
            c_num = str(c_ill.find(name = "span", attrs = {"class" : "heading"}).get_text())
        else:
            c_painter = str(c_ill.find(name = "span", attrs = {"class" : "heading"}).get_text())
            c_num = str(c_ill.find(name = "span", attrs = {"class" : "name"}).get_text())

        df_ret_row["卡名"] = c_name
        df_ret_row["クラス"] = c_1
        df_ret_row["カード種類"] = c_2
        df_ret_row["タイプ"] = c_3
        df_ret_row["レアリティ"] = c_4
        df_ret_row["収録商品"] = c_5
        df_ret_row["COST"] = c_cost
        df_ret_row["攻击力"] = c_power
        df_ret_row["HP"] = c_hp
        df_ret_row["效果"] = c_detail
        df_ret_row["台词"] = c_speech
        df_ret_row["画师"] = c_painter
        df_ret_row["卡片编号"] = c_num
        df_ret = df_ret.append(df_ret_row, ignore_index=True)
        df_ret_row.clear()
        print(df_ret)
    except Exception as e:
        print(e)
        return

def download_img(img_url, img_name):
    print(img_url)
    try:
        r = sess.get(img_url, headers = header, stream = True, timeout=5)
        print(r.status_code)
        if r.status_code == 200:
            filename = os.path.join(r'C:\Users\zy\Desktop\pa\pa\Pic\sve_image', img_name)
            open(filename, 'wb').write(r.content)
            print(filename)
            print('done')
        del r
    except Exception as e:
        print(e)
        return

if __name__ == "__main__":
    url = "https://shadowverse-evolve.com/cardlist/cardsearch/?expansion=BP11"
    r = sess.get(url, headers=header, timeout=5)
    #print(r.content)
    max_page = re.findall(r'\d+', str(re.findall(r'var max_page = \d+;', r.content.decode('utf-8'))))
    print(max_page)
    card_url = []
    img_url = []
    uuid = 0
    
    for i in range(int(max_page[0])):
        url1 = "https://shadowverse-evolve.com/cardlist/cardsearch_ex?expansion=BP11&page={}".format(i+1)
        r2 = sess.get(url=url1, timeout=5, cookies=r.cookies)
        soup = BeautifulSoup(r2.content, "html.parser")
        # tag = soup.find(lambda tag: tag.name == 'ul' and tag.get('class') == ['cardlist-Result_List cardlist-Result_List_Gallery'])
        # print(tag)
        # print(soup)
        tag2 = soup.find_all('li')
        for tag3 in tag2:
            card_url.append("https://shadowverse-evolve.com" + tag3.find('a')['href'])
            img_url.append("https://shadowverse-evolve.com" + tag3.find('img')['src'])
        
        for j, k in zip(card_url, img_url):
            download_detail(j)
            download_img(k, k.split('/')[-1])
            uuid += 1
            time.sleep(random.randint(1, 2))
            if uuid % 5 == 0:
                df_ret.to_excel(os.getcwd() + '/sve_detail_bp11.xlsx', index=False)
        df_ret.to_excel(os.getcwd() + '/sve_detail_bp11.xlsx', index=False)
        card_url.clear()
        img_url.clear()
        print(("第{}页".format(str(i+1))).center(50, '*'))
            

    # for img in img_url:
    #     img_name = img.split('/')[-1]
    #     download_img(img, img_name)
    #     time.sleep(random.randint(1, 3))


