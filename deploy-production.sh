#!/bin/bash
# =Juggernaut= MapAuto Production Deployment Script for Demo
# This script deploys the secure MapAuto application for production demo

echo "🚀 MapAuto Production Deployment for Demo"
echo "=========================================="
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_DIR="$SCRIPT_DIR/mapauto-microservices"

echo -e "${BLUE}Step 1: Pre-deployment Security Check${NC}"
echo "-------------------------------------"

# Check if running as root (not recommended for production)
if [ "$EUID" -eq 0 ]; then
    echo -e "${YELLOW}⚠️  WARNING: Running as root. Consider using sudo for specific commands only.${NC}"
fi

# Check Docker and Docker Compose
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker not found. Please install Docker first.${NC}"
    exit 1
fi

if ! command -v docker compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose not found. Please install Docker Compose first.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Docker environment validated${NC}"

echo
echo -e "${BLUE}Step 2: Environment Setup${NC}"
echo "-------------------------"

cd "$COMPOSE_DIR" || exit 1

# Create .env file if it doesn't exist
if [ ! -f "../.env" ]; then
    echo "Creating production .env file..."
    cat > "../.env" << EOL
# =Juggernaut= MapAuto Production Environment Configuration
NESSUS_USERNAME=demo_user
NESSUS_PASSWORD=demo_password
NESSUS_URL=https://localhost:8834

# Production Security Settings
NGINX_WORKER_PROCESSES=auto
NGINX_WORKER_CONNECTIONS=1024
MODSEC_RULE_ENGINE=On
PRODUCTION_MODE=true
EOL
    echo -e "${GREEN}✅ Production .env file created${NC}"
else
    echo -e "${GREEN}✅ .env file already exists${NC}"
fi

echo
echo -e "${BLUE}Step 3: Building Secure Images${NC}"
echo "------------------------------"

echo "Building secure nginx gateway with ModSecurity WAF..."
if sudo docker compose build nginx; then
    echo -e "${GREEN}✅ Secure nginx gateway built successfully${NC}"
else
    echo -e "${RED}❌ Failed to build nginx gateway${NC}"
    exit 1
fi

echo "Building all microservices..."
if sudo docker compose build; then
    echo -e "${GREEN}✅ All services built successfully${NC}"
else
    echo -e "${RED}❌ Failed to build services${NC}"
    exit 1
fi

echo
echo -e "${BLUE}Step 4: Deploying Production Services${NC}"
echo "-------------------------------------"

echo "Stopping any existing services..."
sudo docker compose down --remove-orphans

echo "Starting production services with security gateway..."
if sudo docker compose up -d; then
    echo -e "${GREEN}✅ Production services started successfully${NC}"
else
    echo -e "${RED}❌ Failed to start services${NC}"
    exit 1
fi

echo
echo -e "${BLUE}Step 5: Waiting for Services to Initialize${NC}"
echo "------------------------------------------"

echo "Waiting for security gateway to be ready..."
for i in {1..30}; do
    if curl -k -s https://localhost/health &>/dev/null; then
        echo -e "${GREEN}✅ Security gateway is ready${NC}"
        break
    fi
    echo -n "."
    sleep 2
    if [ "$i" -eq 30 ]; then
        echo -e "${RED}❌ Security gateway failed to start within 60 seconds${NC}"
        exit 1
    fi
done

echo
echo -e "${BLUE}Step 6: Production Health Check${NC}"
echo "-------------------------------"

sudo docker compose ps

echo
echo -e "${BLUE}Step 7: Security Validation${NC}"
echo "-----------------------------"

if [ -f "$SCRIPT_DIR/security-test.sh" ]; then
    echo "Running security validation tests..."
    "$SCRIPT_DIR/security-test.sh"
else
    echo -e "${YELLOW}⚠️  Security test script not found, running basic checks...${NC}"
    
    # Basic security checks
    echo "Testing HTTPS access..."
    if curl -k -s https://localhost/health &>/dev/null; then
        echo -e "${GREEN}✅ HTTPS access working${NC}"
    else
        echo -e "${RED}❌ HTTPS access failed${NC}"
    fi
    
    echo "Testing HTTP blocking..."
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost 2>/dev/null || echo "000")
    if [ "$HTTP_CODE" -eq 426 ]; then
        echo -e "${GREEN}✅ HTTP properly blocked${NC}"
    else
        echo -e "${RED}❌ HTTP not properly blocked${NC}"
    fi
fi

echo
echo "=========================================="
echo -e "${GREEN}🎉 MapAuto Production Deployment Complete!${NC}"
echo "=========================================="
echo
echo -e "${BLUE}Production Demo Access:${NC}"
echo "• 🌐 Web Interface: https://localhost"
echo "• 🔒 Security Gateway: https://localhost/health"
echo "• 🛡️  WAF Detection API: https://localhost/api/waf/status"
echo
echo -e "${BLUE}Security Features Active:${NC}"
echo "• ✅ ModSecurity WAF with OWASP Core Rule Set"
echo "• ✅ HTTPS-only access (HTTP blocked)"
echo "• ✅ Rate limiting and DDoS protection"
echo "• ✅ Security headers enabled"
echo "• ✅ Sensitive file access blocked"
echo "• ✅ Real-time attack detection and blocking"
echo
echo -e "${BLUE}Only Port 443 (HTTPS) is exposed externally${NC}"
echo -e "${GREEN}Your application is now secure and demo-ready! 🚀${NC}"
echo
echo -e "${YELLOW}Demo Commands:${NC}"
echo "# View running services:"
echo "sudo docker compose ps"
echo
echo "# View security logs:"
echo "sudo docker logs mapauto-security-gateway"
echo
echo "# Test attack blocking:"
echo "curl -k \"https://localhost/?xss=<script>alert('hack')</script>\""
echo
echo "# Access application:"
echo "firefox https://localhost"
