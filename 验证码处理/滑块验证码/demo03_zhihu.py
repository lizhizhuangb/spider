# -*- coding: utf-8 -*-
# @Time    : 2024/11/20 16:47
# @Author  : 烂泥
# @FileName: demo03_zhihu.py
# @Version : v1.0
# @Description:
import time

import ddddocr
import requests
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


def open_page():
    global driver
    url = 'https://www.zhihu.com/'
    driver = webdriver.Chrome(executable_path='D:\Code\python_code\linux_code\spider\chromedriver.exe')
    driver.get(url)
    tag = WebDriverWait(driver, 30, 0.5).until(lambda driver: driver.find_elements(By.CLASS_NAME, 'SignFlow-tab')[-1])
    tag.click()

    tag = WebDriverWait(driver, 30, 0.5).until(lambda driver: driver.find_element(By.XPATH,
                                                                                  '//*[@id="root"]/div/main/div/div/div/div/div[2]/div/div[1]/div/div[1]/form/div[2]/div/label/input'))
    tag.send_keys('******')
    tag = WebDriverWait(driver, 30, 0.5).until(lambda driver: driver.find_element(By.XPATH,
                                                                                  '//*[@id="root"]/div/main/div/div/div/div/div[2]/div/div[1]/div/div[1]/form/div[3]/div/label/input'))
    tag.send_keys('******')

    login_button = WebDriverWait(driver, 30, 0.5).until(
        lambda driver: driver.find_element_by_class_name('SignFlow-submitButton'))
    login_button.click()


def find_png():
    global slice_url, back_url
    slice_url = WebDriverWait(driver, 30, 0.5).until(
        lambda driver: driver.find_element(By.CLASS_NAME, 'yidun_jigsaw').get_attribute('src'))
    back_url = WebDriverWait(driver, 30, 0.5).until(
        lambda driver: driver.find_element(By.CLASS_NAME, 'yidun_bg-img').get_attribute('src'))


def get_target():
    slice_bytes = requests.get(slice_url).content
    back_bytes = requests.get(back_url).content
    slide = ddddocr.DdddOcr(show_ad=False, ocr=False, det=False)

    res = slide.slide_match(slice_bytes, back_bytes, simple_target=True)
    x1, y1, x2, y2 = res['target']
    print(x1, y1, x2, y2)  # 196 12 276 92

    # 6.滑动滑块
    tag = WebDriverWait(driver, 30, 0.5).until(
        lambda driver: driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div/div[2]/div/div[2]/div[2]'))
    time.sleep(2)
    ActionChains(driver).click_and_hold(tag).perform()  # 点击并抓住标签
    ActionChains(driver).move_by_offset(xoffset=x1+6, yoffset=0).perform()  # 向右滑动114像素（向左是负数）
    ActionChains(driver).release().perform()  # 释放

    time.sleep(3)


if __name__ == '__main__':
    open_page()
    while 1:
        find_png()
        get_target()
