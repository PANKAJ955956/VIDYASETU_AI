from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import or_
from .config import settings
from .database import Base, engine, get_db
from .models import User, University, Programme, Course, Resource, PYQ, Ranking, Accreditation, Curriculum, Notice
from .schemas import LoginRequest, RegisterRequest, TokenResponse, UniversityOut, RecommendationRequest, RecommendationItem, TutorRequest, TutorResponse
from .security import hash_password, verify_password, create_token, get_current_user, require_roles
from .services.recommendation import recommend
from .services.tutor import tutor_answer

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="VidyaSetu AI API",
    version="1.0.0",
    description="University Academic Intelligence & Student Success Platform",
    docs_url=None, redoc_url=None, openapi_url=None
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"name": settings.app_name, "status": "running", "docs": "disabled"}

@app.get("/health")
def health():
    return {"status": "healthy", "service": "vidyasetu-backend"}

@app.post("/api/auth/register", response_model=TokenResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload.email.lower()).first():
        raise HTTPException(400, "Email already registered")
    role = payload.role.upper()
    if role not in {"STUDENT", "FACULTY", "ADMIN"}:
        role = "STUDENT"
    user = User(
        name=payload.name,
        email=payload.email.lower(),
        password_hash=hash_password(payload.password),
        role=role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return TokenResponse(access_token=create_token(user))

@app.post("/api/auth/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email.lower()).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(401, "Invalid email or password")
    return TokenResponse(access_token=create_token(user))

@app.get("/api/auth/me")
def me(user=Depends(get_current_user)):
    return {"id": user.id, "name": user.name, "email": user.email, "role": user.role}

@app.get("/api/universities", response_model=list[UniversityOut])
def universities(
    location: str | None = None,
    branch: str | None = None,
    programme: str | None = None,
    specialization: str | None = None,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    query = db.query(University)
    if location:
        q = f"%{location}%"
        query = query.filter(or_(University.location.ilike(q), University.city.ilike(q), University.state.ilike(q)))
    universities = query.all()

    if branch or programme:
        filtered = []
        for u in universities:
            if any(
                (not branch or branch.lower() in (p.branch or "").lower() or branch.lower() in (p.name or "").lower())
                and (not programme or programme.lower() in (p.degree or "").lower() or programme.lower() in (p.name or "").lower())
                and (not specialization or specialization.lower() in (p.specialization or "").lower() or specialization.lower() in (p.name or "").lower())
                for p in u.programmes
            ):
                filtered.append(u)
        universities = filtered
    return universities[offset:offset + limit]

@app.get("/api/universities/{university_id}")
def university_detail(university_id: int, db: Session = Depends(get_db)):
    u = db.get(University, university_id)
    if not u:
        raise HTTPException(404, "University not found")
    return {
        "id": u.id,
        "name": u.name,
        "short_name": u.short_name,
        "location": u.location,
        "type": u.type,
        "description": u.description,
        "data_status": u.data_status,
        "source_url": u.source_url,
        "ranking": {
            "body": u.ranking.body,
            "year": u.ranking.year,
            "rank": u.ranking.rank,
            "category": u.ranking.category,
            "status": u.ranking.status,
            "source_url": u.ranking.source_url
        } if u.ranking else None,
        "accreditation": {
            "body": u.accreditation.body,
            "year": u.accreditation.year,
            "grade": u.accreditation.grade,
            "status": u.accreditation.status
        } if u.accreditation else None,
        "programmes": [
            {
                "id": p.id,
                "name": p.name,
                "degree": p.degree,
                "branch": p.branch,
                "specialization": p.specialization,
                "department": p.department
            } for p in u.programmes
        ]
    }

@app.get("/api/programmes")
def programmes(db: Session = Depends(get_db)):
    rows = db.query(Programme).all()
    return [{
        "id": p.id,
        "university_id": p.university_id,
        "university": p.university.name if p.university else None,
        "name": p.name,
        "degree": p.degree,
        "branch": p.branch,
        "specialization": p.specialization,
        "department": p.department
    } for p in rows]

@app.get("/api/courses")
def courses(programme_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(Course)
    if programme_id:
        query = query.filter(Course.programme_id == programme_id)
    rows = query.all()
    return [{
        "id": c.id,
        "programme_id": c.programme_id,
        "name": c.name,
        "code": c.code,
        "semester": c.semester,
        "credits": c.credits
    } for c in rows]

@app.get("/api/resources")
def resources(course_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(Resource)
    if course_id:
        query = query.filter(Resource.course_id == course_id)
    return [{
        "id": r.id, "course_id": r.course_id, "title": r.title,
        "resource_type": r.resource_type, "description": r.description, "source": r.source
    } for r in query.all()]

@app.get("/api/pyqs")
def pyqs(course_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(PYQ)
    if course_id:
        query = query.filter(PYQ.course_id == course_id)
    return [{
        "id": p.id, "course_id": p.course_id, "year": p.year,
        "exam_type": p.exam_type, "question": p.question_text,
        "topic": p.topic, "marks": p.marks
    } for p in query.order_by(PYQ.year.desc()).all()]

@app.get("/api/notices")
def notices(db: Session = Depends(get_db)):
    return [{
        "id": n.id, "university_id": n.university_id, "title": n.title,
        "content": n.content, "published_at": n.published_at.isoformat()
    } for n in db.query(Notice).order_by(Notice.published_at.desc()).all()]

@app.post("/api/recommendations/universities", response_model=list[RecommendationItem])
def recommendations(payload: RecommendationRequest, db: Session = Depends(get_db)):
    return recommend(db, payload)

@app.post("/api/tutor/chat", response_model=TutorResponse)
def tutor(payload: TutorRequest, db: Session = Depends(get_db)):
    return tutor_answer(db, payload)

@app.get("/api/dashboard")
def dashboard(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return {
        "user": {"name": user.name, "role": user.role},
        "universities": db.query(University).count(),
        "programmes": db.query(Programme).count(),
        "courses": db.query(Course).count(),
        "resources": db.query(Resource).count(),
        "pyqs": db.query(PYQ).count(),
        "notices": db.query(Notice).count()
    }

@app.post("/api/admin/seed-check")
def seed_check(user=Depends(require_roles("ADMIN"))):
    return {"message": "Admin access verified", "role": user.role}
