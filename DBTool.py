# -*- coding: utf-8 -*-
__author__ = 'xiaoxu12'
import os
import pymysql

class DBTool:

    conn = None
    cursor = None

    def __init__(self,conn_dict):
        print conn_dict['charset']
        self.conn = pymysql.connect(host=conn_dict['host'],
                                    port=conn_dict['port'],
                                    user=conn_dict['user'],
                                    passwd=conn_dict['password'],
                                    db=conn_dict['db'],
                                    charset=conn_dict['charset'])
        self.cursor = self.conn.cursor()


    def execute_query(self, sql_string):
        try:
            cursor=self.cursor
            cursor.execute(sql_string)
            list = cursor.fetchall()
            cursor.close()
            self.conn.close()
            return list
        except pymysql.Error as e:
            print("mysql execute error:", e)
            raise

    def execute_noquery(self, sql_string):
        try:
            cursor = self.cursor
            cursor.execute(sql_string)
            self.conn.commit()
            self.cursor.close()
            self.conn.close()
        except pymysql.Error as e:
            print("mysql execute error:", e)
            raise
