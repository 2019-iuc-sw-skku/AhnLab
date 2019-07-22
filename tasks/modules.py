#!/usr/bin/env python3

import re
import subprocess
import processes
from loggingtime import logging_time


class ModClass:
    def __init__(self, pid, path):
        self.name = path.split('/')[-1]
        self.att = ""
        self.pids = [pid]
#        self.digsig
        self.accdate = ""
        self.moddate = ""
        self.version = ""
#        self.product = ""
#        self.company = ""
        self.path = path
        self.md5 = ""
        self.sha256 = ""
        self.strpids = ""

    def add_pids(self, pids):
        for pid in pids:
            if pid not in self.pids:
                self.pids.append(pid)

    def make_strpids(self):
        self.strpids = str(self.pids)
        self.strpids = self.strpids.strip()


def get_data(moddict):
    get_data_from_command(moddict)

@logging_time
def get_data_from_command(moddict):
    argstr = " ".join(moddict.keys())
#    result = subprocess.check_output("./dateandhash.sh " + argstr,
#                                     shell=True).decode("utf-8")
    result = subprocess.check_output("./everyiteration.sh " + argstr,
                                     shell=True).decode("utf-8")
    result = result.strip()
    result = result.split("\n")
    for line in result:
        if line == "":
            continue
        line = line.split(" | ")
        path = line[0]
        moddict[path].accdate = line[1]
        moddict[path].moddate = line[2]
        moddict[path].md5 = line[3]
        moddict[path].sha256 = line[4]
    # self.version

@logging_time
def modules():
    dirlist = processes.get_processes("/proc/")
    
    moddict = dict()
    for dirname in dirlist:
        try:
            f = open("/proc/" + dirname + "/maps")
            data = f.readlines()
            for line in data:
                pline = line.replace("\t", " ")
                pline = pline.replace("\n", "")
                pline = re.sub(" +", " ", pline)
                pline = pline.strip()
                pline = pline.split(" ")[-1]
                if pline[0] != '/':
                    continue
                if pline.split(".so")[-1] != "" and ".so." not in pline:
                    continue
                if pline not in moddict:
                    moddict[pline] = ModClass(int(dirname), pline)
                else:
                    moddict[pline].add_pids([int(dirname)])
            f.close()
        except FileNotFoundError:
            continue

    argstr = " ".join(moddict.keys())
    result = subprocess.check_output("./popensh.sh " + argstr,
                                     shell=True).decode("utf-8")
    result = result.strip()
    result = result.split("\n")
    for line in result:
        if line == "":
            break
        line = line.split(" ")
        moddict[line[1]].add_pids(moddict[line[0]].pids)
        del moddict[line[0]]
    get_data(moddict)

    for mod in moddict.values():
        mod.make_strpids()
        printstr = (
            f"{mod.name:<20} {mod.att:<3} {mod.strpids:<50} "
            f"{mod.accdate:<20} {mod.moddate:<20} {mod.version:<5} "
            f"{mod.path:<40} {mod.md5:<50} {mod.sha256:<50}"
        )
        print(printstr)

# placeholder
if __name__ == "__main__":
    modules()

