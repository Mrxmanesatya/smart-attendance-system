"""
Database Seed Script
Creates sample data for testing the Smart Attendance System
"""

import asyncio
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# MongoDB connection
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017/smart_attendance")
client = AsyncIOMotorClient(MONGODB_URL)
db = client.get_database()


async def clear_database():
    """Clear all collections"""
    print("🗑️  Clearing database...")
    collections = await db.list_collection_names()
    for collection_name in collections:
        await db[collection_name].delete_many({})
    print("✅ Database cleared")


async def create_users():
    """Create sample users"""
    print("\n👥 Creating users...")
    
    users = [
        # Admins
        {
            "name": "Admin User",
            "email": "admin@example.com",
            "password": pwd_context.hash("admin123"),
            "role": "admin",
            "organization": "TechCorp HQ",
            "created_at": datetime.utcnow()
        },
        # Instructors
        {
            "name": "John Smith",
            "email": "john.instructor@example.com",
            "password": pwd_context.hash("instructor123"),
            "role": "instructor",
            "organization": "TechCorp Training",
            "created_at": datetime.utcnow()
        },
        {
            "name": "Sarah Johnson",
            "email": "sarah.instructor@example.com",
            "password": pwd_context.hash("instructor123"),
            "role": "instructor",
            "organization": "TechCorp Training",
            "created_at": datetime.utcnow()
        },
        # Trainees
        {
            "name": "Alice Brown",
            "email": "alice.trainee@example.com",
            "password": pwd_context.hash("trainee123"),
            "role": "trainee",
            "organization": "TechCorp Batch 2025",
            "created_at": datetime.utcnow()
        },
        {
            "name": "Bob Wilson",
            "email": "bob.trainee@example.com",
            "password": pwd_context.hash("trainee123"),
            "role": "trainee",
            "organization": "TechCorp Batch 2025",
            "created_at": datetime.utcnow()
        },
        {
            "name": "Charlie Davis",
            "email": "charlie.trainee@example.com",
            "password": pwd_context.hash("trainee123"),
            "role": "trainee",
            "organization": "TechCorp Batch 2025",
            "created_at": datetime.utcnow()
        },
        {
            "name": "Diana Miller",
            "email": "diana.trainee@example.com",
            "password": pwd_context.hash("trainee123"),
            "role": "trainee",
            "organization": "TechCorp Batch 2025",
            "created_at": datetime.utcnow()
        },
        {
            "name": "Ethan Martinez",
            "email": "ethan.trainee@example.com",
            "password": pwd_context.hash("trainee123"),
            "role": "trainee",
            "organization": "TechCorp Batch 2025",
            "created_at": datetime.utcnow()
        }
    ]
    
    result = await db.users.insert_many(users)
    user_ids = result.inserted_ids
    
    print(f"✅ Created {len(user_ids)} users")
    print("\n📝 Login Credentials:")
    print("=" * 60)
    print("ADMIN:")
    print("  Email: admin@example.com")
    print("  Password: admin123")
    print("\nINSTRUCTOR:")
    print("  Email: john.instructor@example.com")
    print("  Password: instructor123")
    print("\nTRAINEE:")
    print("  Email: alice.trainee@example.com")
    print("  Password: trainee123")
    print("=" * 60)
    
    return user_ids


async def create_sessions(user_ids):
    """Create sample training sessions"""
    print("\n📚 Creating sessions...")
    
    # Get instructor ID
    instructor = await db.users.find_one({"role": "instructor"})
    instructor_id = str(instructor["_id"])
    
    sessions = []
    for i in range(10):
        start_time = datetime.utcnow() - timedelta(days=9-i, hours=9)
        end_time = start_time + timedelta(hours=2)
        
        sessions.append({
            "title": f"Python Training Day {i+1}",
            "description": f"Advanced Python concepts and best practices - Session {i+1}",
            "instructor_id": instructor_id,
            "start_time": start_time,
            "end_time": end_time,
            "is_active": i >= 8,  # Last 2 sessions are active
            "created_at": start_time - timedelta(days=1)
        })
    
    result = await db.sessions.insert_many(sessions)
    session_ids = result.inserted_ids
    
    print(f"✅ Created {len(session_ids)} sessions")
    return session_ids


async def create_attendance(session_ids, user_ids):
    """Create sample attendance records"""
    print("\n✅ Creating attendance records...")
    
    # Get trainee IDs
    trainees = []
    async for user in db.users.find({"role": "trainee"}):
        trainees.append(str(user["_id"]))
    
    attendance_records = []
    
    # For each session (except last 2 which are future)
    for session_id in session_ids[:-2]:
        session = await db.sessions.find_one({"_id": session_id})
        
        # 80% attendance rate simulation
        for trainee_id in trainees:
            import random
            
            # 80% chance of attendance
            if random.random() < 0.8:
                # 70% on time, 30% late
                status = "present" if random.random() < 0.7 else "late"
                timestamp = session["start_time"] + timedelta(minutes=random.randint(-5, 30))
                
                attendance_records.append({
                    "user_id": trainee_id,
                    "session_id": str(session["_id"]),
                    "status": status,
                    "timestamp": timestamp,
                    "method": "qr_scan",
                    "created_at": timestamp
                })
    
    if attendance_records:
        await db.attendance.insert_many(attendance_records)
        print(f"✅ Created {len(attendance_records)} attendance records")


async def create_miss_requests(user_ids):
    """Create sample miss attendance requests"""
    print("\n📝 Creating miss requests...")
    
    # Get trainee and session IDs
    trainees = []
    async for user in db.users.find({"role": "trainee"}, limit=3):
        trainees.append(str(user["_id"]))
    
    sessions = []
    async for session in db.sessions.find({}, limit=5):
        sessions.append(str(session["_id"]))
    
    miss_requests = [
        {
            "user_id": trainees[0],
            "session_id": sessions[0],
            "reason": "Had a medical emergency and couldn't attend the session",
            "status": "pending",
            "created_at": datetime.utcnow() - timedelta(days=2)
        },
        {
            "user_id": trainees[1],
            "session_id": sessions[1],
            "reason": "Network issues prevented me from joining the online session",
            "status": "approved",
            "admin_response": "Request approved. Attendance marked as present.",
            "created_at": datetime.utcnow() - timedelta(days=5),
            "updated_at": datetime.utcnow() - timedelta(days=4)
        },
        {
            "user_id": trainees[2],
            "session_id": sessions[2],
            "reason": "Family emergency",
            "status": "rejected",
            "admin_response": "Please provide a valid medical certificate for future requests.",
            "created_at": datetime.utcnow() - timedelta(days=7),
            "updated_at": datetime.utcnow() - timedelta(days=6)
        }
    ]
    
    await db.miss_requests.insert_many(miss_requests)
    print(f"✅ Created {len(miss_requests)} miss requests")


async def main():
    """Main seed function"""
    print("\n" + "="*60)
    print("🌱 SEEDING DATABASE - Smart Attendance System")
    print("="*60)
    
    try:
        # Clear existing data
        await clear_database()
        
        # Create data
        user_ids = await create_users()
        session_ids = await create_sessions(user_ids)
        await create_attendance(session_ids, user_ids)
        await create_miss_requests(user_ids)
        
        print("\n" + "="*60)
        print("🎉 DATABASE SEEDING COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("\n🚀 You can now:")
        print("  1. Start the backend: python main.py")
        print("  2. Start the frontend: cd client && npm run dev")
        print("  3. Login with the credentials above")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ Error during seeding: {e}")
    finally:
        client.close()


if __name__ == "__main__":
    asyncio.run(main())
