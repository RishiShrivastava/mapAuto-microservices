# MapAuto Microservices

This directory contains FastAPI-based microservices for each main function of the MapAuto toolkit.

## Microservices
- **auto_nessus_service**: Manage Nessus scans
- **nmapscanner_service**: Intelligent Nmap scanning
- **nmapall_service**: Run all Nmap scripts
- **osscan_service**: OS fingerprinting
- **portxmlparser_service**: Parse Nmap XML output

## Quick Start

1. **Configure Environment**
   - Copy or edit the `.env` file in the parent directory with your credentials and settings.

2. **Build and Run All Services**
   ```bash
   docker-compose up --build
   ```

3. **Access Services**
   - AutoNessus:       http://localhost:8000/status
   - NmapScanner:      http://localhost:8001/status
   - NmapAll:          http://localhost:8002/status
   - OSScan:           http://localhost:8003/status
   - PortXmlParser:    http://localhost:8004/status

## Development
- Each service has its own `main.py`, `requirements.txt`, and `Dockerfile`.
- Add your logic to the relevant FastAPI endpoints in each service.

## Security
- Never commit real credentials to version control.
- Use the `.env` file for secrets and environment variables.

## Extending
- Add new endpoints to each service as needed.
- Add new microservices for additional functionality.

---

# Fail-Safe Features & Usage

All microservices have been enhanced with comprehensive fail-safes to prevent hanging, resource exhaustion, and security issues.

## Fail-Safe Features Added

### 1. IP Address Validation
- **What**: Validates IP address format before processing
- **Why**: Prevents invalid input from causing errors
- **Implementation**: Uses `ipaddress.ip_address()` to validate format
- **Services**: All scanning services (nmapall, nmapscanner, osscan)

### 2. Process Timeouts
- **What**: Prevents processes from hanging indefinitely
- **Why**: Prevents resource exhaustion and service unavailability
- **Implementation**: Uses `subprocess.run()` with timeout parameter
- **Services**: All scanning services

### 3. Resource Limits
- **What**: Limits number of scripts/ports processed
- **Why**: Prevents memory/CPU exhaustion
- **Implementation**: 
  - nmapall_service: Limits to 10 scripts by default
  - nmapscanner_service: Limits to 5 scripts per port
  - portxmlparser_service: Limits to 1000 ports, 50MB file size
- **Services**: All services

### 4. Error Handling
- **What**: Graceful handling of subprocess errors
- **Why**: Prevents service crashes and provides meaningful error messages
- **Implementation**: Try-catch blocks with specific error types
- **Services**: All services

### 5. File System Safety
- **What**: Validates file paths and permissions
- **Why**: Prevents path traversal and access errors
- **Implementation**: Checks file existence, readability, and size
- **Services**: portxmlparser_service

### 6. Network Security
- **What**: Safer nmap parameters to prevent aggressive scanning
- **Why**: Reduces chance of hanging and being detected as malicious
- **Implementation**: Uses -T4, --max-retries 1, --host-timeout
- **Services**: nmapscanner_service, osscan_service

### 7. XML Parsing Safety
- **What**: Validates XML structure before processing
- **Why**: Prevents crashes from malformed XML
- **Implementation**: ET.ParseError handling
- **Services**: portxmlparser_service

### 8. Service Binding Safety
- **What**: Binds services to localhost only
- **Why**: Prevents external access and interference from scans
- **Implementation**: Use 127.0.0.1 instead of 0.0.0.0
- **Services**: All services

## Usage Examples

### Safe nmapall_service call:
```bash
curl -X POST "http://localhost:8000/scan-all?ip=192.168.1.1&timeout=300&max_scripts=5"
```

### Safe nmapscanner_service call:
```bash
curl -X POST "http://localhost:8001/scan?ip=192.168.1.1&timeout=600"
```

### Safe osscan_service call:
```bash
curl -X POST "http://localhost:8002/os-scan?ip=192.168.1.1&timeout=120"
```

### Safe portxmlparser_service call:
```bash
curl -X POST "http://localhost:8003/parse-xml?xml_path=/tmp/scan_results.xml"
```

## Cleanup Script
Use `/home/kali/Documents/mapauto/mapAuto/mapauto-microservices/cleanup_processes.sh` to safely stop all services and clean up temporary files.

## Key Safety Parameters

| Service | Default Timeout | Resource Limits | Safety Features |
|---------|----------------|----------------|----------------|
| nmapall_service | 300s | 10 scripts max | IP validation, script timeouts |
| nmapscanner_service | 600s | 5 scripts/port | Distributed timeouts, safer nmap params |
| osscan_service | 120s | N/A | Process timeout, error handling |
| portxmlparser_service | N/A | 1000 ports, 50MB | File validation, XML parsing safety |

## Error Response Format
All services now return structured error responses:
```json
{
  "error": "Description of error",
  "timeout_used": 300,
  "details": "Additional context"
}
```

## Best Practices
1. Always use timeout parameters
2. Monitor service logs for warnings
3. Use cleanup script between tests
4. Bind services to localhost only
5. Validate inputs before calling services

---
