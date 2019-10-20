'''
I send robot-responses (M2 and M3) based on whether the Google Sheet tells me I should.
'''

def modulator_R(campaign,SETTINGS):
	#Imports
	print('\n mod_R @ %s: Importing'%campaign)
	from chrome_R import g_detect, g_write
	from selenium import webdriver 						#this module automatically starts and controls a Chrome web session
	from selenium.webdriver.common.keys import Keys    #this module helps us input automatic login data  
	from time import sleep
	import datetime
	from twilio.rest import Client

	#Aux
	print('\n mod_R @ %s: Defining auxiliaries'%campaign)


	if campaign=='_MF1_':
		SETTINGS['linked_username']='stephane@fullview.ca'
		SETTINGS['linked_password']='Marketforce999!'
		SETTINGS['sheet_name']='_MF1_'
		SETTINGS['servitor']='Stephane Trottier'
		SETTINGS['servitor_fname']='Stephane'
		SETTINGS['msg2_body']= "Our team is impressed by your work. Would you be open to a podcast interview?"
		SETTINGS['msg3_body']="We'd like to host you on a short podcast interview. Thoughts?"

	if campaign=='_MF2_':
		SETTINGS['linked_username']='dan@mediawize.ca'
		SETTINGS['linked_password']='linkedin999'
		SETTINGS['sheet_name']='_MF2_'
		SETTINGS['servitor']='Dan Goulet'
		SETTINGS['servitor_fname']='Dan'
		SETTINGS['msg2_body']= "Our team is impressed by your work. Would you be open to a podcast interview?"
		SETTINGS['msg3_body']="We'd like to host you on a short podcast interview. Thoughts?"

	if campaign=='_MF3_':
		SETTINGS['linked_username']='stephane@fullview.ca'
		SETTINGS['linked_password']='Marketforce999!'
		SETTINGS['sheet_name']='_MF3_'
		SETTINGS['servitor']='Stephane Trottier'
		SETTINGS['servitor_fname']='Stephane'
		SETTINGS['msg2_body']= "Our team is impressed by your work. Would you be open to a podcast interview?"
		SETTINGS['msg3_body']="We'd like to host you on a short podcast interview. Thoughts?"

	if campaign=='_MF4_':
		SETTINGS['linked_username']='dan@mediawize.ca'
		SETTINGS['linked_password']='linkedin999'
		SETTINGS['sheet_name']='_MF4_'
		SETTINGS['servitor']='Dan Goulet'
		SETTINGS['servitor_fname']='Dan'
		SETTINGS['msg2_body']= "Our team is impressed by your work. Would you be open to a podcast interview?"
		SETTINGS['msg3_body']="We'd like to host you on a short podcast interview. Thoughts?"

	if campaign=='_ariLID1_':
		SETTINGS['linked_username']="arilaniado@gmail.com"
		SETTINGS['linked_password']='Marketforce11'
		SETTINGS['sheet_name']='_ariLID1_'
		SETTINGS['servitor']='Ari Laniado'
		SETTINGS['servitor_fname']='Ari'
		SETTINGS['msg2_body']="Great to connect! To briefly introduce myself, I’m a co-founder of the Colliers Venture Workspace Team. Our team advises the Toronto tech sector on securing workspace that fits their team’s growth. The right workspace should provide the flexibility your team requires, promote culture, and support talent recruitment. Would you be open to discussing how your current space is working for your team?"
		SETTINGS['msg3_body']="Employees are becoming increasingly demanding of their organization’s workspace and culture. We help ventures secure workspace that provide value-add to their business. Have you thought about your next workspace? \n\n Are you open to a 10 minute call?"
	
	def compose_msg2(theirname):
		msg2 = ("Hi %s,\n"%theirname)+ SETTINGS['msg2_body'] + ('\n\n -%s'%SETTINGS['servitor_fname'])
		return msg2

	def compose_msg3(theirname):
		msg3 = ("Hey %s, I never heard back.\n"%theirname)+SETTINGS['msg3_body'] + ('\n\n -%s'%SETTINGS['servitor_fname'])
		return msg3

	def sendmsg(msg_content):
		try:
			input('Search for button>>>')
			u=driver.find_element_by_xpath('//div/div/div/span[1]/div/button')
			print('Button is at //div/div/div/span[1]/div/button')
			input('Click button?>>>')
			u.click()
			sleep(2)
			u=driver.find_element_by_xpath('//div[3]/div/div[1]/div[1]/p')
			u.click()
			u=driver.find_element_by_xpath('//form/div[3]/div/div[1]/div[1]')
			u.send_keys(msg_content)
			u=driver.find_element_by_xpath('//form/footer/div[2]/div[1]/button')
			u.click()
		except:
			print('\n Error occurred. Refreshing browser.')
			driver.refresh()
			sleep(2)
			input('Search for button?>>>')
			u=driver.find_element_by_xpath('//div/div/div/span[1]/div/button')
			sleep(2)
			input('Click button?>>>')
			u.click()
			sleep(4)
			u=driver.find_element_by_xpath('//div[3]/div/div[1]/div[1]/p')
			u.click()
			u=driver.find_element_by_xpath('//form/div[3]/div/div[1]/div[1]')
			u.send_keys(msg_content)
			u=driver.find_element_by_xpath('//form/footer/div[2]/div[1]/button')
			u.click()


	#Load data
	print('\n mod_R @ %s: Loading data.'%campaign)
	detections = g_detect(SETTINGS)
	
	if detections[0][0]=='':
		detections=detections[1:]

	print("DETECTIONS: ",detections)



	#Edit data
		#Login
	print('\n mod_R @ %s: Editing data. \n'%campaign)
	location = SETTINGS['location_cd']
	login_url = SETTINGS['linked_login_url']
	target_url = SETTINGS['linked_connections_url']
	user = SETTINGS['linked_username']
	password = SETTINGS['linked_password']


	global driver
	options=webdriver.ChromeOptions()
	options.add_argument("--start-maximized")
	driver = webdriver.Chrome(location,chrome_options=options)					
	driver.get(login_url)								
	u = driver.find_element_by_name('session_key') 		
	u.send_keys(user)									
	u = driver.find_element_by_name('session_password') 
	u.send_keys(password)								
	u.send_keys(Keys.RETURN)							

	countx=0
	for person in detections:
	
		sublist=[]
		sleep(1)
		fullname = person[0]
		sublist.append(fullname)
		firstname = fullname.split(' ')[0]
		try: 
			driver.get(person[1])
			sleep(10)
			driver.execute_script("window.scrollTo(0,100)")
			sleep(10)
			driver.execute_script("window.scrollTo(0,800)")
			sleep(5)
			driver.execute_script("window.scrollTo(0,300)")
			sleep(5)
			driver.execute_script("window.scrollTo(0,0)")
			u=driver.find_element_by_xpath('//div[2]/div[2]/div[1]/ul[1]/li[2]/span/span[2]').text
			if u=='2nd' or u=='3rd':
				print('\n\n !!!!ALERT!!!! Please update GSHEET. This person is not connected. \n \n ALERT!!! \n \n')
				
			else:
				if (person[2]=='1') and (person[4]=='0'):
					#Extract company name --- This is a fucking disaster. Sorry
					try:
						companyname = driver.find_element_by_xpath('//section/div[2]/div[2]/div[2]/ul/li[1]/span')
						companyname = companyname.text
						try: 
							companynameList = companyname.split(' ')
							if ((companynameList[0]=='The') or (companynameList[0]=='THE') or (companynameList[0]=='the')):
								companyname = (companynameList[1]+" "+companynameList[2])
							else:
								companyname = (companynameList[0]+" "+companynameList[1])
						except:
							print('Company name = 1 word. No change made to original.')	
					except: 
						print('No company name detected.')
						companyname=''

					
					if companyname!='':
						msg2 = compose_msg2(firstname)
					else: 
						msg2 = compose_msg2(firstname)

					input('Send msg2? >>>')
					sendmsg(msg2)
					print('Updating gsheet. Do not abort.')
					sublist.append('1')
					sublist.append(str(datetime.datetime.now()))
					sublist.append('0')
					g_write(sublist,SETTINGS)
					countx+=1
				elif (person[2]=='0') and (person[4]=='1'):

					msg3 = compose_msg3(firstname)
					sendmsg(msg3)
					sublist.append('1')
					sublist.append(person[3])
					sublist.append('1')
					g_write(sublist,SETTINGS)
					countx+=1
		except Exception as e:
			print(e)
			print('Aborting program.')
			break
		print('countx = %s'%countx)
		if countx>=10:
			client = Client("AC983906068a9d52fc5a6612fcaeccd8f9","daf93dd641db22bee793ebdf0b8ac03a")
			client.messages.create(to="+16043143827",from_="+12085180535",body="10 messages successfully sent")
			countx=0


	driver.close()
	print('\n mod_R @ %s- Program Complete. \n'%campaign)

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

	modulator_R('_ariLID1_',SETTINGS)