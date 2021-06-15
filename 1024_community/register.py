# -*- coding: utf-8 -*-
import os
import re
import random
import sys
import requests
import string
import time

from .chaojiying import ChaojiyingClient

# 需要遍历破解的邀请码，爬虫自动抓取最新帖子后手动填入此列表中
invite_code_list = ['f70d467e3176f55{}']
base_url = ''
permanent_url = 'https://www.t66y.com/'
latest_url = 'https://cl.912x.xyz/'
# 需要尝试的内容: 数字/字母 -> 0123456789/abcdefghijklmnopqrstuvwxyz
digits_lowercase = [i for i in string.digits + string.ascii_lowercase]
digits = [i for i in string.digits]
lowercase = [i for i in string.ascii_lowercase]
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/90.0.4430.93 Safari/537.36'}
# 邀请码验证返回结果: <script language="JavaScript1.2">parent.retmsg_invcode('1');</script>
msg_invcode = {'0': '恭喜您，您可以使用這個邀請碼註冊！', '1': '邀請碼不存在或已被使用，您無法注冊！', '2': '驗證碼不正確，請重新填寫'}

# 判断当前环境的永久url/最新url是否可用
try:
    if requests.get(permanent_url, headers=headers, timeout=3).status_code == 200:
        base_url = permanent_url
except requests.exceptions.RequestException:
    pass

try:
    if requests.get(latest_url, headers=headers, timeout=3).status_code == 200:
        base_url = latest_url
except requests.exceptions.RequestException:
    pass

if len(base_url) == 0:
    sys.exit()
print('base_url -> ', base_url)

# 邀请码请求网址
url = base_url + 'register.php?reginvcode={}&validate={}&action=reginvcodeck'
# 验证码请求网址
captcha_url = base_url + 'require/codeimg.php?{}'

# 获取随机验证码, 图片id是0～1之间的随机浮点数
ran = random.random()
res = requests.get(captcha_url + str(ran), headers=headers).content
with open('./{}.jpg'.format(ran), 'wb') as f:
    f.write(res)

# 验证码识别：第三方打码平台/深度学习图片识别
chaojiying = ChaojiyingClient('******', '******', '******')
im = open('./{}.jpg'.format(ran), 'rb').read()
captcha_text = chaojiying.PostPic(im, 1004)['pic_str']  # 1004: 1~4位英文数字
print('验证码文本是： ', captcha_text)

# 把帖子中的隐藏邀请码和数字/字母组合，然后调用注册接口，通过返回值索引判断是否注册成功
for i in invite_code_list:
    for j in digits:
        combine_code = i.format(j)
        print('当前尝试的邀请码是： ', combine_code)
        res2 = requests.post(url.format(combine_code, captcha_text), headers=headers).text
        # print(res2)
        res2_help_text = msg_invcode[re.search(r'\(.*\)', res2).group().lstrip("('").rstrip("')")]
        print(res2_help_text)
        time.sleep(random.uniform(0, 2))

os.remove('./{}.jpg'.format(ran))
