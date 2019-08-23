import os
import subprocess

class Env:
    envname = 0
    envval = 0
    envuser = 0
    envnum = 0

def EnvNum():
    cmd = "env | wc -l"
    fd_popen = subprocess.Popen(cmd, stdout = subprocess.PIPE, shell = True).stdout
    num = fd_popen.read().strip()
    return num

def EnvList():
    cmd = "env"
    fd_popen = subprocess.Popen(cmd, stdout = subprocess.PIPE, shell = True).stdout
    while True:
        data = fd_popen.readline().strip()
        if not data:
            break
        print(data.decode('utf-8'))
    fd_popen.close()

if __name__ == "__main__":
    EnvList()
