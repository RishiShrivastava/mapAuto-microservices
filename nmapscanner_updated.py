# Author
#       Rishi Kumar - Rishi_kumar2@dell.com
#       Yadu Krishnan - Yadu_krishnan_1@dell.com


# import nmap
import os
import shlex
import subprocess
import time
import sys
import xml.etree.ElementTree as ET

# Check to make sure the user has version 2.x of python, if not, exit.
current_maj_version = sys.version_info.major
if current_maj_version != 2:
    print('This script must be run with Python version 2.x')
    exit()

# Globals

nsedir = '/usr/share/nmap/scripts'
tempscriptlist = []
nselist = []
selectednseexecutionlist = []  # Final Execution script list
scriptTypeDict = dict([
    (1, 'acarsd'), (2, 'address'), (3, 'afp'), (4, 'ajp'),
    (5, 'allseeingeye'), (6, 'amqp'), (7, 'asn'), (8, 'auth'),
    (9, 'backorifice'), (10, 'bacnet'), (11, 'banner'), (12, 'bitcoin')
    , (13, 'bitcoinrpc'), (14, 'bittorrent'), (15, 'bjnp'), (16, 'broadcast')
    , (17, 'cassandra'), (18, 'cccam'), (19, 'cisc'), (20, 'citrix')
    , (21, 'clamav'), (22, 'clock'), (23, 'coap'), (24, 'couchdb')
    , (25, 'creds'), (26, 'cups'), (27, 'cvs'), (28, 'daap')
    , (29, 'daytime'), (30, 'db2'), (31, 'deluge'), (32, 'dhcp')
    , (33, 'dict'), (34, 'distcc'), (35, 'dns'), (36, 'docker')
    , (37, 'domcon'), (38, 'domino'), (39, 'dpap'), (40, 'drda')
    , (41, 'duplicates'), (42, 'eap'), (43, 'enip'), (44, 'epmd')
    , (45, 'eppc'), (46, 'fcrdns'), (47, 'finger'), (48, 'fingerprint')
    , (49, 'firewalk'), (50, 'firewall'), (51, 'flume'), (52, 'fox')
    , (53, 'freelancer'), (54, 'ftp'), (55, 'ganglia'), (56, 'giop')
    , (57, 'gkrellm'), (58, 'gopher'), (59, 'gpsd'), (60, 'hadoop')
    , (61, 'hbase'), (62, 'hddtemp'), (63, 'hnap'), (64, 'hostmap')
    , (65, 'http'), (66, 'iax2'), (67, 'icap'), (68, 'iec')
    , (69, 'ike'), (70, 'imap'), (71, 'impress'), (72, 'informix')
    , (73, 'ip'), (74, 'ipidseq'), (75, 'ipmi'), (76, 'ipv6')
    , (77, 'irc'), (78, 'iscsi'), (79, 'isns'), (80, 'jdwp')
    , (81, 'knx'), (82, 'krb5'), (83, 'ldap'), (84, 'lexmark')
    , (85, 'llmnr'), (86, 'lltd'), (87, 'lu'), (88, 'maxdb')
    , (89, 'mcafee'), (90, 'membase'), (91, 'memcached'), (92, 'metasploit')
    , (93, 'mikrotik'), (94, 'mmouse'), (95, 'modbus'), (96, 'mongodb')
    , (97, 'mqtt'), (98, 'mrinfo'), (99, 'msrpc'), (100, 'ms')
    , (101, 'mtrace'), (102, 'murmur'), (103, 'mysql'), (104, 'nat')
    , (105, 'nbd'), (106, 'nbstat'), (107, 'ncp'), (108, 'ndmp')
    , (109, 'nessus'), (110, 'netbus'), (111, 'nexpose'), (112, 'nfs')
    , (113, 'nje'), (114, 'nntp'), (115, 'nping'), (116, 'nrpe')
    , (117, 'ntp'), (118, 'omp2'), (119, 'omron'), (120, 'openlookup')
    , (121, 'openvas'), (122, 'openwebnet'), (123, 'oracle'), (124, 'ovs')
    , (125, 'p2p'), (126, 'path'), (127, 'pcanywhere'), (128, 'pcworx')
    , (129, 'pgsql'), (130, 'pjl'), (131, 'pop3'), (132, 'pptp')
    , (133, 'puppet'), (134, 'qconn'), (135, 'qscan'), (136, 'quake1')
    , (137, 'quake3'), (138, 'rdp'), (139, 'realvnc'), (140, 'redis')
    , (141, 'resolveall'), (142, 'reverse'), (143, 'rexec'), (144, 'rfc868')
    , (145, 'riak'), (146, 'rlogin'), (147, 'rmi'), (148, 'rpcap')
    , (149, 'rpc'), (150, 'rpcinfo'), (151, 'rsa'), (152, 'rsync')
    , (153, 'rtsp'), (154, 'rusers'), (155, 's7'), (156, 'samba')
    , (157, 'script'), (158, 'servicetags'), (159, 'shodan'), (160, 'sip')
    , (161, 'skypev2'), (162, 'smb2'), (163, 'smb'), (164, 'smtp')
    , (165, 'sniffer'), (166, 'snmp'), (167, 'socks'), (168, 'ssh2')
    , (169, 'ssh'), (170, 'sshv1'), (171, 'ssl'), (172, 'sslv2')
    , (173, 'sstp'), (174, 'stun'), (175, 'stuxnet'), (176, 'supermicro')
    , (177, 'svn'), (178, 'targets'), (179, 'teamspeak2'), (180, 'telnet')
    , (181, 'tftp'), (182, 'tls'), (183, 'tn3270'), (184, 'tor')
    , (185, 'traceroute'), (186, 'tso'), (187, 'ubiquiti'), (188, 'unittest')
    , (189, 'unusual'), (190, 'upnp'), (191, 'url'), (192, 'ventrilo')
    , (193, 'versant'), (194, 'vmauthd'), (195, 'vmware'), (196, 'vnc')
    , (197, 'voldemort'), (198, 'vtam'), (199, 'vulners'), (200, 'vuze')
    , (201, 'wdb'), (202, 'weblogic'), (203, 'whois'), (204, 'wsdd')
    , (205, 'x11'), (206, 'xdmcp'), (207, 'xmlrpc'), (208, 'xmpp')
])  # type: dictionary


