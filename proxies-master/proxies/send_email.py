import smtplib
from email.mime.text import MIMEText








class SendEmail(object):
    """
    发送邮件
    """
    def __init__(self):
        self.FROM_ADDR = '2081896995@qq.com'
        self.PASSWORD = 'lgcromvicdejccei'
        self.TO_ADDR = ['1206414543@qq.com']
        self.SMTP_SERVER = 'smtp.qq.com'

    def message(self, msg):
        """
        构造邮件内容
        :param msg:
        :return:
        """
        msg = MIMEText(f'{msg}', 'plain', 'utf-8')
        msg['From'] = 'Python-Spider'
        msg['To'] = 'admin'
        msg['Subject'] = 'FROM STMP LOGIN AND SPIDER PROGRAM……'
        return msg

    def send_stmp_email(self, msg):
        """
        发送邮件
        :param msg:
        :return:
        """
        server = smtplib.SMTP(self.SMTP_SERVER, 25)
        try:
            server.set_debuglevel(1)
            server.login(self.FROM_ADDR, self.PASSWORD)
            server.sendmail(self.FROM_ADDR, self.TO_ADDR, msg.as_string())
            server.quit()
        except Exception as e:
            server.quit()

    def run(self, msg: str):
        msg = self.message(msg)
        self.send_stmp_email(msg)


if __name__ == '__main__':
    email = SendEmail()
    email.run('小王是个程序员')