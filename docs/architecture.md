# VidyaSetu AI Architecture

## Primary flow

Student
→ University Discovery
→ Preference Filtering
→ Explainable Recommendation
→ University Comparison
→ Programme Selection
→ Academic Context
→ RAG Retrieval
→ Mock/LLM Tutor
→ Grounded Answer + Sources

## Architectural principle

Database-first and AI-second.

Structured facts such as programme availability, location, ranking fields and accreditation fields are stored/retrieved deterministically. AI is used for grounded academic assistance and later recommendation explanations, not as a replacement for authoritative structured data.
