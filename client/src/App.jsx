import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import Layout from './components/Layout';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';

// Admin Pages
import AdminDashboard from './pages/admin/AdminDashboard';
import UserManagement from './pages/admin/UserManagement';

// Instructor Pages
import CreateSession from './pages/instructor/CreateSession';
import SessionList from './pages/instructor/SessionList';
import SessionDetail from './pages/instructor/SessionDetail';

// Trainee Pages
import QRScanner from './pages/trainee/QRScanner';
import MyAttendance from './pages/trainee/MyAttendance';
import MissRequests from './pages/trainee/MissRequests';

function App() {
  return (
    <Router>
      <AuthProvider>
        <Toaster position="top-right" />
        <Routes>
          {/* Public Routes */}
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          {/* Protected Routes */}
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <Layout />
              </ProtectedRoute>
            }
          >
            <Route index element={<Navigate to="/dashboard" replace />} />
            <Route path="dashboard" element={<Dashboard />} />
            
            {/* Admin Routes */}
            <Route path="admin">
              <Route index element={<AdminDashboard />} />
              <Route path="users" element={<UserManagement />} />
            </Route>

            {/* Instructor Routes */}
            <Route path="instructor">
              <Route index element={<SessionList />} />
              <Route path="sessions" element={<SessionList />} />
              <Route path="sessions/create" element={<CreateSession />} />
              <Route path="sessions/:id" element={<SessionDetail />} />
            </Route>

            {/* Trainee Routes */}
            <Route path="trainee">
              <Route index element={<QRScanner />} />
              <Route path="scan" element={<QRScanner />} />
              <Route path="attendance" element={<MyAttendance />} />
              <Route path="requests" element={<MissRequests />} />
            </Route>
          </Route>

          {/* Fallback */}
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </AuthProvider>
    </Router>
  );
}

export default App;
