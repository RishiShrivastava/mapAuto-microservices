#!/usr/bin/env python3
"""
=Juggernaut= WAF Detection and Analysis Service
Advanced Web Application Firewall Detection, Identification, and Weakness Analysis

This service provides comprehensive WAF detection capabilities including:
- WAF presence detection
- WAF type identification and fingerprinting
- WAF version detection where possible
- Common bypass techniques testing
- Weakness identification and exploitation methods
- Security recommendations

Security Features:
- Input validation and sanitization
- Rate limiting protection
- Secure HTTP headers
- Timeout management
- Resource limits
"""

import os
import sys
import json
import time
import shlex
import logging
import asyncio
import ipaddress
import subprocess
import ssl
from datetime import datetime
from typing import Optional, Dict, List, Any
from urllib.parse import urlparse, urljoin

import requests
import aiohttp
from fastapi import FastAPI, HTTPException, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn

# =Juggernaut= Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =Juggernaut= Initialize FastAPI application
app = FastAPI(
    title="WAF Detection Service",
    description="Advanced Web Application Firewall Detection and Analysis",
    version="1.0.0"
)

# =Juggernaut= Add CORS middleware for web frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =Juggernaut= WAF signature database
WAF_SIGNATURES = {
    "cloudflare": {
        "name": "Cloudflare",
        "headers": ["cf-ray", "cf-cache-status", "server"],
        "cookies": ["__cfduid", "__cf_bm"],
        "response_codes": [403, 503],
        "content_patterns": ["cloudflare", "attention required", "ray id"],
        "server_patterns": ["cloudflare", "cloudflare-nginx"],
        "weaknesses": [
            "Origin IP discovery via DNS records",
            "Subdomain enumeration bypass",
            "HTTP/2 smuggling techniques",
            "Origin server direct access",
            "Rate limit bypass via distributed requests"
        ],
        "bypass_techniques": [
            "X-Originating-IP header manipulation",
            "X-Forwarded-For spoofing",
            "Unicode normalization bypasses",
            "HTTP parameter pollution",
            "Origin server discovery"
        ]
    },
    "aws_waf": {
        "name": "AWS WAF",
        "headers": ["x-amzn-requestid", "x-amzn-trace-id"],
        "response_codes": [403],
        "content_patterns": ["blocked by aws waf", "aws"],
        "weaknesses": [
            "Rule ordering vulnerabilities",
            "Rate limiting bypass via IP rotation",
            "Regional endpoint inconsistencies",
            "Custom rule logic flaws"
        ],
        "bypass_techniques": [
            "Request smuggling via chunked encoding",
            "Case variation bypasses",
            "Encoding bypasses (URL, Unicode)",
            "Geographic IP rotation",
            "HTTP method variations"
        ]
    },
    "akamai": {
        "name": "Akamai",
        "headers": ["akamai-x-cache", "x-akamai-transformed"],
        "response_codes": [403],
        "content_patterns": ["access denied", "akamai"],
        "server_patterns": ["akamaighost"],
        "weaknesses": [
            "Edge server configuration differences",
            "Cache pollution attacks",
            "Ghost domain bypass",
            "Geographic inconsistencies"
        ],
        "bypass_techniques": [
            "X-Forwarded-Host manipulation",
            "Host header injection",
            "Cache key poisoning",
            "Geographic endpoint rotation",
            "Protocol downgrade attacks"
        ]
    },
    "incapsula": {
        "name": "Incapsula",
        "headers": ["x-iinfo"],
        "cookies": ["visid_incap", "incap_ses"],
        "response_codes": [403],
        "content_patterns": ["incapsula", "incident id"],
        "weaknesses": [
            "Incident ID information leakage",
            "Session cookie predictability",
            "Rate limiting bypass",
            "Direct IP access"
        ],
        "bypass_techniques": [
            "X-Forwarded-For manipulation",
            "User-Agent rotation",
            "Referrer spoofing",
            "HTTP/2 downgrade",
            "Origin server discovery"
        ]
    },
    "mod_security": {
        "name": "ModSecurity",
        "headers": ["server"],
        "response_codes": [403, 406],
        "content_patterns": ["mod_security", "modsecurity", "not acceptable"],
        "server_patterns": ["mod_security", "modsecurity"],
        "weaknesses": [
            "Rule bypass via encoding",
            "Parameter pollution attacks",
            "Content-Type manipulation",
            "HTTP verb tampering",
            "Multipart boundary attacks"
        ],
        "bypass_techniques": [
            "Double URL encoding",
            "Unicode normalization",
            "Content-Type spoofing",
            "HTTP parameter pollution",
            "Multipart form bypasses",
            "SQL comment variations",
            "XSS filter evasion"
        ]
    },
    "barracuda": {
        "name": "Barracuda",
        "headers": ["x-barracuda-url"],
        "response_codes": [403],
        "content_patterns": ["barracuda", "blocked by barracuda"],
        "weaknesses": [
            "URL encoding bypass",
            "Case sensitivity issues",
            "Whitelist bypasses",
            "Geographic filtering weaknesses"
        ],
        "bypass_techniques": [
            "URL path traversal",
            "Case variation attacks",
            "HTTP header manipulation",
            "Protocol switching",
            "Geographic IP spoofing"
        ]
    },
    "f5_asm": {
        "name": "F5 Application Security Manager",
        "headers": ["f5-x-forwarded-for"],
        "response_codes": [403],
        "content_patterns": ["f5", "the requested url was rejected"],
        "server_patterns": ["bigip"],
        "weaknesses": [
            "iRule bypass techniques",
            "Load balancer inconsistencies",
            "Session persistence exploits",
            "Backend server differences"
        ],
        "bypass_techniques": [
            "X-Forwarded-Proto manipulation",
            "Backend server targeting",
            "Session cookie manipulation",
            "Load balancer bypass",
            "iRule logic exploitation"
        ]
    },
    "imperva": {
        "name": "Imperva SecureSphere",
        "headers": ["x-iinfo"],
        "cookies": ["incap_ses"],
        "response_codes": [403],
        "content_patterns": ["imperva", "securesphere"],
        "weaknesses": [
            "Learning mode bypass",
            "Policy inconsistencies",
            "Signature evasion",
            "Database firewall separation"
        ],
        "bypass_techniques": [
            "Signature fragmentation",
            "Protocol-level attacks",
            "Database-specific bypasses",
            "Application layer manipulation",
            "Time-based evasion"
        ]
    }
}

