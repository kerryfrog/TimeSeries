#!/usr/bin/env python
# coding: utf-8

# In[154]:


"""

오직 하나의 클러스터군집에 in out 시간만을 뽑아내어 출력해 줍니다.
학교나 직장같은 곳의 클러스터를 선택하여 데이터를 뽑아내는데 사용합니다.

"""


# In[155]:


import json
import numpy as np
import pandas as pd
from haversine import haversine
import csv
import datetime


# In[156]:


def clusterin(cluster_lat, cluster_lon, location_lat, location_lon, cluster_max,cluster_number):
  cluster_center = (cluster_lat, cluster_lon)
  location = (location_lat, location_lon)
  # 클러스터에 있는지 아닌지 확인해 주는 함수 (클러스터의 중심과, 현재 위치와의 거리를 계산해서 cluster 의 크기로 지정한 maxmean인지 확인) 
  #클러스터에 포함된다면 몇번 클러스터인지 반환

    
  if haversine(cluster_center, location) < cluster_max:
    return int(cluster_number)
  else :
    return -1


# In[157]:


#Convert unixtime to datetime
def convert_datetime(unixtime):
    #date = pd.to_datetime(unixtime, unit ='s')
    #unixtime = unixtime +32400
    date = datetime.datetime.fromtimestamp(unixtime).strftime('%Y-%m-%d %H:%M:%S')
    return date # format : str


# In[158]:


################ 사용자 입력  #########################
user  = "ljs"


# 전처리가 필요한 cluster 번호 지정해 주세요 
total_list = [0]


################ 사용자 입력  #########################


### 여기는 필요시 수정하여 사용
list_dir = "./list/list_" + user  

json_dir = "./{0}/results/integratedJSON/Integrated_{1}_Clustering_Result.json".format(user,user)


# 만들어진 클러스터의 정보 가져오기 Integrated_이니셜_Clustering_Result.json의 경로를 적어줍니다.
with open(json_dir)as st_json:
    json_info = json.load(st_json)


# In[159]:


# 해당 클러스터의 정보 받아오기
cluster_count = len(total_list)

cluster_info = np.zeros((cluster_count, 4))
a=0
for clusters in json_info:
        if int(clusters["cluster"]) in total_list:
            cluster_info[a][0]= int(clusters["cluster"])
            cluster_info[a][1] = clusters["latitude"]
            cluster_info[a][2] = clusters["longitude"]
            cluster_info[a][3] = clusters["maxDistance"]
            a += 1
        else:
            continue
#print(cluster_info)


# In[160]:


# list에 기반하여 이용하여 위치 데이터 받아오기
list = open(list_dir)
list_line = list.read().split("\n")

#마지막 공백 삭제 
del list_line[-1]
#print(list_line)


# In[161]:


########### 위치 데이터 읽어오기 
location = np.zeros((50,3))

location_length = 0
for i in list_line:
    trace = open(i).read().split()
    for j in range(0,len(trace)-10):
        if j % 5 == 2:   
            #location[location_length][0] =int(trace[j][0:10]) + 32400  # 시간 보정 (SportsTracker로 수집한 시간은 한국 시간과 차이가 있음)
            location[location_length][0] =int(trace[j][0:10])  # 시간 보정 (SportsTracker로 수집한 시간은 한국 시간과 차이가 있음)
            location[location_length][1] = float(trace[j+1])
            location[location_length][2] = float(trace[j+2])
            location_length = location_length+1
            location.resize(location_length+1,3)

    # 당일 기록을 끝내서 클러스터 out 이 찍히지 않는 경우가 있기 때문에 
    # 당일 기록의 마지막을 표현 
    location[location_length][0] = int(0) # 시간
    location[location_length][1] = float(0.0)   #위도 
    location[location_length][2] = float(0.0)   #경도 


#print(location)


# In[162]:


time = []
cluster_inout =[]

before_cluster = -2
for i in range(location_length):
    # 어떤 클러스터에 속했는지 
    for j in range(cluster_count):
        if location[i][1] == 0.0 and location[i][2] == 0.0:
            now_cluster = -2  # 파일의 마지막인 경우 -2를 반환
            break
        now_cluster = clusterin(cluster_info[j][1],cluster_info[j][2], location[i][1],location[i][2], cluster_info[j][3],cluster_info[j][0])
        if now_cluster in total_list:
            break
    # 클러스터 정보에 따른 처리 
    #print(before_cluster,now_cluster)
    # 해당 위치가 클러스터에 속함
    if now_cluster in total_list:
        if before_cluster in total_list:
            #print("continue")
            continue
        else:
            #print("in")
            time.append(convert_datetime(location[i][0]))
            cluster_inout.append('in')
    # 해당 위치가 클러스터에 속하지 않음
    elif before_cluster in total_list:
        #print("out")
        time.append(convert_datetime(location[i][0]))
        cluster_inout.append('out')
    before_cluster = now_cluster 


# In[163]:


#클러스터 방문 정보를 pandas 형태로 변환 
cluster_visit = pd.DataFrame({
            
            "time":time,
            "in_out":cluster_inout
            
})
#print(len(cluster_visit))
#print(cluster_visit)


# In[164]:


#csv 파일로 작성
csv_name = "cluster_inout1_{0}.csv".format(user)
cluster_visit.to_csv(csv_name, index=False, encoding='cp949') 


# In[165]:


# 두번째 csv 파일 작성 
#실제 분석에 사용할 방법 


# In[166]:


# 기록된 날짜만 출력 
time_list = []
time_list2= []   # 몇번째부터 다음 날짜인지 
k =0 
for i in time:
    tmp = i[0:10]
    #print(tmp)
    if tmp in time_list:
        k = k + 1
        continue
    else:
        time_list.append(tmp)
        time_list2.append(k+1)
        k = 0

time_list2.append(k+1)
del time_list2[0]        
        
#time_list.append("3000-12-12")
#print(time_list)
#print(time_list2)


# In[167]:


k =0
tmp_in =""
tmp_out = ""

date =[]
time_in =[]
time_out = []

for i in range(len(time_list2)):
    for j in range(time_list2[i]):
        if cluster_inout[k] == "in" and tmp_in == "":
            tmp_in = time[k][10:]
        elif cluster_inout[k] == "out" and tmp_in != "":
            tmp_out = time[k][10:]
        k = k+1
    #print(tmp_in, tmp_out)    
    if tmp_in != "" and tmp_out !="":
        #print(time_list[i], tmp_in, tmp_out)
        date.append(time_list[i])
        time_in.append(tmp_in)
        time_out.append(tmp_out)
    tmp_in = ""
    tmp_out =""
#print(date)
#print(time_in)
#print(time_out)


# In[168]:


#클러스터 방문 정보를 pandas 형태로 변환 
cluster_visit2 = pd.DataFrame({
            
            "date":date,
            "in":time_in,
            "out":time_out
})
#print(len(cluster_visit))
#print(cluster_visit2)


# In[169]:


#csv 파일로 작성
csv_name = "cluster_inout2_{0}.csv".format(user)
cluster_visit2.to_csv(csv_name, index=False, encoding='cp949') 


# In[ ]:





# In[ ]:




