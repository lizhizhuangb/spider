# -*- coding: utf-8 -*-
# @Time    : 2024/10/18 16:50
# @Author  : 烂泥
# @FileName: huaban.py
# @Version : v1.0
# @Description:
import json
import math
import random
import time

import requests


class Spider():
    def __init__(self, target):
        self.page = 1
        self.url = 'https://huaban.com/v3/search/file?text=' + target + '&sort=all&limit=100&page=' + str(
            self.page) + '&position=search_pin&fields=pins:PIN%7Ctotal,facets,split_words,relations,rec_topic_material,topics'
        self.img_url = 'https://gd-hbimg.huaban.com/'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
            'cookie': 'xxx' # 更换为你自己的cookie
        }
        self.pages = 0

    def get_max_pages(self):
        resp = requests.get(self.url, headers=self.headers)
        if resp.status_code == 200:
            result_json = json.loads(resp.text)
            self.pages = math.ceil(result_json["total"] / 100)

        else:
            print('状态码有误:' + str(resp.status_code))

    def loop_all_pages(self):
        for self.page in range(1, self.pages + 1):
            resp = requests.get(self.url, headers=self.headers)
            if resp.status_code == 200:
                result_list = json.loads(resp.text)["pins"]
                for pin in result_list:
                    key = pin["file"]["key"]
                    resp_img = requests.get(self.img_url + str(key), headers=self.headers)
                    time.sleep(random.uniform(0.5, 1))
                    if resp_img.status_code == 200:
                        with open(f'./img/{key}.png', 'wb') as img:
                            img.write(resp_img.content)
            else:
                print('状态码有误:' + str(resp.status_code))


if __name__ == '__main__':
    spider = Spider('电吉他')
    spider.get_max_pages()
    spider.loop_all_pages()