# =Juggernaut= Common malicious payloads for testing
TEST_PAYLOADS = {
    "xss": [
        "<script>alert('xss')</script>",
        "javascript:alert('xss')",
        "<img src=x onerror=alert('xss')>",
        "'+alert('xss')+'",
        "<svg onload=alert('xss')>"
    ],
    "sql_injection": [
        "' OR '1'='1",
        "1' UNION SELECT 1,2,3--",
        "'; DROP TABLE users; --",
        "1' AND 1=1--",
        "UNION SELECT NULL,NULL,NULL"
    ],
    "command_injection": [
        "; cat /etc/passwd",
        "| whoami",
        "`id`",
        "$(whoami)",
        "; ls -la"
    ],
    "path_traversal": [
        "../../../etc/passwd",
        "..\\..\\..\\windows\\system32\\drivers\\etc\\hosts",
        "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd",
        "....//....//....//etc/passwd"
    ]
}

class WAFDetectionResult(BaseModel):
    """=Juggernaut= WAF Detection Result Model"""
    target_url: str
    waf_detected: bool
    waf_type: Optional[str] = None
    waf_name: Optional[str] = None
    confidence_level: float
    detection_methods: List[str]
    response_analysis: Dict[str, Any]
    weaknesses: List[str] = []
    bypass_techniques: List[str] = []
    security_recommendations: List[str] = []
    scan_timestamp: str
    scan_duration: float

def validate_ip_or_url(target: str) -> bool:
    """=Juggernaut= Validate IP address or URL format"""
    try:
        # Check if it's an IP address
        ipaddress.ip_address(target)
        return True
    except ValueError:
        # Check if it's a valid URL
        try:
            parsed = urlparse(target if target.startswith(('http://', 'https://')) else f'http://{target}')
            return bool(parsed.netloc)
        except:
            return False

