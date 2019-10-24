'''

linkedin_B: gets connection status from LinkedIn, pushes that to modulator_B

'''

##! c2 >
def findx(xpath):
	return driver.find_element_by_xpath(xpath)

def getx(xpath):
	u=driver.find_element_by_xpath(xpath) 
	return u.text

##! c2 <

def l_read(self,user,password):
	#Imports
	from selenium import webdriver 						#this module automatically starts and controls a Chrome web session
	from selenium.webdriver.common.keys import Keys    #this module helps us input automatic login data  
	from bs4 import BeautifulSoup
	from time import sleep
	import re


	location = self.location_cd
	login_url = self.linked_login_url
	target_url = self.linked_connections_url

	global driver ##! c1
	driver = webdriver.Chrome(location)					#this initiates the auto Chrome session. If any problems, download new chromedriver version from https://sites.google.com/a/chromium.org/chromedriver/downloads and then edit the "Path" environment variable to include the /chromedriver.exe location
	driver.get(login_url)								#navigates to login URL
	u = driver.find_element_by_name('session_key') 		#Finds email login field
	u.send_keys(user)									#Inputs username
	u = driver.find_element_by_name('session_password') #Finds password field
	u.send_keys(password)								#Inputs password
	u.send_keys(Keys.RETURN)							#Presses "enter"

	driver.get(target_url)								#navigates to target URL
	sleep(5)
	
	##! c4 >

	try: #assume xpath =  /html/body/div[6]/*
		biglist = driver.find_elements_by_xpath('/html/body/div[6]/div[5]/div[3]/div/div/div/div/div/div/div/div/section/ul/*') ##!c 3					
		driver.execute_script("arguments[0].scrollIntoView();",biglist[-2])
		biglist2 = driver.find_elements_by_xpath('/html/body/div[6]/div[5]/div[3]/div/div/div/div/div/div/div/div/section/ul/*')
		driver.execute_script("arguments[0].scrollIntoView();",biglist2[-2])
		biglist3 = driver.find_elements_by_xpath('/html/body/div[6]/div[5]/div[3]/div/div/div/div/div/div/div/div/section/ul/*')
		driver.execute_script("arguments[0].scrollIntoView();",biglist3[-2])
		biglist4 = driver.find_elements_by_xpath('/html/body/div[6]/div[5]/div[3]/div/div/div/div/div/div/div/div/section/ul/*')

		lList = []
		for k in range(len(biglist4)):
			name = getx('/html/body/div[6]/div[5]/div[3]/div/div/div/div/div/div/div/div/section/ul/li[%s]/div/div[1]/a/span[2]'%(k+1))
			lList.append(name)
	except: #assume xpath = /html/body/div[5]/*
		biglist = driver.find_elements_by_xpath('/html/body/div[5]/div[5]/div[3]/div/div/div/div/div/div/div/div/section/ul/*') ##!c 3					
		driver.execute_script("arguments[0].scrollIntoView();",biglist[-2])
		biglist2 = driver.find_elements_by_xpath('/html/body/div[5]/div[5]/div[3]/div/div/div/div/div/div/div/div/section/ul/*')
		driver.execute_script("arguments[0].scrollIntoView();",biglist2[-2])
		biglist3 = driver.find_elements_by_xpath('/html/body/div[5]/div[5]/div[3]/div/div/div/div/div/div/div/div/section/ul/*')
		driver.execute_script("arguments[0].scrollIntoView();",biglist3[-2])
		biglist4 = driver.find_elements_by_xpath('/html/body/div[5]/div[5]/div[3]/div/div/div/div/div/div/div/div/section/ul/*')

		lList = []
		for k in range(len(biglist4)):
			name = getx('/html/body/div[5]/div[5]/div[3]/div/div/div/div/div/div/div/div/section/ul/li[%s]/div/div[1]/a/span[2]'%(k+1))
			lList.append(name)	

	driver.close()
	
	return lList
