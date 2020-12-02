import olefile
import os
import uuid, struct, datetime
from bitstring import BitArray
import pymysql
import csv

output_path = os.getcwd()+'\\auto\\'
csv_output_path = os.getcwd()+'\\lnk_csv\\'


def FromFiletime(filetime):
    if filetime < 0:
        return None
    timestamp = filetime / 10

    date_time = datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=timestamp)
    return date_time.strftime("%Y-%m-%d %H:%M:%S")
# This is the function to parse the LNK Flags bitstring
# To get this to work, you do lnk_flags(bits_test.bin)
def lnk_flags(flags_to_parse):
    flags = {0: "HasLinkTargetIDList",
             1: "HasLinkInfo",
             2: "HasName",
             3: "HasRelativePath",
             4: "HasWorkingDir",
             5: "HasArguments",
             6: "HasIconLocation",
             7: "IsUnicode",
             8: "ForceNoLinkInfo",
             9: "HasExpString",
             10: "RunInSeparateProcess",
             11: "Unused1",
             12: "HasDarwinID",
             13: "RunAsUser",
             14: "HasExpIcon",
             15: "NoPidlAlias",
             16: "Unused2",
             17: "RunWithShimLayer",
             18: "ForceNoLinkTrack",
             19: "EnableTargetMetadata",
             20: "DisableLinkPathTracking",
             21: "DisableKnownFolderTracking",
             22: "DisableKnownFolderAlias",
             23: "AllowLinkToLink",
             24: "UnaliasOnSave",
             25: "PreferEnvironmentPath",
             26: "KeepLocalIDListForUNCTarget"}

    flags_to_parse = flags_to_parse[::-1]  # reverse the list
    setflags = []
    for count, items in enumerate(flags_to_parse):
        if int(items) == 1:
            # setflags = setflags.append(count)
            print("{} is set.".format(flags[count]))
            # return setflags
        else:
            continue
# This is the function to parse the attributes
# So to get this to work, you do lnk_attrib(bits_test.bin)
def lnk_attrib(attrib_to_parse):
    attrib = {0: "FILE_ATTRIBUTE_READONLY",
              1: "FILE_ATTRIBUTE_HIDDEN",
              2: "FILE_ATTRIBUTE_SYSTEM",
              3: "Reserved1",
              4: "FILE_ATTRIBUTE_DIRECTORY",
              5: "FILE_ATTRIBUTE_ARCHIVE",
              6: "Reserved2",
              7: "FILE_ATTRIBUTE_NORMAL",
              8: "FILE_ATTRIBUTE_TEMPORARY",
              9: "FILE_ATTRIBUTE_SPARSE_FILE",
              10: "FILE_ATTRIBUTE_REPARSE_POINT",
              11: "FILE_ATTRIBUTE_COMPRESSED",
              12: "FILE_ATTRIBUTE_OFFLINE",
              13: "FILE_ATTRIBUTE_NOT_CONTENT_INDEXED",
              14: "FILE_ATTRIBUTE_ENCRYPTED"}

    for count, items in enumerate(attrib_to_parse):
        if int(items) == 1:
            # print("")
            print("{} is set.".format(attrib[count]))
        else:
            continue
# This function parses the SHOWCOMMAND data
def lnk_show_win(showwin):
    if showwin == hex(0x1):
        return "SW_SHOWNORMAL"
    elif showwin == hex(0x3):
        return "SW_SHOWMAXIMIZED"
    elif showwin == hex(0x7):
        return "SW_SHOWMINNOACTIVE"
    else:
        return "SW_SHOWNORMAL (default)"
# This function parses the High Byte section of the hotkey value
def lnk_hot_key_high(hotkey_high):
    hotkey = {"0x0": "None",
              "0x1": "Shift",
              "0x2": "Ctrl",
              "0x3": "Shift + Ctrl",
              "0x4": "Alt",
              "0x5": "Shift + Alt",
              "0x6": "Ctrl + Alt"}
    bits_hotkey = BitArray(hex(hotkey_high))
    return hotkey[str(bits_hotkey)]
# This function parses out the Low Byte section of the hotkey value
def lnk_hot_key_low(hotkey):
    return chr(hotkey)
# This function parses out the hotkey data; it passes it on to two other functions
def lnk_hot_key_parse(hotkey):
    hotkey_one = lnk_hot_key_high(hotkey[1])
    hotkey_two = lnk_hot_key_low(hotkey[0])
    return hotkey_one, hotkey_two
def convert_hex_to_ascii(h):
    h = h[2:16]
    machine_id = ''.join([chr(int(''.join(c), 16)) for c in zip(h[0::2], h[1::2])])
    return machine_id[::-1]
def convert_mac(mac):
    mac = mac[2:10] + mac[12:16]
    mac = [mac[i:i + 2] for i in range(0, len(mac), 2)]
    return ':'.join(str(i) for i in mac)
def change(changehex):
    changehex = changehex[:2] + changehex[10:] + changehex[6:10] + changehex[2:6]
    return changehex
