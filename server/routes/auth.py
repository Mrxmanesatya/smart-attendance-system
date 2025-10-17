"""
Authentication routes
Handles user registration, login, and profile management
"""
from fastapi import APIRouter, HTTPException, status, Depends
from database import get_database
from models.user import UserCreate, UserLogin, UserResponse, Token, UserInDB
from utils.auth import verify_password, get_password_hash, create_access_token, get_current_user
from models.user import TokenData
from bson import ObjectId

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db=Depends(get_database)):
    """
    Register a new user
    
    - **name**: User's full name
    - **email**: Unique email address
    - **password**: Password (min 8 characters)
    - **organization_type**: Type of organization (corporate/college/gym/training_institute/other)
    - **org_name**: Name of the organization
    - **role**: User role (admin/instructor/trainee)
    """
    # Check if user already exists
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password
    password_hash = get_password_hash(user.password)
    
    # Create user document
    user_dict = user.model_dump(exclude={"password"})
    user_dict["password_hash"] = password_hash
    
    user_in_db = UserInDB(**user_dict)
    
    # Insert into database
    result = await db.users.insert_one(user_in_db.model_dump())
    
    # Retrieve created user
    created_user = await db.users.find_one({"_id": result.inserted_id})
    created_user["_id"] = str(created_user["_id"])
    
    return UserResponse(**created_user)


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin, db=Depends(get_database)):
    """
    Login and receive JWT access token
    
    - **email**: User's email
    - **password**: User's password
    
    Returns JWT token for authentication
    """
    # Find user by email
    user = await db.users.find_one({"email": credentials.email})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    if not verify_password(credentials.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = create_access_token(
        data={"sub": user["email"], "role": user["role"]}
    )
    
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: TokenData = Depends(get_current_user),
    db=Depends(get_database)
):
    """
    Get current authenticated user's profile
    
    Requires valid JWT token in Authorization header
    """
    user = await db.users.find_one({"email": current_user.email})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user["_id"] = str(user["_id"])
    return UserResponse(**user)
