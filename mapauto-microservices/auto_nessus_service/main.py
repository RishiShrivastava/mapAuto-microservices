# ---
# AutoNessus Microservice: FastAPI version of the original CLI script
# This service exposes Nessus scan management as REST endpoints.
#
# Key Endpoints:
#   - /status: Health check
#   - /scans: List all scans
#   - /policies: List all policies
#   - /scans/start: Start a scan
#   - /scans/resume: Resume a scan
#   - /scans/pause: Pause a scan
#   - /scans/stop: Stop a scan
#
# The core logic is adapted from the original autoNessus.py script.
# ---

from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import requests
import json
from typing import Optional

app = FastAPI(title="AutoNessus Microservice")

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

NESSUS_URL = os.environ.get('NESSUS_URL', 'https://localhost:8834')
NESSUS_USERNAME = os.environ.get('NESSUS_USERNAME', 'xxxxx')
NESSUS_PASSWORD = os.environ.get('NESSUS_PASSWORD', 'xxxxx')
VERIFY = False

token = None  # Will be set after login

# --- Helper functions from original script ---
def build_url(resource):
    return f"{NESSUS_URL}{resource}"

def connect(method, resource, data=None, params=None):
    global token
    headers = {'X-Cookie': f'token={token}', 'content-type': 'application/json'}
    if data is not None:
        data = json.dumps(data)
    if method == 'POST':
        r = requests.post(build_url(resource), data=data, headers=headers, verify=VERIFY)
    elif method == 'PUT':
        r = requests.put(build_url(resource), data=data, headers=headers, verify=VERIFY)
    elif method == 'DELETE':
        r = requests.delete(build_url(resource), data=data, headers=headers, verify=VERIFY)
    else:
        r = requests.get(build_url(resource), params=params, headers=headers, verify=VERIFY)
    if r.status_code != 200:
        try:
            e = r.json()
            raise HTTPException(status_code=500, detail=e.get('error', 'Unknown error'))
        except Exception:
            raise HTTPException(status_code=500, detail=f"HTTP Error: {r.status_code}")
    if 'download' in resource:
        return r.content
    try:
        return r.json()
    except ValueError:
        return r.content

def login():
    global token
    login_data = {'username': NESSUS_USERNAME, 'password': NESSUS_PASSWORD}
    data = connect('POST', '/session', data=login_data)
    token = data['token']
    return token

def get_scans():
    data = connect('GET', '/scans/')
    status_dict = {p['id']: p['status'] for p in data['scans']}
    name_dict = {p['id']: p['name'] for p in data['scans']}
    return status_dict, name_dict

def get_policies():
    data = connect('GET', '/editor/policy/templates')
    return {p['title']: p['uuid'] for p in data['templates']}

def launch(sid):
    data = connect('POST', f'/scans/{sid}/launch')
    return data['scan_uuid']

# --- FastAPI Endpoints ---

# =Juggernaut= Modified to handle Nessus connection failure gracefully
@app.on_event("startup")
def startup_event():
    """Login to Nessus on startup and store the token."""
    if 'xxxxx' in [NESSUS_USERNAME, NESSUS_PASSWORD]:
        print("Warning: Please set NESSUS_USERNAME and NESSUS_PASSWORD in your .env file.")
        return
    try:
        login()
        print("Successfully connected to Nessus")
    except Exception as e:
        print(f"Warning: Could not connect to Nessus: {e}")
        print("Service will start but Nessus functionality will be limited")
        # =Juggernaut= Service continues to run even if Nessus is not available

@app.get("/status")
def status():
    return {"status": "AutoNessus microservice is running"}

@app.get("/scans")
def list_scans():
    """List all scans with their status and IDs."""
    # =Juggernaut= Added check for Nessus connection
    if token is None:
        raise HTTPException(status_code=503, detail="Nessus service not available. Please check connection.")
    
    status_dict, name_dict = get_scans()
    scans = []
    for scan_id in status_dict:
        scans.append({
            "id": scan_id,
            "name": name_dict[scan_id],
            "status": status_dict[scan_id]
        })
    return {"scans": scans}

@app.get("/policies")
def list_policies():
    """List all scan policies."""
    # =Juggernaut= Added check for Nessus connection
    if token is None:
        raise HTTPException(status_code=503, detail="Nessus service not available. Please check connection.")
    
    policies = get_policies()
    return {"policies": policies}

@app.post("/scans/start")
def start_scan(scan_id: str = Query(..., description="Scan ID to start")):
    """Start a specified scan by scan ID."""
    # =Juggernaut= Added check for Nessus connection
    if token is None:
        raise HTTPException(status_code=503, detail="Nessus service not available. Please check connection.")
    
    scan_uuid = launch(scan_id)
    return {"message": f"Scan {scan_id} started.", "scan_uuid": scan_uuid}

# More endpoints (resume, pause, stop) can be added similarly.

# ---
# EXPLANATION:
# - The helper functions (connect, login, get_scans, etc.) are adapted from the original script.
# - The FastAPI endpoints call these helpers and return JSON responses.
# - On startup, the service logs in to Nessus and stores the session token.
# - Credentials are loaded from environment variables for security.
# - Error handling is done via HTTPException for API-friendly errors.
# - You can now interact with Nessus via HTTP requests to this service.
# ---
