# MapAuto

MapAuto is a toolkit for automating network scanning and vulnerability assessment using Nmap and Nessus.

---

## Prerequisites
- Python 3.x (for autoNessus.py)
- Python 2.x (for nmapscanner_updated.py, nmapall.py, osScan.py)
- Nmap installed and accessible in your PATH
- Nessus installed and running (for autoNessus.py)

---

## Setup

### 1. Clone the Repository
```bash
git clone https://github.com/RishiShrivastava/mapAuto.git
cd mapAuto
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
- Copy `.env` to your working directory if not present.
- Edit `.env` and set your Nessus credentials:
```
NESSUS_USERNAME=your_actual_username
NESSUS_PASSWORD=your_actual_password
```
- Alternatively, export them in your shell:
```bash
export NESSUS_USERNAME=your_actual_username
export NESSUS_PASSWORD=your_actual_password
```

---

## Usage

### autoNessus.py (Python 3)
Automate Nessus scan management.
- List scans: `python3 autoNessus.py -l`
- List policies: `python3 autoNessus.py -p`
- Start scan: `python3 autoNessus.py -sS <scan_id>`
- Resume scan: `python3 autoNessus.py -sR <scan_id>`
- Pause scan: `python3 autoNessus.py -pS <scan_id>`
- Stop scan: `python3 autoNessus.py -sP <scan_id>`

### nmapscanner_updated.py (Python 2)
- Run: `python2 nmapscanner_updated.py`
- Enter the target IP when prompted.
- The script will perform OS fingerprinting, WAF port scan, and run relevant NSE scripts.

### nmapall.py (Python 2)
- Run: `python2 nmapall.py`
- Enter the target IP when prompted.
- Runs all available Nmap scripts against the target.

### osScan.py (Python 2 or 3)
- Run: `python2 osScan.py` or `python3 osScan.py`
- Enter the target IP when prompted.
- Performs OS fingerprinting using Nmap.

### portXmllParser.py
- Parses Nmap XML output for open ports and services.
- Edit the script to set the XML file path as needed.

---

## Security Notes
- Never commit the `.env` file with real credentials to version control.
- Use environment variables in production environments.
- Rotate credentials regularly and keep them secure.

---

## Troubleshooting
- If you see credential errors, check your `.env` file or environment variables.
- Ensure you are using the correct Python version for each script.
- Make sure Nmap and Nessus are installed and accessible.

---

## License
See the repository for license details.
