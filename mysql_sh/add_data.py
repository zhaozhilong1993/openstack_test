#!/usr/bin/env python

import thread
import MySQLdb
import uuid 
import time
import random
import date


data = ['cpu_detil','mem_used','disk_io','net_id']
servers = ['server60','server61','server62','server63','server64']
now_date = datetime.date.now()

def insert(uuid=None,name=None, data_type=None, unit=None, time=None):
    try:
        conn=MySQLdb.connect(host='localhost',user='root',passwd='',db='gnocchi',port=3306)
        cur=conn.cursor()
        cur.execute("insert into test values(%s,%s,%s,%s,%s)", [uuid,name,data_type,unit,time])
	conn.commit()
        cur.close()
        conn.close()
    except MySQLdb.Error,e:
         print "Mysql Error"
         print e 


def create_time():
    global start_time
    start_time = datetime.date.today()
    # +5 s
    next_time = start_time + datetime.timedelta(seconds=5) 
    # return 
     

def insert_many():
    while 1:
      insert(str(uuid.uuid4()), 
		servers[random.randint(0,3)], 
		data[random.randint(0,3)], 
		random.randint(1,100), 
		create_time()
	    )
      time.sleep(0.1)


def create_thread():
    thread.start_new_thread(insert_many, ())

for i in range(1,8):
    create_thread()

# sleep 10 h
time.sleep(60*60*10)
