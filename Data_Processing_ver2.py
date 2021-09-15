#!/usr/bin/env python
# coding: utf-8

# In[234]:


'''
원하는 클러스터 군집을 두개 골라서, 두 군집에 해당하는 클러스터의 in, out 데이터만을 뽑아내는 코드입니다.

실행 결과 두개의 csv 파일이 나오게 됩니다. 
첫번째 csv 파일은 두 클러스터 군집에 들어가고 나오는 정보를 모두 담아서 출력해 줍니다.

두번째 csv 파일은 하루에 두 클러스터에 모두 방문한 경우에만 출력을 해줍니다.
예를들어 집과 학교 부근의 클러스터들을 각각 클러스터 군집으로 설정한다면,
하루동안 집과 학교를 모두 방문한 날짜의 데이터만 골라서 출력을 하게 됩니다. 

'''


# In[217]:


import json
import numpy as np
import pandas as pd
from haversine import haversine
import csv
import datetime


# In[218]:


def clusterin(cluster_lat, cluster_lon, location_lat, location_lon, cluster_max,cluster_number):
  cluster_center = (cluster_lat, cluster_lon)
  location = (location_lat, location_lon)
  # 클러스터에 있는지 아닌지 확인해 주는 함수 (클러스터의 중심과, 현재 위치와의 거리를 계산해서 cluster 의 크기로 지정한 maxmean인지 확인) 
  #클러스터에 포함된다면 몇번 클러스터인지 반환

    
  if haversine(cluster_center, location) < cluster_max:
    return int(cluster_number)
  else :
    return -1


# In[219]:


#Convert unixtime to datetime
def convert_datetime(unixtime):
    #date = pd.to_datetime(unixtime, unit ='s')
    #unixtime = unixtime +32400
    date = datetime.datetime.fromtimestamp(unixtime).strftime('%Y-%m-%d %H:%M:%S')
    return date # format : str


# In[220]:



################ 사용자 입력  #########################
user  = "cdy"


# 전처리가 필요한 cluster 번호 지정해 주세요 
list1 = [1,23]
list2 = [0,3]

#두 클러스터의 이름을 입력해 주세요
cluster1_name = "집"

cluster2_name ="학교"

################ 사용자 입력  #########################

list_dir = "./list/list_" + user  

json_dir = "./{0}/results/integratedJSON/Integrated_{1}_Clustering_Result.json".format(user,user)




# 만들어진 클러스터의 정보 가져오기 Integrated_이니셜_Clustering_Result.json의 경로를 적어줍니다.
with open(json_dir)as st_json:
    json_info = json.load(st_json)


# In[221]:


total_list = list1 +list2
cluster_count = len(list1) + len(list2)

cluster_info = np.zeros((cluster_count, 4))
a=0
for clusters in json_info:
        if int(clusters["cluster"]) in list1 or int(clusters["cluster"]) in list2:
            cluster_info[a][0]= int(clusters["cluster"])
            cluster_info[a][1] = clusters["latitude"]
            cluster_info[a][2] = clusters["longitude"]
            cluster_info[a][3] = clusters["maxDistance"]
            a += 1
        else:
            continue
#print(cluster_info)


# In[222]:


# list를 이용하여 위치 데이터 받아오기
list = open(list_dir)
list_line = list.read().split("\n")

#마지막 공백 삭제 
del list_line[-1]
#print(list_line)


# In[223]:


########### 위치 데이터 읽어오기 
location = np.zeros((50,3))

location_length = 0
for i in list_line:
    trace = open(i).read().split()
    for j in range(0,len(trace)-10):
        if j % 5 == 2:   
            location[location_length][0] =int(trace[j][0:10]) + 32400  # 시간 보정 (SportsTracker로 수집한 시간은 한국 시간과 차이가 있음)
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


# In[224]:


time = []
cluster_name = []
cluster_inout =[]


