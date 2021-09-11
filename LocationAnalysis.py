# coding: utf-8

#LocationAnalysis.h, LocationAnalysis.cpp

import FileProcess as FP
import Analysis as A

'''
class LocationAnalysis
{
	private:
		/////attributes/////
		int mode;
		char** parameter;
		string outputName;
		string option;
		vector<string> fileList;
		FileProcess fileProcessor;
		Analysis analysis;
	public:
		/////constructor/////
		LocationAnalysis(int, char**);
		///////setter/////
		void SetMode(int);
		void SetOutputName(string);
		void SetOption(string);
		void SetFileList(string);
		/////getter/////
		int GetMode();
		string GetOutputName();
		/////function/////
		void ShowUsage();
		void LoadList();
		bool ConvertRawToKML();
		bool DailyAnalysis();		//Daily based Location Analysis
		bool AnalysisEntireData();			//Location Analysis of entire data

};

#endif
'''

class LocationAnalysis:
	'''
	private:
	/////attributes/////
	int mode;
	char** parameter;
	string outputName;
	string option;
	vector<string> fileList;
	FileProcess fileProcessor;
	Analysis analysis;
	'''

	#int _argc, char** _argv
	def __init__(self, _argc, _argv):
		self.mode = 0
		self.parameter = _argv
		self.outputName = "default"
		self.option = "default"
		self.SetMode(_argc)
		self.fileList = []
		self.fileProcessor = FP.FileProcess()
		self.analysis = A.Analysis()

	#int _mode
	def SetMode(self, _mode):
		if _mode == 1:
			self.mode = 1
		elif _mode == 2:
			temp_option = self.parameter[1]
			self.SetOption(temp_option)
			if self.option == "-t":
				self.mode = 2
			else:
				self.mode = 0
		elif _mode == 3:
			temp_option = self.parameter[1]
			temp_outputName = self.parameter[2]
			self.SetOption(temp_option)
			self.SetOutputName(temp_outputName)
			if self.option == "-a":
				self.mode = 3
			elif self.option == "-fa":
				self.mode = 4
			else:
				self.mode = 0
		else:
			self.mode = 0

	#string _outputName
	def SetOutputName(self, _outputName):
		self.outputName = _outputName
	
	#string _option
	def SetOption(self, _option):
		self.option = _option
		
	#string _file
	def SetFileList(self, _file):
		self.fileList.append(_file)
		
	def GetMode(self):
		return self.mode
	
	def GetOutputName(self):
		return self.outputName
	
	def ShowUsage(self):
		print("Usage: locAnalysis <options> < <liststream>")
		print("where possible options include:")
		print("\t-t\t\t\t\t\tConverting rawdata to kmldata")
		print("\t-a <output name>\t\t\tDaily based Location Analysis")
		print("\t-fa <output name>\t\t\tLocation Analysis of entire data")
		
	def LoadList(self):
		'''
		while buf1:
			buf2 = buf1[:-1]
			tempName = buf2
			self.SetFileList(tempName)
			buf1 = input()
		'''
		try:
			while True:
				buf = input()
				buf = buf[1:-1]
				if buf[len(buf) - 1] == 'x':
					buf += 't'
				self.SetFileList(buf)
				#print(buf)
		except EOFError:
				pass
   
	def ConvertRawToKML(self):
		self.LoadList()
		if self.fileProcessor.RawdataToKML(self.fileList) is False:
			return False
		
		return True
	
	def DailyAnalysis(self):
		self.LoadList()
		self.fileProcessor.SetFileName(self.GetOutputName())
		
		#daily analysis
		for iter_l in self.fileList:
			if self.fileProcessor.MakeGPSlist(iter_l) is False:
				return False
			#add daily mobility
			currentMobility = self.analysis.CreateMobility(self.fileProcessor.GetFileDate(), self.fileProcessor.GetStartTime(), self.fileProcessor.GetEndTime(), self.fileProcessor.GetNOfData(), self.fileProcessor.GetCollectedTime())
			#initialization
			self.analysis.Initialization(self.fileProcessor.GetGPSlist(), currentMobility.GetDuration()) #mode 3(daily) or mode 4(fully)
			#file output of initilization results (numerical & visual)   mode = 3 (daily based analysis)
			if self.fileProcessor.NumericalResultOfInitialization(self.analysis.GetClusters(), self.mode) is False:
				print("NumericalResultOfInitialization fail")
				return False

			if self.fileProcessor.VisualResultOfInitialization(self.analysis.GetClusters(), self.mode) is False:
				print("VisualResultOfInitialization fail")
				return False
			#clustering process
			self.analysis.LocationClustering(self.fileProcessor.GetGPSlist())
			self.analysis.SetTimedMobility()
			self.analysis.CalTransitionInterCluster(self.fileProcessor.GetGPSlist())
			self.analysis.MakeClusterArea()
			self.analysis.CalClusteringAccuracy()
			
			#file output of clustering process (numerical & visual)
			if self.fileProcessor.NumericalResultOfLocationClustering(self.analysis.GetClusters(), self.analysis.GetTransitionMatrix(), self.mode, 0) is False:
				print("NumericalResultOfLocationClustering fail")
				return False
			#print("Transition Matrix :", self.analysis.GetTransitionMatrix())
			if self.fileProcessor.VisualResultOfLocationClustering(self.analysis.GetClusters(), self.mode) is False:
				print("VisualResultOfLocationClustering fail")
				return False
			#set parameter of mobility object
			currentMobility.SetMobility(self.fileProcessor.GetGPSlist(), self.analysis.GetClusters())
			#reset process of Analysis object
			self.analysis.ResetAnalysis()
			self.fileProcessor.DeleteGPSlist()
			
		self.analysis.MergeMobility()
		self.analysis.CalTransitionInterCluster(self.analysis.GetMergeList())
		self.analysis.MakeClusterArea()
		self.analysis.SetTotalTrace()
		temp = self.analysis.GetClusters()
		size = len(temp)
		if self.fileProcessor.NumericalResultOfLocationClustering(self.analysis.GetClusters(), self.analysis.GetTransitionMatrix(), 0, self.analysis.GetTotalDuration()) is False:
			print("NumericalResultOfLocationClustering fail")
			return False
		if self.fileProcessor.VisualResultOfLocationClustering(self.analysis.GetClusters(), 0) is False:
			print("VisualResultOfLocationClustering fail")
			return False
		if self.fileProcessor.ResultOfTotalTimedTrace(self.analysis.GetTotalTimedTrace(), size) is False:
			print("ResultOfTotalTimedTrace fail")
			return False

		self.analysis.ResetAnalysis()

		return True
