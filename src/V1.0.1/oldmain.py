import os
import sys
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
        print('Script not started as root. Running sudo..')
        args = ['sudo', sys.executable] + sys.argv + [os.environ]
        # the next line replaces the currently-running process with the sudo
        os.execlpe('sudo', *args)


if __name__ == "__main__":
    check_permission()
    # main_system.get_sysstat()
    main_network.get_netstat() # Block the function due to error
    # main_package.cli_main()
    # main_syslog.get_syslog()
    # process.get_procinfo()
    # modules.get_moduleinfo()
    os.popen("tar zcf AhnRpt.tar.gz package.txt syslog.txt")

