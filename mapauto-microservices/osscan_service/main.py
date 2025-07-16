# ---
# OSScan Microservice: FastAPI version of the original osScan.py script
# This service exposes OS fingerprinting as REST endpoints.
#
# Key Endpoints:
#   - /status: Health check
#   - /os-scan: Run OS fingerprinting for a given IP
#
# The core logic should be adapted from the original osScan.py script.
# ---

from fastapi import FastAPI, Query, HTTPException
import os
from dotenv import load_dotenv
import subprocess
import shlex
import ipaddress
from typing import Optional
# =Juggernaut= Added imports for timestamped folder creation
import datetime
import pathlib

app = FastAPI(title="OSScan Microservice")

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

# =Juggernaut= Added function to create timestamped result folders
def create_scan_folder(ip: str) -> str:
    """Create a timestamped folder for scan results."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_name = f"osscan_{ip}_{timestamp}"
    scan_folder = os.path.join("/app/scan_results", folder_name)
    pathlib.Path(scan_folder).mkdir(parents=True, exist_ok=True)
    return scan_folder

@app.get("/status")
def status():
    return {"status": "OSScan microservice is running"}


@app.post("/os-scan")
def os_scan(ip: str = Query(..., description="Target IP address"),
           timeout: Optional[int] = Query(120, description="Timeout in seconds (default: 120)")):
    """
    Run OS fingerprinting for the given IP address.
    Replicates the workflow of osScan.py:
    - Runs an Nmap OS scan with XML output.
    - Returns the command, output, and result file location as JSON.
    - Includes fail-safes: IP validation, timeouts, and error handling.
    """
    # Fail-safe: Validate IP address format
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid IP address format")
    
    try:
        # =Juggernaut= Create timestamped folder for this scan
        scan_folder = create_scan_folder(ip)
        oscanxmlfile = os.path.join(scan_folder, f"OSScan_{ip}.xml")
        
        # Fail-safe: Use safer nmap options to prevent hanging
        osscancmd = f"nmap -T4 --max-retries 1 --host-timeout 60s -O --osscan-guess -oX {oscanxmlfile} {ip}"
        args = shlex.split(osscancmd)
        
        try:
            # Fail-safe: Set process timeout to prevent hanging
            result = subprocess.run(args, capture_output=True, text=True, timeout=timeout, check=False)
            
            file_exists = os.path.exists(oscanxmlfile)
            
            if result.returncode == 0:
                return {
                    "command": osscancmd,
                    "output": result.stdout,
                    "os_scan_xml": oscanxmlfile if file_exists else None,
                    "scan_folder": scan_folder,  # =Juggernaut= Added scan folder info
                    "message": f"OSScan completed successfully. Result at: {oscanxmlfile}" if file_exists else "OSScan completed but XML file not found",
                    "timeout_used": timeout
                }
            else:
                return {
                    "command": osscancmd,
                    "output": result.stdout,
                    "error": result.stderr,
                    "os_scan_xml": oscanxmlfile if file_exists else None,
                    "message": "OSScan completed with warnings",
                    "timeout_used": timeout
                }
                
        except subprocess.TimeoutExpired:
            return {
                "command": osscancmd,
                "error": f"OSScan timed out after {timeout} seconds",
                "timeout_used": timeout,
                "message": "Scan was terminated due to timeout"
            }
        except Exception as e:
            return {
                "command": osscancmd,
                "error": f"Error in invoking OSScan Command: {osscancmd}",
                "exception": str(e),
                "timeout_used": timeout
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OSScan error: {e}")

# ---
# EXPLANATION:
# - This service exposes a /os-scan endpoint to run OS fingerprinting via HTTP.
# - Replace the stub logic with the full workflow from osScan.py for full functionality.
# ---
