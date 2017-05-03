#!/usr/bin/python
#coding:utf-8
import dbUtil

def logUtil(file):
    dict_log = {}
    with open(file) as f:
        for line in f:
            ip = line.split()[0]
            context = line.split()[6]
            if '?' in context:
                context = context.split('?')[0]
	    http_status = line.split()[8]
            #print ip + ' ' + context + ' ' + http_status
            dict_log[(ip,context,http_status)] = dict_log.setdefault((ip,context,http_status),0) + 1
    return dict_log

def dict_sorted(dict_log):
    list_log = dict_log.items()
    list_log = sorted(list_log,key=lambda x:x[1])
    return list_log

def list_log_into_db(list_log):
    for i in list_log:
        ip = i[0][0]
        context = i[0][1]
        http_status = i[0][2]
        count = i[1]
        sql = 'insert into loginfo (ip,context,http_status,count) values ("%s","%s",%s,%s)'%(ip,context,http_status,count)
        mydb = dbUtil.DB(host='192.168.16.210',user='log',passwd='ming',port=3307,db='logdb')
	mydb.execute(sql)

if __name__ == '__main__':
    dict_log = logUtil('../access_20170502.log')
    list_log = dict_sorted(dict_log)
    list_log_into_db(list_log)

