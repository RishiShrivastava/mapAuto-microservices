# ---
# PortXmlParser Microservice: FastAPI version of the original portXmllParser.py script
# This service exposes Nmap XML parsing as REST endpoints.
#
# Key Endpoints:
#   - /status: Health check
#   - /parse-xml: Parse an Nmap XML file
#
# The core logic should be adapted from the original portXmllParser.py script.
# ---

from fastapi import FastAPI, Query, HTTPException
import os
from dotenv import load_dotenv
import xml.etree.ElementTree as ET

app = FastAPI(title="PortXmlParser Microservice")

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

@app.get("/status")
def status():
    return {"status": "PortXmlParser microservice is running"}


@app.post("/parse-xml")
def parse_xml(xml_path: str = Query(..., description="Path to Nmap XML file")):
    """
    Parse the given Nmap XML file and return open TCP/UDP ports and their services.
    Replicates the workflow of portXmllParser.py.
    Includes fail-safes: file validation, error handling, and resource limits.
    """
    try:
        # Fail-safe: Validate file path
        if not xml_path or xml_path.strip() == "":
            raise HTTPException(status_code=400, detail="XML file path cannot be empty")
        
        # Fail-safe: Check if file exists and is readable
        if not os.path.exists(xml_path):
            raise HTTPException(status_code=404, detail="XML file not found")
        
        if not os.access(xml_path, os.R_OK):
            raise HTTPException(status_code=403, detail="XML file is not readable")
        
        # Fail-safe: Check file size to prevent parsing huge files
        file_size = os.path.getsize(xml_path)
        if file_size > 50 * 1024 * 1024:  # 50MB limit
            raise HTTPException(status_code=413, detail="XML file too large (max 50MB)")
        
        # Fail-safe: Parse XML with error handling
        try:
            root = ET.parse(xml_path).getroot()
        except ET.ParseError as e:
            raise HTTPException(status_code=400, detail=f"Invalid XML format: {e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error parsing XML: {e}")
        
        open_udp_ports = {}
        open_tcp_ports = {}
        port_state = None
        parsed_ports = 0
        
        # Fail-safe: Limit number of ports processed to prevent resource exhaustion
        MAX_PORTS = 1000
        
        for port in root.iter('port'):
            if parsed_ports >= MAX_PORTS:
                break
                
            try:
                port_id = int(port.attrib.get("portid", 0))
                port_protocol = str(port.attrib.get("protocol", "none")).lower()
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
                        
                if (port_state == 'open' or port_state == 'open|filtered') and port_protocol == 'tcp':
                    open_tcp_ports[port_id] = port_service
                elif (port_state == 'open' or port_state == 'open|filtered') and port_protocol == 'udp':
                    open_udp_ports[port_id] = port_service
                    
                parsed_ports += 1
                
            except (ValueError, TypeError) as e:
                # Skip malformed port entries
                continue
        
        result = {
            "open_tcp_ports": open_tcp_ports,
            "open_udp_ports": open_udp_ports,
            "total_tcp_ports": len(open_tcp_ports),
            "total_udp_ports": len(open_udp_ports),
            "parsed_ports": parsed_ports,
            "file_size_bytes": file_size
        }
        
        # Fail-safe: Add warning if port limit was reached
        if parsed_ports >= MAX_PORTS:
            result["warning"] = f"Port limit reached ({MAX_PORTS}). Some ports may not be included."
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")

# ---
# EXPLANATION:
# - This service exposes a /parse-xml endpoint to parse Nmap XML files via HTTP.
# - Replace the stub logic with the full workflow from portXmllParser.py for full functionality.
# ---
