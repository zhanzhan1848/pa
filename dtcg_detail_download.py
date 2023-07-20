from fileinput import filename
import requests
import json
import pandas as pd

df_ret = pd.DataFrame(columns = ['中文名', '系列', '卡包', '稀有度', '编号', '种类', '颜色', 'COST', '登场COST', '类型', 'DP', '等级', '属性', '形态', '进化条件', '效果', '进化源效果', '安防效果'])

df_ret_now = {'中文名' : '', '系列' : '', '卡包' : '', '稀有度' : '', '编号' : '', '种类' : '', '颜色' : '', 'COST' : '', '登场COST' : '', '类型' : '', 'DP' : '', '等级' : '', '属性' : '', '形态' : '', '进化条件' : '', '效果' : '', '进化源效果' : '', '安防效果' : ''}

url = "https://dtcgweb-api.digimoncard.cn/gamecard/gamecardmanager/weblist?page=1&limit=1560&name=&state=0&cardGroup=&rareDegree=&belongsType=&cardLevel=&form=&attribute=&type=&color=&envolutionEffect=&safeEffect=&parallCard=&keyEffect="

headers = {
       'User-Agent':
       'Mozilla/5.0 (Windows NT 6.1; Win64; WOW64) AppleWebKit/537.36'
       '(KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

# data = {
#     "scheme": "https",
#     "host": "dtcgweb-api.digimoncard.cn",
#     "filename": "/gamecard/gamecardmanager/weblist",
#     "query": {
#         "page": "1",
#         "limit": "",
#         "name": "",
#         "state": "0",
#         "cardGroup": "",
#         "rareDegree": "",
#         "belongsType": "",
#         "cardLevel": "",
#         "form": "",
#         "attribute": "",
#         "type": "",
#         "color": "",
#         "envolutionEffect": "",
#         "safeEffect": "",
#         "parallCard": "",
#         "keyEffect": ""
#     }
# }

content1 = requests.get(url, headers=headers)
print(len(content1.json()['page']['list']))

sfilename = "dtcg_detail"

for i in range(content1.json()['page']['totalCount']):
    df_ret_now['中文名'] = content1.json()['page']['list'][i]['name']
    df_ret_now['系列'] = content1.json()['page']['list'][i]['cardGroup'].split('-')[0]
    df_ret_now['卡包'] = content1.json()['page']['list'][i]['cardGroup']
    df_ret_now['编号'] = content1.json()['page']['list'][i]['model']
    df_ret_now['稀有度'] = content1.json()['page']['list'][i]['rareDegree'].split('（')[1].split('）')[0]
    df_ret_now['形态'] = content1.json()['page']['list'][i]['form']
    df_ret_now['属性'] = content1.json()['page']['list'][i]['attribute']
    df_ret_now['颜色'] = content1.json()['page']['list'][i]['color']
    df_ret_now['种类'] = content1.json()['page']['list'][i]['belongsType']
    df_ret_now['登场COST'] = content1.json()['page']['list'][i]['entryConsumeValue']
    df_ret_now['DP'] = content1.json()['page']['list'][i]['dp']
    df_ret_now['进化条件'] = content1.json()['page']['list'][i]['envolutionConsumeOne']
    df_ret_now['效果'] = content1.json()['page']['list'][i]['effect']
    df_ret_now['进化源效果'] = content1.json()['page']['list'][i]['envolutionEffect']
    df_ret_now['安防效果'] = content1.json()['page']['list'][i]['safeEffect']
    df_ret_now['等级'] = content1.json()['page']['list'][i]['cardLevel']
    df_ret_now['COST'] = content1.json()['page']['list'][i]['envolutionConsumeTwo']
    df_ret_now['类型'] = content1.json()['page']['list'][i]['type']
    print(df_ret_now)
    df_ret = df_ret.append(df_ret_now, ignore_index=True)
    df_ret_now.clear()
df_ret.to_excel(r'C:\Users\27042\Desktop\pa\{}.xlsx'.format(sfilename), index = False)