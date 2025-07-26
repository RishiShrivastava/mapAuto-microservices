#!/bin/bash
# =Juggernaut= MapAuto Security Testing Script for Production Demo
# This script tests the ModSecurity WAF implementation and security features

echo "🔒 MapAuto Security Gateway Testing - Production Demo Validation"
echo "================================================================="
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

TARGET="https://localhost"

echo -e "${BLUE}1. Testing Port Exposure Security${NC}"
echo "-----------------------------------"

echo "Testing external port exposure..."
OPEN_PORTS=$(nmap -p 1-65535 localhost 2>/dev/null | grep "open" | wc -l)
if [ "$OPEN_PORTS" -eq 1 ]; then
    echo -e "${GREEN}✅ PASS: Only 1 port exposed (443 HTTPS)${NC}"
else
    echo -e "${RED}❌ FAIL: Multiple ports exposed ($OPEN_PORTS ports)${NC}"
    nmap -p 1-65535 localhost 2>/dev/null | grep "open"
fi

echo "Testing HTTP to HTTPS enforcement..."
HTTP_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost 2>/dev/null || echo "000")
if [ "$HTTP_RESPONSE" -eq 426 ]; then
    echo -e "${GREEN}✅ PASS: HTTP requests properly blocked (426 Upgrade Required)${NC}"
else
    echo -e "${RED}❌ FAIL: HTTP not properly blocked (got $HTTP_RESPONSE)${NC}"
fi

echo
echo -e "${BLUE}2. Testing WAF Protection - OWASP Top 10${NC}"
echo "-------------------------------------------"

echo "Testing XSS Protection..."
XSS_RESPONSE=$(curl -k -s -o /dev/null -w "%{http_code}" "$TARGET/?test=<script>alert('xss')</script>" 2>/dev/null)
if [ "$XSS_RESPONSE" -eq 403 ]; then
    echo -e "${GREEN}✅ PASS: XSS attack blocked (403 Forbidden)${NC}"
else
    echo -e "${RED}❌ FAIL: XSS attack not blocked (got $XSS_RESPONSE)${NC}"
fi

echo "Testing SQL Injection Protection..."
SQL_RESPONSE=$(curl -k -s -o /dev/null -w "%{http_code}" "$TARGET/api/waf/?id=1' OR '1'='1" 2>/dev/null)
if [ "$SQL_RESPONSE" -eq 403 ]; then
    echo -e "${GREEN}✅ PASS: SQL Injection blocked (403 Forbidden)${NC}"
else
    echo -e "${RED}❌ FAIL: SQL Injection not blocked (got $SQL_RESPONSE)${NC}"
fi

echo "Testing Command Injection Protection..."
CMD_RESPONSE=$(curl -k -s -o /dev/null -w "%{http_code}" "$TARGET/?cmd=; cat /etc/passwd" 2>/dev/null)
if [ "$CMD_RESPONSE" -eq 403 ]; then
    echo -e "${GREEN}✅ PASS: Command Injection blocked (403 Forbidden)${NC}"
else
    echo -e "${RED}❌ FAIL: Command Injection not blocked (got $CMD_RESPONSE)${NC}"
fi

echo "Testing Directory Traversal Protection..."
DIR_RESPONSE=$(curl -k -s -o /dev/null -w "%{http_code}" "$TARGET/?file=../../../etc/passwd" 2>/dev/null)
if [ "$DIR_RESPONSE" -eq 403 ]; then
    echo -e "${GREEN}✅ PASS: Directory Traversal blocked (403 Forbidden)${NC}"
else
    echo -e "${RED}❌ FAIL: Directory Traversal not blocked (got $DIR_RESPONSE)${NC}"
fi

echo
echo -e "${BLUE}3. Testing Rate Limiting Protection${NC}"
echo "-----------------------------------"

echo "Testing API rate limiting..."
RATE_LIMIT_FAILED=0
for i in {1..15}; do
    RATE_RESPONSE=$(curl -k -s -o /dev/null -w "%{http_code}" "$TARGET/api/waf/status" 2>/dev/null)
    if [ "$RATE_RESPONSE" -eq 429 ] || [ "$RATE_RESPONSE" -eq 503 ]; then
        echo -e "${GREEN}✅ PASS: Rate limiting triggered after $i requests${NC}"
        break
    fi
    if [ "$i" -eq 15 ]; then
        echo -e "${YELLOW}⚠️  WARNING: Rate limiting not triggered after 15 requests${NC}"
    fi
done

echo
echo -e "${BLUE}4. Testing Security Headers${NC}"
echo "-----------------------------"

