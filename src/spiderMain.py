#coding:utf8
"""
Created on 2016年1月11日

@author: pan
"""
import urlManager, htmlDownloader, htmlParaser, htmlOutput
from src.login_zhihu import loginZhihu

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

if __name__ == '__main__':
    loginZhihu()
    root_url = "https://www.zhihu.com/"
    spider = SpiderMain()
    spider.craw(root_url)
    pass