# -*- coding: utf-8 -*-
import requests
import smtplib
import os

from bs4 import BeautifulSoup
from email.mime.text import MIMEText

"""
定时任务的几种方式：
1. Linux Crontab: Linux内置的cron进程实现定时任务
2. python-crontab： 对Linux Crontab的封装，针对系统 Cron 操作 crontab 文件的作业调度库
3. schedule：轻量级，无需配置的作业调度库
4. Apscheduler：一个高级的 Python 任务调度框架
"""

# 创建txt文件保存最新章节标题
if not os.path.exists('./zhuixu_latest_chapter.txt'):
    with open('./zhuixu_latest_chapter.txt', 'w') as f:
        f.write('第一〇八一章 乱·战（下）')
        old_chapter_title = '第一〇八一章 乱·战（下）'
else:
    with open('./zhuixu_latest_chapter.txt', 'r') as f:
        old_chapter_title = f.read()

url_check_update = 'https://book.qidian.com/info/1979049'
url_latest_chapter = 'https://www.ibooktxt.com/0_60/'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'}

host_server = 'smtp.qq.com'  # QQ邮箱服务器地址
mail_sender = '******'       # 发件人邮箱账号
mail_password = '******'     # QQ邮箱授权码
mail_receiver = '******'     # 收件人邮箱账号

# 检查是否更新
response = requests.get(url_check_update, headers=headers).text
# print(response)
bs = BeautifulSoup(response, 'html.parser')
html = bs.find('li', {"class": "update"}).find('a')
# print(html)

# new_chapter_title = html.find('a').get('title')
new_chapter_title = html.get_text()
href = 'https:' + html.get('href')
# print(new_chapter_title, href)

response2 = requests.get(href, headers=headers).text
bs2 = BeautifulSoup(response2, 'html.parser')
update_time = bs2.find('span', {'class': 'j_updateTime'}).get_text()
# print(update_time)


if new_chapter_title != old_chapter_title:
    # 爬虫获取最新章节内容
    response3 = requests.get(url_latest_chapter, headers=headers).text
    bs3 = BeautifulSoup(response3, 'html.parser')
    chapter_href = url_latest_chapter + bs3.find('div', {'id': 'info'}).find_all('p')[-1].find('a').get('href')[6:]
    # print(chapter_href)
    response4 = requests.get(chapter_href, headers=headers).text
    bs4 = BeautifulSoup(response4, 'html.parser')
    chapter_content = bs4.find('div', {'id': 'content'}).get_text()
    # print(chapter_content)

    # 发送邮件通知
    # wxpy: 微信消息发送无法使用，不能扫码登录网页版微信
    msg = MIMEText('{}'.format(chapter_content), 'plain', 'utf-8')  # 邮件正文
    msg['From'] = mail_sender  # 发件人邮箱账号
    msg['To'] = mail_receiver  # 收件人邮箱账号
    msg['Subject'] = '《赘婿》更新提醒 -- {} -- {}'.format(new_chapter_title, update_time)  # 邮件的主题，也可以说是标题

    server = smtplib.SMTP_SSL(host_server)
    server.login(mail_sender, mail_password)
    server.sendmail(mail_sender, mail_receiver, msg.as_string())
    server.quit()

    # 定时任务，每晚0:00执行一次，使用Linux Crontab
    # 00 00 * * * /home/huzing2524/.virtualenvs/zhuixu/bin/python3.8 /home/huzing2524/Desktop/zhuixu_checking_update.py >> /home/huzing2524/Desktop/zhuixu.log 2>&1 &

    # 更新txt文件
    with open('./zhuixu_latest_chapter.txt', 'w') as f:
        f.write(new_chapter_title)
