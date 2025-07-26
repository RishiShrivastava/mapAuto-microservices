# MapAuto Microservices User Guide

**Author:** RishiShrivastava/=Juggernaut=
**Date:** July 26, 2025

---

## Table of Contents
1. [Introduction](#introduction)
2. [System Overview](#system-overview)
3. [Installation & Setup](#installation--setup)
4. [Quick Start](#quick-start)
5. [Web Dashboard Usage](#web-dashboard-usage)
6. [API Usage Examples](#api-usage-examples)
7. [Best Practices & Security](#best-practices--security)
8. [Troubleshooting](#troubleshooting)
9. [Use Cases](#use-cases)
10. [Support](#support)

---

## Introduction
MapAuto Microservices is a modular, production-ready toolkit for automated network scanning, OS fingerprinting, WAF detection, and vulnerability assessment. It is designed for security professionals, DevSecOps, and educators who need a robust, containerized solution for network reconnaissance and analysis.

---

## System Overview
- **Microservices:**
  - Nmap Scanner (intelligent port scanning)
  - Nmap All Scripts (comprehensive script execution)
  - OS Fingerprinting
  - XML Parser (nmap result parsing)
  - WAF Detection (advanced firewall analysis)
  - Auto Nessus (optional, for Nessus integration)
  - React Web Dashboard (scan management UI)
- **Security:** HTTPS-only, reverse proxy, WAF, rate limiting, health checks
- **Persistence:** All scan results and data are stored in persistent volumes

---

## Installation & Setup
### Prerequisites
- Docker & Docker Compose
- Python 3.11+ (for health checks)
- (Optional) Nessus for vulnerability scanning

### Steps
```bash
# 1. Clone the repository
 git clone https://github.com/RishiShrivastava/mapAuto-microservices.git
 cd mapAuto-microservices
 git checkout dev

# 2. Configure environment
 cp .env.template .env
 nano .env  # Add Nessus credentials if needed

# 3. Build and start all services
 cd mapauto-microservices
 sudo docker compose up --build -d

# 4. Check status
 sudo docker compose ps
```

---

## Quick Start
- Access the web dashboard: https://localhost (accept SSL warning)
- Use the dashboard to configure and launch scans, view results, and monitor health
- All scan results are saved in `scan_results/`

---

## Web Dashboard Usage
- **Access:** Open https://localhost in your browser
- **Features:**
  - Configure scans (target IP, timeout, max scripts)
  - Launch scans (OS, Nmap, All Scripts, XML Parse, Nessus Status)
  - View results and scan history
  - Monitor service health
- **Scan History:** All scans are timestamped and saved for review

---

## API Usage Examples
### WAF Detection
```bash
curl -X POST "https://localhost/api/waf/analyze?target=https://example.com" -k
curl "https://localhost/api/waf/signatures" -k
curl "https://localhost/api/waf/status" -k
```

### Nmap Scanning
```bash
curl -X POST "https://localhost/api/nmapscanner/scan?ip=192.168.1.100&timeout=300" -k
curl -X POST "https://localhost/api/nmapall/scan-all?ip=192.168.1.100&timeout=300&max_scripts=10" -k
```

### OS Fingerprinting
```bash
curl -X POST "https://localhost/api/osscan/os-scan?ip=192.168.1.100&timeout=60" -k
```

### XML Parsing
```bash
curl -X POST "https://localhost/api/portxmlparser/parse-xml?xml_path=/app/scan_results/osscan_192.168.1.100_YYYYMMDD_HHMMSS/OSScan_192.168.1.100.xml" -k
```

### Nessus Status
```bash
curl -X POST "https://localhost/api/auto_nessus/status" -k
```

---

## Best Practices & Security
- Always use HTTPS (https://localhost)
- Never commit real credentials to git
- Monitor logs for suspicious activity
- Use only on authorized targets
- Review scan history and results regularly

---

## Troubleshooting
- **SSL Warnings:** Normal for self-signed certs in demo mode
- **Scan Fails:** Check logs with `sudo docker compose logs -f`
- **Restart Service:** `sudo docker compose restart <service>`
- **Data Persistence:** All results are in `scan_results/`
- **Update App:** `git pull && sudo docker compose up --build -d`

---

## Use Cases
- **Penetration Testing:** Automate reconnaissance and WAF detection
- **DevSecOps:** Integrate into CI/CD for continuous security scanning
- **Blue Teams:** Monitor and validate WAF deployments
- **Education:** Demonstrate scanning and WAF bypass in labs

---

## Support
- For issues, check the Troubleshooting section
- Open an issue on GitHub with details and logs

---

© 2025 RishiShrivastava/=Juggernaut=. All rights reserved.
