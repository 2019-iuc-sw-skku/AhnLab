#!/usr/bin/env python3

import os
import subprocess

##############파일로 정보 저장######################
f1 = open("./system_orgout.txt", 'w')
f2 = open("./system_out.txt", 'w')

##############환경변수 정보 수집########################


class Environment:
    def __init__(self):
        self.envname = ' '
        self.envval = ' '
        self.envuser = []
        self.envnum = 0

    def set_env_name(self, envname):
        self.envname = envname

    def set_env_value(self, envvalue):
        self.envval = envvalue

    def set_env_user(self, user):
        self.envuser.append(user)

    def set_env_num(self, envnum):
        self.envnum = envnum
    '''
    def print_env(self):
        print(str(self.envnum).ljust(3), end='')
        if len(self.envname) > 15:
            print(self.envname[:13]+"..", end='')
        else:
            print(self.envname.ljust(15), end='')
        if len(self.envval) > 15:
            print(self.envval[:13]+"..", end='')
        else:
            print(self.envval.ljust(15), end='')
        idx = 0
        for i in self.envuser:
            if idx > 3:
                print("..")
                break
            print(i+" ", end='')
            idx += 1
        print("")
    '''
    def write_envorg(self):
        f1.write(str(self.envnum).ljust(15))
        f1.write(self.envname.ljust(15))
        f1.write(self.envval.ljust(15))
        for user in self.envuser:
            f1.write(user+" ")
        f1.write("\n")

    def write_env(self):
        f2.write(str(self.envnum).ljust(15))
        if len(self.envname) > 15:
            f2.write((self.envname[:13]+"..").ljust(15))
        else:
            f2.write((self.envname).ljust(15))
        if len(self.envval) > 15:
            f2.write((self.envval[:13]+"..").ljust(15))
        else:
            f2.write((self.envval).ljust(15))
        for user in self.envuser:
            f2.write(user+" ")
        f2.write("\n")

###############시스템, 런 레벨 부팅 시각 수집######################


class SystemInfo:
    def __init__(self):
        self.sysyear = ''
        self.sysmonth = ''
        self.sysday = ''
        self.syshour = ''
        self.sysmin = ''
        self.syssec = ''
        self.runlevel = ''
        self.rlyear = ''
        self.rlmonth = ''
        self.rlday = ''
        self.rlhour = ''
        self.rlmin = ''

    def set_sys_year(self, year):
        self.sysyear = year

    def set_sys_month(self, month):
        self.sysmonth = month

    def set_sys_day(self, day):
        self.sysday = day

    def set_sys_hour(self, hour):
        self.syshour = hour

    def set_sys_min(self, minute):
        self.sysmin = minute

    def set_sys_sec(self, sec):
        self.syssec = sec

    def set_sys_runlevel(self, runlevel):
        self.runlevel = runlevel

    def set_sys_rlyear(self, rlyear):
        self.rlyear = rlyear

    def set_sys_rlmonth(self, rlmonth):
        self.rlmonth = rlmonth

    def set_sys_rlday(self, rlday):
        self.rlday = rlday

    def set_sys_rlhour(self, rlhour):
        self.rlhour = rlhour

    def set_sys_rlmin(self, rlmin):
        self.rlmin = rlmin
    '''
    def print_sys_info(self):
        print("시스템 부팅 시각 ", end='')
        print(self.sysyear+"년 "+self.sysmonth+"월 "+self.sysday+"일 ", end='')
        print(self.syshour + "시 " + self.sysmin + "분 " + self.syssec + "초 ")
        print("런 레벨 %s 시작 시각 " % self.runlevel, end='')
        print(self.rlyear + "년 " + self.rlmonth +
              "월 " + self.rlday + "일 ", end='')
        print(self.rlhour + "시 " + self.rlmin + "분 ")
    '''
    def write_sys_info_org(self):
        f1.write("시스템 부팅 시각 ")
        f1.write(self.sysyear+"년 "+self.sysmonth+"월 "+self.sysday+"일 ")
        f1.write(self.syshour + "시 " + self.sysmin +
                 "분 " + self.syssec + "초 "+"\n")
        f1.write("런 레벨 "+str(self.runlevel)+"시작 시각 ")
        f1.write(self.rlyear + "년 " + self.rlmonth + "월 " + self.rlday + "일 ")
        f1.write(self.rlhour + "시 " + self.rlmin + "분 "+"\n")

    def write_sys_info(self):
        f2.write("시스템 부팅 시각 ")
        f2.write(self.sysyear+"년 "+self.sysmonth+"월 "+self.sysday+"일 ")
        f2.write(self.syshour + "시 " + self.sysmin +
                 "분 " + self.syssec + "초 "+"\n")
        f2.write("런 레벨 "+str(self.runlevel)+"시작 시각 ")
        f2.write(self.rlyear + "년 " + self.rlmonth + "월 " + self.rlday + "일 ")
        f2.write(self.rlhour + "시 " + self.rlmin + "분 "+"\n")


