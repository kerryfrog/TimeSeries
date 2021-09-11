# coding: utf-8

#FileProcess.h, FileProcess.cpp-> 갱수버전

import time
import math
import os
import Analysis
import Cluster
import GPS
import os.path

BUFSIZE = 1024

def CompareT(a):
	return a.GetTime()

class FileProcess:
	
	def __init__(self):
		self.gpslist = []
		self.date = 0
		self.startT = time.time()
		self.endT = time.time()
		self.collectedT = time.time()
		self.fileName = 'defualt'
		
	   
	#string name
	def SetFileName(self, name):
		self.fileName = name
	
	#int _date
	def SetFileDate(self, _date):
		self.date = _date
		
	def GetGPSlist(self):
		return self.gpslist
	
	def GetFileName(self):
		return self.fileName
	
	def GetFileDate(self):
		return self.date
	
	def GetNOfData(self):
		return len(self.gpslist)
	
	def GetStartTime(self):
		return self.startT
	
	def GetEndTime(self):
		return self.endT
	
	def GetCollectedTime(self):
		return self.collectedT
	
	#vector<string>& filelist
	def RawdataToKML(self, filelist):
		# bool rValue
		for iter_f in filelist:
			rValue = self.MakeKML(iter_f)
			
		return rValue
	
	def MakeKML(self, _f_name):

		timeT = time.time()
		
		s = 1
		d = 1
		cnt = 0
		for i in range(1, len(_f_name)):
			if _f_name[i] == "/":
				if cnt > 2:
					break
				if s == 1:
					s = i
				else:
					d = i

		dir_path = "." + _f_name[s:d]
		dir_name = _f_name[s + 1:d] + "_data"

		path = dir_path + "/" + dir_name
		os.makedirs(path, exist_ok = True)

		try:
			#f_name = _f_name.c_str();
			f_name = _f_name
			#f_in = open(f_name + 't', 'rt') ==>
			#f_in = open("/Users/omingeun/Downloads/temp/em" + f_name , 'rt')
			f_in = open("./" + f_name , 'rt')
			#start = _f_name.rfind("/")
			#output_fname = './kmldata' + _f_name[start:]
			output_fname = '/kmldata_' + _f_name[13:-3]#caution
			#f_name = output_fname.replace(".txt", ".kml") ==>
			#f_name = output_fname.replace(".json", ".kml")
			f_name = output_fname + "kml"#caution
			#f_name = f_name[19:]#caution
			#f_out = open(f_name, "wt")
			f_out = open(dir_path + '/' + dir_name + f_name, "wt")
			
			f_out.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
			f_out.write("<kml xmlns=\"http://www.opengis.net/kml/2.2\"  xmlns:gx=\"http://www.google.com/kml/ext/2.2\" xmlns:kml=\"http://www.opengis.net/kml/2.2\"  xmlns:atom=\"http://www.w3.org/2005/Atom\">\n")
			f_out.write("<Document>\n")
			f_out.write("<Style id=\"Style_1\">\n")
			f_out.write("<IconStyle>\n")
			f_out.write("<color>ffffffff</color>\n")
			f_out.write("<scale>0.8</scale>\n")
			f_out.write("<Icon>\n")
			f_out.write("<href>http://maps.google.com/mapfiles/kml/paddle/wht-circle.png</href>\n")
			f_out.write("</Icon>\n")
			f_out.write("<hotSpot x=\"32\" y=\"1\" xunits=\"pixels\" yunits=\"pixels\"/>\n")
			f_out.write("</IconStyle>\n</Style>\n")
			
			lines = f_in.readlines()
			for line in lines:
				temp = line.split()
				longitude = float(temp[4])
				latitude = float(temp[3])
				timeT = int(temp[2][:-3])
				f_out.write("<Placemark>\n<styleUrl>#Style_1</styleUrl>\n")
				f_out.write("\t<description>%ld</description>" % timeT)
				f_out.write("<Point>\n<coordinates>%.12f, %.12f,0</coordinates>\n</Point>\n" % (longitude, latitude))
				f_out.write("</Placemark>\n")
		   
			f_out.write("</Document>\n")
			f_out.write("</kml>\n")
			
		except:
			if (f_in is None):# or (f_out is None):
				print("fopen(rw) error in FileProcess::MakeKML()")
				return False
		finally:
			#f_in.close()
			#f_out.close()
			'''
			if (f_in.close() != 0) or (f_out.close() != 0):
				print("fclose error in FileProcess::MakeKML()!!")
				return False
			'''
			return True
		
		
		
		#with open(fout_name, "wt") as f_out:

	def MakeGPSlist(self, _f_name):
		count = 0

		timeT = time.time()
    
		f_name = str(_f_name)
  
		date_i = int(f_name[13:21])
		self.SetFileDate(date_i)
		
		try:
			f_in = open("./" + f_name, 'rt')

			lines = f_in.readlines()
			for line in lines:
				temp = line.split()
				longitude = float(temp[4])
				latitude = float(temp[3])
				timeT = int(temp[2][:-3])
				
				##########test code#########
				#print(longitude, latitude, timeT)
				#print(date_i)
				##########test code#########
				
				if count == 0:
					self.startT = timeT
				count += 1
				#/////certification code/////
				obj = time.localtime(timeT)
				trash = obj.tm_year * 10000
				trash += obj.tm_mon * 100
				trash += obj.tm_mday
				
				##########test code#########
				#int("n : ", n)
				#n += 1
				#print("gps date : ", trash)
				#print("file name date : ", date_i)
				#if trash != date_i:
				#	print("-----not match-----")
				##########test code#########
				
				if trash != date_i:
					trash += 1

				temp2 = GPS.GPS(latitude, longitude, timeT)
				self.gpslist.append(temp2)
				
			self.endT = timeT
		except:
			if f_in is None:
				print("fopen(rt) error in FileProcess::MakeGPSlist()")
				return True
		finally:
			#f_in.close()
			'''
			if f_in.close() != 0:
				print("flcose error in FileProcess::MakeGPSlist()")
				return False
			'''
			self.SortGPSlist()
			self.CalTotalCollectedTime()
			
			return True
		
	def SortGPSlist(self):
		self.gpslist.sort(key = CompareT)
		#for iter in self.gpslist:
		#	print("gpslist :", iter.GetTime())
		
	def DeleteGPSlist(self):
		self.gpslist.clear()

	def CalTotalCollectedTime(self):
		temp1 = temp2 = temp3 = time.time()
		temp3 = 0
		for iter_g in range(len(self.gpslist) - 1):
			temp1 = self.gpslist[iter_g].GetTime()
			temp2 = self.gpslist[iter_g + 1].GetTime()
			if Cluster.CheckSameDate(temp1, temp2) is True:
				if temp2 - temp1 < Cluster.THRESHOLD_T:
					temp3 += temp2 - temp1
		self.collectedT = temp3

	#vector<Cluster*> stay_state, int _mode
	def NumericalResultOfInitialization(self, stay_state, _mode):
		
		#merged analysis
		if _mode == 3:
			#out<<date;
			#_fileName = out.str() + "_" + fileName;
			_fileName = str(self.date) + "_" + self.fileName
		#analysis entire data
		elif _mode == 4:
			_fileName = self.fileName
			
		temp = "/results/initialization/" + _fileName + "_Init_Result.txt"
		#//const char* f_name = ("./results/initialization/" + _fileName + "_Init_Result.txt").c_str();
		#const char* f_name = temp.c_str();
		f_name = temp
		
		dir_path = "./" + _fileName[-3:]
		dir_name1 = "results"
		dir_name2 = "initialization"
		'''
		try :
			os.mkdir(dir_path + "/" + dir_name1 + "/", mode = 0o755)
			os.mkdir(dir_path + "/" + dir_name1 + "/" + dir_name2 + "/", mode = 0o755)
		except OSError as error:
			print(error)
		'''
	
		path = dir_path + "/" + dir_name1
		os.makedirs(path, exist_ok = True)

		path = dir_path + "/" + dir_name1 + "/" + dir_name2
		os.makedirs(path, exist_ok = True)

		try:
			if len(self.gpslist) is 0:
				return True
			f_out = open(dir_path + f_name, "wt")

			f_out.write("Number of Data : %d Collected Time(hour) : %f\n" % (int(len(self.gpslist)), float(self.collectedT) / float(3600)) )
			f_out.write("--------------------------------------------------------------\n")
			f_out.write("--------------------------------------------------------------\n")
			for iter_s in stay_state:
				f_out.write("Cluster# %d\n" % iter_s.GetID() )
				f_out.write("Center : %.12f\t%.12f\n" % (iter_s.GetCenterLat(), iter_s.GetCenterLon()) )
				f_out.write("Max Distance : %f\n" % iter_s.GetMaxDistance() ) 
				f_out.write("Mean Distance : %f\n" % iter_s.GetMeanDistance() )
				f_out.write("Count : %d\n" % iter_s.GetMemberCount() )
				f_out.write("Stay time(hour) : %f\n" %  (float(iter_s.GetDuration()) / float(3600)) )
				f_out.write("TimeRatio : %f\n" % iter_s.GetTimeRatio() )
				f_out.write("--------------------------------------------------------------\n")
		except:
			if f_out is None:
				print("fopen(wt) error in FileProcess::NumericalResultOfInitialization()")
				return False
		finally:
			'''
			if f_out.close() != 0:
				print("fclose error in FileProcess::NumericalResultOfInitialization()")
				return False
			'''
			return True

	#vector<Cluster*> stay_state, int _mode
	def VisualResultOfInitialization(self, stay_state, _mode):
		
		#merged analysis
		if _mode == 3:
			#out<<date;
			#_fileName = out.str() + "_" + fileName;
			_fileName = str(self.date) + "_" + self.fileName
		#analysis entire data
		elif _mode == 4:
			_fileName = self.fileName

		temp = "/results/initialization/visual/" + _fileName + "_Init_VisualResult.kml"
		#//const char* f_name = ("./results/initialization/visual/" + _fileName + "_Init_VisualResult.kml").c_str();
		#const char* f_name = temp.c_str();
		f_name = temp
		
		dir_path = "./" + _fileName[-3:]
		dir_name = "/results/initialization/visual"
		'''
		try :
			os.mkdir(dir_path + dir_name + "/", mode = 0o755)
		except OSError as error:
			print(error)
		'''
		path = dir_path + dir_name
		os.makedirs(path, exist_ok = True)
		if len(stay_state) != 0:
			try:#caution --> a+ is right ?
				if os.path.isfile(dir_path + f_name):
					f_out = open(dir_path + f_name, "a+")
				else:
					f_out = open(dir_path + f_name, "a+")
					f_out.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
					f_out.write("<kml xmlns=\"http://www.opengis.net/kml/2.2\"  xmlns:gx=\"http://www.google.com/kml/ext/2.2\" xmlns:kml=\"http://www.opengis.net/kml/2.2\"  xmlns:atom=\"http://www.w3.org/2005/Atom\">\n")
					f_out.write("<Document>\n")
					f_out.write("<Style id=\"Style_1\">\n")
					f_out.write("<IconStyle>\n")
					f_out.write("<color>ffffffff</color>\n")
					f_out.write("<scale>0.8</scale>\n")
					f_out.write("<Icon>\n")
					f_out.write("<href>http://maps.google.com/mapfiles/kml/paddle/wht-circle.png</href>\n")
					f_out.write("</Icon>\n")
					f_out.write("<hotSpot x=\"32\" y=\"1\" xunits=\"pixels\" yunits=\"pixels\"/>\n")
					f_out.write("</IconStyle>\n</Style>\n")
					f_out.write("<Style id=\"redLineBluePoly\">\n")
					f_out.write("<LineStyle>\n<color>ff0000ff</color>\n</LineStyle>\n")
					f_out.write("<PolyStyle>\n<color>ffff0000</color>\n</PolyStyle>\n</Style>\n")
			
			#if len(stay_state) is 0:
				#return True
	
				for iter_c in stay_state:
					f_out.write("<styleUrl>#Style_1</styleUrl>\n")
					f_out.write("<Placemark>\n<name>Cluster #%d</name>\n<visibility>0</visibility>\n" % iter_c.GetID() )
					f_out.write("<Point>\n<coordinates>%.12f, %.12f,0</coordinates>\n</Point>\n" % (iter_c.GetCenterLon(), iter_c.GetCenterLat()) )
					f_out.write("</Placemark>\n")
			
				f_out.write("</Document>\n")
				f_out.write("</kml>\n")
			except:
				if f_out is None:
					print("fopen(wt) error in FileProcess::VisualResultOfInitialization()")
					return False
			finally:
				'''
				if f_out.close() != 0:
					print("fclose error in FileProcess::VisualResultOfInitialization()")
					return False
				'''
				return True

	#vector<Cluster*> stay_state, double** transitionMatrix, int _mode, time_t totalT
	def NumericalResultOfLocationClustering(self, stay_state, transitionMatrix, _mode, totalT):
	
		#merged analysis
		if _mode == 0: 
			#out<<"Integrated";
			#_fileName = out.str() + "_" + fileName;
			_fileName = "Integrated" + "_" + self.fileName
			self.collectedT = totalT
		#daily based analysis
		elif _mode == 3:
			#out<<date;
			#_fileName = out.str() + "_" + fileName;
			_fileName = str(self.date) + "_" + self.fileName
		#analysis entire data
		elif _mode == 4:
			_fileName = self.fileName


		#//////// add////////
		if _mode == 0:
			temp = "/results/integratedJSON/" + _fileName + "_Clustering_Result.json"
			#//const char* f_name = ("./results/clustering/" + _fileName + "_Clustering_Result.json").c_str();
			f_name = temp
		
			dir_path = "./" + _fileName[-3:]
			dir_name = "/results/integratedJSON"
			'''
			try :
				os.mkdir(dir_path + dir_name + "/", mode = 0o755)
			except OSError as error:
				print(error)
			'''

			path = dir_path + dir_name
			os.makedirs(path, exist_ok = True)
			
			try:
				f_out = open(dir_path + f_name, "wt")

				sum_of_time = 0.0
				sum_of_count = 0
				for iter_s in stay_state:
					sum_of_time += float(iter_s.GetDuration())
					sum_of_count += iter_s.GetMemberCount()
			
				#//fprintf(f_out, "Cluster# %d   Accuracy Value : %f\n", (*iter)->GetID(), (*iter)->GetAccuracyValue());
				f_out.write("[\n")
			
				for iter_s in stay_state:
					if iter_s != stay_state[0]:
						f_out.write(",\n")
					f_out.write("\t{\n")
					f_out.write("\t\t\"cluster\" : \"%d\",\n" % iter_s.GetID())
					f_out.write("\t\t\"author\" : \"%s\",\n" % dir_path[-3:])
					f_out.write("\t\t\"latitude\" : \"%.12f\",\n" % iter_s.GetCenterLat() )
					f_out.write("\t\t\"longitude\" : \"%.12f\",\n" % iter_s.GetCenterLon() )
					f_out.write("\t\t\"maxDistance\" : \"%f\",\n" % iter_s.GetMaxDistance() )
					f_out.write("\t\t\"meanDistance\" : \"%f\",\n" % iter_s.GetMeanDistance() )
					f_out.write("\t\t\"timeRatio\" : \"%f\",\n" % iter_s.GetTimeRatio() )
					f_out.write("\t\t\"hourSpent\" : \"%f\",\n" % float(iter_s.GetDuration() / float(3600)) )
					f_out.write("\t\t\"count\" : \"%d\",\n" % iter_s.GetMemberCount() )
					f_out.write("\t\t\"ROAVD\" : \"%.16f\",\n" % math.log10(float(sum_of_time / iter_s.GetDuration())) )
					f_out.write("\t\t\"ROAVF\" : \"%.16f\"\n" % math.log10(float(sum_of_count / iter_s.GetMemberCount())) )
					f_out.write("\t}")

				f_out.write("\n]")

				# make prefernece result
				f_name2 = "/results/preference/" + _fileName + "_Preference_Result.json"
				dir_name2 = "/results/preference"

				path2 = dir_path + dir_name2
				os.makedirs(path2, exist_ok = True)

				lats = []
				tempLats = []
				lons = []
				tempLons = []
				numOfLocs = []
				tempLocs = []
				LVFIA = []
				LVDIA = []
				times = []
				tempTime = []
				for iter_s in stay_state:
					if len(lats) == 0:
						LVFIA, LVDIA, lats, lons, numOfLocs, times = iter_s.LVFIAandLVDIA()
						tempLats = lats
						tempLons = lons
						tempLocs = numOfLocs
						tempTime = times
					else:
						LVFIA.clear()
						LVDIA.clear()
						tempLats.clear()
						tempLons.clear()
						tempLocs.clear()
						tempTime.clear()
						LVFIA, LVDIA, tempLats, tempLons, tempLocs, tempTime = iter_s.LVFIAandLVDIA()
						for i in range(len(tempLats)):
							isDup = False
							for j in range(len(lats)):
								if tempLats[i] == lats[j] and tempLons[i] == lons[j]:
									numOfLocs[j] += tempLocs[i]
									times[j] += tempTime[i]
									isDup = True
									break
							if isDup is False:
								lats.append(tempLats[i])
								lons.append(tempLons[i])
								numOfLocs.append(tempLocs[i])
								times.append(tempTime[i])

					tempMem = iter_s.GetMember()
					for m in tempMem:
						for i in range(len(tempLats)):
							if tempLats[i] == m.GetLatitude() and tempLons[i] == m.GetLongitude():
								m.SetLVFIA(LVFIA[i])
								m.SetCount(tempLocs[i])
								m.SetLVDIA(LVDIA[i])
								m.SetDuration(tempTime[i])
								m.SetUID(iter_s.GetID())
								break

				sumOfLocs = sum(numOfLocs)
				ROLVF = []
				for n in numOfLocs:
					ROLVF.append(math.log(sumOfLocs / n))

				sumOfTime = sum(times)
				ROLVD = []
				for t in times:
					if t == 0:
						t += 1
					ROLVD.append(math.log(sumOfTime / t))
				
				f_out2 = open(dir_path + f_name2, "wt")
				f_out2.write("[\n")

				for iter_s in stay_state:
					tempMem = iter_s.GetMember()
					for i in range(len(lats)):
						for m in tempMem:
							if lats[i] == m.GetLatitude() and lons[i] == m.GetLongitude():
								m.SetROLVF(ROLVF[i])
								m.SetROLVD(ROLVD[i])

					pointer = 0
					while True:
						if pointer != 0:
							f_out2.write(",\n")
						f_out2.write("\t{\n")
						f_out2.write("\t\t\"cluster\" : \"%d\",\n" % tempMem[pointer].GetUID())
						f_out2.write("\t\t\"latitude\" : \"%.16f\",\n" % tempMem[pointer].GetLatitude())
						f_out2.write("\t\t\"longitude\" : \"%.16f\",\n" % tempMem[pointer].GetLongitude())
						f_out2.write("\t\t\"count\" : \"%d\",\n" % tempMem[pointer].GetCount())
						f_out2.write("\t\t\"LVFIA\" : \"%.16f\",\n" % tempMem[pointer].GetLVFIA())
						f_out2.write("\t\t\"ROLVF\" : \"%.16f\",\n" % tempMem[pointer].GetROLVF())
						f_out2.write("\t\t\"hourSpent\" : \"%f\",\n" % tempMem[pointer].GetDuration())
						f_out2.write("\t\t\"LVDIA\" : \"%.16f\",\n" % tempMem[pointer].GetLVDIA())
						f_out2.write("\t\t\"ROLVD\" : \"%.16f\"\n" % tempMem[pointer].GetROLVD())
						f_out2.write("\t}")
						pointer += tempMem[pointer].GetCount()
						if pointer >= len(tempMem):
							break

					f_out2.write("\n]")



			except:
				'''
				if f_out is None:
					print("fopen(wt) error in FileProcess::NumericalResultOfLocationClustering")
					return False
				'''
		#//////// add////////
	
		#temp = "/results/clustering/" + _fileName + "_Clustering_Result.txt"
		temp = "/results/clustering/" + _fileName + "_Clustering_Result.json"
		#//const char* f_name = ("./results/clustering/" + _fileName + "_Clustering_Result.txt").c_str();
		f_name = temp
	
		dir_path = "./" + _fileName[-3:]
		dir_name = "/results/clustering"
		'''
		try :
			os.mkdir(dir_path + dir_name + "/", mode = 0o755)
		except OSError as error:
			print(error)
		'''
		path = dir_path + dir_name
		os.makedirs(path, exist_ok = True)

		try:
			if len(stay_state) != 0:
				f_out = open(dir_path + f_name, "wt")
				'''
			f_out.write("Number of Data : %d Collected Time(hour) : %f\n" % (int(len(self.gpslist)), float(self.collectedT) / float(3600)) )
			f_out.write("--------------------------------------------------------------\n")
			print(len(stay_state))
			for iter_s in stay_state:
				#//		fprintf(f_out,"Cluster# %d\n",(*iter)->GetID());
				f_out.write("Cluster# %d   Accuracy Value : %f\n" % (iter_s.GetID(), iter_s.GetAccuracyValue()) )
				f_out.write("Center : %.12f\t%.12f\n" % (iter_s.GetCenterLat(), iter_s.GetCenterLon()) )
				f_out.write("Stddev : %.12f\t%.12f\n" % (iter_s.GetStddevLat(), iter_s.GetStddevLon()) )
				f_out.write("Max Distance : %f\n" % iter_s.GetMaxDistance() )
				f_out.write("Mean Distance : %f\n" % iter_s.GetMeanDistance() )
				f_out.write("TimeRatio : %f\n" % iter_s.GetTimeRatio() )
				f_out.write("Count : %d\n" % iter_s.GetMemberCount() )
				f_out.write("Stay time(hour) : %f\n" % float(iter_s.GetDuration() / float(3600)) )
				if _mode != 0:
					f_out.write("TimedTrace :\n")
					for i in range(24):
						trace = stay_state[iter_s].GetTimedTrace()
						if trace[i].GetCount() != 0:
							f_out.write("%d~%d - Stay Prob.:%f\tMoving Prob.:%f\n" % (i, i + 1,  float(trace[i].GetStayStateCount()) / float(trace[i].GetCount()), float(trace[i].GetMovingStateCount()) / float(trace[i].GetCount())) )
							#//					fprintf(f_out, "%d ~ %d : %d (stay-%d:moving-%d)\n",i,i+1,trace[i].GetCount(), trace[i].GetStayStateCount(), trace[i].GetMovingStateCount());
				f_out.write("--------------------------------------------------------------\n")
			f_out.write("\n\nTransition Probability\n")
			f_out.write("--------------------------------------------------------------\n\n")
		
			size = len(size_state)
			for i in range(size):
				for j in range(size):
					if transitionMatrix[i][j] != 0.0:
						f_out.write("cluster #%d -> #%d : %.5f\n" % (i, j, transitionMatrix[i][j]) )
				f_out.write("--------------------------------------------------------------\n")
			f_out.write("\n\nMatrix formation\n")
			f_out.write("--------------------------------------------------------------\n\n")
			for i in range(size):
				for j in range(size):
					if transitionMatrix[i][j] != 0:
						f_out.write("%.5f   " % (transitionMatrix[i][j]))
					else:
						f_out.write("%7d   " % (int(transitionMatrix[i][j])) )
				f_out.write("\n\n")
				'''
				f_out.write("[\n")
				for iter_s in stay_state:
					#print("I am working.")
					if iter_s != stay_state[0]:
						f_out.write(",\n")
					f_out.write("{\n")
					f_out.write("\"cluster\" : \"%d\",\n" % iter_s.GetID() )
					f_out.write("\"author\" : \"%s\",\n" % dir_path[-3:])
					f_out.write("\"latitude\" : \"%.12f\",\n" % iter_s.GetCenterLat() )
					f_out.write("\"longitude\" : \"%.12f\",\n" % iter_s.GetCenterLon() )
					f_out.write("\"maxDistance\" : \"%f\",\n" % iter_s.GetMaxDistance() )
					f_out.write("\"meanDistance\" : \"%f\",\n" % iter_s.GetMeanDistance() )
					f_out.write("\"timeRatio\" : \"%f\",\n" % iter_s.GetTimeRatio() )
					f_out.write("\"hourSpent\" : \"%f\",\n" % float(iter_s.GetDuration() / float(3600)) )
					f_out.write("\"count\" : \"%d\"\n" % iter_s.GetMemberCount() )
					f_out.write("}")	
				f_out.write("\n]")
			
		except:
			if f_out is None:
				print("fopen(wt) error in FileProcess::NumericalResultOfLocationClustering")
				return False
		finally:
			'''
		if f_out.close() != 0:
				print("fclose error in FileProcess::NumericalResultOfLocationClustering()")
				return False
			'''

			return True

		
	#vector<Cluster*> stay_state, int _mode
	def VisualResultOfLocationClustering(self, stay_state, _mode):
	
		if _mode == 0:
			#out<<"Integrated";
			#_fileName = out.str() + "_" + fileName;
			_fileName = "Integrated" + "_" + self.fileName
		#daily based analysis
		elif _mode == 3:
			#out<<"date";
			#_fileName = out.str() + "_" + fileName;
			_fileName = str(self.date) + "_" + self.fileName
		#analysis entire data
		elif _mode == 4:
			_fileName = self.fileName
		
		temp = "/results/clustering/visual/" + _fileName + "_Clustering_VisualResult.kml"
		#//const char* f_name = ("./results/clustering/visual/" + _fileName + "_Clustering_VisualResult.kml").c_str();
		f_name = temp
	
		dir_path = "./" + _fileName[-3:]
		dir_name = "/results/clustering/visual"
		'''
		try :
			os.mkdir(dir_path + dir_name + "/", mode = 0o755)
		except OSError as error:
			print(error)
		'''
		path = dir_path + dir_name
		os.makedirs(path, exist_ok = True)

		if len(stay_state) != 0:
			try:
				f_out = open(dir_path + f_name, "wt")
		
				f_out.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
				f_out.write("<kml xmlns=\"http://www.opengis.net/kml/2.2\"  xmlns:gx=\"http://www.google.com/kml/ext/2.2\" xmlns:kml=\"http://www.opengis.net/kml/2.2\"  xmlns:atom=\"http://www.w3.org/2005/Atom\">\n")
				f_out.write("<Document>\n")
				f_out.write("<Style id=\"Style_1\">\n")
				f_out.write("<IconStyle>\n")
				f_out.write("<color>ffffffff</color>\n")
				f_out.write("<scale>0.8</scale>\n")
				f_out.write("<Icon>\n")
				f_out.write("<href>http://maps.google.com/mapfiles/kml/paddle/wht-circle.png</href>\n")
				f_out.write("</Icon>\n")
				f_out.write("<hotSpot x=\"32\" y=\"1\" xunits=\"pixels\" yunits=\"pixels\"/>\n")
				f_out.write("</IconStyle>\n</Style>\n")
				f_out.write("<Style id=\"redLineBluePoly\">\n")
				f_out.write("<LineStyle>\n<color>ff0000ff</color>\n</LineStyle>\n")
				f_out.write("<PolyStyle>\n<color>ffff0000</color>\n</PolyStyle>\n</Style>\n")
		
				for iter_c in range(len(stay_state)):
					f_out.write("<styleUrl>#Style_1</styleUrl>\n")
					f_out.write("<Placemark>\n<name>Cluster #%d</name>\n<visibility>0</visibility>\n" % (stay_state[iter_c].GetID()) )
					f_out.write("<Point>\n<coordinates>%.12f, %.12f,0</coordinates>\n</Point>\n" % (stay_state[iter_c].GetCenterLon(), stay_state[iter_c].GetCenterLat()) )
					f_out.write("</Placemark>\n")
					f_out.write("<styleUrl>#redLineBluePoly</styleUrl>\n")
					f_out.write("<Placemark>\n<name>Cluster# %d</name>\n" % (stay_state[iter_c].GetID()) )
					f_out.write("<visibility>0</visibility>\n<styleUrl>#transRedPoly</styleUrl>\n")
					f_out.write("<Polygon>\n<extrude>1</extrude>\n<altitudeMode>relativeToGround</altitudeMode>\n<outerBoundaryIs>\n<LinearRing>\n")
					f_out.write("<coordinates>\n")

					area = stay_state[iter_c].GetArea()
					for iter_g in range(len(area)):
						f_out.write("%.12f, %.12f, 0\n" %  (area[iter_g].GetLongitude(), area[iter_g].GetLatitude()) )
					f_out.write("</coordinates>\n</LinearRing>\n</outerBoundaryIs>\n</Polygon>\n</Placemark>\n")
					f_out.write("\n")
					f_out.write("\n")
					f_out.write("\n")
				f_out.write("</Document>\n")
				f_out.write("</kml>\n")
			except:
				if f_out is None:
					print("fopen(wt) error in FileProcess::VisualResultOfInitialization()")
					return False
			finally:
				'''
				if f_out.close() != 0:
					print("fclose error in Transformation::EM_VisualResult()")
					return False
				'''
				return True

	#Trace* trace, int size
	def ResultOfTotalTimedTrace(self, trace, size):
	
		#out<<"All";
		#_fileName = out.str() + "_" + fileName;
		_fileName = "All" + "_" + self.fileName
		dir_path = "./" + _fileName[-3:]

		f_name = "/results/clustering/" + _fileName + "_TimedTrace_Result.txt"
	
		try:
			f_out = open(dir_path + f_name, "wt")

			for i in range(24):
				f_out.write("---------------Time %d ~ %d---------------------\n" % (i, (i + 1)) )
				for j in range(size):
					if trace[i].data[j] != 0:
						f_out.write("#%d cluster : %d, %.3f\n" % (j, trace[i].data[j], float(trace[i].data[j]) / float(trace[i].GetCount())) )
				f_out.write("------------------------------------------------\n")
			
		except:
			if f_out is None:
				print("fopen(wt) error in FileProcess::ResultOfTotalTimedTrace()")
				return False
		finally:
			'''
			if f_out.close() != 0:
				print("fclose error in Transformation::ResultOfTotalTimedTrace()")
				return False
			'''
			return True

