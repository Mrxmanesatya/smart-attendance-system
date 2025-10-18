# 🚀 Deployment Guide

Complete guide for deploying the Smart Attendance System to production.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Docker Deployment](#docker-deployment)
4. [Cloud Deployment](#cloud-deployment)
5. [Database Setup](#database-setup)
6. [Security Considerations](#security-considerations)
7. [Monitoring & Maintenance](#monitoring--maintenance)

---

## Prerequisites

### Required Software
- **Docker** 20.10+ and Docker Compose 2.0+
- **Node.js** 20+ (for local builds)
- **Python** 3.10+
- **MongoDB** 4.4+ or MongoDB Atlas account
- **Git** for version control

### Recommended Tools
- **Nginx** for reverse proxy (if not using Docker)
- **SSL Certificate** (Let's Encrypt recommended)
- **Monitoring** (Prometheus, Grafana, or similar)

---

## Environment Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/smart-attendance-system.git
cd smart-attendance-system
```

### 2. Create Environment Files

#### Backend (.env)
Create `server/.env`:

```env
# Database
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/smart_attendance

# Security
SECRET_KEY=your-super-secret-key-min-32-characters-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# CORS
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Optional: Email (for notifications)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

#### Frontend (.env.production)
Create `client/.env.production`:

```env
VITE_API_BASE_URL=https://api.yourdomain.com
```

### 3. Generate Secret Key

```bash
# Python method
python -c "import secrets; print(secrets.token_urlsafe(32))"

# OpenSSL method
openssl rand -base64 32
```

---

## Docker Deployment

### Option 1: Docker Compose (Recommended for Quick Deploy)

1. **Update docker-compose.yml** with your environment variables

2. **Build and start services**:
   ```bash
   docker-compose up -d --build
   ```

3. **Verify services**:
   ```bash
   docker-compose ps
   docker-compose logs -f
   ```

4. **Seed database** (first time only):
   ```bash
   docker-compose exec backend python seed.py
   ```

5. **Access the application**:
   - Frontend: http://localhost
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Option 2: Separate Containers

```bash
# Build images
docker build -t smart-attendance-backend:latest ./server
docker build -t smart-attendance-frontend:latest ./client

# Create network
docker network create smart-attendance-network

# Run MongoDB
docker run -d \
  --name mongodb \
  --network smart-attendance-network \
  -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=admin123 \
  -v mongodb_data:/data/db \
  mongo:7.0

# Run Backend
docker run -d \
  --name backend \
  --network smart-attendance-network \
  -p 8000:8000 \
  -e MONGODB_URL=mongodb://admin:admin123@mongodb:27017/smart_attendance \
  -e SECRET_KEY=your-secret-key \
  smart-attendance-backend:latest

# Run Frontend
docker run -d \
  --name frontend \
  --network smart-attendance-network \
  -p 80:80 \
  smart-attendance-frontend:latest
```

---

## Cloud Deployment

### AWS Deployment

#### 1. Using AWS ECS (Elastic Container Service)

```bash
# Install AWS CLI
pip install awscli

# Configure AWS
aws configure

# Create ECR repositories
aws ecr create-repository --repository-name smart-attendance-backend
aws ecr create-repository --repository-name smart-attendance-frontend

# Build and push images
$(aws ecr get-login --no-include-email --region us-east-1)
docker tag smart-attendance-backend:latest YOUR_AWS_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/smart-attendance-backend:latest
docker push YOUR_AWS_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/smart-attendance-backend:latest

# Deploy using ECS Task Definition (create via AWS Console or CLI)
```

#### 2. Using AWS Elastic Beanstalk

```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p docker smart-attendance-system

# Create environment
eb create smart-attendance-prod

# Deploy
eb deploy
```

### Google Cloud Platform (GCP)

```bash
# Install gcloud CLI
# https://cloud.google.com/sdk/docs/install

# Authenticate
gcloud auth login

# Set project
gcloud config set project YOUR_PROJECT_ID

# Build and push to GCR
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/smart-attendance-backend ./server
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/smart-attendance-frontend ./client

# Deploy to Cloud Run
gcloud run deploy smart-attendance-backend \
  --image gcr.io/YOUR_PROJECT_ID/smart-attendance-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

gcloud run deploy smart-attendance-frontend \
  --image gcr.io/YOUR_PROJECT_ID/smart-attendance-frontend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Azure Deployment

```bash
# Install Azure CLI
# https://docs.microsoft.com/en-us/cli/azure/install-azure-cli

# Login
az login

# Create resource group
az group create --name smart-attendance-rg --location eastus

# Create container registry
az acr create --resource-group smart-attendance-rg \
  --name smartattendanceacr --sku Basic

# Build and push
az acr build --registry smartattendanceacr \
  --image smart-attendance-backend:latest ./server

# Deploy to Azure Container Instances
az container create \
  --resource-group smart-attendance-rg \
  --name smart-attendance-backend \
  --image smartattendanceacr.azurecr.io/smart-attendance-backend:latest \
  --dns-name-label smart-attendance-api \
  --ports 8000
```

### Heroku Deployment

```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Create app
heroku create smart-attendance-system

# Add MongoDB addon
heroku addons:create mongolab:sandbox

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set ALGORITHM=HS256

# Deploy
git push heroku master

# Open app
heroku open
```

---

## Database Setup

### MongoDB Atlas (Recommended)

1. **Create Account**: https://www.mongodb.com/cloud/atlas

2. **Create Cluster**:
   - Choose free tier (M0) for testing
   - Select region closest to your users
   - Click "Create Cluster"

3. **Configure Access**:
   - Database Access: Create database user
   - Network Access: Add IP address (0.0.0.0/0 for all IPs, or specific IPs)

4. **Get Connection String**:
   - Click "Connect" → "Connect your application"
   - Copy connection string
   - Replace `<username>`, `<password>`, and database name

5. **Create Indexes** (Run once):
   ```javascript
   use smart_attendance

   // Users collection
   db.users.createIndex({ email: 1 }, { unique: true })
   db.users.createIndex({ role: 1 })

   // Sessions collection
   db.sessions.createIndex({ instructor_id: 1 })
   db.sessions.createIndex({ start_time: -1 })
   db.sessions.createIndex({ is_active: 1 })

   // Attendance collection
   db.attendance.createIndex({ user_id: 1, session_id: 1 })
   db.attendance.createIndex({ session_id: 1 })
   db.attendance.createIndex({ timestamp: -1 })

   // QR Codes collection
   db.qr_codes.createIndex({ expires_at: 1 }, { expireAfterSeconds: 0 })
   db.qr_codes.createIndex({ value: 1 }, { unique: true })
   ```

### Self-Hosted MongoDB

```bash
# Using Docker
docker run -d \
  --name mongodb \
  -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=your-password \
  -v /path/to/data:/data/db \
  mongo:7.0

# Backup
docker exec mongodb mongodump --out /backup

# Restore
docker exec mongodb mongorestore /backup
```

---

## Security Considerations

### 1. Environment Variables
- ✅ Never commit `.env` files
- ✅ Use strong SECRET_KEY (32+ characters)
- ✅ Rotate secrets regularly
- ✅ Use different keys for dev/staging/prod

### 2. HTTPS/SSL
```nginx
# Nginx SSL configuration
server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /path/to/fullchain.pem;
    ssl_certificate_key /path/to/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://frontend:80;
    }

    location /api/ {
        proxy_pass http://backend:8000;
    }
}
```

### 3. Database Security
- ✅ Enable authentication
- ✅ Use connection string with credentials
- ✅ Whitelist IP addresses
- ✅ Enable encryption at rest (MongoDB Atlas)
- ✅ Regular backups

### 4. Application Security
- ✅ JWT token expiration
- ✅ Rate limiting
- ✅ Input validation
- ✅ CORS configuration
- ✅ Password hashing (bcrypt)

---

## Monitoring & Maintenance

### Health Checks

```bash
# Backend health
curl http://localhost:8000/docs

# Frontend health
curl http://localhost/

# Database health
docker exec mongodb mongosh --eval "db.adminCommand('ping')"
```

### Logs

```bash
# Docker Compose
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f mongodb

# Individual containers
docker logs -f container_name
```

### Backup Script

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"

# Backup MongoDB
docker exec mongodb mongodump \
  --out $BACKUP_DIR/mongo_$DATE

# Compress
tar -czf $BACKUP_DIR/backup_$DATE.tar.gz \
  $BACKUP_DIR/mongo_$DATE

# Upload to S3 (optional)
aws s3 cp $BACKUP_DIR/backup_$DATE.tar.gz \
  s3://your-bucket/backups/

# Cleanup old backups (keep last 7 days)
find $BACKUP_DIR -name "backup_*.tar.gz" -mtime +7 -delete
```

### Cron Job for Backups

```bash
# Edit crontab
crontab -e

# Add daily backup at 2 AM
0 2 * * * /path/to/backup.sh
```

---

## Troubleshooting

### Common Issues

1. **Connection refused to MongoDB**
   ```bash
   # Check MongoDB is running
   docker ps | grep mongodb
   
   # Check network connectivity
   docker exec backend ping mongodb
   ```

2. **CORS errors**
   ```env
   # Update CORS_ORIGINS in .env
   CORS_ORIGINS=https://yourdomain.com
   ```

3. **Build failures**
   ```bash
   # Clear Docker cache
   docker system prune -a
   
   # Rebuild without cache
   docker-compose build --no-cache
   ```

---

## Support

For deployment issues:
1. Check logs: `docker-compose logs`
2. Verify environment variables
3. Test health endpoints
4. Open an issue: https://github.com/yourusername/smart-attendance-system/issues

---

**Last Updated**: 2025
