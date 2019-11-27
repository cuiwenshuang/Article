# -*- coding: utf-8 -*- 
# @Time : 2019/11/27 0027 16:39 
# @Author : cuiws 
# @File : ArticleSpiderBaidu.py

import requests,os
from bs4 import BeautifulSoup
from docx import Document
from datetime import datetime
from urllib.request import quote
from docx.shared import Inches
from PIL import Image
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from RedisUtil import RedisUtil
rs = RedisUtil().get_redis()
def baiduRequest():
    for i in range(1,11):
        headers={
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'www.baidu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
        }
        req_url="https://www.baidu.com/s?ie=utf-8&cl=1&medium=0&rtt=1&bsst=1&tn=news&rsv_sug3=3&rsv_sug4=191&rsv_sug1=3&f=3&rsp=0&rsv_dl=news_b_pn&inputT=953&x_bfe_rqs=03E80&x_bfe_tjscore=0.487742&tngroupname=organic_news&pn=10&word=lol云顶之弈"
        resp = requests.get(req_url,headers=headers)
        resp.encoding='utf-8'
        html = resp.text
        soup = BeautifulSoup(html, 'lxml')
        arr = soup.find_all('div',{"class":"result"})
        for ele in arr:
            title_info = ele.find('a',{'target':'_blank'})
            title = str(title_info.text).strip()
            url = str(title_info['href'])
            domain ="%s//%s"% (url.split("//")[0],url.split("//")[1].split("/")[0])
            author_info = ele.find('p',{'class':'c-author'})
            website = str(author_info.text).strip().split("\xa0")[0]
            print(website)
            print(domain)
            print("%s---%s" % (website, domain))
            print("========================")
            if domain not in rs.keys():
                rs.set(domain.split("//")[1],website)



if __name__ == '__main__':
    baiduRequest()
