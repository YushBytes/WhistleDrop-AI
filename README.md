# WhistleDrop AI

**Anonymous Reporting & Intelligent Case Triage System**

A confidential reporting backend. Anyone can submit a report **without an
account and without revealing their identity**, and receives a single secret
**case code** that is the only way to track it afterwards. Moderators triage
the queue without ever learning who reported what.

Built for **GDG on Campus SRM — Technical Recruitment 2026-27**
(task: *WhistleDrop — Speak Without Being Seen*).

> **Project status: Phase 0 of 8 complete** — foundation and scaffolding.
> The reporting, moderation and ML features are not implemented yet.
> See [Roadmap](#roadmap).

---

## Scope: official task vs. our extension

This repository implements the official task **and** one clearly-marked
addition. The two are kept separate on purpose.

| | Included |
|---|---|
| **Official GDG requirements** | Anonymous submission, category, description, optional evidence URL, secure case code, case tracking, `SUBMITTED → UNDER_REVIEW → RESOLVED / DISMISSED` workflow, moderator access, filtering, status updates, validation, Swagger/OpenAPI, tests |
| **Our extension — *not* part of the official spec** | **AI-Assisted Report Triage**: suggested category + confidence, suggested priority, and the keywords that drove the prediction |

**The AI is advisory only.** It cannot change a report's status or its official
category. Every decision stays with a human moderator, and moderator overrides
are recorded as future training data.

---

## Anonymity: what this system does and does not guarantee

Being precise about this matters more than sounding impressive.

**What it does**

- No reporter name, email, phone number, or account is collected — there is no
  reporters table in the schema at all.
- The case code is stored only as an HMAC-SHA256 digest keyed with a
  server-side pepper. A stolen database dump alone does not yield usable codes.
- Report contents are kept out of application logs.
- Primary keys are UUIDs, so identifiers leak neither volume nor ordering.

**What it does not**

- **Network-level anonymity is out of scope.** Your IP address still reaches
  the server's TLS terminator. Use Tor or a VPN if your threat model needs it.
- Submission timing can be correlated with other events.
- Writing style is identifying, and a report can de-anonymise its author
  through its own contents.
- **A lost case code cannot be recovered.** Any recovery mechanism would
  require an identity, which would defeat the system.

---

## Tech stack

| Layer | Choice |
|---|---|
| API | FastAPI (Python 3.12) |
| Validation | Pydantic v2 |
| Database | PostgreSQL 16 *(via Docker Compose)* |
| ORM / migrations | SQLAlchemy 2.0 + Alembic |
| Auth | JWT (HS256) + bcrypt, moderators only |
| ML | scikit-learn — TF-IDF → Logistic Regression |
| Tests | Pytest against real PostgreSQL |
| Docs | Swagger UI / OpenAPI |

---

## Getting started

### Prerequisites

- **Python 3.12** (3.13+ is not supported; see `pyproject.toml`)
- **Docker Desktop** — required from Phase 1 onward for PostgreSQL

### Setup

```bash
# 1. Create and activate a virtual environment
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1        # PowerShell
# source .venv/bin/activate         # macOS / Linux

# 2. Install dependencies
pip install -r requirements.txt -r requirements-dev.txt

# 3. Create your local environment file
copy .env.example .env              # PowerShell
# cp .env.example .env              # macOS / Linux
```

Then edit `.env` and set a strong `POSTGRES_PASSWORD`, keeping the value
consistent inside `DATABASE_URL` and `TEST_DATABASE_URL`.

`.env` is gitignored and must never be committed.

### Start the database *(needed from Phase 1)*

```bash
docker compose up -d
docker compose ps          # both containers should report "healthy"
```

Two containers are provisioned: development on port **5432** and a disposable
in-memory test database on port **5433**, so the test suite can never touch
development data.

### Run the API

```bash
uvicorn app.main:app --reload
```

| URL | Purpose |
|---|---|
| <http://127.0.0.1:8000/docs> | Swagger UI |
| <http://127.0.0.1:8000/redoc> | ReDoc |
| <http://127.0.0.1:8000/api/v1/health> | Health check |

### Run the checks

```bash
pytest                # test suite
ruff check .          # lint + basic security checks
ruff format --check . # formatting
```

---

## Project structure

```
WhistleDrop/
├── app/
│   ├── main.py              # application factory
│   ├── core/                # config, security, dependencies, errors
│   ├── api/v1/routers/      # HTTP route handlers
│   ├── schemas/             # Pydantic request/response models   (Phase 2)
│   ├── services/            # business logic                     (Phase 2)
│   ├── repositories/        # database access                    (Phase 1)
│   ├── models/              # SQLAlchemy ORM models              (Phase 1)
│   └── ml/                  # triage inference                   (Phase 7)
├── ml/                      # offline training pipeline          (Phase 6)
├── tests/
├── docker-compose.yml
├── .env.example
└── requirements.txt
```

The layering is strictly one-directional:
**router → service → repository → model.**
Routers never touch the ORM; services never touch HTTP. This keeps business
rules testable without a web server and database rules testable without HTTP.

---

## Roadmap

- [x] **Phase 0** — Repository safety, scaffolding, config, health endpoint, Swagger
- [ ] **Phase 1** — SQLAlchemy models, enums, Alembic migrations, PostgreSQL
- [ ] **Phase 2** — Anonymous submission, case-code generation, case tracking
- [ ] **Phase 3** — Moderator authentication (JWT, seeded accounts)
- [ ] **Phase 4** — Moderation workflow, filtering, status transitions, audit trail
- [ ] **Phase 5** — Rate limiting, error handling, security hardening
- [ ] **Phase 6** — ML dataset and training pipeline (offline)
- [ ] **Phase 7** — ML integration into the API, moderator override capture
- [ ] **Phase 8** — Full test coverage, documentation, deployment, screenshots

---

## License

MIT
