#coding:utf8
"""
Created on 2016年1月11日

@author: pan
"""
import cookielib
import json
import os
import urllib
import urllib2
import filter

_Zhihu_URL = 'http://www.zhihu.com'
_Login_URL = _Zhihu_URL + '/login/email'
_root_url = "https://www.zhihu.com"
_Captcha_URL_Prefix = _Zhihu_URL + '/captcha.gif?r='


class HtmlDownloader(object):

    def __init__(self, dao_obj):
        cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        self.opener.addheaders= [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64)AppleWebKit/537.36 (KHTML, like Gecko) '
                                                'Chrome/45.0.2454.85 Safari/537.36)')]
        self.filter = filter.Filter(dao_obj.get_bloom())

    def login(self):
        email ='panyiwen2009@gmail.com'#raw_input('email: ')
        password =raw_input('password: ')
        rep_cap = self.opener.open(_Captcha_URL_Prefix)
        with open('code.gif', 'wb') as f:
            f.write(rep_cap.read())

        print('please check code.gif for captcha')
        captcha = raw_input('captcha: ')

        data = urllib.urlencode({'email': email, 'password': password,
            'rememberme': 'true', 'captcha': captcha})
        rep = self.opener.open(_Login_URL, data=data)
        print rep.getcode()
        temp = rep.read()
        j = json.loads(temp, encoding='utf-8')
        c = int(j['r'])
        m = j['msg']
        os.remove('code.gif')
        return c, m

    def download(self, url):
        if url is None:
            return None

        #过滤重复的url
        if self.filter.check(url):
            print '重复url : %s', (url)
            return None

        response = self.opener.open(url)
        if response.getcode() != 200:
            return None

        return response.read()

    @staticmethod
    def test():
        root_url = "https://www.zhihu.com/question/39660507"
            
    
if __name__ == '__main__':
    downl = HtmlDownloader()
    downl.login()
    print 'hello word'
    #downl.download(root_url)



