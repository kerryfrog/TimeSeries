
# coding: utf-8

# In[5]:


#main.cpp


# In[1]:


import LocationAnalysis as LA
import sys


# In[2]:


#int argc, char** argv
def main(_argv):
	#sys.path.append('/Users/Downloads/temp/em')
	sys.path.append('.')
	locAnalysis = LA.LocationAnalysis(len(_argv), _argv)
	
	if locAnalysis.GetMode() == 0:
		print("please check the arguments")
	elif locAnalysis.GetMode() == 1:
		locAnalysis.ShowUsage()
	elif locAnalysis.GetMode() == 2:
		if locAnalysis.ConvertRawToKML():
			print("success converting rawdata to kmldata")
		else:
			print("fail converting")
	elif locAnalysis.GetMode() == 3:
		if locAnalysis.DailyAnalysis():
			print("daily based locatioin analysis success")
		else:
			print("fail analysis(daily based)")
			
	return 0

if __name__ == "__main__":
	main(sys.argv)


# In[ ]:


'''
int main(int argc, char** argv)
{
	LocationAnalysis locAnalysis(argc, argv);

	switch(locAnalysis.GetMode())
	{
		case 0:
			cout<<"please check the arguments"<<endl;
			break;
		case 1:
			locAnalysis.ShowUsage();
			break;
		case 2:
			if(locAnalysis.ConvertRawToKML()){
				cout<<"success converting rawdata to kmldata"<<endl;
			}
			else{
				cout<<"fail converting"<<endl;
			}
			break;
		case 3:
			if(locAnalysis.DailyAnalysis()){
				cout<<"daily based location analysis success"<<endl;
			}else{
				cout<<"fail analysis(daily based)"<<endl;
			}
			break;
		default:
			break;
	}

	return 0;
}
'''

