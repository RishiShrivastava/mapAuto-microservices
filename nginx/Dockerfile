# =Juggernaut= Nginx Dockerfile for HTTPS reverse proxy
FROM nginx:alpine

# =Juggernaut= Install openssl for generating self-signed certificates
RUN apk add --no-cache openssl

# =Juggernaut= Create SSL directory
RUN mkdir -p /etc/nginx/ssl

# =Juggernaut= Generate self-signed SSL certificate for development
RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/nginx/ssl/key.pem \
    -out /etc/nginx/ssl/cert.pem \
    -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"

# =Juggernaut= Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# =Juggernaut= Expose HTTPS and HTTP ports
EXPOSE 80 443

# =Juggernaut= No original Dockerfile deleted, this is a new file
