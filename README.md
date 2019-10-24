# Marketforce Code


## HOW TO RUN IT
marketforce_code is designed to automate marketforce's LinkedIn-Direct-Messaging (LID) funnel. To run it on a new computer probably requires Python programming experience.:
1. Download the files 
2. Edit the Campaign_Settings.txt so the information is correct
3.   
    a.Open LIDA.py using a python script editor, such as Sublime Text (or even Notepad).
    b.Locate the following lines of code:
    ```
    class Lida():
	    def __init__(self):
    ```
    c. Underneath this line of code you will see "General Variables". Edit these as appropriate.

4.
5. Go to https://chromedriver.chromium.org/downloads and download chromedriver. Save the chromedriver.exe filepath to the General Variable you already edited in step 3c.
6. Open command line in the same directory as "lida.py"
7. Enter "python lida.py"
8. Select the campaigns you wish to run, and the modules you want to run on that campaign.
9. Hit enter to run.

## WHAT IT DOES
marketforce_code is broken into multiple modules

robot (main function)
    - robot_A2 (updates the invite list from an aux spreadsheet)
    - robot_B (checks for connection status)
    - robot_C (checks for message replies)
    - robot_Q (checks CRM for lead status)
    - robot_R (sends out messages)
    
