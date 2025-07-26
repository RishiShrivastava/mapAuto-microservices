# MapAuto Microservices

MapAuto is a production-ready microservices toolkit for automating network scanning and vulnerability assessment using Nmap and Nessus. The system is containerized using Docker and provides REST API endpoints for all scanning functionality.

---

## 🚀 Features

### Core Microservices
- **auto_nessus_service** (Port 8000): Nessus scan management via REST API
- **nmapscanner_service** (Port 8001): Intelligent nmap scanning with OS detection
- **nmapall_service** (Port 8002): Execute all nmap scripts against target IP
- **osscan_service** (Port 8003): OS fingerprinting using nmap
- **portxmlparser_service** (Port 8004): Parse nmap XML files for port information
- **waf_detection_service** (Port 8005): Advanced WAF detection and vulnerability analysis =Juggernaut=
- **frontend** (Port 3000): React web dashboard for scan management =Juggernaut=

### Production Features
- **✅ Timestamped Result Folders**: Each scan creates organized folders with timestamps
- **✅ Persistent Containers**: Auto-restart policies and persistent volumes
- **✅ Health Checks**: Built-in Docker health monitoring
- **✅ Graceful Error Handling**: Services handle missing dependencies gracefully
- **✅ Resource Limits**: Timeout controls and process limits
- **✅ Comprehensive Logging**: All operations logged with timestamps
- **✅ Web Dashboard**: React-based UI for scan management and results =Juggernaut=
- **✅ WAF Detection & Analysis**: Advanced Web Application Firewall identification with weakness analysis =Juggernaut=

### WAF Detection Capabilities =Juggernaut=

#### 🛡️ Supported WAF Types (8 Major Platforms)
- **Cloudflare**: CDN-integrated protection with global edge network
- **AWS WAF**: Amazon's cloud-native web application firewall
- **Akamai**: Enterprise-grade edge security platform
- **Incapsula**: Imperva's cloud-based application security
- **ModSecurity**: Open-source web application firewall engine
- **Barracuda**: Network security and data protection appliances
- **F5 ASM**: Application Security Manager for enterprise environments
- **Imperva SecureSphere**: Advanced threat protection platform

#### 🔍 Detection Methods
- **HTTP Header Analysis**: Server headers, security headers, custom headers
- **Cookie Fingerprinting**: WAF-specific cookies and session tokens
- **Response Code Patterns**: Characteristic HTTP status codes and error pages
- **Content Pattern Matching**: WAF-specific error messages and content signatures
- **Payload Testing**: XSS, SQLi, command injection, and path traversal attempts
- **Nmap Script Integration**: Advanced scripted detection for intensive analysis

#### 🎯 Analysis Features
- **Weakness Identification**: Common vulnerabilities and configuration flaws
- **Bypass Techniques**: Header manipulation, encoding bypasses, protocol attacks
- **Security Recommendations**: Hardening suggestions and best practices
- **Confidence Scoring**: Reliability assessment of detection results
- **Multi-method Validation**: Cross-verification using multiple detection approaches

---

## 📋 Prerequisites

- **Docker** and **Docker Compose** installed
- **Git** for repository management
- **Python 3.11+** (for development/health checks)
- **Nmap** (installed in containers automatically)
- **Nessus** (optional, for auto_nessus_service)
- **Node.js 18+** (for frontend development, optional) =Juggernaut=

---

## 🛠️ Setup and Installation

### 1. Clone the Repository
```bash
git clone https://github.com/RishiShrivastava/mapAuto-microservices.git
cd mapAuto-microservices
git checkout dev  # Use the development branch
```

### 2. Environment Configuration
```bash
# Copy the environment template
cp .env.template .env

# Edit the .env file with your Nessus credentials (optional)
nano .env
```

Add your Nessus credentials to `.env`:
```env
NESSUS_USERNAME=your_actual_username
NESSUS_PASSWORD=your_actual_password
NESSUS_URL=https://your-nessus-server:8834
```

### 3. Build and Start Services
```bash
cd mapauto-microservices
sudo docker compose up --build -d
```

### 4. Verify Services Are Running
```bash
# Check container status
sudo docker compose ps

# Check health status
sudo docker compose ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}"
```

