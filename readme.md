# FastAPI + SQLite + Alembic Boilerplate

A simple **FastAPI** application connected to a **SQLite** database using **SQLAlchemy ORM** and **Alembic** for database migrations.

---

## Features
- **FastAPI** for high-performance REST APIs
- **SQLite** lightweight database (local development)
- **SQLAlchemy ORM** for models & relationships
- **Alembic** for database migrations
- Modular project structure (models, routers, services)

---

## Project Structure
```
├─ app/
│  ├─ core/        # Database & settings
│  ├─ models/      # SQLAlchemy models (Doctor, Patient, Department, etc.)
│  ├─ routers/     # API endpoints
│  ├─ schemas/     # Pydantic schemas (request/response models)
│  ├─ services/    # Business logic & service layer
│  └─ main.py      # FastAPI entry point
├─ alembic/        # Migration scripts
├─ patients.db     # SQLite database (ignored by git)
├─ alembic.ini
├─ requirements.txt
└─ README.md
```

---

## Installation & Setup
### Clone the repository 

``` bash
git clone https://github.com/Zohaib-farooq-dev/CG_Internship_fastapi_backend.git

```
### Create and Activate Virtual Environment

```
python -m venv env
# Windows
env\Scripts\activate
# Linux / macOS
source env/bin/activate
```

### Install Dependencies 
```
pip install -r requirements.txt
```
### Create .env file
Create .env file in root directory of your project with the following content. 
```
DATABASE_URL=sqlite:///./patient_management.db
```
Make sure this url is exactly the path of file where you want to save your database. If you use a **different database (e.g. PostgreSQL, MySQL) → update .env with the appropriate database URL** and make sure the respective DBMS is installed and running.

### Database Migrations 
Initialize Database
```
alembic upgrade head
```
This command will generate the **same database** with tables at your system. If you want to change any table, change in particular models and run the follwoing command
and generate migrations 
```
alembic revision --autogenerate -m "Create/Alter table"
```
### Run the application
```
uvicorn app.main:app --reload
```
After running the application, visit at following url to explore Swagger UI.
```
http://127.0.0.1:8000/docs
```