def convert_hex(gethex):
    # print(gethex)
    gethex = gethex[:2] + "0" + gethex[3:]
    # print(gethex)
    return int(gethex, 0)
# This function parses the LNK file header data
def lnk_file_header(header_data):
    header_list = []  # empty List

    lnk_header_size = struct.unpack("<L", header_data[0:4])
    header_clsid = header_data[4:20]
    lnk_header_clsid = uuid.UUID(bytes_le=header_clsid)

    # These two lines will parse out the individual bits in the Link flags section
    lnk_header_flags = struct.unpack("<I", header_data[20:24])
    lnk_header_flags_bits = BitArray(hex(lnk_header_flags[0]))

    # These two lines will parse out the individual bits for the file attributes
    lnk_header_file_attrib = struct.unpack("<I", header_data[24:28])
    lnk_header_file_attrib_bits = BitArray(hex(lnk_header_file_attrib[0]))

    # Parse the creation time stamp
    header_creation_time = struct.unpack("<Q", header_data[28:36])
    lnk_header_creation_time = FromFiletime(header_creation_time[0])

    # Parse the access time stamp
    header_access_time = struct.unpack("<Q", header_data[36:44])
    lnk_header_access_time = FromFiletime(header_access_time[0])

    # Parse the write time stamp
    header_write_time = struct.unpack("<Q", header_data[44:52])
    lnk_header_write_time = FromFiletime(header_write_time[0])

    lnk_header_file_size = struct.unpack("<L", header_data[52:56])
    lnk_header_icon_indx = struct.unpack("<L", header_data[56:60])
    lnk_header_show_window = struct.unpack("<L", header_data[60:64])
    lnk_header_hot_key = struct.unpack("<2B", header_data[64:66])
    hot_key = lnk_hot_key_parse(lnk_header_hot_key)

    # print("Header size: {} (integer: {})".format(hex(lnk_header_size[0]), lnk_header_size[0]))
    # print("\n\n<<<<<<<<<<<<<<Parsing Link Header Information>>>>>>>>>>>>>>>>")
    # print("Header CLSID: {}".format(lnk_header_clsid))
    # print("Flags:\n")
    # lnk_flags(lnk_header_flags_bits.bin)
    # print("Attributes:\n")
    # lnk_attrib(lnk_header_file_attrib_bits.bin)
    # print("Target Creation Time: {}".format(lnk_header_creation_time))
    # print("Target Access Time: {}".format(lnk_header_access_time))
    # print("Target Write Time: {}".format(lnk_header_write_time))
    # print("Target File Size: {}".format(lnk_header_file_size[0]))
    header_list.append(lnk_header_write_time)
    header_list.append(lnk_header_access_time)
    header_list.append(lnk_header_creation_time)
    header_list.append(lnk_header_file_size[0])

    # print("Icon Index: {}".format(lnk_header_icon_indx[0]))
    # print("Show Window Value: {}".format(lnk_show_win(hex(lnk_header_show_window[0]))))
    # print("Hot Key: {} {}".format(hot_key[0], hot_key[1]))
    return header_list
