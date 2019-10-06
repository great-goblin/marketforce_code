
'''
Top level control for running modulators B,C and R
'''

import sys
from twilio.rest import Client
sys.path.append('C:/Users/Dan/Desktop/Python/marketforce_code/robot_B')
sys.path.append('C:/Users/Dan/Desktop/Python/marketforce_code/robot_C')
sys.path.append('C:/Users/Dan/Desktop/Python/marketforce_code/robot_Q')
sys.path.append('C:/Users/Dan/Desktop/Python/marketforce_code/robot_R')
from modulator_B import modulator_B
from modulator_C import modulator_C
from modulator_Q import modulator_Q
from modulator_R import modulator_R
from time import sleep
import datetime

def maintain_q(SETTINGS):
	modulator_Q(SETTINGS)
def maintain_bc(campaign, SETTINGS):

	modulator_B(campaign, SETTINGS)
	modulator_C(campaign, SETTINGS)

def message(campaign, SETTINGS):
	modulator_R(campaign, SETTINGS)

def txt(err):
	client = Client("AC983906068a9d52fc5a6612fcaeccd8f9","daf93dd641db22bee793ebdf0b8ac03a")
	if err==0:
		body=('Robot succeeded @ %s.'%datetime.datetime.now().strftime("%H%M"))
	else: body=('Robot failed @ %s.'%datetime.datetime.now().strftime("%H%M"))
	client.messages.create(to="+16043143827",from_="+12085180535",body=body)


if __name__=="__main__":
	
	#Define vars 
	SETTINGS = {'campaigns':['_MF1_','_MF2_','_MF3_','_MF4_'],
			"location_cd":"C:/Users/Dan/webdrivers/chromedriver_win32/chromedriver.exe",
			'linked_login_url': "https://www.linkedin.com/uas/login?",
			'linked_connections_url':"https://www.linkedin.com/mynetwork/invite-connect/connections/",
			'linked_messages_url':'https://www.linkedin.com/messaging/',
			'linked_username':"",
			'linked_password':"",
			'spread_name':'Marketforce_Manager_Automated',
			'sheet_name':'',
			'active_login':'https://www.activecampaign.com/login/',
			'linkedA1.ahk loc':"C:/Users/Dan/Desktop/Python/marketforce_code/robot_A/linkedA1.ahk",
			'linkedA2.ahk loc':"C:/Users/Dan/Desktop/Python/marketforce_code/robot_A/linkedA2.ahk",
			'ahkexe loc':"C:/Program Files/AutoHotkey/AutoHotkey.exe",
			'linkhelp_username':"eric@marketforce.ca",
			'linkhelp_password':"Ilovecottage6!!link",
			'invitemax':95,
			'download_folder':"C:/Users/Dan/Downloads",
			'linkhelp_backup.txt loc':'C:/Users/Dan/Desktop/Python/marketforce_code/robot_A/LinkedHelper Backups/backup.txt',
            'servitor':'',
            'servitor_fname':'',
			'msg2_body':'',
			'msg3_body':''}

	

	#execute
	while True:
		curr_time = int(datetime.datetime.now().strftime("%H"))
		err=0

		if curr_time >= 9 and curr_time < 19:
			for campaign in SETTINGS['campaigns']:
				try:
					maintain_bc(campaign, SETTINGS)
					#message(campaign, SETTINGS)
				except Exception as e:
					print(e)
					err = 1
			try: maintain_q(SETTINGS)
			except Exception as e:
				print(e)
				err = 1
			txt(err)
	
		sleep(1800)
