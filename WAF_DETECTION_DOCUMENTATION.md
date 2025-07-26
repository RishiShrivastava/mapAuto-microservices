# =Juggernaut= WAF Detection Service Documentation

## Overview
The WAF Detection Service is an advanced Web Application Firewall identification and analysis tool that provides comprehensive detection, fingerprinting, and vulnerability assessment capabilities.

## Features

### 🛡️ Comprehensive WAF Detection
- **8 Major WAF Types Supported**:
  - Cloudflare
  - AWS WAF  
  - Akamai
  - Incapsula
  - ModSecurity
  - Barracuda
  - F5 Application Security Manager
  - Imperva SecureSphere

### 🔍 Detection Methods
- **HTTP Response Analysis**: Headers, cookies, status codes
- **Content Pattern Matching**: Server responses and error pages
- **Payload Testing**: XSS, SQL Injection, Command Injection, Path Traversal
- **Nmap Integration**: Advanced scripted detection (intensive mode)

### 🚨 Security Analysis
- **Weakness Identification**: Known vulnerabilities for each WAF type
- **Bypass Techniques**: Common evasion methods
- **Security Recommendations**: Actionable remediation advice

## API Endpoints

### Health Check
```bash
GET /status
```
Returns service health status.

### WAF Detection
```bash
POST /detect-waf?target=<URL_OR_IP>&timeout=300&intensive=false
```

**Parameters:**
- `target`: Target URL or IP address (required)
- `timeout`: Scan timeout in seconds (default: 300)
- `intensive`: Enable nmap scans for deeper analysis (default: false)

**Example:**
```bash
curl -X POST "https://localhost/api/waf/detect-waf?target=example.com&timeout=60&intensive=false" -k
```

### WAF Signatures
```bash
GET /waf-signatures
```
Returns supported WAF types and detection capabilities.

## Response Format

```json
{
  "target_url": "example.com",
  "waf_detected": true,
  "waf_type": "cloudflare", 
  "waf_name": "Cloudflare",
  "confidence_level": 0.85,
  "detection_methods": ["HTTP Response Analysis"],
  "weaknesses": [
    "Origin IP discovery via DNS records",
    "Subdomain enumeration bypass"
  ],
  "bypass_techniques": [
    "X-Originating-IP header manipulation",
    "X-Forwarded-For spoofing"
  ],
  "security_recommendations": [
    "Implement proper rate limiting",
    "Use multiple layers of security"
  ],
  "scan_timestamp": "2025-07-25T18:00:00.000000",
  "scan_duration": 2.5
}
```

## Web Dashboard Usage

### Access
1. Navigate to: `https://localhost`
2. Go to the **Scanner Tab**
3. Look for the **WAF Detection** card (red security icon)

### Configuration
1. **WAF Target**: Enter URL (https://example.com) or IP address
2. **Timeout**: Set scan duration (60-300 seconds recommended)
3. **Intensive Scanning**: Enable for nmap-based detection (slower but more thorough)

### Results Interpretation

#### WAF Detected
- **Green Chip**: No WAF detected
- **Orange Chip**: WAF detected with type and confidence level
- **Weaknesses Section**: Known vulnerabilities specific to the detected WAF
- **Bypass Techniques**: Common evasion methods for testing
- **Recommendations**: Security hardening advice

#### No WAF Detected
- Recommendations for implementing WAF protection
- General security best practices

## Security Considerations

### Responsible Usage
- ⚠️ **Only scan authorized targets**
- Use for legitimate security assessments
- Respect rate limits and terms of service
- Do not use bypass techniques on unauthorized systems

### Legal Compliance
- Ensure proper authorization before scanning
- Follow responsible disclosure practices
- Comply with local laws and regulations

## Technical Details

### WAF Fingerprinting Techniques

1. **Header Analysis**
   - Server headers (e.g., `cf-ray` for Cloudflare)
   - Security headers
   - Custom WAF headers

2. **Cookie Analysis**
   - WAF-specific cookies (e.g., `__cfduid` for Cloudflare)
   - Session tracking patterns

3. **Response Code Analysis**
   - HTTP status codes (403, 503, 406)
   - Response timing patterns

4. **Content Pattern Matching**
   - Error page content
   - WAF-specific strings
   - Blocking messages

5. **Payload Testing**
   - Malicious request submission
   - Response analysis for blocking behavior
   - Pattern recognition in responses

### Performance Characteristics
- **Basic Scan**: 2-5 seconds
- **Intensive Scan**: 30-120 seconds (includes nmap)
- **Memory Usage**: ~50MB per scan
- **Concurrent Scans**: Limited by timeout settings

## Integration Examples

### Command Line
```bash
# Basic WAF detection
curl -X POST "https://localhost/api/waf/detect-waf?target=example.com" -k

# Intensive scan with longer timeout
curl -X POST "https://localhost/api/waf/detect-waf?target=example.com&timeout=180&intensive=true" -k
```

### Python Script
```python
import requests

response = requests.post(
    'https://localhost/api/waf/detect-waf',
    params={
        'target': 'example.com',
        'timeout': 60,
        'intensive': False
    },
    verify=False
)

result = response.json()
if result['waf_detected']:
    print(f"WAF Detected: {result['waf_name']}")
    print(f"Confidence: {result['confidence_level']:.1%}")
else:
    print("No WAF detected")
```

## Troubleshooting

### Common Issues

1. **"Invalid IP address or URL format"**
   - Ensure target format is correct
   - Use full URLs with protocol for web targets
   - Use IP addresses for direct scans

2. **Scan timeouts**
   - Increase timeout parameter
   - Check target availability
   - Use intensive=false for faster scans

3. **No WAF detected on known protected sites**
   - Try intensive=true for deeper analysis
   - Some WAFs are designed to be stealthy
   - Check if target is actually behind a WAF

### Log Analysis
```bash
# View WAF detection service logs
sudo docker logs mapauto-waf-detection

# Real-time log monitoring
sudo docker logs -f mapauto-waf-detection
```

## File Locations

- **Service Code**: `/app/main.py`
- **Results Storage**: `/app/waf_results/`
- **Configuration**: `/app/data/`
- **Logs**: Container logs via Docker

## Service Architecture

```
Internet → Nginx (443) → WAF Detection Service (8005)
                      ↓
                 Target Analysis
                      ↓
            Results + Recommendations
```

## Version History

- **v1.0.0**: Initial release with 8 WAF types, HTTP analysis, payload testing
- Future: Additional WAF signatures, machine learning detection, API rate limiting

---

**⚠️ Security Notice**: This tool is for authorized security testing only. Unauthorized scanning may violate terms of service or local laws. Always obtain proper permission before testing systems you do not own.

=Juggernaut= WAF Detection Service - Advanced Security Analysis Platform
