import netifaces


class NicInfo:
    def __init__(self):
        self.ifinfo = None
        self.rtinfo = None


    def switch_socket_type(self, number):
        return {1: 'UNIX', 2: 'IPv4', 3:'AX25', 4: 'IPX', 5: 'Appletalk', 10: 'IPv6',\
             14:'Security', 16: 'Route', 17: 'Link', 31: 'Bluetooth'}[number]


    def switch_netmask_numbers(self, number):
        return {'0': 0, '128': 1, '192': 2, '224': 3, '240': 4, '248': 5, '252': 6,\
             '254': 7, '255': 8}[number]


    def switch_netmask(self, number):
        if '/' in number:
            loc_slice = number.find('/')
            res = number[loc_slice+1:]
            return res
        else:
            split = number.split('.')
            res = 0
            for i in range(len(split)):
                res += self.switch_netmask_numbers(split[i])
            return res


    def parsing_if(self, link_data):
        for i in range(len(link_data)):
            output_string = ""
            key_if = list(link_data[i].keys())
            for j in range(len(key_if)):
                if(key_if[j] == 'netmask'):
                    output_netmask = self.switch_netmask(str(link_data[i]['netmask']))
                    output_string =output_string[:-1] + "/"+str(output_netmask) + " "
                else:
                    if('%' in link_data[i][key_if[j]]):
                        loc_end = str(link_data[i][key_if[j]]).find('%')
                        add_string = str(link_data[i][key_if[j]])[:loc_end]
                    else:
                        add_string = str(link_data[i][key_if[j]])

                    output_string += key_if[j] +": "
                    output_string += add_string + " "
            print(output_string)
        print("")
        return " "


    def check_nic(self):
        interfaces = netifaces.interfaces()
        for i in range(len(interfaces)):
            print("interface%d (%s)status" % (i, interfaces[i]))
            key_nic = interfaces[i]
            if_status = netifaces.ifaddresses(interfaces[i])
            key_if_status = list(if_status.keys())
            for j in range(len(key_if_status)):
                #print(if_status[key_if_status[j]])
                bef_parsed = if_status[key_if_status[j]]
                parsed_if = self.parsing_if(bef_parsed)


if __name__ == "__main__":
    nic = NicInfo()
    nic.check_nic()

