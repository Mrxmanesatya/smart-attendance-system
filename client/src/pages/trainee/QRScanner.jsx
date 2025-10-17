import React, { useState, useEffect } from 'react';
import { Html5QrcodeScanner } from 'html5-qrcode';
import axios from '../../utils/axios';
import { API_ENDPOINTS } from '../../config/api';
import toast from 'react-hot-toast';

const QRScanner = () => {
  const [scanning, setScanning] = useState(false);
  const [scanner, setScanner] = useState(null);

  useEffect(() => {
    return () => {
      if (scanner) {
        scanner.clear().catch(console.error);
      }
    };
  }, [scanner]);

  const startScanning = () => {
    setScanning(true);
    
    const html5QrcodeScanner = new Html5QrcodeScanner(
      "qr-reader",
      { 
        fps: 10,
        qrbox: { width: 250, height: 250 },
        aspectRatio: 1.0
      },
      false
    );

    html5QrcodeScanner.render(onScanSuccess, onScanError);
    setScanner(html5QrcodeScanner);
  };

  const stopScanning = () => {
    if (scanner) {
      scanner.clear().then(() => {
        setScanning(false);
        setScanner(null);
      }).catch(console.error);
    }
  };

  const onScanSuccess = async (decodedText) => {
    console.log('QR Code scanned:', decodedText);
    
    // Stop scanner immediately after successful scan
    stopScanning();

    try {
      const response = await axios.post(API_ENDPOINTS.ATTENDANCE_SCAN, {
        qr_code_value: decodedText
      });

      toast.success(`Attendance marked successfully! Status: ${response.data.status}`);
    } catch (error) {
      const message = error.response?.data?.detail || 'Failed to mark attendance';
      toast.error(message);
    }
  };

  const onScanError = (error) => {
    // Ignore common scanning errors
    if (!error.includes('NotFoundException')) {
      console.warn('Scan error:', error);
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <div className="bg-white rounded-2xl shadow-md p-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">Scan QR Code</h1>
        
        <div className="mb-6">
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h3 className="font-semibold text-blue-900 mb-2">📋 Instructions:</h3>
            <ol className="list-decimal list-inside space-y-1 text-sm text-blue-800">
              <li>Click "Start Scanning" button below</li>
              <li>Allow camera access when prompted</li>
              <li>Point your camera at the QR code displayed by your instructor</li>
              <li>Hold steady until the code is scanned automatically</li>
              <li>Your attendance will be marked instantly</li>
            </ol>
          </div>
        </div>

        {!scanning ? (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">📷</div>
            <p className="text-gray-600 mb-6">Ready to mark your attendance?</p>
            <button
              onClick={startScanning}
              className="px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-medium rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all text-lg"
            >
              Start Scanning
            </button>
          </div>
        ) : (
          <div className="space-y-4">
            <div id="qr-reader" className="border-4 border-blue-500 rounded-lg overflow-hidden"></div>
            <button
              onClick={stopScanning}
              className="w-full py-3 bg-red-600 text-white font-medium rounded-lg hover:bg-red-700 transition-colors"
            >
              Stop Scanning
            </button>
          </div>
        )}

        <div className="mt-8 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
          <p className="text-sm text-yellow-800">
            <strong>⚠️ Note:</strong> QR codes expire after 15 minutes for security. 
            If the code doesn't work, ask your instructor to regenerate it.
          </p>
        </div>
      </div>
    </div>
  );
};

export default QRScanner;
