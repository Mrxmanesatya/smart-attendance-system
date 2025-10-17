import React, { useState, useEffect } from 'react';
import axios from '../../utils/axios';
import { API_ENDPOINTS } from '../../config/api';
import toast from 'react-hot-toast';
import { useAuth } from '../../context/AuthContext';

const MyAttendance = () => {
  const { user } = useAuth();
  const [attendance, setAttendance] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (user?._id) {
      fetchAttendanceData();
    }
  }, [user]);

  const fetchAttendanceData = async () => {
    setLoading(true);
    try {
      const [attendanceRes, statsRes] = await Promise.all([
        axios.get(API_ENDPOINTS.ATTENDANCE_USER(user._id)),
        axios.get(API_ENDPOINTS.ATTENDANCE_USER_STATS(user._id)),
      ]);

      setAttendance(attendanceRes.data);
      setStats(statsRes.data);
    } catch (error) {
      toast.error('Failed to fetch attendance data');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  const getAttendancePercentageColor = (percentage) => {
    if (percentage >= 75) return 'text-green-600';
    if (percentage >= 50) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">My Attendance</h1>
        <p className="text-gray-600 mt-1">Track your attendance records</p>
      </div>

      {/* Stats Cards */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-2xl p-6 text-white shadow-lg">
            <p className="text-blue-100 text-sm">Total Sessions</p>
            <p className="text-3xl font-bold mt-1">{stats.total_sessions}</p>
          </div>

          <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-2xl p-6 text-white shadow-lg">
            <p className="text-green-100 text-sm">Attended</p>
            <p className="text-3xl font-bold mt-1">{stats.attended}</p>
          </div>

          <div className="bg-gradient-to-br from-red-500 to-red-600 rounded-2xl p-6 text-white shadow-lg">
            <p className="text-red-100 text-sm">Missed</p>
            <p className="text-3xl font-bold mt-1">{stats.missed}</p>
          </div>

          <div className="bg-gradient-to-br from-yellow-500 to-yellow-600 rounded-2xl p-6 text-white shadow-lg">
            <p className="text-yellow-100 text-sm">Late</p>
            <p className="text-3xl font-bold mt-1">{stats.late}</p>
          </div>
        </div>
      )}

      {/* Attendance Percentage */}
      {stats && (
        <div className="bg-white rounded-2xl shadow-md p-8 text-center">
          <h2 className="text-lg font-semibold text-gray-700 mb-2">Overall Attendance Rate</h2>
          <div className={`text-6xl font-bold ${getAttendancePercentageColor(stats.attendance_percentage)}`}>
            {stats.attendance_percentage}%
          </div>
          <div className="mt-4 w-full bg-gray-200 rounded-full h-4">
            <div
              className={`h-4 rounded-full transition-all ${
                stats.attendance_percentage >= 75 ? 'bg-green-600' :
                stats.attendance_percentage >= 50 ? 'bg-yellow-600' :
                'bg-red-600'
              }`}
              style={{ width: `${stats.attendance_percentage}%` }}
            ></div>
          </div>
        </div>
      )}

      {/* Attendance History */}
      <div className="bg-white rounded-2xl shadow-md p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Attendance History</h2>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Session</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Method</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Time</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {attendance.map((record, index) => (
                <tr key={index}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    Session {record.session_id.slice(-6)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 py-1 text-xs font-semibold rounded-full ${
                      record.status === 'present' ? 'bg-green-100 text-green-800' :
                      record.status === 'late' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-red-100 text-red-800'
                    }`}>
                      {record.status.toUpperCase()}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 capitalize">
                    {record.method.replace('_', ' ')}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {new Date(record.timestamp).toLocaleString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        {attendance.length === 0 && (
          <p className="text-center text-gray-500 py-8">No attendance records yet. Start scanning QR codes!</p>
        )}
      </div>
    </div>
  );
};

export default MyAttendance;
