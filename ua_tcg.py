from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import requests
import os
import json
from requests.adapters import HTTPAdapter

def download_img(img_url, img_name, package_name):
	print(img_url)
	r = sess.get(img_url, headers = header, stream = True, timeout=5)
	print(r.status_code)
	if r.status_code == 200:
		if not os.path.exists(os.path.join(os.getcwd() + '/Pic/ua_image/{}'.format(package_name))):
			os.mkdir(os.path.join(os.getcwd() + '/Pic/ua_image/{}'.format(package_name)))
		filename = os.path.join(os.getcwd() + '/Pic/ua_image/{}'.format(package_name), img_name)
		open(filename, 'wb').write(r.content)
		print(filename)
		print('done')
		return True
	else:
		return False

sess = requests.session()

sess.mount('http://', HTTPAdapter(max_retries=3))
sess.mount('https://', HTTPAdapter(max_retries=3))

base_url = "https://unionarena-tcg.com"

post_url = "https://unionarena-tcg.com/jp/cardlist/index.php?search=true"
post_data = {
    "freewords": '',
    "selectTitle": "",
    "needEnergy_min": "",
    "needEnergy_max": "",
    "bp_min": "",
    "bp_max": "",
    "keyeffect": "",
    "triggerEffectType": "",
    "attribute": "",
    "series": "570118",
    "parallelFlag": "on"
}

post_data2 = "freewords=&selectTitle=%E5%8B%9D%E5%88%A9%E3%81%AE%E5%A5%B3%E7%A5%9E%EF%BC%9ANIKKE&needEnergy_min=&needEnergy_max=&bp_min=&bp_max=&keyeffect=&triggerEffectType=&attribute=&series=&parallelFlag=on"

header = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
    }

if __name__ == '__main__':
	package_name = "UA18BT"
	data = json.dumps(post_data)
	content = sess.post(url=post_url, data=post_data2, headers=header, timeout=5)
	soup1 = BeautifulSoup(content.text, "html.parser")
	tag5 = soup1.find(name="div", attrs={"class" : "cardlistWrap"})
	tag6 = tag5.find_all(name="li", attrs={"class" : "cardImgCol"})
	for img_src in tag6:
		img_url = base_url + img_src.find(name='img')['data-src']
		download_img(img_url=img_url, img_name=img_url.split("/")[-1].split("?")[0], package_name=package_name)