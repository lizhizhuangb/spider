# -*- coding: utf-8 -*-
# @Time    : 2024/11/20 16:03
# @Author  : 烂泥
# @FileName: demo02.py
# @Version : v1.0
# @Description:
# 进入验证码相关的页面
import re
import time

import requests
import ddddocr
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


def open_page():
    global driver
    driver = webdriver.Chrome(executable_path='D:\Code\python_code\linux_code\spider\chromedriver.exe')
    url = 'https://www.geetest.com/adaptive-captcha-demo'
    driver.get(url)
    tag = WebDriverWait(driver, 30, 0.5).until(lambda dv: dv.find_element(By.XPATH,
                                                                          '//*[@id="gt-showZh-mobile"]/div/section/div/div[2]/div[1]/div[2]/div[3]/div[3]'))
    tag.click()

    # tag = WebDriverWait(driver, 30, 0.5).until(lambda dv: dv.find_element(By.XPATH, '//*[@id="captcha"]/div[2]/div[1]/div[1]'))
    tag = WebDriverWait(driver, 30, 0.5).until(lambda dv: dv.find_element(By.CLASS_NAME, 'geetest_btn_click'))
    tag.click()


def find_png():
    global slice_url, back_url
    slice_png_element = driver.find_element(By.CLASS_NAME, 'geetest_slice_bg').get_attribute("style")
    slice_url = re.findall(r'"(.*?)"', slice_png_element)[0]
    print(slice_url)
    back_png_element = driver.find_element(By.CLASS_NAME, 'geetest_bg').get_attribute("style")
    back_url = re.findall(r'"(.*?)"', back_png_element)[0]
    print(back_url)


def get_target():
    slice_bytes = requests.get(slice_url).content
    back_bytes = requests.get(back_url).content
    slide = ddddocr.DdddOcr(show_ad=False, det=False, ocr=False)
    res = slide.slide_match(slice_bytes, back_bytes, simple_target=True)
    x1, y1, x2, y2 = res['target']
    print(x1, y1, x2, y2)  # 196 12 276 92

    # 6.滑动滑块
    tag = driver.find_element(By.CLASS_NAME, 'geetest_btn')
    time.sleep(2)
    ActionChains(driver).click_and_hold(tag).perform()  # 点击并抓住标签
    ActionChains(driver).move_by_offset(xoffset=x1, yoffset=0).perform()  # 向右滑动114像素（向左是负数）
    ActionChains(driver).release().perform()  # 释放

    time.sleep(3)

if __name__ == '__main__':
    open_page()
    find_png()
    get_target()