# This function parses the LNK file data from 76 bytes to size -100 bytes
def lnk_file_after_header(lnk_file_data):
    after_header_list = []  # Empty List

    # Print if HasLinkTargetIDList is set then

    # Item ID Size

    has_lnk_id_list_size = struct.unpack("<H", lnk_file_data[76:78])  # has link target id list size
    # print("has link target id list size= ", has_lnk_id_list_size[0])

    lnk_info_size = struct.unpack("<H", lnk_file_data[76 + has_lnk_id_list_size[0]:76 + has_lnk_id_list_size[
        0] + 2])  # 2 bytes  termination string
    # print("termination of IDList =",lnk_info_size[0])

    # <<<<<<<<<<<<<<<<<<<<<<< Link Information>>>>>>>>>>>>>>>>>>>
    lnk_info_size = struct.unpack("<L", lnk_file_data[78 + has_lnk_id_list_size[0]:82 + has_lnk_id_list_size[
        0]])  # 4 bytes Link ifomation size
    # print("Link infomation size= ",lnk_info_size[0])

    lnk_info_header_size = struct.unpack("<L", lnk_file_data[82 + has_lnk_id_list_size[0]:82 + has_lnk_id_list_size[
        0] + 4])  # 4 bytes header size
    # print("link information header size= ",lnk_info_header_size[0]) # prints link information header size

    lnk_info_flags = struct.unpack("<L", lnk_file_data[86 + has_lnk_id_list_size[0]:86 + has_lnk_id_list_size[
        0] + 4])  # 4 bytes link information flags
    # print("link information flags= ",lnk_info_flags[0]) # if value =3 prints VolumeIDAndLocalBasePath and CommonNetworkRelativeLinkAndPathSuffix are present

    # if lnk_info_flags[0] == 1:
    #     # print("",end="")
    #     print("Flags: VolomeIDAndLocalBasePath")
    # if lnk_info_flags[0] == 3:
    #     print("Flags: VolomeIDAndLocalBasePath,CommonNetworkRelativeLinkAndPathSuffix")
    #     # print("",end="")

    lnk_volumeidoffset = struct.unpack("<L", lnk_file_data[90 + has_lnk_id_list_size[0]:90 + has_lnk_id_list_size[
        0] + 4])  # 4 bytes volume id offset
    # print("VolumeIDOffset = ",lnk_volumeidoffset[0])

    lnk_localbasepathoffset = struct.unpack("<L", lnk_file_data[94 + has_lnk_id_list_size[0]:94 + has_lnk_id_list_size[
        0] + 4])  # 4 bytes volume id offset
    # print("LocalBasePathOffset = ",lnk_localbasepathoffset[0])

    lnk_commonnetworkrelativelinkoffset = struct.unpack("<L", lnk_file_data[
                                                              98 + has_lnk_id_list_size[0]:102 + has_lnk_id_list_size[
                                                                  0]])  # 4 bytes volume id offset
    # print("CommonNetworkRelativeLinkOffset = ",lnk_commonnetworkrelativelinkoffset[0])

    lnk_commonpathsuffixoffset = struct.unpack("<L", lnk_file_data[
                                                     102 + has_lnk_id_list_size[0]:106 + has_lnk_id_list_size[
                                                         0]])  # 4 bytes volume id offset
    # print("CommonPathSuffixOffset = ",lnk_commonpathsuffixoffset[0])

    # <<<<<<<<<<<<<<<<<<Volume Referenece>>>>>>>>>>>>>>

    lnk_volumeid_size = struct.unpack("<L", lnk_file_data[
                                            78 + has_lnk_id_list_size[0] + lnk_volumeidoffset[0]:lnk_volumeidoffset[
                                                                                                     0] + 82 +
                                                                                                 has_lnk_id_list_size[
                                                                                                     0]])  # 4 bytes volume id offset
    # print("VolumeID size= ",lnk_volumeid_size[0]) # prints the volume header size

    lnk_drivetype = struct.unpack("<L", lnk_file_data[
                                        82 + has_lnk_id_list_size[0] + lnk_volumeidoffset[0]:lnk_volumeidoffset[
                                                                                                 0] + 86 +
                                                                                             has_lnk_id_list_size[
                                                                                                 0]])  # 4 bytes volume id offset
    # print("drive type= ",lnk_drivetype[0])   # prints the drive type

    if lnk_drivetype[0] == 0:
        after_header_list.append("The drive can not be determined")
    elif lnk_drivetype[0] == 1:
        after_header_list.append("No volume mounted")
    elif lnk_drivetype[0] == 2:
        after_header_list.append("Removable")
    elif lnk_drivetype[0] == 3:
        after_header_list.append("Fixed")
    elif lnk_drivetype[0] == 4:
        after_header_list.append("Network")
    elif lnk_drivetype[0] == 5:
        after_header_list.append("CD-ROM")
    else:
        after_header_list.append("RAM Disk")

    lnk_driveserialnumber = struct.unpack("<L", lnk_file_data[
                                                86 + has_lnk_id_list_size[0] + lnk_volumeidoffset[0]:lnk_volumeidoffset[
                                                                                                         0] + 90 +
                                                                                                     has_lnk_id_list_size[
                                                                                                         0]])  # 4 bytes volume id offset
    # print("Drive Serial No.: ",lnk_driveserialnumber[0])# prints the drive serial number

    lnk_volumelabeloffset = struct.unpack("<L", lnk_file_data[90 + has_lnk_id_list_size[0] + lnk_volumeidoffset[0]:
                                                              lnk_volumeidoffset[0] + 94 + has_lnk_id_list_size[
                                                                  0]])  # 4 bytes volume id offset
    # print("Volume label offset= ",lnk_volumelabeloffset[0])   # prints the drive volumelabel offset

    if lnk_volumelabeloffset[0] == 14:
        offset1 = lnk_volumeid_size[0] - (4 + 4 + 4 + 4 + 4)
    else:
        offset1 = lnk_volumeid_size[0] - (4 + 4 + 4 + 4)

    # volume id size - 20
    lnk_volumelabel = lnk_file_data[lnk_volumeidoffset[0] + 94 + has_lnk_id_list_size[0]:lnk_volumeidoffset[0] + 94 +
                                                                                         has_lnk_id_list_size[
                                                                                             0] + offset1]  # 4 bytes volume id offset
    Volume_Label = lnk_volumelabel.decode('ascii')
    after_header_list.append(Volume_Label)
    after_header_list.append(lnk_driveserialnumber[0])

    # <<<<<<<<<<<<<<<LocalBase Path>>>>>>>>>>>

    if lnk_info_flags[0] == 1:
        # print("LocalBasePathOffsetUnicode and CommonNetworkRelativeLinkOffsetUnicode are present.")
        size_of_localbasepath = lnk_info_size[0] - lnk_localbasepathoffset[0]

        lnk_localbasepath = lnk_file_data[
                            78 + has_lnk_id_list_size[0] + lnk_localbasepathoffset[0]:78 + has_lnk_id_list_size[0] +
                                                                                      lnk_localbasepathoffset[
                                                                                          0] + size_of_localbasepath]
        LocalBasePath = lnk_localbasepath.decode('euc-kr')
        # print("Local Base Path:", LocalBasePath)
        after_header_list.append(LocalBasePath)

    # <<<<<<<<<<<<<<<CommonNetworkRelativeLinkAndPathSuffix>>>>>>>>>>>

    if lnk_info_flags[0] == 3:
        size_of_localbasepath = lnk_commonnetworkrelativelinkoffset[0] - lnk_localbasepathoffset[0]
        lnk_localbasepath = lnk_file_data[
                            78 + has_lnk_id_list_size[0] + lnk_localbasepathoffset[0]:78 + has_lnk_id_list_size[0] +
                                                                                      lnk_localbasepathoffset[
                                                                                          0] + size_of_localbasepath]
        # print("LocalBasePath:", lnk_localbasepath.decode('ascii'))

        tempoffset = 78 + has_lnk_id_list_size[0] + lnk_commonnetworkrelativelinkoffset[0]

        lnk_commonnetworkrelativelink_size = struct.unpack("<L", lnk_file_data[
                                                                 tempoffset:tempoffset + 4])  # 4 bytes CommonNetworkRelativeLink Size
        # print("CommonNetworkRelativeLink Size = ",lnk_commonnetworkrelativelink_size[0])   # prints CommonNetworkRelativeLink Size

        lnk_commonnetworkrelativelink_flags = struct.unpack("<L", lnk_file_data[tempoffset + 4:tempoffset + 8])
        # print("CommonNetworkRelativeLink Flags = ",lnk_commonnetworkrelativelink_flags[0])

        lnk_commonnetworkrelativelink_netnameoffset = struct.unpack("<L", lnk_file_data[tempoffset + 8:tempoffset + 12])
        # print("CommonNetworkRelativeLink NetName Offset = ",lnk_commonnetworkrelativelink_netnameoffset[0])

        lnk_commonnetworkrelativelink_devicenameoffset = struct.unpack("<L",
                                                                       lnk_file_data[tempoffset + 12:tempoffset + 16])
        # print("CommonNetworkRelativeLink DeviceName Offset = ",lnk_commonnetworkrelativelink_devicenameoffset[0])

        lnk_commonnetworkrelativelink_networkprovidertype = struct.unpack("<L", lnk_file_data[
                                                                                tempoffset + 16:tempoffset + 20])
        # print("CommonNetworkRelativeLink (Network Provider Type:) = ",lnk_commonnetworkrelativelink_networkprovidertype[0])

        if lnk_commonnetworkrelativelink_netnameoffset[0] > 14:
            netname_size = lnk_commonnetworkrelativelink_size[0] - (20)
            lnk_commonnetworkrelativelink_netname = lnk_file_data[
                                                    tempoffset + lnk_commonnetworkrelativelink_netnameoffset[0]:
                                                    tempoffset + lnk_commonnetworkrelativelink_netnameoffset[
                                                        0] + netname_size]
            # print("CommonNetworkRelativeLink (Net Name): ",lnk_commonnetworkrelativelink_netname.decode('ascii'))

    # <<<<<<<<<<<<CommonPathSuffix>>>>>>>>>>

    commonpathsuffix_size = lnk_info_size[0] - lnk_commonpathsuffixoffset[0]
    lnk_commonpathsuffix = lnk_file_data[78 + lnk_commonpathsuffixoffset[0] + has_lnk_id_list_size[0]:
                                         78 + lnk_commonpathsuffixoffset[0] + has_lnk_id_list_size[
                                             0] + commonpathsuffix_size]  # 4 bytes volume id offset
    # print("Common Path Suffix:",lnk_commonpathsuffix.decode('ascii'))

    return after_header_list
