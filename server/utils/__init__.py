"""Utilities package for Smart Attendance System"""

# Realtime utilities will be imported here for convenience
try:
    from .realtime import realtime_manager
except Exception:
    # Module may not exist during initial import or tooling; ignore
    realtime_manager = None
