# =Juggernaut= MapAuto Web Dashboard Status Report & Tutorial

## 🚀 SYSTEM STATUS: ALL SYSTEMS OPERATIONAL

### Container Status Summary:
✅ **mapauto-nginx** - HEALTHY (HTTPS Proxy on port 443/80)
✅ **auto_nessus** - HEALTHY (Port 8000)
✅ **nmapscanner** - HEALTHY (Port 8001) 
✅ **nmapall** - HEALTHY (Port 8002)
✅ **osscan** - HEALTHY (Port 8003)
✅ **portxmlparser** - HEALTHY (Port 8004)
⚠️ **frontend** - RUNNING (Port 3000) - React app working fine

### Access Points:
🔒 **HTTPS Web Dashboard**: https://localhost (Port 443) - PRIMARY ACCESS
🔓 **HTTP Redirect**: http://localhost (Port 80) - Redirects to HTTPS
🛠️ **Development Access**: http://localhost:3000 - Direct React access

---

## 📋 HOW TO USE THE MAPAUTO WEB DASHBOARD

### Step 1: Access the Dashboard
1. Open your web browser
2. Go to: **https://localhost**
3. Accept the self-signed certificate warning (for development)
4. You'll see the MapAuto Network Scanner Dashboard

### Step 2: Dashboard Overview
The dashboard has 3 main tabs:
- **Scanner Tab**: Configure and run scans
- **Results Tab**: View scan results in real-time
- **History Tab**: See previous scan history

### Step 3: Configure Your Scan
In the **Scanner Tab**:
1. **Target IP Address**: Enter the IP you want to scan (e.g., 192.168.0.231)
2. **Timeout (seconds)**: Set scan timeout (default: 60s)
3. **Max Scripts**: For comprehensive scans (default: 5)
4. **XML File Path**: For parsing existing XML results

### Step 4: Available Scan Types

#### 🔍 **OS Scan** (Blue Button)
- **Purpose**: Identifies the operating system
- **Service**: Port 8003
- **Best for**: Quick OS fingerprinting
- **Example Result**: "Linux 5.0 - 5.4"

#### 🌐 **Nmap Scan** (Purple Button)  
- **Purpose**: Intelligent port scanning with script execution
- **Service**: Port 8001
- **Best for**: Comprehensive security assessment
- **Example Result**: Open ports with service details

#### ⚡ **Nmap All Scripts** (Orange Button)
- **Purpose**: Run extensive Nmap script collection
- **Service**: Port 8002
- **Best for**: Deep vulnerability assessment
- **Warning**: Takes longer, use carefully

#### 📄 **Parse XML** (Blue Button)
- **Purpose**: Parse existing Nmap XML files
- **Service**: Port 8004
- **Best for**: Analyzing saved scan results
- **Input**: Full path to XML file

#### 🛡️ **Nessus Status** (Green Button)
- **Purpose**: Check Nessus service connectivity
- **Service**: Port 8000
- **Best for**: Verifying Nessus integration

### Step 5: Running a Scan
1. Enter your target IP (e.g., 192.168.0.231)
2. Click the desired scan type button
3. Watch the loading indicator
4. Results appear automatically in the **Results Tab**

### Step 6: Understanding Results
Results show:
- **Target Information**: IP address scanned
- **Open Ports**: List of accessible services
- **Scan Details**: Folder location, timing
- **Raw JSON**: Complete technical details

### Step 7: Scan History
- All scans are automatically saved
- Access via **History Tab**
- Shows timestamp, scan type, and target
- Click to expand and view previous results

---

## 🔧 COMMAND LINE ACCESS (Alternative)

If you prefer command line access:

```bash
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

---

## 🛡️ SECURITY FEATURES

### HTTPS Encryption
- All web traffic encrypted via SSL/TLS
- Self-signed certificate for development
- Production deployments should use proper certificates

### Network Isolation
- Backend services only accessible through nginx proxy
- No direct external access to microservices
- Localhost binding for security

### Input Validation
- IP address format validation
- File path validation for XML parsing
- Timeout limits to prevent resource exhaustion

---

## 📊 MONITORING & HEALTH CHECKS

### Service Health
All services have built-in health checks:
- **Nginx**: Tests HTTPS endpoint
- **Frontend**: Tests React development server
- **Backend Services**: Tests API endpoints

### Log Monitoring
```bash
# View all service logs
sudo docker compose logs -f

# View specific service logs
sudo docker logs mapauto-frontend
sudo docker logs mapauto-nginx
```

---

## 🚨 TROUBLESHOOTING

### Common Issues:

#### "Cannot connect to https://localhost"
- Check if nginx container is running: `sudo docker ps | grep nginx`
- Restart if needed: `sudo docker compose restart nginx`

#### "Frontend shows errors"
- Check frontend logs: `sudo docker logs mapauto-frontend`
- Restart frontend: `sudo docker compose restart frontend`

#### "Scan not working"
- Verify target IP is reachable
- Check timeout settings (increase if needed)
- View backend service logs for errors

#### "SSL Certificate Warning"
- This is normal for development (self-signed certificate)
- Click "Advanced" → "Proceed to localhost" in browser

---

## 🔄 SYSTEM MANAGEMENT

### Starting All Services
```bash
cd /home/kali/Documents/mapauto/mapAuto-microservices/mapauto-microservices
sudo docker compose up -d
```

### Stopping All Services
```bash
sudo docker compose down
```

### Rebuilding After Changes
```bash
sudo docker compose up --build -d
```

### View Status
```bash
sudo docker compose ps
```

---

## 🎯 BEST PRACTICES

1. **Always use HTTPS**: Access via https://localhost for security
2. **Set appropriate timeouts**: Longer for comprehensive scans
3. **Monitor resources**: Check system performance during scans
4. **Review scan history**: Learn from previous results
5. **Use development responsibly**: Only scan authorized targets

---

## 📞 SUPPORT

- **Configuration Files**: `/home/kali/Documents/mapauto/mapAuto-microservices/`
- **Logs**: `sudo docker compose logs [service-name]`
- **Health Status**: Available in dashboard or via `sudo docker compose ps`

**🎉 Your MapAuto Web Dashboard is now fully operational with HTTPS on port 443!**

=Juggernaut= Complete tutorial and status report generated
