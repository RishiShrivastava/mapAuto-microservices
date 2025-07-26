# =Juggernaut= WAF Detection Service Dockerfile
FROM python:3.11-slim

# =Juggernaut= Install system dependencies for WAF detection
RUN apt-get update && apt-get install -y \
    nmap \
    curl \
    wget \
    dnsutils \
    whois \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

# =Juggernaut= Set working directory
WORKDIR /app

# =Juggernaut= Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# =Juggernaut= Copy WAF detection service code
COPY . .

# =Juggernaut= Create directories for results and data
RUN mkdir -p /app/waf_results /app/data /app/signatures

# =Juggernaut= Set proper permissions
RUN chmod +x /app/*.py

# =Juggernaut= Expose port for WAF detection service
EXPOSE 8005

# =Juggernaut= Health check for container
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8005/status || exit 1

# =Juggernaut= Run the WAF detection service
CMD ["python", "main.py"]
