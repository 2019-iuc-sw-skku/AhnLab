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
import Tasks.scheduletasks as schedules


def version_info(now_time):
    version = "AhnRpt V1.0.2"
    file_version = open("AhnRpt Info.txt", 'w')
    file_version.write(version)
    record_time = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon,
                                                     now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    file_version.write("\n"+"record_time: "+record_time)
    file_version.close()


def check_permission():
    euid = os.geteuid()
    if euid != 0:
        print('AhnRpt is not started as root. Running sudo..')
        args = ['sudo', sys.executable] + sys.argv + [os.environ]
        # the next line replaces the currently-running process with the sudo
        os.execlpe('sudo', *args)


if __name__ == "__main__":
    check_permission()
    print("AhnRpt for Linux V1.0.2\nThis program is only support Debian Linux.")
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
    print("Check Process/Module/Schedule Status...")
    process.get_procinfo()
    modules.get_moduleinfo()
    schedules.get_croninfo()
    print("Check Package Status...")
    main_package.get_pkginfo()
    print("Check Network status...")
    main_network.get_netstat()
    print("Check System Log info...")
    main_syslog.get_syslog()

    now = time.localtime()
    s = "%02d%02d%02d_%02d%02d%02d" % (now.tm_year % 100, now.tm_mon,
                                       now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    print("Writing Version Info...")
    version_info(now)
    print("Compressing output files...")
    tar_command = "tar zcf AhnRpt" + s + ".tar.gz *.txt"
    filename = "AhnRpt" + s + ".tar.gz"
    os.popen(tar_command)
    time.sleep(1)
    os.popen("rm -r *.txt")
    print("All done! All of the file is stored in " + filename + "\n")
