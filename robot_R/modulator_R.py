'''
I send robot-responses (M2 and M3) based on whether the Google Sheet tells me I should.
'''

def modulator_R(self,campaign,user,password,spread_name,sheet_name,servitor,servitor_fname,m2_body,m3_body):
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


	def compose_msg2(theirname):
		msg2 = ("Hi %s,\n\n"%theirname)+ m2_body + ('\n\n -%s'%servitor_fname)
		return msg2

	def compose_msg3(theirname):
		msg3 = ("Hey %s, I never heard back.\n\n"%theirname)+m3_body + ('\n\n -%s'%servitor_fname)
		return msg3

	def sendmsg(msg_content):
		try:
			print('Search for button>>>')
			sleep(3)
			u=driver.find_element_by_xpath('//div/div/div/span[1]/div/button')
			print('Button is at //div/div/div/span[1]/div/button')
			print('Click button?>>>')
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
			print('Search for button?>>>')
			u=driver.find_element_by_xpath('//div/div/div/span[1]/div/button')
			sleep(2)
			print('Click button?>>>')
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
	detections = g_detect(spread_name,sheet_name)
	try:
		if detections[0][0]=='':
			detections=detections[1:]
	except:
		pass



	#Edit data
		#Login
	print('\n mod_R @ %s: Editing data. \n'%campaign)
	location = self.location_cd
	login_url = self.linked_login_url
	target_url = self.linked_connections_url


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

	if len(detections)>0:
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

				print('FIND ELEMENT>>>')
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

						print('Send msg2? >>>')
						sendmsg(msg2)
						print('Updating gsheet. Do not abort.')
						sublist.append('1')
						sublist.append(str(datetime.datetime.now()))
						sublist.append('0')
						g_write(sublist,spread_name,sheet_name)
						countx+=1
					elif (person[2]=='0') and (person[4]=='1'):

						msg3 = compose_msg3(firstname)
						sendmsg(msg3)
						sublist.append('1')
						sublist.append(person[3])
						sublist.append('1')
						g_write(sublist,spread_name,sheet_name)
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
