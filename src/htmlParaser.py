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
    def _get_new_urls(pageurl, soup):
        newurls = set()
        #href="/question/36217733#answer-22883428"
        links = soup.find_all('a', href=re.compile(r"/question/\d+#answer-\d+"))
        for link in links:
            newurl = link['href']
            newfullurl = urlparse.urljoin(pageurl, newurl)
            newurls.add(newfullurl)
        return newurls


    @staticmethod
    def get_index_urls(pageurl, soup):
        newurls = list()
        links = soup.find_all('div', class_='feed-main')
        for link in links:
            try:
                temp = HtmlParser.get_index_data(pageurl, link)
                if temp is not None:
                    newurls.append(temp)
            except RuntimeError, ex:
                print link+' failed', RuntimeError, ':', ex
        return newurls

    @staticmethod
    def get_second_page_data(rooturl, soup):
        datalist = list()
        links = soup.find_all('div', class_='zm-item-answer  zm-item-expanded')
        for link in links:
            try:
                temp = HtmlParser.get_second_data(rooturl, link)
                if temp is not None:
                    datalist.append(temp)
            except RuntimeError, ex:
                print link+' failed', RuntimeError, ':', ex
        return datalist

    @staticmethod
    def _get_new_data(pageurl, soup):
        resdata = {'url': pageurl}
        #<a class="question_link" target="_blank" href="/question/35667984#answer-22946961">减肥对外貌的改变有多大？</a>
        title_node = soup.find('a', class_="question_link")
        resdata['title'] = title_node.get_text()
        #<div class="zh-summary summary clearfix">
        summar_node = soup.find('div', class_="zh-summary summary clearfix")
        resdata['summary']=summar_node.get_text()
        return resdata



    @staticmethod
    def get_index_data(pageurl, soup):
        resdata = {}
        #<a class="question_link" target="_blank" href="/question/35667984#answer-22946961">减肥对外貌的改变有多大？</a>
        try:
            title_node = soup.find('a', class_="question_link")
            resdata['title'] = title_node.get_text()
            newurl = title_node['href']
            newfullurl = urlparse.urljoin(pageurl, newurl)
            resdata['url'] = newfullurl
            #<div class="source">
            topic_links = soup.find('div', class_="source").find_all('a', href=re.compile(r"/topic/\d+"))
            temp = ''
            for topic in topic_links:
                temp+=topic.get_text()+','
            resdata['source']=temp
            return resdata
        except Exception, ex:
            print 'craw_index failed', Exception, ':', ex
            return None

    @staticmethod
    def get_second_data(rooturl, soup):
        ret_data = {}
        try:
            #获取评论数
            commnet_node = soup.find('a', class_=' meta-item toggle-comment')
            ret_data['source'] = commnet_node.get_text()
            #获取用户信息
            title_node = soup.find('a', class_='author-link')
            ret_data['title'] = title_node.get_text()
            ret_data['url'] = urlparse.urljoin(rooturl, title_node['href'])
            return ret_data
        except Exception, ex:
            print 'get_second_data failed', Exception, ':', ex
            return None

    def parse(self, pageurl, htmlcontent):
        if pageurl is None or htmlcontent is None:
            return None

        soup = BeautifulSoup(htmlcontent, 'html.parser', from_encoding='utf-8')
        newurls = self._get_new_urls(pageurl, soup)
        new_data =self._get_new_data(pageurl, soup)

        return newurls, new_data

    #解析知乎首页数据
    def parse_index(self, pageurl, htmlcontent):
        if pageurl is None or htmlcontent is None:
            return None
        soup = BeautifulSoup(htmlcontent, 'html.parser', from_encoding='utf-8')
        newurls = self.get_index_urls(pageurl, soup)
        return newurls

    #解析连接的问题页面
    def parse_second_page(self, rooturl, htmlcontent):
        if rooturl is None or htmlcontent is None:
            return None
        soup = BeautifulSoup(htmlcontent, 'html.parser', from_encoding='utf-8')
        return self.get_second_page_data(rooturl, soup)









