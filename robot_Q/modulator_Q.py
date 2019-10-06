#Aux functions



#Main function
def modulator_Q(SETTINGS):
	print('\nImporting Q libraries.\n')
	from active_Q import getQdata
	from chrome_Q import writeGdata

	print('\n Getting Q data... \n')
	Q = getQdata(SETTINGS)

	print('\n Upload Q data to gSheet? \n')
	writeGdata(Q,SETTINGS)
	print('Q session complete.')

if __name__=="__main__":
	
	SETTINGS = {"campaigns":["_MF1_","_MF2_","_MF3_","_MF4_"],
				"location_cd":"C:/Users/steve/Downloads/chromedriver.exe",
				'linked_login_url': "https://www.linkedin.com/uas/login?",
				'linked_connections_url':"https://www.linkedin.com/mynetwork/invite-connect/connections/",
				'linked_username':'',
				'linked_password':'',
				'linked_messages_url':"https://www.linkedin.com/messaging/",
				'spread_name':'Marketforce_Manager_Automated',
				'sheet_name':'',
				'linkedA1.ahk loc':"C:/Users/steve/Desktop/Python/marketforce_code/robot_A/linkedA1.ahk",
				'linkedA2.ahk loc':"C:/Users/steve/Desktop/Python/marketforce_code/robot_A/linkedA2.ahk",
				'ahkexe loc':"C:/Program Files/AutoHotkey/AutoHotkey.exe",
				'linkhelp_username':"eric@marketforce.ca",
				'linkhelp_password':"Ilovecottage6!!link",
				'invitemax':95,
				'download_folder':"C:/Users/steve/Downloads/Marketforce2DAN",
				'linkhelp_backup.txt loc':'C:/Users/steve/Desktop/Python/marketforce_code/robot_A/LinkedHelper Backups/backup.txt',
				'servitor':'',
				'servitor_fname':'',
				'active_login':"https://www.activecampaign.com/login/"}

	modulator_Q(SETTINGS)