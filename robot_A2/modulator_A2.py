def modulator_A2(mainspread, mainsheet, auxiliaryspread):
	import pandas as pd
	from gspread_pandas import Spread
	import numpy as np
	import datetime
	from time import sleep


	#Open auxiliary spread
	s1 = Spread(auxiliaryspread)									
	s1.open_sheet('Sheet1')								
	df = s1.sheet_to_df(header_rows=1).astype(str)
	dt = str(datetime.datetime.now())
	ldf_sub = df[['Full name','Profile url']]
	lList = ldf_sub.values.tolist()


	#Open main spread
	s2 = Spread(mainspread)									
	s2.open_sheet(mainsheet)						
	gdf = s2.sheet_to_df(index=0).astype(str)
	gdf_sub = gdf[['Invited at:','Name','URL']]
	gList = gdf_sub.values.tolist()

	gList = list(filter((['','','']).__ne__,gList))			#Removes ['',''] from list.

	for k in range(len(lList)):
		if lList[k][0]==gList[-1][1]:
			fin = k+1

	lList_sub = lList[fin:]

	for elm in lList_sub:									#Append every element of this short list to the end of gList. Also, add the date.
		gList.append([dt,elm[0],elm[1]])
	#print(gList)
	gArray = np.asarray(gList)
	#print(gArray)
	dates = gArray[:,0]
	names = gArray[:,1]
	urls = gArray[:,2]
	#Turn gList back into df
	x = {'Invited at:':dates,'Name':names,'URL':urls}


	xf = pd.DataFrame(x)

	s2.df_to_sheet(xf,index=False,headers=False,sheet=mainsheet,start='A3')