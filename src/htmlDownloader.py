#coding:utf8
'''
Created on 2016年1月11日

@author: pan
'''
import urllib2
from src.login_zhihu import loginZhihu


class HtmlDownloader(object):
    
    
    def download(self,url):
        if url is None:
            return None
        
        response = urllib2.urlopen(url)
        if response.getcode() != 200:
            return None
        
        return response.read()
    
    def test(self):
        root_url = "https://www.zhihu.com/"
        print '第一种方法'
        response1 = urllib2.urlopen(root_url)
        print response1.getcode()
        print response1.read()
            
    
if __name__ == '__main__':
    loginZhihu()
    downl = HtmlDownloader()
    downl.test()
    #downl.download(root_url)



