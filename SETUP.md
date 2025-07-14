# MapAuto Setup Instructions

## Prerequisites
- Python 3.x
- Nmap installed
- Nessus (for autoNessus.py)

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Environment Variables

### For autoNessus.py
Update the `.env` file with your Nessus credentials:
```
NESSUS_USERNAME=your_actual_username
NESSUS_PASSWORD=your_actual_password
```

Or set environment variables directly:
```bash
export NESSUS_USERNAME=your_actual_username
export NESSUS_PASSWORD=your_actual_password
```

## Usage

### autoNessus.py
- List scans: `python3 autoNessus.py -l`
- List policies: `python3 autoNessus.py -p`
- Start scan: `python3 autoNessus.py -sS <scan_id>`
- Resume scan: `python3 autoNessus.py -sR <scan_id>`
- Pause scan: `python3 autoNessus.py -pS <scan_id>`
- Stop scan: `python3 autoNessus.py -sP <scan_id>`

### nmapscanner_updated.py
- Run with Python 2.x: `python2 nmapscanner_updated.py`
- Enter target IP when prompted

### Other scripts
- `nmapall.py`: Run with Python 2.x
- `osScan.py`: Run with Python 2.x or 3.x
- `portXmllParser.py`: XML parser for port scan results

## Security Notes
- Never commit the `.env` file with actual credentials
- Use environment variables in production
- Keep credentials secure and rotated regularly
