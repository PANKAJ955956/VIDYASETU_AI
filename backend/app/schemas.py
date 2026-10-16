from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    role: str = "STUDENT"

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ProgrammeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    degree: Optional[str] = None
    branch: Optional[str] = None
    specialization: Optional[str] = None
    department: Optional[str] = None

class UniversityOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    short_name: Optional[str] = None
    type: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    data_status: str
    source_url: Optional[str] = None

class RecommendationRequest(BaseModel):
    course: Optional[str] = None
    branch: Optional[str] = None
    specialization: Optional[str] = None
    location: Optional[str] = None
    prefer_nirf: bool = True
    prefer_naac: bool = True

class RecommendationItem(BaseModel):
    university_id: int
    university: str
    programme: str
    location: str
    nirf_rank: Optional[int] = None
    naac_grade: Optional[str] = None
    match_score: int
    match_level: str
    match_reasons: List[str]

class TutorRequest(BaseModel):
    question: str
    university_id: Optional[int] = None
    programme_id: Optional[int] = None
    semester: Optional[int] = None
    course_id: Optional[int] = None

class SourceItem(BaseModel):
    title: str
    source: str
    type: str
    relevance: str

class TutorResponse(BaseModel):
    answer: str
    sources: List[SourceItem]
    provider: Optional[str] = None
