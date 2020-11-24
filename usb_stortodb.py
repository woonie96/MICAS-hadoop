import pymysql
import csv
from datetime import datetime
conn = pymysql.connect(host='localhost', user='root', password='root', db='study_db',charset='utf8')
curs = conn.cursor()
sql_usb_stor="insert into usb_stor (sub_key_name, sub_key_time, serial_number, serial_number_time, Device_Parameters_Lastwrite, Logconf_Lastwrite,Properties_Lastwrite,FriendlyName, ParentIdPrefix, First_InstallDate, InstallDate, LastArrival, Last_Removal) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s)"

usbstor = open('usbstor.csv', 'r', encoding='utf-8')
usb_stor_reader = csv.reader(usbstor)

index = 0
for line in usb_stor_reader:
    if index == 0:
        index +=1
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
            t4=None
        try:
            t5 = datetime.strptime(line[5], '%Y-%m-%d_%H:%M:%S')
            t5.strftime('%Y-%m-%d %H:%M:%S')
        except:
            t5 = None
        try:
            t6 = datetime.strptime(line[6], '%Y-%m-%d_%H:%M:%S')
            t6.strftime('%Y-%m-%d %H:%M:%S')
        except:
            t6=None
        try:
            t9 = datetime.strptime(line[9], '%Y-%m-%d_%H:%M:%S')
            t9.strftime('%Y-%m-%d %H:%M:%S')
        except:
            t9=None
        try:
            t10 = datetime.strptime(line[10], '%Y-%m-%d_%H:%M:%S')
            t10.strftime('%Y-%m-%d %H:%M:%S')
        except:
            t10=None
        try:
            t11 = datetime.strptime(line[11], '%Y-%m-%d_%H:%M:%S')
            t11.strftime('%Y-%m-%d %H:%M:%S')
        except:
            t11=None
        try:
            t12 = datetime.strptime(line[12], '%Y-%m-%d_%H:%M:%S')
            t12.strftime('%Y-%m-%d %H:%M:%S')
        except:
            t12 = None

        curs.execute(sql_usb_stor, (line[0],t1,line[2],t3,t4,t5,t6,line[7],line[8],t9,t10,t11,t12))
conn.commit()
conn.close()
usbstor.close()