### 5. Access Web Dashboard =Juggernaut=
```bash
# Open the React web dashboard in your browser
# Visit: http://localhost:3000

# The dashboard provides:
# - Interactive scan configuration
# - Real-time scan execution
# - Results visualization
# - Scan history tracking
```

---

## 📊 Health Monitoring

### Using Built-in Health Checks
```bash
# Check Docker health status
sudo docker compose ps

# View health check logs
sudo docker compose logs --follow
```

### Using the Health Check Script
```bash
# Install health check dependencies
pip install -r requirements-healthcheck.txt

# Run health check
python3 health_check.py
```

Expected output:
```
=== mapAuto Microservices Health Check ===
Checking 6 services...

✅ auto_nessus: healthy (0.025s)
✅ nmapscanner: healthy (0.018s)
✅ nmapall: healthy (0.022s)
✅ osscan: healthy (0.019s)
✅ portxmlparser: healthy (0.016s)
✅ waf_detection: healthy (0.021s)

Health Summary: 6/6 services healthy
🎉 All services are healthy!
```

---

## 🔧 API Usage Examples

### WAF Detection Service (Port 8005) =Juggernaut=
```bash
# Analyze a target for WAF presence and type
curl -X POST "https://localhost/api/waf/analyze?target=https://example.com" -k

# Get supported WAF signatures
curl "https://localhost/api/waf/signatures" -k

# Check service status
curl "https://localhost/api/waf/status" -k

# Response includes comprehensive WAF analysis
{
  "target": "https://example.com",
  "waf_detected": true,
  "waf_type": "cloudflare",
  "confidence": 95,
  "detection_methods": ["headers", "content_patterns"],
  "weaknesses": [
    "Origin IP discovery via DNS records",
    "Subdomain enumeration bypass"
  ],
  "bypass_techniques": [
    "X-Originating-IP header manipulation",
    "Unicode normalization bypasses"
  ],
  "recommendations": [
    "Implement origin server IP protection",
    "Configure proper DNS security"
  ]
}
```

### NmapScanner Service (Port 8001)
```bash
# Basic scan with intelligent script selection
curl -X POST "http://localhost:8001/scan?ip=192.168.1.100&timeout=300"

# Response includes timestamped folder
{
  "target_ip": "192.168.1.100",
  "scan_folder": "/app/scan_results/nmapscanner_192.168.1.100_20250716_143022",
  "open_ports": {"22": "ssh", "80": "http", "443": "https"},
  "port_scripts": {"22": ["ssh-auth-methods.nse", "ssh-hostkey.nse"]},
  "script_results": {...}
}
```

### OS Scan Service (Port 8003)
```bash
# OS fingerprinting scan
curl -X POST "http://localhost:8003/os-scan?ip=192.168.1.100&timeout=60"

# Response with organized results
{
  "command": "nmap -T4 --max-retries 1 --host-timeout 60s -O --osscan-guess -oX /app/scan_results/osscan_192.168.1.100_20250716_143045/OSScan_192.168.1.100.xml 192.168.1.100",
  "scan_folder": "/app/scan_results/osscan_192.168.1.100_20250716_143045",
  "os_scan_xml": "/app/scan_results/osscan_192.168.1.100_20250716_143045/OSScan_192.168.1.100.xml"
}
```

### NmapAll Service (Port 8002)
```bash
# Run all nmap scripts (limited for safety)
curl -X POST "http://localhost:8002/scan-all?ip=192.168.1.100&timeout=300&max_scripts=10"

# Response with script results
{
  "target_ip": "192.168.1.100",
  "scan_folder": "/app/scan_results/nmapall_192.168.1.100_20250716_143112",
  "total_scripts": 10,
  "results": [...]
}
```

### XML Parser Service (Port 8004)
```bash
# Parse existing XML file
curl -X POST "http://localhost:8004/parse-xml?xml_path=/app/scan_results/osscan_192.168.1.100_20250716_143045/OSScan_192.168.1.100.xml"

# Response with parsed port data
{
  "open_tcp_ports": {"22": "ssh", "80": "http"},
  "open_udp_ports": {},
  "parse_folder": "/app/scan_results/xmlparser_20250716_143156",
  "archived_xml": "/app/scan_results/xmlparser_20250716_143156/OSScan_192.168.1.100.xml"
}
```

