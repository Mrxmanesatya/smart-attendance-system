"""
Authentication utilities
Handles password hashing, JWT token generation and verification
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from config import settings
from models.user import TokenData, UserRole

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# HTTP Bearer token scheme
security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password
    
    Args:
        plain_password: Plain text password
        hashed_password: Hashed password from database
    
    Returns:
        bool: True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt
    
    Args:
        password: Plain text password
    
    Returns:
        str: Hashed password
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token
    
    Args:
        data: Dictionary containing token data (email, role, etc.)
        expires_delta: Optional expiration time delta
    
    Returns:
        str: Encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    
    return encoded_jwt


def decode_token(token: str) -> TokenData:
    """
    Decode and verify JWT token
    
    Args:
        token: JWT token string
    
    Returns:
        TokenData: Decoded token data
    
    Raises:
        HTTPException: If token is invalid or expired
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        email: str = payload.get("sub")
        role: str = payload.get("role")
        
        if email is None:
            raise credentials_exception
        
        token_data = TokenData(email=email, role=role)
        return token_data
        
    except JWTError:
        raise credentials_exception


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> TokenData:
    """
    Dependency to get current authenticated user from JWT token
    
    Args:
        credentials: HTTP Bearer credentials
    
    Returns:
        TokenData: Current user token data
    """
    token = credentials.credentials
    return decode_token(token)


async def require_role(required_roles: list[UserRole]):
    """
    Dependency factory to check if user has required role
    
    Args:
        required_roles: List of allowed roles
    
    Returns:
        Callable: Dependency function
    """
    async def role_checker(current_user: TokenData = Depends(get_current_user)) -> TokenData:
        if current_user.role not in [role.value for role in required_roles]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {[r.value for r in required_roles]}"
            )
        return current_user
    
    return role_checker
