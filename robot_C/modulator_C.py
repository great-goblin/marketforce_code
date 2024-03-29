"""
Checks Linkedin messages
"""
def modulator_C(self,campaign,linked_username,linked_password,spread_name,sheet_name,servitor,servitor_fname):

    #Imports
    print('\n mod_C @ %s: Importing'%campaign)
    from linkedin_C import getmessages
    from chrome_C import push2sheets

    #Vars
    print('\n mod_C @ %s: Defining Variables'%campaign)


    

    m = len(servitor)
    

    #Load data
    print('\n mod_C @ %s: Loading Data'%campaign)
    messages = getmessages(self,linked_username,linked_password)
    for message in messages:
        if len(message[1])==0:
            print('ALERT! Conversation with %s unsuccessfully retrieved.'%message[0])

    #Edit data
    print('\n mod_C @ %s: Editing Data'%campaign)
    def check_c1(X,servitorx):
        return (X[1][0]==servitorx) and (X[1][1]==X[0])

    def check_m2(X,servitorx):
        return X[1].count(servitorx) > 1

    def check_c2(X,servitorx):
        return (X[1][0]==servitorx) and (X[1][1]==servitorx) and (X[1][2]==X[0])

    def check_m3(X,servitorx):
        return X[1].count(servitorx) > 2

    def check_c3(X,servitorx):
        return (X[1][0]==servitorx) and (X[1][1]==servitorx) and (X[1][2]==servitorx) and (X[1][3]==X[0])

    def check_d(X,servitorx):
        return X[1].count(X[0]) > 1
    cdct = {}
    for message in messages:
        rdct = {'C1':0,'M2':0,'C2':0,'M3':0,'C3':0,'D':0}

        try:
            if check_c1(message,servitor): rdct['C1']=1
        except: pass

        try:
            if check_m2(message,servitor): rdct['M2']=1
        except: pass
        
        try:
            if check_c2(message,servitor): rdct['C2']=1
        except: pass

        try:
            if check_m3(message,servitor): rdct['M3']=1
        except: pass
                  
        try:
            if check_c3(message,servitor): rdct['C3']=1
        except: pass

        try:
            if check_d(message,servitor): rdct['D']=1
        except: pass
                                
        cdct[message[0]]=rdct


    #Output data
    print('\n mod_C @ %s: Outputting Data'%campaign)
    push2sheets(cdct,spread_name,sheet_name)
    print('\n mod_C @ %s: Program Complete.'%campaign)
