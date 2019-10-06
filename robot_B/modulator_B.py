'''

modulator_B: gets LinkedIn connection data, pushes that to ChromeGoogleSheets

'''



def modulator_B(campaign,SETTINGS):
	# Imports
	print('\n mod_B @ %s: Importing'%campaign)
	from chrome_B import g_read, g_write
	from linkedin_B import l_read
	import pandas as pd

	#Vars
	print('\n mod_B @ %s: Defining Variables'%campaign)


	if campaign=='_MF1_':
		SETTINGS['linked_username']='stephane@fullview.ca'
		SETTINGS['linked_password']='Marketforce999!'
		SETTINGS['sheet_name']='_MF1_'

	if campaign=='_MF2_':
		SETTINGS['linked_username']='dan@mediawize.ca'
		SETTINGS['linked_password']='linkedin999'
		SETTINGS['sheet_name']='_MF2_'

	if campaign=="_MF3_":
		SETTINGS['linked_username']='stephane@fullview.ca'
		SETTINGS['linked_password']='Marketforce999!'
		SETTINGS['sheet_name']='_MF3_'

	if campaign=='_MF4_':
		SETTINGS['linked_username']='dan@mediawize.ca'
		SETTINGS['linked_password']='linkedin999'
		SETTINGS['sheet_name']='_MF4_'

	if campaign=='backupmf4':
		SETTINGS['linked_username']='dan@mediawize.ca'
		SETTINGS['linked_password']='linkedin999'
		SETTINGS['sheet_name']='backupmf4'	

	# Load data
	print('\n mod_B @ %s: Loading Data'%campaign)
	gDict = g_read(SETTINGS)
	lList = l_read(SETTINGS)
	
	# Edit data
	print('\n mod_B @ %s: Editing Data'%campaign)
	gList = list(gDict.keys())						#convert all keys in gDict into list

	for lName in lList:					#if (gName = lName), set gDict entry for that name =1
		for gName in gList:
			if (gName in lName) and (gName != ''):
				gDict[gName]=1

			

	# Output data
	print('\n mod_B @ %s: Outputting Data'%campaign)
	g_write(gDict,SETTINGS)

	print('\n mod_B @ %s: Program Complete.'%campaign)


if __name__=="__main__":
	

	modulator_B('_MF1_')