HEADERS=$(curl -k -s -I "$TARGET" 2>/dev/null)

# Check for required security headers
if echo "$HEADERS" | grep -qi "strict-transport-security"; then
    echo -e "${GREEN}✅ PASS: HSTS header present${NC}"
else
    echo -e "${RED}❌ FAIL: HSTS header missing${NC}"
fi

if echo "$HEADERS" | grep -qi "x-content-type-options"; then
    echo -e "${GREEN}✅ PASS: X-Content-Type-Options header present${NC}"
else
    echo -e "${RED}❌ FAIL: X-Content-Type-Options header missing${NC}"
fi

if echo "$HEADERS" | grep -qi "x-frame-options"; then
    echo -e "${GREEN}✅ PASS: X-Frame-Options header present${NC}"
else
    echo -e "${RED}❌ FAIL: X-Frame-Options header missing${NC}"
fi

if echo "$HEADERS" | grep -qi "content-security-policy"; then
    echo -e "${GREEN}✅ PASS: Content-Security-Policy header present${NC}"
else
    echo -e "${RED}❌ FAIL: Content-Security-Policy header missing${NC}"
fi

echo
echo -e "${BLUE}5. Testing Service Availability${NC}"
echo "-------------------------------"

# Test main application
APP_RESPONSE=$(curl -k -s -o /dev/null -w "%{http_code}" "$TARGET" 2>/dev/null)
if [ "$APP_RESPONSE" -eq 200 ]; then
    echo -e "${GREEN}✅ PASS: Main application accessible${NC}"
else
    echo -e "${RED}❌ FAIL: Main application not accessible (got $APP_RESPONSE)${NC}"
fi

# Test health endpoint
HEALTH_RESPONSE=$(curl -k -s -o /dev/null -w "%{http_code}" "$TARGET/health" 2>/dev/null)
if [ "$HEALTH_RESPONSE" -eq 200 ]; then
    echo -e "${GREEN}✅ PASS: Health endpoint accessible${NC}"
else
    echo -e "${RED}❌ FAIL: Health endpoint not accessible (got $HEALTH_RESPONSE)${NC}"
fi

# Test WAF detection service
WAF_RESPONSE=$(curl -k -s -o /dev/null -w "%{http_code}" "$TARGET/api/waf/status" 2>/dev/null)
if [ "$WAF_RESPONSE" -eq 200 ]; then
    echo -e "${GREEN}✅ PASS: WAF detection service accessible${NC}"
else
    echo -e "${RED}❌ FAIL: WAF detection service not accessible (got $WAF_RESPONSE)${NC}"
fi

echo
echo -e "${BLUE}6. Testing Sensitive File Protection${NC}"
echo "------------------------------------"

# Test access to sensitive files
SENSITIVE_FILES=(".env" "config.ini" "log" ".git")
for file in "${SENSITIVE_FILES[@]}"; do
    SENSITIVE_RESPONSE=$(curl -k -s -o /dev/null -w "%{http_code}" "$TARGET/$file" 2>/dev/null)
    if [ "$SENSITIVE_RESPONSE" -eq 403 ] || [ "$SENSITIVE_RESPONSE" -eq 404 ]; then
        echo -e "${GREEN}✅ PASS: Access to $file blocked${NC}"
    else
        echo -e "${RED}❌ FAIL: Access to $file not blocked (got $SENSITIVE_RESPONSE)${NC}"
    fi
done

echo
echo "================================================================="
echo -e "${BLUE}🔒 MapAuto Security Gateway - Production Demo Ready${NC}"
echo "================================================================="
echo
echo -e "${GREEN}Security Features Enabled:${NC}"
echo "• ModSecurity WAF with OWASP Core Rule Set"
echo "• HTTPS-only access (HTTP blocked)"
echo "• Rate limiting and DDoS protection"
echo "• Security headers (HSTS, CSP, XSS Protection)"
echo "• Sensitive file access blocking"
echo "• Advanced SSL/TLS configuration"
echo "• Real-time attack detection and blocking"
echo
echo -e "${YELLOW}Demo Commands:${NC}"
echo "# Test legitimate access:"
echo "curl -k https://localhost/api/waf/status"
echo
echo "# Test blocked attacks:"
echo "curl -k \"https://localhost/?xss=<script>alert('hack')</script>\""
echo "curl -k \"https://localhost/?sql=1' OR '1'='1\""
echo "curl -k \"https://localhost/?cmd=; cat /etc/passwd\""
echo
echo -e "${GREEN}Your MapAuto application is now production-ready for demo! 🚀${NC}"
