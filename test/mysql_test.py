#coding:utf8
"""
Created on 2016年1月11日

@author: pan
"""
import MySQLdb


conn = MySQLdb.Connect(host='127.0.0.1', port=3306, user='root',
                       passwd='123456', db='shopping', charset='utf8')

cursor = conn.cursor()
cursor.execute("select version()")
print str(cursor.fetchone()).encode('utf-8')

sql = 'select * from items'
cursor.execute(sql)
print cursor.fetchone()


print conn
print cursor

cursor.close()
conn.close()