### Auto Nessus Service (Port 8000)
```bash
# Check service status
curl "http://localhost:8000/status"

# List available scans (requires Nessus)
curl "http://localhost:8000/list-scans"

# Note: Gracefully handles missing Nessus connection
```

---

## 📁 File Organization

### Scan Results Structure
```
scan_results/
├── nmapscanner_192.168.1.100_20250716_143022/
│   ├── OSScan_192.168.1.100.xml
│   └── WAFPortScan_192.168.1.100.xml
├── osscan_192.168.1.100_20250716_143045/
│   └── OSScan_192.168.1.100.xml
├── nmapall_192.168.1.100_20250716_143112/
│   ├── script1_output.txt
│   ├── script2_output.txt
│   └── ...
└── xmlparser_20250716_143156/
    └── OSScan_192.168.1.100.xml (archived)
```

### Service Dependencies
Each service has its own `requirements.txt` with version pinning:
```
fastapi>=0.104.1
uvicorn[standard]>=0.24.0
python-dotenv>=1.0.0
requests>=2.31.0  # (auto_nessus only)
pydantic>=2.4.2   # (auto_nessus only)
```

---

## 🐳 Container Management

### Starting Services
```bash
# Start all services
sudo docker compose up -d

# Start specific service
sudo docker compose up -d nmapscanner

# Build and start
sudo docker compose up --build -d
```

### Stopping Services
```bash
# Stop all services
sudo docker compose down

# Stop specific service
sudo docker compose stop nmapscanner

# Stop and remove volumes (caution: deletes scan results)
sudo docker compose down -v
```

### Viewing Logs
```bash
# View all logs
sudo docker compose logs -f

# View specific service logs
sudo docker compose logs -f nmapscanner

# View recent logs
sudo docker compose logs --tail=50 nmapscanner
```

### Accessing Container Shell
```bash
# Access nmapscanner container
sudo docker exec -it mapauto-microservices-nmapscanner-1 bash

# Check scan results inside container
sudo docker exec -it mapauto-microservices-nmapscanner-1 ls -la /app/scan_results/
```

---

## 🔄 Persistence and Recovery

### Data Persistence
- **Scan Results**: Stored in `./scan_results/` (bind mount)
- **Nessus Data**: Stored in `nessus_data` named volume
- **Restart Policy**: `unless-stopped` - containers auto-restart

### Testing Persistence
```bash
# Stop all containers
sudo docker compose stop

# Start containers - data should persist
sudo docker compose start

# Verify scan results are still there
sudo docker exec -it mapauto-microservices-nmapscanner-1 ls -la /app/scan_results/

# Verify WAF detection data persistence
sudo docker exec -it mapauto-waf-detection ls -la /app/waf_results/
```

### Backup and Recovery
```bash
# Backup scan results
tar -czf scan_results_backup_$(date +%Y%m%d_%H%M%S).tar.gz scan_results/

# Backup Docker volumes
sudo docker run --rm -v mapauto-microservices_nessus_data:/data -v $(pwd):/backup alpine tar czf /backup/nessus_backup.tar.gz -C /data .
```

---

## 🛡️ Security Considerations

### Environment Variables
- Never commit `.env` files with real credentials
- Use Docker secrets in production
- Rotate credentials regularly

### Network Security
- Services run on localhost by default
- Use reverse proxy (nginx) for external access
- Implement rate limiting for production

### Container Security
- Services run as non-root where possible
- Minimal base images (python:3.11-slim)
- Regular security updates

---

## 🐛 Troubleshooting

### Common Issues

#### Services Not Starting
```bash
# Check logs for errors
sudo docker compose logs nmapscanner

# Rebuild containers
sudo docker compose down
sudo docker compose up --build -d
```

#### Permission Errors
```bash
# Fix scan_results permissions
sudo chown -R $USER:$USER scan_results/

# Fix Docker socket permissions
sudo usermod -aG docker $USER
# Log out and back in
```

#### Health Check Failures
```bash
# Check service status
curl http://localhost:8001/status

# Check Docker health
sudo docker compose ps

# Restart unhealthy service
sudo docker compose restart nmapscanner
```

#### Port Conflicts
```bash
# Check what's using ports
sudo netstat -tulpn | grep :8001

# Stop conflicting services
sudo systemctl stop apache2  # example
```

