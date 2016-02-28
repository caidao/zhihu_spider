#coding:utf8
"""
Created on 2016年1月11日

@author: pan
"""
import time

import urlManager, htmlDownloader, htmlParaser, htmlOutput
import threadpool
import dao


class SpiderMain(object):
    def __init__(self, root_url):
        self.dao = dao.Dao()
        self.urlMangers = urlManager.UrlManger()
        self.downloaders= htmlDownloader.HtmlDownloader(self.dao)
        self.parsers = htmlParaser.HtmlParser()
        self.outPuters = htmlOutput.HtmlOutput(self.dao)
        self.root_url = root_url
        self.dictlist = list()
        self.pool = threadpool.ThreadPool(8)

    #抓取关联用户信息
    def craw_relative_user(self, rooturl, srcusers):
        relatelist = list()
        for users in srcusers:
            try:
                #获取用户信息页面(该用户关注的用户)
                htmlcont_followees = self.downloaders.download(users['url']+'/followees')
                datalist = self.parsers.parse_follow_user(rooturl, htmlcont_followees)
                relatelist.append(datalist)
                #获取被关注用户关注信息(关注改用户的用户)
                htmlcont_followers = self.downloaders.download(users['url']+'/followers')
                datalist = self.parsers.parse_follow_user(rooturl, htmlcont_followers)
                relatelist.append(datalist)
            except Exception, ex:
                print(Exception, ex)
        return relatelist

    #抓取用户信息
    def craw_user(self, rooturl, secondurls):
        self.outPuters.clear_user_data()
        for urls in secondurls:
            self.dictlist = list()
            # for url in urls:
            #     try:
            #         #获取问题连接页面
            #         htmlcont = self.downloaders.download(url['url'])
            #         if htmlcont is None:
            #             continue
            #         #解析页面
            #         datadict = self.parsers.parse_first_user(rooturl, htmlcont)
            #         datadict['url'] = url['url']
            #         #收集数据并打印数据
            #         self.outPuters.collect_user_data(datadict)
            #         dictlist.append(datadict)
            #         print 'user infos :' + datadict['name']+ ' '+ datadict['url']
            #     except Exception, ex:
            #         print(Exception, ex)
            requests = threadpool.makeRequests(self._userinfo_, urls, self._collect_user)
            [self.pool.putRequest(req) for req in requests]
            self.pool.wait()
            self.outPuters.output_user_mysql(self.dictlist)
        return self.outPuters.get_user_data()

    def _collect_user(self, request, datadict):
        if datadict is None:
            return
        self.dictlist.append(datadict)
        print '%s %s %s %s' %(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), request.requestID, datadict['name'], datadict['url'])

    def _userinfo_(self, url):
        try:
            #获取问题连接页面
            htmlcont = self.downloaders.download(url['url'])
            if htmlcont is None:
                return None
            #解析页面
            datadict = self.parsers.parse_first_user(self.root_url, htmlcont)
            datadict['url'] = url['url']
            #收集数据并打印数据
            self.outPuters.collect_user_data(datadict)
        except Exception, ex:
            print(Exception, ex)
            return None
        return datadict


    #爬取首页所有连接的页面的评论信息
    def craw_second_page(self, rooturl, indexurls):
        self.outPuters.clear_index_data()
        for index_url in indexurls:
            #获取问题连接页面
            htmlcont = self.downloaders.download(index_url['url'])
            #解析页面
            datas = self.parsers.parse_second_page(rooturl, htmlcont)
            #收集并打印数据
            self.outPuters.collect_index_data(datas)
            print len(datas)
        self.outPuters.output_html('../out/second_page'+time.strftime('%Y-%m-%d', time.localtime(time.time()))+'.html')
        return self.outPuters.get_index_data()


    #爬取首页的数据
    def craw_index(self, rooturl):
        try:
            #登录知乎网
            self.downloaders.login()
            #获取首页页面数据
            htmlcont = self.downloaders.download(rooturl)
            #解析首页
            newurls= self.parsers.parse_index(rooturl, htmlcont)
            #收集并打印数据
            self.outPuters.collect_index_data(newurls)
            print len(newurls)
            self.outPuters.output_html('../out/index'+time.strftime('%Y-%m-%d', time.localtime(time.time()))+'.html')
            return newurls
        except RuntimeError, ex:
            print 'craw_index failed', RuntimeError, ':', ex

    def close(self):
        self.outPuters.close()


if __name__ == '__main__':
    root_url = "https://www.zhihu.com/"
    spider = SpiderMain(root_url)
    index_urls = spider.craw_index(root_url)
    second_urls = spider.craw_second_page(root_url, index_urls)
    src_users = spider.craw_user(root_url, second_urls)

    for i in range(10):
        relative_users = spider.craw_relative_user(root_url, src_users)
        src_users = spider.craw_user(root_url, relative_users)


    spider.close()

    pass