from sqlalchemy.orm import Session
from ..models import University

def _matches(value, target):
    if not target:
        return True
    return bool(value) and target.strip().casefold() in value.strip().casefold()

def recommend(db: Session, request):
    """Recommend only programmes actually present in the database; never synthesize rows."""
    results = []
    for university in db.query(University).all():
        for programme in university.programmes:
            if not _matches(programme.degree or programme.name, request.course):
                continue
            if not _matches(programme.branch or programme.name, request.branch):
                continue
            if not _matches(programme.specialization or programme.name, request.specialization):
                continue
            loc = " ".join(filter(None, [university.location, university.city, university.state]))
            if request.location and request.location.casefold() not in loc.casefold():
                continue
            reasons = ["Verified programme record matches selected filters"]
            score = 70
            if request.location:
                score += 10; reasons.append("Location matches")
            if request.prefer_nirf and university.ranking and university.ranking.status == "VERIFIED":
                score += 10; reasons.append(f"NIRF Engineering rank {university.ranking.rank} ({university.ranking.year})")
            if request.prefer_naac and university.accreditation and university.accreditation.status == "VERIFIED":
                score += 5; reasons.append("Verified accreditation record available")
            results.append({
                "university_id": university.id, "university": university.name,
                "programme": programme.name, "location": university.location or loc,
                "nirf_rank": university.ranking.rank if university.ranking and university.ranking.status == "VERIFIED" else None,
                "naac_grade": university.accreditation.grade if university.accreditation and university.accreditation.status == "VERIFIED" else None,
                "match_score": min(score, 100),
                "match_level": "Strong match" if score >= 85 else "Potential match",
                "match_reasons": reasons,
            })
    return sorted(results, key=lambda x: (x["match_score"], -(x["nirf_rank"] or 9999)), reverse=True)[:100]
