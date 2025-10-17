import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from '../../utils/axios';
import { API_ENDPOINTS } from '../../config/api';
import toast from 'react-hot-toast';

const SessionDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [session, setSession] = useState(null);
  const [qrCode, setQrCode] = useState(null);
  const [attendance, setAttendance] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSessionData();
  }, [id]);

  const fetchSessionData = async () => {
    setLoading(true);
    try {
      const [sessionRes, attendanceRes] = await Promise.all([
        axios.get(API_ENDPOINTS.SESSION_BY_ID(id)),
        axios.get(API_ENDPOINTS.ATTENDANCE_SESSION(id)),
      ]);

      setSession(sessionRes.data);
      setAttendance(attendanceRes.data);
    } catch (error) {
      toast.error('Failed to fetch session data');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const generateQRCode = async () => {
    try {
      const response = await axios.get(API_ENDPOINTS.SESSION_QR(id));
      setQrCode(response.data);
      toast.success('QR Code generated successfully!');
    } catch (error) {
      toast.error('Failed to generate QR code');
    }
  };

  const deactivateSession = async () => {
    if (!window.confirm('Are you sure you want to deactivate this session?')) return;

    try {
      await axios.patch(API_ENDPOINTS.SESSION_DEACTIVATE(id));
      toast.success('Session deactivated');
      navigate('/instructor/sessions');
    } catch (error) {
      toast.error('Failed to deactivate session');
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-2xl shadow-md p-6">
        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">{session?.title}</h1>
            <p className="text-gray-600 mt-2">{session?.description || 'No description'}</p>
            <div className="flex gap-4 mt-4 text-sm text-gray-500">
              <span>📅 {new Date(session?.start_time).toLocaleString()}</span>
              <span>⏰ {new Date(session?.end_time).toLocaleString()}</span>
            </div>
          </div>
          <button
            onClick={deactivateSession}
            className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
          >
            Deactivate
          </button>
        </div>
      </div>

      {/* QR Code Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-2xl shadow-md p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">QR Code</h2>
          {!qrCode ? (
            <div className="text-center py-12">
              <p className="text-gray-600 mb-4">Generate a QR code for this session</p>
              <button
                onClick={generateQRCode}
                className="px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-medium rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all"
              >
                Generate QR Code
              </button>
            </div>
          ) : (
            <div className="text-center">
              <img
                src={`data:image/png;base64,${qrCode.qr_image_base64}`}
                alt="Session QR Code"
                className="mx-auto border-4 border-gray-200 rounded-lg shadow-lg"
              />
              <p className="text-sm text-gray-600 mt-4">
                Expires: {new Date(qrCode.expires_at).toLocaleString()}
              </p>
              <button
                onClick={() => generateQRCode()}
                className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                Regenerate QR Code
              </button>
            </div>
          )}
        </div>

        {/* Attendance Stats */}
        <div className="bg-white rounded-2xl shadow-md p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Attendance Overview</h2>
          <div className="space-y-4">
            <div className="bg-green-50 rounded-lg p-4">
              <p className="text-sm text-green-700">Present</p>
              <p className="text-3xl font-bold text-green-900">
                {attendance.filter(a => a.status === 'present').length}
              </p>
            </div>
            <div className="bg-yellow-50 rounded-lg p-4">
              <p className="text-sm text-yellow-700">Late</p>
              <p className="text-3xl font-bold text-yellow-900">
                {attendance.filter(a => a.status === 'late').length}
              </p>
            </div>
            <div className="bg-blue-50 rounded-lg p-4">
              <p className="text-sm text-blue-700">Total Marked</p>
              <p className="text-3xl font-bold text-blue-900">{attendance.length}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Attendance List */}
      <div className="bg-white rounded-2xl shadow-md p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Attendance List</h2>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Student</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Method</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Time</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {attendance.map((record, index) => (
                <tr key={index}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {record.user_name}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {record.user_email}
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
          <p className="text-center text-gray-500 py-8">No attendance marked yet</p>
        )}
      </div>
    </div>
  );
};

export default SessionDetail;
