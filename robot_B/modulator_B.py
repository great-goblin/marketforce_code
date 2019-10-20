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

	if campaign == '_ariLID1_':
		SETTINGS['sheet_name']='_ariLID1_'


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
	
	SETTINGS = {'campaigns':['_ariLID1_'],
			"location_cd":"C:/Users/Dan/webdrivers/chromedriver_win32/chromedriver.exe",
			'linked_login_url': "https://www.linkedin.com/uas/login?",
			'linked_connections_url':"https://www.linkedin.com/mynetwork/invite-connect/connections/",
			'linked_messages_url':'https://www.linkedin.com/messaging/',
			'linked_username':"arilaniado@gmail.com",
			'linked_password':"Marketforce11",
			'spread_name':"Ari_LID",
			'aux_spreads':['ariLID1'],
			#'active_login':'https://www.activecampaign.com/login/',
			#'linkedA1.ahk loc':"C:/Users/Dan/Desktop/Python/marketforce_code/robot_A/linkedA1.ahk",
			#'linkedA2.ahk loc':"C:/Users/Dan/Desktop/Python/marketforce_code/robot_A/linkedA2.ahk",
			#'ahkexe loc':"C:/Program Files/AutoHotkey/AutoHotkey.exe",
			'linkhelp_username':"eric@marketforce.ca",
			'linkhelp_password':"Ilovecottage6!!link",
			#'invitemax':95,
			#'download_folder':"C:/Users/Dan/Downloads",
			#'linkhelp_backup.txt loc':'C:/Users/Dan/Desktop/Python/marketforce_code/robot_A/LinkedHelper Backups/backup.txt',
            'servitor':'',
            'servitor_fname':'',
			'msg2_body':'',
			'msg3_body':''}

	modulator_B('_ariLID1_',SETTINGS)

