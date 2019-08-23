#!/usr/bin/env python3

import subprocess

from loggingtime import logging_time


class ServClass:
    def __init__(self):
        self.name = ""
        self.stat = ""
        self.pid = ""
        self.uid = ""
        self.priority = ""
        self.nice = ""
        self.desc = ""
        self.lstate = ""
        self.astate = ""
        self.sstate = ""
        self.id = ""
        self.names = ""

    def get_data(self, line):
        linelist = line.split(" | ")
        self.name = linelist[0]
        self.stat = linelist[1]
        self.pid = linelist[2]
        self.uid = linelist[3]
        self.priority = linelist[4]
        self.nice = linelist[5]
        self.desc = linelist[6]
        self.lstate = linelist[7]
        self.astate = linelist[8]
        self.sstate = linelist[9]
        self.id = linelist[10]
        self.names = linelist[11]

@logging_time
def services():
    print("here is services")
    servlist = list()
    res = subprocess.check_output("./ifsysman.sh",
                                  shell=True).decode("utf-8")
    res = res.strip()
    resline = res.split("\n")
    for line in resline:
        if line == "":
            continue
        newserv = ServClass()
        newserv.get_data(line)
        servlist.append(newserv)

    for serv in servlist:
        print(serv.name + ": " + serv.lstate + " " + serv.astate + " " + serv.sstate + " " + serv.desc)


if __name__ == "__main__":
    services()
