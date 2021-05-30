from tools import bro_str_to_dic, load_js
import requests, requests_html, re

session = requests.session()
headers = """
    authority: login.taobao.com
    method: POST
    path: /newlogin/login.do?appName=taobao&fromSite=0&_bx-v=2.0.39
    scheme: https
    accept: application/json, text/plain, */*
    accept-encoding: gzip, deflate, br
    accept-language: en-US,en;q=0.9
    content-length: 4012
    content-type: application/x-www-form-urlencoded
    cookie: _m_h5_tk=6bfce53e3a4b451cfef0aeabe014a2c1_1622355379553; _m_h5_tk_enc=44bee1a6d0df700aaa7f240b08efa587; cna=XPs5GdXSKWQCAXeC5Hssod92; XSRF-TOKEN=636bb9f1-a6f2-499c-90a6-a97b3abcd929; _samesite_flag_=true; cookie2=134ab23bc8b4bf0fc023c706f5b97848; t=8d966cf95888dc996aba3a7847b315d6; _tb_token_=8b65e660de8; xlly_s=1; _bl_uid=s9kjzpmea13nv2kwet4z7w4t38Rz; l=eBOw7RSljG9cOCY6BO5Courza77OXIJbzPVzaNbMiInca1-htFOW8NCCow8ySdtx_t5bhEtPi0So-ReWrSUU5x1Hrt7APlUOrMv68O1..; tfstk=ch6RBgm-7onJ8PtAb_F0dP_2corGaayel4TIpuiG6FHtCDkKds2PIOKu18t3FBrA.; isg=BJSUQYisiPSnehw40z78iWORddQG7bjXBLTYBy50IJ-iGTZjWviiZuzfGBmB5PAv
    eagleeye-pappname: gf3el0xc6g@256d85bbd150cf1
    eagleeye-sessionid: m3kyXphnaa5nU5k1XsU2h03pgXdz
    eagleeye-traceid: f7616c7c1622347131850100250cf1
    origin: https://login.taobao.com
    referer: https://login.taobao.com/member/login.jhtml?spm=a21bo.21814703.754894437.1.5af911d9Ng0Zih&f=top&redirectURL=https%3A%2F%2Fwww.taobao.com%2F
    sec-ch-ua: "Chromium";v="90", "Opera";v="76", ";Not A Brand";v="99"
    sec-ch-ua-mobile: ?0
    sec-fetch-dest: empty
    sec-fetch-mode: cors
    sec-fetch-site: same-origin
    user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 OPR/76.0.4017.137
    appName: taobao
    fromSite: 0
    _bx-v: 2.0.39
"""
headers = bro_str_to_dic(headers)

