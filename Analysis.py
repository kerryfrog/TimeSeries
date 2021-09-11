# coding: utf-8

#SetTimeRatio
#Analysis.h, Anlaysis.cpp

import GPS
import Cluster
import Mobility
import time
import math

TERMINATIONCOND = 0.001
THRESHOLD_P = 0.13533528

def CompareT_c(a):
	return a.GetDuration()

def CompareT_g(a):
	return a.GetTime()

class Analysis:
	def __init__(self):
		self.nOfMobility = 0
		self.dailyMobility = []
		self.stay_state = []
		self.moving_state = []
		self.mergeList = []
		self.totalTrace = []
		self.collectedT = time.time()
		self.transitionMatrix = [[]]
		self.totalTrace = [Cluster.Trace() for i in range(24)]
		
		#self.dailyMobility.clear()
		#self.stay_state.clear()
		#self.moving_state.clear()
		#self.mergeList.clear()
		#self.transitionMatrix.clear()
		
	def GetClusters(self):
		return self.stay_state
	
	def GetMergeList(self):
		return self.mergeList
	
	def GetTransitionMatrix(self):
		return self.transitionMatrix
	
	def GetTotalDuration(self):
		return self.collectedT
	
	def GetTotalTimedTrace(self):
		return self.totalTrace
	
	#(time_t _collectedT)
	def SetCollectedTime(self, _collectedT):
		self.collectedT = _collectedT
	
	#int _ID, time_t _startT, time_t _endT, int _nOfData, int _duration
	def CreateMobility(self, _ID, _startT, _endT, _nOfData, _duration):
		temp = Mobility.Mobility(_ID)
		temp.SetStartTime(_startT)
		temp.SetEndTime(_endT)
		temp.SetNOfData(_nOfData)
		temp.SetDuration(_duration)
		self.dailyMobility.append(temp)
		
		return temp
	
	def AddMobility(self, mobility):#Mobility* mobility
		self.dailyMobility.append(mobility)
		
	def ResetAnalysis(self):
		size = len(self.stay_state)
		if size == 1:
			self.transitionMatrix.clear()
		elif size > 1:
			for i in range(size):
				self.transitionMatrix[i].clear()
			self.transitionMatrix.clear()
		
		for iter_c in self.stay_state:
			templist = iter_c.GetArea()
			for iter_g in templist:
				del iter_g
			del iter_c

		self.stay_state.clear()
		self.moving_state.clear()
	
	#vector<GPS*> gpslist, time_t _collectedT		
	def Initialization(self, gpslist, _collectedT):
		pos_c = 0	# pointer for stay_state
		state = True
		self.SetCollectedTime(_collectedT)
		
		for i in range(len(gpslist)):
			if i == (len(gpslist) - 1):		# last of gpslist
				if gpslist[i - 1].GetState() is True:
					gpslist[i].SetState(True)
					self.stay_state[pos_c].AddMember(gpslist[i])
				else:
					gpslist[i].SetState(False)
				break
			
			if state is True:		# stay state to stay state
				if Cluster.CalVelocity(gpslist[i], gpslist[i + 1]) < Cluster.THRESHOLD_V: 
					gpslist[i].SetState(True)
					pos_c = self.IdentifyCluster(gpslist[i])
					
					if pos_c == -1:#len(self.stay_state) ==0 -> create new cluster
						pos_c = len(self.stay_state)
						temp = Cluster.Cluster(pos_c)
						temp.AddMember(gpslist[i])
						self.stay_state.append(temp)
					else:
						self.stay_state[pos_c].AddMember(gpslist[i])
				else:#stay state to moving state
					gpslist[i].SetState(False)
					self.moving_state.append(gpslist[i])
					state = False
					
			else:
				if Cluster.CalVelocity(gpslist[i], gpslist[i + 1]) > Cluster.THRESHOLD_V:
					gpslist[i].SetState(False)
					self.moving_state.append(gpslist[i])
				else:#moving state to stay state
					#if not(self.CheckMovingState(gpslist, gpslist[i])):
					if self.CheckMovingState(gpslist, i) is False:
						i -= 1
						state = True
		
		self.ApplyInitAttributes()	
	
	#GPS* obj
	def IdentifyCluster(self, obj):
		index = 0
		
		if len(self.stay_state) == 0:
			return -1
		else:
			for iter_s in self.stay_state:
				if iter_s.CheckMember(obj):
					return index
				index += 1
				
		return -1
	
	
	#vector<GPS*> gpslist, vector<GPS*>::iterator &_iter
	def CheckMovingState(self, gpslist, _iter):#_iter?
		t = 0
		
		for i in range(_iter, len(gpslist)): #gpslist[i]  == iter
			if gpslist[i].GetTime() == gpslist[len(gpslist) - 1].GetTime(): #'''end of gpslist'''
				while True:
					if _iter == i:
						break
					gpslist[_iter].SetState(False)
					self.moving_state.append(gpslist[_iter])
					_iter += 1
				gpslist[_iter].SetState(False)
				self.moving_state.append(gpslist[_iter])
				return True		# moving state
			
			t = t + gpslist[i+1].GetTime() - gpslist[i].GetTime()
			
			if (t > Cluster.THRESHOLD_T):
				if Cluster.CalVelocity(gpslist[i], gpslist[i + 1]) < Cluster.THRESHOLD_V: #IN STAY STATE
					if Cluster.CalDistance(gpslist[i], gpslist[i + 1]) > Cluster.THRESHOLD_D:
						while True:
							if _iter == i:
								break
							gpslist[_iter].SetState(False)
							self.moving_state.append(gpslist[_iter])
							_iter += 1
						gpslist[_iter].SetState(False)
						self.moving_state.append(gpslist[_iter])
						return True
					else:
						return False
				else: # in moving state
					while True:
						if _iter == i:
							break
						gpslist[_iter].SetState(False)
						self.moving_state.append(gpslist[_iter])
						_iter += 1
					gpslist[_iter].SetState(False)
					self.moving_state.append(gpslist[_iter])
					return True
			
			if Cluster.CalVelocity(gpslist[i], gpslist[i + 1]) > Cluster.THRESHOLD_V:#moving
				while True:
					if _iter == i:
						break
					gpslist[_iter].SetState(False)
					self.moving_state.append(gpslist[_iter])
					_iter += 1
				gpslist[_iter].SetState(False)
				self.moving_state.append(gpslist[_iter])
				return True
	
		   
	def ErrorCorrection(self, gpslist):#오류남, test code
		for iter_c in self.stay_state:
			iter_c.CalMaxDistance()
			
		for iter_g in self.moving_state:
			for iter_c in self.stay_state:
				temp = GPS.GPS(iter_c.GetCenterLat(), iter_c.GetCenterLon())
				if (Cluster.CalDistance(iter_g, temp)) <= (iter_c.GetMaxDistance()):
					iter_g.SetState(True)
					iter_c.AddMember(iter_g)
					del temp
					break
	
	
	
	def ApplyInitAttributes(self):
		for iter_s in self.stay_state: #vector<Cluster*> stay_state
			iter_s.CalMaxDistance()
			iter_s.CalMeanDistance()
			iter_s.SortMember()
			iter_s.CalStayTime()
			iter_s.SetSeed(iter_s.GetMaxDistance() + iter_s.GetMeanDistance())
			try:
				iter_s.SetTimeRatio(float(iter_s.GetDuration()) / float(self.collectedT))
			except ZeroDivisionError:
				iter_s.SetTimeRatio(float(iter_s.GetDuration()) / Cluster.EPSILON )
			#print("TimeRatio :", iter_s.GetTimeRatio())
	
	
	#vector<GPS*> gpslist
	def ReadjustMovingState(self, gpslist):
		self.moving_state.clear()

		for iter_g in gpslist:
			if (iter_g.GetState()) is False:
				self.moving_state.append(iter_g)
			 
	
	def ReadjustStayState(self):
		#nOfInvalidCluster = 0
		index = 0
		idx = []
		
		for iter_c in self.stay_state:
			if iter_c.GetDuration() < Cluster.THRESHOLD_T:	#stay time is under THRESHOLD_T
				templist = iter_c.GetMember()
				for iter_g in templist:
					iter_g.SetState(False)
				iter_c.SetMemberClear()
				#nOfInvalidCluster += 1
			   
		#for _ in range(nOfInvalidCluster):
		for iter_c in range(len(self.stay_state)):
			if self.stay_state[iter_c].GetMemberCount() == 0:
				idx.append(iter_c)

		idx.sort(reverse = True)
		for i in idx:
			del self.stay_state[i]

		idx.clear()

		self.SortCluster()
		
		for iter_c in self.stay_state:
			iter_c.SetID(index)
			index += 1
			templist = iter_c.GetMember()
			
			for iter_g in templist:
				iter_g.SetID(iter_c.GetID())
	
	#vector<GPS*>  
	def LocationClustering(self, gpslist):
		runCount = 0
		
		#print("length of gpslist :", len(gpslist))
		#count = 0
		while True:
			for iter_g in gpslist:
				self.Expectation(iter_g)
				#count += 1
			#print(len(gpslist), "/", count)

			terminationCond_1 = self.CalTerminationCond()
			self.Maximization(gpslist)
			terminationCond_2 = self.CalTerminationCond()
			runCount += 1
			
			#print("condition :", abs(terminationCond_1 - terminationCond_2))
			if abs(terminationCond_1 - terminationCond_2) <= TERMINATIONCOND:
				break
			
		#print("run count : %d" % runCount)
  
	#GPS* obj 
	'''cluster '''
	def Expectation(self, obj):
		clusterID = -1
		prob = maxProb = 0.0
		
		for iter_s in self.stay_state:
			prob = self.CalWeight(obj, iter_s.GetID())
			if maxProb < prob:
				maxProb = prob
				#maxProb = prob
				clusterID = iter_s.GetID()
				
		obj.SetID(clusterID)
		obj.SetProb(maxProb)

	# vector<GPS*> gpslist
	def Maximization(self, gpslist):
		for iter_c in self.stay_state:
			iter_c.SetMemberClear()
			numer_Lat = numer_Lon = 0.0
			denorm = 0.0
			mean_Lat = mean_Lon = 0.0
			for iter_g in gpslist:
				if iter_c.GetID() == iter_g.GetID():
					iter_c.AddMember(iter_g)
					numer_Lat += (iter_g.GetProb() * iter_g.GetLatitude())
					numer_Lon += (iter_g.GetProb() * iter_g.GetLongitude())
					denorm += iter_g.GetProb()
			try:
				mean_Lat = numer_Lat / denorm
				mean_Lon = numer_Lon / denorm
			except ZeroDivisionError:
				mean_Lat = numer_Lat / Cluster.EPSILON			 # ??????
				mean_Lon = numer_Lon / Cluster.EPSILON
			
			if iter_c.GetMemberCount() != 0:
				numer_Lat = numer_Lon = 0.0
				stddev_Lat = stddev_Lon = 0.0
				denorm = 0.0
				templist = iter_c.GetMember()
				
				for iter_g in templist:
					numer_Lat += (iter_g.GetProb() * math.pow(iter_g.GetLatitude() - mean_Lat, 2))
					numer_Lon += (iter_g.GetProb() * math.pow(iter_g.GetLongitude() - mean_Lon, 2))
					denorm += iter_g.GetProb()
				try:	
					stddev_Lat = math.sqrt(numer_Lat / denorm)
					stddev_Lon = math.sqrt(numer_Lon / denorm)
				except ZeroDivisionError:
					stddev_Lat = math.sqrt(numer_Lat / Cluster.EPSILON)
					stddev_Lon = math.sqrt(numer_Lon / Cluster.EPSILON)
				iter_c.SetCenter(mean_Lat, mean_Lon)
				iter_c.SetCenterStddev(stddev_Lat, stddev_Lon)
				iter_c.CalMaxDistance()
				iter_c.CalMeanDistance()
				iter_c.SortMember()
				iter_c.CalStayTime()

				try:
					iter_c.SetTimeRatio(float(float(iter_c.GetDuration()) / float(self.collectedT)))
				except ZeroDivisionError:
					iter_c.SetTimeRatio(float(iter_c.GetDuration()) / Cluster.EPSILON)
				iter_c.SetSeed(iter_c.GetMaxDistance() + iter_c.GetMeanDistance())	

		self.ReadjustStayState()
	
		
	#double lamda, double distance
	def PDF(self, lamda, distance):
		exponent = (-1/lamda)*distance
		
		return math.exp(exponent)
	
						 
	# GPS* obj, int _ID
	def CalWeight(self, obj, _ID):
		numer = denorm = timeRatio = 0.0
		lamda = distance = 0.0
		
		for iter_s in self.stay_state:
			temp = GPS.GPS(iter_s.GetCenterLat(), iter_s.GetCenterLon())
			lamda = iter_s.GetSeed() #seed value for lamda
			timeRatio = iter_s.GetTimeRatio()
			distance = Cluster.CalDistance(temp, obj)

			
			####### test code #######
			if _ID == iter_s.GetID():
				numer = self.PDF(lamda, distance)
				if numer < THRESHOLD_P:
					numer = 0.0
			######## test code #######	
			

			denorm += self.PDF(lamda, distance)
			
			del temp
	
		if obj.GetState():
			#print('get state is T')
			try:
				return numer / denorm
			except ZeroDivisionError:
				return (numer / Cluster.EPSILON)
		else:
			try:
				return (numer / denorm) * timeRatio
			except ZeroDivisionError:
				return (numer / Cluster.EPSILON) * timeRatio
	
	
	def CalTerminationCond(self):
		rValue = 0.0
		
		for iter_s in self.stay_state:
			rValue += iter_s.GetMeanDistance()
			
		return rValue
	
	def SortCluster(self):
		self.stay_state.sort(key = CompareT_c, reverse = True)
		
	def MakeClusterArea(self):
		for iter_s in self.stay_state:
			center = GPS.GPS(iter_s.GetCenterLat(), iter_s.GetCenterLon())
			c = center.ToUnitVector()
			radius = float((iter_s.GetMaxDistance() + iter_s.GetMeanDistance())) * 1000		# km to m
			t = float(radius / GPS.R)
			k = c * math.cos(t)
			s = float(math.sin(t))
			u = k.Orthogonal()
			v1 = k.Cross(u)
			u = k.Cross(v1)
			
			for i in range(Cluster.AREACOUNT):
				a = float(2) * GPS.PI * float(i) / float(Cluster.AREACOUNT)
				temp1 = u * math.sin(a)
				temp2 = v1 * math.cos(a)
				temp3 = temp1 + temp2
				temp4 = temp3 * s
				p = k + temp4
				
				temp = GPS.GPS(p.ToGPS().GetLatitude(), p.ToGPS().GetLongitude())
				iter_s.AddAreaMember(temp)
				
	def CalClusteringAccuracy(self):
		
		for iter_s in self.stay_state:
			iter_s.CalAccuracyValue()
				
		
	def CalTransitionInterCluster(self, gpslist):

		tempT1 = tempT2 = time.time()

		size = len(self.stay_state)
		
		#self.transitionMatrix = [] # new double*[size]
		#tempMatrix = [] #new int*[size]
		#departureRatio = [] #new double[size]
		
		#matrix = [[0 for col in range(n)] for row in range(n)] 
		#0으로 초기화된 2차원 배열
		self.transitionMatrix = [[0.0 for _ in range(size)] for _ in range(size)]
		tempMatrix = [[0 for _ in range(size)] for _ in range(size)]
		departureRatio = [0.0 for _ in range(size)]
		
		id_1 = id_2 = -1
		#initialization of variable id_1
		for iter_g in gpslist:
			if iter_g.GetState():
				id_1 = iter_g.GetID()
				tempT1 = iter_g.GetTime()
				break
				
		#caculate departure ratio for markov chain
		for iter_c in self.stay_state:			
			departureRatio[iter_c.GetID()] = float(iter_c.GetDuration()) / float(60) 
		
		for iter_g in gpslist:
			if iter_g.GetState() and (iter_g.GetID() != -1):
				id_2 = iter_g.GetID()
				tempT2 = iter_g.GetTime()
				if id_1 != id_2:
					if int(tempT2 - tempT1) < Cluster.THRESHOLD_T2:
						tempMatrix[id_1][id_2] += 1
						############## index out of range
						#tempMatrix[id_1 - 1][id_2 - 1] += 1
					
				id_1 = id_2
				tempT1 = tempT2
			
		
		for i in range(size):
			totalTransition = 0
			priorP = transP = 0.0
			for j in range(size):
				totalTransition += tempMatrix[i][j]
				
			if totalTransition != 0:
				departureRatio[i] /= float(totalTransition)
				if departureRatio[i] < 1:
					departureRatio[i] = 1
					###### test code #####
					print("error departureRatio")
					###### test code #####
			
			else:
				continue
			
			
			for j in range(size):
				if tempMatrix[i][j] != 0:
					priorP = float(tempMatrix[i][j]) / float(totalTransition)
					transP = priorP * (1 / departureRatio[i])
					self.transitionMatrix[i][j] = transP
			
		for i in range(size):		
			tempMatrix[i].clear()
		tempMatrix.clear()
		departureRatio.clear()
   

	def SetTimedMobility(self):
		for iter_s in self.stay_state:
			iter_s.CalTimedMobility()
			
	
	def MergeMobility(self):
		self.collectedT = time.time()
		self.collectedT = 0

		for iter_m in self.dailyMobility:
			self.collectedT += iter_m.GetDuration() #type casting 필요? time_t ???
			self.Merge(iter_m.GetClusters(), iter_m.GetGPSlist())

		self.mergeList.sort(key = CompareT_g)
		self.ReadjustStayState()
		
		totalT = float(self.collectedT)
		for iter_c in self.stay_state:
			duration = float(iter_c.GetDuration())
			try:
				iter_c.SetTimeRatio(duration / totalT)
			except ZeroDivisionError:
				iter_c.SetTimeRatio(duration / Cluster.EPSILON)
	
	def Merge(self, c_list, g_list):
		
		tempDuration1 = tempDuration2 = time.time()
		if len(self.stay_state) == 0: #in first step
			for iter_c in c_list:
				#create new cluster
				tempCluster = Cluster.Cluster(iter_c.GetID())
				tempGPSlist = iter_c.GetMember()
				
				for iter_g in tempGPSlist:
					iter_g.SetID(len(self.stay_state))
					self.mergeList.append(iter_g)
					tempCluster.AddMember(iter_g)
					
				tempCluster.SetMaxDistance(iter_c.GetMaxDistance())
				tempCluster.SetMeanDistance(iter_c.GetMeanDistance())
				tempCluster.SetDuration(iter_c.GetDuration())
				tempCluster.SetAccuracyValue(iter_c.GetAccuracyValue())
				trace = iter_c.GetTimedTrace()
				tempCluster.SetTimedTrace(trace)
				self.stay_state.append(iter_c)
		else:
			
			for iter_c in self.stay_state:
				obj_1 = GPS.GPS(iter_c.GetCenterLat(), iter_c.GetCenterLon())
				_max = iter_c.GetMaxDistance()
				mean = iter_c.GetMeanDistance()
				area = _max + mean
				
				for iter_c_2 in c_list:
					if (iter_c_2.GetOverlapFlag()) is False:
						obj_2 = GPS.GPS(iter_c_2.GetCenterLat(), iter_c_2.GetCenterLon())

						if Cluster.CalDistance(obj_1, obj_2) < area:
							accV_1 = iter_c.GetAccuracyValue()
							accV_2 = iter_c_2.GetAccuracyValue()
							iter_c_2.SetOverlapFlag(True)
							
							if accV_1 < accV_2: #cluster in c_list is more accurate
								iter_c.SetAccuracyValue(iter_c_2.GetAccuracyValue())
								
							tempGPSlist = iter_c_2.GetMember()
							for iter_g in tempGPSlist:
								iter_g.SetID(iter_c.GetID())
								iter_c.AddMember(iter_g)
								self.mergeList.append(iter_g)
								
							iter_c.CalMaxDistance()
							iter_c.CalMeanDistance()

							tempDuration1 = time.time()
							tempDuration2 = time.time()
							tempDuration1 = iter_c.GetDuration()
							tempDuration2 = iter_c_2.GetDuration()
							
							iter_c.SetDuration(tempDuration1 + tempDuration2)
							trace = iter_c_2.GetTimedTrace()
							iter_c.MergeTimedTrace(trace)
				
			index = len(self.stay_state)
			for iter_c in c_list:
				if (iter_c.GetOverlapFlag()) is False:
					tempCluster = Cluster.Cluster(index)
					tempGPSlist = iter_c.GetMember()

					for iter_g in tempGPSlist:
						iter_g.SetID(index)
						self.mergeList.append(iter_g)
						tempCluster.AddMember(iter_g)
						
					tempCluster.SetMaxDistance(iter_c.GetMaxDistance())
					tempCluster.SetMeanDistance(iter_c.GetMeanDistance())
					tempCluster.SetAccuracyValue(iter_c.GetAccuracyValue())
					trace = iter_c.GetTimedTrace()
					tempCluster.SetTimedTrace(trace)
					tempCluster.SetDuration(iter_c.GetDuration())
					self.stay_state.append(tempCluster)
					index += 1
		'''
		if len(self.stay_state) == 0:
			for iter_c in c_list:
				temp_c = Cluster.Cluster(iter_c.GetID())
				temp_Glist = iter_c.GetMember()
				
				for iter_g in temp_Glist:
					self.mergeList.append(iter_g)
					temp_c.AddMember(iter_g)
				
				temp_c.CalMaxDistance()
				temp_c.CalMeanDistance()
				temp_c.SortMember()
				temp_c.CalStayTime()
				self.stay_state.append(temp_c)
				
		else:
			for iter_c in c_list:   
				obj1 = GPS.GPS(iter_c.GetCenterLat(), iter_c.GetCenterLon())
				for iter_c1 in self.stay_state:
					_max = iter_c1.GetMaxDistance()
					mean = iter_c1.GetMeanDistance()
					area = _max + mean
					obj2 = GPS.GPS(iter_c1.GetCenterLat(), iter_c1.GetCenterLon())
					if Cluster.CalDistance(obj1, obj2) < area:
						iter_c.SetOverlapFlag(True)
						temp_Glist = iter_c.GetMember()
						for iter_g in temp_Glist:
							iter_g.SetID(iter_c.GetID())
							self.mergeList.append(iter_g)
							iter_c1.AddMember(iter_g)
						iter_c1.CalMaxDistance()
						iter_c1.CalMeanDistance()
						iter_c1.SortMember()
						iter_c1.CalStayTime()
				del obj1
				del obj2
					
			index = len(self.stay_state)
			for iter_c in c_list:
				if iter_c.GetOverlapFlag() is False:
					temp_c = Cluster.Cluster(index)
					index += 1
					temp_Glist = iter_c.GetMember()
					for iter_g in temp_Glist:
						iter_g.SetID(index - 1)
						self.mergeList.append(iter_g)
						temp_c.AddMember(iter_g)
					temp_c.CalMaxDistance()
					temp_c.CalMeanDistance()
					temp_c.SortMember()
					temp_c.CalStayTime()
					self.stay_state.append(temp_c)
			print("index :", index)
		'''
	def SetTotalTrace(self):
		size = len(self.stay_state)
		
		for i in range(24):
			self.totalTrace[i].data = [0 for _ in range(size)]
				
		for iter_s in self.stay_state:
			trace = iter_s.GetTimedTrace()
			for i in range(24):
				self.totalTrace[i].AddCount(trace[i].GetCount())
				self.totalTrace[i].data[iter_s.GetID()] += trace[i].GetCount()
