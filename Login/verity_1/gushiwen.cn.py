# -*- coding: utf-8 -*-
# @Time    : 2024/12/23 13:46
# @Author  : 秋秋
# @FileName: gushiwen.cn.py
# @Version : v1.0
# @Description:
import logging
import random
import time
import ddddocr

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By


def login():
    # 初始url
    url = 'https://www.gushiwen.cn/user/login.aspx?from=http://www.gushiwen.cn/user/collect.aspx'

    # 初始化webchrome
    driver = webdriver.Chrome(executable_path='D:\Code\python_code\linux_code\spider\chromedriver.exe')
    driver.get(url)

    driver.implicitly_wait(30)

    # 获取acc和pwd
    account = driver.find_element(By.XPATH, '//*[@id="email"]')
    password = driver.find_element(By.XPATH, '//*[@id="pwd"]')
    verity = driver.find_element(By.XPATH, '//*[@id="code"]')

    # 输入账号密码
    account.send_keys('starplm@163.com')
    time.sleep(random.randrange(1, 3))
    password.send_keys('1992128x')
    time.sleep(random.randrange(1, 3))

    # 获取验证码的图片
    verity_url = driver.find_element(By.XPATH, '//*[@id="imgCode"]')  # .get_attribute('src')
    verity_url.screenshot('verity.png')
    img_content = open('verity.png', 'rb').read()
    # logging.info(verity_url)
    # img_content = requests.get(verity_url).content

    # 获取验证码的结果
    ocr = ddddocr.DdddOcr(show_ad=False)
    result = ocr.classification(img_content)
    logging.info(result)
    verity.send_keys(result)

    driver.find_element(By.XPATH, '//*[@id="denglu"]').click()

    print("成功登录")



def main():
    login()


if __name__ == '__main__':
    main()
