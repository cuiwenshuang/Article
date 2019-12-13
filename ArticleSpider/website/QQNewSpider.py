# -*- coding: utf-8 -*- 
# @Time : 2019/11/27 0027 18:25 
# @Author : cuiws 
# @File : QQNewSpider.py
#QQ新闻
import requests
from bs4 import BeautifulSoup
import toutiao_util

def run(url):
    try:
        print(url)
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
        }
        # url = "https://new.qq.com/omn/20191123/20191123A03WKE00.html"
        resp = requests.get(url, headers=headers)
        resp.encoding = requests.utils.get_encoding_from_headers(resp.headers)
        # resp.encoding = requests.utils.get_encodings_from_content(resp.text)
        html = str(resp.text).replace("X博士","师兄")
        soup = BeautifulSoup(html, 'lxml')
        title = str(soup.find('title').text).replace("腾讯新闻","").replace("_","")
        content = soup.find('div',{'class':'content-article'})
        p_arr = content.find_all('p')
        content_list = toutiao_util.format_p(p_arr, title)
        toutiao_util.convert_doc(content_list, title)
    except:
        print("QQ新闻url[%s] 抓取失败 跳过"%url)


if __name__ == '__main__':
    run("https://new.qq.com/omn/20191202/20191202A06UWH00.html")