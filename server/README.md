# Smart Attendance System - Backend

FastAPI-based backend for the Smart Attendance System with MongoDB, JWT authentication, and QR code generation.

## 🚀 Features

- **JWT Authentication**: Secure token-based authentication with bcrypt password hashing
- **Role-Based Access Control**: Admin, Instructor, and Trainee roles with different permissions
- **MongoDB Database**: Async Motor driver for efficient database operations
- **QR Code System**: Dynamic QR code generation with expiry logic
- **RESTful API**: Well-structured endpoints following REST conventions
- **Auto-generated Documentation**: Interactive API docs at `/docs` (Swagger UI)

## 📋 Prerequisites

- Python 3.9 or higher
- MongoDB 4.4 or higher
- pip (Python package manager)

## 🛠️ Installation

1. **Navigate to the server directory**:
   ```bash
   cd server
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   # Copy the example env file
   cp .env.example .env
   
   # Edit .env and update with your configuration
   ```

## ⚙️ Configuration

Edit the `.env` file with your settings:

```env
# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=smart_attendance

# JWT Configuration
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# QR Code Configuration
QR_CODE_EXPIRY_MINUTES=15

# CORS Configuration
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

## 🚦 Running the Server

### Development Mode

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📚 API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register` | Register new user | No |
| POST | `/api/auth/login` | Login and get JWT token | No |
| GET | `/api/auth/me` | Get current user profile | Yes |

### Sessions (Coming in Part 2)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/sessions/` | Create new session | Yes (Admin/Instructor) |
| GET | `/api/sessions/:id` | Get session details | Yes |
| GET | `/api/sessions/:id/qr` | Get QR code for session | Yes (Admin/Instructor) |

### Attendance (Coming in Part 2)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/attendance/scan` | Mark attendance via QR | Yes (Trainee) |
| GET | `/api/attendance/user/:id` | Get user attendance history | Yes |

### Admin (Coming in Part 3)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/admin/stats` | Get system statistics | Yes (Admin) |
| GET | `/api/miss-requests` | Get all miss requests | Yes (Admin) |
| PATCH | `/api/miss-requests/:id` | Approve/reject request | Yes (Admin) |

## 🗄️ Database Schema

### Collections

1. **users**
   - Stores user information, credentials, and roles
   - Fields: name, email, password_hash, role, organization_type, org_name, created_at

2. **sessions**
   - Stores class/training sessions
   - Fields: title, description, created_by, start_time, end_time, qr_code_id, active

3. **attendance_records**
   - Stores attendance marks
   - Fields: session_id, user_id, status, timestamp, method

4. **qr_codes**
   - Stores generated QR codes with expiry
   - Fields: session_id, code_value, expires_at, created_at

5. **miss_requests**
   - Stores missed attendance correction requests
   - Fields: user_id, session_id, reason, status, admin_response, created_at

## 🔐 Authentication Flow

1. **Register**: User registers with email, password, and organization details
2. **Login**: User logs in with credentials, receives JWT token
3. **Access Protected Routes**: Include token in Authorization header: `Bearer <token>`

## 🧪 Testing

Test the API using the interactive documentation:

1. Open http://localhost:8000/docs
2. Click on an endpoint
3. Click "Try it out"
4. Fill in the parameters
5. Execute the request

Or use curl:

```bash
# Register a user
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "securepass123",
    "organization_type": "college",
    "org_name": "MIT",
    "role": "trainee"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepass123"
  }'

# Get current user (with token)
curl -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer <your-token-here>"
```

## 📂 Project Structure

```
server/
├── main.py                 # Application entry point
├── config.py               # Configuration settings
├── database.py             # MongoDB connection and setup
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── models/                # Pydantic models
│   ├── user.py
│   ├── session.py
│   ├── attendance.py
│   ├── qr_code.py
│   └── miss_request.py
├── routes/                # API route handlers
│   └── auth.py
└── utils/                 # Utility functions
    ├── auth.py           # JWT and password utilities
    └── qr_generator.py   # QR code generation
```

## 🛡️ Security Features

- **Password Hashing**: Bcrypt with automatic salt generation
- **JWT Tokens**: Secure token-based authentication
- **Role-Based Access**: Endpoint protection based on user roles
- **QR Expiry**: Time-limited QR codes to prevent replay attacks
- **CORS Protection**: Configurable allowed origins

## 🐛 Troubleshooting

### MongoDB Connection Issues

```bash
# Check if MongoDB is running
# On Windows
net start MongoDB

# On macOS/Linux
sudo systemctl status mongod
```

### Import Errors

```bash
# Make sure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## 📝 Next Steps

- ✅ Part 1: Backend foundation (Current)
- ⏳ Part 2: Session management and QR code system
- ⏳ Part 3: Admin dashboard and analytics
- ⏳ Part 4: Frontend authentication
- ⏳ Part 5: Frontend dashboards
- ⏳ Part 6: Docker and deployment

## 🤝 Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for contribution guidelines.

## 📄 License

This project is open source and available under the MIT License.
