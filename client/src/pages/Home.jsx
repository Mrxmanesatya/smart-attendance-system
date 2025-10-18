import React, { useState, useEffect } from "react";
import HomeSkeleton from "./HomeSkeleton";

const Home = () => {
  const [loading, setLoading] = useState(true);

  // Simulate data loading
  useEffect(() => {
    const timer = setTimeout(() => setLoading(false), 1500);
    return () => clearTimeout(timer);
  }, []);

  if (loading) return <HomeSkeleton />;

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center px-6 py-10">
      <h1 className="text-4xl font-bold text-gray-800 mb-6 text-center">
        Smart Attendance System
      </h1>
      <p className="text-gray-600 mb-8 text-center max-w-xl">
        Mark your attendance easily using{" "}
        <span className="font-semibold">Face Recognition</span> or{" "}
        <span className="font-semibold">QR Code</span>.
        <br />
        Teachers can view and manage attendance records seamlessly.
      </p>

      <div className="flex flex-wrap justify-center gap-6">
        {/* Face Attendance Card */}
        <div className="bg-white shadow-md rounded-2xl p-6 w-72 hover:shadow-lg transition">
          <img
            src="/face-scan.png"
            alt="Face Attendance"
            className="w-20 mx-auto mb-4"
          />
          <h2 className="text-xl font-semibold text-center mb-2">
            Mark Attendance via Face
          </h2>
          <p className="text-gray-500 text-center mb-4">
            Scan your face to verify your attendance.
          </p>
          <button className="bg-blue-600 text-white w-full py-2 rounded-lg hover:bg-blue-700">
            Start Face Scan
          </button>
        </div>

        {/* QR Attendance Card */}
        <div className="bg-white shadow-md rounded-2xl p-6 w-72 hover:shadow-lg transition">
          <img
            src="/qr-scan.png"
            alt="QR Attendance"
            className="w-20 mx-auto mb-4"
          />
          <h2 className="text-xl font-semibold text-center mb-2">
            Mark Attendance via QR
          </h2>
          <p className="text-gray-500 text-center mb-4">
            Scan the QR code provided by your teacher.
          </p>
          <button className="bg-green-600 text-white w-full py-2 rounded-lg hover:bg-green-700">
            Scan QR Code
          </button>
        </div>
      </div>
    </div>
  );
};

export default Home;