#############시스템, 런 레벨 부팅 시각 정보 수집#########################
def extract_sys_year(sys_data):
    startidx = sys_data.find("-") - 4
    endidx = startidx + 4
    year = sys_data[startidx:endidx]
    return year


def extract_sys_month(sys_data):
    startidx = sys_data.find("-") + 1
    endidx = startidx + 2
    month = sys_data[startidx:endidx]
    return month


def extract_sys_day(sys_data):
    startidx = sys_data.find("-") + 4
    endidx = startidx + 2
    day = sys_data[startidx:endidx]
    return day


def extract_sys_hour(sys_data):
    startidx = sys_data.find(":") - 2
    endidx = startidx + 2
    hour = sys_data[startidx:endidx]
    return hour


def extract_sys_min(sys_data):
    startidx = sys_data.find(":") + 1
    endidx = startidx + 2
    minute = sys_data[startidx:endidx]
    return minute


def extract_sys_sec(sys_data):
    startidx = sys_data.find(":") + 4
    endidx = startidx + 2
    sec = sys_data[startidx:endidx]
    return sec


def extract_sys_runlevel(sys_data):
    startidx = sys_data.rfind("-") - 9
    runlevel = sys_data[startidx]
    return runlevel


def extract_sys_rlyear(sys_data):
    startidx = sys_data.rfind("-") - 7
    endidx = startidx + 4
    rlyear = sys_data[startidx:endidx]
    return rlyear


def extract_sys_rlmonth(sys_data):
    startidx = sys_data.rfind("-") - 2
    endidx = startidx + 2
    rlmonth = sys_data[startidx:endidx]
    return rlmonth


def extract_sys_rlday(sys_data):
    startidx = sys_data.rfind("-") + 1
    endidx = startidx + 2
    rlday = sys_data[startidx:endidx]
    return rlday


def extract_sys_rlhour(sys_data):
    startidx = sys_data.rfind(":") - 2
    endidx = startidx + 2
    rlhour = sys_data[startidx:endidx]
    return rlhour


def extract_sys_rlmin(sys_data):
    startidx = sys_data.rfind(":") + 1
    endidx = startidx + 2
    rlmin = sys_data[startidx:endidx]
    return rlmin


#-환경변수-#######env 명령어로 환경변수 수집##############

def extract_env_list(envlist):
    command = "System/exeenv.sh"
    fd_popen = subprocess.Popen(
        command, stdout=subprocess.PIPE, shell=True).stdout
    env_num = 0
    while True:
        envdata = fd_popen.readline().strip().decode()
        if not envdata:
            break
        envobj = Environment()
        env_num += 1
        envobj.set_env_name(extract_env_name(envdata))
        envobj.set_env_value(extract_env_value(envdata))
        envobj.set_env_user(extract_env_user(envdata))
        envobj.set_env_num(env_num)
        envlist.append(envobj)
    fd_popen.close()


def extract_env_name(env_data):
    endofname = env_data.find("=")
    return env_data[0:endofname]


def extract_env_value(env_data):
    startofval = env_data.find("=")
    return env_data[startofval+1:]


def extract_env_user(env_data):
    return "system"

