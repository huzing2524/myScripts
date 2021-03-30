import requests
import json
import smtplib
import time

from datetime import datetime
from email.mime.text import MIMEText


"""
定时任务的几种方式：
1. Linux Crontab: Linux内置的cron进程实现定时任务
2. python-crontab： 对Linux Crontab的封装，针对系统 Cron 操作 crontab 文件的作业调度库
3. schedule：轻量级，无需配置的作业调度库
4. Apscheduler：一个高级的 Python 任务调度框架
"""

old_chapter_title = '第一〇八一章 乱·战（中）'
new_chapter_title = ''

url = 'http://dushu.baidu.com/api/pc/getDetail?data={"book_id":"4315647017"}'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'}

host_server = 'smtp.qq.com'  # QQ邮箱服务器地址
mail_sender = '******'       # 发件人邮箱账号
mail_password = '******'     # QQ邮箱授权码
mail_receiver = '******'     # 收件人邮箱账号


# 检查是否更新
response = requests.get(url, headers=headers).text
# print(response)
res_dict = json.loads(response)
# print(res_dict)
new_chapter_title = res_dict['data']['novel']['lastChapter']['chapter_title']  # 章节标题
update_timestamp = int(res_dict['data']['novel']['lastChapter']['update_time'])  # 更新时间：时间戳
# print(new_chapter_title, update_timestamp)

# 时间戳转换格式
convert_datetime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(update_timestamp))
weekday = datetime.fromtimestamp(update_timestamp).weekday() + 1  # 星期几：星期表示0-6，要+1


if new_chapter_title:
	if new_chapter_title != old_chapter_title:
		# 发送邮件通知
		# wxpy: 微信消息发送无法使用，不能扫码登录网页版微信
		msg = MIMEText('{} - {} - 星期{}'.format(new_chapter_title, convert_datetime, weekday), 'plain', 'utf-8')  # 邮件正文
		msg['From'] = mail_sender  # 发件人邮箱账号
		msg['To'] = mail_receiver  # 收件人邮箱账号
		msg['Subject'] = '《赘婿》更新提醒--{}'.format(new_chapter_title)  # 邮件的主题，也可以说是标题

		server = smtplib.SMTP_SSL(host_server)
		server.login(mail_sender, mail_password)
		server.sendmail(mail_sender, mail_receiver, msg.as_string())
		server.quit()

		# 定时任务，每晚0:00执行一次，使用Linux Crontab
		# 00 00 * * * /home/huzing2524/.virtualenvs/zhuixu/bin/python3.8 /home/huzing2524/Desktop/zhuixu_checking_update.py >> /home/huzing2524/Desktop/zhuixu.log 2>&1 &
