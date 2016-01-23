#coding:utf8
"""
Created on 2016年1月11日

@author: pan
"""
from bs4 import BeautifulSoup
import re
import urlparse



class HtmlParser(object):


    @staticmethod
    def _get_new_urls(pageUrl, soup):
        newurls = set()
        #href="/question/36217733#answer-22883428"
        links = soup.find_all('a',href=re.compile(r"/question/\d+#answer-\d+"))
        for link in links:
            newurl = link['href']
            newfullurl = urlparse.urljoin(pageUrl ,newurl)
            newurls.add(newfullurl)
        return newurls



    @staticmethod
    def _get_new_data(pageUrl, soup):
        resdata = {'url': pageUrl}
        #<a class="question_link" target="_blank" href="/question/35667984#answer-22946961">减肥对外貌的改变有多大？</a>
        title_node = soup.find('a', class_="question_link")
        resdata['title'] = title_node.get_text()
        #<div class="zh-summary summary clearfix">
        summar_node = soup.find('div', class_="zh-summary summary clearfix")
        resdata['summary']=summar_node.get_text()
        return resdata


    def parse(self, pageurl, htmlcontent):
        if pageurl is None or htmlcontent is None:
            return None

        soup = BeautifulSoup(htmlcontent, 'html.parser', from_encoding='utf-8')
        newurls = self._get_new_urls(pageurl, soup)
        new_data = self._get_new_data(pageurl, soup)

        return newurls, new_data







