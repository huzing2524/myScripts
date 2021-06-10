# -*- coding: utf-8 -*-
import os
import re
import time
import random
import smtplib
from datetime import datetime

import requests

from email.mime.text import MIMEText
from bs4 import BeautifulSoup

host_server = 'smtp.qq.com'  # QQ邮箱服务器地址
# mail_sender = '******'  # 发件人邮箱账号
# mail_password = '******'  # QQ邮箱授权码
# mail_receiver = '******'  # 收件人邮箱账号

url = 'https://www.t66y.com/thread0806.php?fid=7&search=&page={}'
proxies = {'https': '127.0.0.1:8888'}
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}

invite_code_list, latest_pub = [], []
if not os.path.exists('invite_code.txt'):
    f = open('invite_code.txt', 'w')
    f.close()

with open('invite_code.txt', 'r') as f:
    store_hrefs = f.readlines()
print('store_hrefs', store_hrefs)

for i in range(1, 6):
    # 代理经常报错 requests.exceptions.ProxyError, Max retries exceeded with url
    session = requests.session()
    session.keep_alive = False
    # content-encoding: br
    # bytes: 使用content会自动解码。使用text会返回压缩格式br的中文乱码，无法用正则表达式匹配。
    res = session.get(url.format(i), headers=headers, proxies=proxies).content

    bs = BeautifulSoup(res, 'html.parser')
    # print(bs)
    html_list = bs.find_all('h3', text=re.compile('码|邀请码'))
    # print(html_list)

    for j in html_list:
        href = 'https://www.t66y.com/' + j.find('a').get('href')
        # print(href)
        invite_code_list.append(href + '\n')

    time.sleep(random.uniform(0, 2))
print('invite_code_list', invite_code_list)

for i in invite_code_list:
    if i not in store_hrefs:
        latest_pub.append(i)
        with open('invite_code.txt', 'a') as f:
            f.write(i)

print('latest_pub', latest_pub)
if len(latest_pub) > 0:
    # 发送邮件通知
    # wxpy: 微信消息发送无法使用，不能扫码登录网页版微信
    msg = MIMEText('{}'.format(', '.join(latest_pub)), 'plain', 'utf-8')  # 邮件正文
    msg['From'] = mail_sender  # 发件人邮箱账号
    msg['To'] = mail_receiver  # 收件人邮箱账号
    msg['Subject'] = '《1024社区》邀请码新贴发布提醒 -- 帖子数量: {} -- 时间: {}'.format(len(latest_pub), datetime.now().strftime(
        '%Y/%m/%d %H:%M:%S'))  # 邮件的主题，也可以说是标题

    server = smtplib.SMTP_SSL(host_server)
    server.login(mail_sender, mail_password)
    server.sendmail(mail_sender, mail_receiver, msg.as_string())
    server.quit()

file_size = os.path.getsize('invite_code.txt')
# print('file_size', file_size)
if file_size / (1024 ** 2) > 10:  # 超过10M删除文件
    os.remove('invite_code.txt')
