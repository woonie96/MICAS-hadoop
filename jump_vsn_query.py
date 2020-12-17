import pymysql
import sys
import os
import datetime
def jump_vsn(case_name,image_name,input_vsn):

    conn = pymysql.connect(host='192.168.4.188', user='hadoopuser', password='Hadoopuser1!', db=case_name, charset='utf8')
    curs = conn.cursor()
    image_jump_sql = "select * from Jumplist where Artifact_ID in (select Artifact_ID from Artifact where Image_ID in (select Image_ID from Disk_Image where Image_Name like \""+image_name+"%\"));"

    curs.execute(image_jump_sql)
    result =[]
    for Jumplist_ID, Artifact_ID, ID, Modified, Accessed, Created, Drive_Type, Friendly_Name, VSN, File_Size, Local_Base_Path in curs.fetchall():
        row =[Jumplist_ID, Artifact_ID, ID, Modified, Accessed, Created, Drive_Type, Friendly_Name, VSN, File_Size, Local_Base_Path]
        if VSN == input_vsn:
            # print("Jumplist_ID, Artifact_ID, ID, Modified, Accessed, Created, Drive_Type, Friendly_Name, VSN, File_Size, Local_Base_Path")
            # print(Jumplist_ID, Artifact_ID, ID, Modified, Accessed, Created, Drive_Type, Friendly_Name, VSN, File_Size, Local_Base_Path)
            result.append(row)
    return result

def partition_usb(case_name, image_name):
    conn = pymysql.connect(host='192.168.4.188', user='hadoopuser', password='Hadoopuser1!', db=case_name, charset='utf8')
    curs = conn.cursor()
    partition_sql ="select * from Usb_Partition_Log where Artifact_ID in (select Artifact_ID from Artifact where Image_ID in (select Image_ID from Disk_Image where Image_Name like \""+image_name+"%\"));"

    curs.execute(partition_sql)
    for Artifact_ID, Manufacturer, Model, Serial_Number, VSN in curs.fetchall():
        input_serial_number = Serial_Number
        usb_sql = "select * from Usb where Serial_Number like \""+input_serial_number+"\";"
        curs.execute(usb_sql)
        for USB_ID, Artifact_ID, Serial_Number, Container_ID, First_Install_Date, Last_Remove_Date, Friendly_Name, Type in curs.fetchall():
            print(USB_ID, Artifact_ID, Serial_Number, Container_ID, First_Install_Date, Last_Remove_Date, Friendly_Name, Type)

def jump_file_name(case_name):
    conn = pymysql.connect(host='192.168.4.188', user='hadoopuser', password='Hadoopuser1!', db=case_name, charset='utf8')
    curs = conn.cursor()

    jump_removable = "select Jumplist_ID, Artifact_ID, Modified, Accessed, Created, VSN, File_Size, Local_Base_Path from Jumplist where Drive_Type like \"Removable\";"
    curs.execute(jump_removable)

    Jump_Info =[]
    for Jumplist_ID,Artifact_ID, Modified, Accessed, Created, VSN, File_Size, Local_Base_Path in curs.fetchall():
        MAC_time = []
        if File_Size != '0':
            MAC_time.append([Modified,Accessed,Created])
            Local_Base_Path = Local_Base_Path.replace("\\", "/")
            File_Name = os.path.basename(Local_Base_Path)
            File_Name = os.path.splitext(File_Name)[0]
            Jump_Info.append([Jumplist_ID,Artifact_ID,MAC_time,VSN,File_Size,File_Name]) #File_Name = list[5]
        else:
            pass

    Usn_list =[]
    new_list =[]

    for list in Jump_Info:
        Usnjrnl_sql = "select Usn, Artifact_ID, TimeStamp, MFT_Entry, File_Name from UsnJrnl where File_Name like \"%"+list[5]+"%\";"
        curs.execute(Usnjrnl_sql)
        for Usn,Artifact_ID, TimeStamp, MFT_Entry, File_Name in curs.fetchall():
            Usn_list =[Artifact_ID,MFT_Entry]
            if Usn_list not in new_list:
                new_list.append([Artifact_ID,MFT_Entry])

    #print(new_list)
    for element in new_list:
        Usnjrnl_final_sql = "select * from UsnJrnl where Artifact_ID =\""+str(element[0])+"\" and MFT_Entry =\""+str(element[1])+"\";"
        curs.execute(Usnjrnl_final_sql)
        for Usn, Artifact_ID, TimeStamp,Reason, MFT_Entry, File_Name in curs.fetchall():
            print(Usn, Artifact_ID, TimeStamp, Reason, MFT_Entry, File_Name)
        print("----------------------------------------------------------------------")

