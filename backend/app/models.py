from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    email = Column(String(180), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(30), default="STUDENT", nullable=False)
    is_active = Column(Boolean, default=True)

class University(Base):
    __tablename__ = "universities"
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    short_name = Column(String(80))
    type = Column(String(80))
    state = Column(String(80))
    city = Column(String(100))
    location = Column(String(150))
    website = Column(String(300))
    description = Column(Text)
    data_status = Column(String(30), default="DEMO")
    source_url = Column(String(500))

    programmes = relationship("Programme", back_populates="university", cascade="all, delete-orphan")
    ranking = relationship("Ranking", back_populates="university", uselist=False, cascade="all, delete-orphan")
    accreditation = relationship("Accreditation", back_populates="university", uselist=False, cascade="all, delete-orphan")

class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True)
    university_id = Column(Integer, ForeignKey("universities.id"))
    name = Column(String(150), nullable=False)

class Programme(Base):
    __tablename__ = "programmes"
    id = Column(Integer, primary_key=True)
    university_id = Column(Integer, ForeignKey("universities.id"))
    department = Column(String(150))
    name = Column(String(200), nullable=False)
    degree = Column(String(100))
    branch = Column(String(150))
    specialization = Column(String(150))
    duration_years = Column(Float, default=4)

    university = relationship("University", back_populates="programmes")
    courses = relationship("Course", back_populates="programme", cascade="all, delete-orphan")

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    programme_id = Column(Integer, ForeignKey("programmes.id"))
    code = Column(String(50))
    name = Column(String(200), nullable=False)
    semester = Column(Integer)
    credits = Column(Integer, default=4)

    programme = relationship("Programme", back_populates="courses")

class Curriculum(Base):
    __tablename__ = "curriculum_versions"
    id = Column(Integer, primary_key=True)
    programme_id = Column(Integer, ForeignKey("programmes.id"))
    version_name = Column(String(100))
    academic_year = Column(String(30))
    status = Column(String(30), default="CURRENT")

class Resource(Base):
    __tablename__ = "resources"
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"))
    title = Column(String(250))
    resource_type = Column(String(50))
    description = Column(Text)
    source = Column(String(300))

class PYQ(Base):
    __tablename__ = "pyqs"
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"))
    year = Column(Integer)
    exam_type = Column(String(80))
    question_text = Column(Text)
    topic = Column(String(150))
    marks = Column(Integer)

class Notice(Base):
    __tablename__ = "notices"
    id = Column(Integer, primary_key=True)
    university_id = Column(Integer, ForeignKey("universities.id"))
    title = Column(String(250))
    content = Column(Text)
    published_at = Column(DateTime, default=datetime.utcnow)

class Ranking(Base):
    __tablename__ = "rankings"
    id = Column(Integer, primary_key=True)
    university_id = Column(Integer, ForeignKey("universities.id"), unique=True)
    body = Column(String(50), default="NIRF")
    year = Column(Integer)
    category = Column(String(100))
    rank = Column(Integer)
    source_url = Column(String(500))
    status = Column(String(30), default="DEMO")

    university = relationship("University", back_populates="ranking")

class Accreditation(Base):
    __tablename__ = "accreditations"
    id = Column(Integer, primary_key=True)
    university_id = Column(Integer, ForeignKey("universities.id"), unique=True)
    body = Column(String(50), default="NAAC")
    grade = Column(String(20))
    year = Column(Integer)
    source_url = Column(String(500))
    status = Column(String(30), default="DEMO")

    university = relationship("University", back_populates="accreditation")
