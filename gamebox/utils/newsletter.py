# -*- coding = utf-8 -*-
# @Time ： 2022/3/31 20:16
# @Author : M
# @File : newsletter.py
# @Software: PyCharm
from smtplib import SMTP_SSL
from email.mime.text import MIMEText


def sendMail(message, recipient_show, to_addrs):
    '''
    :param message: str 邮件内容
    :param recipient_show: str 收件人显示，不起实际作用 多个收件人用','隔开如："xxx,xxxx"
    :param to_addrs: str 实际收件人
    '''
    # 填写真实的发邮件服务器用户名、密码
    user = 'gameboxpy@163.com'
    password = 'YQCBPOLSWQJHRZIN'
    # 邮件内容
    msg = MIMEText(message, 'plain', _charset="utf-8")
    # 邮件主题描述
    msg["Subject"] = "Subscribe success"
    # 发件人显示，不起实际作用
    msg["from"] = "GameBox.co"
    # 收件人显示，不起实际作用
    msg["to"] = recipient_show
    with SMTP_SSL(host="smtp.163.com", port=465) as smtp:
        # 登录发邮件服务器
        smtp.login(user=user, password=password)
        # 实际发送、接收邮件配置
        smtp.sendmail(from_addr=user, to_addrs=to_addrs.split(','), msg=msg.as_string())

    return
