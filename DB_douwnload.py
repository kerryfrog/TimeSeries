import requests


data_adress = "데이터베이스 ip주소 입력 "

def getdata(adress,num,name):

    url='http://%s/mobility/getData?offset=0&limit=%d&name=%s' %(adress,num,name)
    res=requests.get(url)

    latitudeList=[]
    longitudeList=[]
    timeList=[]
    data2=res.json()

    data=data2['content']
    for i in range(len(data)):
        X,Y=data[i]['latitude'], data[i]['longitude']
        Z = data[i]['unixTime']
        lati=float(X)
        long=float(Y)
        time=int(Z[0:10])
        latitudeList.append(lati)
        longitudeList.append(long)
        timeList.append(time)
    return (latitudeList,longitudeList,timeList)



lat , lon ,time = getdata(data_adress,100,'omg')
print(lat , lon, time)


