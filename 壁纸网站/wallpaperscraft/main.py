# -*- coding: utf-8 -*-
# @Time    : 2024/11/7 14:14
# @Author  : 烂泥
# @FileName: main.py
# @Version : v1.0
# @Description:
import os

import requests
from bs4 import BeautifulSoup


class Spider:
    def __init__(self):
        self.page = 1
        self.base_url = 'https://wallpaperscraft.com/'
        self.url = 'https://wallpaperscraft.com/all/page'
        self.flag = False
        self.last_page = 1

    def loop_all_page(self):
        resp = requests.get(self.url + '1')
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            page_link = soup.find_all('a', class_='pager__link')
            self.last_page = int(
                page_link[-1]['href'].replace('/all/page', ''))
            print("成功获取到最大页码:" + str(self.last_page))
            self.analyse_html(soup)
            for self.page in range(2, self.last_page, 1):
                resp = requests.get(self.url + str(self.page))
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, 'html.parser')
                    self.analyse_html(soup)
                else:
                    print(f"程序在获取第{self.page}时出现错误")
                    return
        else:
            print('程序在获取最大页码时出现错误:' + str(resp.status_code))
            return

    def save_img(self, img_id, img_url):
        resp = requests.get(img_url)
        if resp.status_code == 200:
            # if not os.path.exists(f'./img{img_id}.jpg'):
            #     os.makedirs(f'./img{img_id}.jpg')
            with open(f'./img{img_id}.jpg', 'wb') as img:
                img.write(resp.content)
                print(f'{img_id}图片保存成功')
        else:
            print(f"程序在打开{img_id}图片时出现错误")
            return

    def get_img_request(self, img_id):
        resp = requests.get(self.base_url + img_id)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            img_url = soup.find('img', class_='wallpaper__image')['src']
            self.save_img(img_id, img_url)


        else:
            print(f"程序在获取{img_id}图片页面时出现错误" + str(resp.status_code))
            return

    def analyse_html(self, soup):
        li_list = soup.findAll('li', class_='wallpapers__item')
        for li in li_list:
            img_id = li.find('a', class_='wallpapers__link')['href']
            self.get_img_request(img_id)

        return


spider = Spider()
spider.loop_all_page()
