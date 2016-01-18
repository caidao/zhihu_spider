#coding:utf8
'''
Created on 2016年1月11日

@author: pan
'''
from bs4 import BeautifulSoup
import re
import urlparse



class HtmlParser(object):
    
    
    def _getNewUrls(self, pageUrl, soup):
        newUrls = set()
        #href="/question/36217733#answer-22883428"
        links = soup.find_all('a',href=re.compile(r"/question/\d+\#answer-\d+"))
        for link in links:
            newUrl = link['href']
            newFullUrl = urlparse.urljoin(pageUrl,newUrl)
            newUrls.add(newFullUrl)
        return newUrls    
        
 
    
    def _getNewData(self, pageUrl, soup):
        resData = {}
        resData['url'] = pageUrl
        #<a class="question_link" target="_blank" href="/question/35667984#answer-22946961">减肥对外貌的改变有多大？</a>
        titleNode = soup.find('a',class_="question_link")
        resData['title'] = titleNode.get_text()
        #<div class="zh-summary summary clearfix">
        summarNode = soup.find('div',class_="zh-summary summary clearfix")
        resData['summary']=summarNode.get_text()
        return resData
    
    
    def parse(self,pageUrl,htmlContent):
        if pageUrl is None or htmlContent is None:
            return None
        
        soup  = BeautifulSoup(htmlContent,'html.parser',from_encoding='utf-8')
        newUrls = self._getNewUrls(pageUrl,soup)
        newData = self._getNewData(pageUrl,soup)
        
        return newUrls,newData
    
    
    
    



