#coding:utf8
"""
Created on 2016年1月11日

@author: pan
"""
import urlManager, htmlDownloader, htmlParaser, htmlOutput


class SpiderMain(object):
    def __init__(self):
        self.urlMangers = urlManager.UrlManger()
        self.downloaders= htmlDownloader.HtmlDownloader()
        self.parsers = htmlParaser.HtmlParser()
        self.outPuters = htmlOutput.HtmlOutput()

    #抓取第一批用户信息
    def craw_first_user(self, rooturl, secondurls):
        i = 0
        for urls in secondurls:
            for url in urls:
                #获取问题连接页面
                htmlcont = self.downloaders.download(url['url'])
                #解析页面
                datadict = self.parsers.parse_first_user(rooturl, htmlcont)
                datadict['url'] = url['url']
                #收集数据并打印数据
                self.outPuters.collect_user_data(datadict)
                print 'user infos :' + datadict['name']
            #     i+=1
            #     if i==5:
            #         break
            # if i==5:
            #     break
        self.outPuters.output_user_html('../out/user_page.html')



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
        self.outPuters.output_html('../out/second_page.html')
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
            self.outPuters.output_html('../out/index.html')
            return newurls
        except RuntimeError, ex:
            print 'craw_index failed', RuntimeError, ':', ex


if __name__ == '__main__':
    root_url = "https://www.zhihu.com/"
    spider = SpiderMain()
    index_urls = spider.craw_index(root_url)
    second_urls = spider.craw_second_page(root_url, index_urls)
    spider.craw_first_user(root_url, second_urls)
    pass