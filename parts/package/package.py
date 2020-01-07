import pkg_resources
import os


def checkOS():
    pre_os = os.popen("cat /etc/os-release").read().split('\n')
    str_os = None
    for line in pre_os:
        if 'ID_LIKE' in line:
            str_os = line.split('=')
            break
    if str_os is None:
        for line in pre_os:
            if 'ID' in line and 'VERSION' not in line:
                str_os = line.split('=')
                break
    return str_os[1]


def check_pip():
    installed_packages = [(d.project_name, d.version) for d in
                          pkg_resources.working_set]
    print(installed_packages)


def check_package():
    info_os = checkOS()
    res_package = []
    if(info_os == 'ubuntu' or info_os == 'debian'):
        info_pkg = os.popen("dpkg -l").read().split('\n')
        for i in info_pkg:
            if 'ii' in i:
                list_package = i.split(' ')
                for j in list_package:
                    if j is not '':
                        res_package.append(j)
    else:
        info_pkg = os.popen("yum list installed").read().split('\n')
        for i in info_pkg:
            if '@' in i:
                list_package = i.split(' ')
                for j in list_package:
                    if j is not '':
                        res_package.append(j)
    return res_package


def debian_parse(input_list):
    description = 3
    str_description = ''
    res_list = []
    package_info = []
    for input_str in input_list:
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


def fedora_parse(input_list):
    counter = 2
    package_info = []
    res_list = []
    for input_str in input_list:
        if counter == 0:
            counter = 2
            package_info.append(input_str)
            res_list.append(package_info)
            package_info = []
        else:
            counter -= 1
            package_info.append(input_str)
    package_info.append(input_str)
    res_list.append(input_list)
    return res_list


pre_package = check_package()
print(len(debian_parse(pre_package)))


# pip가 깔려있는지 여부도 중요시해야 하나 고민해야 할 것으로 보임.
# package에 대한 추가 정보는 엄청 세세하게 들어가야되는데 이거는 어떻게 처리할 지에 대한 고민도 필요함.
# package 관리가 CentOS는 이상해서 python36u-pip로 되던데?(각 sub버전별로 pip가 있음)
# pip를 통한 보안취약점 유포가 가능한가? 그리고 package에 들어가야할 정보가 뭐가 추가되어야 하는가가 필요할 듯.