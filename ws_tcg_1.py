# coding = utf-8
from tkinter import image_names
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import requests
import os
from requests.adapters import HTTPAdapter

sess = requests.session()

sess.mount('http://', HTTPAdapter(max_retries=3))
sess.mount('https://', HTTPAdapter(max_retries=3))

df_ret = pd.DataFrame(columns = ["卡名", "编号"])

df_ret_row = {"卡名" : "", "编号" : ""}

def down_detail(url):
    global df_ret
    global df_ret_row
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'}
    # ret = Request(url, headers = headers)
    # res = urlopen(ret)
    # constents = res.read()
    try:
        r = sess.get(url, headers=headers, timeout= 5)
        if(r.status_code==200):
            constents = r.text

            soup = BeautifulSoup(constents, "html.parser")

            a_count = 0
            a_detail = {}
            for tag in soup.find_all(name = 'td', attrs={'colspan' : '3'}):
                a_detail[a_count] = str(tag.find(text=True).get_text()).strip()
                a_count += 1
                if a_count > 1:
                    break

            df_ret_row["卡名"] = str(a_detail[0])
            df_ret_row["编号"] = a_detail[1]
            df_ret = df_ret.append(df_ret_row, ignore_index=True)
            df_ret_row.clear()
            print(df_ret)
        if(r.status_code==404):
            print(df_ret)
    except requests.exceptions.RequestException as e:
        print(e)
    #c_detail = main_tag.find(name = "div", attrs = {"class" : "detail"}).find(name = "p").find(name = "br")
    #n3 = len(c_detail.find_all(name = "img"))
    #icon_name = c_detail.find(name = "img")["alt"]
    #print(main_tag)
    #print(c_cost)
    #print(icon_name)
   # print(n3)


def download_img(img_url, img_name):
    print(img_url)
    header = {
       'User-Agent':
       'Mozilla/5.0 (Windows NT 6.1; Win64; WOW64) AppleWebKit/537.36'
       '(KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    try:
        r = sess.get(img_url, headers = header, stream = True, timeout= 5)
        print(r.status_code)
        if r.status_code == 200:
            filename = os.path.join(r'C:\Users\27042\Desktop\pa\Pic\ws_image\S103_T', img_name)
            open(filename, 'wb').write(r.content)
            print(filename)
            print('done')
        del r
    except requests.exceptions.RequestException as e:
        print(e)

if __name__ == '__main__':
    #for i in range(1, 257):
    #    url = r"http://www.pmtcgo.com/card/SWSH8_{}".format(i)
    #    filename = str(url).split("/")[-1].split("_")[0]
    #    print(url)
    #    down_detail(url)
    #    time.sleep(int(format(random.randint(1, 3))))
    #df_ret.to_excel(r'C:\Users\27042\Desktop\pa\pokemon_detail_{}.xlsx'.format(filename), index = False)
    #'SP', 're', 'Sre', 'S', 'WR', 'WRre', 'a', 'b', 'c', 'SPre', 'SWR', ''
    for i in ['SP', 'R', '']:#'PXR', 'SSP', 'SP', 'S', '', 'a',    'KSC',  
        for j in range(1, 21):
            url = r"https://ws-tcg.com/cardlist/?cardno=ARI/S103-T{:02d}{}&l".format(j, i)
            img_url = r"https://ws-tcg.com/wordpress/wp-content/images/cardlist/a/ari_s103/ari_s103_t{:02d}{}.png".format(j, i.lower())
            
            print(str(j).zfill(3) + i)
            if sess.get(img_url, timeout=5).status_code == 403:
                continue
            filename = "ws_S103_T_detail"
            img_name = 'S103_T_{:03d}{}.png'.format(j, i.lower())
            down_detail(url)
            download_img(img_url, img_name)
            time.sleep(int(format(random.randint(1, 3))))
            if(j%5==1):
                df_ret.to_excel(r'C:\Users\27042\Desktop\pa\{}.xlsx'.format(filename), index = False)
    #     df_ret.to_excel(r'C:\Users\27042\Desktop\pa\{}.xlsx'.format(filename), index = False)
    #     for k in range(1, 20):
        # for k in range(1, 13):
        #     url = r"https://ws-tcg.com/cardlist/?cardno=PXR/S94-P{:02d}{}&l".format(k, i)
        #     img_url = r"https://ws-tcg.com/wordpress/wp-content/images/cardlist/r/rsl_s98/rsl_s98_p{:02d}{}.png".format(k,i.lower())
        #     filename = "ws_SW_S49_detail"
        #     img_name = 'S98_P{:02d}{}.png'.format(k, i.lower())
        #     down_detail(url)
        #     download_img(img_url, img_name)
        #     time.sleep(int(format(random.randint(1, 3))))
        #     if(k%5==1):
        #         df_ret.to_excel(r'C:\Users\27042\Desktop\pa\{}.xlsx'.format(filename), index = False)
        df_ret.to_excel(r'C:\Users\27042\Desktop\pa\{}.xlsx'.format(filename), index = False)
    df_ret.to_excel(r'C:\Users\27042\Desktop\pa\{}.xlsx'.format(filename), index = False)