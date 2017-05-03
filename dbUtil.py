#!/usr/bin/python
#encoding:utf-8
import MySQLdb

class DB:
    def __init__(self,host,user,passwd,port,db):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.port = port
        self.db = db
    def connect(self):
        self.conn = MySQLdb.connect(host=self.host,user=self.user,passwd=self.passwd,port=self.port,db=self.db,charset='utf8')
    def execute(self,sql):
        self.connect()
        cursor = self.conn.cursor()
	fetch_all_dict = ()
        try:
            cursor.execute(sql)
            fetch_all_dict = cursor.fetchall()
        except Exception as e:
            print e
        cursor.close()
        self.conn.commit()
        self.conn.close()
        return fetch_all_dict
