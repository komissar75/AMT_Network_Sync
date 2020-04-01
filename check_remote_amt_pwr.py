import sys
import subprocess

meshcmd_path = "/home/komissar/meshcmd"
amt_user = "admin"
amt_password = "P@ssw0rd"
amt_list = "/home/komissar/amt_list.txt"

def pwr_meshcmd(host_ip):
    result = subprocess.run([meshcmd_path, 'amtpower', '--host', host_ip, '--user', amt_user, '--pass', amt_password], stdout=subprocess.PIPE) #check AMT status
    pwr_status_list = result.stdout.decode().splitlines()
    if pwr_status_list[0].count("Current power state") > 0:
        print(host_ip, pwr_status_list[0])
        if pwr_status_list[0] != 'Current power state: Power on':
            print("turning on", host_ip)
            pwr_on_result = subprocess.run([meshcmd_path, 'amtpower', '--host', host_ip, '--user', amt_user, '--pass', amt_password, '--poweron'], stdout=subprocess.PIPE)
            if pwr_on_result.stdout.decode().splitlines()[0] == 'SUCCESS':
                print(host_ip, "was turned on")
            else:
                print(host_ip, "wasn't turned on becouse of the error")
    else:
        print("coldn't connect to", host_ip)

def get_amt_list():
    amt_from_file = open(amt_list,"rt")
    for x in amt_from_file:
        pwr_meshcmd(x.rstrip())
        print('')
    amt_from_file.close()

get_amt_list()