---

## 🔧 Development and Customization

### Adding New Services
1. Create new service directory: `mkdir new_service`
2. Add `main.py`, `requirements.txt`, `Dockerfile`
3. Update `docker-compose.yml`
4. Add health check endpoint
5. Test and document

### Modifying Existing Services
```bash
# Edit service code
nano nmapscanner_service/main.py

# Rebuild specific service
sudo docker compose build nmapscanner

# Restart service
sudo docker compose restart nmapscanner
```

### Local Development
```bash
# Install development dependencies
pip install -r nmapscanner_service/requirements.txt

# Run service locally
cd nmapscanner_service
uvicorn main:app --reload --port 8001
```

---

## 📈 Performance Tuning

### Resource Limits
Edit `docker-compose.yml` to add resource limits:
```yaml
services:
  nmapscanner:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
```

### Timeout Configuration
Adjust timeouts in service code:
```python
# In main.py files
DEFAULT_TIMEOUT = 300  # 5 minutes
MAX_TIMEOUT = 1800     # 30 minutes
```

### Concurrent Scans
Services handle concurrent requests, but consider:
- Resource availability
- Network bandwidth
- Target system load

---

## 🧪 Testing

### Unit Testing
```bash
# Run health checks
python3 health_check.py

# Test individual endpoints
curl "https://localhost/api/auto_nessus/status" -k
curl "https://localhost/api/nmapscanner/status" -k
curl "https://localhost/api/nmapall/status" -k
curl "https://localhost/api/osscan/status" -k
curl "https://localhost/api/portxmlparser/status" -k
curl "https://localhost/api/waf/status" -k
```

### Integration Testing
```bash
# Full workflow test
TARGET_IP="192.168.1.100"
TARGET_URL="https://example.com"

# 1. OS scan
curl -X POST "https://localhost/api/osscan/os-scan?ip=$TARGET_IP&timeout=60" -k

# 2. Intelligent scan
curl -X POST "https://localhost/api/nmapscanner/scan?ip=$TARGET_IP&timeout=300" -k

# 3. WAF analysis
curl -X POST "https://localhost/api/waf/analyze?target=$TARGET_URL" -k

# 4. Parse results
curl -X POST "https://localhost/api/portxmlparser/parse-xml?xml_path=/app/scan_results/osscan_${TARGET_IP}_[timestamp]/OSScan_${TARGET_IP}.xml" -k
```

### Load Testing
```bash
# Install hey (HTTP load testing tool)
sudo apt install hey

# Test service under load
hey -n 100 -c 10 http://localhost:8001/status
```

---

## 📚 API Documentation

### Interactive API Documentation
Access Swagger UI for each service:
- **auto_nessus**: https://localhost/api/auto_nessus/docs
- **nmapscanner**: https://localhost/api/nmapscanner/docs
- **nmapall**: https://localhost/api/nmapall/docs
- **osscan**: https://localhost/api/osscan/docs
- **portxmlparser**: https://localhost/api/portxmlparser/docs
- **waf_detection**: https://localhost/api/waf/docs =Juggernaut=
- **frontend**: https://localhost (React Dashboard) =Juggernaut=

### OpenAPI Specifications
- **auto_nessus**: https://localhost/api/auto_nessus/openapi.json
- **nmapscanner**: https://localhost/api/nmapscanner/openapi.json
- **nmapall**: https://localhost/api/nmapall/openapi.json
- **osscan**: https://localhost/api/osscan/openapi.json
- **portxmlparser**: https://localhost/api/portxmlparser/openapi.json
- **waf_detection**: https://localhost/api/waf/openapi.json =Juggernaut=