def lnk_file_tracker_data(tracker_data):
    # This prints distributed link tracker properties data block is 96 bytes of size.
    # print("Distributed Link Tracker Properties:\n")

    lnk_tracker_size = struct.unpack("<L", tracker_data[0:4])
    # print("Tracker size: {} (integer: {})".format(hex(lnk_tracker_size[0]), lnk_tracker_size[0]))

    # This prints Machine identifier string ASCII string terminated by an end-of-string character Unused bytes are set to 0
    lnk_tracker_machine_identifier = struct.unpack("<2Q", tracker_data[16:32])
    #print("Machine ID: {}".format(convert_hex_to_ascii(hex(lnk_tracker_machine_identifier[0]))))

    # This prints  new volume identifier
    volume_identifier = tracker_data[32:48]
    lnk_volume_identifier = uuid.UUID(bytes_le=volume_identifier)
    #print("New Volume ID: {}".format(lnk_volume_identifier))

    # This prints GUID containing an NTFS new object identifier
    object_identifier = tracker_data[48:64]
    lnk_object_identifier = uuid.UUID(bytes_le=object_identifier)
    #print("New Object ID: {}".format(lnk_object_identifier))

    # This prints the Object ID (Timestamp)
    # reads in little endian form first 2 byte(higher order time) next 2 bytes (middle order time)
    # and next 4 bytes (lower order time). First bit of higher order time is 0. (version number)
    object_timestamp = struct.unpack("<Q", tracker_data[48:56])
    object_timestamp_value = convert_hex(hex(object_timestamp[0]))
    lnk_object_timestamp = FromFiletime(object_timestamp_value - 5748192000000000)
   # print("New Object ID (Timestamp): {}".format(lnk_object_timestamp))

    # This prints the Object ID (Sequence number )
    object_sequence = struct.unpack(">H", tracker_data[56:58])
    #print("New ObjectID (Seq. No): {}".format(object_sequence[0]))

    # This prints the MAC address of the primary newtork card in the computer system
    object_mac1 = struct.unpack(">L", tracker_data[58:62])
    object_mac2 = struct.unpack(">H", tracker_data[62:64])
    #print("New ObjectID (MAC): {}".format(convert_mac(hex(object_mac1[0]) + hex(object_mac2[0]))))

    # This prints Birth volume identifier
    birth_volume_identifier = tracker_data[64:80]
    lnk_birth_volume_identifier = uuid.UUID(bytes_le=birth_volume_identifier)
    #print("Birth Volume ID: {}".format(lnk_birth_volume_identifier))

    # This prints Birth volume identifier
    birth_object_identifier = tracker_data[80:96]
    lnk_birth_object_identifier = uuid.UUID(bytes_le=birth_object_identifier)
    # print("Birth Object ID: {}".format(lnk_birth_object_identifier))

    # This prints the Birth Object ID (Timestamp)
    birth_object_timestamp = struct.unpack("<Q", tracker_data[80:88])
    # print(hex(object_timestamp[0]))
    birth_object_timestamp_value = convert_hex(hex(birth_object_timestamp[0]))
    birth_lnk_object_timestamp = FromFiletime(birth_object_timestamp_value - 5748192000000000)
    # print("Birth Object ID (Timestamp): {}".format(birth_lnk_object_timestamp))

    # This prints the Birth Object ID (Sequence number )
    birth_object_sequence = struct.unpack(">H", tracker_data[88:90])
    # print("Birth Object ID (Seq. No): {}".format(birth_object_sequence[0]))

    # This prints the Birth MAC address of the primary newtork card in the computer system
    birth_object_mac1 = struct.unpack(">L", tracker_data[90:94])
    birth_object_mac2 = struct.unpack(">H", tracker_data[94:96])
    # print("Birth Object ID (MAC): {}".format(convert_mac(hex(birth_object_mac1[0]) + hex(birth_object_mac2[0]))))
