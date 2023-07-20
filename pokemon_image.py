import os
import requests
import time, random
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter

sess = requests.session()

sess.mount('http://', HTTPAdapter(max_retries=3))
sess.mount('https://', HTTPAdapter(max_retries=3))

header = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1; Win64; WOW64) AppleWebKit/537.36'
        '(KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}


def download_img(img_url, img_name):
    print(img_url)
    r = sess.get(img_url, headers = header, stream = True, timeout=5)
    print(r.status_code)
    if r.status_code == 200:
        filename = os.path.join(r'C:\Users\27042\Desktop\pa\Pic\ptcg_image', img_name)
        open(filename, 'wb').write(r.content)
        print(filename)
        print('done')
    del r

if __name__ == '__main__':
    #image_url = pd.read_csv('', skiprows = 1, names = ['date', 'uid', 'qid', 'url'])
    ##image_url = 'https://ws-tcg.com/wordpress/wp-content/images/cardlist/m/mar_s89/mar_s89_001mr.png'
    ##image_url_a = image_url.iloc[:, :]
    #api_token = ""
    #for index, row in image_url_a.iterrows():
    # url1 = "http://www.pmtcgo.com/database?page=1"
    package_list = ['SWSH12', 'SWSH11', 'PGO', 'SWSH10', 'SWSH9', 'SWSH8', '25TH', 'SWSH7', 'SWSH6', 'SWSH5', 
                    'SWSH45', 'SWSH4', 'SWSH35', 'SWSH3', 'SWSH2', 'SWSH1', 'SWSHP', 'SM12', 'SMA', 'SM115', 'SM11', 'SM10', 
                    'det', 'SM9', 'SM8', 'SM75', 'SM7', 'SM6', 'SM5', 'SM4', 'SM35', 'SM3', 'SM2', 'SM', 'SMP', 'XY12', 'XY11', 
                    'XY10', 'g1', 'XY9', 'XY8', 'XY7', 'XY6', 'DC', 'XY5', 'XY4', 'XY3', 'XY2', 'XY1', 'XY', 'XYP', 'XYA', 'BW11', 
                    'BW10', 'BW9', 'BW8', 'BW7', 'DV', 'BW6', 'BW5', 'BW4', 'BW3', 'BW2', 'BW1', 'BWP', 'COL', 'HGSS4', 'HGSS3', 'HGSS2', 
                    'HGSS1', 'HSP', 'PL4', 'PL3', 'PL2', 'PL1', 'DP7', 'DP6', 'DP5', 'DP4', 'DP3', 'DP2', 'DP1', 'EX16', 'EX15', 'EX14', 'EX13', 
                    'EX12', 'EX11', 'EX10', 'EX9', 'EX8', 'EX7', 'EX6', 'EX5', 'EX4', 'EX3', 'EX2', 'EX1']
    
    for src in package_list:
        for i in range(1, 500):
            img_src = "http://www.pmtcgo.com/img/card/default/{}_{}.png".format(src, i)
            img_name = img_src.split("/")[-1]
            try:
                print(img_src)
                r = sess.get(img_src, headers = header, stream = True, timeout=5)
                print(r.status_code)
                if(r.status_code == 200):
                    filename = os.path.join(r'C:\Users\27042\Desktop\pa\Pic\ptcg_image', img_name)
                    open(filename, 'wb').write(r.content)
                    print(filename)
                    print('done')
                    time.sleep(int(format(random.randint(1, 3))))
                    del r
                else:
                    break;
            except:
                break
            
    
