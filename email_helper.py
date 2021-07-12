import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from datetime import datetime


class EmailHelper:
    def __init__(self, config):
        username, password, target_address_list = config['163login']['username'], config['163login']['password'], config['target_address']
        self.con = smtplib.SMTP_SSL('smtp.163.com', 465)
        self.con.login(username, password)
        self.send_time = datetime.now().strftime("%Y-%m-%d")
        self.target_address_list = target_address_list
        self.username = username

    def _build_msg(self, data, target_address):
        msg = MIMEMultipart()
        subject = Header(f'采购消息提醒{self.send_time}', 'utf-8').encode()
        msg['Subject'] = subject
        msg['From'] = f'{self.username} <{self.username}>'
        msg['To'] = target_address
        text = MIMEText('\n'.join(data), 'plain', 'utf-8')
        msg.attach(text)

        return msg

    def send_email(self, data):
        for target_address in self.target_address_list:
            msg = self._build_msg(data, target_address)
            self.con.sendmail(self.username, target_address, msg.as_string())

    def __del__(self):
        self.con.quit()