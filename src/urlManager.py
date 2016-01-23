#coding:utf8
"""
Created on 2016年1月11日

@author: pan
"""


class UrlManger(object):
    def __init__(self):
        self.newUrls = set()
        self.oldUrls = set()
    
    def add_new_url(self, url):
        if url is None:
            return
        if url not in self.newUrls and url not in self.oldUrls:
            self.newUrls.add(url)
  
    
    def addnewurls(self, urls):
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)

    
    def hasnewurl(self):
        return len(self.newUrls)!=0


    
    def get_new_url(self):
        newurl = self.newUrls.pop()
        self.oldUrls.add(newurl)
        return newurl


    
    
    
    
    
    
    
    
    
    
    



