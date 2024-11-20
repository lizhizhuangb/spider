# -*- coding: utf-8 -*-
# @Time    : 2024/11/8 13:27
# @Author  : 烂泥
# @FileName: slider.py
# @Version : v1.0
# @Description:
# 本案例以网站geetest为例，进行滑块验证码的识别


from PIL import Image
from selenium import webdriver
import os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Slider:
    # 初始化
    def __init__(self, browser, c_slice, c_background, c_full_img):
        self.browser = browser
        self.c_slice = c_slice
        self.c_background = c_background
        self.c_full_img = c_full_img

    def hide_element(self, element):
        self.browser.execute_script("arguments[0].style=arguments[1]", element, "display: none;")

    # 设置元素可见
    def show_element(self, element):
        self.browser.execute_script("arguments[0].style=arguments[1]", element, "display: block;")

    # 对三个图像进行截图
    def get_img(self):
        # 隐藏需要滑块的图片
        self.hide_element(self.c_slice)
        self.hide_element(self.c_full_img)
        # 保存有缺口的图片
        self.save_screenshot(self.c_background, 'back')
        # 显示需要滑动的图片
        self.show_element(self.c_slice)
        self.hide_element(self.c_background)
        # 保存滑块的图片
        self.save_screenshot(self.c_slice, 'slice')
        # 显示完整的图片
        self.show_element(self.c_full_img)
        self.hide_element(self.c_background)
        self.hide_element(self.c_slice)
        # 保存完整的图片
        self.save_screenshot(self.c_full_img, 'full')

    def save_screenshot(self, obj, name):
        """
        保存指定元素的截图，考虑屏幕缩放比例

        Parameters:
            obj: WebElement对象，要截图的网页元素
            name: str，保存的文件名（不带扩展名）
        """
        try:
            # 获取浏览器的缩放比例
            scale_ratio = self.browser.execute_script('return window.devicePixelRatio;')

            # 首先对整个页面进行截图
            pic_url = self.browser.save_screenshot('.\\login.png')
            print("%s:截图成功!" % pic_url)

            # 获取元素的位置和大小信息，并根据缩放比例调整
            rect = obj.rect
            left = int(rect['x'] * scale_ratio)
            top = int(rect['y'] * scale_ratio)
            right = int((rect['x'] + rect['width']) * scale_ratio)
            bottom = int((rect['y'] + rect['height']) * scale_ratio)

            # 打印位置信息用于调试
            print('图：' + name)
            print('Left %s' % left)
            print('Top %s' % top)
            print('Right %s' % right)
            print('Bottom %s' % bottom)
            print('Scale Ratio: %s' % scale_ratio)
            print('')

            # 打开截图并裁剪
            im = Image.open('login.png')

            # 确保裁剪区域不超出图片范围
            img_width, img_height = im.size
            left = max(0, min(left, img_width))
            top = max(0, min(top, img_height))
            right = max(0, min(right, img_width))
            bottom = max(0, min(bottom, img_height))

            # 裁剪图片
            if left < right and top < bottom:
                im = im.crop((left, top, right, bottom))
                file_name = name + '.png'
                im.save(file_name)
            else:
                raise ValueError("Invalid crop dimensions")

        except Exception as msg:
            print("%s:截图失败!" % msg)



def main():
    url = 'https://www.geetest.com/demo/slide-float.html'
    path = '/spider/chromedriver.exe'
    chrome_options = Options()
    chrome_options.add_argument('--start-maximized')
    browser = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)
    # browser = webdriver.Chrome(executable_path=path)
    wait = WebDriverWait(browser, 20)
    browser.get(url)
    WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_radar_tip_content'))).click()
    c_slide = wait.until(EC.presence_of_element_located(
        (By.XPATH, '/html/body/div/div[2]/div[1]/div/div[1]/div[1]/div/a/div[1]/div/canvas[2]')))
    c_background = wait.until(EC.presence_of_element_located(
        (By.XPATH, '/html/body/div/div[2]/div[1]/div/div[1]/div[1]/div/a/div[1]/div/canvas[1]')))
    c_full_bg = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, '/html/body/div/div[2]/div[1]/div/div[1]/div[1]/div/a/div[1]/canvas')))
    slider = Slider(browser, c_slide, c_background, c_full_bg)
    slider.get_img()


if __name__ == '__main__':
    main()
