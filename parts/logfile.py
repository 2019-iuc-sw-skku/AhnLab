import os
import subprocess

class logHis:


    print("System Log Status\n ")
    print("choose the number\n" )
    print("1. Users Information\n ")
    print("2. Login,Logout,Boot,Shutdown History\n ")
    print("3. Recent Success Login History\n ")
    print("4. Failed Login History\n ")
    print("5. Open the Error Report\n")
    value=input()

    def choose(cls):

        if cls.value=='1':
            result = os.popen('w').read()
            print(result)
            
        elif cls.value=='2':
            result = os.popen('last').read()
            print(result)

        elif cls.value=='3':
            result = os.popen('lastlog').read()
            print(result)
    
        elif cls.value=='4':
            result = os.popen('lastb').read()
            print(result)
    
    def open_file(self):

        if self.value=='5':
            datafile  = open("kern.log","r")
            for line in datafile:
                if 'failed' in line:
                    print (line)

            datafile2 = open("syslog","r")
            for line in datafile2:
                if 'failed' in line:
                    print(line)

            datafile3 = open("syslog.1","r")
            for line in datafile3:
                if 'failed' in line:
                    print(line)

            datafile4 = open("messages","r")
            for line in datafile4:
                if 'failed' in line:
                    print(line)

            datafile5 = open("messages.1","r")
            for line in datafile5:
                if 'failed' in line:
                    print(line)

        
t=logHis()
t.choose()
t.open_file()
    

        




