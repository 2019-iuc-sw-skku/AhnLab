import netifaces
import os


def check_network():
    print("Network Status\n")
    check_nic()
    print()
    check_rt()


def check_nic():
    print("Interface status")
    connect_count = False
    interfaces = netifaces.interfaces()
    gateway = netifaces.gateways()
    for i in range(len(interfaces)):
        print("interface %d: " % i + interfaces[i])
        if_status = netifaces.ifaddresses(interfaces[i])
        if netifaces.AF_INET in if_status:
            ip = if_status[netifaces.AF_INET][0]['addr']
            if str(ip) != '127.0.0.1':
                connect_count = True
            print(if_status[netifaces.AF_INET])
        if netifaces.AF_INET6 in if_status:
            print(if_status[netifaces.AF_INET6])
        if netifaces.AF_LINK in if_status:
            print(if_status[netifaces.AF_LINK])

    if connect_count:
        print(gateway[netifaces.AF_INET])
    return 0


def check_rt():
    routing_table = os.popen("ip route show")
    print("Routing Table")
    print(routing_table.read())
    return 0

