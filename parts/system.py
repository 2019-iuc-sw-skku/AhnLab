import os
import subprocess
class SystemInfo:
    def __init__(self):
        self.boottime = ' '
        self.year=''
        self.month=''
        self.day=''
        self.time=''


def extract_system_info():
    command="./exewho"
    fd_popen=subprocess.Popen(command,stdout=subprocess.PIPE,shell=True).stdout
    while True:
        systemdata=fd_popen.readline().strip().decode()
        if not systemdata: break
        else:
            for i in systemdata:
                print(i+"!")

##############환경변수 정보 수집########################
class Environment:
    def __init__(self):
        self.envname = ' '
        self.envval = ' '
        self.envuser = []
        self.envnum = ' '

    def set_env_name(self, envname):
        self.envname=envname

    def set_env_value(self, envvalue):
        self.envval=envvalue

    def set_env_user(self, user):
        self.envuser.append(user)

    def print_env(self):
        if len(self.envname) > 15:
            print(self.envname[:13]+"..",end='')
        else:
            print(self.envname.ljust(15),end='')
        if len(self.envval) > 15:
            print(self.envval[:13]+"..",end='')
        else:
            print(self.envval.ljust(15),end='')
        idx=0
        for i in self.envuser:
            if idx > 3:
                print("..")
                break
            print(i+" ",end='')
            idx+=1
        print("")

#########env 명령어로 환경변수 수집##############        

def extract_env_list(envlist):
    command="./exeenv.sh"
    fd_popen=subprocess.Popen(command,stdout=subprocess.PIPE,shell=True).stdout
    while True:
        envdata=fd_popen.readline().strip().decode()
        if not envdata: break
        envobj=Environment()
        envobj.set_env_name(extract_env_name(envdata))
        envobj.set_env_value(extract_env_value(envdata))
        envobj.set_env_user(extract_env_user(envdata))
        envlist.append(envobj)
    fd_popen.close()

def extract_env_name(env_data):
    endofname=env_data.find("=")
    return env_data[0:endofname]

def extract_env_value(env_data):
    startofval=env_data.find("=")
    return env_data[startofval+1:]

def extract_env_user(env_data):
    return "system"

#########export 명령어로 환경변수 수집###################

def extract_export_list(envlist):
    command="./exeexport.sh"
    fd_popen=subprocess.Popen(command,stdout=subprocess.PIPE,shell=True).stdout
    while True:
        exportdata=fd_popen.readline().strip().decode()
        if not exportdata: break
        else:
            flag=0
            exportname=extract_export_name(exportdata)
            for data in envlist:
                if exportname == data.envname:#이미 있는 환경변수
                    data.set_env_user(extract_export_user(exportdata)) #사용자 정보만 추가
                    flag=1
                    break
            if flag is not 1: #리스트에 없는 환경변수
                envobj=Environment()
                envobj.set_env_name(extract_export_name(exportdata))
                envobj.set_env_value(extract_export_value(exportdata))
                envobj.set_env_user(extract_export_user(exportdata))
                envlist.append(envobj)

def is_exist(entirelist,data):
    for i in entirelist:
        if data is i.envname:
            return True     #리스트에 이미 있는 환경변수
    return False         #리스트에 없는 환경변수

def extract_export_name(export_data):      #declare -x 이름 ="값"
    startofname=export_data.find("x")+2
    endofname=export_data.find("=")
    if endofname is not -1:      #쉘 변수에 값이 있으면
        return export_data[startofname:endofname]
    else:       #쉘 변수에 값이 없으면
        return export_data[startofname:]

def extract_export_value(export_data):
    startofval=export_data.find("\"")
    endofval=len(export_data)
    if startofval is not -1:    #쉘 변수의 값이 있으면
        return export_data[startofval+1:endofval-1]
    else:       #쉘 변수의 값이 없으면
        return ""

def extract_export_user(Export_data):
    return "shell"

################ main 함수 ######################

if __name__ == "__main__":
    envlist=[]
    extract_env_list(envlist)
    extract_export_list(envlist)
    print(" 이름".ljust(15)+"  값".ljust(15)+"사용자".ljust(15))
    for i in envlist:
        i.print_env()

