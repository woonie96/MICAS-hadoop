from evtx import PyEvtxParser
import json
from datetime import datetime
import re
import pymysql
import sys


match = "(?<=\{).+?(?=\})"
reg = re.compile(match)
def driver(case_name, file_name,Artifact_ID):
    conn = pymysql.connect(host='192.168.4.188', user='hadoopuser', password='Hadoopuser1!', db=case_name, charset='utf8')
    curs = conn.cursor()

    sql_usb_log = "insert into Usb_Event_Log (Artifact_ID, Event_ID,System_Time, Serial_Number, Manufacturer,Usb_Name) values (%s, %s, %s, %s, %s, %s)"

    file = file_name
    parser = PyEvtxParser(file)

    id =0
    try:
        for record in parser.records_json():
            id += 1
            event = json.loads(record['data'])['Event']
            try:
                Event_ID = event['System']['EventID']
            except:
                Event_ID = None
                print("Event_ID Error")
            try:
                timestamp = record['timestamp']
            except:
                timestamp = None
                print("Timestamp Error")
            try:
                Instance_ID = event['UserData']['UMDFHostDeviceRequest']['InstanceId']
                if Instance_ID.startswith('USB'):
                    try:
                        serial = Instance_ID.split('\\')[2]
                    except:
                        serial = Instance_ID
                    try:
                        prod = Instance_ID.split('\\')[1].split('&')[0].split('VID_')[1]
                    except:
                        prod = None
                    try:
                        ven = Instance_ID.split('\\')[1].split('&')[1].split('PID_')[1]
                    except:
                        ven = None
                    try:
                        t1 = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f UTC')
                        t1.strftime('%Y-%m-%d %H:%M:%S')
                    except:
                        t1 = datetime.datetime(1900, 1, 1, 00, 00, 00)
                elif Instance_ID.startswith('SWD'):
                    try:
                        serial = Instance_ID.split('#')[2].split('&')[0]
                    except:
                        serial = reg.search(Instance_ID)[0]
                    try:
                        ven = Instance_ID.split('&')[1].split('VEN_')[1]
                    except:
                        ven = None
                    try:
                        prod = Instance_ID.split('&')[2].split('PROD_')[1]
                    except:
                        prod = None
                    try:
                        t1 = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f UTC')
                        t1.strftime('%Y-%m-%d %H:%M:%S')
                    except:
                        t1 = datetime.datetime(1900, 1, 1, 00, 00, 00)
                else:
                    continue

            except:
                print("Instance_ID Error")

            curs.execute(sql_usb_log,(Artifact_ID, Event_ID,t1, serial,ven,prod))
    except:
        pass

    conn.commit()
    conn.close()

def partition(case_name, file_name, Artifact_ID):
    conn = pymysql.connect(host='192.168.4.188', user='hadoopuser', password='Hadoopuser1!', db=case_name,charset='utf8')
    curs = conn.cursor()
    file = file_name
    sql_partition_log = "insert into Usb_Partition_Log(Artifact_ID,Manufacturer , Model, Serial_Number , VSN) values (%s, %s, %s, %s, %s)"
    parser = PyEvtxParser(file)
    instance = 0
    id =0
    table =[]
    try:
        for record in parser.records_json():
            id += 1
            data = json.loads(record['data'])['Event']
            try:
                Manufacture = data['EventData']['Manufacturer']
            except:
                Manufacture = None
                print("Manufacture error")
            try:
                Model = data['EventData']['Model']
            except:
                Model = None
                print("Model error")
            try:
                ParentId = data['EventData']['ParentId']
                Serial_Number = ParentId.split('\\')[2]
            except:
                Serial_Number = None
                print("Serial Number error")
            try:
                VBR = data['EventData']['Vbr0']
                
                if VBR[6:14] =='4e544653':
                    vsn_reverse = VBR[144:152] #NTFS
                    vsn = '0x'
                    count = 9
                    for index in range(4):
                        count -= 2
                        vsn = vsn + vsn_reverse[count - 1:count + 1]
    
                elif VBR[164:174] =='4641543332':
                    vsn_reverse = VBR[134:142]  # FAT32
                    vsn = '0x'
                    count = 9
                    for index in range(4):
                        count -= 2
                        vsn = vsn + vsn_reverse[count - 1:count + 1]
    
                elif VBR[6:16] == '4558464154':
                    vsn_reverse = VBR[200:208]  # exfat
                    vsn = '0x'
                    count = 9
                    for index in range(4):
                        count -= 2
                        vsn = vsn + vsn_reverse[count - 1:count + 1]
    
                elif VBR[108:116] == '46415431':
                    vsn_reverse = VBR[78:86]  # fat16
                    vsn = '0x'
                    count = 9
                    for index in range(4):
                        count -= 2
                        vsn = vsn + vsn_reverse[count - 1:count + 1]
                else:
                    vsn = None
            except:
                vsn = None
                print("vsn error")
            if Manufacture != None and Model != None and Serial_Number != None and vsn != None:
                table.append([Manufacture, Model, Serial_Number, vsn])

        new_table = []
        for element in table:
            if element not in new_table:
                new_table.append(element)

        for column in new_table:
            curs.execute(sql_partition_log, (Artifact_ID, column[0], column[1], column[2], column[3]))
    
    
    except:
        print("sql error")
    conn.commit()
    conn.close()

def event_id(case_name):
    conn = pymysql.connect(host='192.168.4.188', user='hadoopuser', password='Hadoopuser1!', db=case_name, charset='utf8')
    curs = conn.cursor()
    evtx_list = [[2003,'connect'], [2004, 'connect'], [2006, 'connect'], [2102,'disconnect']]
    for list in evtx_list:
        evtx_sql = "insert into Event_Log_Id values( %s ,%s);"
        curs.execute(evtx_sql,(list[0], list[1]))
    conn.commit()
    conn.close()


def run(case_name):
    conn = pymysql.connect(host='192.168.4.188', user='hadoopuser', password='Hadoopuser1!', db=case_name,
                           charset='utf8')
    curs = conn.cursor()
    artifact_sql = "select Artifact_ID, File_Path from Artifact where File_Path like \"%Microsoft-Windows-DriverFrameworks-UserMode%4Operational.evtx%\";"
    curs.execute(artifact_sql)
    for Artifact_ID, File_Path in curs.fetchall():
        print(str(Artifact_ID) + '    ' + File_Path)
        driver(case_name,File_Path,Artifact_ID)

    partition_sql = "select Artifact_ID, File_Path from Artifact where File_Path like \"%Microsoft-Windows-Partition%4Diagnostic.evtx%\";"
    curs.execute(partition_sql)
    event_id(case_name)
    for Artifact_ID, File_Path in curs.fetchall():
        print(str(Artifact_ID) + '    ' + File_Path)
        partition(case_name,File_Path,Artifact_ID)

    conn.commit()
    conn.close()
if __name__ == "__main__":
    run(sys.argv)
