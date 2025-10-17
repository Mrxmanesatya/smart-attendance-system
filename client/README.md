# Smart Attendance System - Frontend

React-based frontend for the Smart Attendance System with Tailwind CSS, role-based authentication, and responsive design.

## 🚀 Features

- **Modern UI**: Built with React 19 and Tailwind CSS 4
- **Authentication**: JWT-based auth with protected routes
- **Role-Based Access**: Different dashboards for Admin, Instructor, and Trainee
- **Responsive Design**: Mobile-friendly interface
- **Toast Notifications**: User feedback with react-hot-toast

## 📋 Prerequisites

- Node.js 18+ and npm
- Backend server running on http://localhost:8000

## 🛠️ Installation

```bash
cd client
npm install
cp .env.example .env
npm run dev
```

App will be available at http://localhost:5173

## 🎯 Role-Based Features

**Admin**: System stats, user management, analytics, export data
**Instructor**: Create sessions, generate QR codes, view attendance reports
**Trainee**: Scan QR codes, view attendance history, request corrections

## 📝 Development Progress

- ✅ Part 1-3: Backend complete
- ✅ Part 4: Frontend auth & core UI (Current)
- ⏳ Part 5: Frontend dashboards & QR features
- ⏳ Part 6: Docker & deployment
