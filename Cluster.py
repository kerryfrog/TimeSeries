# coding: utf-8

#Cluster,h, Cluster.cpp

import GPS
import time
import math

THRESHOLD_D = 1.0 #threshhold distance of cluster in initialization process
THRESHOLD_D2 = 0.001 #threshhold distance of cluster in initialization process
THRESHOLD_V = 10 #threshhold velocity of human beeing
THRESHOLD_T = 600 #threshhold time of staying in moving state
THRESHOLD_T2 = 86400 #threshold time of same date (1 day = 86400 seconds)
AREACOUNT = 36
EPSILON = 0.00000000001

def CompareC(a):  # a, b = GPS 객체
	return a.GetTime()

class Trace:   
	def __init__(self):
		self.nOFStay = 0
		self.nOFMoving = 0
		self.count = 0
		self.data = []
		
	def show(self):
		print(self.nOFStay, self.nOFMoving, self.count)
		
	def IncStayState(self):
		self.nOFStay += 1
		
	def IncMovingState(self):
		self.nOFMoving += 1
		
	def IncCount(self):
		self.count += 1
	
	def GetStayStateCount(self):
		return self.nOFStay
	
	def GetMovingStateCount(self):
		return self.nOFMoving
	
	def GetCount(self):
		return self.count
	
	def SetStayStateCount(self, _nOFStay):
		self.nOFStay = _nOFStay
		
	def SetMovingStateCount(self, _nOFMoving):
		self.nOFMoving = _nOFMoving
		
	def SetCount(self, _count):
		self.count = _count
		
	def AddStayStateCount(self, _add):
		self.nOFStay += _add
		
	def AddMovingStateCount(self, _add):
		self.nOFMoving += _add
		
	def AddCount(self, _add):
		self.count += _add

def haversine(obj1, obj2):
	lon1 = obj1.GetLongitude() * (GPS.PI / 180.0)
	lon2 = obj2.GetLongitude() * (GPS.PI / 180.0)
	lat1 = obj1.GetLatitude() * (GPS.PI / 180.0)
	lat2 = obj2.GetLatitude() * (GPS.PI / 180.0)

	dlon = lon2 - lon1
	dlat = lat2 - lat1

	a = math.sin(dlat / 2)**2 + (math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2)
	c = 2 * math.asin(math.sqrt(a))
	r = 6371

	return c * r

#GPS* obj1, GPS* obj2
def CalDistance(obj1, obj2):
	kEarthRadiusKms = 6376.5
	dLat1InRad = obj1.GetLatitude() * (GPS.PI/180.0)
	dLong1InRad = obj1.GetLongitude() * (GPS.PI/180.0)
	dLat2InRad = obj2.GetLatitude() * (GPS.PI/180.0)
	dLong2InRad = obj2.GetLongitude() * (GPS.PI/180.0)
		
	dLongitude = dLong2InRad - dLong1InRad
	dLatitude = dLat2InRad - dLat1InRad
		
	#Intermediate result a
	a = math.pow(math.sin(dLatitude/2.0), 2.0) + math.cos(dLat1InRad) * math.cos(dLat2InRad) * math.pow(math.sin(dLongitude/2.0), 2.0)
	#a = math.sin(dLatitude / 2)**2 + (math.cos(dLat1InRad) * math.cos(dLat2InRad) * math.sin(dLongitude / 2)**2)
	
	
	#Intermediate result c (great circle distance in Radians)
	c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
	#c = 2 * math.asin(math.sqrt(a))
		
	#Distance
	dDistance = kEarthRadiusKms * c
	#dDistance = c * 6731	

	return dDistance
	
#static double CalVelocity(GPS*, GPS*);		//km/h
def CalVelocity(obj1, obj2):
	distance = CalDistance(obj1, obj2)
	sec = int(obj2.GetTime() - obj1.GetTime())
		
	if sec == 0:
		velocity = 0
	else:
		velocity = (distance/float(sec))*float(3600)
						
	return velocity
						
def CheckSameDate(t1, t2):
	obj1 = time.localtime(t1)
	year1 = obj1.tm_year
	mon1 = obj1.tm_mon
	mday1 = obj1.tm_mday
						
	obj2 = time.localtime(t2)
	year2 = obj2.tm_year
	mon2 = obj2.tm_mon
	mday2 = obj2.tm_mday

	if year1 == year2:
		if mon1 == mon2:
			if mday1 == mday2:
				return True
						
	return False

