# AMT_Network_Sync
Sync AMT network settings and System network settings on Ubuntu 18.04

Python script have to read AMT status and network settings using meshcmd, read system network settings using ip or nmcli and sync AMT network settings in accordance with System settings using meshcmd

Python script have to be run as sudo due to meshcmd requirements.
For example: 
$sudo python3 ip_test.py

Script compare IP seetings of AMT and Linux system (ubuntu 18.04) and change AMT seetings in accordance with system settings
