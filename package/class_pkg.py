import os
import sys
import pkg_resources


class package:
    def __init__(self, int_type):
        self.os_type = int_type
        self.syspkg = []
        self.pippkg = []
        self.web = []
        self.info = []
        return None

    def check_syspkg(self):
        if self.os_type == 1:
            self.sys_pkg = self.debian.pkglist(self)
        elif self.os_type == 2:
            self.sys_pkg = self.fedora.pkglist(self)
        elif self.os_type == 3:
            self.sys_pkg = self.arch.pkglist(self)
        else:
            print("Package info can only run at supported Linux.")
            print("Please check your Linux OS type.")
            return None
        return self.sys_pkg

    def check_pippkg(self):
        if self.os_type == 1:
            checkpip = self.check_existpkg('python3-pip')
        if self.os_type == 2:
            checkpip = self.check_existpkg('python36u-pip')
        if checkpip is False:
            self.pip_pkg.append('not installed')
            return 'not installed'
        else:
            installed_packages = [(d.project_name, d.version) for d in
                                  pkg_resources.working_set]
            self.pip_pkg = installed_packages
            return installed_packages

    def check_existpkg(self, str_pkg):
        res_check = False
        if self.os_type == 1:
            list_package = self.debian.pkglist(self)
        elif self.os_type == 2:
            list_package = self.fedora.pkglist(self)
        elif self.os_type == 3:
            list_package = self.arch.pkglist(self)
        else:
            return err_pkg_os()
        for sublist in list_package:
            if str_pkg in sublist:
                res_check = True
        return res_check

    def check_pkginfo(self, str_pkg):
        if self.os_type == 1:
            res_info = self.debian.pkginfo(self, str_pkg)
        elif self.os_type == 2:
            res_info = self.fedora.pkginfo(self, str_pkg)
        elif self.os_type == 3:
            res_info = self.arch.pkginfo(self, str_pkg)
        else:
            return err_pkg_os()

    def err_pkg_os():
        print("package info is only available at supported Linux type.\
            --help for more information")
        return None

    def check_firefox(self):
        pass

    class debian:
        def pkglist(package):
            pre_package = []
            res_package = []
            info_pkg = os.popen("dpkg -l").read().split('\n')
            for i in info_pkg:
                if 'ii' in i:
                    list_package = i.split(' ')
                    for j in list_package:
                        if j is not '':
                            pre_package.append(j)
            res_package = package.debian.pkgparse(pre_package)
            return res_package

        def pkginfo(package, name_pkg):
            list_package = package.debian.pkglist(package)
            res_pkginfo = []
            if name_pkg == 'all':
                print("warning! dkpg do not support showing specific info for\
                    all installed packages. It may take more than a minute,\
                    so please consider searching individual package.")
                print("You may use Ctrl + C for keyboard interrupt")
                for sublist in list_package:
                    if sublist[0] is not '':
                        name_pkg = sublist[0]
                        info_subpkg = os.popen("dpkg -s " + name_pkg).read()
                        res_pkginfo.append(info_subpkg)
                return res_pkginfo
            else:
                if package.check_existpkg(name_pkg):
                    info_subpkg = os.popen("dpkg -s " + name_pkg).read()
                    res_pkginfo.append(info_subpkg)
                    package.info = res_pkginfo
                    return res_pkginfo
                else:
                    print("No package found. Check input.")

        def pkgparse(list_input):
            description = 3
            str_description = ''
            res_list = []
            package_info = []
            for input_str in list_input:
                if input_str == 'ii':
                    description = 3
                    package_info.append(str_description)
                    res_list.append(package_info)
                    str_description = ''
                    package_info = []
                    continue
                if description == 0:
                    str_description += ' ' + input_str
                else:
                    package_info.append(input_str)
                    description -= 1
            package_info.append(str_description)
            res_list.append(package_info)
            return res_list

    class fedora:
        def pkglist(self):
            res_package = []
            pre_package = []
            info_pkg = os.popen("yum list installed").read().split('\n')
            for i in info_pkg:
                if '@' in i:
                    list_package = i.split(' ')
                    for j in list_package:
                        if j is not '':
                            pre_package.append(j)
            res_package = self.pkgparse(pre_package)
            return res_package

        def pkginfo(self):
            pass

        def pkgparse(self, list_input):
            counter = 2
            package_info = []
            res_list = []
            for input_str in list_input:
                if counter == 0:
                    counter = 2
                    package_info.append(input_str)
                    res_list.append(package_info)
                    package_info = []
                else:
                    counter -= 1
                    package_info.append(input_str)
            package_info.append(input_str)
            res_list.append(package_info)
            return res_list

    class arch:
        def pkglist(self):
            res_package = []
            pre_package = os.popen("pacman -Q").read().split('\n')
            for i in pre_package:
                sublist = i.split(' ')
                res_package.append(sublist)
            return res_package

        def pkginfo(self, str_pkg):
            list_package = self.pkglist()
            res_package = []
            if str_pkg == 'all':
                pre_package = os.popen("pacman -Qi").read()
            else:
                if str_pkg in list_package:
                    pre_package = os.popen("pacman -Qi " + str_pkg).read()
            return pre_package
