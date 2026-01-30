from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Admin schemas
class AdminLogin(BaseModel):
    username: str
    password: str

class AdminResponse(BaseModel):
    id: int
    username: str
    email: Optional[str]
    
    class Config:
        from_attributes = True

# Specialty schemas
class SpecialtyBase(BaseModel):
    name: str
    icon_url: Optional[str] = None

class SpecialtyCreate(SpecialtyBase):
    pass

class SpecialtyResponse(SpecialtyBase):
    id: int
    
    class Config:
        from_attributes = True

# Doctor schemas
class DoctorBase(BaseModel):
    name: str
    specialty_id: int
    phone: Optional[str] = None
    email: Optional[str] = None
    photo_url: Optional[str] = None
    bio: Optional[str] = None

class DoctorCreate(DoctorBase):
    pass

class DoctorUpdate(BaseModel):
    name: Optional[str] = None
    specialty_id: Optional[int] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    photo_url: Optional[str] = None
    bio: Optional[str] = None
    rating: Optional[float] = None

class DoctorResponse(DoctorBase):
    id: int
    rating: float
    created_at: datetime
    specialty: SpecialtyResponse
    
    class Config:
        from_attributes = True

# Clinic schemas
class ClinicBase(BaseModel):
    name: str
    address: str
    latitude: float
    longitude: float
    phone: Optional[str] = None
    working_hours: Optional[str] = None

class ClinicCreate(ClinicBase):
    doctor_id: int

class ClinicUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    phone: Optional[str] = None
    working_hours: Optional[str] = None

class ClinicResponse(ClinicBase):
    id: int
    doctor_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ClinicWithDoctorResponse(ClinicResponse):
    doctor: DoctorResponse
    distance: Optional[float] = None  # Distance in km from user location
    
    class Config:
        from_attributes = True

# Search request
class SearchRequest(BaseModel):
    specialty_id: Optional[int] = None
    doctor_name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    max_distance: Optional[float] = 50.0  # km
