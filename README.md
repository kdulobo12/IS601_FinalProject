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

<img width="2468" height="312" alt="image" src="https://github.com/user-attachments/assets/768ffbcb-6004-46c1-9a14-d2544844f367" />

- Docker Hub deployment
  <img width="452" height="260" alt="image" src="https://github.com/user-attachments/assets/601e9cd6-9eb9-4e27-b468-227fc815357a" />
  
- User registration/login
<img width="3350" height="1870" alt="image" src="https://github.com/user-attachments/assets/102baf76-d3a0-4605-9159-2a3141ada75d" />

- Add calculation
<img width="2542" height="670" alt="image" src="https://github.com/user-attachments/assets/9b7212a8-dab4-41a5-8ca3-93b4dda1b496" />


- Browse calculations
<img width="3048" height="1020" alt="image" src="https://github.com/user-attachments/assets/b5e4a9de-7b56-4717-bbdf-bdc28ee0afee" />

- Edit calculation

<img width="1230" height="681" alt="Screenshot 2026-05-13 at 19 48 17" src="https://github.com/user-attachments/assets/fe03f5ad-60a9-45ec-8aef-825a3badd1a6" />


<img width="3360" height="2100" alt="image" src="https://github.com/user-attachments/assets/8713cbc0-9d38-43cf-aa01-318b5540322b" />

- Delete calculation
<img width="3360" height="2100" alt="image" src="https://github.com/user-attachments/assets/61bae754-40dd-4862-8335-ec778a627766" />

- User profile page

<img width="3292" height="1060" alt="image" src="https://github.com/user-attachments/assets/e8f01ae4-a973-4103-9bd9-f88986c37cf9" />

- Password change workflow

<img width="2104" height="904" alt="image" src="https://github.com/user-attachments/assets/3079f60a-94ed-476e-89b5-42ccaa559622" />

<img width="3360" height="2100" alt="image" src="https://github.com/user-attachments/assets/7ad2c8f2-03fb-49d6-9707-da9173ea4dab" />

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

