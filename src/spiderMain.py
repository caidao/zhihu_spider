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
        
    def craw(self, rooturl):
        count = 1
        self.urlMangers.add_new_url(rooturl)
        while self.urlMangers.hasnewurl():
            try:
                newurl = self.urlMangers.get_new_url()
                print 'craw %d : %s' % (count, newurl)
                htmlcont = self.downloaders.download(newurl)
                newurls, newdata = self.parsers.parse(newurl, htmlcont)
                self.urlMangers.addnewurls(newurls)
                self.outPuters.collect_data(newdata)
                if count == 10:
                    break
                count += 1
            except Exception, ex:
                print 'craw failed', Exception, ':', ex
            
        self.outPuters.output_html()

    def craw_index(self, rooturl):
        try:
            #登录知乎网
            self.downloaders.login()
            #获取首页页面数据
            htmlcont = self.downloaders.download(root_url)
            #解析首页
            newurls= self.parsers.parse_index(root_url, htmlcont)
            self.outPuters.collect_index_data(newurls)
            print len(newurls)
            self.outPuters.output_html()
        except Exception, ex:
            print 'craw_index failed', Exception, ':', ex


if __name__ == '__main__':
    root_url = "https://www.zhihu.com/"
    spider = SpiderMain()
    spider.craw_index(root_url)
    #spider.craw(root_url)
    pass