def custom_lnk_parser(data, offset, lnk_writer):
    try:
        header_list = []  # empty List

        lnk_header_size = struct.unpack("<L", data[offset + 0:offset + 4])
        header_clsid = data[offset + 4:offset + 20]
        lnk_header_clsid = uuid.UUID(bytes_le=header_clsid)

        # These two lines will parse out the individual bits in the Link flags section
        lnk_header_flags = struct.unpack("<I", data[offset + 20:offset + 24])
        lnk_header_flags_bits = BitArray(hex(lnk_header_flags[0]))

        # These two lines will parse out the individual bits for the file attributes
        lnk_header_file_attrib = struct.unpack("<I", data[offset + 24:offset + 28])
        lnk_header_file_attrib_bits = BitArray(hex(lnk_header_file_attrib[0]))

        # Parse the creation time stamp
        header_creation_time = struct.unpack("<Q", data[offset + 28:offset + 36])
        lnk_header_creation_time = FromFiletime(header_creation_time[0])

        # Parse the access time stamp
        header_access_time = struct.unpack("<Q", data[offset + 36:offset + 44])
        lnk_header_access_time = FromFiletime(header_access_time[0])

        # Parse the write time stamp
        header_write_time = struct.unpack("<Q", data[offset + 44:offset + 52])
        lnk_header_write_time = FromFiletime(header_write_time[0])

        lnk_header_file_size = struct.unpack("<L", data[offset + 52:offset + 56])
        lnk_header_icon_indx = struct.unpack("<L", data[offset + 56:offset + 60])
        lnk_header_show_window = struct.unpack("<L", data[offset + 60:offset + 64])
        lnk_header_hot_key = struct.unpack("<2B", data[offset + 64:offset + 66])
        hot_key = lnk_hot_key_parse(lnk_header_hot_key)

        #print("\n\n<<<<<<<<<<<<<<Parsing Link Header Information>>>>>>>>>>>>>>>>")
        #print("Header CLSID: {}".format(lnk_header_clsid))
        #print("Flags:\n")
        lnk_flags(lnk_header_flags_bits.bin)
        #print("Attributes:\n")
        lnk_attrib(lnk_header_file_attrib_bits.bin)
        #print("Target Creation Time: {}".format(lnk_header_creation_time))
        #print("Target Access Time: {}".format(lnk_header_access_time))
        #print("Target Write Time: {}".format(lnk_header_write_time))
        #print("Target File Size: {}".format(lnk_header_file_size[0]))
        #print(lnk_header_icon_indx)
        header_list.append(lnk_header_write_time)
        header_list.append(lnk_header_access_time)
        header_list.append(lnk_header_creation_time)
        header_list.append(lnk_header_file_size[0])

        # return header_list

        # def custom_lnk_file_after_header(data, offset):

        after_header_list = []  # Empty List

        # Print if HasLinkTargetIDList is set then

        # Item ID Size

        has_lnk_id_list_size = struct.unpack("<H", data[offset + 76:offset + 78])  # has link target id list size

        lnk_info_size = struct.unpack("<H", data[
                                            offset + 76 + has_lnk_id_list_size[0]:offset + 76 + has_lnk_id_list_size[
                                                0] + 2])  # 2 bytes  termination string

        # <<<<<<<<<<<<<<<<<<<<<<< Link Information>>>>>>>>>>>>>>>>>>>
        lnk_info_size = struct.unpack("<L", data[
                                            offset + 78 + has_lnk_id_list_size[0]:offset + 82 + has_lnk_id_list_size[
                                                0]])  # 4 bytes Link ifomation size

        lnk_info_header_size = struct.unpack("<L", data[offset + 82 + has_lnk_id_list_size[0]:offset + 82 +
                                                                                              has_lnk_id_list_size[
                                                                                                  0] + 4])  # 4 bytes header size

        lnk_info_flags = struct.unpack("<L", data[
                                             offset + 86 + has_lnk_id_list_size[0]:offset + 86 + has_lnk_id_list_size[
                                                 0] + 4])  # 4 bytes link information flags

        # if lnk_info_flags[0] == 1:
        #     print("Flags: VolomeIDAndLocalBasePath")
        # if lnk_info_flags[0] == 3:
        #     print("Flags: VolomeIDAndLocalBasePath,CommonNetworkRelativeLinkAndPathSuffix")

        lnk_volumeidoffset = struct.unpack("<L", data[offset + 90 + has_lnk_id_list_size[0]:offset + 90 +
                                                                                            has_lnk_id_list_size[
                                                                                                0] + 4])  # 4 bytes volume id offset

        lnk_localbasepathoffset = struct.unpack("<L", data[offset + 94 + has_lnk_id_list_size[0]:offset + 94 +
                                                                                                 has_lnk_id_list_size[
                                                                                                     0] + 4])  # 4 bytes volume id offset

        lnk_commonnetworkrelativelinkoffset = struct.unpack("<L", data[
                                                                  offset + 98 + has_lnk_id_list_size[0]:offset + 102 +
                                                                                                        has_lnk_id_list_size[
                                                                                                            0]])  # 4 bytes volume id offset

        lnk_commonpathsuffixoffset = struct.unpack("<L", data[offset + 102 + has_lnk_id_list_size[0]:offset + 106 +
                                                                                                     has_lnk_id_list_size[
                                                                                                         0]])  # 4 bytes volume id offset

        # <<<<<<<<<<<<<<<<<<Volume Referenece>>>>>>>>>>>>>>

        lnk_volumeid_size = struct.unpack("<L", data[
                                                offset + 78 + has_lnk_id_list_size[0] + lnk_volumeidoffset[0]:offset +
                                                                                                              lnk_volumeidoffset[
                                                                                                                  0] + 82 +
                                                                                                              has_lnk_id_list_size[
                                                                                                                  0]])  # 4 bytes volume id off$

        lnk_drivetype = struct.unpack("<L", data[offset + 82 + has_lnk_id_list_size[0] + lnk_volumeidoffset[0]:offset +
                                                                                                               lnk_volumeidoffset[
                                                                                                                   0] + 86 +
                                                                                                               has_lnk_id_list_size[
                                                                                                                   0]])  # 4 bytes volume id offset

        if lnk_drivetype[0] == 0:
            after_header_list.append("The drive can not be determined")
        elif lnk_drivetype[0] == 1:
            after_header_list.append("No volume mounted")
        elif lnk_drivetype[0] == 2:
            after_header_list.append("Removable")
        elif lnk_drivetype[0] == 3:
            after_header_list.append("Fixed")
        elif lnk_drivetype[0] == 4:
            after_header_list.append("Network")
        elif lnk_drivetype[0] == 5:
            after_header_list.append("CD-ROM")
        else:
            after_header_list.append("RAM Disk")

        lnk_driveserialnumber = struct.unpack("<L", data[offset + 86 + has_lnk_id_list_size[0] + lnk_volumeidoffset[
            0]:offset + lnk_volumeidoffset[0] + 90 + has_lnk_id_list_size[0]])  # 4 bytes volume id offset

        lnk_volumelabeloffset = struct.unpack("<L", data[offset + 90 + has_lnk_id_list_size[0] + lnk_volumeidoffset[
            0]:offset + lnk_volumeidoffset[0] + 94 + has_lnk_id_list_size[0]])  # 4 bytes volume id offset

        if lnk_volumelabeloffset[0] == 14:
            offset1 = lnk_volumeid_size[0] - (4 + 4 + 4 + 4 + 4)
        else:
            offset1 = lnk_volumeid_size[0] - (4 + 4 + 4 + 4)

        #    volume id size - 20
        lnk_volumelabel = data[
                          offset + lnk_volumeidoffset[0] + 94 + has_lnk_id_list_size[0]:offset + lnk_volumeidoffset[
                              0] + 94 + has_lnk_id_list_size[0] + offset1]  # 4 bytes volume id offset
        Volume_Label = lnk_volumelabel.decode('ascii')
        after_header_list.append(Volume_Label)
        after_header_list.append(lnk_driveserialnumber[0])

        # <<<<<<<<<<<<<<<LocalBase Path>>>>>>>>>>>

        if lnk_info_flags[0] == 1:
            size_of_localbasepath = lnk_info_size[0] - lnk_localbasepathoffset[0]

            lnk_localbasepath = data[offset + 78 + has_lnk_id_list_size[0] + lnk_localbasepathoffset[0]:offset + 78 +
                                                                                                        has_lnk_id_list_size[
                                                                                                            0] +
                                                                                                        lnk_localbasepathoffset[
                                                                                                            0] + size_of_localbasepath]
            LocalBasePath = lnk_localbasepath.decode('euc-kr')
            #print("Local Base Path:", LocalBasePath)
            after_header_list.append(LocalBasePath)

        # <<<<<<<<<<<<<<<CommonNetworkRelativeLinkAndPathSuffix>>>>>>>>>>>

        if lnk_info_flags[0] == 3:
            size_of_localbasepath = lnk_commonnetworkrelativelinkoffset[0] - lnk_localbasepathoffset[0]
            lnk_localbasepath = data[offset + 78 + has_lnk_id_list_size[0] + lnk_localbasepathoffset[0]:offset + 78 +
                                                                                                        has_lnk_id_list_size[
                                                                                                            0] +
                                                                                                        lnk_localbasepathoffset[
                                                                                                            0] + size_of_localbasepath]

            tempoffset = 78 + has_lnk_id_list_size[0] + lnk_commonnetworkrelativelinkoffset[0]

            lnk_commonnetworkrelativelink_size = struct.unpack("<L", data[
                                                                     offset + tempoffset:offset + tempoffset + 4])  # 4 bytes CommonNetworkRelativeLink Size

            lnk_commonnetworkrelativelink_flags = struct.unpack("<L",
                                                                data[offset + tempoffset + 4:offset + tempoffset + 8])

            lnk_commonnetworkrelativelink_netnameoffset = struct.unpack("<L", data[
                                                                              offset + tempoffset + 8:offset + tempoffset + 12])

            lnk_commonnetworkrelativelink_devicenameoffset = struct.unpack("<L", data[
                                                                                 offset + tempoffset + 12:offset + tempoffset + 16])

            lnk_commonnetworkrelativelink_networkprovidertype = struct.unpack("<L", data[
                                                                                    offset + tempoffset + 16:offset + tempoffset + 20])

            if lnk_commonnetworkrelativelink_netnameoffset[0] > 14:
                netname_size = lnk_commonnetworkrelativelink_size[0] - (20)
                lnk_commonnetworkrelativelink_netname = data[offset + tempoffset +
                                                             lnk_commonnetworkrelativelink_netnameoffset[
                                                                 0]:offset + tempoffset +
                                                                    lnk_commonnetworkrelativelink_netnameoffset[
                                                                        0] + netname_size]

        # <<<<<<<<<<<<CommonPathSuffix>>>>>>>>>>

        commonpathsuffix_size = lnk_info_size[0] - lnk_commonpathsuffixoffset[0]
        lnk_commonpathsuffix = data[78 + lnk_commonpathsuffixoffset[0] + has_lnk_id_list_size[0]:
                                    78 + lnk_commonpathsuffixoffset[0] + has_lnk_id_list_size[
                                        0] + commonpathsuffix_size]  # 4 bytes volume id offset
        # return after_header_list
        print("Edit here")
        lnk_writer.writerow({'Modified': header_list[0], 'Accessed': header_list[1],
                             'Created': header_list[2], 'Drive Type': after_header_list[0],
                             'Volume Name': after_header_list[1], 'Serial No.': hex(after_header_list[2]),
                             'File Size': header_list[3], 'LocalBasePath': after_header_list[3]})

    except:
        pass
