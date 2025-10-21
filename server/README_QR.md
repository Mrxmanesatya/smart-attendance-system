# QR Attendance Service

A Node.js service for QR-based attendance management.

## Features

- Generate unique QR codes for training sessions
- Scan QR codes to mark attendance
- In-memory data storage (no database required)
- RESTful API endpoints
- Automatic QR code expiration (15 minutes)

## Installation

```bash
cd server
npm install
```

## Usage

```bash
npm start
# or for development
npm run dev
```

The service runs on `http://localhost:3001` by default.

## API Endpoints

### Sessions

- `POST /api/sessions` - Create a new session
- `GET /api/sessions` - Get all sessions
- `GET /api/sessions/:id` - Get session by ID
- `GET /api/sessions/:id/qr` - Generate QR code for session
- `PATCH /api/sessions/:id/deactivate` - Deactivate session

### Attendance

- `POST /api/attendance/scan` - Mark attendance by scanning QR code
- `GET /api/attendance/session/:id` - Get attendance for session
- `GET /api/attendance/user/:id` - Get attendance for user

## QR Code Format

QR codes contain: `sessionId:timestamp:randomToken`

Example: `abc123:1697123456789:xyz789`

## Expiration

QR codes expire after 15 minutes for security.

## Integration

Update your frontend API configuration:

```javascript
const QR_SERVICE_URL = 'http://localhost:3001';
// Use QR_SERVICE_URL for session and attendance endpoints
```

## Dependencies

- `express` - Web framework
- `qrcode` - QR code generation
- `cors` - Cross-origin resource sharing
- `uuid` - Unique identifier generation