def usb_connect_time(case_name, image_name):
    conn = pymysql.connect(host='192.168.4.188', user='hadoopuser', password='Hadoopuser1!', db=case_name,charset='utf8')
    curs = conn.cursor()

    connect_sql = "select Event_ID, System_Time, Serial_Number,Event_Log_Id.Status from Usb_Event_Log join Event_Log_Id on Usb_Event_Log.Event_ID = Event_Log_Id.ID where Artifact_ID in (select Artifact_ID from Artifact where Image_ID in (select Image_ID from Disk_Image where Image_Name like \""+image_name+"%\")) order by System_Time;"
    curs.execute(connect_sql)
    for Event_ID, System_Time, Serial_Number, Status in curs.fetchall():
        print(Event_ID, System_Time, Serial_Number, Status)

def jumpfile_usb_name(case_name,image_name):
    conn = pymysql.connect(host='192.168.4.188', user='hadoopuser', password='Hadoopuser1!', db=case_name, charset='utf8')
    curs = conn.cursor()
    time_list =[] #연결해제 임시값
    doc_list = [] #문서의 정보

    act_list=[]
    connect_act_list = []
    new_connect_act_list = []


    jump_removable = "select Jumplist_ID, Artifact_ID, Modified, Accessed, Created, VSN, File_Size, Local_Base_Path from Jumplist where Drive_Type like \"Removable\" and Artifact_ID in (select Artifact_ID from Artifact where Image_ID in (select Image_ID from Disk_Image where Image_Name like \"%"+image_name+"%\"));"
    curs.execute(jump_removable)

    Jump_Info =[]
    for Jumplist_ID,Artifact_ID, Modified, Accessed, Created, VSN, File_Size, Local_Base_Path in curs.fetchall():
        #MAC_time = []
        #MAC_time.append([Modified,Accessed,Created])
        Local_Base_Path = Local_Base_Path.replace("\\", "/")
        File_Name = os.path.basename(Local_Base_Path)
        #print(File_Name)
        File_Name1 = os.path.splitext(File_Name)[0]
        #print(File_Name1)
        serial_sql = "select Serial_Number from Usb_Partition_Log where VSN = \""+VSN+"\" and Artifact_ID in (select Artifact_ID from Artifact where Image_ID in (select Image_ID from Disk_Image where Image_Name like \"%"+image_name+"%\"));"
        #print(VSN)
        curs.execute(serial_sql)
        Serial = curs.fetchone()[0]
        #print(curs.fetchone()[0])
        Jump_Info.append([Jumplist_ID,Artifact_ID,Created,VSN,File_Size,File_Name,image_name,Serial]) #File_Name = list[5]

    # for line in Jump_Info:
    #     print(line)

    for line in Jump_Info:
        File_Name = line[5]
        Created = line[2]
        image_name = line[6]
        Serial_Number = line[7]
        Artifact_id = line[1]
        document_sql = "select Document_ID, Artifact_ID, File_Local_Path from Document where File_Local_Path like\"%"+File_Name+"%\" and Artifact_ID in (select Artifact_ID from Artifact where Image_ID in (select Image_ID from Disk_Image where Image_Name like \"%"+image_name+"%\"));"


        curs.execute(document_sql)
        for Document_ID, Artifact_ID, File_Local_Path in curs.fetchall():
            element =[Document_ID, Artifact_id,Created, File_Local_Path,image_name,Serial_Number]
            if element not in doc_list:
                doc_list.append(element)

    # for line in doc_list:
    #     print(line)

    for column in doc_list:
        act_list.append([column[0], column[1],column[2], 'USB', 'File_Execute', "File_Name: "+column[3]+" Serial_Number: "+column[5],column[5]]) #if document = system_time = act_name -> 하나로 저장
    new_act_list =[]
    for line in act_list:
        if line not in new_act_list:
            new_act_list.append(line)

    # for line in new_act_list:
    #     print(line)

    for line in doc_list: #Created 타임
        new_time_list = []  # usb의 연결 해제 정보
        #print(line[5])
        event_query = "select Artifact_ID,Event_ID, System_Time, Serial_Number,Event_Log_Id.Status from Usb_Event_Log join Event_Log_Id on Usb_Event_Log.Event_ID = Event_Log_Id.ID where Artifact_ID in (select Artifact_ID from Artifact where Image_ID in (select Image_ID from Disk_Image where Image_Name like \"" + image_name + "%\")) and Serial_Number like \""+line[5]+"\" order by System_Time;"
        curs.execute(event_query)

        for Artifact_ID1, Event_ID, System_Time, Serial_Number, Status in curs.fetchall():
            time_list.append([Artifact_ID1, System_Time, Serial_Number, Status, image_name])
        print(time_list)
        for line in time_list:
            Artifact = time_list[0]
            if line not in new_time_list:
                new_time_list.append(line)
        #print(new_time_list)

        max_time = datetime.datetime(2300, 1, 1, 00, 00, 00)
        min_time = datetime.datetime(1900, 1, 1, 00, 00, 00)
        #Artifact = new_time_list[0]
        print(new_time_list)
        for time in new_time_list:
            # min_time = time[0] #System_Time
            # max_time = time[0]
            #print(line[2], min_time, max_time)
            if time[3] == "connect":
                if time[1] < line[2]:
                    min_time = time[1] #시간 값들중 가장 큰 것
            if time[3] == 'disconnect':
                if time[1] > line[2] and max_time >time[1]:
                    max_time = time[1]
        connect_act_list.append([line[0], Artifact,min_time, 'USB', 'Connect', "File_Name: "+line[3]+" Serial_Number: "+line[5]])
        connect_act_list.append([line[0], Artifact,max_time, 'USB', 'Disconnect', "File_Name: "+line[3]+" Serial_Number: "+line[5]])

    for line in connect_act_list:
        if line not in new_connect_act_list:
            new_connect_act_list.append(line)

    for line in new_act_list:
        new_connect_act_list.append(line)

    for line in new_connect_act_list:
        print(line)


    # for line in new_connect_act_list:
    #     #print(line)
    #     act_sql = "insert into Act (Document_ID, Act_time, Act_Type, Act_Name, Act_Comment) values(%s,%s,%s,%s,%s)"
    #     curs.execute(act_sql, (line[0], line[2], line[3], line[4], line[5]))
    #     conn.commit()
    #     curs.execute("select last_insert_id();")
    #     Act_ID = curs.fetchone()[0]
    #     act_reason_sql = "insert into Act_Reason (Act_ID, Artifact_ID) values (%s, %s);"
    #     curs.execute(act_reason_sql,(Act_ID,line[1]))
    #     conn.commit()
    # conn.close()

    #print(min_time, max_time)

