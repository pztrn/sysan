# -*- coding: utf-8 -*-

# Mailer module.
import os
import smtplib
from email.mime.text import MIMEText

from lib import common

class Mailer:
    def __init__(self):
        self.config = common.CONFIG

        self.mail_to = self.config["mailer"]["send_to"]
        self.mail_from = self.config["mailer"]["send_from"]
        self.smtp_host = self.config["smtp"]["smtp_host"]
        self.smtp_username = self.config["smtp"]["smtp_username"]
        self.smtp_password = self.config["smtp"]["smtp_password"]
        self.smtp_tls = self.config["smtp"]["smtp_tls"]
        self.smtp_ssl = self.config["smtp"]["smtp_ssl"]

    def process_mail(self, mail_text):
        """
        Sends an email.
        """
        self.mail_text = mail_text
        if self.config["mailer"]["mail_mode"] == "sendmail":
            print("Sending report with sendmail...")
            self.send_with_sendmail()
            print("Sent.")
        elif self.config["mailer"]["mail_mode"] == "smtp":
            print("Sending report with SMTP...")
            self.send_with_smtp()
            print("Sent.")

    def send_with_sendmail(self):
        """
        Send mail with sendmail.
        """
        p = os.popen("/usr/sbin/sendmail -t", "w")
        p.write("From: {0}\n".format(self.mail_from))
        p.write("To: {0}\n".format(self.mail_to))
        p.write("Subject: SysAn system logs analyze report ({0})\n",format(common.DATE))
        p.write("\n")
        p.write(self.mail_text)
        retcode = p.close()
        if retcode:
            print("Failed to send message with sendmail!")

    def send_with_smtp(self):
        """
        Send mail with SMTP.
        """
        self.mail_text = "Subject: SysAn system logs analyze report ({0})\n\n".format(common.DATE) + self.mail_text
        server = smtplib.SMTP(self.smtp_host)
        server.starttls()
        server.login(self.smtp_username, self.smtp_password)
        server.sendmail(self.mail_from, self.mail_to, self.mail_text)
        server.quit()
        