---

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-feature`

### Code Standards
- Follow PEP 8 for Python code
- Add comprehensive error handling
- Include health check endpoints
- Document all API endpoints


---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🔗 Related Projects

- **Nmap**: https://nmap.org/
- **Nessus**: https://www.tenable.com/products/nessus
- **FastAPI**: https://fastapi.tiangolo.com/
- **Docker**: https://www.docker.com/

---

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Search existing issues on GitHub
3. Create a new issue with detailed information
4. Include logs and error messages

---

## 🚀 Recent Updates and Improvements

### Version 2.1.0 - WAF Detection Integration (July 25, 2025) =Juggernaut=

#### ✅ **Advanced WAF Detection Service**
- **Implementation**: Comprehensive WAF identification and analysis engine
- **Features**: 8 major WAF platform support with fingerprinting capabilities
- **Detection Methods**: HTTP analysis, payload testing, nmap integration
- **Security Analysis**: Weakness identification, bypass techniques, hardening recommendations

#### ✅ **Enhanced Security Architecture**
- **HTTPS-Only Access**: SSL/TLS encryption for all web communications
- **Nginx Reverse Proxy**: Centralized routing with extended timeouts for WAF analysis
- **Input Validation**: URL validation, IP address checking, timeout limits
- **Resource Protection**: Rate limiting and secure header implementation

#### ✅ **Expanded API Coverage**
- **WAF Analysis Endpoint**: `/api/waf/analyze` for comprehensive target analysis
- **Signature Database**: `/api/waf/signatures` for supported WAF information
- **Health Monitoring**: Integrated health checks for service reliability
- **Documentation**: Interactive Swagger UI at `/api/waf/docs`

### Version 2.0.0 - Microservices Architecture (July 16, 2025)

#### ✅ **Timestamped Result Folders**
- **Implementation**: Each service now creates timestamped folders for every scan
- **Format**: `servicename_IP_YYYYMMDD_HHMMSS`
- **Benefits**: Easy organization, no file conflicts, audit trail
- **Commands executed**:
  ```bash
  # Added create_scan_folder() and create_parse_folder() functions
  # Modified all return statements to include folder paths
  # Updated all file operations to use timestamped directories
  ```

#### ✅ **Persistent Containers with Auto-Restart**
- **Implementation**: Docker Compose with restart policies and volumes
- **Features**: 
  - `restart: unless-stopped` for all services
  - Persistent volumes for scan results
  - Named volumes for service data
- **Commands executed**:
  ```bash
  # Updated docker-compose.yml
  sudo docker compose up --build -d
  sudo docker compose down
  sudo docker compose up -d  # Data persists
  ```

#### ✅ **Enhanced Requirements Management**
- **Implementation**: Comprehensive requirements.txt for each service
- **Features**:
  - Version pinning for all dependencies
  - Documented standard library modules
  - Separate health check requirements
- **Files updated**:
  - `auto_nessus_service/requirements.txt`
  - `nmapscanner_service/requirements.txt`
  - `osscan_service/requirements.txt`
  - `nmapall_service/requirements.txt`
  - `portxmlparser_service/requirements.txt`
  - `requirements-healthcheck.txt`

#### ✅ **Docker Health Checks**
- **Implementation**: Built-in health monitoring for all containers
- **Features**:
  - HTTP health check endpoints
  - Configurable intervals and timeouts
  - Automatic container restart on failure
- **Commands executed**:
  ```bash
  # Updated all Dockerfiles to include curl
  # Added healthcheck configurations to docker-compose.yml
  # All services now show "healthy" status
  ```

#### ✅ **Comprehensive Health Monitoring**
- **Implementation**: Python health check script
- **Features**:
  - Tests all 5 services simultaneously
  - Response time monitoring
  - Exit codes for automation
  - Colorized output
- **Usage**:
  ```bash
  python3 health_check.py
  # Expected: 5/5 services healthy 🎉
  ```

#### ✅ **Production-Ready Error Handling**
- **Implementation**: Graceful handling of missing dependencies
- **Features**:
  - Auto_nessus handles missing Nessus gracefully
  - All services have timeout protection
  - Resource limits and fail-safes
- **Testing verified**:
  - Services start without Nessus
  - Timeouts work correctly
  - Error responses are informative

#### ✅ **Complete Documentation**
- **Implementation**: Comprehensive README with all commands
- **Features**:
  - Step-by-step installation guide
  - All API endpoints documented
  - Troubleshooting section
  - Performance tuning guide


### Commands Summary for Full Setup

```bash
# 1. Clone and setup
git clone https://github.com/RishiShrivastava/mapAuto-microservices.git
cd mapAuto-microservices/mapauto-microservices

# 2. Configure environment
cp ../.env.template ../.env
# Edit .env with your credentials

# 3. Build and start services
sudo docker compose up --build -d

# 4. Verify everything is working
sudo docker compose ps
python3 health_check.py

