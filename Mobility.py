# coding: utf-8

# Mobility.h, Mobility.cpp

import GPS
import Cluster
import math
import time

class Mobility:
	def __init__(self, _ID):
		self.ID = _ID
		self.clusters = []
		self.gpslist = []
		self.mon = self.wDay = 0
		self.startT = self.endT = self.duration = time.time()
		self.nOfData = 0
		
	def show(self, how = 'all'):
		if how == 'all':
			print(self.ID, self.mon, self.wDay, self.startT, self.endT, 
				  self.duration, self.nOfData, self.clusters, self.gpslist)
		elif how == 'ID':
			print(self.ID)
		elif how == 'mon':
			print(self.mon)
		elif how == 'wDay':
			print(self.wDay)
		elif how == 'startT':
			print(self.startT)
		elif how == 'endT':
			print(self.endT)
		elif how == 'duration':
			print(self.duration)
		elif how == 'nOfData':
			print(self.nOfData)
		elif how == 'cluster':
			print(self.clusters[:])
		else:
			print(self.gpslist[:])
		
		
	def __del__(self):
		self.clusters.clear()
		self.gpslist.clear()
		
	def SetMon(self, _mon):
		self.mon = _mon
		
	def SetWDay(self, _wDay):
		self.wDay = _wDay
		
	def SetStartTime(self, _startT):
		self.startT = _startT
		
	def SetEndTime(self, _endT):
		self.endT = _endT
		
	def SetNOfData(self, _nOfData):
		self.nOfData = _nOfData
		
	def SetDuration(self, _duration):
		self.duration = _duration
		
	def SetMobility(self, gpslist, _stay_state):
		#tempMember = []
		for iter_c in _stay_state:
			tempCluster = Cluster.Cluster(iter_c.GetID())
			tempMember = iter_c.GetMember()
			
			for iter_g in tempMember:
				if iter_g.GetState() is True:
					tempGps = GPS.GPS(iter_g.GetLatitude(), iter_g.GetLongitude(), iter_g.GetTime(), iter_g.GetID())
					self.gpslist.append(tempGps)
					tempCluster.AddMember(tempGps)
					
			"""copy original timedtrace information to new mobility's cluster object"""
			trace = iter_c.GetTimedTrace()
			tempCluster.SetTimedTrace(trace)
				
			tempCluster.SetCenter(iter_c.GetCenterLat(), iter_c.GetCenterLon())
			tempCluster.SetMaxDistance(iter_c.GetMaxDistance())
			tempCluster.SetMeanDistance(iter_c.GetMeanDistance())
			tempCluster.SetDuration(iter_c.GetDuration())
			tempCluster.SetAccuracyValue(iter_c.GetAccuracyValue())
			self.clusters.append(tempCluster)
				
	def GetID(self):
		return self.ID
	
	def GetStartTime(self):
		return self.startT
	
	def GetEndTime(self):
		return self.endT
	
	def GetDuration(self):
		return self.duration
	
	def GetGPSlist(self):
		return self.gpslist
	
	def GetClusters(self):
		return self.clusters

