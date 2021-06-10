# -*- coding: utf-8 -*-
"""
Time    : 2021/06/10 8:05 PM
Author  : huzing2524
Project : myScripts
File    : code_spider.py
Url     : https://github.com/huzing2524/myScripts
"""
import random
import time

import requests

url = 'https://www.t66y.com/require/codeimg.php?'
proxies = {'https': '127.0.0.1:8888'}
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}

for i in range(100):
    try:
        res = requests.get(url + str(random.random()), headers=headers, proxies=proxies).content
        # print(res)
    except Exception:
        pass
    else:
        with open('./{}.jpg'.format(i), 'wb') as f:
            f.write(res)
        time.sleep(random.uniform(0, 2))
