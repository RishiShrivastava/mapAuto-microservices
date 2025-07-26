# =Juggernaut= Secure Nginx with ModSecurity WAF for Production Demo
FROM owasp/modsecurity-crs:nginx

# =Juggernaut= Create SSL certificate directory
RUN mkdir -p /etc/nginx/certs

# =Juggernaut= Create ModSecurity configuration directory with proper permissions
RUN mkdir -p /etc/nginx/modsecurity.d && chown -R nginx:nginx /etc/nginx/modsecurity.d

# =Juggernaut= Generate SSL certificate for HTTPS
RUN openssl req -x509 -nodes -days 365 -newkey rsa:4096 \
    -keyout /etc/nginx/certs/key.pem \
    -out /etc/nginx/certs/cert.pem \
    -subj "/C=US/ST=Production/L=Demo/O=MapAuto Security/CN=localhost"

# =Juggernaut= Copy nginx configuration adapted for MapAuto services
COPY nginx.conf /etc/nginx/templates/conf.d/default.conf.template

# =Juggernaut= Copy ModSecurity include configuration
COPY include.conf /etc/nginx/modsecurity.d/include.conf

# =Juggernaut= Only expose HTTPS port for external access  
EXPOSE 443
