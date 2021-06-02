import requests, execjs, os, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ChromeOptions


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


    def head_bro(self):
        bro = webdriver.Chrome(executable_path='/Users/wei/workspace/chromedriver', options=self.options)
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


    def login_tb(self, username, password, view_bro=False):
        """
        username: 账号
        password: 密码
        view_bro: 浏览器的可视化
        """
        if not view_bro:
            bro = self.head_bro()
        else:
            bro = self.headless_bro()
        url = 'https://login.taobao.com/member/login.jhtml'
        bro.get(url)
        time.sleep(1)
        bro.find_element_by_xpath('//*[@id="fm-login-id"]').send_keys(username)
        time.sleep(1)
        bro.find_element_by_xpath('//*[@id="fm-login-password"]').send_keys(password)
        time.sleep(1)
        bro.find_element_by_xpath('//*[@id="login-form"]/div[4]/button').click()
        time.sleep(3)
        # print(bro.page_source)
        # with open('tb.html', 'w') as f:
        #     f.write(bro.page_source)
        return bro


