# VidyaSetu AI — Recrafted Full-Stack Student Success Platform

**Tagline:** Discover the right university. Then learn smarter.

This project preserves the supplied React + Vite + TypeScript frontend and FastAPI + SQLAlchemy backend, while removing the fictional VidyaSetu universities, fabricated rankings, fake PYQs, hardcoded comparison table, and deterministic mock tutor. The UI is responsive and the student-facing Swagger navigation and default OpenAPI documentation endpoints are disabled.

## What's implemented

- **University Discovery:** backend-backed filters for course/degree, branch, specialization and location; pagination controls; details view; official links; compare selection.
- **Recommendations:** reads programme rows from the database and ranks only actual matching rows; returns up to 100 results from the available data. It never creates filler recommendations.
- **Comparison:** compare 2–5 selected institutions, using the ranking/accreditation fields stored in the database and showing missing data as not verified.
- **Academic Intelligence:** database-backed counts, course/resource/PYQ lists, source links and empty states instead of fake PDFs or question papers.
- **AI Tutor:** uses the configured OpenAI Chat Completions API from the backend when `OPENAI_API_KEY` is set. Without it, the app clearly reports that the provider is not configured.
- **Institution catalogue seed:** initial institution and NIRF Engineering 2025 ranking records are based on the official NIRF ranking table. Programme availability is deliberately *not* assumed. The seed does not create programmes, course resources or PYQs.
- **No Swagger link in the student UI:** FastAPI docs, ReDoc and OpenAPI endpoints are disabled by default.
- **Security basics:** API keys are backend-only; `.env` is excluded from the archive; `.env.example` contains placeholders.

## Important data accuracy note

The seed contains institution/ranking records, **not 100 verified AI/ML programme offerings**. NIRF ranks institutions in a ranking category; it does not prove that a specific campus currently offers a particular specialization. Programme recommendations remain empty until verified programme rows are imported from each institution's official programme/admissions pages. The same applies to NAAC accreditation, fees, placement statistics, syllabi and PYQ PDFs: unavailable fields remain unavailable rather than being invented.

Official source used for the included ranking records:
- NIRF India Rankings 2025 — Engineering: https://www.nirfindia.org/Rankings/2025/EngineeringRanking.html
- NIRF India Rankings 2025 — Engineering participated institutions: https://www.nirfindia.org/Rankings/2025/EngineeringRankingALL.html

Institution websites are stored as navigation links. These links are not proof of a particular programme or accreditation.

## Requirements

- Python 3.11+ recommended
- Node.js 20+ and npm
- Internet access for package installation and live AI requests (optional for non-AI pages)

## Run locally — Windows PowerShell

Open a terminal in the extracted `vidyasetu-ai` project root.

### 1. Backend setup

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `backend/.env`:
- Keep `DATABASE_URL=sqlite:///./vidyasetu.db` for local development.
- Replace `JWT_SECRET_KEY` with a long random secret.
- To enable live tutor answers, set `OPENAI_API_KEY=your_real_key` and optionally `OPENAI_MODEL=gpt-4o-mini`.
- Never put an LLM API key in frontend environment variables or commit it to Git.

Initialize the database and import the verified institution/ranking seed:

```powershell
python -m app.seed
uvicorn app.main:app --reload --port 8000
```

Backend health endpoint: http://localhost:8000/health  
API base: http://localhost:8000/api  
Swagger/ReDoc/OpenAPI are intentionally disabled in the default app configuration.

Keep this terminal running.

### 2. Frontend setup

Open a second terminal from the project root:

```powershell
cd frontend
npm install
npm run dev
```

Open the URL printed by Vite, usually http://localhost:5173.

### macOS / Linux backend commands

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
python -m app.seed
uvicorn app.main:app --reload --port 8000
```

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

## Database

SQLite is the default local database and persists to `backend/vidyasetu.db`. Do not delete this file if you want to keep your imported records. To use PostgreSQL, set `DATABASE_URL` to a valid SQLAlchemy PostgreSQL URL and install an appropriate PostgreSQL driver such as `psycopg[binary]`. Configure migrations and backups before production use.

`python -m app.seed` is additive: it inserts missing seed institution/ranking records and does not delete existing records. Review data before using it on an existing production database.

## AI tutor configuration

The tutor uses the backend's `OPENAI_API_KEY` and `OPENAI_MODEL` settings. The API key is sent only from the backend. Provider calls require network access, a valid key, available quota/billing and a valid model name. If the provider is not configured or unreachable, the tutor displays a clear message rather than fabricating an AI answer.

Academic database context is passed to the tutor when a course is selected by API clients. A full production RAG system still requires a PDF ingestion/indexing pipeline, embeddings/vector storage, source-page metadata and retrieval evaluation; this release does not claim those features are already populated.

## Populate verified programme and academic data

Use official programme/admissions pages for each campus and academic year. For every programme record, capture its source URL and verification date in the data import workflow. Add the `Programme` rows only after checking that the degree, branch and specialization are actually offered. Add resources/PYQs only when the actual document is available and the source is recorded.

Recommended sources:
- AKTU: https://aktu.ac.in/
- HBTU: https://hbtu.ac.in/
- SRMCEM: https://www.srmcem.ac.in/
- BBD University: https://bbdu.ac.in/
- NIRF: https://www.nirfindia.org/
- UGC: https://www.ugc.gov.in/

Respect the sites' access terms and copyright. Do not scrape restricted resources or present generated practice questions as official PYQs.

## API endpoints used by the UI

- `GET /health`
- `GET /api/universities?location=&branch=&programme=&specialization=&limit=50&offset=0`
- `GET /api/universities/{id}`
- `GET /api/programmes`
- `GET /api/courses`
- `GET /api/resources`
- `GET /api/pyqs`
- `POST /api/recommendations/universities`
- `POST /api/tutor/chat`

## Tests and build

Backend syntax check:

```bash
python -m compileall backend/app
```

Backend tests (if tests are installed):

```bash
cd backend
pytest
```

Frontend production build:

```bash
cd frontend
npm install
npm run build
```

## Production checklist

This is an improved development build, not a claim of fully production-verified data coverage. Before public launch:
1. Import and verify programme data across target institutions.
2. Ingest actual syllabus/PYQ PDFs and persist document provenance.
3. Implement full RAG ingestion, chunking, embeddings, citations and retrieval tests.
4. Add production authentication/authorization for admin operations, database migrations, monitoring, rate limiting and backups.
5. Configure secure CORS, PostgreSQL, secrets, hosting and TLS.
6. Run backend, frontend, responsive and end-to-end tests in the deployment environment.
