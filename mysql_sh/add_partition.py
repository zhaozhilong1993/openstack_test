#!/usr/bin/env python

import thread
import MySQLdb
import uuid 
import time
import random
import datetime

TABLE_NAME = 'sample'
#TIME = time.time()
TIME = 1468598400

def add_partition(partition_key=None,partition_value=None):
    print partition_key,partition_value
    try:
        conn=MySQLdb.connect(host='localhost',user='root',passwd='fbb2a0b544584e96',db='ceilometer',port=3306)
        cur=conn.cursor()
        cur.execute('alter table %s ADD PARTITION (PARTITION %s VALUES LESS THAN (%s));' % (TABLE_NAME,partition_key,partition_value),[])
	conn.commit()
        cur.close()
        conn.close()
    except MySQLdb.Error,e:
         print "Mysql Error"
         print e 

def create_date():
    global TIME
    time = TIME + 60*60*24
    TIME = time
    dateArray = datetime.datetime.utcfromtimestamp(time)
    partition_name = 'p' + str(dateArray.strftime("%Y%m%d"))
    return (partition_name, int(time))


for i in range(100000):
   rec = create_date()
   add_partition(rec[0], rec[1])
   time.sleep(0.1)
