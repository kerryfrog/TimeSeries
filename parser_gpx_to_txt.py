#!/usr/bin/env python
# coding: utf-8

# In[1]:

import gpxpy 
import gpxpy.gpx 
import time
import datetime
import os
import re


# In[39]:

# 에러나면 모듈 설치해주세요~~
# sportstracker 폴더 만들고 gpx 데이터 담아주세요
# rawdata 폴더와 list 폴더를 만들어주세요
# folder_name 자기이름으로 바꾸세요~~!


folder_name = "LDS"
result_dir = "rawdata/"
list_dir = "list/"
sports_path = "./Sports_Tracker"


file_list = os.listdir(sports_path)
print ("file_list: {}".format(file_list))

file_list_gpx = [file for file in file_list if file.endswith(".gpx")]
for file in file_list_gpx:
    file_name = file[:-4].replace("-","")
    print(file_name)


    with open("{0}list_{1}".format(list_dir, folder_name), 'a') as f2:
        data2 = "./{0}{1}/{2}_{3}.txt\n".format(result_dir, folder_name, file_name, folder_name)
        f2.write(data2)
    with open("{0}{1}/{2}_{3}.txt".format(result_dir,folder_name,file_name,folder_name), 'w') as f:
    
        gpx_file = open(sports_path+"/"+file, 'r', encoding='UTF8')

        gpx = gpxpy.parse(gpx_file)

        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    times = point.time
    #                 file_name = times.strftime("%Y") + times.strftime("%m") + times.strftime("%d") + "_" + folder_name
                    data = "{0}|{1}|{2}\t{3}\t{4}\t".format(times.strftime("%Y"),
                                                        times.strftime("%m"),
                                                        times.strftime("%d"),
                                                        times.strftime("%H:%M:%S")+"|00",
                                                        str(int(time.mktime(times.timetuple())))+"|00")
                    la = "{:.12f}".format(point.latitude)
                    lo = "{:.12f}".format(point.longitude)
                    # '{:.2f}'.format(round(12.123123, 2))

                    f.write(data+la+"\t"+lo+"\n")


                            #             ./rawdata/ljs/20130531_ljs.txt

        #             print('Point at ({0},{1}) -> {2}, time : {3}'.format(point.latitude, point.longitude, point.elevation, point.time) )
        #             print(point)
    #                 print(file_name)

        gpx_file.close()

