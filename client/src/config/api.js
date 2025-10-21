// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
const WS_BASE_URL = (import.meta.env.VITE_WS_BASE_URL) || API_BASE_URL.replace('http', 'ws');

export const API_ENDPOINTS = {
  // Auth
  REGISTER: `${API_BASE_URL}/api/auth/register`,
  LOGIN: `${API_BASE_URL}/api/auth/login`,
  ME: `${API_BASE_URL}/api/auth/me`,
  
  // Sessions
  SESSIONS: `${API_BASE_URL}/api/sessions`,
  SESSION_BY_ID: (id) => `${API_BASE_URL}/api/sessions/${id}`,
  SESSION_QR: (id) => `${API_BASE_URL}/api/sessions/${id}/qr`,
  SESSION_DEACTIVATE: (id) => `${API_BASE_URL}/api/sessions/${id}/deactivate`,
  
  // Attendance
  ATTENDANCE_SCAN: `${API_BASE_URL}/api/attendance/scan`,
  ATTENDANCE_USER: (id) => `${API_BASE_URL}/api/attendance/user/${id}`,
  ATTENDANCE_USER_STATS: (id) => `${API_BASE_URL}/api/attendance/user/${id}/stats`,
  ATTENDANCE_SESSION: (id) => `${API_BASE_URL}/api/attendance/session/${id}`,
  // Realtime
  REALTIME_SESSION_LIVE: (id) => `${API_BASE_URL}/api/realtime/session/${id}/live`,
  REALTIME_WS: (sessionId) => `${WS_BASE_URL}/api/realtime/ws?session_id=${sessionId}`,
  
  // Miss Requests
  MISS_REQUESTS: `${API_BASE_URL}/api/miss-requests`,
  MISS_REQUEST_BY_ID: (id) => `${API_BASE_URL}/api/miss-requests/${id}`,
  MISS_REQUEST_USER: (id) => `${API_BASE_URL}/api/miss-requests/user/${id}/requests`,
  
  // Admin
  ADMIN_STATS: `${API_BASE_URL}/api/admin/stats`,
  ADMIN_DAILY_ATTENDANCE: `${API_BASE_URL}/api/admin/analytics/daily-attendance`,
  ADMIN_ABSENCE_REPORT: `${API_BASE_URL}/api/admin/analytics/absence-report`,
  ADMIN_SESSION_SUMMARY: `${API_BASE_URL}/api/admin/analytics/session-summary`,
  ADMIN_USERS: `${API_BASE_URL}/api/admin/users`,
  ADMIN_USER_ROLE: (id) => `${API_BASE_URL}/api/admin/users/${id}/role`,
  ADMIN_USER_DELETE: (id) => `${API_BASE_URL}/api/admin/users/${id}`,
  ADMIN_EXPORT_CSV: `${API_BASE_URL}/api/admin/export/attendance`,
  ADMIN_EXPORT_EXCEL: `${API_BASE_URL}/api/admin/export/attendance-excel`,
};

export default API_BASE_URL;