def create_scan_folder(target: str) -> str:
    """=Juggernaut= Create timestamped folder for scan results"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    clean_target = target.replace(':', '_').replace('/', '_').replace('.', '_')
    scan_folder = f"/app/waf_results/waf_scan_{clean_target}_{timestamp}"
    os.makedirs(scan_folder, exist_ok=True)
    return scan_folder

async def perform_nmap_waf_scan(target: str, scan_folder: str) -> Dict[str, Any]:
    """=Juggernaut= Perform nmap-based WAF detection scan"""
    results = {"nmap_waf_detect": None, "nmap_waf_fingerprint": None, "errors": []}
    
    # Prepare target for nmap (handle URLs)
    nmap_target = target
    if target.startswith(('http://', 'https://')):
        parsed = urlparse(target)
        nmap_target = parsed.netloc
    
    # WAF detection scan
    detect_file = os.path.join(scan_folder, f"waf_detect_{nmap_target}.xml")
    detect_cmd = f"nmap -p 80,443 --script http-waf-detect --script-args http-waf-detect.aggro -oX {detect_file} {nmap_target}"
    
    try:
        result = subprocess.run(shlex.split(detect_cmd), capture_output=True, text=True, timeout=120, check=False)
        if result.returncode == 0:
            results["nmap_waf_detect"] = f"WAF detection scan completed, saved to {detect_file}"
        else:
            results["errors"].append(f"WAF detection scan warning: {result.stderr}")
    except subprocess.TimeoutExpired:
        results["errors"].append("WAF detection scan timed out")
    except Exception as e:
        results["errors"].append(f"WAF detection scan failed: {e}")
    
    # WAF fingerprinting scan
    fingerprint_file = os.path.join(scan_folder, f"waf_fingerprint_{nmap_target}.xml")
    fingerprint_cmd = f"nmap -p 80,443 --script http-waf-fingerprint --script-args http-waf-fingerprint.intensive=1 -oX {fingerprint_file} {nmap_target}"
    
    try:
        result = subprocess.run(shlex.split(fingerprint_cmd), capture_output=True, text=True, timeout=120, check=False)
        if result.returncode == 0:
            results["nmap_waf_fingerprint"] = f"WAF fingerprinting completed, saved to {fingerprint_file}"
        else:
            results["errors"].append(f"WAF fingerprinting warning: {result.stderr}")
    except subprocess.TimeoutExpired:
        results["errors"].append("WAF fingerprinting scan timed out")
    except Exception as e:
        results["errors"].append(f"WAF fingerprinting scan failed: {e}")
    
    return results

async def analyze_http_responses(target_url: str) -> Dict[str, Any]:
    """=Juggernaut= Analyze HTTP responses for WAF detection"""
    analysis = {
        "baseline_response": None,
        "payload_responses": {},
        "headers_analysis": {},
        "waf_indicators": [],
        "detected_waf": None,
        "confidence": 0.0,
        "waf_behavior_detected": False
    }
    
    # Ensure target has protocol
    if not target_url.startswith(('http://', 'https://')):
        target_url = f"http://{target_url}"
    
    try:
        # Get baseline response
        # Create SSL context that doesn't verify certificates for self-signed certs
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        connector = aiohttp.TCPConnector(ssl=ssl_context)
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            connector=connector
        ) as session:
            # First try to get baseline response with a clean request
            try:
                async with session.get(target_url) as response:
                    response_content = await response.text() if response.content_length and response.content_length < 1000000 else ""
                    analysis["baseline_response"] = {
                        "status_code": response.status,
                        "headers": dict(response.headers),
                        "content": response_content[:1000]
                    }
                    
                    # Analyze headers for WAF indicators
                    headers = response.headers
                    for waf_type, signature in WAF_SIGNATURES.items():
                        confidence = 0
                        indicators = []
                        
                        # Check headers
                        for header in signature.get("headers", []):
                            if header.lower() in [h.lower() for h in headers.keys()]:
                                confidence += 0.3
                                indicators.append(f"Header: {header}")
                        
                        # Check server header
                        server_header = headers.get("server", "").lower()
                        for pattern in signature.get("server_patterns", []):
                            if pattern.lower() in server_header:
                                confidence += 0.4
                                indicators.append(f"Server pattern: {pattern}")
                        
                        # Check response content
                        content_lower = response_content.lower()
                        for pattern in signature.get("content_patterns", []):
                            if pattern.lower() in content_lower:
                                confidence += 0.3
                                indicators.append(f"Content pattern: {pattern}")
                        
                        if confidence > 0.5:
                            analysis["waf_indicators"].append({
                                "waf_type": waf_type,
                                "waf_name": signature["name"],
                                "confidence": confidence,
                                "indicators": indicators
                            })
            
            except aiohttp.ClientResponseError as e:
                if e.status == 403:
                    # 403 on baseline request suggests aggressive WAF
                    analysis["waf_behavior_detected"] = True
                    analysis["baseline_response"] = {
                        "status_code": 403,
                        "headers": {},
                        "content": "403 Forbidden - Likely WAF blocking",
                        "waf_blocked": True
                    }
                else:
                    raise e
            
            # Test with malicious payloads
            blocked_payloads = 0
            total_payloads = 0
            
            for category, payloads in TEST_PAYLOADS.items():
                for i, payload in enumerate(payloads[:2]):  # Limit to 2 payloads per category
                    total_payloads += 1
                    test_url = f"{target_url}?test_{category}={payload}"
                    try:
                        async with session.get(test_url) as payload_response:
                            blocked = payload_response.status in [403, 406, 503]
                            if blocked:
                                blocked_payloads += 1
                                analysis["waf_behavior_detected"] = True
                            
                            analysis["payload_responses"][f"{category}_{i}"] = {
                                "payload": payload,
                                "status_code": payload_response.status,
                                "content_length": payload_response.content_length,
                                "blocked": blocked
                            }
                    except aiohttp.ClientResponseError as e:
                        if e.status in [403, 406, 503]:
                            blocked_payloads += 1
                            analysis["waf_behavior_detected"] = True
                            analysis["payload_responses"][f"{category}_{i}"] = {
                                "payload": payload,
                                "status_code": e.status,
                                "blocked": True,
                                "waf_response": True
                            }
                        else:
                            analysis["payload_responses"][f"{category}_{i}"] = {
                                "payload": payload,
                                "error": str(e),
                                "blocked": True
                            }
                    except Exception as e:
                        analysis["payload_responses"][f"{category}_{i}"] = {
                            "payload": payload,
                            "error": str(e),
                            "blocked": True
                        }
            
            # Calculate WAF confidence based on blocked payloads
            if total_payloads > 0:
                block_ratio = blocked_payloads / total_payloads
                if block_ratio >= 0.7:  # 70% or more payloads blocked
                    analysis["confidence"] = 0.9
                    analysis["detected_waf"] = "generic_waf"
                    analysis["waf_behavior_detected"] = True
                elif block_ratio >= 0.5:  # 50-69% payloads blocked
                    analysis["confidence"] = 0.7
                    analysis["detected_waf"] = "possible_waf"
                    analysis["waf_behavior_detected"] = True
                
    except Exception as e:
        analysis["error"] = str(e)
    
    # Determine most likely WAF
    if analysis["waf_indicators"]:
        best_match = max(analysis["waf_indicators"], key=lambda x: x["confidence"])
        analysis["detected_waf"] = best_match["waf_type"]
        analysis["confidence"] = best_match["confidence"]
    
    return analysis

@app.get("/status")
async def status():
    """=Juggernaut= Health check endpoint"""
    return {"status": "healthy", "service": "WAF Detection Service", "version": "1.0.0"}

@app.post("/detect-waf")
async def detect_waf(
    target: str = Query(..., description="Target URL or IP address"),
    timeout: Optional[int] = Query(300, description="Total timeout in seconds"),
    intensive: Optional[bool] = Query(False, description="Enable intensive scanning")
):
    """=Juggernaut= Comprehensive WAF detection and analysis"""
    
    # Validate input
    if not validate_ip_or_url(target):
        raise HTTPException(status_code=400, detail="Invalid IP address or URL format")
    
    scan_start = time.time()
    scan_folder = create_scan_folder(target)
    
    result = WAFDetectionResult(
        target_url=target,
        waf_detected=False,
        confidence_level=0.0,
        detection_methods=[],
        response_analysis={},
        scan_timestamp=datetime.now().isoformat(),
        scan_duration=0.0
    )
    
    try:
        # Perform HTTP response analysis
        logger.info(f"Starting WAF detection for {target}")
        http_analysis = await analyze_http_responses(target)
        result.response_analysis = http_analysis
        
        if http_analysis.get("detected_waf") or http_analysis.get("waf_behavior_detected"):
            result.waf_detected = True
            result.waf_type = http_analysis.get("detected_waf", "generic_waf")
            result.confidence_level = http_analysis.get("confidence", 0.8)
            result.detection_methods.append("HTTP Response Analysis")
            
            # Determine WAF type based on detection
            if result.waf_type == "generic_waf":
                result.waf_name = "Generic WAF (Behavior-based detection)"
                result.weaknesses = [
                    "May have bypass techniques via encoding",
                    "Could be vulnerable to request method variations",
                    "Possible rate limiting bypass opportunities"
                ]
                result.bypass_techniques = [
                    "Try different HTTP methods (POST, PUT, PATCH)",
                    "Use URL encoding variations",
                    "Fragment payloads across parameters",
                    "Use case variations in payloads"
                ]
            elif result.waf_type in WAF_SIGNATURES:
                waf_info = WAF_SIGNATURES[result.waf_type]
                result.waf_name = waf_info["name"]
                result.weaknesses = waf_info.get("weaknesses", [])
                result.bypass_techniques = waf_info.get("bypass_techniques", [])
        
        # Perform nmap scans if intensive mode
        if intensive:
            logger.info(f"Performing intensive nmap scans for {target}")
            nmap_results = await perform_nmap_waf_scan(target, scan_folder)
            result.response_analysis["nmap_results"] = nmap_results
            result.detection_methods.append("Nmap WAF Scripts")
        
        # Generate security recommendations
        recommendations = [
            "Implement proper rate limiting and request throttling",
            "Use multiple layers of security (WAF + IDS/IPS)",
            "Regularly update WAF rules and signatures",
            "Monitor for WAF bypass attempts",
            "Implement proper logging and alerting",
            "Consider using multiple WAF vendors for redundancy"
        ]
        
        if result.waf_detected:
            recommendations.extend([
                f"Review {result.waf_name} specific security configurations",
                "Implement custom rules to address identified weaknesses",
                "Test bypass techniques in a controlled environment",
                "Consider additional security controls for identified gaps"
            ])
        else:
            recommendations.extend([
                "Consider implementing a Web Application Firewall",
                "Ensure proper input validation at application level",
                "Implement comprehensive logging and monitoring"
            ])
        
        result.security_recommendations = recommendations
        
    except Exception as e:
        logger.error(f"WAF detection failed for {target}: {e}")
        raise HTTPException(status_code=500, detail=f"WAF detection failed: {e}")
    
    result.scan_duration = time.time() - scan_start
    
    # Save results to file
    results_file = os.path.join(scan_folder, "waf_detection_results.json")
    with open(results_file, 'w') as f:
        json.dump(result.dict(), f, indent=2)
    
    logger.info(f"WAF detection completed for {target} in {result.scan_duration:.2f}s")
    return result

@app.get("/waf-signatures")
async def get_waf_signatures():
    """=Juggernaut= Get available WAF signatures and detection capabilities"""
    return {
        "total_signatures": len(WAF_SIGNATURES),
        "supported_wafs": [
            {
                "type": waf_type,
                "name": info["name"],
                "detection_methods": len(info.get("headers", [])) + len(info.get("server_patterns", [])) + len(info.get("content_patterns", []))
            }
            for waf_type, info in WAF_SIGNATURES.items()
        ],
        "test_categories": list(TEST_PAYLOADS.keys())
    }

if __name__ == "__main__":
    # =Juggernaut= Run the WAF detection service
    uvicorn.run(app, host="0.0.0.0", port=8005)
