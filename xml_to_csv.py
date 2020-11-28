import xml.etree.ElementTree as ET
import csv
import re
import os
import pymysql
import csv
import Evtx.Evtx as evtx
from datetime import datetime

output_path=os.getcwd()+'\\usb_xml\\'

try:
    os.mkdir(output_path)
except:
    pass
def evtx_parse():
    file = 'Microsoft-Windows-DriverFrameworks-UserMode%4Operational.evtx'
    with evtx.Evtx(file) as log:
        id = 0
        for record in log.records():
            #print(dir(record))
            with open(output_path+ str(id) +'_record.xml','w') as fd:
                fd.write(record.xml())
            id+=1

def xml_to_csv():
	Resident_Data = open('usblog.csv', 'w',newline='')
	csvwriter = csv.writer(Resident_Data)
	xml_list = os.listdir(output_path)
	for xml_file in xml_list:
		usb_log_element = []
		xml = output_path+xml_file
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
def csv_to_db():
	conn = pymysql.connect(host='localhost', user='root', password='root', db='study_db', charset='utf8')
	curs = conn.cursor()
	sql_usb_log = "insert into usb_log (event_id, system_time, serial_number,Manufacturer,usb_name) values (%s, %s, %s, %s, %s)"
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
				serial = line[2].split('#')[2]
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

if __name__ == "__main__":
	evtx_parse()
	xml_to_csv()
	csv_to_db()