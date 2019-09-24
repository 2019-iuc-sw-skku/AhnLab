import platform
import os
import subprocess
import sys

def check_permission():
    euid = os.geteuid()
    if euid != 0:
        print('Script not started as root. Running sudo..')
        args = ['sudo', sys.executable] + sys.argv + [os.environ]
        # the next line replaces the currently-running process with the sudo
        os.execlpe('sudo', *args)

def sh(cmd, in_shell=False, get_str=True):
    output = subprocess.check_output(cmd, shell=in_shell)
    if get_str:
        return str(output, 'utf-8')
    return output

check_permission() 
#Linux Distribution 
print( "OS : " + " ".join(platform.linux_distribution()) + " " + platform.release())


#Device Info
device=str(os.popen('lshw').read())
devices=device.split('\n')
device_info=list()
count=0
for line in devices:

    if "*-cache" in line:
        count=1
    if count==1:
        device_info.append(line)
        device_info.append('\n')



print ("=====================================================")
print ("Devices:\n "+"".join(device_info))




#CPU Info
model_name = None
cpu_core = 0
processor_count=0
with open('/proc/cpuinfo') as f:

    for line in f:
        if line.strip():
            if line.rstrip('\n').startswith('model name'):
                model_name = line.rstrip('\n').split(':')[1]
            if line.rstrip('\n').startswith('cpu cores'):
                cpu_core = line.rstrip('\n').split(':')[1]
            if line.rstrip('\n').startswith("cpu MHz"):
                cpu_clock= line.rstrip('\n').split(":")[1]

            if 'processor' in line.strip():
                processor_count+=1
           
           
print ("=====================================================")
print ("CPU : " + model_name)
print ("CPU Clock speed : {0:.2f}GHz".format((eval(cpu_clock)/1000)))
print ("CPU Core : " + cpu_core)
print("Logical processors :", processor_count)

#Mainboard Info

baseboard=str(os.popen('dmidecode -t baseboard').read())
baseboard=baseboard.split('\n')
for line in baseboard:
    if "Product Name" in line:
        product_name=line.split(': ')[1]
    if "Manufacturer" in line:
        manufacturer=line.split(": ")[1]

bios=str(os.popen('dmidecode -t bios').read())
bios=bios.split('\n')
for line in bios:
    if "Vendor" in line:
        vendor=line.split(': ')[1]
    if "Version" in line:
        version=line.split(': ')[1]
'''
for line in baseboard:
     if line.strip():
        print(line.strip())
        if line.rstrip('\n').startswith('Product Name'):
            product_name = line.rstrip('\n').split(':')[1]
'''


print ("=====================================================")
print ("MainBoard Name: "+product_name)
print ("MainBoard Manufacturer: "+manufacturer)
print ("BIOS brand: "+vendor)
print ("BIOS version: "+version)



#Drive Info
letter=str(os.popen('df | grep "/dev/sd"').read())

file_sys=str(os.popen('mount | grep ^/dev').read())
file_sys=file_sys.split('type ')[1]
size=letter.split(' ')
size1=list()
for line in size:
    if line!='':
        size1.append(line)

size=(eval(size1[1])/(1024*1024))
free_size=(eval(size1[3])/(1024*1024))


print ("=====================================================")
print(letter)
print("File system: "+file_sys)
print("Size: {0:.2f}G".format(size))
print("Free size: {0:.2f}G".format(free_size))



#Volume Info

lshw_info=str(os.popen('lshw').read())
lshw_info=lshw_info.split('\n')
volume_info=list()
count=0
for line in lshw_info:

    if "volume" in line:
        line="Volume"
        count=1
        continue
    if count==1:
        volume_info.append(line)
    if "state" in line:
        count=0

print ("=====================================================")
print ("Volume")
for line in volume_info:
    
    if "=" in line:
        line=line.split(' ')
        for i in range(0,len(line)):
            if line[i]=='':
                continue
            elif '=' in line[i]:
                if i+1<len(line) and (':' in line[i+1]):
                    print(line[i],line[i+1])        
                else:
                    print(line[i])
            elif ('=' in line[i-1])==False:
                print(line[i])
                
    else:
        print(line.lstrip())



#Disk Info

disk=str(os.popen('lshw').read())
disc=disk.split('\n')
disk_info=list()
count=0
for line in disc:

    if "*-disk" in line:
        line="Disk"
        count=1
        continue
    if count==1:
        disk_info.append(line)
        disk_info.append('\n')
    if "sectorsize" in line:
        count=0




print ("=====================================================")
print ("Disk:\n "+"".join(disk_info))


#Memory Info
from collections import OrderedDict
meminfo=OrderedDict()
with open('/proc/meminfo') as f:
    for line in f:
        meminfo[line.split(':')[0]] = line.split(':')[1].strip()
print ("=====================================================")
print('Total memory: {0}'.format(meminfo['MemTotal']))
print('Free memory: {0}'.format(meminfo['MemFree']))
print ("=====================================================")
#HDD Info
import glob
import re
import os
# Add any other device pattern to read from
dev_pattern = ['sd.*','mmcblk*']
def size(device):
    nr_sectors = open(device+'/size').read().rstrip('\n')
    sect_size = open(device+'/queue/hw_sector_size').read().rstrip('\n')
    # The sect_size is in bytes, so we convert it to GiB and then send it back
    return (float(nr_sectors)*float(sect_size))/(1024.0*1024.0*1024.0)
def detect_devs():
    for device in glob.glob('/sys/block/*'):
        for pattern in dev_pattern:
            if re.compile(pattern).match(os.path.basename(device)):
                print('Device:: {0}, Size:: {1} GiB'.format(device, size(device)))


detect_devs()
