'''
I update google sheets
'''

def push2sheets(dictionary,SETTINGS):

	#Imports
	import pandas as pd
	from gspread_pandas import Spread
	import numpy as np
	import datetime

	#Vars
	spread_name = SETTINGS['spread_name']
	sheet_name = SETTINGS['sheet_name']

	s = Spread(spread_name)									#This grabs the entire spreadsheet document and injects it into "s"
	s.open_sheet(sheet_name)								#This selects just one tab-sheet
	df = s.sheet_to_df(header_rows=1).astype(str)			#This converts the spreadsheet into a Panda's dataframe
	df_sub = df[['Name','C1 - They first replied to invite','M2 - We sent message 2.','Date we sent message 2','C2 - They first replied to message 2.','M3 - We sent message 3.','C3 - They first replied to message 3','D - They have replied a second time']]				#Creates a smaller df, with just column 0 and column 3
	kf = df_sub.values

	A_list = list(dictionary.keys())

	for key in A_list:
		for name_index in range(len(kf[:,0])):
			if key==kf[name_index,0]:
				kf[name_index,1]=dictionary[key]['C1']
				kf[name_index,2]=dictionary[key]['M2']

				if ((kf[name_index,2]==1) and (kf[name_index,3]=='')):
					print('ALERT! Message 2 was sent with no time entry. Inserting one now.')
					kf[name_index,3]=str(datetime.datetime.now())
				kf[name_index,4]=dictionary[key]['C2']
				kf[name_index,5]=dictionary[key]['M3']
				kf[name_index,6]=dictionary[key]['C3']
				kf[name_index,7]=dictionary[key]['D']
	
	kf = kf[1:,:]										#Drops first row, which only has summations


	c1 = pd.DataFrame(np.asarray(kf[:,1]))
	s.df_to_sheet(c1,index=False,headers=False,sheet=sheet_name,start='G3')

	m2 = pd.DataFrame(np.asarray(kf[:,2]))
	s.df_to_sheet(m2,index=False,headers=False,sheet=sheet_name,start='I3')

	dm2 = pd.DataFrame(np.asarray(kf[:,3]))
	s.df_to_sheet(dm2,index=False,headers=False,sheet=sheet_name,start='J3')

	c2 = pd.DataFrame(np.asarray(kf[:,4]))
	s.df_to_sheet(c2,index=False,headers=False,sheet=sheet_name,start='K3')

	if SETTINGS['campaigns'][0]=='_ariLID1_':
		m3 = pd.DataFrame(np.asarray(kf[:,5]))
		s.df_to_sheet(m3,index=False,headers=False,sheet=sheet_name,start='M3')

		c3 = pd.DataFrame(np.asarray(kf[:,6]))
		s.df_to_sheet(c3,index=False,headers=False,sheet=sheet_name,start='N3')

		d = pd.DataFrame(np.asarray(kf[:,7]))
		s.df_to_sheet(d,index=False,headers=False,sheet=sheet_name,start='O3')

	else:
		m3 = pd.DataFrame(np.asarray(kf[:,5]))
		s.df_to_sheet(m3,index=False,headers=False,sheet=sheet_name,start='N3')

		c3 = pd.DataFrame(np.asarray(kf[:,6]))
		s.df_to_sheet(c3,index=False,headers=False,sheet=sheet_name,start='O3')

		d = pd.DataFrame(np.asarray(kf[:,7]))
		s.df_to_sheet(d,index=False,headers=False,sheet=sheet_name,start='P3')

