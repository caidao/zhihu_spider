#coding:utf8
"""
Created on 2016年1月11日

@author: pan
"""
import urllib2
from src.login_zhihu import loginZhihu, _Cookies_File_Name
import json


class HtmlDownloader(object):
    
    
    @staticmethod
    def download(url):
        if url is None:
            return None

        response = urllib2.urlopen(url)
        if response.getcode() != 200:
            return None

        return response.read()

    @staticmethod
    def test():
        root_url = "https://www.zhihu.com/question/39660507"
        print '第一种方法'
        opener = urllib2.build_opener()
        with open(_Cookies_File_Name, 'r') as f:
            cookies_dict = json.load(f)
            cookstr = ''
            for k, v in cookies_dict.items():
                cookstr += str(k + '=' + v + ';')
        opener.addheaders.append(('Cookie', cookstr))
        opener.addheaders.append(('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'))
        response1 = opener.open(root_url)
        print response1.getcode()
        print response1.read()
            
    
if __name__ == '__main__':
    loginZhihu()
    downl = HtmlDownloader()
    downl.test()
    print 'hello word'
    #downl.download(root_url)



