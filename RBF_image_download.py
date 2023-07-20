from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
import time
import random
import requests
import os

sess = requests.Session()
sess.mount('http://', HTTPAdapter(max_retries=3))
sess.mount('https://', HTTPAdapter(max_retries=3))

def download_img(img_url, img_name):
    print(img_url)
    header = {
       'User-Agent':
       'Mozilla/5.0 (Windows NT 6.1; Win64; WOW64) AppleWebKit/537.36'
       '(KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    try:
        r = sess.get(img_url, headers = header, stream = True)
        print(r.status_code)
        if r.status_code == 200:
            filename = os.path.join(r'C:\Users\27042\Desktop\pa\Pic\rbl_image\HP002B', img_name)
            open(filename, 'wb').write(r.content)
            print(filename)
            print('done')
        del r
    except requests.exceptions.RequestException as e:
        print(e)

if __name__ == "__main__":
    for i in range(1, 73):
        for j in ['', 'S']:
            url = "https://rebirth-fy.com/wordpress/wp-content/images/cardlist/HPB2/HP002B-{}{}.png".format(str(i).zfill(3), j)
            image_name = url.split('-')[-1]
            print(image_name)
            download_img(url, image_name)
            time.sleep(int(format(random.randint(1, 3))))
                

    for i in range(1, 61):
        for j in ['', 'S', 'SNP']:
            url = "https://rebirth-fy.com/wordpress/wp-content/images/cardlist/HPB2/HP002B-P{}{}.png".format(str(i).zfill(2), j)
            image_name = url.split('-')[-1]
            print(image_name)
            download_img(url, image_name)
            time.sleep(int(format(random.randint(1, 3))))

#1 - 19 SP  20 - 38 SU   39 - 57 AU  58 - 76 wi   C 4  PR 1
#url = "https://ws-blau.com/wordpress/wp-content/images/cardlist/A3!/01Ssu/A3!_C-002.png"

