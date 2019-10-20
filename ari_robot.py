
'''
Top level control for running modulators B,C and R
'''

import sys
from twilio.rest import Client
sys.path.append('C:/Users/Dan/Desktop/Python/marketforce_code/robot_A2')
sys.path.append('C:/Users/Dan/Desktop/Python/marketforce_code/robot_B')
sys.path.append('C:/Users/Dan/Desktop/Python/marketforce_code/robot_C')
#sys.path.append('C:/Users/Dan/Desktop/Python/marketforce_code/robot_Q')
sys.path.append('C:/Users/Dan/Desktop/Python/marketforce_code/robot_R')
from modulator_A2 import modulator_A2
from modulator_B import modulator_B
from modulator_C import modulator_C
#from modulator_Q import modulator_Q
from modulator_R import modulator_R
from time import sleep
import datetime


def txt(alert,alertmsg):

	client = Client("AC983906068a9d52fc5a6612fcaeccd8f9","daf93dd641db22bee793ebdf0b8ac03a")
	if alert==0:
		body=('ARI Robot ran with 0 alerts @ %s.'%datetime.datetime.now().strftime("%H%M"))
	else: body=('ARI Alerts @ %s.%s'%(datetime.datetime.now().strftime("%H%M"),alertmsg))
	client.messages.create(to="+16043143827",from_="+12085180535",body=body)
	#client.messages.create(to="+1/",from_="+12085180535",body=body)


if __name__=="__main__":
	
	#Define vars 
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

	

	#execute
	while True:
		curr_time = int(datetime.datetime.now().strftime("%H"))
		alert=0

		if curr_time >= 9 and curr_time < 17:
			alertmsg = 'Alerts: '
			try: modulator_A2(SETTINGS['spread_name'],SETTINGS['aux_spreads'],'Sheet1')
			except Exception as e:
				print('Alert for A2:',e)
				alert +=1
				alertmsg = alertmsg + ("Alert for A2: %s"%e)

			for campaign in SETTINGS['campaigns']:
				try:
					modulator_B(campaign, SETTINGS)
				except Exception as e:
					print('Alert for B:',e)
					alert += 1
					alertmsg = alertmsg + ("Alert for B: %s"%e)
				if alert == 1: break
				
				try:
					modulator_C(campaign, SETTINGS)
				except Exception as e:
					print('Alert for C:',e)
					alert = 1
					alertmsg = alertmsg + ("Alert for C: %s "%e)
				if alert == 1: break

				try:
					modulator_R(campaign,SETTINGS)
				except Exception as e:
					print('Alert for R:',e)
					alert = 1
					alertmsg = alertmsg + ("Alert for R: %s "%e)
			
			''' mod_Q is for a different CRM 
			try: modulator_Q(SETTINGS)
			except Exception as e:
				print('Alert in Q:',e)
				alert = 1
				alertmsg = alertmsg + ("Q alert: %s "%e)
			'''
			txt(alert, alertmsg)
	
		sleep(1800)
