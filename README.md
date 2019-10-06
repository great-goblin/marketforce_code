# Marketforce Code


## HOW TO RUN IT
marketforce_code is designed to automate marketforce's LinkedIn-Direct-Messaging (LID) funnel. To run it on a new computer probably requires Python programming experience.:
1. Download the files 
2. Open robot.py (the main function)
3. Edit the SETTINGS variable so the directory information is correct. 
4. (Optional) Open all the modulator.py files (eg. modulator_A.py, modulator_B.py). Edit all the 'if campaign == '_MF1_'' data, if you desire.
5. Go to https://chromedriver.chromium.org/downloads and download chromedriver. Save the chromedriver.exe filepath to the SETTINGS variable you already edited in step 3.
6. Edit robot.py so it runs the modules you desire.
7. Open command line, and type "python robot.py"

## WHAT IT DOES
marketforce_code is broken into multiple modules

robot (main function)
    - robot_A (sends out invites)
    - robot_B (checks for connection status)
    - robot_C (checks for message replies)
    - robot_Q (checks CRM for lead status)
    - robot_R (sends out messages)
    
