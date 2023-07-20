import requests
#import os

headers={
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
}

urla = "https://www.db.yugioh-card.com/yugiohdb/get_image.action?type=1&osplang=1&cid=17757&ciid=1&enc=ZijxzX84efFuJhD7o9n2JQ&app=tournament&request_locale=ja"

r = requests.get(urla, headers=headers)


with open('C:/Users/27042/Desktop/pa/Pic/ygo_image/1.png', 'wb') as f:
    f.write(r.content)


#https://www.db.yugioh-card.com/yugiohdb/get_image.action?type=1&osplang=1&cid=17757&ciid=1&enc=ZijxzX84efFuJhD7o9n2JQ&app=tournament&request_locale=ja
#start cid=4007 end cid=17835


#http://cdn.jihuanshe.com/13457.jpg
#start 1 end 13510