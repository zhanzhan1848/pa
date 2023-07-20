import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time, random
from requests.adapters import HTTPAdapter
import xlsxwriter

sess = requests.session()

sess.mount('http://', HTTPAdapter(max_retries=3))
sess.mount('https://', HTTPAdapter(max_retries=3))

df_ret = pd.DataFrame(columns=['编号', '中文名', '日文名', '属性', '发售日', '比例', '制作', '系列', '原型', '角色', '作品', '尺寸', '材质'])

df_row = {'编号' : '', '中文名' : '', '日文名' : '', '属性' : '', '发售日' : '', '比例' : '', '制作' : '', '系列' : '', '原型' : '', '角色' : '', '作品' : '', '尺寸' : '', '材质' : ''}

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
            if len(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})) >0:
                if "发售" in str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[3].get_text()).strip():
                    if "," in str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[3].find(name = 'p').get_text()).strip():
                        if "/" in str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[3].find(name = 'p').get_text()).strip():
                            if "年" in str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[3].find(name = 'p').get_text()).strip().split("/")[0].strip():
                                if int(str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[3].find(name = 'p').get_text()).strip().split("/")[0].strip().split("年")[0].strip()) < 2017:
                                    return
                            elif int(str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[3].find(name = 'p').get_text()).strip().split("/")[0].strip()) < 2017:
                                return
                        elif "年" in str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[3].find(name = 'p').get_text()).strip():
                            if int(str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[3].find(name = 'p').get_text()).strip().split("年")[0].strip()) < 2017:
                                return
                    elif "年" in str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[3].find(name = 'p').get_text()).strip():
                        if int(str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[3].find(name = 'p').get_text()).strip().split("年")[0].strip()) < 2017:
                            return
                else:
                    return
            else:
                return

            if len(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})) == 12:
                df_row['编号'] = str(url).split('/')[-1]
                df_row['中文名'] = str(soup.find(name = "div", attrs={'class' : 'hpoi-ibox-title'}).get_text()).split("：")[1].strip().replace('=|#|@|&', '')
                df_row['日文名'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[0].find(name = 'p').get_text()).strip().replace('=|#|@|&', '')
                df_row['属性'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[1].find(name = 'p').get_text()).strip()
                df_row['发售日'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[3].find(name = 'p').get_text()).strip()
                df_row['比例'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[4].find(name = 'p').get_text()).strip()
                df_row['制作'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[5].find(name = 'p').get_text()).strip()
                df_row['系列'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[6].find(name = 'p').get_text()).strip()
                df_row['原型'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[7].find(name = 'p').get_text()).strip()
                df_row['作品'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[8].find(name = 'p').get_text()).strip()
                df_row['尺寸'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[9].find(name = 'p').get_text()).strip()
                df_row['材质'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[10].find(name = 'p').get_text()).strip()
                df_row['角色'] = '-'
            elif len(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})) == 9:
                df_row['编号'] = str(url).split('/')[-1]
                df_row['中文名'] = str(soup.find(name = "div", attrs={'class' : 'hpoi-ibox-title'}).get_text()).split("：")[1].strip().replace('=|#|@|&', '')
                df_row['日文名'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[0].find(name = 'p').get_text()).strip().replace('=|#|@|&', '')
                df_row['属性'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[1].find(name = 'p').get_text()).strip()
                df_row['发售日'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[3].find(name = 'p').get_text()).strip()
                df_row['比例'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[4].find(name = 'p').get_text()).strip()
                df_row['制作'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[5].find(name = 'p').get_text()).strip()
                df_row['系列'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[6].find(name = 'p').get_text()).strip()
                df_row['原型'] = '-'
                df_row['作品'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[7].find(name = 'p').get_text()).strip()
                df_row['尺寸'] = '-'
                df_row['材质'] = '-'
                df_row['角色'] = '-'
            elif len(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})) == 10:
                df_row['编号'] = str(url).split('/')[-1]
                df_row['中文名'] = str(soup.find(name = "div", attrs={'class' : 'hpoi-ibox-title'}).get_text()).split("：")[1].strip().replace('=|#|@|&', '')
                df_row['日文名'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[0].find(name = 'p').get_text()).strip().replace('=|#|@|&', '')
                df_row['属性'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[1].find(name = 'p').get_text()).strip()
                df_row['发售日'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[3].find(name = 'p').get_text()).strip()
                df_row['比例'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[4].find(name = 'p').get_text()).strip()
                df_row['制作'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[5].find(name = 'p').get_text()).strip()
                df_row['系列'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[6].find(name = 'p').get_text()).strip()
                df_row['原型'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[7].find(name = 'p').get_text()).strip()
                df_row['作品'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[8].find(name = 'p').get_text()).strip()
                df_row['尺寸'] = '-'
                df_row['材质'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[9].find(name = 'p').get_text()).strip()
                df_row['角色'] = '-'
            elif len(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})) == 11:
                df_row['编号'] = str(url).split('/')[-1]
                df_row['中文名'] = str(soup.find(name = "div", attrs={'class' : 'hpoi-ibox-title'}).get_text()).split("：")[1].strip().replace('=|#|@|&', '')
                df_row['日文名'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[0].find(name = 'p').get_text()).strip().replace('=|#|@|&', '')
                df_row['属性'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[1].find(name = 'p').get_text()).strip()
                df_row['发售日'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[3].find(name = 'p').get_text()).strip()
                df_row['比例'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[4].find(name = 'p').get_text()).strip()
                df_row['制作'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[5].find(name = 'p').get_text()).strip()
                df_row['系列'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[6].find(name = 'p').get_text()).strip()
                df_row['原型'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[7].find(name = 'p').get_text()).strip()
                df_row['作品'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[8].find(name = 'p').get_text()).strip()
                df_row['尺寸'] = '-'
                df_row['材质'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[9].find(name = 'p').get_text()).strip()
                df_row['角色'] = '-'
            elif len(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})) == 8:
                df_row['编号'] = str(url).split('/')[-1]
                df_row['中文名'] = str(soup.find(name = "div", attrs={'class' : 'hpoi-ibox-title'}).get_text()).split("：")[1].strip().replace('=|#|@|&', '')
                df_row['日文名'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[0].find(name = 'p').get_text()).strip().replace('=|#|@|&', '')
                df_row['属性'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[1].find(name = 'p').get_text()).strip()
                df_row['发售日'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[3].find(name = 'p').get_text()).strip()
                df_row['比例'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[4].find(name = 'p').get_text()).strip()
                df_row['制作'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[5].find(name = 'p').get_text()).strip()
                df_row['系列'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[6].find(name = 'p').get_text()).strip()
                df_row['原型'] = '-'
                df_row['作品'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[7].find(name = 'p').get_text()).strip()
                df_row['尺寸'] = '-'
                df_row['材质'] = '-'
                df_row['角色'] = '-'
            elif len(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})) >= 14:
                df_row['编号'] = str(url).split('/')[-1]
                df_row['中文名'] = str(soup.find(name = "div", attrs={'class' : 'hpoi-ibox-title'}).get_text()).split("：")[1].strip().replace('=|#|@|&', '')
                df_row['日文名'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[0].find(name = 'p').get_text()).strip().replace('=|#|@|&', '')
                df_row['属性'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[1].find(name = 'p').get_text()).strip()
                df_row['发售日'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[3].find(name = 'p').get_text()).strip()
                df_row['比例'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[4].find(name = 'p').get_text()).strip()
                df_row['制作'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[5].find(name = 'p').get_text()).strip()
                df_row['系列'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[7].find(name = 'p').get_text()).strip()
                df_row['原型'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[8].find(name = 'p').get_text()).strip()
                df_row['作品'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[10].find(name = 'p').get_text()).strip()
                df_row['尺寸'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[11].find(name = 'p').get_text()).strip()
                df_row['材质'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[12].find(name = 'p').get_text()).strip()
                df_row['角色'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[9].find(name = 'p').get_text()).strip()
            elif len(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})) == 13:
                df_row['编号'] = str(url).split('/')[-1]
                df_row['中文名'] = str(soup.find(name = "div", attrs={'class' : 'hpoi-ibox-title'}).get_text()).split("：")[1].strip().replace('=|#|@|&', '')
                df_row['日文名'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[0].find(name = 'p').get_text()).strip().replace('=|#|@|&', '')
                df_row['属性'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[1].find(name = 'p').get_text()).strip()
                df_row['发售日'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[3].find(name = 'p').get_text()).strip()
                df_row['比例'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[4].find(name = 'p').get_text()).strip()
                df_row['制作'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[5].find(name = 'p').get_text()).strip()
                df_row['系列'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[7].find(name = 'p').get_text()).strip()
                df_row['原型'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[6].find(name = 'p').get_text()).strip()
                df_row['作品'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[9].find(name = 'p').get_text()).strip()
                df_row['尺寸'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[10].find(name = 'p').get_text()).strip()
                df_row['材质'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[11].find(name = 'p').get_text()).strip()
                df_row['角色'] = str(soup.find_all(name="div", attrs={'class' : 'hpoi-infoList-item'})[8].find(name = 'p').get_text()).strip()
            else:
                return

            try:
                imgs_urls = soup.find_all(name="div", attrs={'class' : 'container'})[1].find(name='div', attrs={'class' : 'swiper-wrapper'}).find_all(name='img')
                filename = 'C:/Users/27042/Desktop/pa/Pic/hpoi_image/' + str(df_row['编号'])
                if not os.path.exists(filename):
                    os.mkdir(filename)
                for iurl in imgs_urls:
                    img_url = iurl['src']
                    img_name = str(img_url).split('=')[-1] + '.png'
                    if 'date=' not in img_url:
                        continue
                    download_img(img_url, img_name, filename)
                    time.sleep(int(format(random.randint(1, 3))))
            except AttributeError as e:
                print(e)
                pass
            df_ret = df_ret.append(df_row, ignore_index=True)
            df_row.clear()
            print(df_ret)
        if(r.status_code==404):
            print(df_ret)
    except requests.exceptions.RequestException as e:
        print(e)
        return

def download_img(img_url, img_name, filename):
    print(img_url)
    header = {
       'User-Agent':
       'Mozilla/5.0 (Windows NT 6.1; Win64; WOW64) AppleWebKit/537.36'
       '(KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    try:
        r = sess.get(img_url, headers = header, stream = True, timeout= 5)
        print(r.status_code)
        if r.status_code == 200:
            filename_all = os.path.join(filename, img_name)
            open(filename_all, 'wb').write(r.content)
            print(filename_all)
            print('done')
        del r
    except requests.exceptions.RequestException as e:
        print(e)

if __name__ == "__main__":
    for i in range(78332, 80850):
        url = 'https://www.hpoi.net/hobby/{}'.format(i)
        print(url)
        down_detail(url)
        filename = "hpoi_base"
        time.sleep(int(format(random.randint(1, 6))))
        df_ret.to_excel(r'C:\Users\27042\Desktop\pa\{}.xlsx'.format(filename), index = False)
        if i % 50 == 1:
            df_ret.to_excel(r'C:\Users\27042\Desktop\pa\{}_back_up.xlsx'.format(filename), index = False)