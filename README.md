# Smart Attendance System 📱✅

A comprehensive QR code-based Smart Attendance System with role-based access control, built for corporate offices, colleges, gyms, and training institutes.

[![GitHub stars](https://img.shields.io/github/stars/yourusername/smart-attendance-system)](https://github.com/yourusername/smart-attendance-system/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/yourusername/smart-attendance-system)](https://github.com/yourusername/smart-attendance-system/network)
[![GitHub issues](https://img.shields.io/github/issues/yourusername/smart-attendance-system)](https://github.com/yourusername/smart-attendance-system/issues)
[![Hacktoberfest](https://img.shields.io/badge/Hacktoberfest-2025-blueviolet)](https://hacktoberfest.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🌟 Features

- **QR-Based Attendance**: Dynamic QR code generation with time expiry (15 min) for secure attendance marking
- **Role-Based Access Control**: Three distinct roles - Admin, Instructor, and Trainee
- **JWT Authentication**: Secure token-based authentication with bcrypt password hashing
- **Interactive Dashboards**: Role-specific dashboards with analytics and charts
- **Attendance Analytics**: Track attendance trends, generate reports, and export data (CSV/Excel)
- **Miss Request System**: Trainees can raise missed attendance correction requests
- **Responsive Design**: Clean, modern UI built with React and Tailwind CSS
- **Scalable Architecture**: FastAPI backend with MongoDB for efficient data handling
- **Docker Ready**: Complete containerization with Docker and Docker Compose
- **CI/CD Pipeline**: Automated testing and deployment with GitHub Actions

## 🏗️ Tech Stack

### Frontend
- **Framework**: React 19 with Vite 6
- **Styling**: Tailwind CSS 4
- **Charts**: Recharts 3
- **QR Scanner**: HTML5 QR Code 2.3
- **HTTP Client**: Axios 1.12
- **Routing**: React Router 7
- **State Management**: React Context API
- **Notifications**: React Hot Toast

### Backend
- **Framework**: FastAPI 0.109 (Python 3.10)
- **Database**: MongoDB with Motor (async driver)
- **Authentication**: JWT with python-jose
- **Password Hashing**: Bcrypt via passlib
- **QR Generation**: qrcode library with PIL
- **Data Export**: pandas + openpyxl for Excel export
- **Configuration**: Pydantic Settings

### DevOps
- **Containerization**: Docker & Docker Compose
- **CI/CD**: GitHub Actions
- **Web Server**: Nginx (production)
- **Monitoring**: Health checks & logging

## 📂 Project Structure

```
smart-attendance-system/
├── client/                 # React frontend
│   ├── src/
│   │   ├── components/    # Reusable components
│   │   ├── pages/         # Page components
│   │   ├── context/       # Auth & app context
│   │   ├── utils/         # Utility functions
│   │   └── App.jsx        # Main app component
│   ├── public/            # Static assets
│   └── package.json       # Frontend dependencies
│
├── server/                # FastAPI backend
│   ├── models/            # Pydantic models
│   ├── routes/            # API endpoints
│   ├── utils/             # Utility functions
│   ├── main.py            # Application entry
│   ├── config.py          # Configuration
│   ├── database.py        # MongoDB connection
│   └── requirements.txt   # Python dependencies
│
├── docs/                  # Documentation (to be added)
├── .github/               # GitHub Actions CI/CD (to be added)
├── CODE_OF_CONDUCT.md     # Contributor Covenant
├── CONTRIBUTING.md        # Contribution guidelines
└── README.md              # This file
```

## 🚀 Quick Start

### Prerequisites

- **Node.js** 20+ and npm
- **Python** 3.10+
- **MongoDB** 4.4+ (or MongoDB Atlas account)
- **Docker** (optional, for containerized deployment)

### Option 1: Docker Deployment (Recommended)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/smart-attendance-system.git
   cd smart-attendance-system
   ```

2. **Configure environment**:
   ```bash
   # Update docker-compose.yml with your MongoDB credentials
   # Or use the default configuration for local testing
   ```

3. **Start all services**:
   ```bash
   docker-compose up -d
   ```

4. **Seed database** (first time only):
   ```bash
   docker-compose exec backend python seed.py
   ```

5. **Access the application**:
   - Frontend: http://localhost
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Option 2: Manual Setup

#### Backend Setup

1. **Navigate to server directory**:
   ```bash
   cd server
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**:
   ```bash
   # Create .env file with the following:
   MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/smart_attendance
   SECRET_KEY=your-super-secret-key-min-32-characters
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=1440
   CORS_ORIGINS=http://localhost:5173,http://localhost:3000
   ```

5. **Seed database**:
   ```bash
   python seed.py
   ```

6. **Run the server**:
   ```bash
   python main.py
   ```
   
   API will be available at http://localhost:8000

#### Frontend Setup

1. **Navigate to client directory**:
   ```bash
   cd client
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Configure environment**:
   ```bash
   # Create .env file with:
   VITE_API_BASE_URL=http://localhost:8000
   ```

4. **Run development server**:
   ```bash
   npm run dev
   ```
   
   App will be available at http://localhost:5173

### Default Login Credentials

After seeding the database, use these credentials:

**Admin**:
- Email: `admin@example.com`
- Password: `admin123`

**Instructor**:
- Email: `john.instructor@example.com`
- Password: `instructor123`

**Trainee**:
- Email: `alice.trainee@example.com`
- Password: `trainee123`

## 📚 Documentation

- [Deployment Guide](./docs/DEPLOYMENT.md) - Complete deployment instructions
- [API Documentation](http://localhost:8000/docs) - Interactive Swagger docs (when server is running)
- [Contributing Guidelines](./CONTRIBUTING.md) - How to contribute
- [Code of Conduct](./CODE_OF_CONDUCT.md) - Community guidelines

## 🎯 User Roles & Features

### 👨‍💼 Admin
- ✅ View system-wide analytics dashboard
- ✅ Manage users and roles
- ✅ Approve/reject missed attendance requests
- ✅ Export attendance reports (CSV/Excel)
- ✅ Monitor attendance trends with charts
- ✅ View absence reports and statistics

### 👨‍🏫 Instructor
- ✅ Create training/class sessions
- ✅ Generate time-limited QR codes (15 min expiry)
- ✅ View session-specific attendance
- ✅ Monitor trainee participation
- ✅ Deactivate sessions
- ✅ Track attendance statistics

### 👨‍🎓 Trainee
- ✅ Scan QR codes to mark attendance (camera-based)
- ✅ View personal attendance history
- ✅ Track attendance percentage
- ✅ Raise missed attendance correction requests
- ✅ View request status and admin responses
- ✅ Monitor late/present/absent records

## 🔐 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and receive JWT token
- `GET /api/auth/me` - Get current user profile

### Sessions
- `POST /api/sessions` - Create new session (Instructor)
- `GET /api/sessions` - Get all sessions
- `GET /api/sessions/:id` - Get session by ID
- `POST /api/sessions/:id/qr` - Generate QR code for session
- `PATCH /api/sessions/:id/deactivate` - Deactivate session

### Attendance
- `POST /api/attendance/scan` - Mark attendance via QR scan
- `GET /api/attendance/user/:id` - Get user attendance history
- `GET /api/attendance/user/:id/stats` - Get user attendance statistics
- `GET /api/attendance/session/:id` - Get session attendance records

### Miss Requests
- `POST /api/miss-requests` - Create miss request
- `GET /api/miss-requests` - Get all miss requests (Admin)
- `GET /api/miss-requests/user/:id/requests` - Get user's requests
- `PATCH /api/miss-requests/:id` - Update request status (Admin)

### Admin
- `GET /api/admin/stats` - Get system statistics
- `GET /api/admin/analytics/daily-attendance` - Daily attendance trends
- `GET /api/admin/analytics/absence-report` - Absence report
- `GET /api/admin/analytics/session-summary` - Session summary
- `GET /api/admin/users` - Get all users
- `PATCH /api/admin/users/:id/role` - Update user role
- `DELETE /api/admin/users/:id` - Delete user
- `GET /api/admin/export/attendance` - Export to CSV
- `GET /api/admin/export/attendance-excel` - Export to Excel

**Full API Documentation**: http://localhost:8000/docs (Interactive Swagger UI)

## 🗓️ Development Progress

- ✅ **Part 1**: Project setup, backend foundation, JWT authentication
- ✅ **Part 2**: Session management, QR code generation/scanning system
- ✅ **Part 3**: Admin analytics backend, user management APIs, CSV/Excel export
- ✅ **Part 4**: Frontend authentication, protected routes, role-based navigation
- ✅ **Part 5**: Complete dashboards for Admin/Instructor/Trainee with charts
- ✅ **Part 6**: Docker containerization, CI/CD pipeline, deployment docs

**Status**: 🎉 **PROJECT COMPLETE & PRODUCTION READY** 🎉

## 🧪 Testing

### Backend Testing
```bash
cd server

# Interactive API testing
# Visit http://localhost:8000/docs for Swagger UI

# Manual endpoint testing
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com","password":"test123","role":"trainee","organization":"Test Org"}'
```

### Frontend Testing
```bash
cd client

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

### Docker Testing
```bash
# Build and test
docker-compose up --build

# Run health checks
docker-compose ps
docker-compose logs backend
docker-compose logs frontend
```

## 🤝 Contributing

We welcome contributions! This project is **Hacktoberfest-friendly**. 🎉

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please read [CONTRIBUTING.md](./CONTRIBUTING.md) for detailed guidelines.

## 🐛 Found a Bug?

Open an issue with:
- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Screenshots (if applicable)

## 📜 License

This project is open source and available under the MIT License.

## 👥 Maintainers

We welcome contributions from everyone. Please read the [CONTRIBUTING.md](./CONTRIBUTING.md) before making a pull request.

## 🌟 Show Your Support

Give a ⭐️ if this project helped you!

## 📧 Contact

For questions or suggestions, please open an issue or reach out to the maintainers.

---

**Happy Coding! 🚀** | **Hacktoberfest 2025** 🎃