#!/usr/bin/env python3

import os
import subprocess


class SchedClass:
    def __init__(self, cmd):
        self.cmdline = cmd
        self.cycle_min = ""
        self.cycle_hour = ""
        self.cycle_date = ""
        self.cycle_month = ""
        self.cycle_day = ""


def sched():
    cronlist = list()
    f = open("./res_sched.txt", "w")
    try:
        res = subprocess.check_output("crontab -l",
                                      shell=True).decode("utf-8")
        res = res.replace('\t', ' ')
        res = res.split('\n')
        for line in res:
            try:
                line = line.split('#', 1)
            except ValueError:
                continue
            try:
                result = line[0].split(" ")
                cmd = ""
                for i in result[5:]:
                    cmd += (i + " ")
                newsched = SchedClass(cmd)
                newsched.cycle_min = result[0]
                newsched.cycle_hour = result[1]
                newsched.cycle_date = result[2]
                newsched.cycle_month = result[3]
                newsched.cycle_day = result[4]
                cronlist.append(newsched)
            except IndexError:
                continue

    except subprocess.CalledProcessError:
        f.write("Cannot call crontab\n")

    for cron in cronlist:
        printstr = (
            f"{cron.cmdline:<40} {cron.cycle_min:<7} {cron.cycle_hour:<7} "
            f"{cron.cycle_date:<7} {cron.cycle_month:<7} {cron.cycle_day:<7}"
        )
        f.write(printstr + "\n")
    f.close()


def get_croninfo():
    sched()
