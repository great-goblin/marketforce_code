#Aux functions
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

#Main function
def getQdata(SETTINGS):

	#Imports and vars
	from selenium import webdriver 						#this module automatically starts and controls a Chrome web session
	from selenium.webdriver.common.keys import Keys    #this module helps us input automatic login data  
	from time import sleep

	location = SETTINGS['location_cd']
	ac_login = SETTINGS['active_login']

	#Initialize and login
	global driver
	driver = webdriver.Chrome(location)

	driver.get(ac_login)

	u=findx('//*[@id="accountname"]')
	u.send_keys('brokeraccelerator')#Inputs password
	u.send_keys(Keys.RETURN)#Presses "enter"

	email = findx('//*[@id="user"]')
	email.send_keys('eric@marketforce.ca')
	password = findx('//*[@id="pass"]')
	password.send_keys('Marketforce999!')
	password.send_keys(Keys.RETURN)

	driver.get('https://brokeraccelerator.activehosted.com/app/deals/')

	#Download data from site
	qualifying = []
	qualified = []
	closed = []

	sleep(30)

	list_of_qualifying1 = driver.find_elements_by_xpath('/html/body/div[5]/div[1]/div[2]/div[2]/div[1]/div[3]/div/div[1]/div/div[4]/div/*')
	for i in range(len(list_of_qualifying1)):
		precursor = findx('/html/body/div[5]/div[1]/div[2]/div[2]/div[1]/div[3]/div/div[1]/div/div[4]/div/div[%s]'%(i+1))
		driver.execute_script("arguments[0].scrollIntoView();",precursor)
		sleep(1)
		qualifying.append(getx('/html/body/div[5]/div[1]/div[2]/div[2]/div[1]/div[3]/div/div[1]/div/div[4]/div/div[%s]/a/div[2]/div[2]/div'%(i+1)))
		

	list_of_qualifying2 = driver.find_elements_by_xpath('/html/body/div[5]/div[1]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div/div[3]/div/*')
	for i in range(len(list_of_qualifying2)):
		precursor = findx('/html/body/div[5]/div[1]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div/div[3]/div/div[%s]'%(i+1))
		driver.execute_script("arguments[0].scrollIntoView();",precursor)
		sleep(1)
		element = '/html/body/div[5]/div[1]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div/div[3]/div/div[%s]/a/div[2]/div[2]/div'%(i+1)
		qualifying.append(getx(element))

	list_of_qualified = driver.find_elements_by_xpath('/html/body/div[5]/div[1]/div[2]/div[2]/div[1]/div[3]/div/div[3]/div/div[4]/div/*')
	for i in range(len(list_of_qualified)):
		precursor = findx('/html/body/div[5]/div[1]/div[2]/div[2]/div[1]/div[3]/div/div[3]/div/div[4]/div/div[%s]'%(i+1))
		driver.execute_script("arguments[0].scrollIntoView();",precursor)
		sleep(1)
		element = '/html/body/div[5]/div[1]/div[2]/div[2]/div[1]/div[3]/div/div[3]/div/div[4]/div/div[%s]/a/div[2]/div[2]/div'%(i+1)
		qualified.append(getx(element))

	
	list_of_closed = driver.find_elements_by_xpath('/html/body/div[5]/div[1]/div[2]/div[2]/div[1]/div[3]/div/div[4]/div/div[2]/div/*')
	for i in range(len(list_of_closed)):
		try:
			precursor = findx('/html/body/div[5]/div[1]/div[2]/div[2]/div[1]/div[3]/div/div[3]/div/div[4]/div/div[%s]'%(i+1))
			driver.execute_script("arguments[0].scrollIntoView();",precursor)
			sleep(1)
			element = '/html/body/div[5]/div[1]/div[2]/div[2]/div[1]/div[3]/div/div[3]/div/div[4]/div/div[%s]/a/div[2]/div[2]/div'%(i+1)
			closed.append(getx(element))
		except Exception as e: print(e)

	driver.close()
	#Output data
	Q = [qualifying,qualified,closed]
	return Q