import Package.class_pkg as class_pkg
import time
import argparse
import os


def pkg_main():
    parser = argparse.ArgumentParser(prog="AhnRpt package part")
    parser.add_argument("--option", "-o", required=True)
    parser.add_argument("--name", "-n")
    args = parser.parse_args()
    options = ['list', 'info', 'pip']
    res_list = None
    if args.option in options:
        res_pkg = class_pkg.package(1)
        if(args.option == 'info' and args.name is None):
            print("wrong options, you should input name")
            return None
        else:
            if args.option == 'info':
                res_pkg.check_pkginfo(args.name)
                print(res_pkg.info)
            elif args.option == 'list':
                res_list = res_pkg.check_syspkg()
                print(res_list)
            elif args.option == 'pip':
                res_list = res_pkg.check_pippkg()
                print(res_list)
        res_pkg = class_pkg.package(1)
    else:
        print("wrong options")


def get_pkginfo():
    str_os = check_os()
    int_os = os_parser(str_os)
    res_pkg = class_pkg.package(int_os)
    res_pkg.check_syspkg()
    file_list = open("package_list.txt", "w")
    file_list.write(res_pkg.syspkg)
    file_list.close()
    res_pkg.check_pkginfo('all')
    res_pkg.check_pippkg()
    file = open("package.txt", "w")
    file.write(res_pkg.info)
    file.write(res_pkg.pippkg)
    file.close()
    '''
    parsed_pkg = parser_pkg(res_pkg.info)
    print(parsed_pkg)
    '''
    return None


def check_os():
    file_os = os.popen('cat /etc/os-release').read().split('\n')
    checker = ['ID', 'ID_LIKE']
    list_res = []
    for i in file_os:
        list_i = i.split('=')
        if list_i[0] in checker:
            list_res.append(list_i[1])
    if len(list_res) == 2 and list_res[1] is not '':
        str_os = list_res[1]
    else:
        str_os = list_res[0]
    return str_os


def os_parser(str_os):
    down_os = str_os.lower()
    return {'debian': 1, 'ubuntu': 1, 'fedora': 2, 'arch': 3}.get(down_os, 0)
