"""
Database connection and initialization module
Handles MongoDB connection using Motor async driver
"""
from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

# Global database client
client: AsyncIOMotorClient = None
database = None


async def connect_to_mongo():
    """
    Establish connection to MongoDB
    Called on application startup
    """
    global client, database
    try:
        client = AsyncIOMotorClient(settings.mongodb_url)
        database = client[settings.database_name]
        
        # Test connection
        await client.admin.command('ping')
        print(f"✅ Connected to MongoDB: {settings.database_name}")
        
        # Create indexes for optimization
        await create_indexes()
        
    except Exception as e:
        print(f"❌ Error connecting to MongoDB: {e}")
        raise


async def close_mongo_connection():
    """
    Close MongoDB connection
    Called on application shutdown
    """
    global client
    if client:
        client.close()
        print("🔌 Closed MongoDB connection")


async def create_indexes():
    """
    Create database indexes for better query performance
    """
    # Users collection indexes
    await database.users.create_index("email", unique=True)
    await database.users.create_index("role")
    await database.users.create_index("organization_type")
    
    # Sessions collection indexes
    await database.sessions.create_index("created_by")
    await database.sessions.create_index("start_time")
    await database.sessions.create_index("active")
    
    # Attendance records indexes
    await database.attendance_records.create_index([("session_id", 1), ("user_id", 1)], unique=True)
    await database.attendance_records.create_index("user_id")
    await database.attendance_records.create_index("timestamp")
    
    # QR codes indexes
    await database.qr_codes.create_index("session_id")
    await database.qr_codes.create_index("expires_at")
    await database.qr_codes.create_index("code_value", unique=True)
    
    # Miss requests indexes
    await database.miss_requests.create_index("user_id")
    await database.miss_requests.create_index("session_id")
    await database.miss_requests.create_index("status")
    
    print("📑 Database indexes created successfully")


def get_database():
    """
    Dependency to get database instance
    """
    return database
