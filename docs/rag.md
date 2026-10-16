# RAG Design

Production pipeline:

Documents
→ extraction
→ cleaning
→ chunking
→ embeddings
→ vector store
→ metadata filtering
→ semantic retrieval
→ context builder
→ provider
→ answer + citations

Required metadata:

- university_id
- programme_id
- semester
- course_id
- document_type
- academic_year
- source
- source_url
