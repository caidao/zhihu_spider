#coding:utf8
'''
Created on 2016年1月11日

@author: pan
'''
import urlManager, htmlDownloader, htmlParaser, htmlOutput
from src.login_zhihu import loginZhihu

class SpiderMain(object):
    def __init__(self):
        self.urlMangers = urlManager.UrlManger()
        self.downloaders= htmlDownloader.HtmlDownloader()
        self.parsers = htmlParaser.HtmlParser()
        self.outPuters = htmlOutput.HtmlOutput()
        
    def craw(self,root_url):
        count = 1
        self.urlMangers.addNewUrl(root_url)
        while self.urlMangers.hasNewUrl():
            try:
                newUrl = self.urlMangers.getNewUrl()
                print 'craw %d : %s' % (count,newUrl)
                htmlCont = self.downloaders.download(newUrl)
                newUrls,newData = self.parsers.parse(newUrl,htmlCont)
                self.urlMangers.addNewUrls(newUrls)
                self.outPuters.collectData(newData)
                if count == 10:
                    break
                count = count +1
            except Exception,ex:
                print 'craw failed',Exception,':',ex
            
        self.outPuters.outputHtml()

if __name__ == '__main__':
    loginZhihu()
    root_url = "https://www.zhihu.com/"
    spider = SpiderMain()
    spider.craw(root_url)
    pass