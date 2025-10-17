"""
Main application entry point
FastAPI application for Smart Attendance System
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from config import settings
from database import connect_to_mongo, close_mongo_connection
from routes import auth, sessions, attendance, miss_requests, admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler
    Manages startup and shutdown events
    """
    # Startup
    print("🚀 Starting Smart Attendance System...")
    await connect_to_mongo()
    yield
    # Shutdown
    print("🛑 Shutting down...")
    await close_mongo_connection()


# Initialize FastAPI app
app = FastAPI(
    title="Smart Attendance System API",
    description="QR-based attendance tracking system with role-based access control",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(sessions.router)
app.include_router(attendance.router)
app.include_router(miss_requests.router)
app.include_router(admin.router)


@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "message": "Smart Attendance System API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=True
    )