#-환경변수-#######export 명령어로 환경변수 수집###################


def extract_export_list(envlist):
    command = "System/exeexport.sh"
    fd_popen = subprocess.Popen(
        command, stdout=subprocess.PIPE, shell=True).stdout
    while True:
        exportdata = fd_popen.readline().strip().decode()
        env_num = 0
        if not exportdata:
            break
        else:
            flag = 0
            exportname = extract_export_name(exportdata)
            for data in envlist:
                if exportname == data.envname:  # 이미 있는 환경변수
                    data.set_env_user(extract_export_user(
                        exportdata))  # 사용자 정보만 추가
                    flag = 1
                    break
            if flag is not 1:  # 리스트에 없는 환경변수
                envobj = Environment()
                env_num += 1
                envobj.set_env_name(extract_export_name(exportdata))
                envobj.set_env_value(extract_export_value(exportdata))
                envobj.set_env_user(extract_export_user(exportdata))
                envobj.set_env_num(env_num)
                envlist.append(envobj)


def is_exist(entirelist, data):
    for i in entirelist:
        if data is i.envname:
            return True  # 리스트에 이미 있는 환경변수
    return False  # 리스트에 없는 환경변수


def extract_export_name(export_data):  # declare -x 이름 ="값"
    startofname = export_data.find("x")+2
    endofname = export_data.find("=")
    if endofname is not -1:  # 쉘 변수에 값이 있으면
        return export_data[startofname:endofname]
    else:  # 쉘 변수에 값이 없으면
        return export_data[startofname:]


def extract_export_value(export_data):
    startofval = export_data.find("\"")
    endofval = len(export_data)
    if startofval is not -1:  # 쉘 변수의 값이 있으면
        return export_data[startofval+1:endofval-1]
    else:  # 쉘 변수의 값이 없으면
        return ""


def extract_export_user(Export_data):
    return "shell"


#-환경변수-#####파일 탐색으로 환경변수 정보 수집#############
# def extract_envfile(envlist)


#-시스템, 런 레벨 부팅시각-####uptime, who  명령어로 정보 수집###############
def extract_sys_info(syslist):
    command = "System/exewho.sh"
    result = subprocess.Popen(
        command, stdout=subprocess.PIPE, shell=True).stdout
    while True:
        sysdata = result.read().strip().decode()
        if not sysdata:
            break
        else:
            sysobj = SystemInfo()
            sysobj.set_sys_year(extract_sys_year(sysdata))
            sysobj.set_sys_month(extract_sys_month(sysdata))
            sysobj.set_sys_day(extract_sys_day(sysdata))
            sysobj.set_sys_hour(extract_sys_hour(sysdata))
            sysobj.set_sys_min(extract_sys_min(sysdata))
            sysobj.set_sys_sec(extract_sys_sec(sysdata))
            sysobj.set_sys_runlevel(extract_sys_runlevel(sysdata))
            sysobj.set_sys_rlyear(extract_sys_rlyear(sysdata))
            sysobj.set_sys_rlmonth(extract_sys_rlmonth(sysdata))
            sysobj.set_sys_rlday(extract_sys_rlday(sysdata))
            sysobj.set_sys_rlhour(extract_sys_rlhour(sysdata))
            sysobj.set_sys_rlmin(extract_sys_rlmin(sysdata))
            syslist.append(sysobj)
    result.close()


################ main 함수 ######################

def get_sysstat():
    syslist = []
    envlist = []

    extract_sys_info(syslist)
    extract_env_list(envlist)
    extract_export_list(envlist)
    for i in syslist:
        i.write_sys_info()
        i.write_sys_info()
        # i.print_sys_info()
    # print("   이름".ljust(15)+"  값".ljust(15)+"사용자".ljust(15))
    file_format = " ".ljust(15)+"이름".ljust(15)+"값".ljust(15)+"사용자".ljust(15)
    f1.write(file_format+"\n")
    f2.write(file_format+"\n")
    for i in envlist:
        i.write_envorg()
        i.write_env()
        # i.print_env()
    f1.close()
    f2.close()

