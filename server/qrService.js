const express = require('express');
const qrcode = require('qrcode');
const cors = require('cors');
const { v4: uuidv4 } = require('uuid');

const app = express();
const PORT = process.env.QR_SERVICE_PORT || 3001;

// Middleware
app.use(cors());
app.use(express.json());

// In-memory storage (since no MongoDB)
let sessions = [];
let qrCodes = [];
let attendanceRecords = [];

// Helper functions
function generateQRValue(sessionId) {
  const timestamp = Date.now();
  const randomToken = uuidv4();
  return `${sessionId}:${timestamp}:${randomToken}`;
}

function isQRExpired(expiresAt) {
  return new Date() > new Date(expiresAt);
}

// Routes

// Create a new session
app.post('/api/sessions', (req, res) => {
  try {
    const { title, description, startTime, endTime, instructorId } = req.body;

    if (!title || !startTime || !endTime) {
      return res.status(400).json({ error: 'Title, startTime, and endTime are required' });
    }

    const session = {
      id: uuidv4(),
      title,
      description: description || '',
      startTime,
      endTime,
      instructorId: instructorId || 'instructor-1',
      active: true,
      createdAt: new Date().toISOString(),
      qrCodeId: null
    };

    sessions.push(session);
    res.status(201).json(session);
  } catch (error) {
    res.status(500).json({ error: 'Failed to create session' });
  }
});

// Get all sessions
app.get('/api/sessions', (req, res) => {
  const activeOnly = req.query.activeOnly !== 'false';
  let filteredSessions = sessions;

  if (activeOnly) {
    filteredSessions = sessions.filter(s => s.active);
  }

  res.json(filteredSessions);
});

// Get session by ID
app.get('/api/sessions/:sessionId', (req, res) => {
  const session = sessions.find(s => s.id === req.params.sessionId);

  if (!session) {
    return res.status(404).json({ error: 'Session not found' });
  }

  res.json(session);
});

// Generate QR code for session
app.get('/api/sessions/:sessionId/qr', async (req, res) => {
  try {
    const session = sessions.find(s => s.id === req.params.sessionId);

    if (!session) {
      return res.status(404).json({ error: 'Session not found' });
    }

    if (!session.active) {
      return res.status(400).json({ error: 'Session is not active' });
    }

    const regenerate = req.query.regenerate === 'true';
    let existingQR = null;

    if (!regenerate && session.qrCodeId) {
      existingQR = qrCodes.find(qr => qr.id === session.qrCodeId);
      if (existingQR && !isQRExpired(existingQR.expiresAt)) {
        // Return existing valid QR code
        const qrImageBase64 = await qrcode.toDataURL(existingQR.codeValue);
        return res.json({
          qrImageBase64,
          codeValue: existingQR.codeValue,
          expiresAt: existingQR.expiresAt,
          sessionId: session.id,
          sessionTitle: session.title
        });
      }
    }

    // Generate new QR code
    const qrValue = generateQRValue(session.id);
    const expiresAt = new Date(Date.now() + 15 * 60 * 1000).toISOString(); // 15 minutes

    const qrCode = {
      id: uuidv4(),
      sessionId: session.id,
      codeValue: qrValue,
      expiresAt,
      createdAt: new Date().toISOString()
    };

    qrCodes.push(qrCode);

    // Update session with QR code ID
    session.qrCodeId = qrCode.id;

    // Generate QR code image
    const qrImageBase64 = await qrcode.toDataURL(qrValue);

    res.json({
      qrImageBase64,
      codeValue: qrValue,
      expiresAt,
      sessionId: session.id,
      sessionTitle: session.title
    });

  } catch (error) {
    console.error('QR generation error:', error);
    res.status(500).json({ error: 'Failed to generate QR code' });
  }
});

// Mark attendance by scanning QR code
app.post('/api/attendance/scan', (req, res) => {
  try {
    const { qrCodeValue, userId } = req.body;

    if (!qrCodeValue || !userId) {
      return res.status(400).json({ error: 'QR code value and user ID are required' });
    }

    // Find QR code
    const qrCode = qrCodes.find(qr => qr.codeValue === qrCodeValue);

    if (!qrCode) {
      return res.status(404).json({ error: 'Invalid QR code' });
    }

    // Check if QR code has expired
    if (isQRExpired(qrCode.expiresAt)) {
      return res.status(400).json({ error: 'QR code has expired' });
    }

    // Find session
    const session = sessions.find(s => s.id === qrCode.sessionId);

    if (!session || !session.active) {
      return res.status(404).json({ error: 'Session not found or inactive' });
    }

    // Check if attendance already marked
    const existingAttendance = attendanceRecords.find(
      a => a.sessionId === session.id && a.userId === userId
    );

    if (existingAttendance) {
      return res.status(400).json({ error: 'Attendance already marked for this session' });
    }

    // Determine attendance status
    const currentTime = new Date();
    const sessionStart = new Date(session.startTime);
    const status = currentTime > sessionStart ? 'late' : 'present';

    // Create attendance record
    const attendance = {
      id: uuidv4(),
      sessionId: session.id,
      userId,
      status,
      method: 'qr_code',
      timestamp: new Date().toISOString()
    };

    attendanceRecords.push(attendance);

    res.status(201).json(attendance);

  } catch (error) {
    console.error('Attendance scanning error:', error);
    res.status(500).json({ error: 'Failed to mark attendance' });
  }
});

// Get attendance for a session
app.get('/api/attendance/session/:sessionId', (req, res) => {
  const sessionAttendance = attendanceRecords.filter(a => a.sessionId === req.params.sessionId);

  // Mock user data (in real app, this would come from user service)
  const attendanceWithUsers = sessionAttendance.map(record => ({
    attendanceId: record.id,
    userId: record.userId,
    userName: `User ${record.userId}`,
    userEmail: `user${record.userId}@example.com`,
    status: record.status,
    method: record.method,
    timestamp: record.timestamp
  }));

  res.json(attendanceWithUsers);
});

// Get attendance for a user
app.get('/api/attendance/user/:userId', (req, res) => {
  const userAttendance = attendanceRecords.filter(a => a.userId === req.params.userId);
  res.json(userAttendance);
});

// Deactivate session
app.patch('/api/sessions/:sessionId/deactivate', (req, res) => {
  const session = sessions.find(s => s.id === req.params.sessionId);

  if (!session) {
    return res.status(404).json({ error: 'Session not found' });
  }

  session.active = false;
  res.json({ message: 'Session deactivated successfully', sessionId: session.id });
});

// Health check
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'QR Attendance Service',
    timestamp: new Date().toISOString()
  });
});

// Root endpoint
app.get('/', (req, res) => {
  res.json({
    message: 'QR-based Attendance Service',
    version: '1.0.0',
    endpoints: {
      'POST /api/sessions': 'Create new session',
      'GET /api/sessions': 'Get all sessions',
      'GET /api/sessions/:id': 'Get session by ID',
      'GET /api/sessions/:id/qr': 'Generate/get QR code for session',
      'POST /api/attendance/scan': 'Mark attendance by scanning QR',
      'GET /api/attendance/session/:id': 'Get attendance for session',
      'GET /api/attendance/user/:id': 'Get attendance for user',
      'PATCH /api/sessions/:id/deactivate': 'Deactivate session'
    }
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`🚀 QR Attendance Service running on port ${PORT}`);
  console.log(`📊 Sessions: ${sessions.length}`);
  console.log(`🔗 QR Codes: ${qrCodes.length}`);
  console.log(`📝 Attendance Records: ${attendanceRecords.length}`);
});

module.exports = app;