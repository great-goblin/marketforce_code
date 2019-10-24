from tkinter import *
from tkinter.ttk import *
import tkinter as tk
import sys
from twilio.rest import Client
sys.path.append('C:/Users/steve/Desktop/Python/marketforce_code/robot_A2')
sys.path.append('C:/Users/steve/Desktop/Python/marketforce_code/robot_B')
sys.path.append('C:/Users/steve/Desktop/Python/marketforce_code/robot_C')
sys.path.append('C:/Users/steve/Desktop/Python/marketforce_code/robot_Q')
sys.path.append('C:/Users/steve/Desktop/Python/marketforce_code/robot_R')
from modulator_A2 import modulator_A2
from modulator_B import modulator_B
from modulator_C import modulator_C
from modulator_Q import modulator_Q
from modulator_R import modulator_R
from time import sleep
import datetime
import threading
import re

##NOTE: IF YOU NEED TO ADD A NEW CAMPAIGN TO THE FINAL ROW:
##
## (1) ADD THE APPROPRIATE ELMENTS IN:
## "campaign stuff"
## "status stuff"
## "a2 stuff"
## "b stuff"
## "c stuff"
## "r stuff"
## "q stuff"
##
## AND:
## (2) ADD THE APPROPRIATE RUN GATES (SEARCH FOR "run(self)")
##
## AND:
## (3) EDIT THE REGEX READ FUNCTIONS IN CAMPAIGNS() CLASS
##
## BE ADVISED THAT DOING ANYTHING OTHER THAN ADDING NEW CAMPAIGNS TO THE LAST ROW WILL ALSO REQUIRE 
## REINDEXING THE A2_results[0] --> A2_results[2], B_results[2] --> B_results[4], etc.
##
## IF YOU NEED TO EDIT CAMPAIGN SETTINGS, EDIT THE SETTINGS.TXT VARIABLE DIRECTLY 



#Aux class
class Campaigns():
	def __init__(self):
		#open settings
		f=open('campaign_settings.txt','r')
		f_content = f.read()

		#make list of names
		result = re.search('CAMPAIGNS:(.*)\n',f_content)
		self.names = result.group(1).split(",")

		#make list of usernames
		linked_usernames = []
		for name in self.names:
			result = re.search('%s.linked_username:(.*)\n'%(name),f_content)
			linked_usernames.append(result.group(1))
		self.linked_usernames = linked_usernames

		#make list of passwords
		linked_passwords = []
		for name in self.names:
			result = re.search('%s.linked_password:(.*)\n'%(name),f_content)
			linked_passwords.append(result.group(1))
		self.linked_passwords = linked_passwords

		#make list of spreads
		spread_names = []
		for name in self.names:
			result = re.search('%s.spread_name:(.*)\n'%(name),f_content)
			spread_names.append(result.group(1)) 
		self.spread_names = spread_names

		#make list of sheets
		sheet_names = []
		for name in self.names:
			result = re.search('%s.sheet_name:(.*)\n'%(name),f_content)
			sheet_names.append(result.group(1))
		self.sheet_names = sheet_names

		#make list of aux spreads
		aux_spreads = []
		for name in self.names:
			result = re.search('%s.aux_spreads:(.*)\n'%(name),f_content)
			aux_spreads.append(result.group(1))
		self.aux_spreads = aux_spreads	

		#make list of A2 results
		A2_results = []
		for name in self.names:
			result = re.search('%s.A2:(.*)\n'%(name),f_content)
			A2_results.append(result.group(1))
		self.A2_results = A2_results	

		#make list of B results
		B_results = []
		for name in self.names:
			result = re.search('%s.B:(.*)\n'%(name),f_content)
			B_results.append(result.group(1))
		self.B_results = B_results	

		#make list of C results
		C_results = []
		for name in self.names:
			result = re.search('%s.C:(.*)\n'%(name),f_content)
			C_results.append(result.group(1))
		self.C_results = C_results

		#make list of R results
		R_results = []
		for name in self.names:
			result = re.search('%s.R:(.*)\n'%(name),f_content)
			R_results.append(result.group(1))
		self.R_results = R_results

		#make list of Q results
		Q_results = []
		for name in self.names:
			result = re.search('%s.Q:(.*)\n'%(name),f_content)
			Q_results.append(result.group(1))
		self.Q_results = Q_results

		#get starttime
		result=re.search('starttime:(.*)\n',f_content)
		self.starttime = result.group(1)

		#get endtime
		result=re.search('endtime:(.*)\n',f_content)
		self.endtime = result.group(1)

		#servitors
		servitors = []
		for name in self.names:
			result = re.search('%s.servitor:(.*)\n'%(name),f_content)
			servitors.append(result.group(1))
		self.servitors = servitors		

		#servitor_fnames
		servitor_fnames = []
		for name in self.names:
			result = re.search('%s.servitor_fname:(.*)\n'%(name),f_content)
			servitor_fnames.append(result.group(1))
		self.servitor_fnames = servitor_fnames

		#m2s
		m2s=[]
		for name in self.names:	
			result = re.search('%s.m2:(.*)\n'%(name),f_content)
			m2s.append(result.group(1))
		self.m2s = m2s

		#m3s	
		m3s=[]
		for name in self.names:	
			result = re.search('%s.m3:(.*)\n'%(name),f_content)
			m3s.append(result.group(1))
		self.m3s = m3s



