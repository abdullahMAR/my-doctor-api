"""
Seed script to populate the database with sample data for testing.
Run this after starting the server for the first time.
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def seed_database():
    print("🌱 Starting database seeding...")
    
    # Login as admin
    print("\n1️⃣ Logging in as admin...")
    login_response = requests.post(f"{BASE_URL}/admin/login", json={
        "username": "admin",
        "password": "admin123"
    })
    
    if login_response.status_code != 200:
        print("❌ Login failed!")
        return
    
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("✅ Logged in successfully")
    
    # Create specialties
    print("\n2️⃣ Creating specialties...")
    specialties = [
        {"name": "طب عام", "icon_url": None},
        {"name": "أسنان", "icon_url": None},
        {"name": "عيون", "icon_url": None},
        {"name": "قلب", "icon_url": None},
        {"name": "عظام", "icon_url": None},
        {"name": "جلدية", "icon_url": None},
        {"name": "أطفال", "icon_url": None},
        {"name": "نساء وولادة", "icon_url": None},
    ]
    
    specialty_ids = {}
    for specialty in specialties:
        response = requests.post(f"{BASE_URL}/specialties", json=specialty, headers=headers)
        if response.status_code == 200:
            data = response.json()
            specialty_ids[specialty["name"]] = data["id"]
            print(f"  ✅ {specialty['name']}")
    
    # Create doctors
    print("\n3️⃣ Creating doctors...")
    doctors = [
        {
            "name": "د. محمد أحمد",
            "specialty_id": specialty_ids["طب عام"],
            "phone": "+970599123456",
            "email": "dr.mohammed@example.com",
            "bio": "طبيب عام مع خبرة 15 سنة"
        },
        {
            "name": "د. فاطمة علي",
            "specialty_id": specialty_ids["أسنان"],
            "phone": "+970599234567",
            "email": "dr.fatima@example.com",
            "bio": "أخصائية طب الأسنان"
        },
        {
            "name": "د. خالد محمود",
            "specialty_id": specialty_ids["عيون"],
            "phone": "+970599345678",
            "email": "dr.khaled@example.com",
            "bio": "استشاري طب وجراحة العيون"
        },
        {
            "name": "د. سارة حسن",
            "specialty_id": specialty_ids["قلب"],
            "phone": "+970599456789",
            "email": "dr.sarah@example.com",
            "bio": "أخصائية أمراض القلب"
        },
        {
            "name": "د. يوسف عبدالله",
            "specialty_id": specialty_ids["عظام"],
            "phone": "+970599567890",
            "email": "dr.yousef@example.com",
            "bio": "جراح عظام ومفاصل"
        },
    ]
    
    doctor_ids = []
    for doctor in doctors:
        response = requests.post(f"{BASE_URL}/doctors", json=doctor, headers=headers)
        if response.status_code == 200:
            data = response.json()
            doctor_ids.append(data["id"])
            print(f"  ✅ {doctor['name']}")
    
    # Create clinics (sample locations in Palestine)
    print("\n4️⃣ Creating clinics...")
    clinics = [
        {
            "doctor_id": doctor_ids[0],
            "name": "عيادة د. محمد - رام الله",
            "address": "شارع الإرسال، رام الله",
            "latitude": 31.9038,
            "longitude": 35.2034,
            "phone": "+970599123456",
            "working_hours": "8:00 ص - 4:00 م"
        },
        {
            "doctor_id": doctor_ids[1],
            "name": "عيادة د. فاطمة للأسنان - نابلس",
            "address": "شارع فيصل، نابلس",
            "latitude": 32.2211,
            "longitude": 35.2544,
            "phone": "+970599234567",
            "working_hours": "9:00 ص - 5:00 م"
        },
        {
            "doctor_id": doctor_ids[2],
            "name": "مركز د. خالد للعيون - القدس",
            "address": "شارع صلاح الدين، القدس",
            "latitude": 31.7833,
            "longitude": 35.2167,
            "phone": "+970599345678",
            "working_hours": "10:00 ص - 6:00 م"
        },
        {
            "doctor_id": doctor_ids[3],
            "name": "عيادة القلب - الخليل",
            "address": "شارع عين سارة، الخليل",
            "latitude": 31.5326,
            "longitude": 35.0998,
            "phone": "+970599456789",
            "working_hours": "8:00 ص - 3:00 م"
        },
        {
            "doctor_id": doctor_ids[4],
            "name": "عيادة العظام والمفاصل - بيت لحم",
            "address": "شارع المهد، بيت لحم",
            "latitude": 31.7054,
            "longitude": 35.2024,
            "phone": "+970599567890",
            "working_hours": "9:00 ص - 4:00 م"
        },
    ]
    
    for clinic in clinics:
        response = requests.post(f"{BASE_URL}/clinics", json=clinic, headers=headers)
        if response.status_code == 200:
            print(f"  ✅ {clinic['name']}")
    
    print("\n✅ Database seeded successfully!")
    print("\n📊 Summary:")
    print(f"  - Specialties: {len(specialties)}")
    print(f"  - Doctors: {len(doctors)}")
    print(f"  - Clinics: {len(clinics)}")

if __name__ == "__main__":
    try:
        seed_database()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the server.")
        print("Make sure the server is running: uvicorn main:app --reload")
    except Exception as e:
        print(f"❌ Error: {e}")
