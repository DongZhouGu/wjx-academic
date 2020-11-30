"""
@Time ： 2020-10-22 12:41
@Auth ： DongZhou GU
@File ：main.py
@IDE ：PyCharm
"""
from selenium import webdriver
from selenium.webdriver import ChromeOptions
import time
from time import ctime, mktime
import yaml


class submit():
    def __init__(self, browser, questions,info):
        self.browser = browser
        self.questions = questions
        self.info=info

    def re_random(self, num, div_string):
        if "姓名" in div_string or "名字" in div_string:
            self.submit_text(num, self.info["name"])
        elif "联系方式" in div_string or "手机" in div_string or "电话" in div_string:
            self.submit_text(num, self.info["phone"])
        elif "学号" in div_string:
            self.submit_text(num, self.info["id"])
        elif "身份证" in div_string:
            self.submit_text(num, self.info["card_id"])
        elif "专业" in div_string:
            self.submit_text(num, self.info["major"])
        elif "年级" in div_string:
            self.submit_choice(num)
        elif "性别" in div_string:
            self.submit_choice(num)
        else:
            if (self.is_choice(num) == False):
                self.submit_text(num, "1")

    def post(self, info):
        for i in range(len(self.questions)):
            div_string = self.questions[i].find_element_by_class_name('field-label').get_attribute("innerHTML")
            self.re_random(i, div_string)
        self.browser.find_element_by_id('ctlNext').click()
        time.sleep(20)
        print(f'时间: {ctime()}==== {info["name"]}提交成功！')

    def submit_choice(self, num):
        answers = self.questions[num].find_elements_by_class_name('ui-radio')
        for answer in answers:
            text = answer.text
            if '20' in text or '男' in text or '研一' in text:
                return answer.click()

    def submit_text(self, question_number, text):  # 填空题
        text_area = self.questions[question_number].find_element_by_css_selector('input')
        text_area.clear()
        text_area.send_keys(text)



    def is_choice(self, num):
        answers = self.questions[num].find_elements_by_class_name('ui-radio')
        if answers == None:
            return False
        else:
            answers[0].click()
            return True


# 加载yaml
def load_config(config_path):
    with open(config_path, encoding='utf8') as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def need_weixin(config):
    url = config['url']
    index = url.find('.aspx&response_type')
    index2 = url.find("state=sojump")
    url = url[:index - 8] + config['wjx_id'][-13:-5] + url[index:index2 + 12] + "&connect_redirect=1" + url[
                                                                                                        index2 + 12:]
    target_time = config['target_time']
    useragent = config['user-agent']
    option = ChromeOptions()
    option.add_argument(f'--user-agent={useragent}')
    option.add_experimental_option('excludeSwitches', ['enable-automation'])

    # 下面两行取消注释即可 浏览器不跳出来
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(executable_path='chromedriver.exe', options=option)
    target_time = mktime(time.strptime(target_time, "%Y-%m-%d %H:%M:%S"))

    for i, info in enumerate(config['users']):
        while (True):
            if (time.time() > target_time):
                browser.get(url)
                yes = browser.find_element_by_id('btnOk')
                while (yes == None):
                    browser.refresh()
                    yes = browser.find_element_by_id('btnOk')
                # yes = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'btnOk')))
                yes.click()
                break
            else:
                print(f'时间: {ctime()}====等待中')
                time.sleep(1)
        print(f'时间: {ctime()}===={info["name"]}开始提交')
        questions = browser.find_elements_by_css_selector('.field')
        while (len(questions) == 0):
            time.sleep(0.5)
            browser.refresh()
            questions = browser.find_elements_by_css_selector('.field')

        submit(browser, questions,info).post(info)

    print(f'时间: {ctime()}====任务完成')


def deneed_weixin(config):
    url = "https://www.wjx.cn/m/"+config['wjx_id'][-13:]
    target_time = config['target_time']
    useragent = config['user-agent']
    option = ChromeOptions()
    option.add_argument(f'--user-agent={useragent}')
    option.add_experimental_option('excludeSwitches', ['enable-automation'])

    # 下面两行取消注释即可 浏览器不跳出来
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(executable_path='chromedriver.exe', options=option)
    target_time = mktime(time.strptime(target_time, "%Y-%m-%d %H:%M:%S"))
    for i, info in enumerate(config['users']):
        while (True):
            if (time.time() > target_time):
                browser.get(url)
                break
            else:
                print(f'时间: {ctime()}====等待中')
                time.sleep(1)
        print(f'时间: {ctime()}===={info["name"]}开始提交')
        questions = browser.find_elements_by_css_selector('.field')
        print(questions)
        while (len(questions) == 0):
            time.sleep(0.5)
            browser.refresh()
            questions = browser.find_elements_by_css_selector('.field')
            print(questions)
        submit(browser, questions,info).post(info)

    print(f'时间: {ctime()}====任务完成')


if __name__ == "__main__":
    config = load_config("setting_config.yaml")
    flag = config['need_weixin']
    if (flag == "true"):
        need_weixin(config)
    if (flag == "false"):
        deneed_weixin(config)
