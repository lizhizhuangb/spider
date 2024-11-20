# -*- coding: utf-8 -*-
# @Time    : 2024/11/6 15:35
# @Author  : 烂泥
# @FileName: main.py
# @Version : v1.0
# @Description:
import json
import re

import requests
import xlwt


class No_Visa:
    def __init__(self):
        self.url = 'https://vacations.ctrip.com/visa/visarecommand'
        self.resp_content = ''
        self.data = ''
        self.wb = xlwt.Workbook()
        self.sheet_free = self.wb.add_sheet(sheetname='免签国家')
        titles = ['国家', '可停留天数', '是否可以延期', '费用', '描述']
        for title in titles:
            self.sheet_free.write(0, titles.index(title), title)
        self.sheet_arrive = self.wb.add_sheet(sheetname='落地签国家')
        titles = ['国家', '可停留天数', '是否可以延期', '费用', '描述']
        for title in titles:
            self.sheet_arrive.write(0, titles.index(title), title)

    # def write_to_excel(self):

    def get_html(self):
        self.resp_content = requests.get(self.url).text

    def analyse_content_freevisa(self):
        ori_data = re.search(r'window.__INITIAL_STATE__ = (.*?)window.__APP_SETTINGS__', self.resp_content,
                             re.DOTALL).group(
            1)
        json_data = json.loads(ori_data
                               )["visaPolicyGroupedList"]["freeVisa"]
        row, col = 1, 0
        for data in json_data:
            displayedName = data["displayedName"]
            self.sheet_free.write(row, col, displayedName)
            col += 1
            data = data['PolicyInfoDTO']['VisaFreeOrArrivals'][0]

            StayDaysStructDesc = data['StayDaysStructDesc']
            data_time = StayDaysStructDesc.replace('可停留天数：', '')
            if data_time:
                data_time = int(data_time)
            self.sheet_free.write(row, col, data_time)
            col += 1

            PostponedStructDesc = data['PostponedStructDesc']
            self.sheet_free.write(row, col, PostponedStructDesc.replace('是否可延期：', ''))
            col += 1

            CostStructDesc = data['CostStructDesc']
            self.sheet_free.write(row, col, CostStructDesc.replace('费用：', ''))
            col += 1

            Remark = data['Remark']
            self.sheet_free.write(row, col, Remark)
            row += 1
            col = 0

    def analyse_content_arrivalVisa(self):
        ori_data = re.search(r'window.__INITIAL_STATE__ = (.*?)window.__APP_SETTINGS__', self.resp_content,
                             re.DOTALL).group(
            1)
        json_data = json.loads(ori_data
                               )["visaPolicyGroupedList"]["arrivalVisa"]
        row, col = 1, 0
        for data in json_data:
            displayedName = data["displayedName"]
            self.sheet_arrive.write(row, col, displayedName)
            col += 1
            data = data['PolicyInfoDTO']['VisaFreeOrArrivals'][0]

            StayDaysStructDesc = data['StayDaysStructDesc']
            data_time = StayDaysStructDesc.replace('可停留天数：', '')
            if data_time:
                data_time = int(data_time)
            self.sheet_arrive.write(row, col, data_time)
            col += 1

            PostponedStructDesc = data['PostponedStructDesc']
            self.sheet_arrive.write(row, col, PostponedStructDesc.replace('是否可延期：', ''))
            col += 1

            CostStructDesc = data['CostStructDesc']
            self.sheet_arrive.write(row, col, CostStructDesc.replace('费用：', ''))
            col += 1

            Remark = data['Remark']
            self.sheet_arrive.write(row, col, Remark)
            row += 1
            col = 0

    def save_wb(self):
        self.wb.save('visa.xls')


visa = No_Visa()
visa.get_html()
visa.analyse_content_freevisa()
visa.analyse_content_arrivalVisa()
visa.save_wb()
