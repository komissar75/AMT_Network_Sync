import sys
#import os
import subprocess

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


def net_meshcmd():
    #check AMT status
    result = subprocess.run([meshcmd_path, 'AmtInfo'], stdout=subprocess.PIPE)
    #print(result.stdout.decode())
    amt_result_list = result.stdout.decode().splitlines()
    amt_version = amt_result_list[0].split(",")[0]
    amt_status = amt_result_list[0].split(",")[1].strip()
    print("AMT version: " + amt_version)
    print("AMT status: " + amt_status)
    #print(amt_result_list)
    #net_result = subprocess.run([meshcmd_path, 'AmtNetwork', '--user', amt_user, '--password', amt_password], stdout=subprocess.PIPE)
    #print(type(net_result.stdout.decode()))
    #sys_result = subprocess.run(['ip', '-o', '-f', 'inet', 'address'], stdout=subprocess.PIPE)
    sys_result_list = subprocess.run(['ip', '-o', '-f', 'inet', 'address'], stdout=subprocess.PIPE).stdout.decode().splitlines()
    #print(sys_result_list[0][3:5])
    if len(sys.argv) == 1:
        #print("AMT status is:")
        #for i in amt_result_list:
        #    print(i)
        print("Loclal system IP conf is:")
        for i in sys_result_list:
            if i[3:5] != "lo":
                print(i)
        
    

net_meshcmd()
#print(sys.argv)
#print(len(sys.argv))