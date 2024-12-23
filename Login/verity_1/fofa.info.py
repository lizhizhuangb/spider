# -*- coding: utf-8 -*-
# @Time    : 2024/12/23 14:59
# @Author  : 秋秋
# @FileName: fofa.info.py
# @Version : v1.0
# @Description:
import random
import time

import ddddocr
from selenium import webdriver
from selenium.webdriver.common.by import By


def login():
    # 初始url
    url = 'https://i.nosec.org/login?locale=zh-CN&service=https:%2F%2Ffofa.info%2Ff_login'

    # 初始化webdriver
    driver = webdriver.Chrome(executable_path='D:\Code\python_code\linux_code\spider\chromedriver.exe')
    driver.implicitly_wait(30)

    # 请求fofa.info
    driver.get(url)

    # 获取account password verity
    account = driver.find_element(By.XPATH, '//*[@id="username"]')
    password = driver.find_element(By.XPATH, '//*[@id="password"]')
    verity = driver.find_element(By.XPATH, '//*[@id="login-form"]/table/tbody/tr[3]/td/input')

    account.send_keys('s**********il.com')
    time.sleep(random.randrange(1, 3))
    password.send_keys('Q*****5.')
    time.sleep(random.randrange(1, 3))

    verity_element = driver.find_element(By.XPATH, '//*[@id="captcha_image"]')
    verity_element.screenshot('verity.png')
    img_content = open('verity.png', 'rb').read()

    ocr = ddddocr.DdddOcr(show_ad=False)
    result = ocr.classification(img_content)

    verity.send_keys(result)
    driver.find_element(By.XPATH, '//*[@id="fofa_service"]').click()
    driver.find_element(By.XPATH, '//*[@id="login-form"]/table/tbody/tr[5]/td/button').click()

    time.sleep(10)


def main():
    login()


if __name__ == '__main__':
    main()