def lnk_to_csv():
    try:
        os.makedirs('auto')
        os.makedirs('lnk_csv')
        print("DONE")
    except:
        pass
    conn = pymysql.connect(host='localhost', user='root', password='root', db='study_db', charset='utf8')
    curs = conn.cursor()
    sql_lnk = "insert into jumplist (ID,Modified,Accessed,Created,Drive_Type,Volume_Name,VSN,File_Size,Local_Base_Path) values ( %s, %s, %s, %s,%s, %s, %s, %s, %s)"
    jump_list = os.listdir(output_path)
    for jump_file in jump_list:
        try:
            assert olefile.isOleFile(output_path+jump_file)
            #print(jump_file+" has lnk")
            base = os.path.basename(jump_file)
            base = os.path.splitext(base)[0]# Get the JumpList file name
            ole = olefile.OleFileIO(output_path+jump_file)
            ole_list = ole.listdir(streams=True,storages=False)
            ole_list = list(ole_list)
            if len(ole_list) == 0:
                #print("None")
                pass
            elif ole_list[0][0] == 'DestList':
                #print("DestList")
                pass
            else:
                #print(base+' '+str(ole_list))
                lnk_csv = csv_output_path+base+'_jumplist'+'.csv'
                csvfilename = open(lnk_csv, 'w')
                field_names = ['ID', 'E.No.', 'Modified', 'Accessed',
                               'Created', 'Drive Type', 'Volume Name', 'Serial No.', 'File Size',
                               'LocalBasePath']
                lnk_writer = csv.DictWriter(csvfilename, delimiter=',', lineterminator='\n',
                                            fieldnames=field_names)

            try:
                for item in ole.listdir():
                    # lnk_writer.writeheader()
                    date_list = [0, 1, 2]
                    time_list = []
                    file = ole.openstream(item)
                    file_data = file.read()
                    header_value = file_data[:4]  # first four bytes value should be 76 bytes
                    try:
                        if header_value[0] == 76:  # first four bytes value should be 76 bytes
                            lnk_header = lnk_file_header(file_data[:76])
                            lnk_after_header = lnk_file_after_header(file_data)  # after 76 bytes to last 100 bytes
                            lnk_writer.writerow({'ID':base ,
                                                 'Modified': lnk_header[0], 'Accessed': lnk_header[1],
                                                 'Created': lnk_header[2],'Drive Type': lnk_after_header[0],
                                                 'Volume Name': lnk_after_header[1],
                                                 'Serial No.': hex(lnk_after_header[2]),
                                                 'File Size': lnk_header[3], 'LocalBasePath': lnk_after_header[3].rstrip('\00')})


                            ID = base
                            Modified = lnk_header[0]
                            Accessed = lnk_header[1]
                            Created = lnk_header[2]
                            Drive_Type = lnk_after_header[0]
                            Volume_Name = lnk_after_header[1]
                            VSN = hex(lnk_after_header[2])
                            File_Size = lnk_header[3]
                            Local_Base_Path = lnk_after_header[3]
                            try:
                                curs.execute(sql_lnk, (
                                     ID, Modified, Accessed, Created, Drive_Type, Volume_Name, VSN, File_Size,
                                    Local_Base_Path))
                            except:
                                print('error')
                            lnk_tracker_value = file_data[ole.get_size(item) - 100:ole.get_size(item) - 96]
                            if lnk_tracker_value[0] == 96:  # link tracker information 4 byte value = 96
                                try:
                                    print("We run here")
                                    lnk_tracker = lnk_file_tracker_data(
                                        file_data[ole.get_size(item) - 100:])  # last 100 bytes

                                except:
                                    pass
                            # file_size = float(os.path.getsize(lnk_csv))
                            # if file_size:
                            #     print(lnk_csv + ' is ' ,str(file_size))
                        else:  # if first four byte value is not 76 then it is DestList stream
                            pass
                    except:
                        pass
            except:
                print("Can not create csv file")

        except:
            print(jump_file+" doesn't have lnk")
    conn.commit()
    conn.close()
    csvfilename.close()
