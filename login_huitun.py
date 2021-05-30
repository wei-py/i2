from tools import bro_str_to_dic
import requests

headers = """
    Accept: */*
    Accept-Encoding: gzip, deflate, br
    Accept-Language: en-US,en;q=0.9
    Connection: keep-alive
    Cookie: 
    Host: liveapi.huitun.com
    Origin: https://huitun.com
    Referer: https://huitun.com/
    sec-ch-ua: "Chromium";v="90", "Opera";v="76", ";Not A Brand";v="99"
    sec-ch-ua-mobile: ?0
    Sec-Fetch-Dest: empty
    Sec-Fetch-Mode: cors
    Sec-Fetch-Site: same-site
    User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 OPR/76.0.4017.137
    X-Requested-LOGIN: plugin
"""
headers = bro_str_to_dic(headers)

session = requests.Session()
login_api = 'https://liveapi.huitun.com/user/login?mobile=13178802311&password=liang123456789'
cookies = session.get(url=login_api, headers=headers).cookies
print(cookies)
main_url = 'https://huitun.com/app/#/anchor/anchor_ranking'
resp = session.get(url=main_url, cookies=cookies)
print(resp.text, resp.status_code)