# 5. Test the services
curl -X POST "https://localhost/api/osscan/os-scan?ip=192.168.0.231&timeout=30" -k
curl -X POST "https://localhost/api/nmapscanner/scan?ip=192.168.0.231&timeout=60" -k
curl -X POST "https://localhost/api/nmapall/scan-all?ip=192.168.0.231&timeout=60&max_scripts=5" -k
curl -X POST "https://localhost/api/portxmlparser/parse-xml?xml_path=/path/to/xml" -k
curl -X POST "https://localhost/api/waf/analyze?target=https://example.com" -k

# 6. Access web dashboard
# Visit https://localhost for the React web interface

# 7. Access API documentation
# Visit http://localhost:8001/docs (and ports 8000-8004)
```

## 🌐 Web Dashboard Usage =Juggernaut=

### Access the Dashboard
```bash
# Start all services
sudo docker compose up --build -d

# Access the web interface
# Open browser to: http://localhost:3000
```

### Dashboard Features
- **Interactive Scan Configuration**: Set target IP, timeout, and scan parameters
- **Real-time Scan Execution**: Click-to-start scans with live progress indicators  
- **Results Visualization**: Formatted display of scan results with expandable sections
- **Scan History**: Automatic tracking of previous scans with timestamps
- **Service Status**: Visual indicators for microservice health
- **Responsive Design**: Works on desktop and mobile devices

### Available Scans in Dashboard
1. **OS Scan** (Port 8003): Operating system fingerprinting
2. **Nmap Scan** (Port 8001): Intelligent port scanning with script execution
3. **Nmap All Scripts** (Port 8002): Execute all available nmap scripts
4. **Parse XML** (Port 8004): Parse and format existing XML scan results
5. **Nessus Status** (Port 8000): Check Nessus service connectivity

### Scan Configuration
In the **Scanner Tab**:
- **Target IP Address**: Enter the IP you want to scan (e.g., 192.168.0.231)
- **Timeout (seconds)**: Set scan timeout (default: 60s)
- **Max Scripts**: For comprehensive scans (default: 5)
- **XML File Path**: For parsing existing XML results

## Running a Scan
1. Enter your target IP (e.g., 192.168.0.231)
2. Click the desired scan type button
3. Watch the loading indicator
4. Results appear automatically in the **Results Tab**

## Understanding Results
Results show:
- **Target Information**: IP address scanned
- **Open Ports**: List of accessible services
- **Scan Details**: Folder location, timing
- **Raw JSON**: Complete technical details

## Scan History
- All scans are automatically saved
- Access via **History Tab**
- Shows timestamp, scan type, and target
- Click to expand and view previous results

## Command Line Access (Alternative)
If you prefer command line access:
```bash
# WAF Detection
curl -X POST "https://localhost/api/waf/analyze?target=https://example.com" -k

# OS Scan
curl -X POST "https://localhost/api/osscan/os-scan?ip=192.168.0.231&timeout=30" -k

# Nmap Scan  
curl -X POST "https://localhost/api/nmapscanner/scan?ip=192.168.0.231&timeout=60" -k

# Nmap All Scripts
curl -X POST "https://localhost/api/nmapall/scan-all?ip=192.168.0.231&timeout=60&max_scripts=5" -k

# Parse XML
curl -X POST "https://localhost/api/portxmlparser/parse-xml?xml_path=/path/to/file.xml" -k

