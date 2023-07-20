import os
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

df_row = pd.DataFrame(columns=["cardnum", "game", "packages", "set_ch_name", "set1", "set2", "set", "password", "type1", "type2", "type3", "name1", "name2", "name3", "card_num", 
                               "type4", "type5", "color", "atrtrib", "cost", "power", "hp", "rarity", "effect"])

df_row_now = {"cardnum" : '', "game" : '航海王', "packages" : '', "set_ch_name" : '', "set1": '', "set2" : '', "set" : '', 
              "password" : '', "type1" : '', "type2" : '', "type3" : '', "name1" : '', "name2" : '', "name3" : '', "card_num" : '', 
                               "type4" : '无', "type5" : '无', "color" : '', "atrtrib" : '', "cost" : '无', "power" : '', "hp" : '', "rarity" : '', "effect" : ''}

header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
}

url = "https://onepieceserve.windoent.com/cardList/cardlist/weblist?cardName=&cardColor=&cardType=&cardCartograph=&limit=500&page=1"

r = requests.get(url, headers=header)
card_index = 200000

for num in json.loads(r.text)['page']['list']:
    print(num['id'])
    url1 = "https://onepieceserve.windoent.com/cardList/cardlist/webInfo/{}".format(num['id'])
    r1 = requests.get(url1, headers=header)
    print(json.loads(r1.text))
    info = json.loads(r1.text)['info']
    df_row_now['cardnum'] = str(card_index)
    df_row_now['game'] = '航海王'
    df_row_now['set_ch_name'] = info['cardOfferType']
    df_row_now['set'] = info['cardNumber'].split('-')[0]
    df_row_now['set1'] = info['cardNumber'].split('-')[0]
    df_row_now['set2'] = info['cardNumber'].split('-')[0]
    df_row_now["packages"] = info['cardOfferType']
    df_row_now["password"] = info['cardNumber']
    df_row_now["type1"] = info['cardType']
    df_row_now["type2"] = info['cardCartograph']
    df_row_now["type3"] = info['cardFeatures']
    df_row_now["type4"] = '无'
    df_row_now["type5"] = '无'
    df_row_now['cost'] = '无'
    df_row_now["name1"] = info['cardName']
    df_row_now["name2"] = info['cardName']
    df_row_now["name3"] = info['cardName']
    df_row_now["card_num"] = info['cardNumber']
    df_row_now["color"] = info['cardColor']
    df_row_now["atrtrib"] = info['cardAttribute']
    df_row_now["power"] = info['cardPower']
    df_row_now["hp"] = info['cardLife']
    df_row_now["rarity"] = info['cardRarity']
    df_row_now["effect"] = info['cardTextDesc']
    df_row = df_row.append(df_row_now, ignore_index=True)
    card_index += 1
    print(df_row)
    df_row_now.clear()
    if(card_index > 200000 and card_index % 5 == 0):
        df_row.to_excel(os.getcwd() + '/opcg_detail.xlsx', index=False)
df_row.to_excel(os.getcwd() + '/opcg_detail.xlsx', index=False)