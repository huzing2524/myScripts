# -*- coding: utf-8 -*-
"""
Time    : 2021/03/13 10:41 PM
Author  : huzing2524
Project : test
File    : zhuixu.py
Url     : https://github.com/huzing2524/test

网址: https://www.ibooktxt.com/0_60/
赘婿 爬虫 -> 生成txt文档
手机版网站上全都是广告，烦死了
"""

import time
import random
import requests
from bs4 import BeautifulSoup

menu_url = 'https://www.ibooktxt.com/0_60/'  # 总目录url -> 末尾必须要有斜杠/, 否则报404
chapter_urls = []  # 子章节跳转url
count = 1

menu_responses = requests.get(menu_url).text  # str
# print(menu_responses)

bs = BeautifulSoup(menu_responses, 'html.parser').find_all('dd')[28:]  # 删除前面无关章节
# print(bs)  # list
print('总的章节数: ', len(bs))

for i in bs:
    href = i.find('a').get('href')[6:]  # 去掉最左边url中重复的内容
    # print(href)
    chapter_urls.append(href)

# print(chapter_urls)

with open('赘婿.txt', 'w+') as f:
    for url in chapter_urls:
        res = requests.get(menu_url + url).text
        # print(res)
        chapter_bs = BeautifulSoup(res, 'html.parser')
        title = chapter_bs.title.string[9:-7]  # 章节标题
        print('当前下载章节: {} + 章节数: {}'.format(title, count))
        content = chapter_bs.find(id='content').text  # 章节内容
        # print(content)
        f.write(title + content + '\n\n\n\n')
        count += 1
        time.sleep(round(random.random(), 2))  # 睡眠时间: 0~1之间浮点数
