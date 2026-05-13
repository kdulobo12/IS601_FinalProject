# 🧮 IS601 Final Project – FastAPI Calculations Application

## 📌 Project Description

This project is a full-stack FastAPI web application that implements secure BREAD (Browse, Read, Edit, Add, Delete) functionality for user-specific calculations along with a complete User Profile & Password Change feature.

Each authenticated user can:

- ➕ Add new calculations
- 📋 Browse saved calculations
- 🔍 Read individual calculation details
- ✏️ Edit calculations
- ❌ Delete calculations
- 👤 Update profile information
- 🔐 Change passwords securely

The project also includes:

- PostgreSQL database integration
- JWT authentication
- Password hashing with bcrypt
- Pytest testing
- Playwright E2E testing
- Docker containerization
- GitHub Actions CI/CD pipeline
- Docker Hub deployment

---

# 🚀 Features

## 🧮 Calculator Features
- ➕ Addition
- ➖ Subtraction
- ✖️ Multiplication
- ➗ Division
- 📋 Browse all calculations
- 🔍 Read individual calculation
- ✏️ Edit calculations
- ❌ Delete calculations

## 👤 User Profile & Password Change
- Update first name and last name
- Update username and email
- Change password securely
- Password validation and hashing
- Auto logout after password change
- Protected profile routes

## 🔐 Authentication & Security
- JWT authentication
- Secure password hashing with bcrypt
- Protected API routes
- Input validation with Pydantic
- Password strength enforcement

## 🧪 Testing
- Unit tests
- Integration tests
- End-to-End Playwright tests

## ⚙️ DevOps
- Dockerized application
- PostgreSQL + pgAdmin containers
- GitHub Actions CI/CD pipeline
- Docker Hub image deployment

---

# 🛠️ Tech Stack

| Layer | Technology |
|------|-------------|
| Backend | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Validation | Pydantic |
| Authentication | JWT |
| Frontend | HTML, Tailwind CSS, JavaScript |
| Testing | Pytest, Playwright |
| Containerization | Docker |
| CI/CD | GitHub Actions |

---

# ▶️ Running the Application Locally

## 1. Clone Repository

```bash
git clone https://github.com/kdulobo12/IS601_FinalProject.git
cd IS601_FinalProject
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Start Application

```bash
uvicorn app.main:app --reload
```

Application runs at:

```text
http://localhost:8000
```

---

# 🐳 Running with Docker

## Build Containers

```bash
docker compose build --no-cache
```

## Start Containers

```bash
docker compose up -d
```

Application:

```text
http://localhost:8000
```

pgAdmin:

```text
http://localhost:5050
```

---

# 🧪 Running Tests

## Run All Tests

```bash
pytest tests/ -v
```

## Run Unit Tests

```bash
pytest tests/unit -v
```

## Run Integration Tests

```bash
pytest tests/integration -v
```

## Run E2E Tests

```bash
pytest tests/e2e -v
```

---

# 🔄 CI/CD Pipeline

This project uses GitHub Actions to:

- ✅ Run automated tests
- ✅ Build Docker image
- ✅ Install Playwright browsers
- ✅ Push Docker image to Docker Hub
- ✅ Validate application before deployment

---

# 🐳 Docker Hub Repository

👉 https://hub.docker.com/r/kdulobo12/is601_finalproject

---

# 📸 Screenshots Included

- GitHub Actions successful workflow
- Docker Hub deployment
- User registration/login
- Add calculation
- Browse calculations
- Edit calculation
- Delete calculation
- User profile page
- Password change workflow

---

# 🔐 Security Features

- JWT authentication
- bcrypt password hashing
- Password validation
- Protected routes
- Token-based authorization
- Secure profile updates

---

# 📚 Learning Outcomes

This project demonstrates:

- Building REST APIs with FastAPI
- Integrating PostgreSQL with SQLAlchemy
- Using JWT authentication
- Secure password hashing
- Writing automated tests
- Using Playwright for E2E testing
- Containerizing applications with Docker
- Setting up CI/CD pipelines
- Deploying images to Docker Hub

---

## Reflection

Building this project deepened my understanding of how FastAPI, SQLAlchemy, and Pydantic work together to create a robust, type-safe backend. The most challenging part was ensuring proper test isolation — each integration test registers a fresh user so tests don't interfere with each other.

The User Profile feature required touching every layer of the stack: new Pydantic schemas for validation, new FastAPI routes with proper auth dependencies, a Jinja2 template with JavaScript for API calls, and three tiers of tests. This end-to-end ownership of a feature gave me a clear picture of how real-world web apps are structured.

The CI/CD pipeline with GitHub Actions was especially valuable — catching bugs automatically on every push means broken code never reaches production. Using Docker for both development and deployment ensures consistent behaviour across environments.

# 👩‍💻 Author

Krupa Dulobo

