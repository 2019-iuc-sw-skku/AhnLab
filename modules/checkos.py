import os
import time

def checkOS():
    pre_os = os.popen("cat /etc/os-release").read().split('\n')
    str_os = None
    for line in pre_os:
        if 'ID_LIKE' in line:
            str_os = line.split('=')
            break
    if str_os == None:
        for line in pre_os:
            if 'ID' in line and 'VERSION' not in line:
                str_os = line.split('=')
                break
    print(str_os)
    return str_os[1]

if __name__ == "__main__":
    res_os = checkOS()
    print(res_os)
