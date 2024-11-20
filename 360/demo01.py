# -*- coding: utf-8 -*-
# @Time    : 2024/11/14 16:09
# @Author  : 烂泥
# @FileName: demo01.py
# @Version : v1.0
# @Description:
import json
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def login():
    global driver
    url = 'https://quake.360.net/quake/login#/'
    driver = webdriver.Chrome(executable_path='D:\Code\python_code\linux_code\spider\chromedriver.exe')

    driver.implicitly_wait(30)
    driver.get(url)
    time.sleep(3)
    driver.find_element(By.XPATH, '//*[@id="login"]/div/div[2]/div/div/div/div[2]/form/div[1]/div/div/input').send_keys(
        'smyolo')
    time.sleep(3)
    driver.find_element(By.XPATH, '//*[@id="login"]/div/div[2]/div/div/div/div[2]/form/div[2]/div/div/input').send_keys(
        'a19980407')#输入你的密码
    time.sleep(3)
    driver.find_element(By.XPATH, '//*[@id="login"]/div/div[2]/div/div/div/div[2]/form/div[5]/input').click()
    time.sleep(20)


def get_all(name):
    domain_set = set()
    driver.get('https://quake.360.net/quake/#/index')
    time.sleep(1)
    driver.find_element(By.XPATH,
                        '//*[@id="app droptarget"]/div[1]/section/main/div[1]/div/div/div[1]/div/div[2]/div/div[1]/div[1]/input').send_keys(
        f'domain:"{name}"')
    time.sleep(1)
    driver.find_element(By.XPATH,
                        '//*[@id="app droptarget"]/div[1]/section/main/div[1]/div/div/div[1]/div/div[2]/div/div[1]/span').click()
    count = 1

    while True:
        count += 1
        time.sleep(5)
        datas = driver.find_elements(By.XPATH,
                                     '//*[contains(@id, "app droptarget")]/div[1]/section/main//span[@class="copy_btn"]')

        for data in datas:
            # domain = data.find_element(By.CSS_SELECTOR, '//*[@id="app droptarget"]/div[1]/section/main/div[1]/div/div[2]/div/div[2]/div[2]/div[2]/div/div[1]/div/div[1]/div[1]/div[1]/div[1]/div[1]/span')

            domain_set.add(data.text)
        try:
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'btn-next'))
            )
            print("成功获取到下一页按钮了")
            button.click()
            # time.sleep(13)
            # driver.find_element(By.XPATH,'//*[@id="app droptarget"]/div[1]/section/main/div[1]/div/div[2]/div/div[2]/div[2]/div[2]/div/div[1]/div/div[1]/div[11]/div/button[2]/i').click()
        except:
            f = open(f'./{name}_domain.txt', 'w', encoding='utf-8')
            f.write('\n'.join(domain_set))
            f.close()
            break


def main():
    login()
    with open('name.txt', 'r', encoding='utf-8') as name_file:
        for name in name_file:
            name = name.strip()
            get_all(name.strip())


def get_domain():
    resules = set()
    f = open('./aecom.com.txt', 'a', encoding='utf-8', newline='')
    with open('l3harris.txt', 'r', encoding='utf-8',errors='ignore') as file:
        json_data = json.load(file)
        for _ in json_data["data"]:
            datas = _['data']
            for data in datas:
                # f.write(data['service']['http']['host'] + '\n')
                resules.add(data['service']['http']['host'])
    f.write('\n'.join(resules))
    f.close()


if __name__ == '__main__':
    main()
    # get_domain()
