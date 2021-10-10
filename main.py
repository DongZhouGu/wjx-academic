"""
@Time ： 2020-11-30 12:41
@Auth ： DongZhou GU
@File ：main.py
@IDE ：PyCharm
"""
import asyncio
import re

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


async def submit_choice(q, choice):
    answers = await q.querySelectorAll('.ui-radio')
    flag = False
    for i, answer in enumerate(answers):
        text = await (await answer.getProperty('textContent')).jsonValue()
        if choice in text:
            flag = True
            break
    if flag:
        return await answers[i].click()
    # 都没匹配到 随便选第一个
    else:
        return await answers[0].click()


async def submit_text(q, text):  # 填空题
    text_area = await q.querySelector('input')
    await text_area.type(text)


async def submit_code(q, div_string, keyword):  # 特殊人工验证
    text_area = await q.querySelector('input')
    i = div_string.rfind(keyword) + len(keyword)
    j = max(div_string.rfind("("), div_string.rfind("（"), -1)

    res = []
    res.append(re.compile(r'"(.*)"').findall(div_string[i:j]))
    res.append(re.compile(r'“(.*)”').findall(div_string[i:j]))
    res.append(re.compile(r'"(.*)”').findall(div_string[i:j]))
    res.append(re.compile(r'“(.*)"').findall(div_string[i:j]))
    flag = False
    for i, r in enumerate(res):
        if r:
            flag = True
            break
    if flag:
        await text_area.type(res[i][0])
    else:
        num = re.findall(r'[1-9]+\.?[0-9]*', div_string[i:j])
        await text_area.type(num[0])


async def main_logic_text(q, div_string):
    if "姓名" in div_string or "名字" in div_string:
        await submit_text(q, info["name"])
    elif "联系方式" in div_string or "手机" in div_string or "电话" in div_string:
        await submit_text(q, info["phone"])
    elif "学号" in div_string:
        await submit_text(q, info["id"])
    elif "身份证" in div_string:
        await submit_text(q, info["card_id"])
    elif "专业" in div_string:
        await submit_text(q, info["major"])
    elif "年级" in div_string:
        await submit_text(q, info["grade"])
    elif "性别" in div_string:
        await submit_text(q, info["gender"])
    elif "输入" in div_string:
        await submit_code(q, div_string, "输入")
    elif "填写" in div_string:
        await submit_code(q, div_string, "填写")
    else:
        await submit_text(q, "1")


async def main_logic_choice(q, div_string):
    if "专业" in div_string:
        await submit_choice(q, info["major"])
    elif "年级" in div_string:
        await submit_choice(q, info["grade"])
    elif "性别" in div_string:
        await submit_choice(q, info["gender"])
    else:
        answers = await q.querySelectorAll('.ui-radio')
        answers[0].click()


async def submit(page, questions, info):
    for i, q in enumerate(questions):
        element = await q.querySelector(f'#div{i + 1} > div.field-label')
        div_string = await (await element.getProperty('textContent')).jsonValue()
        # 是填空题
        if await q.querySelectorAll('.ui-input-text'):
            await main_logic_text(q, div_string)
        # 是选择题
        elif await q.querySelectorAll('.ui-radio'):
            await main_logic_choice(q, div_string)

    time.sleep(0.5)
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
    global info
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
                            page.querySelectorAll('.field')])
                        questions = await page.querySelectorAll('.field')
                        # print(questions)
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
