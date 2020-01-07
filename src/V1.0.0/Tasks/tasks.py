#!/usr/bin/env python3

import sys
import getopt
import processes
import modules
import startup
import services
import scheduletasks


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
            startup.startup()
        if o == "--services":
            services.services()
        if o == "--schedule-tasks":
            scheduletasks.sched()


if __name__ == "__main__":
    main()
