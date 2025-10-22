import React, { useEffect, useMemo, useRef, useState } from "react";
import axios from "../../utils/axios";
import { API_ENDPOINTS } from "../../config/api";
import { useParams } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

const LiveAttendance = () => {
  const { id: routeSessionId } = useParams();
  const { user } = useAuth();
  const [sessionId, setSessionId] = useState(routeSessionId || "");
  const [stats, setStats] = useState({ total_students: 0, present: 0, absent: 0, late: 0, percentage: 0 });
  const [sessionInfo, setSessionInfo] = useState({ id: "", title: "", active: false });
  const [recent, setRecent] = useState([]);
  const wsRef = useRef(null);
  const [connected, setConnected] = useState(false);

  const connectWebSocket = (sid) => {
    if (!sid) return;
    const url = API_ENDPOINTS.REALTIME_WS(sid);
    const ws = new WebSocket(url);
    wsRef.current = ws;
    ws.onopen = () => setConnected(true);
    ws.onclose = () => setConnected(false);
    ws.onerror = () => setConnected(false);
    ws.onmessage = (evt) => {
      try {
        const msg = JSON.parse(evt.data);
        if (msg.event === "attendance_scanned") {
          // Optimistically refetch stats for accuracy
          fetchLive(sid);
        }
      } catch (_) {}
    };
  };

  const fetchLive = async (sid) => {
    try {
      const { data } = await axios.get(API_ENDPOINTS.REALTIME_SESSION_LIVE(sid));
      setSessionInfo(data.session);
      setStats(data.stats);
      setRecent(data.recent_scans);
    } catch (e) {
      // Silent fail in UI; page shows last known data
    }
  };

  useEffect(() => {
    if (routeSessionId) {
      setSessionId(routeSessionId);
    }
  }, [routeSessionId]);

  useEffect(() => {
    if (!sessionId) return;
    fetchLive(sessionId);
    connectWebSocket(sessionId);
    const interval = setInterval(() => fetchLive(sessionId), 15000);
    return () => {
      clearInterval(interval);
      if (wsRef.current) {
        try { wsRef.current.close(); } catch (_) {}
      }
    };
  }, [sessionId]);

  const cards = [
    { label: "Total", value: stats.total_students },
    { label: "Present", value: stats.present },
    { label: "Absent", value: stats.absent },
    { label: "Late", value: stats.late },
    { label: "%", value: `${stats.percentage}%` },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Live Attendance</h1>
          <p className="text-gray-600">Session: {sessionInfo.title || sessionId}</p>
        </div>
        <div className={`px-3 py-1 rounded-full text-sm ${connected ? "bg-green-100 text-green-700" : "bg-gray-100 text-gray-600"}`}>
          {connected ? "Live" : "Offline"}
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        {cards.map((c) => (
          <div key={c.label} className="bg-white rounded-xl shadow p-4 text-center">
            <div className="text-gray-500 text-sm">{c.label}</div>
            <div className="text-2xl font-semibold">{c.value}</div>
          </div>
        ))}
      </div>

      <div className="bg-white rounded-xl shadow p-4">
        <div className="flex items-center justify-between mb-3">
          <h2 className="font-semibold">Recent Scans</h2>
          <div className="text-sm text-gray-500">Latest 10</div>
        </div>
        <div className="overflow-auto">
          <table className="w-full text-left">
            <thead>
              <tr className="text-sm text-gray-500">
                <th className="py-2">Name</th>
                <th className="py-2">Email</th>
                <th className="py-2">Status</th>
                <th className="py-2">Time</th>
              </tr>
            </thead>
            <tbody>
              {recent.map((r) => (
                <tr key={r.id} className="border-t">
                  <td className="py-2">{r.user_name || r.user_id}</td>
                  <td className="py-2">{r.user_email || "-"}</td>
                  <td className="py-2 capitalize">{r.status}</td>
                  <td className="py-2">{new Date(r.timestamp).toLocaleString()}</td>
                </tr>
              ))}
              {recent.length === 0 && (
                <tr>
                  <td className="py-6 text-center text-gray-500" colSpan={4}>No scans yet.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default LiveAttendance;


