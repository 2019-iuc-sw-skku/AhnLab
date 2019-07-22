#!/usr/bin/env python3

import sys
import getopt

import processes
import modules


def main():
    try:
        opt, arg = getopt.getopt(sys.argv[1:], "",
                                 ["processes", "modules", "startup",
                                  "services", "schedule-tasks"]
                                 )
    except getopt.GetoptError as err:
        print(err)
        sys.exit(-1)

    if not opt or arg:
        print("Invalid option")
        sys.exit(-1)

    for o, a in opt:
        if o == "--processes":
            processes.processes()
        if o == "--modules":
            modules.modules()
        if o == "--startup":
            print("startup")
        if o == "--services":
            print("services")
        if o == "--schedule-tasks":
            print("schedule-tasks")


if __name__ == "__main__":
    main()

