
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import xlrd
import time
import random
import ssl
import os

#rdexcle = xlrd.open_workbook(r'C:\Users\27042\Desktop\pa\\pokemon_image.xls')
#table = rdexcle.sheet_by_name('Sheet1')

#su = pd.DataFrame()
#src_urls = []

url_main_list = []
url_card_list = []
card_list = []

hangui_dic = {"Normal" : "N", "Rare" : "R", "Super Rare" : "SR", "Gold Rare" : "GR", "Secret Rare" : "SER", "Ultra Rare" : "UR", "Secret Rare(20th)" : "20th SER", "Ultimate Rare" : "UTR",
                "Holographic Rare" : "HR", "Ghost Rare" : "GHR", "10000 SECRET RARE" : "10000 SER", "Collection Rare" : "CR", "Prismatic Secret Rare" : "PSER" , "Premium Gold Rare" : "PGR", 
                "Shattefoil" : "Unknown1", "Starfoil" : "N", "PSE Secret Rare" : "PSER"}

df_ret = pd.DataFrame(columns = ["卡片密码", "卡片种类1", "卡片种类2", "卡片种类3", "日文名", "中文名", "英文名",  "种族", "属性", "星级", "攻击力", "防御力", "卡包", "罕贵度", "效果"])

df_ret_row = { "卡片密码" : "" , "卡片种类1" : "" , "卡片种类2" : "", "卡片种类3" : "" , "日文名" : "", "中文名" : "", "英文名" : "", "种族" : "", "属性" : "", 
              "星级" : "", "攻击力" : "", "防御力" : "", "卡包" : "", "罕贵度" : "", "效果" : ""}


def down_detail(url):
    global df_ret
    global df_ret_row
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'}
    ssl._create_default_https_context = ssl._create_unverified_context
    ret = Request(url, headers = headers)
    res = urlopen(ret)
    constents = res.read()

    soup = BeautifulSoup(constents, "html.parser", from_encoding="utf-8")#utf-8

    tag_count = 0
    tag_detail = {}

    if soup.find(name="div", attrs={"class" : "rd-mark"}) is None:
        for tag in soup.find_all(name = 'div', attrs = {"class":"val el-col-xs-18 el-col-sm-12 el-col-md-14 el-col-sm-pull-8 el-col-md-pull-6"}):
            tag_detail[tag_count] = str(tag.get_text()).strip()
            tag_count += 1
            
        print(tag_detail)
        df_ret_row["中文名"] = tag_detail[0]
        df_ret_row["日文名"] = tag_detail[1]
        df_ret_row["英文名"] = tag_detail[2]
        if(len(str(tag_detail[3]).split("\n")) == 2):
            df_ret_row["卡片种类1"] = str(tag_detail[3]).split("\n")[0]
            df_ret_row["卡片种类2"] = str(tag_detail[3]).split("\n")[1]
            df_ret_row["卡片种类3"] = "-"
    #        print(str(tag_detail[3]).split("\n"))
        if(len(str(tag_detail[3]).split("\n")) == 3):
            df_ret_row["卡片种类1"] = str(tag_detail[3]).split("\n")[0]
            df_ret_row["卡片种类2"] = str(tag_detail[3]).split("\n")[1]
            df_ret_row["卡片种类3"] = str(tag_detail[3]).split("\n")[2]
    #        print(str(tag_detail[3]).split("\n"))

    #    df_ret_row["卡片种类"] = tag_detail[3]
        if (len(tag_detail) > 4):
            df_ret_row["卡片密码"] = tag_detail[4]
        else:
            df_ret_row["卡片密码"] = "-"


        a_count = 0
        a_detail = {}
        if(len(soup.find_all(name = "div", attrs = {"class" : "val el-col-xs-6 el-col-sm-4"})) != 0):
            for a in soup.find_all(name = "div", attrs = {"class" : "val el-col-xs-6 el-col-sm-4"}):
                a_detail[a_count] = str(a.get_text()).strip()
                a_count += 1
            print(a_detail)
            df_ret_row["种族"] = a_detail[0]
            df_ret_row["属性"] = a_detail[1]
            df_ret_row["攻击力"] = a_detail[2]
            if(len(soup.find_all(name="div", attrs={"class" : "val el-col-xs-6 el-col-sm-4 el-col-md-6"})) != 0):
                df_ret_row["星级"] = str(soup.find(name = "div", attrs = {"class" : "val el-col-xs-6 el-col-sm-4 el-col-md-6"}).get_text()).strip()
                df_ret_row["防御力"] = "-"
            else:
                df_ret_row["星级"] = str(soup.find(name = "div", attrs = {"class" : "val el-col-xs-18 el-col-sm-4"}).get_text()).strip()
                df_ret_row["防御力"] = str(soup.find(name = "div", attrs = {"class" : "val el-col-xs-6 el-col-sm-12"}).get_text()).strip()
        else:
            df_ret_row["种族"] = "-"
            df_ret_row["属性"] = "-"
            df_ret_row["攻击力"] = "-"
            df_ret_row["星级"] = "-"
            df_ret_row["防御力"] = "-"

        df_ret_row["效果"] = str(soup.find(name = "div", attrs = {"class" : "val el-col-24 effect"}).get_text()).strip()

        cb_count = 0
        cb_detail = {}
        if soup.find("div", attrs={"class" : "val el-col-xs-18 el-col-sm-20"}) is not None:
            if(len(soup.find_all(name="div", attrs={"class" : "val el-col-xs-18 el-col-sm-20"})) == 1):
                df_ret_row["卡包"] = str(soup.find(name="div", attrs={"class" : "val el-col-xs-18 el-col-sm-20"}).get_text()).strip()
                df_ret_row["罕贵度"] = "-"
                df_ret = df_ret.append(df_ret_row, ignore_index=True)
            else:
                for cb in soup.find_all(name="div", attrs={"class" : "val el-col-xs-18 el-col-sm-20"}):
                    cb_detail[cb_count] = str(cb.get_text()).strip()
                    cb_count += 1
                df_ret_row["卡包"] = cb_detail[1]
                for s in str(cb_detail[0]).split('，'):
                    df_ret_row["罕贵度"] = s
                    df_ret = df_ret.append(df_ret_row, ignore_index=True)
        else:
            df_ret_row["卡包"] = "-"
            df_ret_row["罕贵度"] = "-"
            df_ret = df_ret.append(df_ret_row, ignore_index=True)



    #    df_ret_row["星级"] = str(soup.find(name = "div", attrs = {"class" : "val el-col-xs-18 el-col-sm-4"}).get_text()).strip()
        


    #    df_ret_row["防御力"] = str(soup.find(name = "div", attrs = {"class" : "val el-col-xs-6 el-col-sm-12"}).get_text()).strip()



        # if(soup.find(lambda tag: tag.name=="div" and tag.get('class')==['hidden-xs']) is not None):
        #     if(str(soup.find(lambda tag: tag.name=="div" and tag.get('class')==['hidden-xs']).find(name="div", attrs={"class" : "head el-col-24 text-center"}).get_text()).strip() != "Master Duel 归属卡包"):
        #         card_package_list = soup.find(name = "div", attrs = {"id" : "pack_table"})
        #         if card_package_list is not None:
        #             for i in range(int(len(card_package_list.find_all("td"))/3)):
        #                 df_ret_row["卡包"] = str(card_package_list.find_all(name = "td")[i * 3 + 1].get_text()).strip()
        #                 df_ret_row["罕贵度"] = hangui_dic['{}'.format(str(card_package_list.find_all(name = "td")[i * 3 + 2].get_text()).strip())]
        #                 df_ret = df_ret.append(df_ret_row, ignore_index=True)
        #         else:
        #             df_ret_row["卡包"] = "-"
        #             df_ret_row["罕贵度"] = "-"
        #             df_ret = df_ret.append(df_ret_row, ignore_index=True)
        #     #    df_ret_row.clear()
        #     else:
        #         df_ret_row["卡包"] = "-"
        #         df_ret_row["罕贵度"] = "-"
        #         df_ret = df_ret.append(df_ret_row, ignore_index=True)
        # else:
        #     df_ret_row["卡包"] = "-"
        #     df_ret_row["罕贵度"] = "-"
        #     df_ret = df_ret.append(df_ret_row, ignore_index=True)
        print(df_ret)


