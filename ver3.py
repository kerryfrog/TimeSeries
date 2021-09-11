import tensorflow as tf
import numpy as np
import csv
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from haversine import haversine
from numba import jit

def clusterin(cluster_lat, cluster_lon, location_lat, location_lon, cluster_maxmean, cluster_number):
  cluster_center = (cluster_lat, cluster_lon)
  location = (location_lat, location_lon)
  # 클러스터에 있는지 아닌지 확인해 주는 함수 (클러스터의 중심과, 현재 위치와의 거리를 계산해서 cluster 의 크기로 지정한 maxmean인지 확인) 
  #클러스터에 포함된다면 몇번 클러스터인지 반환
  if haversine(cluster_center, location) < cluster_maxmean :
    return cluster_number
  else :
    return 0

# time slicing 
def slicing_count_arr(count_data):
  arr = np.zeros((len(count_data)-14, 15))
  for i in range(0, len(arr)):
    for j in range(0,15):
      arr[i][j] = count_data[i+j]
  return arr

cluster_ljs = np.zeros((100,5))

data = open('/home/TimeSeries/Integrated_ljs_Clustering_Result.txt')

'''
클러스터 데이터 형식 
Cluster# 0   Accuracy Value : 1.000000
Center : 37.550312136530	126.924508177261
Stddev : 0.000000000000	0.000000000000
Max Distance : 0.999837
Mean Distance : 0.100480
TimeRatio : 0.402190
Count : 161366
Stay time(hour) : 1386.613056

이런식으로 나열되어 있고  아래 
Transition Probability 로 전이 확률이 나옴 

'''

data_ljs = data.read().split()
j = 0 #클러스터 배열 개수 
k = 0 # 어떤 데이터를 선ㄴ택할지 
for i in data_ljs:
  if i == 'Transition':
    break
  elif i == 'Cluster#' :
    cluster_ljs[j][0] = int(data_ljs[k+1])+1
  elif i == 'Center' :
    cluster_ljs[j][1] = data_ljs[k+2]
    cluster_ljs[j][2] = data_ljs[k+3]
  elif i == 'Max' :
    cluster_ljs[j][3] = data_ljs[k+3]
    cluster_ljs[j][4] = float(data_ljs[k+3])+float(data_ljs[k+7])
    j = j+1
    cluster_ljs.resize(j+1,5)
  k = k+1

cluster_ljs.resize(j,5)
print(len(cluster_ljs))
# cluster_ljs [클러스터 번호, center x , center y , Max_distance, Max_distance + Mean distance] 
print(cluster_ljs)


########### total cluster number
TCN = j-1

########### read the location data 
location_ljs = np.zeros((50,3))

'''
list에 들어갈 데이터  이런식으로 데이터가 있는 위치
C:/Users/idaso/Google Drive/PEM/timeseries/시계열 rawdata/rawdata/ljs/20130531_ljs.txt
C:/Users/idaso/Google Drive/PEM/timeseries/시계열 rawdata/rawdata/ljs/20130602_ljs.txt
C:/Users/idaso/Google Drive/PEM/timeseries/시계열 rawdata/rawdata/ljs/20130603_ljs.txt
'''

list = open('/home/TimeSeries/list_ljs')
list_ljs = list.read().split("\n")


# time 은 길이 10의 int

"""
trace_ljs에 들어가는 데이터 이렇게 생김 
2013|05|31	11:56:15|000	1369968975|000	37.504221666667	126.965225000000
2013|05|31	11:56:19|000	1369968979|000	37.504221666667	126.965225000000
2013|05|31	11:56:20|000	1369968980|000	37.504230000000	126.965196666667
2013|05|31	11:56:21|000	1369968981|000	37.504236666667	126.965206666667
2013|05|31	11:56:22|000	1369968982|000	37.504246666667	126.965220000000
2013|05|31	11:56:23|000	1369968983|000	37.504246666667	126.965220000000
2013|05|31	11:56:24|000	1369968984|000	37.504246666667	126.965220000000
2013|05|31	11:56:25|000	1369968985|000	37.504246666667	126.965220000000
2013|05|31	11:56:26|000	1369968986|000	37.504246666667	126.965220000000
2013|05|31	11:56:27|000	1369968987|000	37.504246666667	126.965220000000
2013|05|31	11:56:28|000	1369968988|000	37.504246666667	126.965220000000
2013|05|31	11:56:29|000	1369968989|000	37.504246666667	126.965220000000
2013|05|31	11:56:30|000	1369968990|000	37.504246666667	126.965220000000
"""
k = 0
for i in list_ljs:
    trace_ljs = open(i).read().split()
    for j in range(0,len(trace_ljs)-10):
        if j % 5 == 2:   
            location_ljs[k][0] = np.int(trace_ljs[j][0:10])
            location_ljs[k][1] = np.float(trace_ljs[j+1])
            location_ljs[k][2] = np.float(trace_ljs[j+2])
            k = k+1
            location_ljs.resize(k+1,3)

location_ljs.resize(k,3)
print(location_ljs[1][0])
print(location_ljs[1][1])
print(location_ljs[1][2])
#잘 저장된걸 볼 수 있다 


