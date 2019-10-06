'''

chrome_B: gets spreadsheet, updates spreadsheet (with connection status)


'''

def g_read(SETTINGS):
	#Imports
	import pandas as pd
	from gspread_pandas import Spread
	import numpy as np

	#Vars
	spread_name = SETTINGS['spread_name']
	sheet_name = SETTINGS['sheet_name']

	#Instantiate
	s = Spread(spread_name)									#This grabs the entire spreadsheet document and injects it into "s"
	s.open_sheet(sheet_name)								#This selects just one tab-sheet
	df = s.sheet_to_df(header_rows=1).astype(str)			#This converts the spreadsheet into a Panda's dataframe
	df_sub = df[['Name','B - Connected']]				#Creates a smaller df, with just column 0 and column 3

	#Convert List to gDict
	gList = df_sub.values.tolist()							#This converts the df to an array, and an array to a list. 
	gList=gList[1:]											#Cuts off first element in the list

	#Check gList subarray for name duplicates, eg. "Bob","Bob"
	gNames=np.asarray(gList)[:,0]
	gNames=gNames.tolist()
	#Check for multiple entries
	multiD = {i:gNames.count(i) for i in gNames}
	for key in list(multiD.keys()):
		if multiD[key] > 1 and key!='':
			print('ALERT! Multiple occurances of %s in Spreadsheet.\n Will add underscore to end of first instance. \n Please check initial conditions now \n\n Hit enter to alter. >>>'%key)
			try: 
				z = gList.index([key,'0'])
				x = '0'
			except: 
				z = gList.index([key,'1'])
				x = '1' 
			gList[z] = [key+"_",x]
			print('\n\n gList altered, new entry is %s'%gList[z])
			

	gDict = {}
	for element in gList:									#gList looks like this:   [		['Name','0'],	['Name2','0']	]
		gDict[element[0]] = int(element[1])					#Converts first item of each element into a dictionary key, and the second into a dictionary value.	

	#Output
	return gDict


# I submit updated dictionaries to a specific Google Sheet.
def g_write(gDict_updated,SETTINGS):
	#Imports
	import pandas as pd
	from gspread_pandas import Spread
	import numpy as np

	#Vars
	spread_name = SETTINGS['spread_name']
	sheet_name = SETTINGS['sheet_name']
	
	#Instantiate
	s = Spread(spread_name)

	#Convert gDict to df
	gList_0 = []
	gList_1 = []
	for element in gDict_updated.items():
		gList_0.append([element[0]])
		gList_1.append([element[1]])	


	df_0 = pd.DataFrame(np.asarray(gList_0))
	df_1 = pd.DataFrame(np.asarray(gList_1))

	#Inject df back into Google Sheet
	s.df_to_sheet(df_0,index=False,headers=False,sheet=sheet_name,start='B3') ##For bug testing. Places list of names next to other list of names.
	s.df_to_sheet(df_1,index=False,headers=False,sheet=sheet_name,start='F3')

