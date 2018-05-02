#coding:utf-8
from email.mime.text import MIMEText

msg = MIMEText('Hello,new message come from yeah.net edited by python client.', 'plain', 'utf-8')

from_addr = r"quanchaozhao@yeah.net"
password = r"112625yeah"
to_addr = r'1012264866@qq.com'
smtp_server = r'smtp.yeah.net'
import smtplib
server = smtplib.SMTP(smtp_server, 25) # SMTP协议默认端口是25
server.set_debuglevel(1)
server.login(from_addr, password)
msg['from'] = from_addr # 设置发送人
msg['to'] = to_addr  # 设置接收人
msg['subject'] = "Hello, new messages."
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()