#import nmap
import os
import shlex
import subprocess
import time

# Author 
#       Rishi Kumar - Rishi_kumar2@dell.com
#       Yadu Krishnan - Yadu_krishnan_1@dell.com






#get available ports to scan
def nmap_port_finder(scanIP):

    try:
        socket.inet_aton (scanIP)
        try:
            outFile_Port = open(os.getcwd()+"/"+"nmap_Port_Scan"+scanIP+"_"+scanIP+".txt",'w+')
        except Exception:
            print("\n\nUnable to create output file. Please check directory permissions/n/nProgram will display output in console.")
            outFile.close()
    except Exception:
        print("\nIP invalid or Unreachable")
        return #Dont proceed further
    finally:
        #IP valid, ourFile_Port created
        cmd = "/usr/bin/nmap -A -O -V -p "+scanIP
        pass
    if cmd is None:
        print("DEBUG- Empty Command")
    print("Firing Command:  "+cmd)
    outFile.write("\nFiring Command: "+cmd+"\n")
    args = shlex.split(cmd)
    try:
        result = subprocess.check_output(args)
        print(result)
        outFile.write(result)
    except Exception:
        print("Error in invoking Script: "+file)
        outFile.write("\nError invoking Script: "+file+"\n")
        pass
    finally:
        print("\n\n***********Successfully stored Port List File************")
        outFile.close()



#def parse_port_file():
	   
#Dir in which NMAP Scripts reside
scanScripts = os.listdir("/usr/share/nmap/scripts/")
scanIP = raw_input("IP: ")
#scanPort = raw_input("PORT: ")
#rawOut = raw_input("Show RAW Output(XML) (y/n) ? ")  
print "Triggering NMAP on IP %(ip)s PORT [1-65535]" % { "ip":scanIP }
print "******************************************************************"
try:
    timeNow = time.strftime('%d%b%Y--%H%M%S')
    print("Result File can be found at:  "+os.getcwd()+"/"+"nmap_Result_"+scanIP+"_"+timeNow+".txt",'w+')
    try:
        outFile = open(os.getcwd()+"/"+"nmap_Result_"+scanIP+"_"+timeNow+".txt",'w+')
    except Exception:
        print("\n\nUnable to create output file. Please check directory permissions/n/nProgram will display output in console.")
        outFile.close()
    finally:
         pass
    print("CWD: "+os.getcwd()+"\n\n")
    outFile.write("Running Scan on "+scanIP+"\n------------------------------------------------------------------\n\n")
    #nm=nmap.PortScanner()
    for file in scanScripts:
        print("NMAP SCRIPT:  " +file)
        outFile.write("\nNMAP SCRIPT: " +file+"\n")
        cmd = "/usr/bin/nmap -A -p- --script /usr/share/nmap/scripts/"+file+" "+scanIP
        print("Firing Command:  "+cmd)
        outFile.write("\nFiring Command: "+cmd+"\n")
        args = shlex.split(cmd)
        try:
            result = subprocess.check_output(args)
            print(result)
            outFile.write(result)
        except Exception:
            print("Error in invoking Script: "+file)
            outFile.write("\nError invoking Script: "+file+"\n")
            pass
finally:
    print("/n/nExecution complete.....")
    pass
    #Enable below code for python nmap exec & byepass shell exec

    """
    nm=nmap.PortScanner()
    scan_dict = nm.scan(scanIP, scanPort, arguments='--script /usr/share/nmap/scripts/%(filename)s' % { "filename":file } )
    if (str(rawOut) == 'y') or (str(rawOut) =='Y'):
        print( str(scan_dict) )
    #print(nm.csv())
    print("##############################")
    print("REPORT SCAN: ")
    print("    IP: "+scanIP)
    try:
            for osmatch in nm[scanIP]['osmatch']:
                print('     OS:{0} - {1}%'.format(osmatch['name'], osmatch['accuracy']))
                print('           OsClass: {0}|{1}|{2}|{3}|{4}|{5}%'.format(
                                                           osmatch['osclass'][0]['type'],
                                                           osmatch['osclass'][0]['vendor'],
                                                           osmatch['osclass'][0]['osfamily'],
                                                           osmatch['osclass'][0]['osgen'],
                                                           osmatch['osclass'][0]['osgen'])
                )
    except:
            pass

    # TODO: port details, services, etc...
    try:
            for proto in nm[scanIP].all_protocols():
                print('        -----PORTS-----')
                print('        Protocol : %s' % proto)
                lport = list(nm[scanIP][proto].keys())
                lport.sort()
                for port in lport:
                    print('        PORT : %s\tSTATE : %s' % (port, nm[scanIP][proto][port]['state']))
    except:
            pass
"""
