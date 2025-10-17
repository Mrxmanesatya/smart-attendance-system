import React from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const getRoleBadgeColor = (role) => {
    switch (role) {
      case 'admin':
        return 'bg-purple-100 text-purple-800';
      case 'instructor':
        return 'bg-blue-100 text-blue-800';
      case 'trainee':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getNavigationLinks = () => {
    switch (user?.role) {
      case 'admin':
        return (
          <div className="flex items-center space-x-4">
            <Link to="/admin" className="text-gray-700 hover:text-blue-600 font-medium transition-colors">
              Dashboard
            </Link>
            <Link to="/admin/users" className="text-gray-700 hover:text-blue-600 font-medium transition-colors">
              User Management
            </Link>
          </div>
        );
      case 'instructor':
        return (
          <div className="flex items-center space-x-4">
            <Link to="/instructor/sessions" className="text-gray-700 hover:text-blue-600 font-medium transition-colors">
              My Sessions
            </Link>
            <Link to="/instructor/sessions/create" className="text-gray-700 hover:text-blue-600 font-medium transition-colors">
              Create Session
            </Link>
          </div>
        );
      case 'trainee':
        return (
          <div className="flex items-center space-x-4">
            <Link to="/trainee/scan" className="text-gray-700 hover:text-blue-600 font-medium transition-colors">
              Scan QR
            </Link>
            <Link to="/trainee/attendance" className="text-gray-700 hover:text-blue-600 font-medium transition-colors">
              My Attendance
            </Link>
            <Link to="/trainee/requests" className="text-gray-700 hover:text-blue-600 font-medium transition-colors">
              Requests
            </Link>
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <nav className="bg-white shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center space-x-8">
            <Link to="/dashboard">
              <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent cursor-pointer">
                Smart Attendance
              </h1>
            </Link>
            {getNavigationLinks()}
          </div>

          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-3">
              <div className="text-right">
                <p className="text-sm font-medium text-gray-900">{user?.name}</p>
                <p className="text-xs text-gray-500">{user?.email}</p>
              </div>
              <span className={`px-3 py-1 rounded-full text-xs font-medium ${getRoleBadgeColor(user?.role)}`}>
                {user?.role?.toUpperCase()}
              </span>
            </div>

            <button
              onClick={handleLogout}
              className="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-lg hover:bg-red-700 transition-colors"
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
