import React, { useState, useEffect } from 'react';
import axios from '../../utils/axios';
import { API_ENDPOINTS } from '../../config/api';
import toast from 'react-hot-toast';
import { useAuth } from '../../context/AuthContext';

const MissRequests = () => {
  const { user } = useAuth();
  const [requests, setRequests] = useState([]);
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    session_id: '',
    reason: '',
  });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [requestsRes, sessionsRes] = await Promise.all([
        axios.get(API_ENDPOINTS.MISS_REQUESTS),
        axios.get(API_ENDPOINTS.SESSIONS),
      ]);

      setRequests(requestsRes.data);
      setSessions(sessionsRes.data);
    } catch (error) {
      toast.error('Failed to fetch data');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (formData.reason.length < 10) {
      toast.error('Reason must be at least 10 characters');
      return;
    }

    try {
      await axios.post(API_ENDPOINTS.MISS_REQUESTS, formData);
      toast.success('Request submitted successfully!');
      setShowForm(false);
      setFormData({ session_id: '', reason: '' });
      fetchData();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to submit request');
    }
  };

  const getStatusBadge = (status) => {
    const badges = {
      pending: 'bg-yellow-100 text-yellow-800',
      approved: 'bg-green-100 text-green-800',
      rejected: 'bg-red-100 text-red-800',
    };
    return badges[status] || 'bg-gray-100 text-gray-800';
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
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Attendance Requests</h1>
          <p className="text-gray-600 mt-1">Request corrections for missed sessions</p>
        </div>
        <button
          onClick={() => setShowForm(!showForm)}
          className="px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-medium rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all"
        >
          {showForm ? 'Cancel' : '➕ New Request'}
        </button>
      </div>

      {/* Request Form */}
      {showForm && (
        <div className="bg-white rounded-2xl shadow-md p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Submit Missed Attendance Request</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="session_id" className="block text-sm font-medium text-gray-700 mb-2">
                Select Session *
              </label>
              <select
                id="session_id"
                name="session_id"
                required
                value={formData.session_id}
                onChange={(e) => setFormData({ ...formData, session_id: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">Choose a session</option>
                {sessions.map((session) => (
                  <option key={session._id} value={session._id}>
                    {session.title} - {new Date(session.start_time).toLocaleDateString()}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label htmlFor="reason" className="block text-sm font-medium text-gray-700 mb-2">
                Reason (minimum 10 characters) *
              </label>
              <textarea
                id="reason"
                name="reason"
                required
                rows={4}
                value={formData.reason}
                onChange={(e) => setFormData({ ...formData, reason: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Explain why you missed the session..."
              />
            </div>

            <button
              type="submit"
              className="w-full py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors"
            >
              Submit Request
            </button>
          </form>
        </div>
      )}

      {/* Requests List */}
      <div className="bg-white rounded-2xl shadow-md p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-4">My Requests</h2>
        <div className="space-y-4">
          {requests.length === 0 ? (
            <p className="text-center text-gray-500 py-8">No requests yet</p>
          ) : (
            requests.map((request) => (
              <div key={request._id} className="border border-gray-200 rounded-lg p-4">
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <p className="font-semibold text-gray-900">Session: {request.session_id.slice(-6)}</p>
                    <p className="text-sm text-gray-600 mt-1">{request.reason}</p>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-xs font-semibold ${getStatusBadge(request.status)}`}>
                    {request.status.toUpperCase()}
                  </span>
                </div>

                {request.admin_response && (
                  <div className="mt-3 p-3 bg-gray-50 rounded-lg">
                    <p className="text-sm font-medium text-gray-700">Admin Response:</p>
                    <p className="text-sm text-gray-600 mt-1">{request.admin_response}</p>
                  </div>
                )}

                <p className="text-xs text-gray-500 mt-2">
                  Submitted: {new Date(request.created_at).toLocaleString()}
                </p>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default MissRequests;