# Make list of available nse scripts in default directory
def make_nsescript_list():
    # Check to make sure nmap Scripts exist
    global nselist
    if not os.path.isdir(nsedir):
        print('Cannot locate default script directory')
        exit()
    else:
        for scriptfile in os.listdir(nsedir):  # type: str
            if scriptfile.endswith(".nse"):
                nselist.append(scriptfile)
        nselist.sort()
        # print('Script Count: '+str(len(nselist)))
        # print(nselist)
        # print('\t******** AVAILABLE SCRIPT TYPES *********')
        # for k, v in scriptTypeDict.iteritems():
        #     print k, v  # Print the scriptTypeDict
        # print('All Correspronding '+str(v)+" Scripts")
        # for nsescript in nselist:
        #     if str(nsescript).startswith(v):
        #         print nsescript


# Build the TempScript List
# not used anymore

# def build_intermediate_nsescriptlist(key):
#     global tempscriptlist
#     if key == 0:
#         print('EXITING....')
#         exit()
#     elif key == 'all' or key == 'ALL':
#         return nselist
#     # print scriptTypeDict.keys()
#     if int(key) in scriptTypeDict.keys():
#         print('Found the following Scripts for the type ' + scriptTypeDict[int(key)])
#         for nsescript in nselist:
#             if str(nsescript).startswith(scriptTypeDict[int(key)]):
#                 tempscriptlist.append(nsescript)
#                 print nsescript,
#     tempscriptlist = list(dict.fromkeys(tempscriptlist))
#     # print(tempscriptlist)
#     return tempscriptlist


# Makes the list of executable scripts for each port depending on the service associated with it
# pass the dict of all the {port:'service}
# return {port1: [script1,script2...] , port2: [script1,script2...]}
# selects the scripts based on sub-string match only
def make_executable_script_list_for_service(portsDict):
    # User input loop
    global selectednseexecutionlist
    from collections import defaultdict
    port_script_dict = defaultdict(list)

    make_nsescript_list()

    # print portsDict.keys()
    for port in portsDict.keys():
        # print port
        # print portsDict[port]
        for item in nselist:
            if (item.find(portsDict[port]) != -1):
                port_script_dict[port].append(item)

    print('\nScripts found for corresponding OpenPorts: ' + str(dict(port_script_dict)))
    return dict(port_script_dict)


