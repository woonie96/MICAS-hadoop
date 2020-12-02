import xml.etree.ElementTree as ET
import csv
import base64
import re
import os
import pymysql
import csv
import Evtx.Evtx as evtx
from datetime import datetime

driver_output_path=os.getcwd()+'\\driver_usb_xml\\'
partition_output_path=os.getcwd()+'\\partition_usb_xml\\'

try:
    os.mkdir(driver_output_path)
    os.mkdir(partition_output_path)
except:
    pass


def Driver_evtx_parse():

    try:
        os.mkdir(driver_output_path)
    except:
        pass

    file = 'Microsoft-Windows-DriverFrameworks-UserMode%4Operational.evtx'
    with evtx.Evtx(file) as log:
        id = 0
        for record in log.records():
            #print(dir(record))
            with open(driver_output_path+ str(id) +'_record.xml','w') as fd:
                fd.write(record.xml())
            id+=1
def Partition_evtx_parse():
    try:
        os.mkdir(partition_output_path)
    except:
        pass
    file = 'Microsoft-Windows-Partition%4Diagnostic.evtx'
    with evtx.Evtx(file) as log:
        id = 0
        for record in log.records():
            #print(dir(record))
            with open(partition_output_path+ str(id) +'_record.xml','w') as fd:
                fd.write(record.xml())
            id+=1

def Driver_xml_to_csv():
    Resident_Data = open('usblog.csv', 'w',newline='')
    csvwriter = csv.writer(Resident_Data)
    xml_list = os.listdir(driver_output_path)
    for xml_file in xml_list:
        usb_log_element = []
        xml = driver_output_path+xml_file
        tree = ET.parse(xml)
        root = tree.getroot()
        try:
            event_id = root[0][1].text
            usb_log_element.append(event_id)
        except:
            event_id = None
            usb_log_element.append(event_id)
        try:
            system_time = root[0][7].attrib['SystemTime']
            usb_log_element.append(system_time)
        except:
            system_time = None
            usb_log_element.append(system_time)
        try:
            instance_id = root[1][0][1].text
            usb_log_element.append(instance_id)
        except:
            instance_id = None
            usb_log_element.append(instance_id)
        csvwriter.writerow(usb_log_element)

    Resident_Data.close()
def Partition_xml_to_csv():
    Resident_Data = open('partitionlog.csv', 'w', newline='')
    csvwriter = csv.writer(Resident_Data)
    xml_list = os.listdir(partition_output_path)
    for xml_file in xml_list:
        usb_log_element = []
        xml = partition_output_path + xml_file
        tree = ET.parse(xml)
        root = tree.getroot()
        try:
            Manufacturer = root[1][10].text
            usb_log_element.append(Manufacturer)
        except:
            Manufacturer = None
            usb_log_element.append(Manufacturer)
        try:
            Model = root[1][11].text
            usb_log_element.append(Model)
        except:
            Model = None
            usb_log_element.append(Model)
        try:
            ParentId = root[1][15].text
            SerialNumber = ParentId.split('\\')[2]
            usb_log_element.append(SerialNumber)
        except:
            ParentId = None
            usb_log_element.append(ParentId)
        try:
            VBR = root[1][74].text
            vbr_decode = base64.b64decode(VBR).hex()
            vsn_reverse = vbr_decode[144:152]
            vsn = '0x'
            count = 9
            for index in range(4):
                count -= 2
                vsn = vsn + vsn_reverse[count - 1:count + 1]
            usb_log_element.append(vsn)
        except:
            vsn = None
            usb_log_element.append(vsn)
        csvwriter.writerow(usb_log_element)
    Resident_Data.close()
def logcsv_to_db():
    conn = pymysql.connect(host='localhost', user='root', password='root', db='study_db', charset='utf8')
    curs = conn.cursor()
    sql_usb_log = "insert into usb_log (event_id, system_time, Serial_Number,Manufacturer,usb_name) values (%s, %s, %s, %s, %s)"
    usb_log = open('usblog.csv','r',encoding='utf-8')
    usb_log_reader = csv.reader(usb_log)
    match = "(?<=\{).+?(?=\})"
    reg = re.compile(match)
    for line in usb_log_reader:
        if line[2].startswith('USB'):
            try:
                serial = line[2].split('\\')[2]
                prod = line[2].split('\\')[1].split('&')[0].split('VID_')[1]
                ven = line[2].split('\\')[1].split('&')[1].split('PID_')[1]
                t1 = datetime.strptime(line[1], '%Y-%m-%d %H:%M:%S.%f')
                t1.strftime('%Y-%m-%d %H:%M:%S')
            except:
                serial = line[2]
                prod = None
                ven = None
        elif line[2].startswith('SWD'):
            try:
                serial = line[2].split('#')[2].split('&')[0]
                ven = line[2].split('&')[1].split('VEN_')[1]
                prod = line[2].split('&')[2].split('PROD_')[1]
                t1 = datetime.strptime(line[1], '%Y-%m-%d %H:%M:%S.%f')
                t1.strftime('%Y-%m-%d %H:%M:%S')
            except:
                serial = reg.search(line[2])[0]
                prod = None
                ven = None
        else:
            continue

        curs.execute(sql_usb_log,(line[0],t1,serial,ven,prod))

    conn.commit()
    conn.close()
    usb_log.close()
def partitioncsv_to_db():
    conn = pymysql.connect(host='localhost', user='root', password='root', db='study_db', charset='utf8')
    curs = conn.cursor()
    sql_partition_log = "insert into usb_partition(Manufacturer , Model, Serial_Number , VSN) values (%s, %s, %s, %s)"
    partition_log = open('partitionlog.csv','r',encoding='utf-8')
    partition_log_reader = csv.reader(partition_log)
    match = "(?<=\{).+?(?=\})"
    reg = re.compile(match)
    for line in partition_log_reader:
        curs.execute(sql_partition_log,(line[0],line[1],line[2],line[3]))

    conn.commit()
    conn.close()
    partition_log.close()
if __name__ == "__main__":
    # Driver_evtx_parse()
    # Driver_xml_to_csv()
    # logcsv_to_db()
    #Partition_evtx_parse()
    Partition_xml_to_csv()
    #partitioncsv_to_db()