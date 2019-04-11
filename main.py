#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

from dotenv import load_dotenv

from backup import backup_mysql
from libs import create_mail, send_mail

load_dotenv()

if __name__ == "__main__":

    timestamp, bks = backup_mysql(
        user=os.getenv('DB_USER'), 
        password=os.getenv('DB_PASSWORD'), 
        host=os.getenv('DB_HOST')
    )
    if bks:
        msg = create_mail(
            mail_received=os.getenv('MAIL_RECEIVED'), 
            subject=os.getenv('MAIL_SUBJECT'), 
            text="{}:{}".format(timestamp, os.getenv('MAIL_MSG')), 
            attachs=bks
        )
        send_mail(mail_received=os.getenv('MAIL_RECEIVED'), msg=msg)