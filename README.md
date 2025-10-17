# Smart Attendance System 📱✅

A comprehensive QR code-based Smart Attendance System with role-based access control, built for corporate offices, colleges, gyms, and training institutes.

## 🌟 Features

- **QR-Based Attendance**: Dynamic QR code generation with time expiry for secure attendance marking
- **Role-Based Access Control**: Three distinct roles - Admin, Instructor, and Trainee
- **JWT Authentication**: Secure token-based authentication with bcrypt password hashing
- **Interactive Dashboards**: Role-specific dashboards with analytics and charts
- **Attendance Analytics**: Track attendance trends, generate reports, and export data
- **Miss Request System**: Trainees can raise missed attendance correction requests
- **Responsive Design**: Clean, modern UI built with React and Tailwind CSS
- **Scalable Architecture**: FastAPI backend with MongoDB for efficient data handling

## 🏗️ Tech Stack

### Frontend
- **Framework**: React 19 with Vite
- **Styling**: Tailwind CSS 4
- **Charts**: Recharts (to be added)
- **QR Scanner**: HTML5 QR Code (to be added)
- **HTTP Client**: Axios (to be added)
- **Routing**: React Router (to be added)
- **State Management**: React Context API

### Backend
- **Framework**: FastAPI (Python)
- **Database**: MongoDB with Motor (async driver)
- **Authentication**: JWT with python-jose
- **Password Hashing**: Bcrypt via passlib
- **QR Generation**: qrcode library with PIL
- **Data Export**: pandas + openpyxl for Excel export

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

- **Node.js** 18+ and npm
- **Python** 3.9+
- **MongoDB** 4.4+

### Backend Setup

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
   cp .env.example .env
   # Edit .env with your MongoDB URL and secret key
   ```

5. **Run the server**:
   ```bash
   python main.py
   ```
   
   API will be available at http://localhost:8000
   
   Interactive docs: http://localhost:8000/docs

### Frontend Setup

1. **Navigate to client directory**:
   ```bash
   cd client
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Run development server**:
   ```bash
   npm run dev
   ```
   
   App will be available at http://localhost:5173

## 📚 Documentation

- [Backend API Documentation](./server/README.md)
- [Frontend Documentation](./client/README.md)
- [Contributing Guidelines](./CONTRIBUTING.md)
- [Code of Conduct](./CODE_OF_CONDUCT.md)

## 🎯 User Roles

### Admin
- Manage users and roles
- View system-wide analytics
- Approve/reject missed attendance requests
- Export attendance reports (CSV/Excel)
- Create and manage sessions

### Instructor
- Create training/class sessions
- Generate QR codes for attendance
- View session-specific attendance
- Monitor trainee participation

### Trainee
- Scan QR codes to mark attendance
- View personal attendance history
- Raise missed attendance requests
- Track attendance percentage

## 🔐 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and receive JWT token
- `GET /api/auth/me` - Get current user profile

### Sessions (Part 2)
- `POST /api/sessions/` - Create new session
- `GET /api/sessions/:id/qr` - Get QR code for session

### Attendance (Part 2)
- `POST /api/attendance/scan` - Mark attendance via QR scan
- `GET /api/attendance/user/:id` - Get user attendance history

### Admin (Part 3)
- `GET /api/admin/stats` - Get system statistics
- `GET /api/miss-requests` - View all miss requests
- `PATCH /api/miss-requests/:id` - Approve/reject request

## 🗓️ Development Roadmap

- ✅ **Part 1**: Project setup, backend foundation, authentication
- ⏳ **Part 2**: Session management, QR code system
- ⏳ **Part 3**: Admin dashboard, analytics backend
- ⏳ **Part 4**: Frontend auth, core UI setup
- ⏳ **Part 5**: Frontend dashboards, QR features
- ⏳ **Part 6**: Docker, CI/CD, deployment

## 🧪 Testing

### Backend Testing
```bash
cd server
# Interactive API testing at http://localhost:8000/docs
```

### Frontend Testing
```bash
cd client
npm run test  # (To be added)
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