form_data = """
    loginId: 15918983899
    password2: 1ce4664c6c005ea923f623bfc74c53fdd7fc1e53357d991b09d35d3a464d6d52a26415b66de292b81ea0334b6daba5a806d598d97fee78051432dd5a9eaafba265bb3fae7a64bf98625e8a4fb7fd0f8605ac8faf85a9e319a9218aed4a57dc72ede4a4639aa6e660e8b83939931d9b4e5878e40064deeae4d002036f7f276c1f
    keepLogin: false
    ua: 140#jT1DdDLzzzP1Nzo22i2uCtSdvlxrmEKT924DV2nSpRFABsiTpCuv3gNoP2JAtfO+3oLa5CFSjJfIgoCHt4dvqPrHY3hqzzn6NLKd+WzzzXZi9jnqlbrz2DD3V3gqzk9lGYNaU61xzoObV2EqlXze2PPKAzpHRjmijDapV3yN6Lj4QWEhEgzQDYjHMRSwvfUbNPEf5ElVIgvRNDithG16o6zE8f+NTgXJZVyDNZgyGJBtKlWcFpIA6f375Rijo88EP4e/ZGeqqGXrUskk3rzawQ3AIhFTt+InFZrUT0D/HDHZ/xNw+6KnmjKdMEmNyUcdds+dgDDXElHRB657d8wSgKHjy29A6qqVH0qhUj7jJtUHdAjhSyJK+/NNJm49mzNZRAeIXdtTNHs322W6400JP7vg+HUR7Je4wI3ZjCqWtKouXlUjACh6VDn6/WVvSSeK7s5FROaFxhS0dcKLJKNAVS1ABRkkcsSsi8o41HTIrx7TI+ZM1z2ZYEuLQvDveVJy+Myt5Ql/Rt1Dz/X08zL8pn+vGPxKiLjtXFTjlia2i7++IQgttD4X9NtapKZleBe7vcH3IrzCwP66U+WWc9/PTQ7s13lWxvw5hfLD3cpOCKcTl8iJCpJTtsBdqIGy0Y4iup4EN5Ij97E2Sp6nPJaPM5qxykIzsllug3RQctwykArBfFUjY5Y3uKHmObG1GCi2LOhsAG0aY8tE62N/4QmKcCW2vEbwBN2hPD4cBA25pxbxXrelvprmAzUKTXi1RbxPrvaBcDIrXtuPF6tmK5jzb/BjgFAQ4p03KRZhD8B0PI9oVUDAF5PGQxvN0GUm3rKsBQdWwPu36t+3K6uOzXyW4Gy8ZlZqBzhRgEdeGwoDiJ5TnD1m36HoZVRPNoCtSlsfRK5FTRW4dnEnRpoMC7nV53h1PQ7Ar9WTJjAma7vhWcnh5VNs8nMoQdFVu/YH2U8T5SEtN6hjQffsNMZ+xTT3cO9rxd1F2etAdPaZXHnB1zDoYaCo+s4hqBtr4a+KZSw2fRQweV+sm5IK29UMZdJoP4ABG7qZeNexCB889Nu2pQT=
    umidGetStatusVal: 255
    screenPixel: 1680x1050
    navlanguage: en-US
    navUserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 OPR/76.0.4017.137
    navPlatform: MacIntel
    appName: taobao
    appEntrance: taobao_pc
    _csrf_token: 7t7SoDoP0Sp0j8WgUF0Ko
    umidToken: ca13ed133d0f7885b28b817daeb10da818c09178
    hsiz: 1d7ec1af7abe3c52ed3326a609d5facd
    bizParams: 
    style: default
    appkey: 00000000
    from: tbTop
    isMobile: false
    lang: zh_CN
    returnUrl: https://www.taobao.com/
    fromSite: 0
    bx-ua: 211!q4okO9pMUMl7Uyr9E92ES3/kt1TPikGcPUyA kgbG61Mh0/E3BsmbOQbUfGtyQy UgnQf8pgtqOID9xXksX7BDqcDI2AXnk5SR207 PWngO1Hg12Nu0VeSOs22HU0BBo8sMWOmvVvDHpDuc3kyPDKXqft5F1LDGo0JvB vAnJs5DC0R/2MYsfM1QyKG1pCUZKGN6W44gv1oI7kEbyTqI1AnkFNtkfy33mCTWG3o3qfCaBqEjLDHUwLltBhhVxu/LZEa3ooz H56XqH/lEIQR uW5KRxG8SsAKIG2fNvRa9TPh5IlgYZ1HWYmRyQpD2KN7XkRDcRiJl5H/uKlfZL/BRGgjJN7QvuF CskJ51FUI9ZqBFLIw87k ukCqAg0OUPMgQaDrSEYN/0r1qeB9YmD3kDYbFWl7kj2e0hXCWoy09YlZuMa/BSZwEkVmiLnJexmDYkZG7qisBboqw/3vJcuA4ZfhqWT9nekIM0C0WJQ/OrpSZ4UNqOiGpnZ09l bW0bSnXQl6LURGVPuKDKMOVwHOu27BafuBTt Kyq0H/VQ9JVQgiBK40e2r6xYbT/G5r9irm6KWXj0f0Ng3K2GxLBW8i2KV5ia76hODzWtc6LOXgooZ1JAQNqKtkrTJWqMH5L2W48x4xohaRdyIIAhZjoIw83frqCHkBfeyhTTKhykl9PFrvJrl4GI0flNdfIzIUT k62uk0OUBchwZdvGNpe9coUtbVDn1xrL7qlIvi/yX7uIVlxm V0bKkP8HLfUZEElGKn1EdPvjX5m2Jiz/WNzNa5Q6J1hSubxhqxYI2PtVvkAU5Scg3KpNqV6W2aiXILlSx95NvLj4sUsDhXopD0EOHN/b1AxifJ7V7WNo8O7qvRO3QgAxV79EU7rUHF/dWQOg97nQRo9qc7B7EK9qDzBqUEv8KOGAcU9iQLBFK5pEASuZRlY93jFLvXOGllXG9DMKLOTWOSZtzF/Ir9R3yUyl5WVh6LRuUnohk mOzHxzPbik1Oo3lY9XnD64Ezkg6z 4 dEAs/uYeEoTUtvEM9OD9lz1SxVoMyD2tpef23VTS0hW/yNmfhu/HvPahS4vBqXf/k6j7kFN77xHDDScq5Nwg4obNPhqvayIUE4KHOZSBVNLRzrF8pbVs1KQHp3oxr6/SdwXnWEIRehBK2SVX4csI 7v1v8EdYcxS6JIGlYuXMqzSRg7fdXFLpp Vt3Noe5G7wL5sBPyLflLFTQxOobsazm9sRwVzm9NwrySqp6E1eS3sYdDrdZtxvdIUCHuDcM0IJ1cRMxETBx3ER ZH54Q5VsUprZSGyH6wsD2gvtDGpQdCvHbF  xX1hOlxmbpTr3BRumyTTeRA0p rFGLbin8hl7CHOHFTsIUYPdDN0hDkS7Xszkcfs g2V4v1qwe9 tkQ7JuD4PAQ3js9ghZ9PNcRDyXdBXbGqvab4gWa2PGXKm39b8H4IORimJ93/nGyo9zq0OgqmX1BlQl4LAaBDyMHtvCp/yiVRfqQl7qOOszDz4RD2YRamdkkxTHk0/TlDtQlmlhDWGGE Rgly6uGZ5 PzJ218onIzwTS9h0ZOtG7RzHOxzKlsWmtgLWtWtzyzrei oeo /TwC6RtQm9MJpPzuA3rmfHPREjdoASV6grBqYQOUtf4TH84uXSdJZ0AdXeqr8SaWke3Aq5aK0do9opj1rITKDWJg0N/FXCUJ9u46w6rDRRH aDjAtqSy9fIU9O p3lgKdYAuNAhzPq/PMHD9GdjK7bhgGWA796mSH1phP7YBhXdhTCFd3V04dxgVx=
    bx-umidtoken: T2gA9SR5Neq93EJSp6gvyX_bb6PWhxRU_Rsk7tDbBQwUNEJrgey_nJVpCkvpXfphVDk=
"""
form_data = bro_str_to_dic(form_data)

# password2 密码js获取
password2 = load_js('tb_password.js', 'get_pwd()')
form_data['password2'] = password2

# token
resp = session.get(url='https://login.taobao.com/member/login.jhtml').text
hsiz = re.search('","hsiz":"(.*?)","', resp).group(1)
umidToken = re.search('","umidToken":"(.*?)","', resp).group(1)
_csrf_token = re.search('","_csrf_token":"(.*?)","', resp).group(1)
form_data['hsiz'] = hsiz
form_data['umidToken'] = umidToken
form_data['_csrf_token'] = _csrf_token



login_api = 'https://login.taobao.com/newlogin/login.do?appName=taobao&fromSite=0&_bx-v=2.0.39'
login_flag = session.post(url=login_api, headers=headers, data=form_data)
cookies = login_flag.cookies
login_json = login_flag.json()
print(login_json)


# 请求重定向链接
print(login_json['content']['data']['redirectUrl'])
session.get(url=login_json['content']['data']['redirectUrl'], headers=headers, cookies=cookies)

# 请求搜索页
res = session.get(
    url='https://s.taobao.com/search?q=%E6%89%8B%E6%9C%BA&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306',
    headers=headers)
with open('taobao.html', 'w') as f:
    f.write(res.text)
print(res.text)