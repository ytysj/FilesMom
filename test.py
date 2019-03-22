
import time
import os
import shutil
import numpy.matlib
import numpy as np
input_path = "D:\\github\\FilesMom\\test2"#"D:\\github\\FilesMom\\test"


def TimeStampToTime(timestamp):     # 1479264792 to 2016-11-16 10:53:12
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)

def get_file_create_time(filePath):  # get file's create time
    t = os.path.getctime(filePath)
    return t
    #return TimeStampToTime(t)
    

def get_file_last_edit_time(filePath):   # get file's last edit time
    t = os.path.getmtime(filePath)
    return t
    #return TimeStampToTime(t)

def get_file_info(file_dir):
    file_list = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            tail_name = os.path.splitext(file)[1]
            file_path = os.path.join(root, file)
            tmp_file_dict = {}
            tmp_file_dict["Name"] = os.path.splitext(file)[0]
            tmp_file_dict["Extension"] = tail_name
            tmp_file_dict["File_path"] = file_path
            tmp_file_dict["CreateTime"] = get_file_create_time(file_path)
            tmp_file_dict["LastEditTime"] = get_file_last_edit_time(file_path)
            tmp_file_dict["IsSort"] = False
            tmp_file_dict["SortPath"] = ''
            file_list.append(tmp_file_dict)
            # print(file,tail_name)
            # if os.path.splitext(file)[1] == '.jpeg':
            #    L.append(os.path.join(root, file))
    return file_list

def decide_by_same_name(file_info1,file_info2):
    if file_info1['Name'] == file_info2['Name']:
        return True
    else:
        return False

def decide_by_simular_name(file_info1,file_info2):
    str1 = file_info1['Name']+file_info1["Extension"]
    str2 = file_info2['Name']+file_info2["Extension"]
    edit_dist = cmp_str_dist(str1, str2)
    str_diff_rate = 0.3
    if str_diff_rate*max(len(str1),len(str2)) < 1:
        min_dist = 1
    else:
        min_dist = str_diff_rate*max(len(str1),len(str2))

    if edit_dist <= min_dist:
        return True
    else:
        str1 = file_info1['Name']
        str2 = file_info2['Name']
        edit_dist = cmp_str_dist(str1, str2)
        str_diff_rate = 0.3
        if str_diff_rate*max(len(str1),len(str2)) < 1:
            min_dist = 1
        else:
            min_dist = str_diff_rate*max(len(str1),len(str2))

        if edit_dist <= min_dist:
            return True
        return False

def decide_by_simular_time(file_info1,file_info2):
    max_time_diff = 60*30   #30min

    # file_create_time1 = file_info1['CreateTime']
    # file_create_time2 = file_info2['CreateTime']
    # if abs(file_create_time1 - file_create_time2)<max_time_diff:
    #     return True
    
    file_last_time1 = file_info1['LastEditTime']
    file_last_time2 = file_info2['LastEditTime']
    if abs(file_last_time1 - file_last_time2)<max_time_diff:
        return True

    return False

def decide_simular(file_info1,file_info2):
    if decide_by_same_name(file_info1,file_info2):
        return True

    if decide_by_simular_name(file_info1,file_info2):
        return True

    if decide_by_simular_time(file_info1,file_info2):
        return True
    
    return False

def cmp_str_dist(str1, str2):  # compare str similarity
    len_1 = len(str1)
    len_2 = len(str2)
    matrix = np.matlib.zeros((len_1+1, len_2+1))
    # init the boundary
    for i in range(len_1+1):
        matrix[i, 0] = i
    for j in range(len_2+1):
        matrix[0, j] = j

    for i in range(1, len_1+1):  # matrix x asix
        for j in range(1, len_2+1):  # matrix y asix
            if str1[i-1] == str2[j-1]:  # equal
                matrix[i, j] = matrix[i - 1, j - 1]
            else:
                # get the min of upLeft,up,and left
                temp1 = min(matrix[i - 1, j], matrix[i, j - 1])
                temp_min = min(temp1, matrix[i - 1, j - 1])  # get min
                matrix[i, j] = temp_min + 1

    return matrix[len_1, len_2]  # return the str's edit distant

def sort_file_by_name(file_info):
    for i in range(len(file_info)):
        for j in range(i+1,len(file_info)):
            if file_info[j]['IsSort']:
                continue
            is_sim = decide_simular(file_info[i], file_info[j])
            if is_sim:
                #print("is_sim:",file_info[i]['CreateTime'],file_info[j]['CreateTime'],abs(file_info[i]['CreateTime'] - file_info[j]['CreateTime']))
                folder_path = os.path.join(input_path, "[F]"+file_info[i]['Name']) 
                if not os.path.exists(folder_path):
                    #print(folder_path)
                    os.makedirs(folder_path)

                if file_info[i]['IsSort']:
                    folder_path = file_info[i]['SortPath']
                else:
                    shutil.move(file_info[i]['File_path'],folder_path)
                    file_info[i]['IsSort'] = True 
                    file_info[i]['SortPath'] = folder_path

                if not file_info[j]['IsSort']:              
                    shutil.move(file_info[j]['File_path'],folder_path)
                    file_info[j]['IsSort'] = True
                    file_info[j]['SortPath'] = folder_path

if __name__ == "__main__":
    print('start')
    file_info_list = []
    file_info_list = get_file_info(input_path)
    sort_file_by_name(file_info_list)
    print('end')

