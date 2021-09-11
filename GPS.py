# coding: utf-8

#gps.h, gps.c++
import time
import math

PI = 3.14159265358979323846
R = 6371000

class GPS:
	#constructor & setter
	# 초기화시 3번째 인자 time은 time.time으로 넣어야됨 ,,
	#def __init__(self, _latitude, _longitude, _time=time.time(), _clusterID = -1, _state = False, _prob = 1):
	def __init__(self, _latitude, _longitude, _time = time.time(), _clusterID = -1, _state = False, _prob = 1):
		self.latitude = _latitude
		self.longitude = _longitude
		self.time = _time
		self.clusterID = _clusterID
		self.count = 0
		self.duration = 0
		self.UID = 0
		self.LVFIA = 0.0 #test
		self.ROLVF = 0.0 #test
		self.LVDIA = 0.0 #test
		self.ROLVD = 0.0 #test
		if self.clusterID != -1:
			self.state = True
		else:
			self.state = _state
		self.prob = _prob
		#self.data = list(range(self.size())) #?
		
	def show(self):
		print(self.latitude, self.longitude, self.time, self.clusterID, self.state, self.prob)
		
	def SetID(self, _clusterID):
		self.clusterID = _clusterID
		
	def SetProb(self, _prob):
		self.prob = _prob
	
	def SetState(self, _state):
		self.state = _state

	def SetCount(self, _count):
		self.count = _count

	def SetDuration(self, _duration):
		self.duration = _duration

	def SetUID(self, _UID):
		self.UID = _UID

	def SetLVFIA(self, _LVFIA):
		self.LVFIA = _LVFIA

	def SetROLVF(self, _ROLVF):
		self.ROLVF = _ROLVF

	def SetLVDIA(self, _LVDIA):
		self.LVDIA = _LVDIA

	def SetROLVD(self, _ROLVD):
		self.ROLVD = _ROLVD
		
	#getter
	def GetID(self):
		return self.clusterID
	
	def GetProb(self):
		return self.prob
	
	def GetState(self):
		return self.state
	
	def GetLatitude(self):
		return self.latitude
	
	def GetLongitude(self):
		return self.longitude

	def GetTime(self):
		return self.time

	def GetCount(self):
		return self.count

	def GetDuration(self):
		return self.duration

	def GetUID(self):
		return self.UID

	def GetLVFIA(self):
		return self.LVFIA

	def GetROLVF(self):
		return self.ROLVF

	def GetLVDIA(self):
		return self.LVDIA

	def GetROLVD(self):
		return self.ROLVD
	
	#function
	def ToUnitVector(self): 
		lat = self.latitude / 180 * PI
		lon = self.longitude / 180 * PI
		
		# z is north
		_x = math.cos(lon) * math.cos(lat)
		_y = math.sin(lon) * math.cos(lat)
		_z = math.sin(lat)
		
		return Vector(_x, _y, _z)
		
class Vector:
	# double x, y, z
	
	#constructor
	def __init__(self, _x = 0.0, _y = 0.0, _z = 0.0):
		self.x = _x
		self.y = _y
		self.z = _z
		
	def show(self):
		print(self.x, self.y, self.z)
	
	#getter
	def GetX(self):
		return self.x
	
	def GetY(self):
		return self.y
	
	def GetZ(self):
		return self.z
	
	#function
	def MagnitudeSquared(self):
		return (self.x * self.x) + (self.y * self.y) + (self.z * self.z)
	
	def Magnitude(self): 
		return math.sqrt(self.MagnitudeSquared())
	
	def ToUnit(self): 
		m = self.Magnitude()
		
		return Vector(self.x/m, self.y/m, self.z/m)
	
	def Cross(self, v): 
		_x = self.y * (v.GetZ()) - self.z * (v.GetY())
		_y = self.z * (v.GetX()) - self.x * (v.GetZ())
		_z = self.x * (v.GetY()) - self.y * (v.GetX())
		
		return Vector(_x, _y, _z)
	
	def Orthogonal(self):
		minNormal = abs(self.x)
		minIndex = 0
		
		if abs(self.y) < minNormal:
			minNormal = abs(self.y)
			minIndex = 1;
		
		if abs(self.z) < minNormal:
			minNormal = abs(self.z);
			minIndex = 2;
			
		if minIndex == 0:
			A = Vector(1,0,0)
		elif minIndex == 1:
			A = Vector(0,1,0)
		else:
			A = Vector(0,0,1)
		
		B =  self * minNormal
		
		return (A - B).ToUnit()	
	
	def ToGPS(self):
		unit = self.ToUnit()
		
		_z = unit.GetZ()
		
		if _z > 1:
			_z = 1
		
		lat = math.asin(_z)
		lon = math.atan2(unit.GetY(), unit.GetX())
		
		return GPS((lat*180/PI),(lon*180/PI))
	
	def __mul__(self, m):
		return Vector(m * self.x, m * self.y, m * self.z)
	
	def __add__(self, right):
		_x = self.x + right.GetX()
		_y = self.y + right.GetY()
		_z = self.z + right.GetZ()
		
		return Vector(_x, _y, _z)
	
	def __sub__(self, right):
		_x = self.x - right.GetX()
		_y = self.y - right.GetY()
		_z = self.z - right.GetZ()
		
		return Vector(_x, _y, _z)
