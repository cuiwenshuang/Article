# -*- coding: utf-8 -*- 
# @Time : 2019/11/28 0028 12:02 
# @Author : cuiws 
# @File : Spider18183.py
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
        # url = "http://www.18183.com/yundingzhiyi/201911/2512764.html"
        resp = requests.get(url, headers=headers)
        # resp.encoding = requests.utils.get_encodings_from_content(resp.text)
        resp.encoding = requests.utils.get_encoding_from_headers(resp.headers)
        html = resp.text
        soup = BeautifulSoup(html, 'lxml')
        title = str(soup.find('h1',{'class':'arc-tit'}).text)
        content = soup.find('div',{'class':'warp_center'})
        p_arr = content.find_all('p')
        content_list = toutiao_util.format_p(p_arr, title)
        toutiao_util.convert_doc(content_list, title)
        return True
    except:
        print("18183url[%s] 抓取失败 跳过" % url)
        return False



if __name__ == '__main__':
    run("https://new.qq.com/omn/20191031/20191031A0B7L100.html")