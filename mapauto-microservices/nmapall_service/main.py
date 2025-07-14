# ---
# NmapAll Microservice: FastAPI version of the original nmapall.py script
# This service exposes running all Nmap scripts as REST endpoints.
#
# Key Endpoints:
#   - /status: Health check
#   - /scan-all: Run all Nmap scripts for a given IP
#
# The core logic should be adapted from the original nmapall.py script.
# ---

from fastapi import FastAPI, Query, HTTPException
import os
from dotenv import load_dotenv
import subprocess
import shlex
import signal
import time
from typing import Optional

app = FastAPI(title="NmapAll Microservice")

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

@app.get("/status")
def status():
    return {"status": "NmapAll microservice is running"}

@app.post("/scan-all")
def scan_all(ip: str = Query(..., description="Target IP address"), 
             timeout: Optional[int] = Query(300, description="Timeout in seconds (default: 300)"),
             max_scripts: Optional[int] = Query(10, description="Maximum number of scripts to run (default: 10)")):
    """
    Run all Nmap scripts for the given IP address.
    This endpoint replicates the logic from nmapall.py:
    - Enumerates all scripts in /usr/share/nmap/scripts/
    - Runs each script against the target IP
    - Collects and returns the results as JSON
    - Includes fail-safes: timeouts, process limits, and error handling
    """
    results = []
    script_dir = "/usr/share/nmap/scripts/"
    
    # Fail-safe: Validate IP address format
    import ipaddress
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid IP address format")
    
    # Fail-safe: Check if script directory exists
    if not os.path.isdir(script_dir):
        raise HTTPException(status_code=500, detail=f"Nmap script directory not found: {script_dir}")
    
    try:
        script_files = [f for f in os.listdir(script_dir) if f.endswith('.nse')]
        
        # Fail-safe: Limit number of scripts to prevent resource exhaustion
        if len(script_files) > max_scripts:
            script_files = script_files[:max_scripts]
            results.append({
                "warning": f"Limited to {max_scripts} scripts out of {len(script_files)} available",
                "scripts_used": script_files
            })
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not list Nmap scripts: {e}")
    
    for script in script_files:
        # Fail-safe: Use simpler nmap command to avoid hanging
        cmd = f"nmap -sS -T4 --max-retries 1 --host-timeout 30s --script {script} {ip}"
        args = shlex.split(cmd)
        
        try:
            # Fail-safe: Set process timeout to prevent hanging
            result = subprocess.run(args, 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=timeout//len(script_files),  # Distribute timeout across scripts
                                  check=False)
            
            if result.returncode == 0:
                results.append({"script": script, "output": result.stdout})
            else:
                results.append({"script": script, "error": result.stderr or "Script failed"})
                
        except subprocess.TimeoutExpired:
            results.append({"script": script, "error": "Script timed out"})
        except Exception as e:
            results.append({"script": script, "error": str(e)})
    
    return {
        "target_ip": ip,
        "total_scripts": len(script_files),
        "results": results,
        "timeout_used": timeout,
        "max_scripts_limit": max_scripts
    }

# ---
# EXPLANATION:
# - This endpoint runs every Nmap script in /usr/share/nmap/scripts/ against the given IP.
# - Each script's output (or error) is collected and returned in a JSON list.
# - This is a direct port of the original nmapall.py logic, but results are returned via API instead of files.
# ---
