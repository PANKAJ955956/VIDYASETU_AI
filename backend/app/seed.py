"""Initialize the schema and optionally import verified NIRF institution records.
No synthetic universities, programmes, rankings, or PYQs are seeded.
"""
from .database import Base, engine, SessionLocal
from .models import University, Ranking

NIRF_2025_ENGINEERING = [
    ("Indian Institute of Technology Madras", "IIT Madras", "Chennai", "Tamil Nadu", 1, "https://www.iitm.ac.in/"),
    ("Indian Institute of Technology Delhi", "IIT Delhi", "New Delhi", "Delhi", 2, "https://home.iitd.ac.in/"),
    ("Indian Institute of Technology Bombay", "IIT Bombay", "Mumbai", "Maharashtra", 3, "https://www.iitb.ac.in/"),
    ("Indian Institute of Technology Kanpur", "IIT Kanpur", "Kanpur", "Uttar Pradesh", 4, "https://www.iitk.ac.in/"),
    ("Indian Institute of Technology Kharagpur", "IIT Kharagpur", "Kharagpur", "West Bengal", 5, "https://www.iitkgp.ac.in/"),
    ("Indian Institute of Technology Roorkee", "IIT Roorkee", "Roorkee", "Uttarakhand", 6, "https://www.iitr.ac.in/"),
    ("Indian Institute of Technology Hyderabad", "IIT Hyderabad", "Hyderabad", "Telangana", 7, "https://iith.ac.in/"),
    ("National Institute of Technology Tiruchirappalli", "NIT Trichy", "Tiruchirappalli", "Tamil Nadu", 9, "https://www.nitt.edu/"),
    ("Indian Institute of Technology (BHU) Varanasi", "IIT (BHU) Varanasi", "Varanasi", "Uttar Pradesh", 10, "https://www.iitbhu.ac.in/"),
    ("National Institute of Technology Karnataka", "NITK Surathkal", "Mangaluru", "Karnataka", 17, "https://www.nitk.ac.in/"),
    ("Indian Institute of Technology (ISM) Dhanbad", "IIT (ISM) Dhanbad", "Dhanbad", "Jharkhand", 15, "https://www.iitism.ac.in/"),
    ("Indian Institute of Technology Indore", "IIT Indore", "Indore", "Madhya Pradesh", 16, "https://www.iiti.ac.in/"),
    ("National Institute of Technology Rourkela", "NIT Rourkela", "Rourkela", "Odisha", 13, "https://www.nitrkl.ac.in/"),
    ("National Institute of Technology Calicut", "NIT Calicut", "Kozhikode", "Kerala", 21, "https://nitc.ac.in/"),
    ("Delhi Technological University", "DTU", "New Delhi", "Delhi", 30, "https://dtu.ac.in/"),
    ("Motilal Nehru National Institute of Technology Allahabad", "MNNIT Allahabad", "Prayagraj", "Uttar Pradesh", 62, "https://www.mnnit.ac.in/"),
    ("Madan Mohan Malaviya University of Technology", "MMMUT", "Gorakhpur", "Uttar Pradesh", 60, "https://www.mmmut.ac.in/"),
]
NIRF_SOURCE = "https://www.nirfindia.org/Rankings/2025/EngineeringRanking.html"

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        for name, short, city, state, rank, website in NIRF_2025_ENGINEERING:
            u = db.query(University).filter(University.name == name).first()
            if not u:
                u = University(name=name, short_name=short, type="Higher education institution",
                    state=state, city=city, location=city, website=website,
                    description="Institution listed in the official NIRF India Rankings 2025 Engineering category. Programme-level availability must be verified separately.",
                    data_status="VERIFIED_INSTITUTION_RANKING", source_url=NIRF_SOURCE)
                db.add(u); db.flush()
            existing = db.query(Ranking).filter(Ranking.university_id == u.id, Ranking.year == 2025,
                                                Ranking.category == "Engineering").first()
            if not existing:
                db.add(Ranking(university_id=u.id, year=2025, category="Engineering", rank=rank,
                               status="VERIFIED", source_url=NIRF_SOURCE))
        db.commit()
        print("Database initialized. Imported verified NIRF 2025 Engineering institution/rank records; no fake programmes or PYQs were created.")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
