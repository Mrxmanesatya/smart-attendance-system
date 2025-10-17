"""
QR Code generation utilities
Handles QR code creation and encoding
"""
import qrcode
import io
import base64
from datetime import datetime, timedelta
import secrets
from config import settings


def generate_qr_code_value(session_id: str) -> str:
    """
    Generate a unique QR code value for a session
    
    Args:
        session_id: ID of the session
    
    Returns:
        str: Unique QR code value
    """
    # Create a unique token combining session ID, timestamp, and random string
    timestamp = int(datetime.utcnow().timestamp())
    random_token = secrets.token_urlsafe(32)
    
    qr_value = f"{session_id}:{timestamp}:{random_token}"
    return qr_value


def create_qr_image(data: str) -> str:
    """
    Create QR code image and return as base64 encoded string
    
    Args:
        data: Data to encode in QR code
    
    Returns:
        str: Base64 encoded QR code image
    """
    # Create QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    # Add data and generate
    qr.add_data(data)
    qr.make(fit=True)
    
    # Create image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    return img_base64


def get_qr_expiry_time() -> datetime:
    """
    Calculate QR code expiry time
    
    Returns:
        datetime: Expiry timestamp
    """
    return datetime.utcnow() + timedelta(minutes=settings.qr_code_expiry_minutes)


def is_qr_expired(expires_at: datetime) -> bool:
    """
    Check if QR code has expired
    
    Args:
        expires_at: Expiry timestamp
    
    Returns:
        bool: True if expired, False otherwise
    """
    return datetime.utcnow() > expires_at
