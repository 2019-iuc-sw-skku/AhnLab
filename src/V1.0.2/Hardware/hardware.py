import platform
import os
import subprocess
import sys
from collections import OrderedDict
import glob
import re


def check_permission():
    euid = os.geteuid()
    if euid != 0:
        print('Script not started as root. Running sudo..')
        args = ['sudo', sys.executable] + sys.argv + [os.environ]
        # the next line replaces the currently-running process with the sudo
        os.execlpe('sudo', *args)


def check_hwcmd():
    res_l = os.popen("dpkg -l | grep lshw").read().split(' ')
    res_d = os.popen("dpkg -l | grep dmidecode").read().split(' ')
    if 'lshw' not in res_l:
        print("package lshw not found. Stop H/W check\n")
        return 0
    if 'dmidecode' not in res_d:
        print("package dmidecode not found. Stop H/W check\n")
        return 0
    return 1


def sh(cmd, in_shell=False, get_str=True):
    output = subprocess.check_output(cmd, shell=in_shell)
    if get_str:
        return str(output, 'utf-8')
    return output


def get_hwinfo():
    res_strinfo = ""
    check_permission()
    # Linux Distribution
    res_strinfo += ("OS : " + " ".join(platform.uname()) + " " +
                    platform.release()+" ")

    # Device Info
    device = str(os.popen('lshw').read())
    devices = device.split('\n')
    device_info = list()
    count = 0
    for line in devices:

        if "*-cache" in line:
            count = 1
        if count == 1:
            device_info.append(line)
            device_info.append('\n')

    res_strinfo += "=====================================================\n"
    res_strinfo += "Devices:\n "+"".join(device_info)

    # CPU Info
    model_name = None
    cpu_core = 0
    processor_count = 0
    with open('/proc/cpuinfo') as f:

        for line in f:
            if line.strip():
                if line.rstrip('\n').startswith('model name'):
                    model_name = line.rstrip('\n').split(':')[1]
                if line.rstrip('\n').startswith('cpu cores'):
                    cpu_core = line.rstrip('\n').split(':')[1]
                if line.rstrip('\n').startswith("cpu MHz"):
                    cpu_clock = line.rstrip('\n').split(":")[1]

                if 'processor' in line.strip():
                    processor_count += 1

    res_strinfo += "=====================================================\n"
    res_strinfo += "CPU : " + model_name + '\n'
    res_strinfo += "CPU Clock speed : {0:.2f}GHz".format(
        (eval(cpu_clock)/1000)) + '\n'
    res_strinfo += "CPU Core : " + cpu_core + '\n'
    res_strinfo += "Logical processors :" + str(processor_count) + '\n'

    # Mainboard Info

    baseboard = str(os.popen('dmidecode -t baseboard').read())
    baseboard = baseboard.split('\n')
    for line in baseboard:
        if "Product Name" in line:
            product_name = line.split(': ')[1]
        if "Manufacturer" in line:
            manufacturer = line.split(": ")[1]

    bios = str(os.popen('dmidecode -t bios').read())
    bios = bios.split('\n')
    for line in bios:
        if "Vendor" in line:
            vendor = line.split(': ')[1]
        if "Version" in line:
            version = line.split(': ')[1]
    '''
    for line in baseboard:
        if line.strip():
            print(line.strip())
            if line.rstrip('\n').startswith('Product Name'):
                product_name = line.rstrip('\n').split(':')[1]
    '''

    res_strinfo += "=====================================================" + '\n'
    res_strinfo += "MainBoard Name: " + product_name + '\n'
    res_strinfo += "MainBoard Manufacturer: " + manufacturer + '\n'
    res_strinfo += "BIOS brand: " + vendor + '\n'
    res_strinfo += "BIOS version: " + version + '\n'

    # Drive Info
    letter_hdd = str(os.popen('df | grep "/dev/sd"').read())
    letter_ssd = str(os.popen('df | grep "/dev/nvme"').read())
    file_sys_hdd = str(os.popen('mount | grep ^/dev/sd').read())
    if file_sys_hdd != '':
        file_sys_hdd = file_sys_hdd.split('type ')[1]
    file_sys_ssd = str(os.popen('mount | grep ^/dev/neve').read())
    if file_sys_ssd != '':
        file_sys_ssd = file_sys_ssd.split('type ')[1]
    hdd_mem_size = letter_hdd.split(' ')
    ssd_mem_size = letter_ssd.split(' ')
    hdd_size = list()
    ssd_size = list()
    for line in hdd_mem_size:
        if line != '':
            hdd_size.append(line)
    for line in ssd_mem_size:
        if line != '':
            ssd_size.append(line)
    if hdd_size != []:
        hdd_mem_size = (eval(hdd_size[1])/(1024*1024))
        hdd_free_size = (eval(hdd_size[3])/(1024*1024))
    if ssd_size != []:
        ssd_mem_size = (eval(ssd_size[1])/(1024*1024))
        ssd_free_size = (eval(ssd_size[3])/(1024*1024))

    res_strinfo += "=====================================================" + '\n'
    try:
        hdd_res = "HDD Info\n"
        hdd_res += letter_hdd + '\n'
        hdd_res += "File system: " + file_sys_hdd + '\n'
        hdd_res += "Size: {0:.2f}G".format(hdd_mem_size) + '\n'
        hdd_res += "Free size: {0:.2f}G".format(hdd_free_size) + '\n'
        res_strinfo += hdd_res
    except:
        pass
    try:
        ssd_res = "SSD Info\n"
        ssd_res += letter_ssd + '\n'
        ssd_res += "File system: " + file_sys_ssd + '\n'
        ssd_res += "Size: {0:.2f}G".format(ssd_mem_size) + '\n'
        ssd_res += "Free size: {0:.2f}G".format(ssd_free_size) + '\n'
        res_strinfo += ssd_res
    except:
        pass

    # Volume Info

    lshw_info = os.popen("df | grep '^/dev/'").read()
    lshw_info = lshw_info.split('\n')
    volume_info = list()
    count = 0
    for line in lshw_info:
        if "volume" in line:
            line = "Volume"
            count = 1
            continue
        if count == 1:
            volume_info.append(line)
        if "state" in line:
            count = 0

    res_strinfo += "=====================================================" + '\n'
    res_strinfo += "Volume" + '\n'
    for line in volume_info:
        if "=" in line:
            line = line.split(' ')
            for i in range(0, len(line)):
                if line[i] == '':
                    continue
                elif '=' in line[i]:
                    if i+1 < len(line) and (':' in line[i+1]):
                        res_strinfo += line[i] + line[i+1] + '\n'
                    else:
                        res_strinfo += line[i] + '\n'
                elif ('=' in line[i-1]) is False:
                    res_strinfo += line[i] + '\n'
        else:
            res_strinfo += line.lstrip() + '\n'

    # Disk Info

    disk = device
    disc = disk.split('\n')
    disk_info = list()
    count = 0
    for line in disc:
        if "*-disk" in line:
            line = "Disk"
            count = 1
            continue
        if count == 1:
            disk_info.append(line)
            disk_info.append('\n')
        if "sectorsize" in line:
            count = 0

    res_strinfo += "=====================================================" + '\n'
    res_strinfo += "Disk:\n " + "".join(disk_info) + '\n'

    # Memory Info
    meminfo = OrderedDict()
    with open('/proc/meminfo') as f:
        for line in f:
            meminfo[line.split(':')[0]] = line.split(':')[1].strip()
    res_strinfo += "=====================================================" + '\n'
    res_strinfo += 'Total memory: {0}'.format(meminfo['MemTotal']) + '\n'
    res_strinfo += 'Free memory: {0}'.format(meminfo['MemFree']) + '\n'
    res_strinfo += "=====================================================" + '\n'
    # HDD Info

    # Add any other device pattern to read from
    # dev_pattern = ['sd.*', 'mmcblk*']

    f = open("hardware.txt", "w")
    f.write(res_strinfo)
    f.close


def size(device):
    nr_sectors = open(device+'/size').read().rstrip('\n')
    sect_size = open(device+'/queue/hw_sector_size').read().rstrip('\n')
    # The sect_size is in bytes, so we convert it to GiB and then send it back
    return (float(nr_sectors)*float(sect_size))/(1024.0*1024.0*1024.0)


'''
def detect_devs():
    for device in glob.glob('/sys/block/*'):
        for pattern in dev_pattern:
            if re.compile(pattern).match(os.path.basename(device)):
                print('Device:: {0}, Size:: {1} GiB'.format(device,
                    size(device)))
'''


def get_hwstat():
    res = check_hwcmd()
    if res == 1:
        get_hwinfo()
