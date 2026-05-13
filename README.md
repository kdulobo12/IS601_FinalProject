# IS601 Final Project — Calculations API

A full-stack web application built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL** that provides a secure calculator with BREAD operations (Browse, Read, Edit, Add, Delete) and a complete **User Profile & Password Change** feature.

---

## Table of Contents

1. [Features](#features)
2. [Tech Stack](#tech-stack)
3. [Getting Started](#getting-started)
4. [Running Tests](#running-tests)
5. [Docker Hub](#docker-hub)
6. [CI/CD Pipeline](#cicd-pipeline)
7. [API Reference](#api-reference)
8. [Final Project Feature: User Profile & Password Change](#final-project-feature)
9. [Security](#security)
10. [Reflection](#reflection)

---

## Features

### Core (BREAD Operations)
- **Browse** — list all calculations for the authenticated user
- **Read** — view a single calculation in detail
- **Edit** — update inputs and recalculate result
- **Add** — create a new calculation (addition, subtraction, multiplication, division)
- **Delete** — remove a calculation

### Final Project Feature: User Profile & Password Change
- View and update profile info (first name, last name, username, email)
- Change password with current-password verification
- Full client-side and server-side validation
- Secure bcrypt password hashing
- Profile nav link appears in the header when logged in
- Force re-login after successful password change for security

### Authentication & Security
- JWT access + refresh tokens
- bcrypt password hashing
- Password strength enforcement (uppercase, lowercase, digit, special character, min 8 chars)
- Protected routes via OAuth2 Bearer tokens

---

## Tech Stack

| Layer      | Technology                         |
|------------|-------------------------------------|
| Backend    | FastAPI, SQLAlchemy, Pydantic v2   |
| Database   | PostgreSQL 17                       |
| Auth       | JWT (python-jose), passlib/bcrypt  |
| Frontend   | Jinja2 templates, Tailwind CSS      |
| Testing    | pytest, Playwright (E2E)            |
| Container  | Docker, Docker Compose              |
| CI/CD      | GitHub Actions                      |

---

## Getting Started

### Prerequisites
- Docker & Docker Compose
- Python 3.11+ (for local development)

### Run with Docker Compose

```bash
git clone <your-repo-url>
cd IS601_FinalProject

# Start all services (app + PostgreSQL + pgAdmin)
docker compose up --build
```

The app will be available at: **http://localhost:8000**

pgAdmin is available at: **http://localhost:5050**
- Email: `admin@example.com`
- Password: `admin`

### Run Locally (without Docker)

```bash
# 1. Create a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set environment variables (create a .env file)
cat > .env << EOF
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/fastapi_db
TEST_DATABASE_URL=postgresql://postgres:postgres@localhost:5432/fastapi_test_db
JWT_SECRET_KEY=your-secret-key-minimum-32-characters
JWT_REFRESH_SECRET_KEY=your-refresh-secret-key-minimum-32-characters
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
BCRYPT_ROUNDS=12
EOF

# 4. Start a local PostgreSQL instance, then run:
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## Running Tests

### Run all tests locally

```bash
# Make sure the app environment variables are set (see above)

# All tests
pytest tests/ -v

# Unit tests only
pytest tests/unit/ -v

# Integration tests only
pytest tests/integration/ -v

# E2E tests only (requires a running server — conftest.py starts one automatically)
pytest tests/e2e/ -v

# With coverage report
pytest tests/ --cov=app --cov-report=html
# Open htmlcov/index.html in a browser
```

### Run tests with Docker

```bash
docker compose run web pytest tests/ -v
```

### Test Categories

| Category    | Location                         | What it tests                                      |
|-------------|-----------------------------------|----------------------------------------------------|
| Unit        | `tests/unit/`                    | Calculator logic, schema validation, password hashing |
| Integration | `tests/integration/`             | FastAPI routes + real DB interactions              |
| E2E         | `tests/e2e/`                     | Full browser flows using Playwright                |

---

## Docker Hub

The Docker image is published to Docker Hub on every successful push to `main`.

**Repository:** `https://hub.docker.com/r/<your-dockerhub-username>/is601-final-project`

### Pull and run the image

```bash
docker pull <your-dockerhub-username>/is601-final-project:latest

docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://postgres:postgres@host.docker.internal:5432/fastapi_db \
  -e JWT_SECRET_KEY=your-secret-key-minimum-32-characters \
  -e JWT_REFRESH_SECRET_KEY=your-refresh-secret-key-minimum-32-chars \
  <your-dockerhub-username>/is601-final-project:latest
```

---

## CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/ci.yml`) runs on every push and pull request to `main`:

1. **Spin up PostgreSQL** service container
2. **Install Python 3.11** and all dependencies
3. **Install Playwright** browsers for E2E tests
4. **Run unit tests** → fail fast if any unit test breaks
5. **Run integration tests** → validates all API routes
6. **Run E2E tests** → validates full browser workflows
7. **Build Docker image** (only on passing tests on `main` branch)
8. **Push to Docker Hub** with `latest` and `sha-<commit>` tags

### Required GitHub Secrets

| Secret                  | Description                      |
|-------------------------|----------------------------------|
| `DOCKERHUB_USERNAME`    | Your Docker Hub username         |
| `DOCKERHUB_TOKEN`       | Docker Hub access token (not password) |

---

## API Reference

All routes requiring authentication need the `Authorization: Bearer <token>` header.

### Auth

| Method | Route             | Description              |
|--------|-------------------|--------------------------|
| POST   | `/auth/register`  | Register a new user      |
| POST   | `/auth/login`     | Login, get JWT tokens    |
| POST   | `/auth/token`     | OAuth2 form-based login  |

### Calculations

| Method | Route                      | Description                        |
|--------|----------------------------|------------------------------------|
| POST   | `/calculations`            | Create a new calculation           |
| GET    | `/calculations`            | List all user's calculations       |
| GET    | `/calculations/{id}`       | Get a single calculation           |
| PUT    | `/calculations/{id}`       | Update a calculation               |
| DELETE | `/calculations/{id}`       | Delete a calculation               |

### User Profile (New Feature)

| Method | Route                  | Description                         |
|--------|------------------------|-------------------------------------|
| GET    | `/users/me`            | Get current user's profile          |
| PUT    | `/users/me`            | Update profile (name, email, etc.)  |
| PUT    | `/users/me/password`   | Change password                     |
| GET    | `/profile`             | Profile page (HTML)                 |

---

## Final Project Feature

### User Profile & Password Change

**What was implemented:**

#### Backend
- `GET /users/me` — returns the authenticated user's full profile from the database
- `PUT /users/me` — updates first name, last name, username, and/or email with uniqueness checks
- `PUT /users/me/password` — verifies current password, validates new password strength, hashes and saves the new password

#### Pydantic Schemas
- `UserUpdate` — optional fields, email validation via `EmailStr`
- `PasswordUpdate` — validators ensure passwords match and new ≠ old

#### Frontend
- `/profile` page with two forms: **Profile Information** and **Change Password**
- Profile fields auto-populate from `GET /users/me` on page load
- Client-side validation (empty fields, email format, password strength, mismatch indicator)
- Success/error alert banners
- Forces re-login after password change for security

#### Tests Written
- **Unit** (`tests/unit/test_profile_logic.py`): 19 tests covering schema validation, password hashing, and User.update()
- **Integration** (`tests/integration/test_profile.py`): 16 tests covering all three API endpoints including negative cases
- **E2E** (`tests/e2e/test_profile_e2e.py`): 14 Playwright tests covering navigation, form filling, validation errors, and the full login→profile→password change→re-login flow

---

## Security

- **Passwords**: hashed with bcrypt (configurable rounds via `BCRYPT_ROUNDS`)
- **Password strength**: enforced at both schema and route level (8+ chars, upper, lower, digit, special)
- **JWT**: short-lived access tokens (default 30 min) + refresh tokens
- **Re-login on password change**: tokens invalidated by redirecting to login after password change
- **Uniqueness checks**: email and username conflicts return 400, not 500
- **Cascade deletes**: calculations deleted when a user is deleted

---

## Reflection

Building this project deepened my understanding of how FastAPI, SQLAlchemy, and Pydantic work together to create a robust, type-safe backend. The most challenging part was ensuring proper test isolation — each integration test registers a fresh user so tests don't interfere with each other.

The User Profile feature required touching every layer of the stack: new Pydantic schemas for validation, new FastAPI routes with proper auth dependencies, a Jinja2 template with JavaScript for API calls, and three tiers of tests. This end-to-end ownership of a feature gave me a clear picture of how real-world web apps are structured.

The CI/CD pipeline with GitHub Actions was especially valuable — catching bugs automatically on every push means broken code never reaches production. Using Docker for both development and deployment ensures consistent behaviour across environments.
