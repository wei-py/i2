import json,  requests, execjs

# def bro_str_to_dic_2(s):
#     dic = {}
#     for i in s.split('\n'):
#         i = i.strip().split(': ')
        
#         if len(i[0]) == 0:
#             continue
#         else:
#             if len(i) == 2:   
#                 dic[i[0]] = i[1]
#             else:
#                 dic[i[0]] = ''
#     return dic


def cookie_jar_to_str(cookies):
    cookies_str = ''
    for key ,value in requests.utils.dict_from_cookiejar(cookies).items():
        cookies_str += key + '=' + value + ';' + ' '
    return cookies_str[:-2]

def bro_str_to_dic(s):
    return {i.split(': ')[0].strip(): i.split(': ')[1].strip() if len(i.split(': ')[1].strip()) > 0 else '' for i in s.split('\n') if len(i) > 0}

def bro_jar_to_dic(cookies):
    return {cookie['name']: cookie['value'] for cookie in cookies}

def load_js(js_path, jscode):
    with open(js_path, 'r') as f:
        content = f.read()
    ctx = execjs.compile(content)
    return ctx.eval(jscode)