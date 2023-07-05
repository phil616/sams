"""
    libs.mailsender.py
    ~~~~~~~~~
    邮件发送模块
    :copyright: (c) 2023 by Fei Dongxu.
    :date: 2023.07.04
    :license: Apache Licence 2.0
"""
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from config import app_cfg
class EMailSender:
    def __init__(self, username: str, password: str, host: str = "smtp.163.com"):
        self.smtp_server_username = username
        self.smtp_server_password = password
        self.smtp_server_host = host

    def syncSendMail(self, message, Subject, sender_show, recipient_show, to_addrs, text_type, cc_show=''):
        '''
        :param text_type: str 发送类型
        :param message: str 邮件内容
        :param Subject: str 邮件主题描述
        :param sender_show: str 发件人显示，不起实际作用如："xxx"
        :param recipient_show: str 收件人显示，不起实际作用 多个收件人用','隔开如："xxx,xxxx"
        :param to_addrs: str 实际收件人
        :param cc_show: str 抄送人显示，不起实际作用，多个抄送人用','隔开如："xxx,xxxx"
        '''
        # 填写真实的发邮件服务器用户名、密码
        user = self.smtp_server_username
        password = self.smtp_server_password
        # 邮件内容
        msg = MIMEText(message, text_type, _charset="utf-8")
        # 邮件主题描述
        msg["Subject"] = Subject
        # 发件人显示，不起实际作用
        msg["from"] = sender_show
        # 收件人显示，不起实际作用
        msg["to"] = recipient_show
        # 抄送人显示，不起实际作用
        msg["Cc"] = cc_show
        with SMTP_SSL(host=self.smtp_server_host, port=465) as smtp:
            # 登录发送邮件服务器
            try:
                smtp.login(user=user, password=password)
                # 实际发送、接收邮件配置
                smtp.sendmail(from_addr=user, to_addrs=to_addrs.split(','), msg=msg.as_string())
            except Exception as e:
                print(e)
                # TODO logger
EMailSender(username=app_cfg.EMAIL_USERNAME,password=app_cfg.EMAIL_PASSWORD)
