
import time
import os
import shutil
import numpy.matlib 
import numpy as np
input_path = "D:\\github\\FilesMom\\test"

def TimeStampToTime(timestamp):     # 1479264792 to 2016-11-16 10:53:12
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)


def get_file_create_time(filePath):  # get file's create time
    t = os.path.getctime(filePath)
    # return TimeStampToTime(t)
    return t


def get_FileModifyTime(filePath):   # get file's last edit time
    t = os.path.getmtime(filePath)
    return TimeStampToTime(t)


def get_file_info(file_dir):
    file_list = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            tail_name = os.path.splitext(file)[1]
            file_path = os.path.join(root, file)
            tmp_file_dict = {}
            tmp_file_dict["Name"] = file
            tmp_file_dict["Extension"] = tail_name
            tmp_file_dict["file_path"] = file_path
            tmp_file_dict["CreateTime"] = get_file_create_time(file_path)
            tmp_file_dict["LastEditTime"] = tail_name
            file_list.append(tmp_file_dict)
            # print(file,tail_name)
            # if os.path.splitext(file)[1] == '.jpeg':
            #    L.append(os.path.join(root, file))
    return file_list

def decide_simular(str1,str2):
    len_1 = len(str1)
    len_2 = len(str2)
    
    edit_dist = cmp_str_dist(str1,str2)
    
    str_diff_rate = 0.3
    if str_diff_rate*len_1<1:
        min_dist = 1
    else:
        min_dist = str_diff_rate*len_1

    print("edit_dist:",edit_dist,min_dist)
    if edit_dist<=min_dist:
        return True
    else:
        return False

def cmp_str_dist(str1, str2):        #compare str similarity
    len_1 = len(str1)
    len_2 = len(str2)
    matrix = np.matlib.zeros((len_1+1, len_2+1))
    #init the boundary
    for i in range(len_1+1):
        matrix[i, 0] = i
    for j in range(len_2+1):
        matrix[0, j] = j

    for i in range(1, len_1+1):  #matrix x asix
        for j in range(1, len_2+1):  #matrix y asix
            if str1[i-1] == str2[j-1]:  #equal
                matrix[i, j] = matrix[i - 1, j - 1]
            else:
                #get the min of upLeft,up,and left
                temp1 = min(matrix[i - 1, j], matrix[i, j - 1])
                temp_min = min(temp1, matrix[i - 1, j - 1])  #get min
                matrix[i, j] = temp_min + 1

    return matrix[len_1, len_2]  #return the str's edit distant

if __name__ == "__main__":
    file_list = []
    #file_list = get_file_info(input_path)
    #print(file_list)
    str1='我知道你在的这意'
    str2='我知道你在看这玩意'
    a = decide_simular(str1,str2)
    print(a)


"""
import os
import shutil
lis=[]
i=1
destinationDir='C:\\Users\\Prasanth\\Desktop\\Desktop'
while os.path.exists(destinationDir):
    destinationDir=destinationDir+str(i)
    i+=1
os.makedirs(destinationDir)
lis=os.listdir('C:\\Users\\Prasanth\\Desktop')
print lis
for x in lis:
    if x==__file__:
        continue
    shutil.move(x, destinationDir)
"""
