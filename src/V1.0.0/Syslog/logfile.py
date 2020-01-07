import os
import subprocess
import sys


'''
print("System Log Status\n ")
print("choose the number\n" )
print("1. Users Information\n ")
print("2. Login,Logout,Boot,Shutdown History\n ")
print("3. Recent Success Login History\n ")
print("4. Failed Login History\n ")
print("5. Open the Error Report\n")
'''

def check_permission():
    euid = os.geteuid()
    if euid != 0:
        print('Script not started as root. Running sudo..')
        args = ['sudo', sys.executable] + sys.argv + [os.environ]
        # the next line replaces the currently-running process with the sudo
        os.execlpe('sudo', *args)


class logHis:
    def __init__(self):
        self.res_data = ""

    def check_permission(self):
        euid = os.geteuid()
        if euid != 0:
            print('Script not started as root. Running sudo..')
            args = ['sudo', sys.executable] + sys.argv + [os.environ]
            # the next line replaces the currently-running process with the sudo
            os.execlpe('sudo', *args)


    def choose(self):
        self.res_data += "-"*20 + "Start of recent logs" + "-"*20 + "\n\n"
        result = os.popen('w').read()
        self.res_data += result
        result = os.popen('last').read()
        self.res_data += result
        result = os.popen('lastlog').read()
        self.res_data += result
        result = os.popen('lastb').read()
        self.res_data += result
        self.res_data += "-"*20 + "End of recent logs" + "-"*20 + "\n\n"
    
    def open_file(self):
        try:
            datafile  = open("/var/log/kern.log","r")
            self.res_data += "failed log at kern.log\n"
            self.res_data += "-"*70 + '\n'
            for line in datafile:
                if 'failed' in line:
                    self.res_data += line
            self.res_data += "\n\n"
        except:
            self.res_data += "No kern.log file founded\n\n"

        try:
            datafile2 = open("/var/log/syslog","r")
            self.res_data += "failed log at syslog\n"
            self.res_data += "-"*70 + '\n'
            for line in datafile2:
                if 'failed' in line:
                    self.res_data += line
            self.res_data += "\n\n"
        except:
            self.res_data += "No syslog file founded\n\n"

        try:
            datafile3 = open("/var/log/syslog.1","r")
            self.res_data += "failed log at syslog.1\n"
            self.res_data += "-"*70 + '\n'
            for line in datafile3:
                if 'failed' in line:
                    self.res_data += line
            self.res_data += "\n\n"
        except:
            self.res_data += "No messages file founded\n"

        try:
            datafile4 = open("/var/log/messages","r")
            self.res_data += "failed log at messages\n"
            self.res_data += "-"*70 + '\n'
            for line in datafile4:
                if 'failed' in line:
                    self.res_data += line
            self.res_data += "\n\n"
        except:
            self.res_data += "No messages file founded\n"

        try:
            datafile5 = open("/var/log/messages.1","r")
            self.res_data += "failed log at messages.1\n"
            self.res_data += "-"*70 + '\n'
            for line in datafile5:
                if 'failed' in line:
                    self.res_data += line
            self.res_data += "\n\n"
        except:
            self.res_data += "No messages.1 file founded\n"

def get_syslog():
    t=logHis()
    #t.check_permission()
    t.choose()
    t.open_file()
    sysfile = open("syslog.txt", "w")
    sysfile.write(t.res_data)
    sysfile.close()