# -*- coding: utf-8 -*- 
# @Time : 2019/11/27 0027 18:24 
# @Author : cuiws 
# @File : BaiduBJHSpider.py
#百家号
import requests,os,random
from datetime import datetime as dt
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
        resp = requests.get(url, headers=headers)
        resp.encoding = requests.utils.get_encoding_from_headers(resp.headers)

        html = resp.text
        soup = BeautifulSoup(html, 'lxml')
        title = str(soup.find('div', {'class': 'article-title'}).text).strip()  # 标题
        print(title)
        content = soup.find('div', {'class': 'article-content'})  # 文章主体
        content_list = []
        for con in content.contents:
            if str(con).__contains__("img"):
                pic_url = str(con.find('img')['src'])
                if not pic_url.startswith("http"):
                    pic_url = "http:" + pic_url
                pic_name = "".join(random.sample('zyxwvutsrqponmlkjihgfedcba', 20)) + ".png"

                # 上级目录
                upper = os.path.abspath(os.path.join(os.getcwd(), ".."))
                source = os.path.join(upper, 'source').replace("\\", "/")
                if not os.path.exists(source):
                    os.mkdir(source)

                local_file_path = "%s/%s/picture/%s/" % (source, str(dt.now().date()), title)
                if not os.path.exists(local_file_path):
                    os.makedirs(local_file_path)
                pic_path = os.path.join(local_file_path, pic_name)
                toutiao_util.download_pic(pic_url, pic_path)
                content = pic_path
            else:
                text = con.find('span',{'class','bjh-p'})
                if text!=None:
                    content = str(text.text)
                else:
                    continue
            content = toutiao_util.tag_filter(content)
            toutiao_util.write_log(content)
            content_list.append(content)
        toutiao_util.convert_doc(content_list, title)
        return True
    except:
        toutiao_util.write_log("百家号url[%s] 抓取失败 跳过" % url)
        return False


if __name__ == '__main__':
    run()
