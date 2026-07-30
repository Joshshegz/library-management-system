# LAUTECH Library Management System

Multimodal biometric library system (Windows Hello + nose landmarks) — Final Year Project.

**Authors:** Adesanwo Joshua Olusegun (2021000382) & Abubakar Abdullah Ishaq (2021002417)  
**Supervisor:** Prof. W. O. Ismaila

## Project setup (Django boilerplate)

```powershell
cd library-management-system-1

# Virtual environment (recommended — already created as ./venv)
.\venv\Scripts\Activate.ps1
# You should see (venv) in your prompt

pip install -r requirements.txt

# Already run once to create structure:
# django-admin startproject config .
# python manage.py startapp accounts
# python manage.py startapp catalog
# python manage.py startapp circulation
# python manage.py startapp biometrics

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Admin: http://127.0.0.1:8000/admin/

## Biometrics & circulation

1. Register → **Complete biometric enrolment** at `/biometrics/enroll/` (Step 1: Windows Hello, Step 2: nose capture)
2. Sign in with password or **Windows Hello** at `/biometrics/login/`
3. **Borrow / return** books — webcam nose verification on each transaction

**Important:** Open the site as **http://localhost:8000** (not `127.0.0.1`) — Windows Hello rejects IP addresses as invalid domain.

```powershell
python manage.py migrate
python manage.py runserver
```

Run `python manage.py evaluate_biometrics` to benchmark enrolled templates (accuracy, FPR, sensitivity, average match time).

## Apps

| App | Role |
|-----|------|
| `accounts` | Users, roles, matric numbers |
| `catalog` | Books and inventory |
| `circulation` | Borrow / return (nose verification) |
| `biometrics` | Windows Hello + nose enrollment & matching |

## Seed data

```powershell
python manage.py populate_cs_books   # seed catalog books
python scripts/seed_data.py          # seed users and loans
```