#def get_image_url(url):
#    global su
#    global src_urls
#    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'}
#    ret = Request(url, headers = headers)
#    res = urlopen(ret)
#    constents = res.read()

#    soup = BeautifulSoup(constents, "html.parser", from_encoding="iso-8859-1")#utf-8

#    for src in soup.find_all(name = "img", attrs = {"class" : "img-kk"}):
#        src_url = src['src']
#        src_urls.append(src_url)
#    su = su.append(src_urls, ignore_index = True)
#    src_urls.clear()
#    print(su)



if __name__ == '__main__':
    ygo_package = r"C:\Users\27042\Desktop\pa\ygo_package"
#    abc_count = 0
    for ygo_url_file in os.listdir(ygo_package):
        filename = str(ygo_url_file)
        df = pd.read_excel(str(ygo_package + "\\" + ygo_url_file))
        url_main_lists = list(np.array(df.iloc[:].values).flatten())
    #for url in url_main_lists:
    #    url_main_list.append(url)
    #for url2 in url_main_list:
    #    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'}
    #    ret = Request(url2, headers = headers)
    #    res = urlopen(ret)
    #    constents = res.read()

    #    soup = BeautifulSoup(constents, "html.parser", from_encoding="utf-8")#utf-8

    #    soup_main = soup.find(name = "div", attrs = {"class" : "mw-parser-output"})
    #    for tag in soup_main.find_all(name = "a"):
    #        sec_url = tag["href"]
    #        main_url = "https://wiki.biligame.com" + str(sec_url)
    #        card_list.append(main_url)
    #    for a in card_list:
    #        if a not in url_card_list:
    #            url_card_list.append(a)
    #    card_list.clear()
    #    print(url_card_list)
#        print(url_main_lists)
        for url1 in url_main_lists:
            url = url1
            print(url)
            down_detail(url)
#            get_image_url(url)
#            filename = str(df_ret_row["编号"]).split("/")[1].split("-")[0]
#            abc_count += 1
#            if(abc_count == 10):
            df_ret.to_excel(r'C:\Users\27042\Desktop\pa\ygo_detail\ygo_detail.xlsx', index = False)
#                abc_count = 0
            time.sleep(int(format(random.randint(1, 4))))
        url_main_lists.clear()
        df_ret_row.clear()
        #df_ret.to_excel(r'C:\Users\27042\Desktop\pa\ygo_detail\ygo_detail.xlsx', index = False)
        #su.to_excel(r"C:\Users\27042\Desktop\pa\ws_img_url\{}-src-urls.xlsx".format(filename), index = False)
        df_ret.drop(df_ret.index, inplace = True)
        #su.drop(su.index, inplace = True)
        url_card_list.clear()



