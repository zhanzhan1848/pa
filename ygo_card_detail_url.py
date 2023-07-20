from unicodedata import name
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd
import time, random
import json

df_ret = pd.DataFrame(columns = ["地址"])

df_ret_row = {"地址" : ""}

for i in range(1308, 1312):
    url1 = "https://www.ourocg.cn/card/list-5/{}".format(i)

    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'}
    ret = Request(url1, headers = headers)
    res = urlopen(ret)
    constents = res.read()

    soup = BeautifulSoup(constents, "html.parser")

    main_tag = soup.find(name="body")
    sec_tag = main_tag.find_all(name="script")[1]
    s = str(sec_tag).split("window.__STORE__ = ")[1]
    s = s.split(";\n</script>")[0]
    #print(re.findall(r"'href':'(\w*)'", str(s)))
    #print(s)
    sdata = json.loads(s)
    #print(sdata)
    for data in sdata["cards"]:
        print(data['href'])
        df_ret_row["地址"] = data['href']
        print(df_ret_row)
        df_ret = df_ret.append(df_ret_row, ignore_index=True)
        print(df_ret)
        df_ret_row.clear()
    df_ret.to_excel(r'C:/Users/27042/Desktop/pa/ygo_detail_url.xlsx', index = False)
    time.sleep(int(format(random.randint(1, 3))))

df_ret.to_excel(r'C:/Users/27042/Desktop/pa/ygo_detail_url.xlsx', index = False)

    

#https://www.ourocg.cn/card/list-5/1