'''
I get recent messages from linkedin and push them to modulator
'''


#Helper Functions
def expand_shadow_element(element):
	shadow_root = driver.execute_script('return arguments[0].shadowRoot', element)
	return shadow_root

def bruteclickx(xpath,child='',error=0):
	if error==0:
		try:
			sleep(2)
			if child == '':
				u=driver.find_element_by_xpath(xpath)
				u.click()
			else:
				u=driver.find_elements_by_xpath(xpath)[child]
				u.click()
		except:
			driver.refresh()
			error+=1
			bruteclickx(xpath,child,error)
	else:
		print('Bruteclickx Failure.')

def clickx(xpath,child=''):
	if child == '':
		u=driver.find_element_by_xpath(xpath)
		u.click()
	else:
		u=driver.find_elements_by_xpath(xpath)[child]
		u.click()



def getx(xpath):
	u=driver.find_element_by_xpath(xpath)
	return u.text

def findx(xpath):
	return driver.find_element_by_xpath(xpath)

def getmessages(self,user,password):
	#Imports
	from selenium import webdriver 						#this module automatically starts and controls a Chrome web session
	from selenium.webdriver.common.keys import Keys    #this module helps us input automatic login data
	from bs4 import BeautifulSoup
	from time import sleep
	import re

	#Vars
	location = self.location_cd
	login_url = self.linked_login_url
	target_url = self.linked_messages_url

	#Initialize
	global driver
	driver = webdriver.Chrome(location)
	#this initiates the auto Chrome session. If any problems, download new chromedriver version from https://sites.google.com/a/chromium.org/chromedriver/downloads and then edit the "Path" environment variable to include the /chromedriver.exe location

	#Login
	driver.get(login_url)#navigates to login URL
	u = driver.find_element_by_name('session_key')#Finds email login field
	u.send_keys(user)#Inputs username
	u = driver.find_element_by_name('session_password') #Finds password field
	u.send_keys(password)#Inputs password
	u.send_keys(Keys.RETURN)#Presses "enter"
	driver.get(target_url)#navigates to target URL

	sleep(5)

	#Get Conversations (scroll down three times)
	print('Building biglist')
	biglist = driver.find_elements_by_xpath("//div/div[1]/div/div[1]/ul/*")
	driver.execute_script("arguments[0].scrollIntoView();",biglist[-2])
	biglist2 = driver.find_elements_by_xpath("//div/div[1]/div/div[1]/ul/*")
	driver.execute_script("arguments[0].scrollIntoView();",biglist2[-2])
	biglist3 = driver.find_elements_by_xpath("//div/div[1]/div/div[1]/ul/*")
	driver.execute_script("arguments[0].scrollIntoView();",biglist3[-2])
	biglist4 = driver.find_elements_by_xpath("//div/div[1]/div/div[1]/ul/*")
	print('Biglist built')
	clist = []

	#Retrieve most recent ~100 conversations
	print('Building CLIST')
	for index in range(len(biglist4)):
		clist.append("//div/div[1]/div/div[1]/ul/li[%s]/div/a/div[2]/div[2]/p/span/span"%(index+1))

	clist=clist[1:-1]
	print('CLIST built')
	#Scroll down

	


	messages=[]
	for convo in clist:
		passval = 1
		try: 
			clickx(convo)
		except: 
			print('Cant click this shit')
			passval = 0
		

		sleep(2)

		if passval == 1:
			listx=driver.find_elements_by_xpath("//div[4]/div/ul/*")
			listx=listx[2:]
			dialogue = []
			for index in range(len(listx)):
				try:
					dialogue.append(getx('//div[4]/div/ul/li[%s]/div/div[1]/a/span'%(index+2)))
				except:
					pass

			messages.append([getx('//*/dl/dt/h2'),dialogue]	)
	driver.close()
	return messages
