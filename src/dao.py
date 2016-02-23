#coding:utf8

import MySQLdb

class Dao(object):
    def __init__(self):
        self.conn = MySQLdb.Connect(host='127.0.0.1', port=3306, user='root',
                       passwd='123456', db='zhihu', charset='utf8')
        self.cursor = self.conn.cursor()

    def insert(self, user_info_list):
        sql = "insert into user_tbl (name,bio,location,business,gender,companies,profession,school,major,src," \
              "followees,folloeers,url) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            self.cursor.executemany(sql, user_info_list)
            self.conn.commit()
        except Exception, ex:
            print(Exception, ex)

    def close_conn(self):
        self.cursor.close()
        self.conn.close()

if __name__ == '__main__':
    dao = Dao()
    paa_dict = {'1': '测试2', '2': '测试3', '3': u'男', '4': 'aa', '5': '测试5','6': '测试2',
                '7': '测试3', '8': 15, '9': 23, '10': '测试5', '11': '测试5', '12': '测试5'}
    param_list = list()
    param_list.append(paa_dict.values())
    dao.insert(param_list)


