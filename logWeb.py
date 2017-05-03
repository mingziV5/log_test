#!/usr/bin/python
#coding:utf-8
import dbUtil
import json
from flask import Flask
from flask import render_template

log_web = Flask(__name__)
log_web.secret_key = 'secret_key'

@log_web.route('/')
def index():
    return render_template('index.html')

@log_web.route('/get-http-status')
def get_http_status():
    sql = 'select http_status,sum(count) from loginfo group by http_status'
    mydb = dbUtil.DB(host='192.168.16.210',user='log',passwd='ming',port=3307,db='logdb')
    list_b = mydb.execute(sql)
    http_status_list = []
    for i in list_b:
        i1 = str(i[0])
        i2 = int(i[1])
        http_status_list.append((i1,i2))
    #print http_status_list
    return json.dumps(http_status_list) 

@log_web.route('/get-url')
def get_url():
    sql = 'select context,sum(count) from loginfo where context like "%htm" or context like "%html"  group by context order by sum(count) desc limit 20'
    mysql = dbUtil.DB(host='192.168.16.210',user='log',passwd='ming',port=3307,db='logdb')
    list_b = mysql.execute(sql)
    context_list = []
    for i in list_b:
        i1 = str(i[0])
        i2 = int(i[1])
        context_list.append((i1,i2))
    return json.dumps(context_list)

if __name__ == '__main__':
    log_web.run(host='0.0.0.0',debug=True)
