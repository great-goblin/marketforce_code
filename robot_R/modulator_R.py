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

	#Aux
	print('\n mod_R @ %s: Defining auxiliaries'%campaign)


	if campaign=='_MF1_':
		SETTINGS['linked_username']='stephane@fullview.ca'
		SETTINGS['linked_password']='Marketforce999!'
		SETTINGS['sheet_name']='_MF1_'
		SETTINGS['servitor']='Stephane Trottier'
		SETTINGS['servitor_fname']='Stephane'
		SETTINGS['msg2_body']="I'm one of the founders at Marketforce. I've developed a Facebook Ads training course specifically for realtors. This course will show you how to 5X your leads in 60 days or less. Have you thought about investing in your advertising skills?"
		SETTINGS['msg3_body']="You're frustrated with ineffective Facebook Ads and worried about Purplebricks. I help realtors who are struggling to generate enough leads become Facebook Ads experts and 5X their leads in less than 60 days. \n\n After all, research shows that 93% of all buyers search online for their home. (Proof: https://bit.ly/2ZkRZ0e). \n Are you open to a 10 minute call?"

	if campaign=='_MF2_':
		SETTINGS['linked_username']='dan@mediawize.ca'
		SETTINGS['linked_password']='linkedin999'
		SETTINGS['sheet_name']='_MF2_'
		SETTINGS['servitor']='Dan Goulet'
		SETTINGS['servitor_fname']='Dan'
		SETTINGS['msg2_body'] = "I'm one of the founders at Marketforce. My team has over 19 years of experience building custom brokerage websites. A custom website will showcase your brand and get you and your agents consistent leads that convert. Have you thought about investing in your website?"
		SETTINGS['msg3_body'] = "Your agents are disappointed with inconsistent leads, your customers are upset when their listing isn't on your site, and your admin is frustrated by your site's poor useability. I help brokers to upgrade their website's design, SEO and lead generation consistency. \n\n After all, research shows that 93% of all buyers make their buying decision online. (Proof: https://bit.ly/2ZkRZ0e). \n Are you open to a 10 minute call?"

	if campaign=='_MF3_':
		SETTINGS['linked_username']='stephane@fullview.ca'
		SETTINGS['linked_password']='Marketforce999!'
		SETTINGS['sheet_name']='_MF3_'
		SETTINGS['servitor']='Stephane Trottier'
		SETTINGS['servitor_fname']='Stephane'
		SETTINGS['msg2_body']="I'm one of the founders at Marketforce. I've developed a Facebook Ads training course specifically for realtors. This course will show you how to 5X your leads in 60 days or less. Have you thought about investing in your advertising skills?"
		SETTINGS['msg3_body']="You're frustrated with ineffective Facebook Ads and worried about Purplebricks. I help realtors who are struggling to generate enough leads become Facebook Ads experts and 5X their leads in less than 60 days. \n\n After all, research shows that 93% of all buyers search online for their home. (Proof: https://bit.ly/2ZkRZ0e). \n Are you open to a 10 minute call?"

	if campaign=='_MF4_':
		SETTINGS['linked_username']='dan@mediawize.ca'
		SETTINGS['linked_password']='linkedin999'
		SETTINGS['sheet_name']='_MF4_'
		SETTINGS['servitor']='Dan Goulet'
		SETTINGS['servitor_fname']='Dan'
		SETTINGS['msg2_body'] = "I'm one of the founders at Marketforce. My team has over 19 years of experience building custom brokerage websites. A custom website will showcase your brand and get you and your agents consistent leads that convert. Have you thought about investing in your website?"
		SETTINGS['msg3_body'] = "Your agents are disappointed with inconsistent leads, your customers are upset when their listing isn't on your site, and your admin is frustrated by your site's poor useability. I help brokers to upgrade their website's design, SEO and lead generation consistency. \n\n After all, research shows that 93% of all buyers make their buying decision online. (Proof: https://bit.ly/2ZkRZ0e). \n Are you open to a 10 minute call?"


	def compose_msg2(theirname):
		msg2 = ("Hi %s,\n"%theirname)+ SETTINGS['msg2_body'] + ('\n\n -%s'%SETTINGS['servitor_fname'])
		return msg2

	def compose_msg3(theirname):
		msg3 = ("Hey %s, I never heard back.\n"%theirname)+SETTINGS['msg3_body'] + ('\n\n -%s'%SETTINGS['servitor_fname'])
		return msg3

	def sendmsg(msg_content):
		try:
			u=driver.find_element_by_xpath('//div/div/div/span[1]/div/button')
			u.click()
			sleep(2)
			u=driver.find_element_by_xpath('//div[3]/div/div[1]/div[1]/p')
			u.click()
			u=driver.find_element_by_xpath('//form/div[3]/div/div[1]/div[1]')
			u.send_keys(msg_content)
			u=driver.find_element_by_xpath('//form/footer/div[2]/div[1]/button')
			u.click()
		except:
			driver.refresh()
			sleep(2)
			u=driver.find_element_by_xpath('//div/div/div/span[1]/div/button')
			sleep(2)
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
	detections = detections[1:]





	#Edit data
		#Login
	print('\n mod_R @ %s: Editing data. \n'%campaign)
	location = SETTINGS['location_cd']
	login_url = SETTINGS['linked_login_url']
	target_url = SETTINGS['linked_connections_url']
	user = SETTINGS['linked_username']
	password = SETTINGS['linked_password']
	global driver
	driver = webdriver.Chrome(location)					
	driver.get(login_url)								
	u = driver.find_element_by_name('session_key') 		
	u.send_keys(user)									
	u = driver.find_element_by_name('session_password') 
	u.send_keys(password)								
	u.send_keys(Keys.RETURN)							


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

					#Ask user if we should use companyname
					if companyname!='':
						msg2 = compose_msg2(firstname)
					else: 
						msg2 = compose_msg2(firstname)

					
					sendmsg(msg2)
					sublist.append('1')
					sublist.append(str(datetime.datetime.now()))
					sublist.append('0')
					g_write(sublist,SETTINGS)
				elif (person[2]=='0') and (person[4]=='1'):

					msg3 = compose_msg3(firstname)
					sendmsg(msg3)
					sublist.append('1')
					sublist.append(person[3])
					sublist.append('1')
					g_write(sublist,SETTINGS)
	
		except Exception as e:
			print(e)
			print('Aborting program.')
			break

	driver.close()
	print('\n mod_R @ %s- Program Complete. \n'%campaign)

if __name__=="__main__":
	
	modulator_R('Stephane')