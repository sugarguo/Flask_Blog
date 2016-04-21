#! usr/bin/python
#  -_-  coding:utf-8 -_-

'''
@author          sugarguo

@email           sugarguo@live.com

@date            2016年04月21日

@version         v1.0.0 

@copyright       Sugarguo

File             install.py

'''


import os
import sys
sys.path.insert(0,'ext_lib')
import sqlite3
from werkzeug.security import generate_password_hash

DB_FILE_PATH = 'db_flask_blog_dev.sqlite'
SHOW_SQL = False#True

def get_conn(path):
    conn = sqlite3.connect(path)
    if os.path.exists(path) and os.path.isfile(path):
        print('Sqlite in :[{}]'.format(path))
        return conn
    else:
        conn = None
        print('Mem Sqlite :[:memory:]')
        return sqlite3.connect(':memory:')

def get_cursor(conn):
    if conn is not None:
        return conn.cursor()
    else:
        return get_conn('').cursor()

def close_all(conn, cu):
    try:
        if cu is not None:
            cu.close()
    finally:
        if cu is not None:
            cu.close()

def run_sql(conn, sql):
    if sql is not None and sql != '':
        cu = get_cursor(conn)
        if SHOW_SQL:
            print('Done sql:[{}]'.format(sql))
        cu.execute(sql)
        conn.commit()
        print('    __SQL...Success!\n')
        close_all(conn, cu)
    else:
        print('the [{}] is empty or equal None!'.format(sql))


site_name = raw_input("Please input site name:\n")
site_domain = raw_input("Please input site domain:\n")
site_email = raw_input("Please input site email:\n")


user_name = raw_input("Please input user name:\n")
user_password = raw_input("Please input user password:\n")
user_email = raw_input("Please input user email:\n")

insuser_password = generate_password_hash(user_password)


sqlfile = file('sqlite.sql','r')
sqlstr = sqlfile.read()[:-2]
sqlfile.close()

conn = get_conn(DB_FILE_PATH)

print "Create DB!\n"
for itemsql in sqlstr.split(";"):
    run_sql(conn, itemsql + ";")



print "INSERT packets!\n"
sqlpacket = "INSERT INTO packets (id, packet_name) VALUES (0, '未分组');"
#conn = get_conn(DB_FILE_PATH)
run_sql(conn, sqlpacket)
print "INSERT users!\n"
sqluser = "INSERT INTO users (username, password_hash, email) VALUES ('%s','%s','%s');" % (user_name, insuser_password, user_email)
#conn = get_conn(DB_FILE_PATH)
run_sql(conn, sqluser)
print "INSERT sites!\n"
sqlsite = "INSERT INTO sites (site_name, site_domain, site_email) VALUES ('%s','%s','%s');" % (site_name, site_domain, site_email)
#conn = get_conn(DB_FILE_PATH)
run_sql(conn, sqlsite)




print "\n\nWell Done! Please use\n\ngunicorn --config gunicorn.conf runserver:app\n\nrun the project!"

