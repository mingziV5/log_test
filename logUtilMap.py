#!/usr/bin/python
#coding:utf-8
import dbUtil
import requests

def getMap(ip):
    #print ip
    res = requests.get('http://api.map.baidu.com/location/ip?ak=q5mTrTGzCSVq5QmGpI9y18Bo&coor=bd09ll&ip='+ip)
    location = res.json()['content']['point']
    return location
    #print location['x']
    #print location['y']


def logUtil(file):
    dict_log = {}
    with open(file) as f:
        for line in f:
            ip = line.split()[0]
            #location = getMap(ip)
            #loc_x = location['x']
            #loc_y = location['y']
            http_status = line.split()[8]
            dict_log[(ip,http_status)] = dict_log.get((ip,http_status),0) + 1
    return dict_log

def dict_sorted(dict_log):
    list_log = dict_log.items()
    list_log = sorted(list_log,key=lambda x:x[1])
    return list_log

def list_log_into_db(list_log):
    for i in list_log:
        print i
        ip = i[0][0]
        location = getMap(ip)
        #loc_x = i[0][1]
        #loc_y = i[0][2]
        loc_x = location['x']
        loc_y = location['y']
        http_status = i[0][1]
        count = i[1]
        sql = 'insert into logmap (ip,x,y,http_status,count) values ("%s","%s","%s",%s,%s)'%(ip,loc_x,loc_y,http_status,count)
        mydb = dbUtil.DB(host='192.168.31.2',user='log',passwd='ming',port=3306,db='logdb')
        mydb.execute(sql)

if __name__ == '__main__':
    dict_log = logUtil('access-web.log')
    list_log = dict_sorted(dict_log)
    #list_log = dict_log.items()
    #print list_log
    list_log_into_db(list_log)
    #getMap('114.114.114.114')

