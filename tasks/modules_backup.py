#!/usr/bin/env python3

import re
import subprocess
import processes

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

    def add_pid(self, pid):
        if pid not in self.pids:
            self.pids.append(pid)

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
                """
               linkres = subprocess.check_output("ls -l " + pline, shell=True).decode("utf-8")"""
                linkres = pline
                linkres = linkres.strip()
                linkres = linkres.split(" ")[-1]
                
                if linkres not in moddict:
                    moddict[linkres] = ModClass(int(dirname), linkres)
                else:
                    moddict[linkres].add_pid(int(dirname))
            f.close()
        except FileNotFoundError:
            continue
    for paths in moddict:
        print(paths + " : ", end='')
        print(moddict[paths].pids)
        
#placeholder


if __name__ == "__main__":
    modules()

