import os
import time


class test_fund:
    def __init__(self):
        self.res_type = []
        self.typecode = int
        self.res_kernel = str
        self.res_locale = str
        self.res_host = str
        self.res_memory = []

    def check_type(self):
        pre_type = os.popen("cat /etc/os-release").read().split('\n')
        str_type = None
        list_type = []
        for line in pre_type:
            if 'ID_LIKE' in line:
                str_type = line.split('=')
                list_type.append(str_type)
            if 'ID' in line and 'VERSION' not in line and 'ID_LIKE' not in\
                    line:
                str_type = line.split('=')
                list_type.append(str_type)
        self.typecode = self.classify_type(list_type)
        return list_type

    def classify_type(self, input_list):
        for i in input_list:
            if i[0] == 'ID_LIKE':
                str_type = i[1].lower()
                return {'ubuntu': 1, 'debian': 1, 'fedora': 2, 'arch': 3}\
                    .get(str_type, '-1')

    def check_kernel(self):
        res_kernel = os.popen("uname -r").read().split("\n")
        return res_kernel[0]

    def check_locale(self):
        pre_locale = os.popen("locale").read().split("\n")
        for line in pre_locale:
            if 'LANG' in line:
                str_locale = line.split("=")
                break
        return str_locale[1]

    def check_host(self):
        res_host = os.popen("cat /etc/hostname").read().split('\n')[0]
        return res_host

    def check_memory(self):
        pre_mem = os.popen("free").read().split('\n')
        ret_memlist = []
        for line in pre_mem:
            if 'Mem' in line:
                str_mem = line.split(' ')
                break
        for string_mem in str_mem:
            if 'Mem:' not in string_mem and string_mem is not '':
                ret_memlist.append(string_mem)
        return ret_memlist[:3]

    def check_basic(self):
        self.res_os = self.check_os()
        self.res_kernel = self.check_kernel()
        self.res_locale = self.check_locale()
        self.res_host = self.check_host()
        self.res_memory = self.check_memory()

    def print_basic(self):
        print("Basic settings")
        print("OS-type: \t\t\t\t" + self.res_os)
        print("Linux Kernel Version: \t" + self.res_kernel)
        print("default locale: \t\t" + self.res_locale)
        print("hostname: \t\t\t\t" + self.res_host)
        print("total memory: \t\t\t" + self.res_memory[0])
        print("used memory: \t\t\t" + self.res_memory[1])
        print("free memory: \t\t\t" + self.res_memory[2])
