#!/usr/bin/env python3

import os
import copy
import subprocess


class StartupClass:
    def __init__(self, path):
        self.path = path
        self.name = ""
        self.runlevel = ""
        self.location = ""
        self.priority = ""
        self.moddate = ""
        self.md5 = ""
        self.sha256 = ""
        self.status = ""

    def get_data(self):
        try:
            result = subprocess.check_output("readlink -f " + self.path,
                                             shell=True).decode("utf-8")
        except subprocess.CalledProcessError:
            self.location = result

        try:
            result = subprocess.check_output("md5sum " + self.path,
                                             shell=True).decode("utf-8")
            result = result.split(' ', 1)
            result[1] = result[1].replace(' ', '')
            result[1] = result[1].replace('\n', '')
            if result[1] != self.path:
                result = ""
            else:
                result = result[0]
        except subprocess.CalledProcessError:
            result = ""
        self.md5 = result

        try:
            result = subprocess.check_output("sha256sum " + self.path,
                                             shell=True).decode("utf-8")
            result = result.split(' ', 1)
            result[1] = result[1].replace(' ', '')
            result[1] = result[1].replace('\n', '')
            if result[1] != self.path:
                result = ""
            else:
                result = result[0]
        except subprocess.CalledProcessError:
            result = ""
        self.sha256 = result
        self.status = self.name[0]
        self.priority = self.name[1:3]
        try:
            result = subprocess.check_output("stat " + self.path,
                                             shell=True).decode("utf-8")
            result = result.replace('\t', ' ')
            result = result.split('\n')
            for line in result:
                try:
                    c, rest = line.split(' ', 1)
                except ValueError:
                    continue
                if c == "Modify:" and\
                        len(rest.split(' ', 1)[0].split('-')) == 3:
                    self.moddate = rest.split(' ', 1)[0] + " "
                    self.moddate += rest.split(' ', 2)[1].split('.', 1)[0]
        except subprocess.CalledProcessError:
            self.moddate = ""


def startup():
    basepath = "/etc/"
    startuplist = list()
    for i in range(0, 7):
        dirlist = os.listdir(basepath + "rc" + str(i) + ".d/")
        for dirname in copy.deepcopy(dirlist):
            newstartup = StartupClass(basepath + "rc" + str(i) + ".d/" + dirname)
            newstartup.name = dirname
            newstartup.runlevel = str(i)
            newstartup.get_data()
            startuplist.append(newstartup)
    dirlist = os.listdir(basepath + "rcS.d/")
    for dirname in copy.deepcopy(dirlist):
        newstartup = StartupClass(basepath + "rcS.d/" + dirname)
        newstartup.name = dirname
        newstartup.runlevel = str(i)
        newstartup.get_data()
        startuplist.append(newstartup)
    f = open("./res_startup", "w")
    for startup in startuplist:
        printstr = (
            f"{startup.name:<40} {startup.status:<3} {startup.runlevel:<5} "
            f"{startup.priority:<5} "
            f"{startup.path:<50} {startup.location:<50} {startup.moddate:<25} "
            f"{startup.md5:<50} {startup.sha256:<50}"
        )
        f.write(printstr + "\n")
    f.close()


if __name__ == "__main__":
    startup()
