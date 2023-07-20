import requests
import re
import json
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup

pattern = re.compile(r"\"masterUrl\": \"(.*)\",")
url = 'https://www.xiaohongshu.com/explore/'

header = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }

cookiesss = {
		"a1": "18678781850uw716dkbqqw4rej0conbwv9dd8ghq150000345244",
		"extra_exp_ids": "yamcha_0327_exp,h5_1208_exp3,ques_exp1",
		"extra_exp_ids.sig": "w9AsUUGxef90M-4Z5VfjRwwhB2K939rTZnKSUXm2_EI",
		"gid": "yYKWYWYydqhYyYKWYWYyYjkx287EWyKfTDAAfAyE4FdV8f28SlIDEY888q42J448WJK0JDJd",
		"gid.sign": "izS0YGUSyKrJ5/kIF659G3HWBCU=",
		"gid.ss": "gSMQ9UOnDuZwH2oRGJG6BW6e4grs67TaYpnrW+8Wmd0vOdKR+LlC0kHAgUXNnXgo",
		"sec_poison_id": "cd074885-6291-4221-b893-459abb83c64a",
		"timestamp2": "1669901114066a133c88918be4815ce034a525379e717d4075ce811ee5d64a9",
		"timestamp2.sig": "Jx-zQ8pTZvMBE7IxotbetOnqGDZHV8kLSQgqhphQhdk",
		"web_session": "030037a4c6b53a05012202a78d244aba1b8568",
		"webBuild": "2.0.3",
		"webId": "0d21a6d4c7dabf73f559e87af3637e82",
		"websectiga": "f3d8eaee8a8c63016320d94a1bd00562d516a5417bc43a032a80cbf70f07d5c0",
		"xhsTracker": "url=explore&xhsshare=CopyLink",
		"xhsTracker.sig": "wmLdXV__wbETiz1qUgqoiY8swj2zGxC5B-xOV9HIhWg",
		"xhsTrackerId": "89d39794-be8a-4180-9907-0d15f3bdc55a",
		"xhsTrackerId.sig": "LcQQfDU2CgJXdKu6SVbblhSLmJNxsQ5ybYsMXMad7RQ",
		"xsecappid": "xhs-pc-web"
}

sess = requests.session()

sess.mount('http://', HTTPAdapter(max_retries=3))
sess.mount('https://', HTTPAdapter(max_retries=3))


c1 = sess.get("http://xhslink.com/B5wqop", headers=header)

url2 = url + str(re.findall('/explore/(.*)?app',c1.url)[0])
c2 = sess.get(url2, headers=header, cookies=cookiesss)

soup = BeautifulSoup(c2.text, "html.parser")

tag1 = soup.find_all('script')[7]
f = str(tag1).split("__=")[1].split("</script>")[0]
print(type(f))
b = f.replace("undefined", "false")
c = json.loads(b)
print(c["note"]["note"]["video"]["media"]["stream"]["h264"][0]["masterUrl"])




