"""
@Time ： 2020-10-22 12:41
@Auth ： DongZhou GU
@File ：main.py
@IDE ：PyCharm

"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from time import ctime, mktime
import yaml
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


class submit():
    def __init__(self, browser, questions):
        self.browser = browser
        self.questions = questions

    def re_random(self, num, div_string):
        if "姓名" in div_string:
            self.submit_text(num, info["name"])
        elif "联系方式" in div_string:
            self.submit_text(num, info["phone"])
        elif "学号" in div_string:
            self.submit_text(num, info["id"])
        elif "年级" in div_string:
            self.submit_choice(num)
        elif "性别" in div_string:
            self.submit_choice(num)

    def post(self, info):
        for i in range(len(self.questions)):
            div_string = self.questions[i].find_element_by_class_name('field-label').get_attribute("innerHTML")
            self.re_random(i, div_string)
        # self.browser.find_element_by_id('ctlNext').click()
        time.sleep(0.5)
        print(f'时间: {ctime()}==== {info["name"]}提交成功！')

    def submit_choice(self, num):
        answers = self.questions[num].find_elements_by_class_name('ui-radio')
        for answer in answers:
            text = answer.text
            if '20' in text or '男' in text:
                return answer.click()

    def submit_text(self, question_number, text):  # 填空题
        text_area = self.questions[question_number].find_element_by_css_selector('input')
        text_area.clear()
        text_area.send_keys(text)


# 加载yaml
def load_config(config_path):
    with open(config_path, encoding='utf8') as f:
        return yaml.load(f, Loader=yaml.FullLoader)


if __name__ == "__main__":
    config = load_config("setting_config.yaml")
    url = config['url']
    index = url.find('.aspx&response_type')
    url = url[:index - 8] + config['wjx_id'] + url[index:]
    target_time = config['target_time']
    useragent = config['user-agent']
    chrome_options = Options()
    chrome_options.add_argument(f'--user-agent={useragent}')
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=chrome_options)
    target_time = mktime(time.strptime(target_time, "%Y-%m-%d %H:%M:%S"))

    for i, info in enumerate(config['users']):
        browser.get(url)
        time.sleep(1)
        yes = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'btnOk')))
        while (True):
            if (time.time() > target_time):
                yes.click()
                break
            else:
                print(f'时间: {ctime()}====等待中')
        print(f'时间: {ctime()}===={info["name"]}开始提交')
        questions = browser.find_elements_by_css_selector('.field')
        while (len(questions) == 0):
            questions = browser.find_elements_by_css_selector('.field')
        submit(browser, questions).post(info)

    print(f'时间: {ctime()}====任务完成')
