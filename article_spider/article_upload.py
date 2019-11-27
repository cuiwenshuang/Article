from datetime import datetime,timedelta
from toutiao_util import *
from urllib.request import quote
from bs4 import BeautifulSoup
import os
import requests
import json
import time

def all_files():
    arr = []
    base_path = str(datetime.now().date())
    for root, dirs, files in os.walk(base_path):
        for file in files:
            filename = "%s/%s"%(base_path,file)
            arr.append(filename)
    return arr


def upload_title(title):
    req_url="https://mp.toutiao.com/check_title/?title=%s"%quote(title)
    refer = "https://mp.toutiao.com/profile_v3/graphic/publish"
    text = requests.get(req_url,headers=RequestUtil.get_header(CookieUtil.get_cookie(),refer)).text
    print(text)


def format_content(text):
    res_arr = []
    soup = BeautifulSoup(text,'lxml')
    arr = soup.find_all('p')
    for res in arr:
        if str(res).__contains__("xmlns") and not str(res).__contains__("src="):
            res_arr.append("<p>%s</p>"%res.text)
        elif str(res).__contains__("src="):
            soup = BeautifulSoup(str(res.img),'lxml')
            a = soup.find('img')
            res_arr.append('<div class="pgc-img"><img class="" src="%s" data-ic="false" data-ic-uri="" data-height="0" data-width="0" data-story_id="" data-image_ids="[]" image_type="1" mime_type="image/jpeg" web_uri="%s" img_width="0" img_height="0"><p class="pgc-img-caption"></p></div><p><br></p>'%(str(a['src']),str(a['alt'])))
        else:
            pass
    return "".join(res_arr)


def get_article_id():
    req_url = "https://mp.toutiao.com/core/article/new_article/?article_type=0&format=json&compat=1&column_no="
    refer = "https://mp.toutiao.com/profile_v3/graphic/publish"
    text = requests.get(req_url,headers=RequestUtil.get_header(CookieUtil.get_cookie(),refer))
    text.encoding="utf-8"
    html = text.text
    res = json.loads(html)
    return res['data']['media']['id']


def submit_file(title,content):
    article_id = get_article_id()
    timer = datetime.now() + timedelta(hours=12)
    timer_time = timer.strftime("%Y-%m-%d %H:%M:%S")
    req_url = "https://mp.toutiao.com/core/article/edit_article_post/?source=mp&type=article"
    refer = "https://mp.toutiao.com/profile_v3/graphic/publish"
    params = {
        "article_type": 0,
        "title":title,
        "content":content,
        "activity_tag":0,
        "title_id":"%s_%s"%(str(int(time.time())),article_id),#当前时间戳_xxx
        "claim_origin":0,
        "article_ad_type":3,
        "add_third_title":0,
        "recommend_auto_analyse":0,
        "tag":"",
        "article_label":"",
        "is_fans_article":0,
        "quote_hot_spot":0,
        "govern_forward":0,
        "push_status":0,
        "push_android_title":"",
        "push_android_summary":"",
        "push_ios_summary":"",
        "timer_status":0,
        "timer_time":timer_time,#当前时间12小时后
        "praise":0,
        "community_sync":0,
        "column_chosen":0,
        "pgc_id":0,
        "qy_self_recommendation":0,
        "pgc_feed_covers":[],
        "from_diagnosis":0,
        "origin_debut_check_pgc_normal":0,
        "tree_plan_article":0,
        "save":1
    }
    cookis = ""
    text = requests.post(req_url,headers= RequestUtil.get_header(cookis,refer),json=params)
    text.encoding="utf-8"
    html = text.text
    print(html)



def load_local_file(filename):
    req_url="https://mp.toutiao.com/other/tika/ueditor"
    refer = "https://mp.toutiao.com/profile_v3/graphic/publish"
    cookis=""
    text = requests.post(req_url,headers=RequestUtil.get_header(cookis),files={"file":open(filename,'rb')})
    text.encoding = "utf-8"
    html = text.text
    title = filename.split("/")[-1].replace(".doc","")
    upload_title(title)
    content = format_content(html)
    submit_file(title,content)



if __name__ == '__main__':
    arr = all_files()
    load_local_file(arr[0])

