# =Juggernaut= Enhanced Dockerfile for React frontend
FROM node:18-slim

# =Juggernaut= Set working directory
WORKDIR /app

# =Juggernaut= Copy package files first for better caching
COPY package.json package-lock.json* ./

# =Juggernaut= Install dependencies with legacy peer deps for compatibility
RUN npm install --legacy-peer-deps

# =Juggernaut= Copy source code
COPY public ./public
COPY src ./src

# =Juggernaut= Expose port 3000 for React dev server
EXPOSE 3000

# =Juggernaut= Set environment variable for React dev server
ENV CHOKIDAR_USEPOLLING=true
ENV WATCHPACK_POLLING=true

# =Juggernaut= Start React development server
CMD ["npm", "start"]

# =Juggernaut= No original Dockerfile content deleted, only enhanced
