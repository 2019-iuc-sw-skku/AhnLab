#!/usr/bin/env python3

import os
import copy
import subprocess
import re


class ProcClass:
    def __init__(self, pid):
        self.dirpath = "/proc/" + str(pid)

        # following fields will be printed until #####
        self.name = ""
        self.att = ""
        self.pid = pid
        self.ppid = ""
        self.thread = ""
        self.priority = ""
        self.nice = ""
        self.crtime = ""
        self.cpu = ""
        self.cputime = ""
        self.platform = ""
        self.mem = ""
        self.pfault = ""
        self.vmpeak = ""
        self.vmsize = ""
        self.user = ""
        self.sessid = ""
        self.cmd = ""
        # self.digsig
        self.accdate = ""
        self.moddate = ""
        # self.version
        # self.product
        # self.company
        self.path = ""
        self.md5 = ""
        self.sha256 = ""
        #####
        ProcClass.uptime = None

    def get_data(self):
        self.get_data_from_stat()
        self.get_data_from_status()
        self.get_data_from_exe()
        self.get_data_from_statm()

    def get_data_from_stat(self):
        f = open(self.dirpath + "/stat", 'r')
        data = f.read()
        datalist = data.split(' ')

        cnt = 0
        for words in datalist[1:]:
            if words[-1] == ')':
                break
            cnt += 1
        for i in range(2, 2 + cnt):
            datalist[1] += " " + datalist[i]
        for i in range(2 + cnt, len(datalist)):
            datalist[i - cnt] = datalist[i]

        self.att = datalist[2]
        self.ppid = int(datalist[3])
        self.sessid = int(datalist[5])
        self.pfault = int(datalist[9]) + int(datalist[10])
        self.priority = int(datalist[17])
        self.nice = int(datalist[18])
        f.close()

    def get_data_from_status(self):
        f = open(self.dirpath + "/status", 'r')
        data = f.readlines()
        for line in data:
            line = line.replace('\t', ' ')
            line = line.replace('\n', '')
            line = re.sub("  +", "", line)
            line = line.replace(':', ' ')
            line = line.split(' ', 1)
            line[1] = line[1].strip()
            if line[0] == "Name":
                self.name = line[1]
            elif line[0] == "State":
                self.att = line[1].split(' ', 1)[0]
            elif line[0] == "Threads":
                self.thread = int(line[1])
            elif line[0] == "VmPeak":
                line[1] = line[1].replace('k', '')
                line[1] = line[1].replace('B', '')
                self.vmpeak = int(line[1].split(' ', 1)[0])
            elif line[0] == "VmSize":
                line[1] = line[1].replace('k', '')
                line[1] = line[1].replace('B', '')
                self.vmsize = int(line[1].split(' ', 1)[0])
            elif line[0] == "Uid":
                uid = line[1].split(' ', 1)[0]
                result = subprocess.check_output("id " + str(uid),
                                                 shell=True).decode("utf-8")
                result = result.split('(', 1)[1]
                result = result.split(')', 1)[0]
                self.user = result
        f.close()

    def get_data_from_exe(self):
        exepath = self.dirpath + "/exe"
        if os.path.isfile(exepath):
            try:
                result = subprocess.check_output("stat " + exepath,
                                                 shell=True).decode("utf-8")
                result = result.replace('\t', ' ')
                result = result.split('\n')
                for line in result:
                    try:
                        c, rest = line.split(' ', 1)
                    except ValueError:
                        continue
                    if c == "Access:" and\
                            len(rest.split(' ', 1)[0].split('-')) == 3:
                        self.accdate = rest.split(' ', 1)[0] + " "
                        self.accdate += rest.split(' ', 2)[1].split('.', 1)[0]
                    if c == "Modify:" and\
                            len(rest.split(' ', 1)[0].split('-')) == 3:
                        self.moddate = rest.split(' ', 1)[0] + " "
                        self.moddate += rest.split(' ', 2)[1].split('.', 1)[0]

            except subprocess.CalledProcessError:
                self.accdate = ""
                self.moddate = ""

            try:
                result = subprocess.check_output("readlink " + exepath,
                                                 shell=True).decode("utf-8")
            except subprocess.CalledProcessError:
                result = ""
            self.path = result.replace('\n', '')
            try:
                result = subprocess.check_output("md5sum " + exepath,
                                                 shell=True).decode("utf-8")
                result = result.split(' ', 1)
                result[1] = result[1].replace(' ', '')
                result[1] = result[1].replace('\n', '')
                if result[1] != exepath:
                    result = ""
                else:
                    result = result[0]
            except subprocess.CalledProcessError:
                result = ""
            self.md5 = result.replace('\n', '')
            try:
                result = subprocess.check_output("sha256sum " + exepath,
                                                 shell=True).decode("utf-8")
                result = result.split(' ', 1)
                result[1] = result[1].replace(' ', '')
                result[1] = result[1].replace('\n', '')
                if result[1] != exepath:
                    result = ""
                else:
                    result = result[0]
            except subprocess.CalledProcessError:
                result = ""
            self.sha256 = result.replace('\n', '')
        else:
            self.path = ""
            self.md5 = ""
            self.sha256 = ""

    def get_data_from_statm(self):
        f = open(self.dirpath + "/statm", 'r')
        data = f.read()
        data = data.replace('\n', ' ')
        data = data.replace('\t', ' ')
        data = data.split(' ', 1)
        self.mem = data[0]
        f.close()


def get_processes(path):
    dirlist = os.listdir(path)
    for dirname in copy.deepcopy(dirlist):
        if (not dirname.isdigit()) or\
                (not os.path.isfile(path + dirname + "/stat")):
            dirlist.remove(dirname)
    return dirlist


def processes():
    basepath = "/proc/"
    dirlist = get_processes(basepath)
    proclist = list()
    for dirname in dirlist:
        if os.path.isfile(basepath + dirname + "/stat"):
            newproc = ProcClass(int(dirname))
            newproc.get_data()
            proclist.append(newproc)
    f = open("./res_processes", "w")
    for proc in proclist:
        # Python 3.6+ code (f-string) started
        printstr = (
            f"{proc.name:<40} {proc.att:<3} {proc.pid:<5} {proc.ppid:<5} "
            f"{proc.thread:<4} {proc.priority:<4} {proc.nice:<4} "
            f"{proc.crtime:<5} {proc.cpu:<5} {proc.cputime:<5} "
            f"{proc.platform:<4} {proc.mem:<8} {proc.pfault:<8} "
            f"{proc.vmpeak:<8} {proc.vmsize:<8} {proc.user:<20} "
            f"{proc.sessid:<5} {proc.cmd:<50} {proc.accdate:<25} "
            f"{proc.moddate:<25} {proc.path:<30} {proc.md5:<50} "
            f"{proc.sha256:<50}"
        )
        # Python 3.6+ code (f-string) ended
#        print(printstr)
        f.write(printstr + "\n")
    f.close()


if __name__ == "__main__":
    processes()

