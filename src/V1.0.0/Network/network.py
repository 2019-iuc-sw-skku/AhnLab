import os
import re


class Firewall:
    def __init__(self):
        if os.path.exists("/etc/ufw"):
            self.ufw = True
        else:
            self.ufw = False

    def UFW(self):
        if self.ufw is False:
            return

        # user_rule = os.popen("sudo cat /etc/ufw/user.rules")
        # user6_rule = os.popen("sudo cat /etc/ufw/user6.rules")

        self.data = os.popen("sudo ufw show raw")
        self.output = self.parse(self.data.read())

    def parse(self, data):
        firewall_rules = []
        line_data = data.split("\n")
        for i in line_data:
            firewall_rules.append(i.split())

        temp = []
        temp.extend(firewall_rules)

        for i in temp:
            if not i or i[0] is 'pkts':
                firewall_rules.remove(i)

        firewall_rules.insert(0, ['packets', 'bytes', 'target', 'protocol',
                                  'option', 'in', 'out', 'source',
                                  'destination'])
        return firewall_rules


class NetConnect:
    def __init__(self):
        self.output = os.popen("sudo ss").read()
        # self.output = self.parse(self.data.read())

    def parse(self, data):
        net_info = []
        print(data)
        internet, unix = data.split("\nActive ")
        split_data = internet.split("\n")

        for line_data in split_data:
            single_net = line_data.split()
            single_net = [x for x in single_net if x]
            if len(single_net) is not 6:
                single_net.append(" ")
            net_info.append(single_net)

        del net_info[0], net_info[0]
        net_info.insert(0, ['Protocol', 'Recv-Q', 'Send-Q', 'Local Address',
                            'Foreign Address', 'State'])
        return net_info


class IpConfig:
    def __init__(self):
        self.output = os.popen("sudo ip addr show").read()
        # self.output = self.parse(self.data.read())

    def parse(self, data):
        ip_info = []
        ip_all = data.split('\n\n')

        for ip in ip_all:
            ip_name = ip[:ip.find(":")]
            ip = ip[ip.find(" ")+1:]

            data_line = ip.split('\n')
            tmp = {}
            for datak in data_line:
                datak = datak.strip()
                temp = datak.split('  ')
                for t in temp:
                    p = re.compile('\(.*\)$')
                    m = p.search(t)

                    if m:
                        t = t[:m.start()]
                        t = t.strip()

                    a = t.rfind(" ")

                    if a is not -1:
                        tmp[t[:a]] = t[a+1:]
                    else:
                        k = re.compile('flags=')
                        m = k.search(t)

                        if m:
                            tmp[t[:m.end()-1]] = t[m.end():]
                        else:
                            if t is 'loop':
                                tmp[t] = 'loopback'
            ip_info.append({ip_name: tmp})

        return ip_info


class RouteTable:
    def __init__(self):
        self.output = os.popen("sudo ip route show").read()
        # self.output = self.parse(self.data.read())

    def parse(self, data):
        route_info = []
        split_data = data.split("\n")
        start_pattern = re.compile('^[\d]')

        for line_data in split_data:
            if not start_pattern.match(line_data):
                continue

            single_route = line_data.split()
            single_route = [x for x in single_route if x]
            route_info.append(single_route)

        route_info.insert(0, ['Destination', 'Gateway', 'Genmask', 'Flags',
                              'Metric', 'Ref', 'Use', 'Iface'])
        return route_info


class ArpCache:
    def __init__(self):
        self.output = os.popen("sudo ip n s").read()
        # self.output = self.parse(self.data.read())

    def parse(self, data):
        arp_info = []
        split_data = data.split("\n")
        start_pattern = re.compile('^[\d]')

        for line_data in split_data:
            if not start_pattern.match(line_data):
                continue

            single_arp = line_data.split()
            single_arp = [x for x in single_arp if x]
            arp_info.append(single_arp)

        arp_info.insert(0, ['Address', 'HWtype', 'HWaddress', 'Flags',
                            'Iface'])
        return arp_info


def get_netstat():
    f = open("network.txt", 'w')

    firewall = Firewall()
    firewall.UFW()
    net = NetConnect()
    ip = IpConfig()
    route = RouteTable()
    arp = ArpCache()

    f.write("*** Firwall Rules ***")
    for i in firewall.output:
        for j in i:
            f.write(j + ' ')
        f.write("\n")
    f.write("------------------------------------------------------------------\
            ----------\n")
    f.write("*** Network Connection ***\n")
    f.write(net.output)
    f.write("\n")
    f.write("------------------------------------------------------------------\
            ----------\n")
    f.write("*** IP Configuartion ***\n")
    f.write(ip.output)
    f.write("------------------------------------------------------------------\
            ----------\n")
    f.write("*** Routing Table ***\n")
    f.write(route.output)
    f.write("------------------------------------------------------------------\
            ----------\n")
    f.write("*** ARP Cache ***\n")
    f.write(arp.output)
    f.write("------------------------------------------------------------------\
            ----------\n")
    f.close()

    os.system("sudo cat network.txt")