########### execute data collection time 
# 시간을 분으로 바꿔주는 작업인듯 , 기존 시간은 유닉스시간 
start_time = int(location_ljs[0][0])/60
end_time = int(location_ljs[k-1][0])/60
data_collection_time = end_time - start_time + 1  #단위 : 분

print(data_collection_time)


########### cluster in location data
CN = 1  ########cluster number
cluster_in_location_ljs = np.zeros((50,4))
j = 0


#print(cluster_in_location_ljs )

#location_ljs는 time, latitude, longitude가 차례로 있는 데이터 
# clusterin(cluster_lat, cluster_lon, location_lat, location_lon, cluster_maxmean, cluster_number)
#베열의 범위를 벗어나는듯함 , 배열을 두개로 나누어 주어야 할까 ?
#cluster_in_location_ljs[j][3] - > time 을 넣어준다 
# 속한 클러스터 , 시간, 위도, 경도 

for i in range(0,len(location_ljs)):
  if clusterin(cluster_ljs[CN][1], cluster_ljs[CN][2], location_ljs[i][1], location_ljs[i][2], cluster_ljs[CN][4], cluster_ljs[CN][0]) != 0 :
    cluster_in_location_ljs[j][0] = cluster_ljs[CN][0]  
    cluster_in_location_ljs[j][1] = location_ljs[i][1]
    cluster_in_location_ljs[j][2] = location_ljs[i][2]
    cluster_in_location_ljs[j][3] = location_ljs[i][0]
    j = j+1
    cluster_in_location_ljs.resize(j+1,4)
cluster_in_location_ljs.resize(j,4)


int_data_collection_time = int(data_collection_time)


count_arr = np.zeros(int_data_collection_time) # 데이터를 모아온 시간만큼 배열 크기 생성 (단위 분)

'''
testing code 
for i in range(0,20):
    print(cluster_in_location_ljs[i][3],start_time,(cluster_in_location_ljs[i][3])/60)
    print((cluster_in_location_ljs[i][3])/60 - start_time)
'''   
print(type(start_time))
print(start_time)
for i in range(0,len(cluster_in_location_ljs)):
    #print(cluster_in_location_ljs[i][3]/60)
    count_arr[int(cluster_in_location_ljs[i][3]/60 - start_time)] += 1

print(count_arr)

count = slicing_count_arr(count_arr)
print(count)

tmp = tf.reduce_sum(count, 1, keepdims = True)
print(tmp)

@tf.function
def func1(X):
    sum = tf.reduce_sum(X, 1, keepdims = True)
    div = X/sum
    return div

#세션을 실행

distribution = func1(count)
print(distribution)
distribution_ljs = np.nan_to_num(distribution)
print(distribution_ljs)
print(len(distribution_ljs))

result_ljs_chart = np.zeros((10080))

@tf.function
def func2(X_, Y_):
    X_mean = tf.reduce_mean(X_)
    Y_mean = tf.reduce_mean(Y_,1,keepdims = True)
    X_derivation = X_ - X_mean
    Y_derivation = Y_ - Y_mean
    X_2 = tf.pow(X_derivation,2)
    Y_2 = tf.pow(Y_derivation,2)
    X_dev = tf.reduce_sum(X_2)
    Y_dev = tf.reduce_sum(Y_2,1,keepdims = True)
    var_sqrt = tf.sqrt(X_dev * Y_dev)
    var = X_derivation * Y_derivation
    cov = tf.reduce_sum(var, 1, keepdims = True)
    corr = cov / var_sqrt
    return corr

fname = '/home/TimeSeries/result/result_ljs_test/list_ljs_test_result'
f = open(fname + '.csv', 'a+')
wr = csv.writer(f)

print(len(distribution_ljs))

for i in range(0, len(distribution_ljs)):
    print(i)
    fplot = fname+str(int(i/10080)) + '.png'
    if(i % 10080 == 0):
        wr.writerow(result_ljs_chart)
        plt.xlabel('time(min)')
        plt.ylabel('correlation coefficient')
        plt.savefig(fplot, format='png')
        plt.clf()
    
    result = func2(distribution_ljs[i],distribution_ljs)    
    mynan = np.isnan(result)
    my_result = result.numpy()
    
    for j in range(0, len(mynan)):
        if mynan[j]:
            my_result[j] = 0

    for j in range(i+1, i+10080):
        if my_result[j] >= 0.7 or my_result[j] <= -0.7:
            #print(i,j)
            result_ljs_chart[j-i] = result_ljs_chart[j-i] + 1
            plt.scatter(j-i, result[j], s = 0.1)


print(result_ljs_chart)


fplotname = '/home/TimeSeries/result/result_ljs_test/list_ljs_test_result/plot'
for i in range(0, len(distribution_ljs)) :
  fplot = fname + str(int(i/10080)) + '.png'
  if(i % 10080 == 0):
    wr.writerow(result_ljs_chart)
    plt.xlabel('time(min)')
    plt.ylabel('correlation coefficient')
    plt.savefig(fplot, format='png')
    plt.clf()