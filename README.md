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
- **frontend** (Port 3000): React web dashboard for scan management =Juggernaut=

### Production Features
- **✅ Timestamped Result Folders**: Each scan creates organized folders with timestamps
- **✅ Persistent Containers**: Auto-restart policies and persistent volumes
- **✅ Health Checks**: Built-in Docker health monitoring
- **✅ Graceful Error Handling**: Services handle missing dependencies gracefully
- **✅ Resource Limits**: Timeout controls and process limits
- **✅ Comprehensive Logging**: All operations logged with timestamps
- **✅ Web Dashboard**: React-based UI for scan management and results =Juggernaut=

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
Checking 5 services...

✅ auto_nessus: healthy (0.025s)
✅ nmapscanner: healthy (0.018s)
✅ nmapall: healthy (0.022s)
✅ osscan: healthy (0.019s)
✅ portxmlparser: healthy (0.016s)

Health Summary: 5/5 services healthy
🎉 All services are healthy!
```

---

## 🔧 API Usage Examples

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
curl http://localhost:8001/status
curl http://localhost:8002/status
curl http://localhost:8003/status
curl http://localhost:8004/status
curl http://localhost:8000/status
```

### Integration Testing
```bash
# Full workflow test
TARGET_IP="192.168.1.100"

# 1. OS scan
curl -X POST "http://localhost:8003/os-scan?ip=$TARGET_IP&timeout=60"

# 2. Intelligent scan
curl -X POST "http://localhost:8001/scan?ip=$TARGET_IP&timeout=300"

# 3. Parse results
curl -X POST "http://localhost:8004/parse-xml?xml_path=/app/scan_results/osscan_${TARGET_IP}_[timestamp]/OSScan_${TARGET_IP}.xml"
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
- **auto_nessus**: http://localhost:8000/docs
- **nmapscanner**: http://localhost:8001/docs
- **nmapall**: http://localhost:8002/docs
- **osscan**: http://localhost:8003/docs
- **portxmlparser**: http://localhost:8004/docs
- **frontend**: http://localhost:3000 (React Dashboard) =Juggernaut=

### OpenAPI Specifications
- **auto_nessus**: http://localhost:8000/openapi.json
- **nmapscanner**: http://localhost:8001/openapi.json
- **nmapall**: http://localhost:8002/openapi.json
- **osscan**: http://localhost:8003/openapi.json
- **portxmlparser**: http://localhost:8004/openapi.json

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
curl -X POST "http://localhost:8003/os-scan?ip=192.168.0.231&timeout=30"
curl -X POST "http://localhost:8001/scan?ip=192.168.0.231&timeout=60"
curl -X POST "http://localhost:8002/scan-all?ip=192.168.0.231&timeout=60&max_scripts=5"
curl -X POST "http://localhost:8004/parse-xml?xml_path=/path/to/xml"

# 6. Access web dashboard
# Visit http://localhost:3000 for the React web interface

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

---

### Test Results Summary

All services tested successfully with target IP `192.168.0.231`:

- **✅ auto_nessus_service**: Running, graceful Nessus handling
- **✅ nmapscanner_service**: OS scan + intelligent script selection
- **✅ nmapall_service**: Limited script execution (safety)
- **✅ osscan_service**: OS fingerprinting (Linux 5.4 detected)
- **✅ portxmlparser_service**: XML parsing with archival

**Container Health**: All 5 containers showing `healthy` status
**Persistence**: Verified across container restarts
**Folder Organization**: All scans create timestamped folders
**Performance**: Response times < 10ms for health checks

---

*Last updated: July 16, 2025*
*Version: 2.0.0 (Microservices Architecture)*
