# -*- coding: utf-8 -*- 
# @Time : 2019/11/27 0027 18:26 
# @Author : cuiws 
# @File : Gao7NewSpider.py
#搞趣网
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
        resp = requests.get(url,headers=headers)
        # resp.encoding=requests.utils.get_encodings_from_content(resp.text)
        resp.encoding = requests.utils.get_encoding_from_headers(resp.headers)
        html = resp.text
        soup = BeautifulSoup(html,'lxml')
        article = soup.find('div',{'class':'area-gao7-article'})#文章框架
        title = str(article.find('h1',{'class':'article-title'}).text).strip()#标题
        content = article.find('div',{'class':'gao7-article clearfix'})#文章主体
        p_arr = content.find_all('p')
        content_list = toutiao_util.format_p(p_arr,title)
        toutiao_util.convert_doc(content_list,title)
        return True
    except:
        print("搞趣网url[%s] 抓取失败 跳过" % url)
        return False


if __name__ == '__main__':
    run()





