# 🚀 Quick Reference Guide

## Table of Contents
- [Local Development](#local-development)
- [Docker Commands](#docker-commands)
- [API Testing](#api-testing)
- [Common Issues](#common-issues)
- [Useful Commands](#useful-commands)

---

## Local Development

### Start Backend
```bash
cd server
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```
**URL**: http://localhost:8000
**Docs**: http://localhost:8000/docs

### Start Frontend
```bash
cd client
npm install
npm run dev
```
**URL**: http://localhost:5173

### Seed Database
```bash
cd server
python seed.py
```

---

## Docker Commands

### Start All Services
```bash
docker-compose up -d
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f mongodb
```

### Stop Services
```bash
docker-compose down
```

### Rebuild
```bash
docker-compose up -d --build
```

### Seed Database (Docker)
```bash
docker-compose exec backend python seed.py
```

### Access MongoDB Shell
```bash
docker-compose exec mongodb mongosh
```

---

## API Testing

### Register User
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "test123",
    "role": "trainee",
    "organization": "Test Org"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "admin123"
  }'
```

### Get Current User (with token)
```bash
curl -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Create Session
```bash
curl -X POST http://localhost:8000/api/sessions \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Python Training",
    "description": "Advanced Python concepts",
    "start_time": "2025-01-20T09:00:00",
    "end_time": "2025-01-20T11:00:00"
  }'
```

---

## Common Issues

### Issue: MongoDB Connection Error
**Solution**:
```bash
# Check MongoDB is running
docker-compose ps mongodb

# Restart MongoDB
docker-compose restart mongodb

# Check logs
docker-compose logs mongodb
```

### Issue: Frontend Can't Connect to Backend
**Solution**:
```bash
# Check VITE_API_BASE_URL in .env
echo $VITE_API_BASE_URL

# Should be: http://localhost:8000

# Restart frontend
npm run dev
```

### Issue: CORS Error
**Solution**:
Update `server/.env`:
```env
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Issue: Port Already in Use
**Solution**:
```bash
# Find process using port 8000
lsof -i :8000  # Mac/Linux
netstat -ano | findstr :8000  # Windows

# Kill process
kill -9 PID  # Mac/Linux
taskkill /PID PID /F  # Windows
```

---

## Useful Commands

### Check Running Services
```bash
# Docker
docker-compose ps

# Processes
ps aux | grep python  # Backend
ps aux | grep node    # Frontend
```

### Database Operations
```bash
# MongoDB shell
docker-compose exec mongodb mongosh

# In mongosh:
use smart_attendance
db.users.find()
db.sessions.find()
db.attendance.find()
```

### Clean Up
```bash
# Remove containers and volumes
docker-compose down -v

# Clean Docker system
docker system prune -a

# Remove node_modules
rm -rf client/node_modules

# Remove Python cache
find . -type d -name __pycache__ -exec rm -r {} +
```

### Environment Variables
```bash
# Backend (.env)
MONGODB_URL=mongodb://localhost:27017/smart_attendance
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
CORS_ORIGINS=http://localhost:5173

# Frontend (.env)
VITE_API_BASE_URL=http://localhost:8000
```

### Build Production
```bash
# Frontend
cd client
npm run build
npm run preview

# Backend (with Docker)
docker build -t backend:prod ./server
docker run -p 8000:8000 backend:prod
```

---

## Default Credentials (After Seeding)

### Admin
- Email: `admin@example.com`
- Password: `admin123`

### Instructor
- Email: `john.instructor@example.com`
- Password: `instructor123`

### Trainee
- Email: `alice.trainee@example.com`
- Password: `trainee123`

---

## Health Checks

### Backend
```bash
curl http://localhost:8000/docs
```
Should return: 200 OK

### Frontend
```bash
curl http://localhost:5173
```
Should return: 200 OK

### MongoDB
```bash
docker exec mongodb mongosh --eval "db.adminCommand('ping')"
```
Should return: `{ ok: 1 }`

---

## Git Workflow

### Commit Changes
```bash
git add .
git commit -m "Description of changes"
git push origin master
```

### Create Branch
```bash
git checkout -b feature/new-feature
git push -u origin feature/new-feature
```

### Update from Remote
```bash
git pull origin master
```

---

## Performance Tips

1. **Backend**: Use MongoDB indexes
   ```javascript
   db.users.createIndex({ email: 1 })
   db.attendance.createIndex({ user_id: 1, session_id: 1 })
   ```

2. **Frontend**: Build for production
   ```bash
   npm run build
   ```

3. **Docker**: Use build cache
   ```bash
   docker-compose build --parallel
   ```

---

## Monitoring

### Check Logs
```bash
# Backend logs
docker-compose logs -f backend

# Frontend logs
docker-compose logs -f frontend

# Database logs
docker-compose logs -f mongodb
```

### Resource Usage
```bash
docker stats
```

---

## Security Checklist

- [ ] Change default SECRET_KEY in production
- [ ] Use strong MongoDB passwords
- [ ] Enable HTTPS with SSL certificates
- [ ] Update CORS_ORIGINS for production domain
- [ ] Rotate JWT tokens regularly
- [ ] Keep dependencies updated
- [ ] Use environment-specific .env files

---

## Links

- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Frontend**: http://localhost:5173
- **GitHub**: https://github.com/Satyasuranjeet/smart-attendance-system

---

**Need Help?**
- Check [DEPLOYMENT.md](./docs/DEPLOYMENT.md) for detailed deployment
- Check [PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md) for overview
- Open an issue on GitHub

---

Last Updated: January 2025