def csv_to_db():
    conn = pymysql.connect(host='localhost', user='root', password='root', db='study_db', charset='utf8')
    curs = conn.cursor()
    sql_lnk = "insert into jumplist (E_No,ID,Modified,Accessed,Created,Drive_Type,Volume_Name,VSN,File_Size,Local_Base_Path) values (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s)"
    lnk_list = os.listdir(csv_output_path)

    for lnk in lnk_list:
        lnk_csv = open(csv_output_path + lnk, 'r', encoding='utf-8')
        lnk_csv_reader = csv.reader(lnk_csv)
        # try:
        #     for line in lnk_csv_reader:
        #         print(line)
        # except:
        #     pass


        for line in lnk_csv_reader:
            date_list = [2, 3, 4]
            time_list = []
            for date in date_list:
                try:
                    time = datetime.strptime(line[date], '%Y-%m-%d_%H:%M:%S')
                    time.strftime('%Y-%m-%d %H:%M:%S')
                    time_list.append(time)
                except:
                    time = None
                    time_list.append(time)
            E_No = line[0]
            ID = line[1]
            Modified = time_list[0]
            Accessed = time_list[1]
            Created = time_list[2]
            Drive_Type = line[5]
            Volume_Name = line[6]
            VSN = line[7]
            File_Size = line[8]
            Local_Base_Path = line[9]
            curs.execute(sql_lnk, (
            E_No, ID, Modified, Accessed, Created, Drive_Type, Volume_Name, VSN, File_Size, Local_Base_Path))

    conn.commit()
    conn.close()
    lnk_csv.close()






if __name__ == "__main__":
    lnk_to_csv()
    #csv_to_db()
