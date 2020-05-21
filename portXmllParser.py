import sys
import os
import xml.etree.ElementTree as ET

portscanxmlfile =  '/root/Downloads/WAFPortScan_100.96.20.117.xml'
open_udp_ports = {} #{port:"service"}
open_tcp_ports = {} #{port:"service"}
port_scriptDict = {520: 'route', 123: 'ntp', 68: 'dhcpc', 80: 'http', 9929: 'nping-echo', 22: 'ssh', 31337: 'tcpwrapped'}
if not os.path.exists(str(portscanxmlfile)):
    print('Cannot access file : ' + str(portscanxmlfile))
    print('EXITING....')
    exit()
# Begin parsing the file
# root = ET.fromstring(portscanxmlfile_as_string) #Use this when fn parameter is a string
root = ET.parse(str(portscanxmlfile)).getroot()

#get the OS Fingerprint
# for service in root.iter('service'):
#     os_fingerprint = (service.attrib.get("ostype",0))
#     if os_fingerprint > 0 :
#         print('OS ' + str(service.attrib["ostype"]))

open_udp_ports = {}  # {port:"service"}
open_tcp_ports = {}  # {port:"service"}
if not os.path.exists(str(portscanxmlfile)):
    print('Cannot access file : ' + str(portscanxmlfile))
    print('EXITING....')
    exit()
# root = ET.fromstring(portscanxmlfile_as_string) #Use this when fn parameter is a string
root = ET.parse(str(portscanxmlfile)).getroot()
port_state = None
# get open port IDs
for port in root.iter('port'):
    port_id = int(port.attrib.get("portid", 0))
    port_protocol = str(port.attrib.get("protocol", "none")).lower()
    for state in port.iter('state'):
        port_state = str(state.attrib.get("state", 0)).lower()
    for service in port.iter('service'):
        port_service = str(service.attrib.get("name", "none")).lower()
        if (port_service.find('postgresql') != -1 ):
            port_service = 'pgsql'
        elif (port_service.find('nfs') != -1 ):
            port_service = 'nfs'
        elif (port_service.find('rpc') != -1):
            port_service = 'rpc'
    if (port_state == 'open' or port_state == 'open|filtered') and port_protocol == 'tcp':
        open_tcp_ports[port_id] = port_service
    elif (port_state == 'open' or port_state == 'open|filtered') and port_protocol == 'udp':
        open_udp_ports[port_id] = port_service
print open_tcp_ports
print open_udp_ports