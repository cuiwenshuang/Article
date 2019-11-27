from redis import StrictRedis


#请求工具
class RequestUtil():
    @staticmethod
    def get_header(cookie,referer=None):
        header = {
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.64 Safari/537.36',
            'Host':'mp.toutiao.com',
            'Cookie': cookie
        }
        if referer is not None:
            header["Referer"] = referer
        return header