# Parse the Port Scan file for Open WAF Ports
# Common parser for all port scan scripts
# Return open ports & service associated with those ports
# Returns only UDP & TCP ports
def parse_port_file(portscanxmlfile):
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
            if port_service.find('postgresql') != -1:
                port_service = 'pgsql'
            elif port_service.find('nfs') != -1:
                port_service = 'nfs'
            elif port_service.find('rpc') != -1:
                port_service = 'rpc'
            elif port_service.find('ajp') != -1:
                port_service = 'ajp'
        if (port_state == 'open' or port_state == 'open|filtered') and port_protocol == 'tcp':
            open_tcp_ports[port_id] = port_service
        elif (port_state == 'open' or port_state == 'open|filtered') and port_protocol == 'udp':
            open_udp_ports[port_id] = port_service
    return open_udp_ports, open_tcp_ports


# Parse the osScan file for os fingerprint probablilities
def parse_osscanxml_file(osscanxmlfile):
    import os as osimport
    if not osimport.path.exists(osscanxmlfile):
        print('Cannot access file : ' + str(osscanxmlfile))
        print('EXITING....')
        exit()
    # root = ET.fromstring(osscanxmlfile_as_string) #Use this when fn parameter is a string
    root = ET.parse(str(osscanxmlfile)).getroot()
    for osImport in root.iter('os'):
        for os_guessed in osImport.iter('osclass'):
            os_name = str(os_guessed.attrib.get("osfamily", 0)).lower() + str(os_guessed.attrib.get("osgen", 0)).lower()
            os_accuracy = int(os_guessed.attrib.get("accuracy", 0))
            os_type = str(os_guessed.attrib.get("type", "UNKOWN"))
            if os_accuracy > 0 and "UNKOWN" != os_type:
                print('OS: ' + os_name + '     Accuracy Level: ' + str(os_accuracy) + ' OSType: ' + os_type)


# get WAF open ports
# return dict {UDPOpenPorts,services} , dict {TCPOpenPorts,services}
def nmap_wafport_finder(scanip):
    portscanfile = os.getcwd() + "/" + "WAFPortScan_" + scanip + ".xml"
    portcmd = "/usr/bin/nmap -sU -sS --script http-waf-detect --script-args=\"http-waf-detect.aggro\" -oX {0} -sV {1}".format(
        portscanfile, scanIP)
    if portcmd is None:
        print("DEBUG- Empty Command")
    print('\nPerforming OpenPorts(UDP,TCP) Scan with WAF detection on: ' + scanip)
    print(
            "Note: This scan can take upto 15 Mins on a single target.Please wait while scan executes in background...\n\nExec Command:  " + portcmd)
    args = shlex.split(portcmd)
    try:
        portscanresult = subprocess.check_output(args)
        # print(portscanresult)
        if os.path.exists(str(portscanfile)):
            print('\nWAF PortScan Result at : ' + str(portscanfile))
    except Exception:
        print("Error in invoking WAF PortScan Command: " + str(portcmd))
        exit()
    finally:
        print("***********Successfully stored WAF-OpenPort Scan File************")
        # parse the xml for open ports
        return parse_port_file(portscanfile)


# get OS Fingerprint
# writes result to file
def nmap_osscan(scanip):
    oscanxmlfile = '/root/Downloads/OSScan_' + scanip + '.xml'  # type: str
    osscancmd = "/usr/bin/nmap -r -O --osscan-guess -oX {0} -sV {1}".format(
        oscanxmlfile, scanip)
    print('Performing OS Fingerprinting on ' + scanIP)
    print("Exec Command:  " + osscancmd)
    args = shlex.split(osscancmd)
    try:
        osscanresult = subprocess.check_output(args)
        # print(osscanresult)
        if os.path.exists(str(oscanxmlfile)):
            print('\nOSScan Result at : ' + str(oscanxmlfile))
    except Exception:
        print("Error in invoking OSScan Command: " + str(osscancmd))
        pass
    finally:
        print("***********Successfully stored OS-Scan Result File************")
        parse_osscanxml_file(oscanxmlfile)


