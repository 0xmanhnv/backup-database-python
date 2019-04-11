#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.utils import formatdate
from email import encoders

from dotenv import load_dotenv

load_dotenv()

def create_mail(mail_received, subject, text, attachs:list = None):
    msg = MIMEMultipart()

    msg['Subject'] = subject
    msg['From'] = os.getenv('FROM_MAIL')
    msg['To'] = mail_received
    msg['Date'] = formatdate()

    msg.attach(MIMEText(text, 'plain', 'utf-8'))

    if attachs:
        for attach in attachs:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(open(attach, 'rb').read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition','attachment', filename=os.path.basename(attach))

            msg.attach(part)

    return msg


def send_mail(mail_received, msg) -> None:
    if os.getenv('MAIL_ENCRYPTION') == 'ssl':
        smtp_server = smtplib.SMTP_SSL(os.getenv('SMTP_SERVER'), os.getenv('SMTP_PORT'))
        smtp_server.login(os.getenv('FROM_MAIL'), os.getenv('MAIL_PASSWORD'))
        smtp_server.sendmail(os.getenv('FROM_MAIL'), mail_received, msg.as_string())
        smtp_server.close()
    else:
        smtp_server = smtplib.SMTP(os.getenv('SMTP_SERVER'), os.getenv('SMTP_PORT'))
        smtp_server.login(os.getenv('FROM_MAIL'), os.getenv('MAIL_PASSWORD'))
        smtp_server.sendmail(os.getenv('FROM_MAIL'), mail_received, msg.as_string())
        smtp_server.close()