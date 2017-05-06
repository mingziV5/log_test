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

@log_web.route('/map')
def map():
    return render_template('map.html')

@log_web.route('/mape')
def map2():
    return render_template('mapexample.html')
@log_web.route('/get-http-status')
def get_http_status():
    sql = 'select http_status,sum(count) from loginfo group by http_status'
    mydb = dbUtil.DB(host='192.168.31.2',user='log',passwd='ming',port=3306,db='logdb')
    res = mydb.execute(sql)
    http_dict = {'legend':[],'data':[]}
    for i in res:
        i1 = str(i[0])
        i2 = int(i[1])
        http_dict['legend'].append(i1)
        http_dict['data'].append({'name':i1,'value':i2})
        #http_status_list.append((i1,i2))
    #print http_status_list
    return json.dumps(http_dict) 

@log_web.route('/get-url')
def get_url():
    sql = 'select context,sum(count) from loginfo where context like "%htm" or context like "%html"  group by context order by sum(count) desc limit 20'
    mysql = dbUtil.DB(host='192.168.31.2',user='log',passwd='ming',port=3306,db='logdb')
    res = mysql.execute(sql)
    context_list = []
    for i in res:
        i1 = str(i[0])
        i2 = int(i[1])
        context_list.append((i1,i2))
    return json.dumps(context_list)

@log_web.route('/get-map-data')
def get_map_data():
    sql = 'select ip,x,y,count from logmap'
    mysql = dbUtil.DB(host='192.168.31.2',user='log',passwd='ming',port=3306,db='logdb')
    res = mysql.execute(sql)
    map_data = []
    for i in res:
        ip = str(i[0])
        x = float(i[1])
        y = float(i[2])
        count = int(i[3])
        map_data.append({'name':ip,'value':[x,y,count]})
    return json.dumps(map_data)

if __name__ == '__main__':
    log_web.run(host='0.0.0.0',debug=True)
