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
        self.call_os = None
        if int_type == 1:
            self.call_os = self.debian
        elif int_type == 2:
            self.call_os = self.fedora
        elif int_type == 3:
            self.call_os = self.arch
        return None

    def check_syspkg(self):
        if self.os_type == 1:
            self.sys_pkg = self.debian.pkglist(self.call_os, self)
        elif self.os_type == 2:
            self.sys_pkg = self.fedora.pkglist(self.call_os, self)
        elif self.os_type == 3:
            self.sys_pkg = self.arch.pkglist(self.call_os, self)
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
            self.pippkg.append('not installed')
            return 'not installed'
        else:
            installed_packages = [(d.project_name, d.version) for d in
                                  pkg_resources.working_set]
            # self.pippkg = installed_packages
            str_package = self.pipparse(installed_packages)
            self.pippkg = str_package
            return str_package

    def check_existpkg(self, str_pkg):
        res_check = False
        if self.os_type == 1:
            list_package = self.debian.pkglist(self.call_os, self)
        elif self.os_type == 2:
            list_package = self.fedora.pkglist(self.call_os, self)
        elif self.os_type == 3:
            list_package = self.arch.pkglist(self.call_os, self)
        else:
            return self.err_pkg_os()
        for sublist in list_package:
            if str_pkg in sublist:
                res_check = True
        return res_check

    def check_pkginfo(self, str_pkg):
        if self.os_type == 1:
            res_info = self.debian.pkginfo(self.call_os, self, str_pkg)
        elif self.os_type == 2:
            res_info = self.fedora.pkginfo(self.call_os, self, str_pkg)
        elif self.os_type == 3:
            res_info = self.arch.pkginfo(self.call_os, self, str_pkg)
        else:
            return self.err_pkg_os()
        self.info = res_info

    def err_pkg_os(self):
        print("package info is only available at supported Linux type.\
            -h for more information")
        return None

    def check_firefox(self):
        pass

    def infoparse(self, list_info):
        res_infostr = "---------------------------------------------\n"
        res_infostr += "Individual Package info\n\n"
        for sublist in list_info:
            str_one = ""
            for element in sublist:
                str_one += element[0] + ": " + element[1] + '\n'
            str_one += '\n'
            res_infostr += str_one
        return res_infostr

    def pipparse(self, list_info):
        res_infostr = "---------------------------------------------\n"
        res_infostr += "Pip Package info\n\n"
        for sublist in list_info:
            str_one = ""
            str_one += "Name: " + sublist[0] + " | Version: " + sublist[1]
            str_one += "\n"
            res_infostr += str_one
        return res_infostr

    class debian:
        def __init__(self):
            return None

        def pkglist(self, package):
            pre_package = []
            res_package = []
            info_pkg = os.popen("dpkg -l").read().split('\n')
            for i in info_pkg:
                if 'ii' in i:
                    list_package = i.split(' ')
                    for j in list_package:
                        if j is not '':
                            pre_package.append(j)
            res_package = package.debian.pkgparse(self, pre_package)
            return res_package

        def pkginfo(self, package, name_pkg):
            infochecker = ['Package', 'Version', 'Architecture',
                           'Installed-Size',
                           'Depends', 'Pre-Depends', 'Description', 'Homepage']
            list_package = package.debian.pkglist(self, package)
            res_pkginfo = []
            if name_pkg == 'all':
                '''
                print("warning! dkpg do not support showing specific info for\
                       all installed packages. It may take more than a minute,\
                       so please consider searching individual package.")
                print("You may use Ctrl + C for keyboard interrupt")
                '''
                for sublist in list_package:
                    if sublist[0] is not '':
                        name_pkg = sublist[0]
                        info_subpkg = os.popen("dpkg -s " + name_pkg).read().\
                            split('\n')
                        res_onepkg = []
                        for sub_info in info_subpkg:
                            check_list = sub_info.split(': ')
                            if len(check_list) == 1:
                                res_onepkg[-1] += check_list
                            elif check_list[0] in infochecker:
                                res_onepkg.append(check_list)
                        res_pkginfo.append(res_onepkg)
                file_pkginfo = package.infoparse(res_pkginfo)
                return file_pkginfo
            else:
                if package.check_existpkg(name_pkg):
                    info_subpkg = os.popen("dpkg -s " + name_pkg).read()
                    res_pkginfo.append(info_subpkg)
                    package.info = res_pkginfo
                    return res_pkginfo
                else:
                    print("No package found. Check input.")

        def pkgparse(self, list_input):
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
        def __init__(self):
            return None

        def pkglist(self, package):
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

        def pkginfo(self, package, pkg_name):
            return 0

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
        def __init__(self):
            return None

        def pkglist(self, package):
            res_package = []
            pre_package = os.popen("pacman -Q").read().split('\n')
            for i in pre_package:
                sublist = i.split(' ')
                res_package.append(sublist)
            return res_package

        def pkginfo(self, package, str_pkg):
            list_package = self.pkglist(package)
            res_package = []
            if str_pkg == 'all':
                pre_package = os.popen("pacman -Qi").read()
            else:
                if str_pkg in list_package:
                    pre_package = os.popen("pacman -Qi " + str_pkg).read()
            res_package = pre_package
            return res_package