def document_id(case_name):
    conn = pymysql.connect(host='192.168.4.188', user='hadoopuser', password='Hadoopuser1!', db=case_name, charset='utf8')
    curs = conn.cursor()

def time_sort():
    time =[]
    max_time4 = datetime.datetime(2020, 10, 11, 10, 10, 2)
    max_time5 = datetime.datetime(2020, 10, 11, 10, 10, 3)
    max_time1 = datetime.datetime(2200, 1, 1, 00, 00, 00)
    max_time2 = datetime.datetime(2300, 1, 1, 00, 00, 00)
    max_time3 = datetime.datetime(2100, 1, 1, 00, 00, 00)

    time.append(max_time1)
    time.append(max_time2)
    time.append(max_time3)
    time.append(max_time4)
    time.append(max_time5)

    time = sorted(time)

    for line in time:
        print(line)

def similar_check(case_name, Document):
    conn = pymysql.connect(host='192.168.4.188', user='hadoopuser', password='Hadoopuser1!', db=case_name,charset='utf8')
    curs = conn.cursor()

    first_sql ="select  distinct Document.Document_ID from Relate_Document join Document on Relate_Document.Document_ID = Document.Document_ID where Relate_ID = %s order by Document.Document_ID;"
    similar_sql ="select Reason, Type from Relate_Document join Document on Relate_Document.Document_ID = Document.Document_ID where Relate_ID = %s and Document.Document_ID =%s;"
    curs.execute(first_sql,Document)


    similar_list =[]
    new_list=[]
    for Document_ID in curs.fetchall():
        list = {'Doc_ID':'','SHA':'','TLHash':'','File_Name':'','Similar':''}
        curs.execute(similar_sql, (Document,Document_ID))
        list['Doc_ID'] = Document_ID[0]
        for Reason, Type in curs.fetchall():
            if Reason == 'TLHash':
                list['TLHash'] = Type
            elif Reason == 'SHA':
                list['SHA'] = Type
            elif Reason == 'File_Name':
                list['File_Name'] = Type
        new_list.append(list)

    for line in new_list:
        if line['SHA'] == 'Same':
            line['Similar'] = 'Sha'
            continue
        elif line['TLHash'] == 'Same':
            line['Similar'] = 'TLHash'
            continue
        elif line['TLHash'] == 'Similar':
            line['Similar'] = 'TLHash'
            continue
        elif line['File_Name'] == 'Same':
            line['Similar'] = 'File_Name'
            continue
        elif line['File_Name'] == None:
            line['Similar'] = 'Not Similar'
            continue

    for line in new_list:
        print(line)


    # for line in list:
    #     if line[0] not in new_list:
    #         new_list.append(line[0])
    #     if line[2] == 'Sha256':
    #         new_list.append()
    #



if __name__ == "__main__":
    #print(jump_vsn(sys.argv[1],sys.argv[2],sys.argv[3]))
    # partition_usb(sys.argv[1],sys.argv[2])
    # print('-----------------------------------------')
    # jump_file_name(sys.argv[1])
    # print('-----------------------------------------')
    # usb_connect_time(sys.argv[1],sys.argv[2])
    # print('-----------------------------------------')
    jumpfile_usb_name(sys.argv[1],sys.argv[2])
    #time_sort()
    #similar_check(sys.argv[1], sys.argv[2])