'''
Pulls send message 2? and send message 3? status from GSHEET
'''

def g_detect(spread_name,sheet_name):
	#Imports
	import pandas as pd
	from gspread_pandas import Spread
	

	#Load data
	s = Spread(spread_name)
	s.open_sheet(sheet_name)
	df = s.sheet_to_df(header_rows=1).astype(str)	
	df_sub = df[['Name','URL','send message 2?','Date we sent message 2','should we send message 3?']]		
	df_sublist = df_sub.values.tolist()

	#Edit data
	detections=[]
	for thing in df_sublist:
		if thing[2]=='1' or thing[4]=='1':
			detections.append(thing)
	
	#detections = [['Eric Laycock','https://www.linkedin.com/in/eric-laycock-938a64185','1','2019/5/9 13:47:00',0'],['Dan Goulet','https://www.linkedin.com/in/dan-goulet-8b73a639','0','2019/5/9 13:47:00','1']]

	return detections


def g_write(m2dm3,spread_name,sheet_name):
	import pandas as pd
	from gspread_pandas import Spread
	import numpy as np


	#Load data
	s = Spread(spread_name)
	s.open_sheet(sheet_name)
	df = s.sheet_to_df(header_rows=1).astype(str)			#This converts the spreadsheet into a Panda's dataframe
	df_sub = df[['Name','M2 - We sent message 2.','Date we sent message 2','M3 - We sent message 3.']]
	kf = df_sub.values.tolist()

	for element in kf:
		if element[0] == m2dm3[0]:
			element[1]=m2dm3[1]
			element[2]=m2dm3[2]
			element[3]=m2dm3[3]


	kf=np.asarray(kf)
	kf=kf[1:]

	m2 = pd.DataFrame(kf[:,1])

	d = pd.DataFrame(kf[:,2])

	m3 = pd.DataFrame(kf[:,3])



	s.df_to_sheet(m2,index=False,headers=False,sheet=sheet_name,start='I3')

	s.df_to_sheet(d,index=False,headers=False,sheet=sheet_name,start='J3')

	s.df_to_sheet(m3,index=False,headers=False,sheet=sheet_name,start='N3')
