import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Dashboard = () => {
  const { user } = useAuth();
  const navigate = useNavigate();

  const getDashboardContent = () => {
    switch (user?.role) {
      case 'admin':
        return {
          title: 'Admin Dashboard',
          description: 'Manage system, users, and view analytics',
          cards: [
            { title: 'System Stats', icon: '📊', link: '/admin/stats', color: 'blue' },
            { title: 'User Management', icon: '👥', link: '/admin/users', color: 'purple' },
            { title: 'Sessions', icon: '📅', link: '/admin/sessions', color: 'green' },
            { title: 'Miss Requests', icon: '📝', link: '/admin/requests', color: 'yellow' },
            { title: 'Analytics', icon: '📈', link: '/admin/analytics', color: 'red' },
            { title: 'Export Data', icon: '💾', link: '/admin/export', color: 'indigo' },
          ],
        };
      case 'instructor':
        return {
          title: 'Instructor Dashboard',
          description: 'Manage sessions and track attendance',
          cards: [
            { title: 'Create Session', icon: '➕', link: '/instructor/create-session', color: 'blue' },
            { title: 'My Sessions', icon: '📅', link: '/instructor/sessions', color: 'green' },
            { title: 'Attendance Reports', icon: '📊', link: '/instructor/reports', color: 'purple' },
          ],
        };
      case 'trainee':
        return {
          title: 'Trainee Dashboard',
          description: 'Mark attendance and track your progress',
          cards: [
            { title: 'Scan QR Code', icon: '📷', link: '/trainee/scan', color: 'blue' },
            { title: 'My Attendance', icon: '✅', link: '/trainee/attendance', color: 'green' },
            { title: 'Request Correction', icon: '📝', link: '/trainee/requests', color: 'yellow' },
          ],
        };
      default:
        return {
          title: 'Dashboard',
          description: 'Welcome to Smart Attendance System',
          cards: [],
        };
    }
  };

  const content = getDashboardContent();

  const getColorClasses = (color) => {
    const colors = {
      blue: 'from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700',
      purple: 'from-purple-500 to-purple-600 hover:from-purple-600 hover:to-purple-700',
      green: 'from-green-500 to-green-600 hover:from-green-600 hover:to-green-700',
      yellow: 'from-yellow-500 to-yellow-600 hover:from-yellow-600 hover:to-yellow-700',
      red: 'from-red-500 to-red-600 hover:from-red-600 hover:to-red-700',
      indigo: 'from-indigo-500 to-indigo-600 hover:from-indigo-600 hover:to-indigo-700',
    };
    return colors[color] || colors.blue;
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="bg-white rounded-2xl shadow-md p-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">{content.title}</h1>
        <p className="text-gray-600">{content.description}</p>
      </div>

      {/* Quick Stats */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl shadow-lg p-8 text-white">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center">
            <p className="text-white/80 text-sm mb-1">Organization</p>
            <p className="text-2xl font-bold">{user?.org_name}</p>
          </div>
          <div className="text-center">
            <p className="text-white/80 text-sm mb-1">Role</p>
            <p className="text-2xl font-bold capitalize">{user?.role}</p>
          </div>
          <div className="text-center">
            <p className="text-white/80 text-sm mb-1">Status</p>
            <p className="text-2xl font-bold">Active</p>
          </div>
        </div>
      </div>

      {/* Dashboard Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {content.cards.map((card, index) => (
          <button
            key={index}
            onClick={() => navigate(card.link)}
            className={`bg-gradient-to-br ${getColorClasses(card.color)} text-white rounded-2xl shadow-lg p-8 transition-all transform hover:scale-105`}
          >
            <div className="text-5xl mb-4">{card.icon}</div>
            <h3 className="text-xl font-bold">{card.title}</h3>
          </button>
        ))}
      </div>

      {/* Coming Soon Notice */}
      <div className="bg-yellow-50 border border-yellow-200 rounded-2xl p-6">
        <h3 className="text-lg font-semibold text-yellow-800 mb-2">🚧 Development in Progress</h3>
        <p className="text-yellow-700">
          Dashboard features are being implemented. Check back soon for full functionality!
        </p>
      </div>
    </div>
  );
};

export default Dashboard;
