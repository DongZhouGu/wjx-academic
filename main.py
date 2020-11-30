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


# 加载yaml
def load_config(config_path):
    with open(config_path, encoding='utf8') as f:
        return yaml.load(f, Loader=yaml.FullLoader)


async def submit_choice(questions, num):
    answers = await questions[num].querySelectorAll('.ui-radio')
    for answer in answers:
        text = await (await answer.getProperty('textContent')).jsonValue()
        print(text)
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
        print(div_string)
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
    print(f'时间: {ctime()}==== {info["name"]}提交成功！')
    time.sleep(10)


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
                await page.goto(url)
                if (flag == "true"):
                    await asyncio.wait([
                        page.click('#btnOk'),
                        page.waitForNavigation(),
                    ])
                break
            else:
                print(f'时间: {ctime()}====等待中')
                time.sleep(1)

        print(f'时间: {ctime()}===={info["name"]}开始提交')
        questions = await page.querySelectorAll('.field')
        await submit(page, questions, info)

    print(f'时间: {ctime()}====任务完成')
    # 关闭浏览器
    # await browser.close()


# 运行入口
if __name__ == '__main__':
    config = load_config("setting_config.yaml")
    flag = config['need_weixin']
    if (flag == "true"):
        url = config['url']
        index = url.find('.aspx&response_type')
        index2 = url.find("state=sojump")
        url = url[:index - 8] + config['wjx_id'][-13:-5] + url[index:index2 + 12] + "&connect_redirect=1" + url[
                                                                                                            index2 + 12:]
    if (flag == "false"):
        url = "https://www.wjx.cn/m/" + config['wjx_id'][-13:]

    useragent = config['user-agent']

    asyncio.get_event_loop().run_until_complete(main())
