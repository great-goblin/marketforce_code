def writeGdata(Q, SETTINGS):
	print('Importing.')
	#Imports
	import pandas as pd
	from gspread_pandas import Spread
	import numpy as np
	import datetime

	#Vars
	spread_name = SETTINGS['spread_name']
	s = Spread(spread_name)

	for campaign in SETTINGS['campaigns']:

		#Initialize
		sheet_name = campaign
		s.open_sheet(sheet_name)
		df = s.sheet_to_df(header_rows=1).astype(str)			#This converts the spreadsheet into a Panda's dataframe
		df_sub = df['Name']

		#Build initial array
		nf = df_sub.values
		nf = nf[:,np.newaxis]
		zeroes = np.asarray(['0'] * len(nf))
		zeroes = zeroes[:,np.newaxis]
		NF0 = np.append(nf,zeroes,axis=1)
		NF1 = np.append(NF0,zeroes,axis=1)
		NF2 = np.append(NF1,zeroes,axis=1)
		NF2 = NF2[1:,:] #cut off first row
		lf = NF2[:,0].tolist()


		#Edit data
		for qualifying in Q[0]:
			try: 
				z = lf.index(qualifying)
				NF2[z,1]='1'
			except:pass	
		for qualified in Q[1]:
			try:
				z = lf.index(qualified)
				NF2[z,1]='1'
				NF2[z,2]='1'
			except:pass
		for closed in Q[2]:
			try:
				z = lf.index(closed)
				NF2[z,1]='1'
				NF2[z,2]='1'
				NF2[z,3]='1'
			except:pass



		df_qualifying = pd.DataFrame(NF2[:,1])
		s.df_to_sheet(df_qualifying,index=False,headers=False,sheet=sheet_name,start='Q3')
		df_qualified = pd.DataFrame(NF2[:,2])
		s.df_to_sheet(df_qualified,index=False,headers=False,sheet=sheet_name,start='R3')
		df_closed = pd.DataFrame(NF2[:,3])
		s.df_to_sheet(df_closed,index=False,headers=False,sheet=sheet_name,start='S3')
		
	
