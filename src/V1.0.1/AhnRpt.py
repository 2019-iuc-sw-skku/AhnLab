import os
import sys
import time
import Hardware.hardware as main_hardware
import Package.test as main_package
import Package.class_pkg as class_pkg
import Network.network as main_network
import System.system as main_system
import Syslog.logfile as main_syslog
import Tasks.processes as process
import Tasks.modules as modules


def check_permission():
    euid = os.geteuid()
    if euid != 0:
        print('AhnRpt is not started as root. Running sudo..')
        args = ['sudo', sys.executable] + sys.argv + [os.environ]
        # the next line replaces the currently-running process with the sudo
        os.execlpe('sudo', *args)


if __name__ == "__main__":
    check_permission()
    print("AhnRpt for Linux V1.0\nThis program is only support Debian Linux right now.")
    print("We are stadily updating the program to cover most of linux OS.\n")
    print("****************************************************************")
    print("Warning! Please make sure that no .txt files in this directory!")
    print("****************************************************************")
    print("The process will start in 5 seconds...")
    print("If you have things to backup, press Ctrl+C to abort")
    time.sleep(5)
    print("Whole process will take about 30sec ~ 3 min.")
    print("Check System Status...")
    main_system.get_sysstat()
    print("Check Hardware Status...")
    main_hardware.get_hwstat()
    print("Check Process/Module Status...")
    process.get_procinfo()
    modules.get_moduleinfo()
    print("check Package Status...")
    main_package.get_pkginfo()
    print("check network status...")
    main_network.get_netstat()
    print("Check System Log info...")
    main_syslog.get_syslog()

    print("Compressing output files...")
    os.popen("tar zcf AhnRpt.tar.gz *.txt")
    time.sleep(1)
    os.popen("rm -r *.txt")
    print("All done! All of the file is stored in AhnRpt.tar.gz\n")
