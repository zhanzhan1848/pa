from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
import time, random
import os

sess = requests.session()

sess.mount('http://', HTTPAdapter(max_retries=3))
sess.mount('https://', HTTPAdapter(max_retries=3))



headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'}

package_list = ['?search=true&category=507013', '?search=true&category=507012', '?search=true&category=507011', '?search=true&category=507010', '?search=true&category=507009', '?search=true&category=507008', '?search=true&category=507007', '?search=true&category=507006', '?search=true&category=507005', '?search=true&category=507004', '?search=true&category=507003', '?search=true&category=507002', '?search=true&category=507001', '?search=true&category=507114', '?search=true&category=507113', '?search=true&category=507112', '?search=true&category=507111', '?search=true&category=507110', '?search=true&category=507109', '?search=true&category=507108', '?search=true&category=507107', '?search=true&category=507106', '?search=true&category=507105', '?search=true&category=507104', '?search=true&category=507103', '?search=true&category=507102', '?search=true&category=507101', '?search=true&category=507901']

def get_packages():
    global package_list

    try:
        url1 = r"https://hk.digimoncard.com/cardlist/?search=true&category=507102"
        r = sess.get(url1, headers=headers, timeout= 5)
        constents = r.text

        soup = BeautifulSoup(constents, "html.parser")
        tag1 = soup.find(name="div", attrs={"id": "snaviList"})
        for tag2 in tag1.find_all(name="a"):
                package_list.append(str(tag2['href']))
        print(package_list)

    except:
         return

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
            filename = os.path.join(r'C:/Users/27042/Desktop/pa/Pic/dtcg_image', img_name)
            open(filename, 'wb').write(r.content)
            print(filename)
            print('done')
        del r
    except requests.exceptions.RequestException as e:
        print(e)

if __name__ == '__main__':
     #get_packages()
     for p in package_list:
          url2 = "https://hk.digimoncard.com/cardlist/" + p
          print(url2)
          r = sess.get(url2, headers=headers, timeout= 5)
          constents = r.text

          soup = BeautifulSoup(constents, "html.parser")
          image_lists = soup.find(name="div", attrs={"class": "cardlistCol"})
          for src1 in image_lists.find_all(name="a", attrs={"class": "card_img"}):
              image_src = "https://hk.digimoncard.com" + str(src1.find(name="img")['src']).split("..")[1]
              image_name = str(src1.find(name="img")['src']).split("/")[-1]
              download_img(image_src, image_name)
