#!/usr/bin/env python
from datetime import datetime
import sys

# 你的邮件内容
# 使用你的邮件账户名和密码登录服务器
sender='*@163.com' 
password="QZCAAZQDQSZQWRNJ" #打开POP3/SMTP服务，获取邮箱授权码

recipient='*@163.com' 
message = sys.argv[1]
mail_content = {
    'subject': 'senteion licence error! {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),  # 随便填写
    'content_text': message,  # 随便填写
    #'attachments': '/public/test_data/Multiplex_MRD/results/Topgen-20220107-L-02-2022-01-111237/umi/summary_umi.xls',
}

try:
    import zmail
    server = zmail.server(sender,password)
    server.send_mail([recipient], mail_content)
except:
    sys.exit(1)
else:
    sys.exit(0)

