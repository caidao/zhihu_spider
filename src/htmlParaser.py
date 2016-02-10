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
    def get_first_users(rooturl, soup):
        retdata = {'name': '', 'bio': '', 'location': '', 'business': '', 'gender': ''}
        header = soup.find('div', class_='zm-profile-header-main')

        #该用户的主要信息
        main_node = header.find('div', class_='title-section ellipsis')
        if main_node is not None:
            try:
                retdata['name'] = main_node.find('span', class_='name').get_text()
                retdata['bio'] = main_node.find('span', class_='bio').get_text()
            except Exception, ex:
                print ' get_first_users name', Exception, ':', ex

        #用户其他信息
        other_node = header.find('div', class_='zm-profile-header-user-describe')
        if other_node is not None:
            try:#地点
                retdata['location'] = other_node.find('span', class_='location item').get('title')
            except Exception, ex:
                print ' get_first_users location', Exception, ':', ex

            try:#方向
                retdata['business'] = other_node.find('span', class_='business item').get('title')
            except Exception, ex:
                print ' get_first_users business', Exception, ':', ex

            try:#性别
                gender = other_node.find('span', class_='item gender').find('i').get('class')
                if gender[1].find('female')>0:
                    retdata['gender']=u'女'
                else:
                    retdata['gender']=u'男'
            except Exception, ex:
                print ' get_first_users gender', Exception, ':', ex

            try:#公司
                retdata['employment'] = other_node.find('span', class_='employment item').get('title')
            except Exception, ex:
                retdata['employment']=''
                print ' get_first_users employment', Exception, ':', ex

            try:#职位
                retdata['position'] = other_node.find('span', class_='position item').get('title')
            except Exception, ex:
                retdata['position']=''
                print ' get_first_users position', Exception, ':', ex

            try:#学校
                retdata['school'] = other_node.find('span', class_='education item').get('title')
            except Exception, ex:
                retdata['school'] = ''
                print ' get_first_users school', Exception, ':', ex

            try:#专业
                retdata['major'] = other_node.find('span', class_='education-extra item').get('title')
            except Exception, ex:
                retdata['major'] = ''
                print ' get_first_users major', Exception, ':', ex


        return retdata

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

    #解析评论的用户信息
    def parse_first_user(self, rooturl, htmlcontent):
        if rooturl is None or htmlcontent is None:
            return None
        soup = BeautifulSoup(htmlcontent, 'html.parser', from_encoding='utf-8')
        return self.get_first_users(rooturl, soup)






