from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import database
import schemas
import auth
from utils import calculate_distance

# Initialize FastAPI app
app = FastAPI(
    title="My Doctor API",
    description="API for finding nearby doctors and clinics",
    version="1.0.0"
)

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    database.init_db()
    # Create default admin if not exists
    db = database.SessionLocal()
    admin = db.query(database.Admin).filter(database.Admin.username == "admin").first()
    if not admin:
        default_admin = database.Admin(
            username="admin",
            password_hash=auth.get_password_hash("admin123"),
            email="admin@mydoctor.com"
        )
        db.add(default_admin)
        db.commit()
        print("✅ Default admin created: username=admin, password=admin123")
    db.close()

# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": "Welcome to My Doctor API",
        "docs": "/docs",
        "version": "1.0.0"
    }

# ==================== Admin Authentication ====================

@app.post("/api/admin/login")
def admin_login(credentials: schemas.AdminLogin, db: Session = Depends(database.get_db)):
    """Admin login endpoint."""
    admin = db.query(database.Admin).filter(
        database.Admin.username == credentials.username
    ).first()
    
    if not admin or not auth.verify_password(credentials.password, admin.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="اسم المستخدم أو كلمة المرور غير صحيحة"
        )
    
    access_token = auth.create_access_token(data={"sub": admin.username})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "admin": {
            "id": admin.id,
            "username": admin.username,
            "email": admin.email
        }
    }

# ==================== Specialties ====================

@app.get("/api/specialties", response_model=List[schemas.SpecialtyResponse])
def get_specialties(db: Session = Depends(database.get_db)):
    """Get all medical specialties."""
    specialties = db.query(database.Specialty).all()
    return specialties

@app.post("/api/specialties", response_model=schemas.SpecialtyResponse)
def create_specialty(specialty: schemas.SpecialtyCreate, db: Session = Depends(database.get_db)):
    """Create a new specialty (admin only)."""
    db_specialty = database.Specialty(**specialty.dict())
    db.add(db_specialty)
    db.commit()
    db.refresh(db_specialty)
    return db_specialty

# ==================== Doctors ====================

@app.get("/api/doctors", response_model=List[schemas.DoctorResponse])
def get_doctors(
    specialty_id: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(database.get_db)
):
    """Get all doctors with optional filters."""
    query = db.query(database.Doctor)
    
    if specialty_id:
        query = query.filter(database.Doctor.specialty_id == specialty_id)
    
    if search:
        query = query.filter(database.Doctor.name.contains(search))
    
    doctors = query.all()
    return doctors

@app.get("/api/doctors/{doctor_id}", response_model=schemas.DoctorResponse)
def get_doctor(doctor_id: int, db: Session = Depends(database.get_db)):
    """Get a specific doctor by ID."""
    doctor = db.query(database.Doctor).filter(database.Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="الطبيب غير موجود")
    return doctor

@app.post("/api/doctors", response_model=schemas.DoctorResponse)
def create_doctor(doctor: schemas.DoctorCreate, db: Session = Depends(database.get_db)):
    """Create a new doctor (admin only)."""
    # Check if specialty exists
    specialty = db.query(database.Specialty).filter(
        database.Specialty.id == doctor.specialty_id
    ).first()
    if not specialty:
        raise HTTPException(status_code=404, detail="التخصص غير موجود")
    
    db_doctor = database.Doctor(**doctor.dict())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

@app.put("/api/doctors/{doctor_id}", response_model=schemas.DoctorResponse)
def update_doctor(
    doctor_id: int,
    doctor: schemas.DoctorUpdate,
    db: Session = Depends(database.get_db)
):
    """Update a doctor (admin only)."""
    db_doctor = db.query(database.Doctor).filter(database.Doctor.id == doctor_id).first()
    if not db_doctor:
        raise HTTPException(status_code=404, detail="الطبيب غير موجود")
    
    # Update only provided fields
    for field, value in doctor.dict(exclude_unset=True).items():
        setattr(db_doctor, field, value)
    
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

@app.delete("/api/doctors/{doctor_id}")
def delete_doctor(doctor_id: int, db: Session = Depends(database.get_db)):
    """Delete a doctor (admin only)."""
    db_doctor = db.query(database.Doctor).filter(database.Doctor.id == doctor_id).first()
    if not db_doctor:
        raise HTTPException(status_code=404, detail="الطبيب غير موجود")
    
    db.delete(db_doctor)
    db.commit()
    return {"message": "تم حذف الطبيب بنجاح"}

# ==================== Clinics ====================

