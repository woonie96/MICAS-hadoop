import pymysql
import csv
import re
conn = pymysql.connect(host='localhost', user='root', password='root', db='study_db',charset='utf8')
curs = conn.cursor()
sql_wpdbusenum="insert into wpdbusenum (Device_Class, Device_Desc,Friendly_Name, ContainerID, Mfg) values (%s, %s, %s, %s, %s)"
match ="(?<=\{).+?(?=\})"
reg = re.compile(match)
example="'_??_USBSTOR#Disk&Ven_SMI&Prod_USB_DISK&Rev_1100#AA00000000015049&0#{53f56307-b6bf-11d0-94f2-00a0c91efb8b}', 'USB DISK        ', 'D:\\', '{00000000-0000-0000-ffff-ffffffffffff}', 'SMI     '"
wpdbusenum = open('wpdbusenum.csv', 'r', encoding='utf-8')
wpdbusenum_reader = csv.reader(wpdbusenum)
index = 0
for line in wpdbusenum_reader:

    if index == 0:
        index +=1
        pass
    else:
        try:
            id = line[0].split('#')[0]
            DeviceClass = reg.search(id)[0]

        except:
            DeviceClass = line[0].split('#')[2].split('&')[0]
        try:
            ContainerID = reg.search(line[3])[0]
            if ContainerID == "00000000-0000-0000-ffff-ffffffffffff":
                ContainerID = None
        except:
            ContainerID = None
        curs.execute(sql_wpdbusenum, (DeviceClass,line[1],line[2],ContainerID,line[4]))

conn.commit()
conn.close()
wpdbusenum.close()