# perform hail mary script scan
# scan all ports, aggressive, fullyverbose, all scripts
def execute_aggressive_nsescript_scan(nsescriptdir):
    if not os.path.isdir(str(nsescriptdir)):
        print('Cannot access directory : ' + str(nsescriptdir))
        print('EXITING....')
        exit()
    try:
        scripts = []
        for scriptfile in os.listdir(nsescriptdir):  # type: str
            if file.endswith(".nse"):
                scripts.append(scriptfile)
        scripts.sort()
        timeNow = time.strftime('%d%b%Y--%H%M%S')
        outFilePath = os.getcwd() + "/" + "nmap_Aggressive_Result_" + scanIP + "_" + timeNow + ".txt"  # type: String
        print("Result File can be found at:  " + outFilePath)
        try:
            outFile = open(outFilePath, 'w+')
        except Exception:
            print(
                "\n\nUnable to create output file. Please check directory permissions\n\nProgram will display output in console.")
            outFile.close()
        finally:
            pass
        print("CWD: " + os.getcwd() + "\n\n")
        outFile.write(
            "Running Scan on " + scanIP + "\n------------------------------------------------------------------\n\n")
        # nm=nmap.PortScanner()
        print ('Commencing Scan for Scripts: ' + scripts + ' \nOn ALL Ports: ')
        outFile.write('\nCommencing Scan for Scripts: ' + scripts + ' \nOn ALL Ports: ')
        for execute_script in scripts:
            print ('\nExecuting Script: ' + str(execute_script))
            outFile.write('\nExecuting Script: ' + str(execute_script))
            cmd = "/usr/bin/nmap -A -sV -sU -T5 -vv --script /usr/share/nmap/scripts/" + execute_script + " --script-timeout 7m " + scanIP
            print("Exec Command:  " + cmd)
            outFile.write("\nExec Command: " + cmd + "\n")
            args = shlex.split(cmd)
            try:
                result = subprocess.check_output(args)
                print(result)
                outFile.write(result)
            except Exception:
                print("Error in invoking Script: " + execute_script)
                outFile.write("\nError invoking Script: " + execute_script + "\n")
                pass
    finally:
        print("\n\n************Aggressive Execution complete.....************")
        outFile.close()


# execute command for IP, dictionary of [port:nse_scripts]
# writes the result to file
def execute_nsescript_scan(scanip, scan_port_scripts_dict):
    # scan_port_scripts_dict : {port1:'[script1,script2...]',' port2:'[script1,script2...]'}
    if len(scanip) <= 0 or len(scan_port_scripts_dict.keys()) <= 0:
        print("Cannot Continue scan. INVALID PARAMETERS\tEXITING.....")
        exit()
    try:
        print('\n\nPerforming Intelligent Script Scan on: ' + str(scanip))
        timeNow = time.strftime('%d%b%Y--%H%M%S')
        outFilePath = os.getcwd() + "/" + "nmap_Result_" + scanIP + "_" + timeNow + ".txt"  # type: String
        print("Result File can be found at:  " + outFilePath)
        try:
            outFile = open(outFilePath, 'w+')
        except Exception:
            print(
                "\n\nUnable to create output file. Please check directory permissions\n\nProgram will display output in console.")
            outFile.close()
        finally:
            pass
        # print("CWD: " + os.getcwd() + "\n\n")
        outFile.write(
            "Running Scan on " + scanIP + "\n------------------------------------------------------------------\n\n")

        for port in scan_port_scripts_dict.keys():
            print ('Commencing Scan for Port: ' + str(port) + ' \nWith Scripts: ' + str(scan_port_scripts_dict[port]))
            outFile.write(
                '\nCommencing Scan for Port: ' + str(port) + ' \nWith Scripts: ' + str(scan_port_scripts_dict[port]))
            for execute_script in scan_port_scripts_dict[port]:
                print ('\nExecuting Script: ' + str(execute_script))
                outFile.write('\nExecuting Script: ' + str(execute_script))
                cmd = "/usr/bin/nmap -p " + str(
                    port) + " --min-parallelism 16 --script /usr/share/nmap/scripts/" + execute_script + " " + scanIP
                print("Exec Command:  " + cmd)
                outFile.write("\nExec Command: " + cmd + "\n")
                args = shlex.split(cmd)
                try:
                    result = subprocess.check_output(args)
                    print(result)
                    outFile.write(result)
                except Exception:
                    print("Error in invoking Script: " + execute_script)
                    outFile.write("\nError invoking Script: " + execute_script + "\n")
                    pass
    finally:
        print("\n\n************Execution complete.....************")
        outFile.close()


# MAIN

# Dir in which NMAP Scripts reside
scanScripts = os.listdir("/usr/share/nmap/scripts/")
ports_services_dict = {}
scanIP = raw_input("IP: ")  # type: str
nmap_osscan(scanIP)
scanUDPPorts, scanTCPPorts = nmap_wafport_finder(scanIP)
#
ports_services_dict.update(scanUDPPorts)
ports_services_dict.update(scanTCPPorts)

ports_scripts_dict = make_executable_script_list_for_service(
    ports_services_dict)  # List of scripts for the specified port,service
# For each open port, run the corresponding scripts alone
execute_nsescript_scan(scanIP, ports_scripts_dict)
