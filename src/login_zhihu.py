#coding:utf8
'''
Created on 2016��1��18��

@author: pan
'''
import time
import json
import os
from pip._vendor import requests

_Zhihu_URL = 'http://www.zhihu.com'
_Login_URL = _Zhihu_URL + '/login/email'
_Captcha_URL_Prefix = _Zhihu_URL + '/captcha.gif?r='
_Cookies_File_Name = 'cookies.json'

_session = None
_header = {'X-Requested-With': 'XMLHttpRequest',
           'Referer': 'http://www.zhihu.com',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; '
                         'Trident/7.0; Touch; LCJB; rv:11.0)'
                         ' like Gecko',
           'Host': 'www.zhihu.com'}

def get_captcha_url():

    return _Captcha_URL_Prefix + str(int(time.time() * 1000))

def _save_captcha(url):
    global _session
    r = _session.get(url)
    with open('code.gif', 'wb') as f:
        f.write(r.content)

def login(email='', password='', captcha='', savecookies=True):
 
    global _session
    global _header
    data = {'email': email, 'password': password,
            'rememberme': 'true', 'captcha': captcha}
    r = _session.post(_Login_URL, data=data)
    j = r.json()
    c = int(j['r'])
    m = j['msg']
    if c == 0 and savecookies is True:
        with open(_Cookies_File_Name, 'w') as f:
            json.dump(_session.cookies.get_dict(), f)
    return c, m

def create_cookies():
    if os.path.isfile(_Cookies_File_Name) is False:
        email ='panyiwen2009@gmail.com' #raw_input('email: ')
        password = raw_input('password: ')
        url = get_captcha_url()
        _save_captcha(url)
        print('please check code.gif for captcha')
        captcha = raw_input('captcha: ')
        code, msg = login(email, password, captcha)

        if code == 0:
            print('cookies file created!'+msg)
        else:
            print(msg)
        os.remove('code.gif')
    else:
        print('Please delete [' + _Cookies_File_Name + '] first.')

def _init():
    global _session
    if _session is None:
        _session = requests.session()
        _session.headers.update(_header)
        if os.path.isfile(_Cookies_File_Name):
            with open(_Cookies_File_Name, 'r') as f:
                cookies_dict = json.load(f)
                _session.cookies.update(cookies_dict)
        else:
            print('no cookies file, this may make something wrong.')
            print('if you will run create_cookies or login next, '
                  'please ignore me.')
            _session.post(_Login_URL, data={})
    else:
        raise Exception('call init func two times')

def loginZhihu():
    _init()
    create_cookies()

if __name__ == '__main__':
    _init()
    create_cookies()

    
