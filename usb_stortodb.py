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
    date_list=[1,3,4,5,6,9,10,11,12]
    time_list =[]
    if index == 0:
        index +=1
        pass
    else:
        for date in date_list:
            try:
                time = datetime.strptime(line[date],'%Y-%m-%d_%H:%M:%S')
                time.strftime('%Y-%m-%d %H:%M:%S')
                time_list.append(time)
            except:
                time = None
                time_list.append(time)

        curs.execute(sql_usb_stor, (line[0],time_list[0],line[2],time_list[1],time_list[2],time_list[3],time_list[4],line[7],line[8],time_list[5],time_list[6],time_list[7],time_list[8]))
conn.commit()
conn.close()
usbstor.close()
