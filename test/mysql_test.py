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



sql = "insert into items(name, city, price, number, picture) values(%s,%s,%s,%s,%s) "
para_dict = {}
paa_dict = {'test': '测试2', 'test1': '测试3', 'test2': 15, 'test3': 23, 'test4': '测试5'}
print(paa_dict.values())
params = ('测试11', '上海', 13, 34, '12.jpg')
print cursor.execute(sql, paa_dict.values())
conn.commit()

sql = 'select * from items where price=23'
cursor.execute(sql)
ret = cursor.fetchone()
print ret[2]
print(ret[1])

cursor.close()
conn.close()

