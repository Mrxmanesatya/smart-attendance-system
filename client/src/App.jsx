import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import Layout from './components/Layout';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';

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
            
            {/* Placeholder routes for Part 5 */}
            <Route path="admin/*" element={<div className="text-center py-12"><h2 className="text-2xl font-bold">Admin Section - Coming in Part 5</h2></div>} />
            <Route path="instructor/*" element={<div className="text-center py-12"><h2 className="text-2xl font-bold">Instructor Section - Coming in Part 5</h2></div>} />
            <Route path="trainee/*" element={<div className="text-center py-12"><h2 className="text-2xl font-bold">Trainee Section - Coming in Part 5</h2></div>} />
          </Route>

          {/* Fallback */}
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </AuthProvider>
    </Router>
  );
}

export default App;
