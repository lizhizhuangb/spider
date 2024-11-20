# -*- coding: utf-8 -*-
# @Time    : 2024/11/13 9:51
# @Author  : 烂泥
# @FileName: slider_2.py
# @Version : v1.0
# @Description:
'''----------滑块验证码----------'''
import os
import base64
import time
import numpy as np

import cv2
import requests
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from io import BytesIO
import traceback
import ddddocr
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

# 滑块图片路径
slider_path = r".\slider.png"
# 背景图片路径
background_path = r".\background.png"


def login(webpath):
    """geetest滑块验证码"""
    driver = webdriver.Chrome(executable_path='D:\Code\python_code\linux_code\spider\chromedriver.exe')
    driver.get(webpath)
    time.sleep(2)
    # 最大化窗口
    # driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    element = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="gt-showZh-mobile"]/div/section/div/div[2]/div[1]/div[2]/div[3]/div[3]'))
    )
    # 元素加载完成后点击
    element.click()
    element = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="captcha"]/div[2]/div[1]/div[1]'))
    )
    # 元素加载完成后点击
    element.click()
    time.sleep(5)

    for i in range(8):
        slider_element = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="captcha"]/div[2]/div[1]/div[4]/div[1]/div[2]/div/div/div[1]/div[1]/div[1]'))
        )

        background_element = driver.find_element(By.XPATH,
                                                 '//*[@id="captcha"]/div[2]/div[1]/div[4]/div[1]/div[2]/div/div/div[1]/div[2]')

        # 获取滑块和背景图片的 style 属性
        slider_style = slider_element.get_attribute('style')
        background_style = background_element.get_attribute('style')

        # 提取滑块和背景图片的 URL
        slider_url = slider_style.split('"')[1]  # 提取滑块图片链接
        background_url = background_style.split('"')[1]  # 提取背景图片链接

        # 下载并保存图片
        with open('slice.png', 'wb') as f1:
            f1.write(requests.get(slider_url).content)

        with open('bg.png', 'wb') as f2:
            f2.write(requests.get(background_url).content)

        print("滑块图片和背景图片已下载")
        time.sleep(2)

        # save_canvas_as_image(slider_element, slider_path)
        # # transPNG(slider_path, slider_path)
        # # extract_slider(slider_path,slider_path)
        # save_canvas_as_image(background_element, background_path)
        # 下载图片
        # req_slider = requests.get(slider_url)
        # with open(r"C:\Users\Desktop\shuo\slider.png", "wb") as f:
        #     f.write(req_slider.content)
        # req_background = requests.get(background_url)
        # with open(r"C:\Users\Desktop\shuo\background.png", "wb") as f:
        #     f.write(req_background.content)

        # 获取滑块在背景图片的位置
        det = ddddocr.DdddOcr(det=False, ocr=False, show_ad=False)
        with open('./slice.png', 'rb') as f:
            target_bytes = f.read()
        with open('./bg.png', 'rb') as f:
            background_bytes = f.read()
        res = det.slide_match(target_bytes=target_bytes, background_bytes=background_bytes, simple_target=True)
        print(res)
        # 计算滑块轨迹
        distance = res["target"][0] - 10
        # tracks = [distance]
        tracks = get_tracks(distance)
        print(tracks)
        time.sleep(2)
        slider_button = driver.find_element(By.XPATH, '//*[@id="captcha"]/div[2]/div[1]/div[4]/div[1]/div[2]/div/div/div[2]/div/div[3]')
        # 移动滑块
        move_to_gap(driver, slider_button, tracks)
        time.sleep(2)

    driver.close()


def extract_slider(input_image_path, output_image_path):
    """
    从具有透明背景的图片中提取滑块部分，并保存为输出图片。

    :param input_image_path: 输入图像的路径（RGBA格式）
    :param output_image_path: 输出图像的路径
    """
    # 读取图像（确保读取带Alpha通道的图像）
    img = cv2.imread(input_image_path, cv2.IMREAD_UNCHANGED)

    # 如果图像没有Alpha通道（即不是RGBA图像），直接返回
    if img.shape[2] != 4:
        print("输入图像不是带Alpha通道的图片，无法处理透明背景。")
        return

    # 分离颜色通道（BGR）和Alpha通道（透明度）
    bgr = img[:, :, :3]  # 只保留RGB部分
    alpha = img[:, :, 3]  # 获取Alpha通道

    # 创建掩膜，Alpha通道值为0的部分是透明的，值为255的部分是非透明的
    _, mask = cv2.threshold(alpha, 1, 255, cv2.THRESH_BINARY)

    # 找到非透明区域的边界框
    coords = np.column_stack(np.where(mask > 0))

    if coords.size == 0:
        print("没有非透明区域，无法提取滑块。")
        return

    # 获取非透明区域的边界框（最小矩形）
    top_left = coords.min(axis=0)
    bottom_right = coords.max(axis=0)

    # 使用边界框裁剪出滑块部分
    slider = bgr[top_left[0]:bottom_right[0] + 1, top_left[1]:bottom_right[1] + 1]
    slider_alpha = mask[top_left[0]:bottom_right[0] + 1, top_left[1]:bottom_right[1] + 1]

    # 将RGB部分和Alpha通道合并
    result = cv2.merge([slider, slider_alpha])

    # 保存提取的滑块部分（带透明背景）
    cv2.imwrite(output_image_path, result)

    print(f"提取的滑块已保存到：{output_image_path}")

