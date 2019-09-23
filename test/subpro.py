#!/usr/bin/env python3

import subprocess

for i in range(30000):
    res = subprocess.check_output("echo hi", shell=True).decode("utf-8").strip()
print("end")
