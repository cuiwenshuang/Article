# -*- coding: utf-8 -*- 
# @Time : 2019/11/27 0027 16:39 
# @Author : cuiws 
# @File : ArticleSpiderBaidu.py

import requests
from bs4 import BeautifulSoup
from RedisUtil import RedisUtil
import BaiduBJHSpider, Spider18183, Gao7NewSpider, QQNewSpider
import toutiao_util
rs = RedisUtil().get_redis()
website_info = [
    'baijiahao.baidu.com',
    'new.qq.com',
    'news.gao7.com',
    'www.18183.com'
]


def web_exist(url):
    res = False
    for i in website_info:
        if str(url).__contains__(i):
            res = True
            break
    return res


def baiduRequest():
    word_arr = ['LOL', 'LOL云顶']
    for word in word_arr:
        max = 10
        current = 0
        # article_arr = set()
        is_over = False

        for i in range(1, 20):
            if is_over:
                break
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Connection': 'keep-alive',
                'Host': 'www.baidu.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
            }
            req_url = "https://www.baidu.com/s?ie=utf-8&cl=1&medium=0&rtt=%d&bsst=1&tn=news&rsv_sug3=3&rsv_sug4=191&rsv_sug1=3&f=3&rsp=0&rsv_dl=news_b_pn&inputT=953&x_bfe_rqs=03E80&x_bfe_tjscore=0.487742&tngroupname=organic_news&pn=10&word=%s" % (
            i, word)
            resp = requests.get(req_url, headers=headers)
            resp.encoding = 'utf-8'
            html = resp.text
            soup = BeautifulSoup(html, 'lxml')
            arr = soup.find_all('div', {"class": "result"})
            for ele in arr:
                flag = False
                title_info = ele.find('a', {'target': '_blank'})
                url = str(title_info['href'])
                if url.__contains__('baijiahao.baidu.com'):
                    flag = BaiduBJHSpider.run(url)
                elif url.__contains__('new.qq.com'):
                    flag = QQNewSpider.run(url)
                elif url.__contains__('news.gao7.com'):
                    flag = Gao7NewSpider.run(url)
                elif url.__contains__('www.18183.com'):
                    flag = Spider18183.run(url)
                else:
                    toutiao_util.write_log("无法识别的网站类型[%s],跳过"%url)
                if flag:
                    current += 1
                    if current >= max:
                        is_over = True
                        current = 0
                        break


if __name__ == '__main__':
    baiduRequest()
