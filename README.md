# 🧑‍💻 Job Board Backend – ProDev BE Capstone

## 📌 Overview
The **Job Board Backend** is a scalable and secure RESTful API designed for managing job postings, categories, and applications.  
It was developed as part of the **ProDev Backend Engineering Program (Capstone Project)**, with a strong focus on **clean architecture, authentication, and industry best practices**.  

This backend enables employers to post jobs and candidates to browse, apply, and manage opportunities efficiently.

---

## 🎯 Core Objectives
- **Job Management** → CRUD operations for job postings and categories.  
- **User Roles** → Admins manage postings; users apply and save jobs.  
- **Security** → JWT authentication with role-based access control (RBAC).  
- **Search & Filter** → Optimized queries by categories, locations, and job types.  
- **Documentation** → Interactive API documentation with Swagger/OpenAPI.  

---

## 🛠️ Tech Stack

| Technology       | Purpose |
|------------------|---------|
| **Django & DRF** | Backend framework & RESTful API design |
| **PostgreSQL**   | Relational database |
| **JWT (SimpleJWT)** | Authentication & authorization |
| **Swagger (drf-yasg)** | Interactive API documentation |
| **pytest / DRF Test** | Automated testing |
| **Gunicorn + Whitenoise** | Deployment-ready stack |

---

## 🔑 Features

### 📂 Job Posting & Categories
- CRUD operations for jobs and categories.  
- Organize jobs by **category, location, and employment type**.  

### 🔒 Authentication & Permissions
- **Admins** → Manage jobs & categories.  
- **Users** → Apply for jobs, manage favorites, and view applications.  
- JWT tokens with refresh & expiration.  

### ⚡ Optimized Job Search
- Filter jobs by **category, location, type**.  
- Indexed queries for performance on large datasets.  

### 📑 API Documentation
- Swagger/OpenAPI available at `/api/docs/`.  
- DRF browsable API included.  

### 🧪 Testing
- Automated tests for:
  - Authentication  
  - Job CRUD endpoints  
  - Role-based access  
  - Filtering & search  

---

## ⚙️ Setup & Installation

```bash
# Clone repository
git clone https://github.com/your-username/jobboard-backend.git
cd jobboard-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Run development server
python manage.py runserver
