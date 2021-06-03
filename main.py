"""
@Time ： 2020-11-30 12:41
@Auth ： DongZhou GU
@File ：main.py
@IDE ：PyCharm
"""
import asyncio
from pyppeteer import launch
import time
from time import ctime, mktime
import yaml
import os

# 加载yaml
from pyppeteer.errors import ElementHandleError


def load_config(config_path):
    with open(config_path, encoding='utf8') as f:
        return yaml.load(f, Loader=yaml.FullLoader)


async def submit_choice(questions, num):
    answers = await questions[num].querySelectorAll('.ui-radio')
    for answer in answers:
        text = await (await answer.getProperty('textContent')).jsonValue()
        if '20' in text or '男' in text or '研一' in text:
            return await answer.click()


async def submit_text(questions, num, text):  # 填空题
    text_area = await questions[num].querySelector('input')
    await text_area.type(text)


async def is_choice(questions, num):
    answers = await questions[num].querySelectorAll('.ui-radio')
    if answers == None:
        return False
    else:
        await answers[0].click()
        return True


async def submit(page, questions, info):
    for num in range(len(questions)):
        element = await questions[num].querySelector(f'#div{num + 1} > div.field-label')
        div_string = await (await element.getProperty('textContent')).jsonValue()
        if "姓名" in div_string or "名字" in div_string:
            await submit_text(questions, num, info["name"])
        elif "联系方式" in div_string or "手机" in div_string or "电话" in div_string:
            await submit_text(questions, num, info["phone"])
        elif "学号" in div_string:
            await submit_text(questions, num, info["id"])
        elif "身份证" in div_string:
            await submit_text(questions, num, info["card_id"])
        elif "专业" in div_string:
            await submit_text(questions, num, info["major"])
        elif "年级" in div_string:
            await submit_choice(questions, num)
        elif "性别" in div_string:
            await submit_choice(questions, num)
        else:
            if (await is_choice(questions, num) == False):
                await submit_text(questions, num, "1")
    # time.sleep(100)
    submitb = await page.querySelector('#ctlNext')
    await submitb.click()
    time.sleep(1)
    print(f'时间: {ctime()}==== {info["name"]}提交成功！不管是否爆红，请查看result.png截图进行验证！')
    time.sleep(2)
    # 登录成功截图
    await page.screenshot({'path': './result.png', 'quality': 100, 'fullPage': True})
    time.sleep(2)


# 主函数
async def main():
    target_time = config['target_time']
    browser = await launch({'headless': False,
                            'dumpio': True,
                            'ignoreDefaultArgs': ["--enable-automation"],
                            'args': [
                                # '--disable-extensions',
                                # '--disable-bundled-ppapi-flash',
                                # '--mute-audio',
                                # '--no-sandbox',
                                # '--disable-setuid-sandbox',
                                '--disable-gpu',
                            ]})
    # 打开新标签页
    page = await browser.newPage()
    await page.setUserAgent(useragent)
    target_time = mktime(time.strptime(target_time, "%Y-%m-%d %H:%M:%S"))

    for i, info in enumerate(config['users']):
        while (True):
            if (time.time() > target_time):
                await page.goto(url, {'timeout': 1000 * 60})
                if (flag == "true"):
                    ok = await page.querySelector('#btnOk')
                    if (ok != None):
                        await asyncio.wait([
                            ok.click(),
                            page.waitForNavigation({'timeout': 1000 * 60}),
                        ])
                        # await asyncio.wait([
                        #     page.querySelectorAll('.field'), page.waitForNavigation({'timeout': 50000}), ])
                        await asyncio.wait([
                            page.querySelectorAll('.field') ])
                        questions = await page.querySelectorAll('.field')
                        print(questions)
                        if (len(questions) != 0): break
                else:
                    questions = await page.querySelectorAll('.field')
                    if (len(questions) != 0): break
            else:
                print(f'时间: {ctime()}====等待中')
                time.sleep(1)

    print(f'时间: {ctime()}===={info["name"]}开始提交')
    await submit(page, questions, info)
    print(f'时间: {ctime()}====任务完成')
    # 关闭浏览器
    # await browser.close()


# 运行入口
if __name__ == '__main__':
    if os.path.exists("./result.png"):
        os.remove("./result.png")
    config = load_config("setting_config.yaml")
    flag = config['need_weixin']
    ind = config['wjx_id'].rfind('/')
    ind2 = config['wjx_id'].rfind('.aspx')
    if (flag == "true"):
        url = config['url']
        index = url.find('.aspx&response_type')
        index2 = url.find("state=sojump")
        url = url[:index - 7] + config['wjx_id'][ind + 1:ind2] + url[index:index2 + 12] + "&connect_redirect=1" + url[
                                                                                                                  index2 + 12:]
    if (flag == "false"):
        url = "https://www.wjx.cn/vm" + config['wjx_id'][ind:]

    useragent = config['user-agent']
    asyncio.get_event_loop().run_until_complete(main())