#{"user":{"loggedIn":false,"activated":false,"userInfo":{},"follow":[],"userPageData":{},"activeTabKey":0,"notes":[[],[],[]],"isFetchingNotes":[false,false,false],"tabScrollTop":[0,0,0],"userFetchingStatus":undefined,"bannedInfo":{"code":0,"showAlert":false,"reason":""}},"login":{"from":"","showLogin":false,"agreed":false,"showTooltip":false,"loginData":{"phone":"","authCode":""},"errors":{"phone":"","authCode":""},"qrData":{"backend":{"qrId":"","code":""},"image":"","status":"un_scanned"}},"global":{"supportWebp":true,"serverTime":1680795784062},"layout":{"layoutInfoReady":false,"columns":6,"gap":{"vertical":16,"horizontal":32},"columnWidth":0,"showSideBar":true},"search":{"state":"auto","searchContext":{"keyword":"","page":1,"pageSize":20,"searchId":"","sort":"general","noteType":0},"feeds":[],"searchValue":""},"note":{"prevRouteData":{},"prevRoute":"Empty","note":{"noteId":"62a70ac9000000001b035550","imageList":[{"url":"https:\u002F\u002Fsns-img-qc.xhscdn.com\u002Fd51d9183-279c-11fc-bc72-808c5409fc91","traceId":"01026d016jqnz8kfs7b0112lrcb06ftkzm","fileId":"d51d9183-279c-11fc-bc72-808c5409fc91","height":1920,"width":1080}],"video":{"capa":{"duration":25},"consumer":{"originVideoKey":"pre_post\u002F01026d016jqnz8kfs7b0212kuuv0iowrzm"},"media":{"videoId":135854602958128670,"video":{"bizName":110,"bizId":"279969791621420368","duration":25,"hdrType":0,"drmType":0,"streamTypes":[259]},"stream":{"h264":[{"width":720,"audioBitrate":64249,"hdrType":0,"vmaf":-1,"defaultStream":0,"masterUrl":"http:\u002F\u002Fsns-video-qc.xhscdn.com\u002Fpre_post\u002F01e2a70aa66bc61801037003815c82a6c1_259.mp4?sign=ef85daf6610eebe4436a95e5a9651962&t=64303cd4","weight":62,"audioChannels":2,"format":"mp4","size":2482754,"backupUrls":["http:\u002F\u002Fsns-video-bd.xhscdn.com\u002Fpre_post\u002F01e2a70aa66bc61801037003815c82a6c1_259.mp4","http:\u002F\u002Fsns-video-hw.xhscdn.com\u002Fpre_post\u002F01e2a70aa66bc61801037003815c82a6c1_259.mp4","http:\u002F\u002Fsns-video-al.xhscdn.com\u002Fpre_post\u002F01e2a70aa66bc61801037003815c82a6c1_259.mp4"],"videoBitrate":729307,"avgBitrate":797960,"fps":25,"rotate":0,"streamDesc":"WM_X264_MP4","volume":0,"audioCodec":"aac","audioDuration":24843,"ssim":0,"qualityType":"HD","height":1280,"duration":24891,"videoCodec":"h264","videoDuration":24800,"psnr":0,"streamType":259}],"h265":[],"av1":[]}},"image":{"thumbnailFileid":"thumbnail\u002F6ebb467937c444018e19cdcb6aa2d4d3"}},"tagList":[{"type":"topic","id":"531ce1eeb4c4d657c90870c5","name":"美甲"},{"name":"美甲分享","type":"topic","id":"5660083c3fef925334336553"},{"name":"教程","type":"topic","id":"5bf7be7ba97628000137c5ee"}],"lastUpdateTime":1655114442000,"type":"video","title":"新手小雏菊教程","desc":"  ","user":{"avatar":"https:\u002F\u002Fsns-avatar-qc.xhscdn.com\u002Favatar\u002F5c507e860263e800018e4685.jpg","userId":"5afb9cdd4eacab3d22a3e087","nickname":"ZHANGJUNA"},"interactInfo":{"collectedCount":"1k+","commentCount":"10+","shareCount":"100+","followed":false,"liked":false,"likedCount":"1k+","collected":false},"atUserList":[],"time":1655114441000},"volume":0,"currentTime":1680795784096,"comments":{"list":[],"cursor":"","hasMore":true,"loading":false},"commentValue":"","commentAt":[],"commentSelectionStart":0,"commentSelectionEnd":0,"mediaWidth":450,"noteHeight":800,"showRedmoji":false,"commentTarget":{},"noteContentHeight":0,"metricsReportMetaData":{"currentReportType":"enter","startReadNoteClientTimeStamp":0,"noteStaySeconds":0,"isCommentCurrentNote":false,"isLikeCurrentNote":false,"isCollectCurrentNote":false,"isFollowCurrentNoteAuthor":false},"isImgFullscreen":false,"noteId":"62a70ac9000000001b035550","gotoPage":"","commentNickName":"","firstNoteId":"62a70ac9000000001b035550"},"feed":{"query":{"cursorScore":"","num":30,"refreshType":1,"noteIndex":0,"unreadBeginNoteId":"","unreadEndNoteId":"","unreadNoteCount":0,"category":"homefeed_recommend"},"feedBizFmp":{"fmp":0,"fmpWithImg":0},"isFetching":false,"isError":false,"feedsWrapper":undefined,"feeds":[],"currentChannel":"homefeed_recommend","unreadInfo":{"cachedFeeds":[],"unreadBeginNoteId":"","unreadEndNoteId":"","unreadNoteCount":0,"timestamp":0},"preloadSuccess":false,"preloadConfig":{"usePreload":false,"cacheExpires":259200000,"checkCache":false},"validIds":{"noteIds":[]},"mfStatistics":{"timestamp":0,"visitTimes":0,"readFeedCount":0},"channels":undefined},"redMoji":{"mojiData":{"version":"","redmojiTabs":[],"redmojiMap":{}}}}