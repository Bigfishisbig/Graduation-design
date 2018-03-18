#-*-coding:utf8-*-
import pymysql, traceback
from PyQt5 import QtWidgets

class Common(object):
    def get_data(self, sql):
        try:
            self.conn = pymysql.connect(
                host='localhost',
                user='root',
                passwd='',
                db='info',
                charset='utf8',
            )
            self.cur = self.conn.cursor()

            print ("sql:", sql)
            self.cur.execute(sql)
            self.rows = self.cur.fetchall()
            self.row = self.cur.rowcount  # 取得记录个数，用于设置表格的行数
            # self.vol = len(self.rows[0])  # 取得字段数，用于设置表格的列数
            self.cur.close()
            self.conn.close()

            return self.rows, self.row
        except:
            traceback.print_exc()