class Lida():
	def __init__(self):
		#General variables
		self.location_cd = "C:/Users/steve/Downloads/chromedriver.exe"
		self.linked_login_url = "https://www.linkedin.com/uas/login?"
		self.linked_connections_url = "https://www.linkedin.com/mynetwork/invite-connect/connections/"
		self.linked_messages_url = 'https://www.linkedin.com/messaging/'
		self.campaigns = Campaigns()
		self.active_login = 'https://www.activecampaign.com/login/'


		#Tkinter Variables
			#root variables
		self.width=1000
		self.height=600
		self.root = Tk()
		self.root.title("LIDA")
		self.MainWindow = Canvas(self.root,width=self.width,height=self.height)
		self.MainWindow.pack()

			#title variables
		self.label_Campaigns = Label(self.MainWindow,text="Campaigns")
		self.label_Campaigns.config(font=("Courier", 14))
		self.MainWindow.create_window(self.width*0.1,self.height*0.1,window=self.label_Campaigns)

		self.label_Status = Label(self.MainWindow,text="Status")
		self.label_Status.config(font=("Courier", 14))
		self.MainWindow.create_window(self.width*0.2,self.height*0.1,window=self.label_Status)

		self.label_A2 = Label(self.MainWindow,text="A2")
		self.label_A2.config(font=("Courier", 14))
		self.MainWindow.create_window(self.width*0.3,self.height*0.1,window=self.label_A2)

		self.label_B = Label(self.MainWindow,text="B")
		self.label_B.config(font=("Courier", 14))
		self.MainWindow.create_window(self.width*0.4,self.height*0.1,window=self.label_B)

		self.label_C = Label(self.MainWindow,text="C")
		self.label_C.config(font=("Courier", 14))
		self.MainWindow.create_window(self.width*0.5,self.height*0.1,window=self.label_C)

		self.label_R = Label(self.MainWindow,text="R")
		self.label_R.config(font=("Courier", 14))
		self.MainWindow.create_window(self.width*0.6,self.height*0.1,window=self.label_R)

		self.label_Q = Label(self.MainWindow,text="Q")
		self.label_Q.config(font=("Courier", 14))
		self.MainWindow.create_window(self.width*0.7,self.height*0.1,window=self.label_Q)

			#campaign stuff
		self.label_MF1_ = Label(self.MainWindow,text="_MF1_")
		self.label_MF1_.config(font=("Courier", 14))
		self.MainWindow.create_window(self.width*0.1,self.height*0.2,window=self.label_MF1_)

		self.label_MF2_ = Label(self.MainWindow,text="_MF2_")
		self.label_MF2_.config(font=("Courier", 14))
		self.MainWindow.create_window(self.width*0.1,self.height*0.3,window=self.label_MF2_)

		self.label_MF3_ = Label(self.MainWindow,text="_MF3_")
		self.label_MF3_.config(font=("Courier", 14))
		self.MainWindow.create_window(self.width*0.1,self.height*0.4,window=self.label_MF3_)

		self.label_MF4_ = Label(self.MainWindow,text="_MF4_")
		self.label_MF4_.config(font=("Courier", 14))
		self.MainWindow.create_window(self.width*0.1,self.height*0.5,window=self.label_MF4_)

		self.label_ariLID1_ = Label(self.MainWindow,text="_ariLID1_")
		self.label_ariLID1_.config(font=("Courier", 14))
		self.MainWindow.create_window(self.width*0.1,self.height*0.6,window=self.label_ariLID1_)

		self.label_MF5_ = Label(self.MainWindow,text="_MF5_")
		self.label_MF5_.config(font=("Courier", 14))
		self.MainWindow.create_window(self.width*0.1,self.height*0.7,window=self.label_MF5_)

			#status stuff
		self.v_status_MF1_ = tk.IntVar(value=1)
		self.off_status_MF1_ = Radiobutton(self.MainWindow,text="off",variable=self.v_status_MF1_,value=0)
		self.on_status_MF1_ = Radiobutton(self.MainWindow,text="on",variable=self.v_status_MF1_,value=1)
		self.MainWindow.create_window(self.width*0.18,self.height*0.2,window=self.off_status_MF1_)
		self.MainWindow.create_window(self.width*0.23,self.height*0.2,window=self.on_status_MF1_)


		self.v_status_MF2_ = tk.IntVar(value=1)
		self.off_status_MF2_ = Radiobutton(self.MainWindow,text="off",variable=self.v_status_MF2_,value=0)
		self.on_status_MF2_ = Radiobutton(self.MainWindow,text="on",variable=self.v_status_MF2_,value=1)
		self.MainWindow.create_window(self.width*0.18,self.height*0.3,window=self.off_status_MF2_)
		self.MainWindow.create_window(self.width*0.23,self.height*0.3,window=self.on_status_MF2_)

		self.v_status_MF3_ = tk.IntVar(value=1)
		self.off_status_MF3_ = Radiobutton(self.MainWindow,text="off",variable=self.v_status_MF3_,value=0)
		self.on_status_MF3_ = Radiobutton(self.MainWindow,text="on",variable=self.v_status_MF3_,value=1)
		self.MainWindow.create_window(self.width*0.18,self.height*0.4,window=self.off_status_MF3_)
		self.MainWindow.create_window(self.width*0.23,self.height*0.4,window=self.on_status_MF3_)		

		self.v_status_MF4_ = tk.IntVar(value=1)
		self.off_status_MF4_ = Radiobutton(self.MainWindow,text="off",variable=self.v_status_MF4_,value=0)
		self.on_status_MF4_ = Radiobutton(self.MainWindow,text="on",variable=self.v_status_MF4_,value=1)
		self.MainWindow.create_window(self.width*0.18,self.height*0.5,window=self.off_status_MF4_)
		self.MainWindow.create_window(self.width*0.23,self.height*0.5,window=self.on_status_MF4_)
		
		self.v_status_ariLID1_ = tk.IntVar(value=1)
		self.off_status_ariLID1_ = Radiobutton(self.MainWindow,text="off",variable=self.v_status_ariLID1_,value=0)
		self.on_status_ariLID1_ = Radiobutton(self.MainWindow,text="on",variable=self.v_status_ariLID1_,value=1)
		self.MainWindow.create_window(self.width*0.18,self.height*0.6,window=self.off_status_ariLID1_)
		self.MainWindow.create_window(self.width*0.23,self.height*0.6,window=self.on_status_ariLID1_)

		self.v_status_MF5_ = tk.IntVar(value=1)
		self.off_status_MF5_ = Radiobutton(self.MainWindow,text="off",variable=self.v_status_MF5_,value=0)
		self.on_status_MF5_ = Radiobutton(self.MainWindow,text="on",variable=self.v_status_MF5_,value=1)
		self.MainWindow.create_window(self.width*0.18,self.height*0.7,window=self.off_status_MF5_)
		self.MainWindow.create_window(self.width*0.23,self.height*0.7,window=self.on_status_MF5_)

			#A2 stuff

				#A2 - _MF1_
		self.v_A2_MF1_ = tk.IntVar(value=0)
		self.ckbutton_A2_MF1_ = Checkbutton(self.MainWindow,variable=self.v_A2_MF1_)
		self.MainWindow.create_window(self.width*0.3,self.height*0.2,window=self.ckbutton_A2_MF1_)
		self.canvas_A2_MF1_ = Canvas(self.MainWindow,width=10,height=10)
		if self.campaigns.A2_results[0]=='off':
			fill='black'
		elif self.campaigns.A2_results[0]=='bad':
			fill='red'
		elif self.campaigns.A2_results[0]=='good':
			fill='green2'
		self.canvas_A2_MF1_.create_oval(2,2,10,10,fill=fill)
		self.MainWindow.create_window(self.width*0.32,self.height*0.2,window=self.canvas_A2_MF1_)

				#A2 - _MF2_
		self.v_A2_MF2_ = tk.IntVar(value=0)
		self.ckbutton_A2_MF2_ = Checkbutton(self.MainWindow,variable=self.v_A2_MF2_)
		self.MainWindow.create_window(self.width*0.3,self.height*0.3,window=self.ckbutton_A2_MF2_)
		self.canvas_A2_MF2_ = Canvas(self.MainWindow,width=10,height=10)
		if self.campaigns.A2_results[1]=='off':
			fill='black'
		elif self.campaigns.A2_results[1]=='bad':
			fill='red'
		elif self.campaigns.A2_results[1]=='good':
			fill='green2'
		self.canvas_A2_MF2_.create_oval(2,2,10,10,fill=fill)
		self.MainWindow.create_window(self.width*0.32,self.height*0.3,window=self.canvas_A2_MF2_)		

				#A2 - _MF3_
		self.v_A2_MF3_ = tk.IntVar(value=1)
		self.ckbutton_A2_MF3_ = Checkbutton(self.MainWindow,variable=self.v_A2_MF3_)
		self.MainWindow.create_window(self.width*0.3,self.height*0.4,window=self.ckbutton_A2_MF3_)
		self.canvas_A2_MF3_ = Canvas(self.MainWindow,width=10,height=10)
		if self.campaigns.A2_results[2]=='off':
			fill='black'
		elif self.campaigns.A2_results[2]=='bad':
			fill='red'
		elif self.campaigns.A2_results[2]=='good':
			fill='green2'
		self.canvas_A2_MF3_.create_oval(2,2,10,10,fill=fill)
		self.MainWindow.create_window(self.width*0.32,self.height*0.4,window=self.canvas_A2_MF3_)

				#A2 - _MF4_
		self.v_A2_MF4_ = tk.IntVar(value=1)
		self.ckbutton_A2_MF4_ = Checkbutton(self.MainWindow,variable=self.v_A2_MF4_)
		self.MainWindow.create_window(self.width*0.3,self.height*0.5,window=self.ckbutton_A2_MF4_)
		self.canvas_A2_MF4_ = Canvas(self.MainWindow,width=10,height=10)
		if self.campaigns.A2_results[3]=='off':
			fill='black'
		elif self.campaigns.A2_results[3]=='bad':
			fill='red'
		elif self.campaigns.A2_results[3]=='good':
			fill='green2'
		self.canvas_A2_MF4_.create_oval(2,2,10,10,fill=fill)
		self.MainWindow.create_window(self.width*0.32,self.height*0.5,window=self.canvas_A2_MF4_)		


				#A2 - _ariLID1_
		self.v_A2_ariLID1_ = tk.IntVar(value=1)
		self.ckbutton_A2_ariLID1_ = Checkbutton(self.MainWindow,variable=self.v_A2_ariLID1_)
		self.MainWindow.create_window(self.width*0.3,self.height*0.6,window=self.ckbutton_A2_ariLID1_)
		self.canvas_A2_ariLID1_ = Canvas(self.MainWindow,width=10,height=10)
		if self.campaigns.A2_results[4]=='off':
			fill='black'
		elif self.campaigns.A2_results[4]=='bad':
			fill='red'
		elif self.campaigns.A2_results[4]=='good':
			fill='green2'
		self.canvas_A2_ariLID1_.create_oval(2,2,10,10,fill=fill)
		self.MainWindow.create_window(self.width*0.32,self.height*0.6,window=self.canvas_A2_ariLID1_)


				#A2 - _MF5_
		self.v_A2_MF5_ = tk.IntVar(value=1)
		self.ckbutton_A2_MF5_ = Checkbutton(self.MainWindow,variable=self.v_A2_MF5_)
		self.MainWindow.create_window(self.width*0.3,self.height*0.7,window=self.ckbutton_A2_MF5_)
		self.canvas_A2_MF5_ = Canvas(self.MainWindow,width=10,height=10)
		if self.campaigns.A2_results[4]=='off':
			fill='black'
		elif self.campaigns.A2_results[4]=='bad':
			fill='red'
		elif self.campaigns.A2_results[4]=='good':
			fill='green2'
		self.canvas_A2_MF5_.create_oval(2,2,10,10,fill=fill)
		self.MainWindow.create_window(self.width*0.32,self.height*0.7,window=self.canvas_A2_ariLID1_)			
						
			#B stuff

				#B - _MF1_
		self.v_B_MF1_ = tk.IntVar(value=1)
		self.ckbutton_B_MF1_ = Checkbutton(self.MainWindow,variable=self.v_B_MF1_)
		self.MainWindow.create_window(self.width*0.4,self.height*0.2,window=self.ckbutton_B_MF1_)
		self.canvas_B_MF1_ = Canvas(self.MainWindow,width=10,height=10)
		if self.campaigns.B_results[0]=='off':
			fill='black'
		elif self.campaigns.B_results[0]=='bad':
			fill='red'
		elif self.campaigns.B_results[0]=='good':
			fill='green2'
		self.canvas_B_MF1_.create_oval(2,2,10,10,fill=fill)
		self.MainWindow.create_window(self.width*0.42,self.height*0.2,window=self.canvas_B_MF1_)

				#B - _MF2_
		self.v_B_MF2_ = tk.IntVar(value=1)
		self.ckbutton_B_MF2_ = Checkbutton(self.MainWindow,variable=self.v_B_MF2_)
		self.MainWindow.create_window(self.width*0.4,self.height*0.3,window=self.ckbutton_B_MF2_)
		self.canvas_B_MF2_ = Canvas(self.MainWindow,width=10,height=10)
		if self.campaigns.B_results[1]=='off':
			fill='black'
		elif self.campaigns.B_results[1]=='bad':
			fill='red'
		elif self.campaigns.B_results[1]=='good':
			fill='green2'
		self.canvas_B_MF2_.create_oval(2,2,10,10,fill=fill)
		self.MainWindow.create_window(self.width*0.42,self.height*0.3,window=self.canvas_B_MF2_)		

				#B - _MF3_
		self.v_B_MF3_ = tk.IntVar(value=1)
		self.ckbutton_B_MF3_ = Checkbutton(self.MainWindow,variable=self.v_B_MF3_)
		self.MainWindow.create_window(self.width*0.4,self.height*0.4,window=self.ckbutton_B_MF3_)
		self.canvas_B_MF3_ = Canvas(self.MainWindow,width=10,height=10)
		if self.campaigns.B_results[2]=='off':
			fill='black'
		elif self.campaigns.B_results[2]=='bad':
			fill='red'
		elif self.campaigns.B_results[2]=='good':
			fill='green2'
		self.canvas_B_MF3_.create_oval(2,2,10,10,fill=fill)
		self.MainWindow.create_window(self.width*0.42,self.height*0.4,window=self.canvas_B_MF3_)

				#B - _MF4_
		self.v_B_MF4_ = tk.IntVar(value=1)
		self.ckbutton_B_MF4_ = Checkbutton(self.MainWindow,variable=self.v_B_MF4_)
		self.MainWindow.create_window(self.width*0.4,self.height*0.5,window=self.ckbutton_B_MF4_)
		self.canvas_B_MF4_ = Canvas(self.MainWindow,width=10,height=10)
		if self.campaigns.B_results[3]=='off':
			fill='black'
		elif self.campaigns.B_results[3]=='bad':
			fill='red'
		elif self.campaigns.B_results[3]=='good':
			fill='green2'
		self.canvas_B_MF4_.create_oval(2,2,10,10,fill=fill)
		self.MainWindow.create_window(self.width*0.42,self.height*0.5,window=self.canvas_B_MF4_)		


				#B - _ariLID1_
		self.v_B_ariLID1_ = tk.IntVar(value=1)
		self.ckbutton_B_ariLID1_ = Checkbutton(self.MainWindow,variable=self.v_B_ariLID1_)
		self.MainWindow.create_window(self.width*0.4,self.height*0.6,window=self.ckbutton_B_ariLID1_)
		self.canvas_B_ariLID1_ = Canvas(self.MainWindow,width=10,height=10)
		if self.campaigns.B_results[4]=='off':
			fill='black'
		elif self.campaigns.B_results[4]=='bad':
			fill='red'
		elif self.campaigns.B_results[4]=='good':
			fill='green2'
		self.canvas_B_ariLID1_.create_oval(2,2,10,10,fill=fill)
		self.MainWindow.create_window(self.width*0.42,self.height*0.6,window=self.canvas_B_ariLID1_)				


				#B - _MF5_
		self.v_B_MF5_ = tk.IntVar(value=1)
		self.ckbutton_B_MF5_ = Checkbutton(self.MainWindow,variable=self.v_B_MF5_)
		self.MainWindow.create_window(self.width*0.4,self.height*0.7,window=self.ckbutton_B_MF5_)
		self.canvas_B_MF5_ = Canvas(self.MainWindow,width=10,height=10)
		if self.campaigns.B_results[4]=='off':
			fill='black'
		elif self.campaigns.B_results[4]=='bad':
			fill='red'
		elif self.campaigns.B_results[4]=='good':
			fill='green2'
		self.canvas_B_ariLID1_.create_oval(2,2,10,10,fill=fill)
		self.MainWindow.create_window(self.width*0.42,self.height*0.7,window=self.canvas_B_MF5_)			

			#C stuff

				#C - _MF1_
		self.v_C_MF1_ = tk.IntVar(value=1)
		self.ckbutton_C_MF1_ = Checkbutton(self.MainWindow,variable=self.v_C_MF1_)
		self.MainWindow.create_window(self.width*0.5,self.height*0.2,window=self.ckbutton_C_MF1_)
		self.canvas_C_MF1_ = Canvas(self.MainWindow,width=10,height=10)
		if self.campaigns.C_results[0]=='off':
			fill='black'
		elif self.campaigns.C_results[0]=='bad':
			fill='red'
		elif self.campaigns.C_results[0]=='good':
			fill='green2'
		self.canvas_C_MF1_.create_oval(2,2,10,10,fill=fill)
		self.MainWindow.create_window(self.width*0.52,self.height*0.2,window=self.canvas_C_MF1_)

				#C - _MF2_
		self.v_C_MF2_ = tk.IntVar(value=1)
		self.ckbutton_C_MF2_ = Checkbutton(self.MainWindow,variable=self.v_C_MF2_)
		self.MainWindow.create_window(self.width*0.5,self.height*0.3,window=self.ckbutton_C_MF2_)
		self.canvas_C_MF2_ = Canvas(self.MainWindow,width=10,height=10)
		if self.campaigns.C_results[1]=='off':
			fill='black'
		elif self.campaigns.C_results[1]=='bad':
			fill='red'
		elif self.campaigns.C_results[1]=='good':
			fill='green2'
		self.canvas_C_MF2_.create_oval(2,2,10,10,fill=fill)
		self.MainWindow.create_window(self.width*0.52,self.height*0.3,window=self.canvas_C_MF2_)		

				#C - _MF3_
		self.v_C_MF3_ = tk.IntVar(value=1)
		self.ckbutton_C_MF3_ = Checkbutton(self.MainWindow,variable=self.v_C_MF3_)
		self.MainWindow.create_window(self.width*0.5,self.height*0.4,window=self.ckbutton_C_MF3_)
		self.canvas_C_MF3_ = Canvas(self.MainWindow,width=10,height=10)
		if self.campaigns.C_results[2]=='off':
			fill='black'
		elif self.campaigns.C_results[2]=='bad':
			fill='red'
		elif self.campaigns.C_results[2]=='good':
			fill='green2'
		self.canvas_C_MF3_.create_oval(2,2,10,10,fill=fill)
		self.MainWindow.create_window(self.width*0.52,self.height*0.4,window=self.canvas_C_MF3_)

				#C - _MF4_
		self.v_C_MF4_ = tk.IntVar(value=1)
		self.ckbutton_C_MF4_ = Checkbutton(self.MainWindow,variable=self.v_C_MF4_)
		self.MainWindow.create_window(self.width*0.5,self.height*0.5,window=self.ckbutton_C_MF4_)
		self.canvas_C_MF4_ = Canvas(self.MainWindow,width=10,height=10)
		if self.campaigns.C_results[3]=='off':
			fill='black'
		elif self.campaigns.C_results[3]=='bad':
			fill='red'
		elif self.campaigns.C_results[3]=='good':
			fill='green2'
		self.canvas_C_MF4_.create_oval(2,2,10,10,fill=fill)
		self.MainWindow.create_window(self.width*0.52,self.height*0.5,window=self.canvas_C_MF4_)		


				#C - _ariLID1_
		self.v_C_ariLID1_ = tk.IntVar(value=1)
		self.ckbutton_C_ariLID1_ = Checkbutton(self.MainWindow,variable=self.v_C_ariLID1_)
		self.MainWindow.create_window(self.width*0.5,self.height*0.6,window=self.ckbutton_C_ariLID1_)
		self.canvas_C_ariLID1_ = Canvas(self.MainWindow,width=10,height=10)
		if self.campaigns.C_results[4]=='off':
			fill='black'
		elif self.campaigns.C_results[4]=='bad':
			fill='red'
		elif self.campaigns.C_results[4]=='good':
			fill='green2'
		self.canvas_C_ariLID1_.create_oval(2,2,10,10,fill=fill)
		self.MainWindow.create_window(self.width*0.52,self.height*0.6,window=self.canvas_C_ariLID1_)

				#C - _MF5_
		self.v_C_MF5_ = tk.IntVar(value=1)
		self.ckbutton_C_MF5_ = Checkbutton(self.MainWindow,variable=self.v_C_MF5_)
		self.MainWindow.create_window(self.width*0.5,self.height*0.7,window=self.ckbutton_C_MF5_)
		self.canvas_C_MF5_ = Canvas(self.MainWindow,width=10,height=10)
		if self.campaigns.C_results[4]=='off':
			fill='black'
		elif self.campaigns.C_results[4]=='bad':
			fill='red'
		elif self.campaigns.C_results[4]=='good':
			fill='green2'
		self.canvas_C_MF5_.create_oval(2,2,10,10,fill=fill)
		self.MainWindow.create_window(self.width*0.52,self.height*0.7,window=self.canvas_C_MF5_)	

			#R stuff

				#R - _MF1_
		self.v_R_MF1_ = tk.IntVar(value=0)
		self.ckbutton_R_MF1_ = Checkbutton(self.MainWindow,variable=self.v_R_MF1_)
		self.MainWindow.create_window(self.width*0.6,self.height*0.2,window=self.ckbutton_R_MF1_)
		self.canvas_R_MF1_ = Canvas(self.MainWindow,width=10,height=10)
		if self.campaigns.R_results[0]=='off':
			fill='black'
		elif self.campaigns.R_results[0]=='bad':
			fill='red'
		elif self.campaigns.R_results[0]=='good':
			fill='green2'
		self.canvas_R_MF1_.create_oval(2,2,10,10,fill=fill)
		self.MainWindow.create_window(self.width*0.62,self.height*0.2,window=self.canvas_R_MF1_)

				#R - _MF2_
		self.v_R_MF2_ = tk.IntVar(value=0)
		self.ckbutton_R_MF2_ = Checkbutton(self.MainWindow,variable=self.v_R_MF2_)
		self.MainWindow.create_window(self.width*0.6,self.height*0.3,window=self.ckbutton_R_MF2_)
		self.canvas_R_MF2_ = Canvas(self.MainWindow,width=10,height=10)
		if self.campaigns.R_results[1]=='off':
			fill='black'
		elif self.campaigns.R_results[1]=='bad':
			fill='red'
		elif self.campaigns.R_results[1]=='good':
			fill='green2'
		self.canvas_R_MF2_.create_oval(2,2,10,10,fill=fill)
		self.MainWindow.create_window(self.width*0.62,self.height*0.3,window=self.canvas_R_MF2_)		

				#R - _MF3_
		self.v_R_MF3_ = tk.IntVar(value=0)
		self.ckbutton_R_MF3_ = Checkbutton(self.MainWindow,variable=self.v_R_MF3_)
		self.MainWindow.create_window(self.width*0.6,self.height*0.4,window=self.ckbutton_R_MF3_)
		self.canvas_R_MF3_ = Canvas(self.MainWindow,width=10,height=10)
		if self.campaigns.R_results[2]=='off':
			fill='black'
		elif self.campaigns.R_results[2]=='bad':
			fill='red'
		elif self.campaigns.R_results[2]=='good':
			fill='green2'
		self.canvas_R_MF3_.create_oval(2,2,10,10,fill=fill)
		self.MainWindow.create_window(self.width*0.62,self.height*0.4,window=self.canvas_R_MF3_)

				#R - _MF4_
		self.v_R_MF4_ = tk.IntVar(value=0)
		self.ckbutton_R_MF4_ = Checkbutton(self.MainWindow,variable=self.v_R_MF4_)
		self.MainWindow.create_window(self.width*0.6,self.height*0.5,window=self.ckbutton_R_MF4_)
		self.canvas_R_MF4_ = Canvas(self.MainWindow,width=10,height=10)
		if self.campaigns.R_results[3]=='off':
			fill='black'
		elif self.campaigns.R_results[3]=='bad':
			fill='red'
		elif self.campaigns.R_results[3]=='good':
			fill='green2'
		self.canvas_R_MF4_.create_oval(2,2,10,10,fill=fill)
		self.MainWindow.create_window(self.width*0.62,self.height*0.5,window=self.canvas_R_MF4_)		


				#R - _ariLID1_
		self.v_R_ariLID1_ = tk.IntVar(value=1)
		self.ckbutton_R_ariLID1_ = Checkbutton(self.MainWindow,variable=self.v_R_ariLID1_)
		self.MainWindow.create_window(self.width*0.6,self.height*0.6,window=self.ckbutton_R_ariLID1_)
		self.canvas_R_ariLID1_ = Canvas(self.MainWindow,width=10,height=10)
		if self.campaigns.R_results[4]=='off':
			fill='black'
		elif self.campaigns.R_results[4]=='bad':
			fill='red'
		elif self.campaigns.R_results[4]=='good':
			fill='green2'
		self.canvas_R_ariLID1_.create_oval(2,2,10,10,fill=fill)
		self.MainWindow.create_window(self.width*0.62,self.height*0.6,window=self.canvas_R_ariLID1_)	


				#R - _MF5_
		self.v_R_MF5_ = tk.IntVar(value=1)
		self.ckbutton_R_MF5_ = Checkbutton(self.MainWindow,variable=self.v_R_MF5_)
		self.MainWindow.create_window(self.width*0.6,self.height*0.7,window=self.ckbutton_R_MF5_)
		self.canvas_R_MF5_ = Canvas(self.MainWindow,width=10,height=10)
		if self.campaigns.R_results[4]=='off':
			fill='black'
		elif self.campaigns.R_results[4]=='bad':
			fill='red'
		elif self.campaigns.R_results[4]=='good':
			fill='green2'
		self.canvas_R_MF5_.create_oval(2,2,10,10,fill=fill)
		self.MainWindow.create_window(self.width*0.62,self.height*0.7,window=self.canvas_R_MF5_)	

			#Q stuff	

				#Q - _MF1_
		self.v_Q_MF1_ = tk.IntVar(value=0)
		self.ckbutton_Q_MF1_ = Checkbutton(self.MainWindow,variable=self.v_Q_MF1_)
		self.MainWindow.create_window(self.width*0.7,self.height*0.2,window=self.ckbutton_Q_MF1_)
		self.canvas_Q_MF1_ = Canvas(self.MainWindow,width=10,height=10)
		if self.campaigns.Q_results[0]=='off':
			fill='black'
		elif self.campaigns.Q_results[0]=='bad':
			fill='red'
		elif self.campaigns.Q_results[0]=='good':
			fill='green2'
		self.canvas_Q_MF1_.create_oval(2,2,10,10,fill=fill)
		self.MainWindow.create_window(self.width*0.72,self.height*0.2,window=self.canvas_Q_MF1_)

				#Q - _MF2_
		self.v_Q_MF2_ = tk.IntVar(value=0)
		self.ckbutton_Q_MF2_ = Checkbutton(self.MainWindow,variable=self.v_Q_MF2_)
		self.MainWindow.create_window(self.width*0.7,self.height*0.3,window=self.ckbutton_Q_MF2_)
		self.canvas_Q_MF2_ = Canvas(self.MainWindow,width=10,height=10)
		if self.campaigns.Q_results[1]=='off':
			fill='black'
		elif self.campaigns.Q_results[1]=='bad':
			fill='red'
		elif self.campaigns.Q_results[1]=='good':
			fill='green2'
		self.canvas_Q_MF2_.create_oval(2,2,10,10,fill=fill)
		self.MainWindow.create_window(self.width*0.72,self.height*0.3,window=self.canvas_Q_MF2_)		

				#Q - _MF3_
		self.v_Q_MF3_ = tk.IntVar(value=0)
		self.ckbutton_Q_MF3_ = Checkbutton(self.MainWindow,variable=self.v_Q_MF3_)
		self.MainWindow.create_window(self.width*0.7,self.height*0.4,window=self.ckbutton_Q_MF3_)
		self.canvas_Q_MF3_ = Canvas(self.MainWindow,width=10,height=10)
		if self.campaigns.Q_results[2]=='off':
			fill='black'
		elif self.campaigns.Q_results[2]=='bad':
			fill='red'
		elif self.campaigns.Q_results[2]=='good':
			fill='green2'
		self.canvas_Q_MF3_.create_oval(2,2,10,10,fill=fill)
		self.MainWindow.create_window(self.width*0.72,self.height*0.4,window=self.canvas_Q_MF3_)

				#Q - _MF4_
		self.v_Q_MF4_ = tk.IntVar(value=0)
		self.ckbutton_Q_MF4_ = Checkbutton(self.MainWindow,variable=self.v_Q_MF4_)
		self.MainWindow.create_window(self.width*0.7,self.height*0.5,window=self.ckbutton_Q_MF4_)
		self.canvas_Q_MF4_ = Canvas(self.MainWindow,width=10,height=10)
		if self.campaigns.Q_results[3]=='off':
			fill='black'
		elif self.campaigns.Q_results[3]=='bad':
			fill='red'
		elif self.campaigns.Q_results[3]=='good':
			fill='green2'
		self.canvas_Q_MF4_.create_oval(2,2,10,10,fill=fill)
		self.MainWindow.create_window(self.width*0.72,self.height*0.5,window=self.canvas_Q_MF4_)		


				#Q - _ariLID1_
		self.v_Q_ariLID1_ = tk.IntVar(value=0)
		self.ckbutton_Q_ariLID1_ = Checkbutton(self.MainWindow,variable=self.v_Q_ariLID1_)
		self.MainWindow.create_window(self.width*0.7,self.height*0.6,window=self.ckbutton_Q_ariLID1_)
		self.canvas_Q_ariLID1_ = Canvas(self.MainWindow,width=10,height=10)
		if self.campaigns.Q_results[4]=='off':
			fill='black'
		elif self.campaigns.Q_results[4]=='bad':
			fill='red'
		elif self.campaigns.Q_results[4]=='good':
			fill='green2'
		self.canvas_Q_ariLID1_.create_oval(2,2,10,10,fill=fill)
		self.MainWindow.create_window(self.width*0.72,self.height*0.6,window=self.canvas_Q_ariLID1_)


				#Q - _MF5_
		self.v_Q_MF5_ = tk.IntVar(value=0)
		self.ckbutton_Q_MF5_ = Checkbutton(self.MainWindow,variable=self.v_Q_MF5_)
		self.MainWindow.create_window(self.width*0.7,self.height*0.7,window=self.ckbutton_Q_MF5_)
		self.canvas_Q_MF5_ = Canvas(self.MainWindow,width=10,height=10)
		if self.campaigns.Q_results[4]=='off':
			fill='black'
		elif self.campaigns.Q_results[4]=='bad':
			fill='red'
		elif self.campaigns.Q_results[4]=='good':
			fill='green2'
		self.canvas_Q_MF5_.create_oval(2,2,10,10,fill=fill)
		self.MainWindow.create_window(self.width*0.72,self.height*0.7,window=self.canvas_Q_MF5_)

		#Buttons
		self.abort_button = Button(self.MainWindow,text='Abort',command=lambda:sys.exit())
		self.run_button = Button(self.MainWindow,text='Run',command=lambda:self.daemon.start())
		self.MainWindow.create_window(self.width*0.4,self.height*0.9,window=self.abort_button)
		self.MainWindow.create_window(self.width*0.5,self.height*0.9,window=self.run_button)		


		self.daemon = threading.Thread(target=self.run,daemon=True)
		self.root.mainloop()

	def run(self):
		while True:
			curr_time = int(datetime.datetime.now().strftime("%H"))
			err = 0

			if curr_time >= int(self.campaigns.starttime) and curr_time < int(self.campaigns.endtime):
				errmsg: 'Err: '


				
				#_MF1_ gates
				if self.v_status_MF1_.get() == 1:
					print('_MF1_ follows:')

					try: #A
						if self.v_A2_MF1_.get() == 1:
							print('A2 is go.')
							modulator_A2(mainspread=self.campaigns.spread_names[0],mainsheet=self.campaigns.sheet_names[0],auxiliaryspread=self.campaigns.aux_spreads[0])

						#B
						if self.v_B_MF1_.get() == 1:
							modulator_B(self=self,campaign=self.campaigns.names[0],linked_username=self.campaigns.linked_usernames[0],linked_password=self.campaigns.linked_passwords[0],spread_name=self.campaigns.spread_names[0],sheet_name=self.campaigns.sheet_names[0])
						
						#C
						if self.v_C_MF1_.get() == 1:
							print('C is go.')
							modulator_C(self=self,campaign=self.campaigns.names[0],linked_username=self.campaigns.linked_usernames[0],linked_password=self.campaigns.linked_passwords[0],spread_name=self.campaigns.spread_names[0],sheet_name=self.campaigns.sheet_names[0],servitor=self.campaigns.servitors[0],servitor_fname=self.campaigns.servitor_fnames[0])
						
						#R
						if self.v_R_MF1_.get() == 1:
							print('R is go.')
							modulator_R(self=self,campaign=self.campaigns.names[0],user=self.campaigns.linked_usernames[0],password=self.campaigns.linked_passwords[0],spread_name=self.campaigns.spread_names[0],sheet_name=self.campaigns.sheet_names[0],servitor=self.campaigns.servitors[0],servitor_fname=self.campaigns.servitor_fnames[0],m2_body=self.campaigns.m2s[0],m3_body=self.campaigns.m3s[0])
						
						#Q
						if self.v_Q_MF1_.get() == 1:
							print('Q is go.')

						self.txt('_MF1_ succeeded.')
					except Exception as e:
						self.txt('_MF1_ failed: %s'%e)

				#_MF2_ gates
				if self.v_status_MF2_.get() == 1:
					print('_MF2_ follows:')

					try:
						#A2
						if self.v_A2_MF2_.get() == 1:
							print('A2 is go.')
							modulator_A2(mainspread=self.campaigns.spread_names[1],mainsheet=self.campaigns.sheet_names[1],auxiliaryspread=self.campaigns.aux_spreads[1])

						#B
						if self.v_B_MF2_.get() == 1:
							modulator_B(self=self,campaign=self.campaigns.names[1],linked_username=self.campaigns.linked_usernames[1],linked_password=self.campaigns.linked_passwords[1],spread_name=self.campaigns.spread_names[1],sheet_name=self.campaigns.sheet_names[1])
						
						#C
						if self.v_C_MF2_.get() == 1:
							print('C is go.')
							modulator_C(self=self,campaign=self.campaigns.names[1],linked_username=self.campaigns.linked_usernames[1],linked_password=self.campaigns.linked_passwords[1],spread_name=self.campaigns.spread_names[1],sheet_name=self.campaigns.sheet_names[1],servitor=self.campaigns.servitors[1],servitor_fname=self.campaigns.servitor_fnames[1])
						
						#R
						if self.v_R_MF2_.get() == 1:
							print('R is go.')
							modulator_R(self=self,campaign=self.campaigns.names[1],user=self.campaigns.linked_usernames[1],password=self.campaigns.linked_passwords[1],spread_name=self.campaigns.spread_names[1],sheet_name=self.campaigns.sheet_names[1],servitor=self.campaigns.servitors[1],servitor_fname=self.campaigns.servitor_fnames[1],m2_body=self.campaigns.m2s[1],m3_body=self.campaigns.m3s[1])

						#Q
						if self.v_Q_MF2_.get() == 1:
							print('Q is go.')

						self.txt('_MF2_ succeeded.')
					except Exception as e:
						self.txt('_MF2_ failed: %s'%e)

				#_MF3_ gates
				if self.v_status_MF3_.get() == 1:
					print('_MF3_ follows:')
					
					try:#A2
						if self.v_A2_MF3_.get() == 1:
							print('A2 is go.')
							modulator_A2(mainspread=self.campaigns.spread_names[2],mainsheet=self.campaigns.sheet_names[2],auxiliaryspread=self.campaigns.aux_spreads[2])
						
						#B
						if self.v_B_MF3_.get() == 1:
							print('B is go.')
							modulator_B(self=self,campaign=self.campaigns.names[2],linked_username=self.campaigns.linked_usernames[2],linked_password=self.campaigns.linked_passwords[2],spread_name=self.campaigns.spread_names[2],sheet_name=self.campaigns.sheet_names[2])
						#C	
						if self.v_C_MF3_.get() == 1:
							print('C is go.')
							modulator_C(self=self,campaign=self.campaigns.names[2],linked_username=self.campaigns.linked_usernames[2],linked_password=self.campaigns.linked_passwords[2],spread_name=self.campaigns.spread_names[2],sheet_name=self.campaigns.sheet_names[2],servitor=self.campaigns.servitors[2],servitor_fname=self.campaigns.servitor_fnames[2])
						#R
						if self.v_R_MF3_.get() == 1:
							print('R is go.')
							modulator_R(self=self,campaign=self.campaigns.names[2],user=self.campaigns.linked_usernames[2],password=self.campaigns.linked_passwords[2],spread_name=self.campaigns.spread_names[2],sheet_name=self.campaigns.sheet_names[2],servitor=self.campaigns.servitors[2],servitor_fname=self.campaigns.servitor_fnames[2],m2_body=self.campaigns.m2s[2],m3_body=self.campaigns.m3s[2])
						
						#Q
						if self.v_Q_MF3_.get() == 1:
							print('Q is go.')

						self.txt('_MF3_ succeeded.')
					except Exception as e:
						self.txt('_MF3_ failed: %s'%e)

				#_MF4_ gates
				if self.v_status_MF4_.get() == 1:
					print('_MF4_ follows:')

					try:#A2
						if self.v_A2_MF4_.get() == 1:
							print('A2 is go.')
							modulator_A2(mainspread=self.campaigns.spread_names[3],mainsheet=self.campaigns.sheet_names[3],auxiliaryspread=self.campaigns.aux_spreads[3])
						
						#B
						if self.v_B_MF4_.get() == 1:
							print('B is go.')
							modulator_B(self=self,campaign=self.campaigns.names[3],linked_username=self.campaigns.linked_usernames[3],linked_password=self.campaigns.linked_passwords[3],spread_name=self.campaigns.spread_names[3],sheet_name=self.campaigns.sheet_names[3])

						#C
						if self.v_C_MF4_.get() == 1:
							print('C is go.')
							modulator_C(self=self,campaign=self.campaigns.names[3],linked_username=self.campaigns.linked_usernames[3],linked_password=self.campaigns.linked_passwords[3],spread_name=self.campaigns.spread_names[3],sheet_name=self.campaigns.sheet_names[3],servitor=self.campaigns.servitors[3],servitor_fname=self.campaigns.servitor_fnames[3])

						#R
						if self.v_R_MF4_.get() == 1:
							print('R is go.')
							modulator_R(self=self,campaign=self.campaigns.names[3],user=self.campaigns.linked_usernames[3],password=self.campaigns.linked_passwords[3],spread_name=self.campaigns.spread_names[3],sheet_name=self.campaigns.sheet_names[3],servitor=self.campaigns.servitors[3],servitor_fname=self.campaigns.servitor_fnames[3],m2_body=self.campaigns.m2s[3],m3_body=self.campaigns.m3s[3])
						
						#Q
						if self.v_Q_MF4_.get() == 1:
							print('Q is go.')

						self.txt('_MF4_ succeeded')
					except Exception as e:
						self.txt('_MF4_ failed: %s'%e)

				#_ariLID1_ gates
				if self.v_status_ariLID1_.get() == 1:
					print('_ariLID1_ follows:')
					
					try:#A2
						if self.v_A2_ariLID1_.get() == 1:
							print('A2 is go.')
							modulator_A2(mainspread=self.campaigns.spread_names[4],mainsheet=self.campaigns.sheet_names[4],auxiliaryspread=self.campaigns.aux_spreads[4])
						
						#B
						if self.v_B_ariLID1_.get() == 1:
							print('B is go.')
							modulator_B(self=self,campaign=self.campaigns.names[4],linked_username=self.campaigns.linked_usernames[4],linked_password=self.campaigns.linked_passwords[4],spread_name=self.campaigns.spread_names[4],sheet_name=self.campaigns.sheet_names[4])

						#C
						if self.v_C_ariLID1_.get() == 1:
							print('C is go.')
							modulator_C(self=self,campaign=self.campaigns.names[4],linked_username=self.campaigns.linked_usernames[4],linked_password=self.campaigns.linked_passwords[4],spread_name=self.campaigns.spread_names[4],sheet_name=self.campaigns.sheet_names[4],servitor=self.campaigns.servitors[4],servitor_fname=self.campaigns.servitor_fnames[4])

						#R
						if self.v_R_ariLID1_.get() == 1:
							print('R is go.')
							modulator_R(self=self,campaign=self.campaigns.names[4],user=self.campaigns.linked_usernames[4],password=self.campaigns.linked_passwords[4],spread_name=self.campaigns.spread_names[4],sheet_name=self.campaigns.sheet_names[4],servitor=self.campaigns.servitors[4],servitor_fname=self.campaigns.servitor_fnames[4],m2_body=self.campaigns.m2s[4],m3_body=self.campaigns.m3s[4])
						
						#Q
						if self.v_Q_ariLID1_.get() == 1:
							print('Q is go.')

						self.txt('_ariLID1_ succeeded.')
					except Exception as e:
						self.txt('_ariLid1_ failed: %s'%e)

				#_MF5_ gates
				if self.v_status_MF5_.get() == 1:
					print('_MF5_ follows:')
					
					try:	#A2
						if self.v_A2_MF5_.get() == 1:
							print('A2 is go.')
							modulator_A2(mainspread=self.campaigns.spread_names[5],mainsheet=self.campaigns.sheet_names[5],auxiliaryspread=self.campaigns.aux_spreads[5])
						
						#B
						if self.v_B_MF5_.get() == 1:
							print('B is go.')
							modulator_B(self=self,campaign=self.campaigns.names[5],linked_username=self.campaigns.linked_usernames[5],linked_password=self.campaigns.linked_passwords[5],spread_name=self.campaigns.spread_names[5],sheet_name=self.campaigns.sheet_names[5])

						#C
						if self.v_C_MF5_.get() == 1:
							print('C is go.')
							modulator_C(self=self,campaign=self.campaigns.names[5],linked_username=self.campaigns.linked_usernames[5],linked_password=self.campaigns.linked_passwords[5],spread_name=self.campaigns.spread_names[5],sheet_name=self.campaigns.sheet_names[5],servitor=self.campaigns.servitors[5],servitor_fname=self.campaigns.servitor_fnames[5])

						#R
						if self.v_R_MF5_.get() == 1:
							print('R is go.')
							modulator_R(self=self,campaign=self.campaigns.names[5],user=self.campaigns.linked_usernames[5],password=self.campaigns.linked_passwords[5],spread_name=self.campaigns.spread_names[5],sheet_name=self.campaigns.sheet_names[5],servitor=self.campaigns.servitors[5],servitor_fname=self.campaigns.servitor_fnames[5],m2_body=self.campaigns.m2s[5],m3_body=self.campaigns.m3s[5])
						
						#Q
						if self.v_Q_MF5_.get() == 1:
							print('Q is go.')

						self.txt('_MF5_ succeeded')
					except Exception as e:
						self.txt('_MF5_ failed: %s'%e)

			print('Cycle complete. Next cycle will begin in 30 minutes.')
			sleep(1800)




	
	def txt(self,msg):
		client = Client("AC983906068a9d52fc5a6612fcaeccd8f9","daf93dd641db22bee793ebdf0b8ac03a")
		client.messages.create(to="+16043143827",from_="+12085180535",body=msg)





if __name__=='__main__':
	L = Lida()