def save_canvas_as_image(canvas_element, save_path):
    """
    将 Selenium 中找到的 canvas 元素保存为图片文件。

    :param canvas_element: Selenium 中找到的 canvas 元素
    :param save_path: 保存图片的路径，包括文件名和扩展名 (如 'output.png')
    """
    # 使用 JavaScript 获取 canvas 的 Base64 编码数据
    canvas_base64 = canvas_element.parent.execute_script(
        "return arguments[0].toDataURL('image/png').substring(22);", canvas_element
    )

    # 解码 Base64 数据并保存为图片
    image_data = base64.b64decode(canvas_base64)
    image = Image.open(BytesIO(image_data))
    image.save(save_path)


def test():
    # 测试 滑块到背景之间得距离
    det = ddddocr.DdddOcr(det=False, ocr=False, show_ad=False)
    with open(slider_path, 'rb') as f:
        target_bytes = f.read()
    with open(background_path, 'rb') as f:
        background_bytes = f.read()
    res = det.slide_match(target_bytes=target_bytes, background_bytes=background_bytes, simple_target=False)
    print(res)


def transPNG(srcImageName, dstImageName):
    '''
    图片透明化处理
    :param srcImageName: 原图片路径
    :param dstImageName: 处理完的图片路径
    :return:
    '''
    img = Image.open(srcImageName)
    img = img.convert("RGBA")
    datas = img.getdata()
    newData = list()
    for item in datas:
        if item[0] < 50 and item[1] < 50 and item[2] < 50:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    img.putdata(newData)
    img.save(dstImageName, "PNG")


def get_tracks(distance):
    """
    根据偏移量获取移动轨迹
    :param distance:偏移量
    :return:移动轨迹
    """
    # 移动轨迹
    tracks = []
    # 减速阈值
    mid = distance * 4 / 5

    for i in range(5):
        tracks.append(mid / 5)
    for j in range(2):
        tracks.append(distance / 5 / 2)

    return tracks


def move_to_gap(browser, slider, tracks):
    """
    拖动滑块
    :param browser 浏览器
    :param slider: 滑块
    :param tracks: 轨迹
    :return:
    """
    # 模拟滑动滑块
    action = ActionChains(browser)
    action.click_and_hold(slider).perform()
    # action.reset_actions()   # 清除之前的action
    for i in tracks:
        action.move_by_offset(xoffset=i, yoffset=0).perform()
    time.sleep(0.5)
    action.release().perform()


def base64_to_image(base64_string, save_path):
    try:
        image_data = base64.b64decode(base64_string)
        image = Image.open(BytesIO(image_data))
        image.save(save_path)
    except:
        print(traceback.format_exc())
    # return image


if __name__ == '__main__':
    web_path = "https://www.geetest.com/adaptive-captcha-demo"
    login(web_path)
    # base64_to_image('iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAAARJJREFUWEftVksKglAUvbePLcJx+9AFRBOHRQQStqIkgggaOmsBto+auojQeqEglPh55xK9iU4995zjfedeH5Phhw3rU2+g70BjB3ani83p40xD2gRr7yYJa3iMpvSkvRpPFtvVLKnjaDQQHqJYkXKYKaEBu6iJQvylYqXIZuJr4HsuZuCTADTxJd5R2xpChKj8OrSmcwoQQgRbGu40kAN1iHUwUAaq4DYBqXiuodWBtvMt3pVpB8MKG6g9DiIqRk0gLjJQNVGQCMV/amBkWY6/nN/RjQllwPgRVNOef3WWpfyXEBodQ50518GIFhFCjGC1VrGEEK1pvg+Y/h0bv5AYv5KhG02KhzehVKiprjfQd+ANvPZXMANfapQAAAAASUVORK5CYII=',background_path)