class Cluster:  
	def __init__(self, _clusterID):
		self.clusterID = _clusterID
		self.duration = time.time()
		self.duration = 0
		self.timeRatio = 0
		self.centerLat = self.centerLon = 0.0
		self.stddevLat = self.stddevLon = 0.0
		self.maxDistance = self.meanDistance = 0.0
		self.seed = 0.0
		self.overlap = False
		self.member = []
		self.area = []
		#self.member.clear()
		#self.area.clear()
		self.accuracyValue = 0
		self.timedTrace = []
		temp = Trace()
		for _ in range(24):
			self.timedTrace.append(temp)
		
	def show(self):
		print(self.clusterID, self.duration, self.centerLat, self.centerLon,
			self.stddevLat, self.stddevLon, self.maxDistance, self.meanDistance,
			self.seed, self.overlap, self.member, self.area, self.accuracyValue,
			self.timedTrace)
		
		
	def AddMember(self, gps):
		self.member.append(gps)
		try:
			self.centerLat += ((gps.GetLatitude() - self.centerLat) / len(self.member))
			self.centerLon += ((gps.GetLongitude() - self.centerLon) / len(self.member))
		except:
			self.centerLat += ((gps.GetLatitude() - self.centerLat)/ EPSILON)
			self.centerLon += ((gps.GetLongitude() - self.centerLon)/ EPSILON)

	def AddAreaMember(self, gps):
		self.area.append(gps)
		
	def SetMaxDistance(self, _maxDistance):
		self.maxDistance = _maxDistance
		
	def SetMeanDistance(self, _meanDistance):
		self.meanDistance = _meanDistance
		
	def SetSeed(self, _seed):
		self.seed = _seed
		
	def SetDuration(self, _duration):
		self.duration = _duration
		
	def SetTimeRatio(self, _timeRatio):
		self.timeRatio = _timeRatio
		
	def SetCenter(self, _centerLat, _centerLon):
		self.centerLat = _centerLat
		self.centerLon = _centerLon
		
	def SetCenterStddev(self, _stddevLat, _stddevLon):
		self.stddevLat = _stddevLat
		self.stddevLon = _stddevLon
		
	def SetID(self, _clusterID):
		self.clusterID = _clusterID
		
	def SetMemberClear(self):
		self.member.clear()
		
	def SetOverlapFlag(self, _overlap):
		self.overlap = _overlap
		
	def SetAccuracyValue(self, _accuracyValue):
		self.accuracyValue = _accuracyValue
		
	def SetTimedTrace(self, trace):#Trace* trace
		count = 1;
		for i in range(24):
			self.timedTrace[i].SetCount(trace[i].GetCount())
			self.timedTrace[i].SetStayStateCount(trace[i].GetStayStateCount())
			self.timedTrace[i].SetMovingStateCount(trace[i].GetMovingStateCount())

	def MergeTimedTrace(self, trace):
		for i in range(24):
			self.timedTrace[i].AddStayStateCount(trace[i].GetStayStateCount())
			self.timedTrace[i].AddMovingStateCount(trace[i].GetMovingStateCount())
			self.timedTrace[i].AddCount(trace[i].GetCount())
			
	def GetID(self):
		return self.clusterID
	
	def GetMemberCount(self):
		return len(self.member)
	
	def GetDuration(self):
		return self.duration
	
	def GetCenterLat(self):
		return self.centerLat
	
	def GetCenterLon(self):
		return self.centerLon
	
	def GetStddevLat(self):
		return self.stddevLat
	
	def GetstddevLon(self):
		return self.stddevLon
	
	def GetMaxDistance(self):
		return self.maxDistance
	
	def GetMeanDistance(self):
		return self.meanDistance
	
	def GetTimeRatio(self):
		return self.timeRatio
	
	def GetSeed(self):
		return self.seed
	
	def GetOverlapFlag(self):
		return self.overlap
	
	def GetAccuracyValue(self):
		return self.accuracyValue
	
	def GetTimedTrace(self):
		return self.timedTrace
	
	def GetMember(self):
		return self.member
	
	def GetArea(self):
		return self.area
	'''	
	#GPS* obj1, GPS* obj2
	def CalDistance(self, obj1, obj2):
		kEarthRadiusKms = 6376.5
		dLat1InRad = obj1.GetLatitude() * (GPS.PI/180.0)
		dLong1InRad = obj1.GetLongitude() * (GPS.PI/180.0)
		dLat2InRad = obj2.GetLatitude() * (GPS.PI/180.0)
		dLong2InRad = obj2.GetLongitude() * (GPS.PI/180.0)
		
		dLongitude = dLong2InRad - dLong1InRad
		dLatitude = dLat2InRad - dLat1InRad
		
		#Intermediate result a
		a = math.pow(math.sin(dLatitude/2.0), 2.0) + math.cos(dLat1InRad) * math.cos(dLat2InRad) * math.pow(math.sin(dLongitude)/2.0, 2.0)
	
		#Intermediate result c (great circle distance in Radians)
		c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
		
		#Distance
		dDistance = kEarthRadiusKms * c
		return dDistance
	
	#static double CalVelocity(GPS*, GPS*);		//km/h
	def CalVelocity(self, obj1, obj2):
		distance = self.CalDistance(obj1, obj2)
		sec = int(obj2.GetTime() - obj1.GetTime())
		
		if sec == 0:
			velocity = 0
		else:
			velocity = (distance/float(sec))*float(3600)
						
		return velocity
						
	def CheckSameDate(self, t1, t2):
		obj1 = time.localtime(t1)
		year1 = obj1.tm_year
		mon1 = obj1.tm_mon
		mday1 = obj1.tm_mday
						
		obj2 = time.localtime(t2)
		year2 = obj2.tm_year
		mon2 = obj2.tm_mon
		mday2 = obj2.tm_mday
		
		if year1 == year2:
			if mon1 == mon2:
				if mday1 == mday2:
					return True
						
		return False
	'''	   
	def CalMaxDistance(self):
		temp = GPS.GPS(self.centerLat, self.centerLon)
		distance = _max = 0.0
						
		for iter_m in self.member:
			if iter_m.GetState() is True:
				distance = CalDistance(temp, iter_m)
				if distance < THRESHOLD_D:
					if distance > _max:
						_max = distance
						
		if _max == 0:
			self.maxDistance = THRESHOLD_D2
		else:
			self.maxDistance = _max
						
		del temp
						
	def CalMeanDistance(self):
		numer = denorm = 0.0
						
		for iter_m in self.member:
			temp = GPS.GPS(self.centerLat, self.centerLon)
			prob = iter_m.GetProb()
			if iter_m.GetState() is False:
				prob *= self.timeRatio
						
			numer = numer + (prob * CalDistance(temp, iter_m))
			denorm = denorm + prob
			
			del temp
		try:
			self.meanDistance = numer / denorm
		except ZeroDivisionError:
			self.meanDistance = number / EPSILON
		
	def CheckMember(self, obj):
		temp = GPS.GPS(self.centerLat, self.centerLon)
		distance = CalDistance(temp, obj)
		
		if distance > THRESHOLD_D:
			del temp
			return False
		else:
			del temp
			return True
		
	def SortMember(self): 
		self.member.sort(key = CompareC)
	
	def CalStayTime(self):
		temp1 = temp2 = temp3 = time.time()
		temp3 = 0;
		
		for i in range(len(self.member)-1):
			if CheckSameDate(self.member[i].GetTime(), self.member[i + 1].GetTime()):
				if self.member[i].GetState() is True:
					temp1 = self.member[i].GetTime()
					temp2 = self.member[i + 1].GetTime()
					if (temp2 - temp1) < THRESHOLD_T:
						temp3 += (temp2 - temp1)
	
		self.SetDuration(temp3)
		
	def CalAccuracyValue(self):
		totalProb = 0.0
		count = 0
		
		for iter_m in self.member:
			totalProb += iter_m.GetProb()
			count += 1
			
		try:
			self.accuracyValue = totalProb/float(count)
		except ZeroDivisionError:
			self.accuracyValue = totalProb
			# ?????????????
		
	def CalTimedMobility(self):
		timeTmp = time.time()

		for iter_m in self.member:
			timeTmp = iter_m.GetTime()
			tmTmp = time.localtime(timeTmp)
			hour = tmTmp.tm_hour
			
			if iter_m.GetState():
				self.timedTrace[hour].IncStayState()
			else:
				self.timedTrace[hour].IncMovingState()
			
			self.timedTrace[hour].IncCount()

	def LVFIAandLVDIA(self):
		lats = []
		lons = []
		size = 0
		times = []
		numOfLocs = []

		tempMem = self.GetMember()
		for i in range(len(tempMem)):
			isDup = False
			tempLat = tempMem[i].GetLatitude()
			tempLon = tempMem[i].GetLongitude()
			if i != len(tempMem) - 1:
				tempTime = abs(tempMem[i + 1].GetTime() - tempMem[i].GetTime())
			else:
				tempTime = 1

			if size == 0:
				lats.append(tempLat)
				lons.append(tempLon)
				times.append(tempTime)
				numOfLocs.append(1)
				size += 1
			else:
				for i in range(size):
					if lats[i] == tempLat and lons[i] == tempLon:
						numOfLocs[i] += 1
						times[i] += tempTime
						isDup = True
						break
				if isDup is False:
					lats.append(tempLat)
					lons.append(tempLon)
					times.append(tempTime)
					numOfLocs.append(1)
					size += 1

		sumOfTime = sum(times)
		sumOfLocs = sum(numOfLocs)
		#LVFIA = [0 for _ in range(size)]
		LVFIA = []
		for n in numOfLocs:
			LVFIA.append(float(n / sumOfLocs))

		#LVDIA = [0 for _ in range(size)]
		LVDIA = []
		for t in times:
			LVDIA.append(float(t / sumOfTime))

		return LVFIA, LVDIA, lats, lons, numOfLocs, times