before_cluster = -2
for i in range(location_length):
    # 해당 위치의 클러스터 정보 파악 
    for j in range(cluster_count):
        if location[i][1] == 0.0 and location[i][2] == 0.0:
            now_cluster = -2  # 파일의 마지막인 경우 -2를 반환
            break
        now_cluster = clusterin(cluster_info[j][1],cluster_info[j][2], location[i][1],location[i][2], cluster_info[j][3],cluster_info[j][0])
        if now_cluster in total_list:
            break
    # 클러스터 정보에 따른 처리
    #print(before_cluster ,now_cluster)
    if now_cluster in list1:
        if before_cluster in list1:         # 계속 첫번째 클러스터 군집에 있는 경우 
            continue
        
        elif before_cluster in list2:
            #print("cluster2 out")
            time.append(convert_datetime(location[i][0]))
            cluster_name.append(cluster2_name)
            cluster_inout.append('out')
            time.append(convert_datetime(location[i][0]))
            cluster_name.append(cluster1_name)
            cluster_inout.append('in')
        
        else:                              # 다른 클러스터에서 해당 클러스터로 처음 진입한 경우 
            #print("cluster1 in")
            time.append(convert_datetime(location[i][0]))
            cluster_name.append(cluster1_name)
            cluster_inout.append('in')
                
    elif now_cluster in list2:
        if before_cluster in list2:         # 계속  두번째 클러스터 군집에 있는 경우 
            continue
        elif before_cluster in list1:
            time.append(convert_datetime(location[i][0]))
            cluster_name.append(cluster1_name)
            cluster_inout.append('out')
            time.append(convert_datetime(location[i][0]))
            cluster_name.append(cluster2_name)
            cluster_inout.append('in')
        else:                              # 다른 클러스터에서 해당 클러스터로 처음 진입한 경우 
            #print("cluster2 in")
            time.append(convert_datetime(location[i][0]))
            cluster_name.append(cluster2_name)
            cluster_inout.append('in')
          
    elif now_cluster == -2:  # 파일이 종료된 경우 클러스터 out 을 표시해줌
        time.append(convert_datetime(location[i][0]))   
        if before_cluster in list1:
            #print("cluster1 out file_end")
            cluster_name.append(cluster1_name)
        elif before_cluster in list2:
            #print("cluster2 out file_end")
            cluster_name.append(cluster2_name)
        else:
            print('error')
        cluster_inout.append('out')
    
    
    else:                                  # 클러스터에서 나온경우 
        if before_cluster in total_list:
            time.append(convert_datetime(location[i][0]))
            if before_cluster in list1:
                #print("cluster1 out ")
                cluster_name.append(cluster1_name)
            elif before_cluster in list2:
                #print("cluster2 out ")
                cluster_name.append(cluster2_name)
            else:
                print('error')
            cluster_inout.append('out')
    
    before_cluster = now_cluster 



# In[225]:


#클러스터 방문 정보를 pandas 형태로 변환 
cluster_visit = pd.DataFrame({
            
            "time":time,
            "cluster":cluster_name,
            "in_out":cluster_inout
            
})
#print(len(cluster_visit))
#print(cluster_visit)


# In[226]:


# 기록된 날짜만 출력 
time_list = []
for i in time:
    tmp = i[0:10]
    if tmp in time_list:
        continue
    else:
        time_list.append(tmp)
#print(time_list)


# In[227]:


time2 = []

a,b = 0,0
k=0

for i in range(len(time)):
    now = time[i][0:10]
    print(time_list[k], now)
    if now == time_list[k]:
        if cluster_name[i] == cluster1_name:
             a = 1 
        elif cluster_name[i] == cluster2_name:
            b = 1
        
    else:
        if a ==1 and b ==1:
            time2.append(time_list[k])
        k = k+1
        a,b = 0,0 
        if cluster_name[i] == cluster1_name:
             a = 1 
        elif cluster_name[i] == cluster2_name:
            b = 1

if a ==1 and b ==1:
    time2.append(time_list[k])
       
        
#print(time2)


# In[233]:



cluster_visit2 = pd.DataFrame({
            
            "time":time,
            "cluster":cluster_name,
            "in_out":cluster_inout
            
})

#csv 파일로 작성
csv_name = "cluster_visit1_{0}.csv".format(user)
cluster_visit2.to_csv(csv_name, index=False, encoding='cp949') 


# In[228]:


time_meaning = []
cluster_name_meaning = []
cluster_inout_meaning = []
for i in range(len(time)):
    if time[i][0:10] in time2:
        time_meaning.append(time[i])
        cluster_name_meaning.append(cluster_name[i])
        cluster_inout_meaning.append(cluster_inout[i]) 


# In[229]:


#클러스터 방문 정보를 pandas 형태로 변환 
cluster_visit2 = pd.DataFrame({
            
            "time":time_meaning,
            "cluster":cluster_name_meaning,
            "in_out":cluster_inout_meaning
            
})
#print(cluster_visit2)


# In[230]:


#csv 파일로 작성
csv_name = "cluster_visit2_{0}.csv".format(user)
cluster_visit2.to_csv(csv_name, index=False, encoding='cp949') 


# In[ ]:





# In[ ]:





# In[ ]:




