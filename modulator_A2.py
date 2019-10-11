def modulator_A2():
	import pandas as pd
	from gspread_pandas import Spread
	import numpy as np
	import datetime
	from time import sleep

	spread_names = ['MF3','MF4']
	sheet_name = "Sheet1"

#
	for spread in spread_names:
		
		#Spread 1 -> lList
		
		s1 = Spread(spread)									
		s1.open_sheet(sheet_name)								
		df = s1.sheet_to_df(header_rows=1).astype(str)
		dt = str(datetime.datetime.now())
		ldf_sub = df[['Full name','Profile url']]
		lList = ldf_sub.values.tolist()



		#Spread 2 -> gList
		sheet2_name = "_"+spread+"_"
		s2 = Spread("Marketforce_Manager_Automated")									
		s2.open_sheet(sheet2_name)						
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

		s2.df_to_sheet(xf,index=False,headers=False,sheet=sheet2_name,start='A3')

if __name__ == '__main__':
	modulator_A2()