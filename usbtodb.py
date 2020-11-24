import pymysql
import csv
from datetime import datetime
conn = pymysql.connect(host='localhost', user='root', password='root', db='study_db',charset='utf8')
curs = conn.cursor()
sql_usb="insert into usb (sub_key_name, sub_key_time, serial_number, serial_number_time, properties_key_last_write,FriendlyName, ParentIdPrefix, First_InstallDate, InstallDate, LastArrival, LastRemoval) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"
usb = open('usb.csv', 'r', encoding='utf-8')


usb_reader = csv.reader(usb)
index = 0
for line in usb_reader:
    if index == 0:
        index +=1
        pass
    else:
        if index == 0:
            index += 1
            pass
        else:
            try:
                t1 = datetime.strptime(line[1], '%Y-%m-%d_%H:%M:%S')
                t1.strftime('%Y-%m-%d %H:%M:%S')
            except:
                t1 = None
            try:
                t3 = datetime.strptime(line[3], '%Y-%m-%d_%H:%M:%S')
                t3.strftime('%Y-%m-%d %H:%M:%S')
            except:
                t3 = None
            try:
                t4 = datetime.strptime(line[4], '%Y-%m-%d_%H:%M:%S')
                t4.strftime('%Y-%m-%d %H:%M:%S')
            except:
                t4 = None
            try:
                t7 = datetime.strptime(line[7], '%Y-%m-%d_%H:%M:%S')
                t7.strftime('%Y-%m-%d %H:%M:%S')
            except:
                t7 = None
            try:
                t8 = datetime.strptime(line[8], '%Y-%m-%d_%H:%M:%S')
                t8.strftime('%Y-%m-%d %H:%M:%S')
            except:
                t8 = None
            try:
                t9 = datetime.strptime(line[9], '%Y-%m-%d_%H:%M:%S')
                t9.strftime('%Y-%m-%d %H:%M:%S')
            except:
                t9 = None
            try:
                t10 = datetime.strptime(line[10], '%Y-%m-%d_%H:%M:%S')
                t10.strftime('%Y-%m-%d %H:%M:%S')
            except:
                t10 = None

        curs.execute(sql_usb, (line[0],t1,line[2],t3,t4,line[5],line[6],t7,t8,t9,t10))

conn.commit()
conn.close()
usb.close()