@app.get("/api/clinics", response_model=List[schemas.ClinicWithDoctorResponse])
def get_clinics(
    doctor_id: Optional[int] = None,
    db: Session = Depends(database.get_db)
):
    """Get all clinics with optional filters."""
    query = db.query(database.Clinic)
    
    if doctor_id:
        query = query.filter(database.Clinic.doctor_id == doctor_id)
    
    clinics = query.all()
    return clinics

@app.post("/api/clinics", response_model=schemas.ClinicResponse)
def create_clinic(clinic: schemas.ClinicCreate, db: Session = Depends(database.get_db)):
    """Create a new clinic (admin only)."""
    # Check if doctor exists
    doctor = db.query(database.Doctor).filter(database.Doctor.id == clinic.doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="الطبيب غير موجود")
    
    db_clinic = database.Clinic(**clinic.dict())
    db.add(db_clinic)
    db.commit()
    db.refresh(db_clinic)
    return db_clinic

@app.put("/api/clinics/{clinic_id}", response_model=schemas.ClinicResponse)
def update_clinic(
    clinic_id: int,
    clinic: schemas.ClinicUpdate,
    db: Session = Depends(database.get_db)
):
    """Update a clinic (admin only)."""
    db_clinic = db.query(database.Clinic).filter(database.Clinic.id == clinic_id).first()
    if not db_clinic:
        raise HTTPException(status_code=404, detail="العيادة غير موجودة")
    
    for field, value in clinic.dict(exclude_unset=True).items():
        setattr(db_clinic, field, value)
    
    db.commit()
    db.refresh(db_clinic)
    return db_clinic

@app.delete("/api/clinics/{clinic_id}")
def delete_clinic(clinic_id: int, db: Session = Depends(database.get_db)):
    """Delete a clinic (admin only)."""
    db_clinic = db.query(database.Clinic).filter(database.Clinic.id == clinic_id).first()
    if not db_clinic:
        raise HTTPException(status_code=404, detail="العيادة غير موجودة")
    
    db.delete(db_clinic)
    db.commit()
    return {"message": "تم حذف العيادة بنجاح"}

# ==================== Search & Location ====================

@app.get("/api/clinics/nearby", response_model=List[schemas.ClinicWithDoctorResponse])
def get_nearby_clinics(
    latitude: float,
    longitude: float,
    specialty_id: Optional[int] = None,
    max_distance: float = 50.0,
    db: Session = Depends(database.get_db)
):
    """
    Find nearby clinics based on user location.
    Returns clinics sorted by distance.
    """
    query = db.query(database.Clinic)
    
    if specialty_id:
        query = query.join(database.Doctor).filter(database.Doctor.specialty_id == specialty_id)
    
    clinics = query.all()
    
    # Calculate distance for each clinic
    clinics_with_distance = []
    for clinic in clinics:
        distance = calculate_distance(latitude, longitude, clinic.latitude, clinic.longitude)
        if distance <= max_distance:
            clinic_dict = schemas.ClinicWithDoctorResponse.from_orm(clinic).dict()
            clinic_dict['distance'] = round(distance, 2)
            clinics_with_distance.append(clinic_dict)
    
    # Sort by distance
    clinics_with_distance.sort(key=lambda x: x['distance'])
    
    return clinics_with_distance

@app.post("/api/search", response_model=List[schemas.ClinicWithDoctorResponse])
def search_clinics(search_req: schemas.SearchRequest, db: Session = Depends(database.get_db)):
    """
    Advanced search for clinics by specialty, doctor name, or location.
    """
    query = db.query(database.Clinic).join(database.Doctor)
    
    if search_req.specialty_id:
        query = query.filter(database.Doctor.specialty_id == search_req.specialty_id)
    
    if search_req.doctor_name:
        query = query.filter(database.Doctor.name.contains(search_req.doctor_name))
    
    clinics = query.all()
    
    # If location provided, calculate distances
    if search_req.latitude and search_req.longitude:
        clinics_with_distance = []
        for clinic in clinics:
            distance = calculate_distance(
                search_req.latitude,
                search_req.longitude,
                clinic.latitude,
                clinic.longitude
            )
            if distance <= search_req.max_distance:
                clinic_dict = schemas.ClinicWithDoctorResponse.from_orm(clinic).dict()
                clinic_dict['distance'] = round(distance, 2)
                clinics_with_distance.append(clinic_dict)
        
        clinics_with_distance.sort(key=lambda x: x['distance'])
        return clinics_with_distance
    
    return clinics

# ==================== Health Check ====================

@app.get("/health")
def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy", "service": "My Doctor API"}
