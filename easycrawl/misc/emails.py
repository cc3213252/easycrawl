# -*- coding:utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header
import random


EmailAccounts = [
    {
        'host': 'smtp.exmail.qq.com',
        'port': 465,
        'auth': ('chenyd@billbear.cn', '密码')
    },
    {
        'host': 'smtp.163.com',
        'port': 994,
        'auth': ('cc3213252@163.com', '密码')
    },
]

class Email(smtplib.SMTP_SSL):

    target_list = ["chenyd@billbear.cn"]

    def send_diff(self,diff):
        pass

    def __init__(self,send_list = []):
        account = EmailAccounts[random.randint(0,len(EmailAccounts) - 1)]
        smtplib.SMTP_SSL.__init__(self,host = account['host'], port= account['port'])
        self.login(*account['auth'])
        self._from_user = account['auth'][0]
        self._attach = MIMEMultipart()
        self._send_list = Email.target_list
        self._send_list.extend(send_list)
        print("### _send_list:",self._send_list)

    def sendhtml(self,subject = "",content = ""):
        return self.sendmail(self._from_user,self._send_list,self.generate_mail(subject,content))

    def generate_mail(self,subect,content):
        self._attach['Subject'] = subect
        me = ("<" + self._from_user + ">")
        self._attach['From'] = me
        self._attach['To'] = ",".join(e for e in self._send_list)
        self._attach["Accept-Language"] = "zh-CN"
        self._attach["Accept-Charset"] = "utf-8"

        #body = "<a href='http://blog.csdn.net/u010415792'>Zhu_Julian's Blog</a>"
        if content:
            self._attach.attach(MIMEText(content, 'html','utf-8'))
        return self._attach.as_string()


    def attach(self,file_path = None,file_name = None,paths = []):
        if file_path:
            att = MIMEApplication(open('%s' % file_path, 'rb').read())
            if file_name is None:
                file_name = file_path.split('/')[-1]
            att.add_header('Content-Disposition', 'attachment', filename = file_name)
            self._attach.attach(att)
        for path in paths:
            att = MIMEApplication(open('%s' % path, 'rb').read())
            file_name = path.split('/')[-1]
            att.add_header('Content-Disposition', 'attachment', filename=file_name)
            self._attach.attach(att)
