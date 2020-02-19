import sys
#import os
import subprocess
import socket
import struct

meshcmd_path = "/home/komissar/Downloads/meshcmd"
amt_user = "admin"
amt_password = "P@ssw0rd"
amt_version = ""
amt_status ="" #activated or not
amt_ip_mode = "" #static or dynamic
amt_mac = ""
amt_ip = ""
amt_mask = ""
amt_gate = ""
amt_dns = ""
amt_dns2 = ""
system_devise = ""
system_ip_mode = "" #static or dynamic
system_mac = ""
system_ip = ""
system_mask = ""
system_gate = ""
system_dns = ""
system_dns2 = ""

def net_meshcmd():
    global amt_version
    global amt_status
    global amt_ip_mode
    global amt_mac
    global amt_ip
    global amt_mask
    global amt_gate
    global amt_dns
    global amt_dns2
    global system_devise
    global system_ip_mode 
    global system_mac
    global system_ip
    global system_mask
    global system_gate
    global system_dns
    global system_dns2
    result = subprocess.run([meshcmd_path, 'AmtInfo'], stdout=subprocess.PIPE) #check AMT status
    #print(result.stdout.decode())
    amt_result_list = result.stdout.decode().splitlines()
    #print(amt_result_list)
    amt_version = amt_result_list[0].split(", ")[0]
    if amt_result_list[0].split(", ")[1][-1] == ".":
        amt_status = amt_result_list[0].split(", ")[1][0:-1]
    else:
        amt_status = amt_result_list[0].split(", ")[1]
    print("AMT version: " + amt_version)
    print("AMT status: " + amt_status)
    list_len = len(amt_result_list[1].split(", "))
    if amt_result_list[1].split(", ")[0] == "Wired Enabled":
        if amt_result_list[1].split(", ")[1] == "DHCP": amt_ip_mode = "Dynamic"
        else: amt_ip_mode = amt_result_list[1].split(", ")[1]
        if list_len >=3: amt_mac = amt_result_list[1].split(", ")[2].replace(".", "")
        if list_len >=4: amt_ip = amt_result_list[1].split(", ")[3]
    else:
        print("wired interface not enabled")
        return
    print("AMT ip mode is: "+ amt_ip_mode)
    if amt_mac != '': print("AMT MAC is: " + amt_mac)
    if amt_ip != '': print("AMT IP is: " + amt_ip)
    net_result = subprocess.run([meshcmd_path, 'AmtNetwork', '--user', amt_user, '--password', amt_password], stdout=subprocess.PIPE)
    amt_ip_result_list = net_result.stdout.decode().splitlines()
    #print(amt_ip_result_list)
    for i in amt_ip_result_list:
        if i.count("WIRELESS") == 1: break
        if i.split(": ")[0].count("DefaultGateway") == 1: amt_gate = i.split(": ")[1]
        elif i.split(": ")[0].count("PrimaryDNS") == 1: amt_dns = i.split(": ")[1]
        elif i.split(": ")[0].count("SecondaryDNS") == 1: amt_dns2 = i.split(": ")[1]
        elif i.split(": ")[0].count("SubnetMask") == 1: amt_mask = i.split(": ")[1]
    print("AMT Gate is: " + amt_gate)
    print("AMT Primary DNS is: " + amt_dns)
    print("AMT Scondary DNS is: " + amt_dns2)
    print("AMT Subnet Mask is: " + amt_mask)
    sys_link_list = subprocess.run(['ip', '-o', 'link'], stdout=subprocess.PIPE).stdout.decode().splitlines()
    for i in sys_link_list:
        if i.count(amt_mac.casefold()) == 1:
            system_devise = i.split(": ")[1]
            if i.count("state DOWN") == 1: 
                print("Wired link is down")
                return
    #print(system_devise)
    if system_devise != "":
        sys_inet_str = subprocess.run(['ip', '-o', '-f', 'inet', 'address', 'show', system_devise], stdout=subprocess.PIPE).stdout.decode()
        if sys_inet_str == "":
            system_ip_mode = "Dynamic"
        else:
            if sys_inet_str.count("dynamic") == 1:
                system_ip_mode = "Dynamic"
            else:
                system_ip_mode = "Static"
            sys_ip_str = subprocess.run(['nmcli', '-t', '-f', 'IP4.ADDRESS', 'device', 'show', system_devise], stdout=subprocess.PIPE).stdout.decode().splitlines()[0]
            system_ip = sys_ip_str.split(":")[1].split("/")[0]
            system_mask = socket.inet_ntoa(struct.pack('!I', (1 << 32) - (1 << (32 - int(sys_ip_str.split(":")[1].split("/")[1])))))
            system_gate = subprocess.run(['nmcli', '-t', '-f', 'IP4.GATEWAY', 'device', 'show', system_devise], stdout=subprocess.PIPE).stdout.decode().splitlines()[0].split(":")[1]
            sys_dns_list = subprocess.run(['nmcli', '-t', '-f', 'IP4.DNS', 'device', 'show', system_devise], stdout=subprocess.PIPE).stdout.decode().splitlines()
            if len(sys_dns_list) >= 1: system_dns = sys_dns_list[0].split(":")[1]
            if len(sys_dns_list) >= 2: system_dns2 = sys_dns_list[1].split(":")[1]
            #system_dns = subprocess.run(['nmcli', '-t', '-f', 'IP4.DNS', 'device', 'show', system_devise], stdout=subprocess.PIPE).stdout.decode().splitlines()[0].split(":")[1]
            #system_dns2 = subprocess.run(['nmcli', '-t', '-f', 'IP4.DNS', 'device', 'show', system_devise], stdout=subprocess.PIPE).stdout.decode().splitlines()[2].split(":")[1]
    print("System IP mode is: " + system_ip_mode)
    print("System IP is: " + system_ip)
    print("System GATE is: " + system_gate)
    print("System Primary DNS is: " + system_dns)
    print("System Secondary DNS is: " + system_dns2)
    print("System Subnet Mask is: " + system_mask)
    if amt_ip_mode == "Dynamic" and system_ip_mode == "Dynamic":
        print("AMT and System IP settings are synced.")
        return
    elif amt_ip_mode == "Static" and system_ip_mode == "Dynamic":
        print("Changing AMT IP mode to Dynamic...")
        ip_change = subprocess.run([meshcmd_path, 'AmtNetwork', '--user', amt_user, '--password', amt_password, "--dhcp"], stdout=subprocess.PIPE)
        print(ip_change.stdout.decode())
        return
    elif amt_ip_mode == "Static" and system_ip_mode == "Static":
        if amt_ip == system_ip and amt_mask == system_mask and amt_gate == system_gate and amt_dns == system_dns and amt_dns2 == system_dns2:
            print("AMT and System IP settings are synced.")
            return
        else:
            print("Changing AMT IP settings...")
            ip_change = subprocess.run([meshcmd_path, 'AmtNetwork', '--user', amt_user, '--password', amt_password, "--dhcp"], stdout=subprocess.PIPE)
            print(meshcmd_path + " " + 'AmtNetwork' + " " + '--user' + " " + amt_user + " " + '--password' + " " + amt_password + " " + "--static" + " " + "--ip" + " " + system_ip + " " + "--subnet" + " " + system_mask + " " + "--gateway" + " " + system_gate + " " + "--dns" + " " + system_dns + " " + "--dns2" + " " + system_dns2)
            ip_change = subprocess.run([meshcmd_path, 'AmtNetwork', '--user', amt_user, '--password', amt_password, "--static", "--ip", system_ip, "--subnet", system_mask, "--gateway", system_gate, "--dns", system_dns, "--dns2", system_dns2], stdout=subprocess.PIPE)
            print(ip_change.stdout.decode())
            return
    elif amt_ip_mode == "Dynamic" and system_ip_mode == "Static":
        print("Changing AMT IP settings...")
        ip_change = subprocess.run([meshcmd_path, 'AmtNetwork', '--user', amt_user, '--password', amt_password, "--static", "--ip", system_ip, "--subnet", system_mask, "--gateway", system_gate, "--dns", system_dns, "--dns2", system_dns2], stdout=subprocess.PIPE)
        print(ip_change.stdout.decode())
        return

net_meshcmd()
#print(sys.argv)
#print(len(sys.argv))