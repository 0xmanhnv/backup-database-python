#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import time

import pymysql as MySQLdb


def backup_mysql(user='', password='', host='', db_name=None) -> list or None:
    list_bk = []
    dbs_systems = ['information_schema', 'sys', 'performance_schema', 'mysql']

    conn = MySQLdb.connect(host, user, password)
    cursor = conn.cursor()
    cursor.execute("SHOW DATABASES")
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    timestamp = time.strftime('%Y-%m-%d')
    backup_folder = 'BK_{}'.format(timestamp)
    cmd_folder = 'mkdir -p {}'.format(backup_folder)
    os.system(cmd_folder)

    for result in results:
        if db_name:
            if result[0] == db_name:
                backup_file_name = '{}_{}.sql.gz'.format(result[0], timestamp)

                cmd_echo = "echo 'Backup {} database to {}'".format(result[0], backup_file_name)
                os.system(cmd_echo)
                
                cmd_dump = 'mysqldump -u {} -h {} -p{} {} | gzip -9 --rsyncable > ./{}/{}'.format(
                    user, 
                    host, 
                    password, 
                    db_name, 
                    backup_folder,
                    backup_file_name
                )
                os.system(cmd_dump)
                print("Backup {}".format({result[0]}))
                list_bk.append("{}/{}".format(backup_folder,backup_file_name))
        
        else:
            if result[0] not in dbs_systems:
                backup_file_name = '{}_{}.sql.gz'.format(result[0], timestamp)
                cmd_echo = "echo 'Backup {} database to {}'".format(result[0], backup_file_name)
                os.system(cmd_echo)
                
                cmd_dump = 'mysqldump -u {} -h {} -p{} {} | gzip -9 --rsyncable > ./{}/{}'.format(
                    user, 
                    host, 
                    password, 
                    result[0], 
                    backup_folder, 
                    backup_file_name
                )
                os.system(cmd_dump)
                print("Đã backup {}".format(result[0]))
                list_bk.append("{}/{}".format(backup_folder,backup_file_name))

    return timestamp, list_bk