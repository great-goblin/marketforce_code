'''

modulator_B: gets LinkedIn connection data, pushes that to ChromeGoogleSheets

'''



def modulator_B(self,campaign,linked_username,linked_password,spread_name,sheet_name):
	# Imports
	print('\n mod_B @ %s: Importing'%campaign)
	from chrome_B import g_read, g_write
	from linkedin_B import l_read
	import pandas as pd



	# Load data
	print('\n mod_B @ %s: Loading Data'%campaign)
	gDict = g_read(spread_name,sheet_name)
	lList = l_read(self,linked_username,linked_password)
	

	
	# Edit data
	print('\n mod_B @ %s: Editing Data'%campaign)
	gList = list(gDict.keys())						#convert all keys in gDict into list

	for lName in lList:					#if (gName = lName), set gDict entry for that name =1
		for gName in gList:
			if (gName in lName) and (gName != ''):
				gDict[gName]=1

			

	# Output data
	print('\n mod_B @ %s: Outputting Data?>>>'%campaign)
	g_write(gDict,spread_name,sheet_name)

	print('\n mod_B @ %s: Program Complete.'%campaign)

