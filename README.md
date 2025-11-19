# NSUT Internship/Placement Portal

## Database Management System Project

A simple, teacher-friendly Flask-based placement management system using MySQL for managing internship and placement activities at Netaji Subhas University of Technology (NSUT).

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Technology Stack](#technology-stack)
4. [Prerequisites](#prerequisites)
5. [Installation & Setup](#installation--setup)
6. [Running the Application](#running-the-application)
7. [Default Credentials](#default-credentials)
8. [Project Structure](#project-structure)
9. [Database Schema](#database-schema)
10. [Testing](#testing)
11. [Troubleshooting](#troubleshooting)

---

## Project Overview

This placement portal provides a centralized platform for:
- **Students** to browse jobs, apply, and track application status
- **Companies** to post job openings and review applications
- **Placement Cell Admins** to manage the entire placement process

---

## Features

### Student Features
- ✅ Self-registration with profile management
- ✅ Resume upload (PDF only, max 2MB)
- ✅ Browse and filter job postings by branch, CGPA, job type
- ✅ Apply to eligible jobs with automatic deadline enforcement
- ✅ Track application status (Applied → Shortlisted → Interview → Selected/Rejected)
- ✅ View and respond to interview invitations
- ✅ View placement cell announcements

### Company Features
- ✅ Admin-created company accounts
- ✅ Post job openings with eligibility criteria
- ✅ View and manage applications
- ✅ Update application status

### Placement Cell Admin Features
- ✅ Dashboard with statistics
- ✅ Create company accounts
- ✅ Approve/reject job postings
- ✅ Bulk import students via CSV
- ✅ Schedule interviews and send invitations
- ✅ Post announcements
- ✅ Monitor all placement activities

---

## Technology Stack

- **Backend:** Python 3.x + Flask (lightweight web framework)
- **Database:** MySQL (via XAMPP)
- **Frontend:** HTML5, CSS3, Bootstrap 5, Vanilla JavaScript
- **Database Connector:** mysql-connector-python (no ORM)
- **Authentication:** Flask sessions + bcrypt password hashing

---

## Prerequisites

Before you begin, ensure you have the following installed:

1. **XAMPP** (for Apache + MySQL)
   - Download from: https://www.apachefriends.org/
   - Or install MySQL separately

2. **Python 3.7+**
   - Download from: https://www.python.org/downloads/
   - Ensure `pip` is installed

3. **Git** (optional, for cloning)
   - Download from: https://git-scm.com/

---

## Installation & Setup

### Step 1: Install XAMPP and Start MySQL

#### Windows:
1. Download and install XAMPP
2. Open XAMPP Control Panel
3. Start **Apache** and **MySQL** services
4. Click **Admin** button next to MySQL to open phpMyAdmin

#### Linux/Mac:
```bash
sudo /opt/lampp/lampp start
```

### Step 2: Create Database

#### Method 1: Using phpMyAdmin (Recommended)
1. Open browser and go to `http://localhost/phpmyadmin`
2. Click "SQL" tab
3. Copy entire contents of `db/nsut_placement.sql`
4. Paste into SQL editor
5. Click "Go" to execute

#### Method 2: Using MySQL Command Line
```bash
# Windows (open Command Prompt)
cd C:\xampp\mysql\bin
mysql -u root -p

# Linux/Mac (open Terminal)
mysql -u root -p

# Then execute:
mysql> source /path/to/db/nsut_placement.sql;
mysql> exit;
```

**Note:** XAMPP's default MySQL root password is empty. If prompted for password, just press Enter.

### Step 3: Set Up Python Environment

#### Windows:
```cmd
# Navigate to project directory
cd path\to\nsut-placement-portal

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### Linux/Mac:
```bash
# Navigate to project directory
cd path/to/nsut-placement-portal

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` file (optional - default values work with XAMPP):
   ```
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=root
   DB_PASSWORD=
   DB_NAME=nsut_placement
   SECRET_KEY=your-secret-key-change-this
   ```

**Note:** For XAMPP, `DB_PASSWORD` is empty by default.

---

## Running the Application

### Step 1: Ensure MySQL is Running
- Open XAMPP Control Panel
- Verify MySQL service is running (green indicator)

### Step 2: Start Flask Application

#### Windows:
```cmd
# Make sure virtual environment is activated
venv\Scripts\activate

# Run the application
python app.py
```

#### Linux/Mac:
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Run the application
python app.py
```

**Or use the provided scripts:**

Windows:
```cmd
run_local.bat
```

Linux/Mac:
```bash
chmod +x run_local.sh
./run_local.sh
```

### Step 3: Access the Application

Open your web browser and navigate to:
```
http://localhost:5000
```

You should see the NSUT Placement Portal home page!

---

## Default Credentials

### Placement Cell Admin
- **Email:** admin@nsut.ac.in
- **Password:** admin123
- **Note:** Change this password after first login (update in database)

### Sample Students (from seed data)
- **Email:** rahul.sharma@nsut.ac.in
- **Password:** [See note below]

### Sample Companies (from seed data)
- Companies must be created by admin
- Passwords are auto-generated and displayed when created

**Important:** The seed SQL includes placeholder password hashes. You have two options:

1. **Register new accounts** through the application (recommended)
2. **Manually update passwords** in database:
   ```python
   from werkzeug.security import generate_password_hash
   print(generate_password_hash('your_password'))
   # Copy the output and update in database
   ```

---

## Project Structure

```
nsut-placement-portal/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── db.py                       # Database connection utilities
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .env                       # Environment variables (create this)
│
├── db/
│   ├── nsut_placement.sql     # Complete database schema + seed data
│
├── templates/                 # HTML templates (Jinja2)
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── student_*.html
│   ├── company_*.html
│   └── admin_*.html
│
├── static/
│   ├── images/
│   │   └── nsut_logo.png
│   ├── css/                   # (Optional custom CSS)
│   └── js/                    # (Optional custom JS)
│
├── uploads/                   # Resume storage (created automatically)
│
├── run_local.bat             # Windows run script
└── run_local.sh              # Linux/Mac run script
```

---

## Database Schema

The database consists of 8 main tables:

1. **students** - Student information and credentials
2. **companies** - Company/recruiter accounts
3. **pc_admins** - Placement cell administrators
4. **job_postings** - Job/internship postings
5. **applications** - Student applications to jobs
6. **interviews** - Interview schedules
7. **interview_invitations** - Student-interview mapping
8. **announcements** - Placement cell announcements

For detailed schema and relationships, see:
- `db/nsut_placement.sql` - Full SQL schema

---

## Testing

### Manual Testing

Follow the checklist in `MANUAL_TEST_CHECKLIST.md` to test all features.

### Quick Test Flow

1. **Login as Admin**
   - Email: admin@nsut.ac.in
   - Password: admin123

2. **Create a Company**
   - Go to Companies → Add New Company
   - Note the generated password

3. **Login as Company**
   - Logout and login with company credentials
   - Post a new job

4. **Approve Job (as Admin)**
   - Login as admin
   - Go to Jobs → Approve pending job

5. **Register as Student**
   - Logout and go to Student Signup
   - Register with year 3 or 4

6. **Apply to Job**
   - Login as student
   - Browse jobs and apply

7. **Update Application Status**
   - Login as company
   - View applications and update status

---

## Troubleshooting

### Database Connection Error

**Error:** `Database connection failed`

**Solutions:**
1. Ensure MySQL is running in XAMPP
2. Check `.env` file has correct database credentials
3. Verify database `nsut_placement` exists:
   ```sql
   mysql -u root -p
   SHOW DATABASES;
   ```

### Port Already in Use

**Error:** `Address already in use: 5000`

**Solution:**
1. Change port in `app.py`:
   ```python
   app.run(host='0.0.0.0', port=5001, debug=True)
   ```
2. Or kill process using port 5000

### Module Not Found

**Error:** `ModuleNotFoundError: No module named 'flask'`

**Solution:**
1. Ensure virtual environment is activated
2. Reinstall dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Password Hash Mismatch

**Error:** Cannot login with seed data credentials

**Solution:**
1. Register new accounts through the application
2. Or manually update password hashes in database:
   ```python
   from werkzeug.security import generate_password_hash
   hash = generate_password_hash('admin123')
   # Update in database: UPDATE pc_admins SET password_hash = '<hash>' WHERE id = 1;
   ```

### Resume Upload Fails

**Error:** File upload not working

**Solution:**
1. Ensure `uploads/` directory exists
2. Check file is PDF and under 2MB
3. Verify file permissions on `uploads/` folder

---

## Support

For issues or questions:
1. Check database logs in XAMPP
2. Review Flask console output for errors

---

## License

This project is created for educational purposes as a Database Management System project.

---

## Contributors

- NSUT Student : Shreshth (2024UCM2334) , Akshat Jain (2024UCM3327) , Prince Shah (2024UCM2348)
- DBMS Project - 2025

---

**Happy Placement Season! 🎓**
# NSUT_Placement_Portal
