import requests, execjs, os, time, pickle
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ChromeOptions


def bro_str_to_dic(x):
    return {x[:x.find(':')]: x[x.find(':') + 1:].strip() for x in str.strip().split('\n')}


def cookiesStrToDic(s):
    return {i.split('=')[0].strip(): i.split('=')[1].strip() for i in s.split('; ')}

def cookie_jar_to_str(cookies):
    cookies_str = ''
    for key ,value in requests.utils.dict_from_cookiejar(cookies).items():
        cookies_str += key + '=' + value + ';' + ' '
    return cookies_str[:-2]

def headerStrToDic(s):
    return {i.split(': ')[0].strip(): i.split(': ')[1].strip() if len(i.split(': ')) > 1 else '' for i in s.split('\n') if len(i.split(': ')) > 1}

def runJs(js_path, jscode):
    with open(js_path, 'r') as f:
        content = f.read()
    ctx = execjs.compile(content)
    return ctx.eval(jscode)

def load_cookies(cookies_path):
    with open(cookies_path, 'rb') as f:
        cookies = pickle.load(f)
    return cookies




class Hidden_Bro():
    def __init__(self):
        self.options = ChromeOptions()
        self.options.add_argument("start-minimized")
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.options.add_experimental_option("useAutomationExtension", False)
    def write_identity(self):
        url = 'https://raw.githubusercontent.com/kingname/stealth.min.js/main/stealth.min.js'
        resp = requests.get(url)
        with open('identity.txt', 'w') as f:
            f.write(resp.text)

    def read_identity(self):
        with open('identity.txt', 'r') as f:
            identity = f.read()
        return identity

    def headless_bro(self):
        chrome_options = Options()
        # chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--headless')
        # options = ChromeOptions()
        # options.add_argument("start-minimized")
        # options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # options.add_experimental_option("useAutomationExtension", False)
        bro = webdriver.Chrome(executable_path='/Users/wei/workspace/chromedriver', chrome_options=chrome_options, options=self.options)
        if os.path.exists('./identity.txt'):
            js = self.read_identity()
            bro.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": js
            })
            # driver.minimize_window()
            return bro
        else:
            self.write_identity()
            return self.headless_bro()


    def head_bro(self, port=None):
        bro = webdriver.Chrome(executable_path='E:/chromedriver.exe', options=self.options)
        if port:
            self.options.add_argument(f'--proxy-server=http://127.0.0.1:{port}')  
        if os.path.exists('./identity.txt'):
            js = self.read_identity()
            bro.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": js
            })
            # driver.minimize_window()
            return bro
        else:
            self.write_identity()
            return self.head_bro()


    

# 各大网站的登录 selenium版
class login_web():
    def __init__(self, view_bro=False, port=None):
        if not view_bro:
            self.bro = Hidden_Bro().head_bro(port)
        else:
            self.bro = Hidden_Bro().headless_bro()

    def login_tb(self, username, password):
        """
        username: 账号
        password: 密码
        view_bro: 浏览器的可视化
        """
        url = 'https://login.taobao.com/member/login.jhtml'
        self.bro.get(url)
        time.sleep(1)
        self.bro.find_element_by_xpath('//*[@id="fm-login-id"]').send_keys(username)
        time.sleep(1)
        self.bro.find_element_by_xpath('//*[@id="fm-login-password"]').send_keys(password)
        time.sleep(1)
        self.bro.find_element_by_xpath('//*[@id="login-form"]/div[4]/button').click()
        time.sleep(3)
        return self.bro
    
    def login_tb_cookies(self, cookies):
        if type(cookies) == str:
            cookies = cookiesStrToDic(cookies)
        self.bro.get("https://www.taobao.com")
        for cookie in cookies:
            self.bro.add_cookie({
                "domain":".taobao.com",
                "name":cookie,
                "value":cookies[cookie],
                "path":'/',
                "expires":None
            })
        self.bro.get("https://www.taobao.com")
        return self.bro

if __name__ == '__main__':
    # cookies = "thw=cn; hng=CN%7Czh-CN%7CCNY%7C156; cna=SNKXGFvrbxgCAXFE4HZczSFH; lgc=pgalimkt; tracknick=pgalimkt; mt=ci=7_1; sgcookie=E1006AiGcC6K3p69FtU%2BmESGo2fzBzrOhrK5BkPRGxWiuEkrXDdAnFH5SDOP9v01RxkxkcCPAHmFPvw2PSbOaGxaJg%3D%3D; _cc_=Vq8l%2BKCLiw%3D%3D; xlly_s=1; _m_h5_tk=5ef57936b24f9f9621726dd714506ee8_1623128399851; _m_h5_tk_enc=dd69db3fdb7058d9a77292d0230c0c6f; t=a2c9a1a583b2bb22b6022fe22524183b; _tb_token_=37ee90b33e1b; uc1=cookie14=Uoe2zshs80wyQw%3D%3D; isg=BHV1J6aVeYq83p0AmVTNgC3QhPEv8ikEioM1ZveaOuw7zpXAv0Cx1YdEGJJ4iUG8; l=eBNH4x-HjXEXgrWtBOfanurza77OSIRYYuPzaNbMiOCPOh5B592GW6_UcbY6C3GVh6-MR3l-cR2XBeYBqQAonxvtIosM_Ckmn; tfstk=cmuCBy_7g9XBn6xP8XONYc8z6QaRwX__sN2ZOmeBwXT3y-1DiZyb_6VCCNEY1"
    # tb_login = login_web(port=9000).login_tb_cookies(cookies)
    tb_login = login_web(port=9000).login_tb(username='pgalimkt', password='2021pgalimkt')
    time.sleep(3)
    # tb_login.execute_script('document.querySelector("#q").value="小米12"; document.querySelector("#J_TSearchForm > div.search-button > button").click()')
    tb_login.find_element_by_xpath('//*[@id="q"]').send_keys('小米12')
    time.sleep(3)
    tb_login.find_element_by_xpath('//*[@id="J_TSearchForm"]/div[1]/button').click()
    time.sleep(3)
    tb_login.close()
    time.sleep(3)
    handles = tb_login.window_handles
    tb_login.switch_to_window(handles[0])
    with open('tb.html', 'w', encoding='utf-8') as f:
        f.write(tb_login.page_source)
