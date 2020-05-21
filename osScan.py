import shlex
import subprocess
import sys
import os
import xml.etree.ElementTree as ET

oscanxmlfile =  '/root/Downloads/OSScan_45.33.32.156.xml'
scanIP = raw_input("IP: ")
osscancmd = "/usr/bin/nmap -r -O --osscan-guess -oX {0} -sV {1}".format(
        oscanxmlfile, scanIP)

print("Firing Command:  " + osscancmd)
args = shlex.split(osscancmd)
try:
    osscanresult = subprocess.check_output(args)
    print(osscanresult)
    if os.path.exists(str(oscanxmlfile)):
        print('\nOSScan Result at : ' + str(oscanxmlfile))
except Exception:
    print("Error in invoking OSScan Command: " + str(osscancmd))
    pass
finally:
    print("\n***********Successfully stored Port List File************")
    # parse the xml for open ports
    #return parse_port_file(portscanfile)
