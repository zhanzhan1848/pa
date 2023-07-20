from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import requests
import os
import json
from requests.adapters import HTTPAdapter

sess = requests.session()

sess.mount('http://', HTTPAdapter(max_retries=3))
sess.mount('https://', HTTPAdapter(max_retries=3))

dict1 = {"S": 120, "W": 120, "SE": 50, "WE": 50}

df_ret = pd.DataFrame(columns = ["卡名", "片假名", "编号", "商品区分", "作品区分", "稀有度", "种类", "颜色", "等级", "费用", "战斗力", "灵魂值", "触发标记", "特征", "效果", "台词", "高罕台词"])

df_ret_row = {"卡名" : "", "片假名" : "", "编号" : "", "商品区分" : "", "作品区分" : "" , "稀有度" : "", "种类" : "" , "颜色" : "" , "等级" : "", "费用" : "", 
              "战斗力" : "", "灵魂值" : "", "触发标记" : "", "特征" : "", "效果" : "", "台词" : "", "高罕台词" : ""}

url1 = "https://ws-tcg.com/cardlist/search"

header = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
    }



def get_package_url(index, value):
	data = {
		"_method": "POST",
		"expansion_select": "",
		"title_number_select": "",
		"cmd": "search",
		"keyword": "W106",#str(index) + str(value).zfill(2),
		"keyword_or": "",
		"keyword_not": "",
		"keyword_cardname": 0,
		"keyword_feature": 0,
		"keyword_text": 0,
		"keyword_cardnumber": 1,
		"side": "",
		"title_number": "",
		"expansion_category": "",
		"expansion": "",
		"card_kind": "",
		"level_s": "",
		"level_e": "",
		"power_s": "",
		"power_e": "",
		"color": "",
		"soul_s": "",
		"soul_e": "",
		"cost_s": "",
		"cost_e": "",
		"trigger": "",
		"option_counter": "0",
		"option_clock": "0",
		"show_page_count": 100,
		"show_small": 0,
		"expansion_filter": "",
		"button": "条件を変えて再検索する"
	}
	data = json.dumps(data)

	content = sess.post(url=url1, data=data, headers=header, timeout=5)

	soup = BeautifulSoup(content.text, "html.parser")

	tag = soup.find(name="div", attrs={"class" : "search-result-table-container"})
	url_ext = []
	uuid = 0

	for i in range(1, 5):
		# tag1 = soup.find(lambda tag: tag.name == 'table' and tag.get('class') == ['search-result-table'])
		# tag2 = tag1.find_all(name="td")
		# for tag3 in tag2:
		# 	url_ext.append(tag3.find(name="h4").find(name="a")['href'])

		content1 = sess.get(url=content.url, params={'page': i}, headers=header, timeout=5)
		soup1 = BeautifulSoup(content1.text, "html.parser")
		tag5 = soup1.find(lambda tag: tag.name == 'table' and tag.get('class') == ['search-result-table'])
		tag6 = tag5.find_all(name="td")
		for tag7 in tag6:
			url_ext.append(tag7.find(name="h4").find(name="a")['href'])
	
	#print(len(url_ext))
		for ext in url_ext:
		# 	print(tag4)
		# print(tag2)

		# p = tag.find(name="a")
		# m = p.find(name="img")
		# for j in range(1, 170):
		# 	for k in ["SSP", "SP", "SEC", "S", "R", ""]:
			# detail_url = r"https://ws-tcg.com" + p['href'].split("-")[0] + "-" + str(j).zfill(3) + k + r"&l"
			detail_url = r"https://ws-tcg.com" + ext
			print(detail_url)
			down_detail(detail_url)
			time.sleep(int(format(random.randint(1, 2))))
			uuid += 1
			if uuid % 5 == 0:
				df_ret.to_excel(os.getcwd() + "/ws_detail_W106.xlsx", index = False)
		df_ret.to_excel(os.getcwd() + "/ws_detail_W106.xlsx", index = False)
		url_ext.clear()
		print("*******************   This  is page : (   %d  )  **********************" % i)



def down_detail(url):
	global df_ret
	global df_ret_row
	ret = sess.get(url, headers = header, timeout=5)
	constents = ret.text
	soup = BeautifulSoup(constents, "html.parser")#utf-8
	tag = soup.find(lambda tag: tag.name == 'div' and tag.get('class') == ['card-detail'])
	try:
		tag_detail = tag.find_all(name="td")
		#print(tag.find_all(name="td"))
		image_url = "https://ws-tcg.com" + tag_detail[0].find(name="img")['src']
		image_name = str(image_url).split("_")[-2] + "_" + str(image_url).split("_")[-1]
		if not download_img(image_url, image_name):
			return
		df_ret_row["卡名"] = tag_detail[1].contents[0]
		df_ret_row["片假名"] = tag_detail[1].find(name="span", attrs={'class':'kana'}).get_text()
		df_ret_row["编号"] = tag_detail[2].get_text()
		df_ret_row["商品区分"] = tag_detail[3].get_text()
		df_ret_row["作品区分"] = tag_detail[4].get_text()
		df_ret_row["稀有度"] = tag_detail[6].get_text()
		df_ret_row["种类"] = tag_detail[8].get_text()
		df_ret_row["颜色"] = str(tag_detail[9].find(name="img")['src']).split("/")[-1].split(".")[0]
		df_ret_row["等级"] = tag_detail[10].get_text()
		df_ret_row["费用"] = tag_detail[11].get_text()
		df_ret_row["战斗力"] = tag_detail[12].get_text()
		df_ret_row["灵魂值"] = len(tag_detail[13].find_all(name="img"))
		df_ret_row["触发标记"] = tag_detail[14].get_text()
		df_ret_row["特征"] = tag_detail[15].get_text()
		df_ret_row["效果"] = tag_detail[16].get_text()
		df_ret_row["台词"] = tag_detail[17].get_text()
		df_ret_row["高罕台词"] = "-"

		df_ret = df_ret.append(df_ret_row, ignore_index=True)
		df_ret_row.clear()
		print(df_ret)
	except:
		return


def download_img(img_url, img_name):
	print(img_url)
	r = sess.get(img_url, headers = header, stream = True, timeout=5)
	print(r.status_code)
	if r.status_code == 200:
		filename = os.path.join(os.getcwd() + '/Pic/ws_image/W106', img_name)
		open(filename, 'wb').write(r.content)
		print(filename)
		print('done')
		return True
	else:
		return False

if __name__ == '__main__':
	# for index in dict1:
	# 	for i in range(1, dict1[index]):
	# 		if index == 'W' and i == 102:
	# 			get_package_url(index, i)
	# 		df_ret.to_excel(r"C:/Users/27042/Desktop/pa/ws_detail_w102.xlsx", index = False)
	# 	df_ret.to_excel(r"C:/Users/27042/Desktop/pa/ws_detail_w102.xlsx", index = False)
	# df_ret.to_excel(r"C:/Users/27042/Desktop/pa/ws_detail_w102.xlsx", index = False)
	get_package_url("W", 105)
	df_ret.to_excel(os.getcwd() + "/ws_detail_W106.xlsx", index = False)
