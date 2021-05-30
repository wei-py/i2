# from tools import bro_str_to_dic
# import requests

# session = requests.session()
# headers = """
#     Accept: application/json
#     Accept-Encoding: gzip, deflate, br
#     Accept-Language: en-US,en;q=0.9
#     Connection: keep-alive
#     Content-Length: 222
#     Content-Type: application/x-www-form-urlencoded
#     Cookie: viewed="1139426"; bid=WnTYr4KbJmU; gr_user_id=2ace45fb-e3b0-40a0-b1c2-0ceaa1262192; __gads=ID=3da38d73a50f7ba8-2258fd6003c70014:T=1617541135:RT=1617541135:S=ALNI_MYDcsvN5G02m-IcfTDaGxTvaRxc2Q; ll="118281"; douban-fav-remind=1; __utmz=30149280.1620358826.3.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; apiKey=; __utma=30149280.750056971.1617541136.1620358826.1622359207.4; __utmc=30149280; __utmt=1; last_login_way=account; ap_v=0,6.0; push_noty_num=0; push_doumail_num=0; __utmv=30149280.21530; __utmb=30149280.11.10.1622359207; login_start_time=1622359392741
#     Host: accounts.douban.com
#     Origin: https://accounts.douban.com
#     Referer: https://accounts.douban.com/passport/login_popup?login_source=anony
#     sec-ch-ua: "Chromium";v="90", "Opera";v="76", ";Not A Brand";v="99"
#     sec-ch-ua-mobile: ?0
#     Sec-Fetch-Dest: empty
#     Sec-Fetch-Mode: cors
#     Sec-Fetch-Site: same-origin
#     User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 OPR/76.0.4017.137
#     X-Requested-With: XMLHttpRequest
# """
# headers = bro_str_to_dic(headers)


# form_data = """
#     ck: 
#     remember: true
#     name: 15918983899
#     password: douban159..
#     ticket: t03QLXhD7bAFylw50btOmB6V_s_TEnTMyXjfTwgl6gYzOxQSIT9aZohW_snk9Q9oS-mbPowtmIkwV1zdsXVOVCXQHT9AuDlLbikGTDQQDNKeonnG7cqogQWjg**
#     randstr: @Uel
#     tc_app_id: 2044348370
# """
# form_data = bro_str_to_dic(form_data)


# login_api = 'https://accounts.douban.com/j/mobile/login/basic'

# resp = session.post(url=login_api, headers=headers, data=form_data)
# print(resp.status_code)
# print(resp.json())



#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Required
- requests (必须)
- bs4 (必选)
- pillow (可选)
Info
- author : "shjunlee"
- email  : "shjunlee@foxmail.com"
- date   : "2017.8.30"
'''

from urllib.request import urlretrieve
import requests
from bs4 import BeautifulSoup
from os import remove
try:
    import cookielib
except:
    import http.cookiejar as cookielib
try:
    from PIL import Image
except:
    pass

url = 'https://accounts.douban.com/login'

datas = {'source': 'index_nav',
         'remember': 'on'}

headers = {'Host':'www.douban.com',
           'Referer': 'https://www.douban.com/',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
           'Accept-Encoding':'gzip, deflate, br'}

# 尝试使用cookie信息
session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookies')
try:
    session.cookies.load(ignore_discard=True)
except:
    print("Cookies未能加载")
    #cookies加载不成功，则输入账号密码信息
    datas['form_email'] = input('Please input your account:')
    datas['form_password'] = input('Please input your password:')


def get_captcha():
    '''
    获取验证码及其ID
    '''
    r = requests.post(url, data=datas, headers=headers)
    page = r.text
    soup = BeautifulSoup(page, "html.parser")
    # 利用bs4获得验证码图片地址
    img_src = soup.find('img', {'id': 'captcha_image'}).get('src')
    urlretrieve(img_src, 'captcha.jpg')
    try:
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
    except:
        print('到本地目录打开captcha.jpg获取验证码')
    finally:
        captcha = input('please input the captcha:')
        remove('captcha.jpg')
    captcha_id = soup.find(
        'input', {'type': 'hidden', 'name': 'captcha-id'}).get('value')
    return captcha, captcha_id


def isLogin():
    '''
    通过查看用户个人账户信息来判断是否已经登录
    '''
    url = "https://www.douban.com/accounts/"
    login_code = session.get(url, headers=headers,
                             allow_redirects=False).status_code
    if login_code == 200:
        return True
    else:
        return False


def login():
    captcha, captcha_id = get_captcha()
    # 增加表数据
    datas['captcha-solution'] = captcha
    datas['captcha-id'] = captcha_id
    login_page = session.post(url, data=datas, headers=headers)
    page = login_page.text
    soup = BeautifulSoup(page, "html.parser")
    result = soup.findAll('div', attrs={'class': 'title'})
    #进入豆瓣登陆后页面，打印热门内容
    for item in result:
        print(item.find('a').get_text())
    # 保存 cookies 到文件，
    # 下次可以使用 cookie 直接登录，不需要输入账号和密码
    session.cookies.save()

if __name__ == '__main__':
    if isLogin():
        print('Login successfully')
    else:
        login()
