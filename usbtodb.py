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
    date_list = [1, 3, 4, 7, 8, 9, 10]
    time_list = []
    if index == 0:
        index +=1
        pass
    else:
        if index == 0:
            index += 1
            pass
        else:
            for date in date_list:
                try:
                    time = datetime.strptime(line[date], '%Y-%m-%d_%H:%M:%S')
                    time.strftime('%Y-%m-%d %H:%M:%S')
                    time_list.append(time)
                except:
                    time = None
                    time_list.append(time)

        curs.execute(sql_usb, (line[0],time_list[0],line[2],time_list[1],time_list[2],line[5],line[6],time_list[3],time_list[4],time_list[5],time_list[6]))

conn.commit()
conn.close()
usb.close()