# Nessus Status
curl -X POST "https://localhost/api/auto_nessus/status" -k
```

## Security Features
- **HTTPS Encryption**: All web traffic encrypted via SSL/TLS
- **Network Isolation**: Backend services only accessible through nginx proxy
- **Input Validation**: IP address and file path validation, timeout limits

## Monitoring & Health Checks
- **Service Health**: All services have built-in health checks
- **Log Monitoring**: `sudo docker compose logs -f` or `sudo docker logs mapauto-frontend`

## Troubleshooting
- "Cannot connect to https://localhost": Check nginx container, restart if needed
- "Frontend shows errors": Check frontend logs, restart frontend
- "Scan not working": Verify target IP, check timeout, view backend logs
- "SSL Certificate Warning": Normal for development, click "Advanced" → "Proceed to localhost"

## System Management
- **Start All Services**: `sudo docker compose up -d`
- **Stop All Services**: `sudo docker compose down`
- **Rebuild After Changes**: `sudo docker compose up --build -d`
- **View Status**: `sudo docker compose ps`

## Best Practices
1. Always use HTTPS: Access via https://localhost for security
2. Set appropriate timeouts: Longer for comprehensive scans
3. Monitor resources: Check system performance during scans
4. Review scan history: Learn from previous results
5. Use development responsibly: Only scan authorized targets

---

## 📖 User Guide: MapAuto Microservices

## Getting Started

### 1. Prerequisites
- Docker & Docker Compose installed
- Python 3.11+ (for health checks)
- (Optional) Nessus for vulnerability scanning

### 2. Quick Start
```bash
# Clone the repository
git clone https://github.com/RishiShrivastava/mapAuto-microservices.git
cd mapAuto-microservices

# Switch to dev branch
git checkout dev

# Copy and edit environment variables
cp .env.template .env
nano .env  # Add Nessus credentials if needed

# Build and start all services
cd mapauto-microservices
sudo docker compose up --build -d

# Check status
sudo docker compose ps
```

### 3. Access the Web Dashboard
- Open your browser and go to: **https://localhost**
- Accept the SSL warning (self-signed cert for demo)
- Use the dashboard to:
  - Configure and launch scans
  - View scan results and history
  - Monitor service health

---

## Example Workflows

### A. WAF Detection (via API)
```bash
# Analyze a target for WAF presence and type
curl -X POST "https://localhost/api/waf/analyze?target=https://example.com" -k

# Get supported WAF signatures
curl "https://localhost/api/waf/signatures" -k

# Check WAF detection service status
curl "https://localhost/api/waf/status" -k
```

### B. Nmap Scanning (via API)
```bash
# Intelligent scan
curl -X POST "https://localhost/api/nmapscanner/scan?ip=192.168.1.100&timeout=300" -k

# All scripts scan (limited for safety)
curl -X POST "https://localhost/api/nmapall/scan-all?ip=192.168.1.100&timeout=300&max_scripts=10" -k
```

### C. OS Fingerprinting
```bash
curl -X POST "https://localhost/api/osscan/os-scan?ip=192.168.1.100&timeout=60" -k
```

### D. XML Parsing
```bash
curl -X POST "https://localhost/api/portxmlparser/parse-xml?xml_path=/app/scan_results/osscan_192.168.1.100_20250716_143045/OSScan_192.168.1.100.xml" -k
```

### E. Nessus Status
```bash
curl -X POST "https://localhost/api/auto_nessus/status" -k
```

---

## Using the Web Dashboard

1. **Start all services:**
   ```bash
   sudo docker compose up --build -d
   ```
2. **Open your browser:**
   - Go to: https://localhost
   - Accept the SSL warning
3. **Configure a scan:**
   - Enter the target IP (e.g., 192.168.0.231)
   - Set timeout and max scripts as needed
   - Click the scan type (OS Scan, Nmap Scan, etc.)
4. **View results:**
   - Results appear in the Results tab
   - Scan history is available in the History tab
5. **Monitor health:**
   - Health status is shown for all services

---

## Troubleshooting & Tips
- If you see SSL warnings, this is normal for self-signed certs in demo mode.
- If a scan fails, check the logs:
  ```bash
  sudo docker compose logs -f
  ```
- To restart a service:
  ```bash
  sudo docker compose restart <service>
  ```
- For persistent data, all scan results are saved in `scan_results/`.
- To update the app, pull the latest code and rebuild:
  ```bash
  git pull
  sudo docker compose up --build -d
  ```

---

## Security Best Practices
- Always use HTTPS (https://localhost)
- Never commit real credentials to git
- Monitor logs for suspicious activity
- Use only on authorized targets

---

# 🎯 Example Use Cases

- **Penetration Testers:** Automate reconnaissance and WAF detection for client networks.
- **DevSecOps:** Integrate into CI/CD for continuous security scanning.
- **Blue Teams:** Monitor and validate WAF deployments and network exposure.
- **Educators:** Demonstrate real-world scanning and WAF bypass techniques in a safe lab.

---

For more details, see the full API documentation and the examples above. For help, check the Troubleshooting section or open an issue on GitHub.
