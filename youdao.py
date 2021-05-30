from tools import bro_str_to_dic, cookie_jar_to_str
import requests, hashlib, time, random, requests_html

youdao_api = 'https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'

origin_data = """
    i: 海贼王
    from: AUTO
    to: AUTO
    smartresult: dict
    client: fanyideskweb
    salt: 16221269072599
    sign: bfb60dbd2dbfc69a2567bab8409fceb2
    lts: 1622126907259
    bv: e5fe214c3c3b3dc9e13c5e17843bbc53
    doctype: json
    version: 2.1
    keyfrom: fanyi.web
    action: FY_BY_REALTlME
"""

new_data = bro_str_to_dic(origin_data)


headers = """
    Accept: application/json, text/javascript, */*; q=0.01
    Accept-Encoding: gzip, deflate, br
    Accept-Language: en-US,en;q=0.9
    Cache-Control: no-cache
    Connection: keep-alive
    Content-Length: 264
    Content-Type: application/x-www-form-urlencoded; charset=UTF-8
    Cookie: OUTFOX_SEARCH_USER_ID=1708780914@10.108.160.105; OUTFOX_SEARCH_USER_ID_NCOO=1236818069.0203967; _ntes_nnid=25ba70dd0305687e0f915c5635d149d7,1620371478958; fanyi-ad-id=109753; fanyi-ad-closed=1; JSESSIONID=aaaAHB30CeoC_-uOJsUMx; ___rl__test__cookies=1622298392652
    Host: fanyi.youdao.com
    Origin: https://fanyi.youdao.com
    Pragma: no-cache
    Referer: https://fanyi.youdao.com/
    sec-ch-ua: "Chromium";v="90", "Opera";v="76", ";Not A Brand";v="99"
    sec-ch-ua-mobile: ?0
    Sec-Fetch-Dest: empty
    Sec-Fetch-Mode: cors
    Sec-Fetch-Site: same-origin
    User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 OPR/76.0.4017.137
    X-Requested-With: XMLHttpRequest
"""

headers = bro_str_to_dic(headers)
url = 'https://fanyi.youdao.com'


word = input('input word:')
# word = '海贼王'
appVersion = "5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 OPR/76.0.4017.137".encode('utf-8')
bv = hashlib.md5(appVersion).hexdigest()
ts = str(int(time.time()) * 1000)
salt = ts + str(int(random.random()*10))
#  拼接
sign = "fanyideskweb" + word + salt + "Tbh5E8=q6U3EXe+&L[4c@"
#  处理（加密）
sign = hashlib.md5(sign.encode('utf-8')).hexdigest()

new_data['i'] = word
new_data['salt'] = salt
new_data['sign'] = sign
new_data['lts'] = ts
new_data['bv'] = bv

resp = requests.post(url=youdao_api, headers=headers, data=new_data).json()
print(resp)