import os
import subprocess

class SystemInfo:
    def __init__(self):
        self.sysyear = ''
        self.sysmonth = ''
        self.sysday = ''
        self.syshour = ''
        self.sysmin = ''
        self.runlevel = ''
        self.rlyear = ''
        self.rlmonth = ''
        self.rlday = ''
        self.rlhour = ''
        self.rlmin = ''

    def set_sys_year(self , year):
        self.sysyear = year

    def set_sys_month(self , month):
        self.sysmonth = month

    def set_sys_day(self , day):
        self.sysday = day

    def set_sys_hour(self , hour):
        self.syshour = hour

    def set_sys_min(self , minute):
        self.sysmin = minute

    def set_sys_runlevel(self , runlevel):
        self.runlevel = runlevel

    def set_sys_rlyear(self , rlyear):
        self.rlyear = rlyear
    
    def set_sys_rlmonth(self , rlmonth):
        self.rlmonth = rlmonth

    def set_sys_rlday(self , rlday):
        self.rlday = rlday

    def set_sys_rlhour(self , rlhour):
        self.rlhour = rlhour

    def set_sys_rlmin(self , rlmin):
        self.rlmin = rlmin

   # def print_sys(self):
       # print(self.year+"년"+self.month+"월"+self.day+"일"+self.time
        

def extract_sys_year(sys_data):
    endidx = sys_data.find("-") - 1
    startidx = endidx - 4
    year = sys_data[startidx:endidx]
    return year

def extract_sys_month(sys_data):
    startidx = sys_data.find("-") + 1
    endidx = startidx+1
    month = sys_data[startidx:endidx]
    return month

def extract_sys_day(sys_data):
    startidx = sys_data.find("-") + 4
    endidx = startidx + 1
    day = sys_data[startidx:endidx]
    return day

def extract_sys_hour(sys_data):
    startidx = sys_data.find(":") - 2
    endidx = startidx + 1
    hour = sys_data[startidx:endidx]
    return hour

def extract_sys_min(sys_data):
    startidx = sys_data.find(":") + 1
    endidx = startidx + 1
    minute = sys_data[startidx:endidx]
    return minute

def extract_sys_rlyear(sys_data):
    


def extract_sys_info(syslist):
    command = "./exewho.sh"
    result = subprocess.Popen(command,stdout=subprocess.PIPE,shell=True).stdout
    while True:
        sysdata = result.readline().strip().decode()
        if not sysdata: break
        else:
            for i in sysdata:
                print(i+"!")
    sysobj =  SystemInfo()
    sysobj.set_sys_year(extract_sys_year(sysdata))
    sysobj.set_sys_month(extract_sys_month(sysdata))
    sysobj.set_sys_day(extract_sys_day(sysdata))
    sysobj.set_sys_hour(extract_sys_hour(sysdata))
    syslist.append(sysobj)
    result.close()


if __name__ == "__main__":
    syslist = []
    extract_sys_info(syslist)



