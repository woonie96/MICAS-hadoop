import pymysql
import csv
import re
from datetime import datetime

def usb_stor_db():
    conn = pymysql.connect(host='localhost', user='root', password='root', db='study_db', charset='utf8')
    curs = conn.cursor()
    match = "(?<=\{).+?(?=\})"
    reg = re.compile(match)
    sql_usb_stor = "insert into usb_stor (Subkey_Name,Serial_Number,Friendly_Name,ContainerID,First_Install_Date,Last_Remove_Date) values (%s, %s, %s, %s, %s, %s)"
    usbstor = open('usbstor.csv', 'r', encoding='utf-8')
    usb_stor_reader = csv.reader(usbstor)
    index = 0
    for line in usb_stor_reader:
        date_list=[10,13]
        time_list =[]

        if index == 0:
            index +=1
            pass
        else:
            Subkey_Name = line[0]
            Serial_Number = line[2]
            Friendly_Name = line[7]
            try:
                ContainerID = reg.search(line[8])[0]
                if ContainerID == "00000000-0000-0000-ffff-ffffffffffff":
                    ContainerID = None
            except:
                ContainerID = None
            for date in date_list:
                try:
                    time = datetime.strptime(line[date],'%Y-%m-%d_%H:%M:%S')
                    time.strftime('%Y-%m-%d %H:%M:%S')
                    time_list.append(time)
                except:
                    time = None
                    time_list.append(time)

            curs.execute(sql_usb_stor, (Subkey_Name,Serial_Number,Friendly_Name,ContainerID,time_list[0],time_list[1]))
    conn.commit()
    conn.close()
    usbstor.close()

def usb_db():
    conn = pymysql.connect(host='localhost', user='root', password='root', db='study_db', charset='utf8')
    curs = conn.cursor()
    match = "(?<=\{).+?(?=\})"
    reg = re.compile(match)
    sql_usb = "insert into usb (Subkey_Name,Serial_Number,Friendly_Name,ContainerID,First_Install_Date,Last_Remove_Date) values (%s, %s, %s, %s, %s, %s)"
    usb = open('usb.csv', 'r', encoding='utf-8')
    usb_reader = csv.reader(usb)
    print(usb_reader)
    index = 0;
    for line in usb_reader:
        date_list=[8,11]
        time_list =[]
        if index == 0:
            index +=1
            pass
        else:
            Subkey_Name = line[0]
            Serial_Number = line[2]
            Friendly_Name = line[5]
            try:
                ContainerID = reg.search(line[6])[0]
                if ContainerID == "00000000-0000-0000-ffff-ffffffffffff":
                    ContainerID = None
            except:
                ContainerID = None
            for date in date_list:
                try:
                    time = datetime.strptime(line[date],'%Y-%m-%d_%H:%M:%S')
                    time.strftime('%Y-%m-%d %H:%M:%S')
                    time_list.append(time)
                except:
                    time = None
                    time_list.append(time)

    #         curs.execute(sql_usb, (Subkey_Name, Serial_Number, Friendly_Name, ContainerID, time_list[0], time_list[1]))
    # conn.commit()
    # conn.close()
    # usb.close()
if __name__ == "__main__":
    usb_db()
    #usb_stor_db()