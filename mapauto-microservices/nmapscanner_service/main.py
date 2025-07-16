# ---
# NmapScanner Microservice: FastAPI version of the original nmapscanner_updated.py script
# This service exposes intelligent Nmap scanning as REST endpoints.
#
# Key Endpoints:
#   - /status: Health check
#   - /scan: Run a scan for a given IP
#
# The core logic should be adapted from the original nmapscanner_updated.py script.
# ---


from fastapi import FastAPI, Query, HTTPException
import os
from dotenv import load_dotenv
import subprocess
import shlex
import xml.etree.ElementTree as ET
import time
from collections import defaultdict
from typing import Optional
import ipaddress
# =Juggernaut= Added imports for timestamped folder creation
import datetime
import pathlib


app = FastAPI(title="NmapScanner Microservice")

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

# =Juggernaut= Added function to create timestamped result folders
def create_scan_folder(ip: str) -> str:
    """Create a timestamped folder for scan results."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_name = f"nmapscanner_{ip}_{timestamp}"
    scan_folder = os.path.join("/app/scan_results", folder_name)
    pathlib.Path(scan_folder).mkdir(parents=True, exist_ok=True)
    return scan_folder

@app.get("/status")
def status():
    return {"status": "NmapScanner microservice is running"}


# ---
# Ported logic from nmapscanner_updated.py
# ---

@app.post("/scan")
def scan(ip: str = Query(..., description="Target IP address"),
         timeout: Optional[int] = Query(600, description="Total timeout in seconds (default: 600)")):
    """
    Run an intelligent Nmap scan for the given IP address.
    This replicates the workflow of nmapscanner_updated.py:
    1. Run OS scan and WAF port scan, saving results as XML.
    2. Parse XML to extract open ports and services.
    3. Match Nmap scripts to each open port based on service.
    4. Run the relevant scripts for each port and return results as JSON.
    
    Includes fail-safes: IP validation, timeouts, error handling, and resource limits.
    """
    # Fail-safe: Validate IP address format
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid IP address format")
    
    nsedir = '/usr/share/nmap/scripts'
    
    # Fail-safe: Check if script directory exists
    if not os.path.isdir(nsedir):
        raise HTTPException(status_code=500, detail=f"Nmap script directory not found: {nsedir}")
    
    results = {
        "target_ip": ip,
        "os_scan": None,
        "waf_port_scan": None,
        "open_ports": {},
        "port_scripts": {},
        "script_results": {},
        "errors": [],
        "timeout_used": timeout,
        "scan_folder": None  # =Juggernaut= Added scan folder info
    }
    
    try:
        # =Juggernaut= Create timestamped folder for this scan
        scan_folder = create_scan_folder(ip)
        results["scan_folder"] = scan_folder
        
        # 1. Run OS scan with fail-safes
        oscanxmlfile = os.path.join(scan_folder, f"OSScan_{ip}.xml")
        osscancmd = f"nmap -T4 --max-retries 1 --host-timeout 60s -O --osscan-guess -oX {oscanxmlfile} {ip}"
        args = shlex.split(osscancmd)
        try:
            result = subprocess.run(args, capture_output=True, text=True, timeout=120, check=False)
            if result.returncode == 0:
                results["os_scan"] = f"OS scan completed, XML saved to {oscanxmlfile}"
            else:
                results["errors"].append(f"OS scan warning: {result.stderr}")
                results["os_scan"] = "OS scan completed with warnings"
        except subprocess.TimeoutExpired:
            results["errors"].append("OS scan timed out")
            results["os_scan"] = None
        except Exception as e:
            results["errors"].append(f"OS scan failed: {e}")
            results["os_scan"] = None

        # 2. Run WAF port scan with fail-safes
        portscanfile = os.path.join(scan_folder, f"WAFPortScan_{ip}.xml")
        portcmd = f"nmap -T4 --max-retries 1 --host-timeout 60s -sS --top-ports 1000 --script http-waf-detect -oX {portscanfile} {ip}"
        args = shlex.split(portcmd)
        try:
            result = subprocess.run(args, capture_output=True, text=True, timeout=180, check=False)
            if result.returncode == 0:
                results["waf_port_scan"] = f"WAF port scan completed, XML saved to {portscanfile}"
            else:
                results["errors"].append(f"WAF port scan warning: {result.stderr}")
                results["waf_port_scan"] = "WAF port scan completed with warnings"
        except subprocess.TimeoutExpired:
            results["errors"].append("WAF port scan timed out")
            results["waf_port_scan"] = None
        except Exception as e:
            results["errors"].append(f"WAF port scan failed: {e}")
            results["waf_port_scan"] = None

        # 3. Parse port scan XML for open ports and services
        open_udp_ports = {}
        open_tcp_ports = {}
        if os.path.exists(portscanfile):
            try:
                root = ET.parse(portscanfile).getroot()
                for port in root.iter('port'):
                    port_id = int(port.attrib.get("portid", 0))
                    port_protocol = str(port.attrib.get("protocol", "none")).lower()
                    port_state = None
                    port_service = None
                    for state in port.iter('state'):
                        port_state = str(state.attrib.get("state", 0)).lower()
                    for service in port.iter('service'):
                        port_service = str(service.attrib.get("name", "none")).lower()
                        if 'postgresql' in port_service:
                            port_service = 'pgsql'
                        elif 'nfs' in port_service:
                            port_service = 'nfs'
                        elif 'rpc' in port_service:
                            port_service = 'rpc'
                        elif 'ajp' in port_service:
                            port_service = 'ajp'
                    if (port_state == 'open' or port_state == 'open|filtered') and port_protocol == 'tcp':
                        open_tcp_ports[port_id] = port_service
                    elif (port_state == 'open' or port_state == 'open|filtered') and port_protocol == 'udp':
                        open_udp_ports[port_id] = port_service
            except Exception as e:
                results["errors"].append(f"Error parsing port scan XML: {e}")
        else:
            results["errors"].append(f"Port scan XML file not found: {portscanfile}")

        # Merge UDP and TCP ports
        ports_services_dict = {}
        ports_services_dict.update(open_udp_ports)
        ports_services_dict.update(open_tcp_ports)
        results["open_ports"] = ports_services_dict

        # 4. Make list of available nse scripts
        nselist = []
        try:
            for scriptfile in os.listdir(nsedir):
                if scriptfile.endswith(".nse"):
                    nselist.append(scriptfile)
            nselist.sort()
        except Exception as e:
            results["errors"].append(f"Could not list scripts: {e}")

        # 5. For each open port, find matching scripts by service substring
        port_script_dict = defaultdict(list)
        for port, service in ports_services_dict.items():
            for item in nselist:
                if service and (item.find(service) != -1):
                    port_script_dict[port].append(item)
        
        # Fail-safe: Limit scripts per port to prevent resource exhaustion
        for port in port_script_dict:
            if len(port_script_dict[port]) > 5:
                port_script_dict[port] = port_script_dict[port][:5]
                results["errors"].append(f"Limited port {port} to 5 scripts")
        
        results["port_scripts"] = {str(port): scripts for port, scripts in port_script_dict.items()}

        # 6. For each open port, run the corresponding scripts with fail-safes
        script_results = defaultdict(list)
        remaining_timeout = timeout - 300  # Reserve 300s for initial scans
        
        for port, scripts in port_script_dict.items():
            if remaining_timeout <= 0:
                results["errors"].append("Global timeout reached, stopping script execution")
                break
                
            script_timeout = min(30, remaining_timeout // len(scripts)) if scripts else 30
            
            for execute_script in scripts:
                if remaining_timeout <= 0:
                    break
                    
                cmd = f"nmap -T4 --max-retries 1 -p {port} --script {execute_script} {ip}"
                args = shlex.split(cmd)
                try:
                    result = subprocess.run(args, capture_output=True, text=True, 
                                          timeout=script_timeout, check=False)
                    if result.returncode == 0:
                        script_results[str(port)].append({"script": execute_script, "output": result.stdout})
                    else:
                        script_results[str(port)].append({"script": execute_script, "error": result.stderr or "Script failed"})
                except subprocess.TimeoutExpired:
                    script_results[str(port)].append({"script": execute_script, "error": "Script timed out"})
                except Exception as e:
                    script_results[str(port)].append({"script": execute_script, "error": str(e)})
                
                remaining_timeout -= script_timeout
                
        results["script_results"] = script_results

        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"NmapScanner error: {e}")

# ---
# EXPLANATION:
# - This service exposes a /scan endpoint to trigger Nmap scans via HTTP.
# - Replace the stub logic with the full workflow from nmapscanner_updated.py for full functionality.
# ---
