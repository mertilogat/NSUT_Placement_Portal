"""
NSUT Internship/Placement Portal - Main Application
A simple Flask-based placement management system using MySQL
Database Management System Project
"""

import os
import secrets
import string
from datetime import datetime, timedelta
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
import csv
from io import StringIO

from config import Config
from db import execute_query, get_by_id, get_all, test_connection

# Initialize Flask application
app = Flask(__name__)
app.config.from_object(Config)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# ============================================
# HELPER FUNCTIONS
# ============================================

def allowed_file(filename):
    """Check if uploaded file has allowed extension (PDF only)"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


def generate_random_password(length=10):
    """Generate a random password for auto-created accounts"""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))


def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Decorator to require admin login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            flash('Admin access required', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def company_required(f):
    """Decorator to require company login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'company':
            flash('Company access required', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def student_required(f):
    """Decorator to require student login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'student':
            flash('Student access required', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# ============================================
# PUBLIC ROUTES
# ============================================

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Universal login page for all user types"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user_type = request.form.get('user_type')  # student, company, admin
        
        if not all([email, password, user_type]):
            flash('All fields are required', 'danger')
            return redirect(url_for('login'))
        
        # Determine which table to check based on user type
        if user_type == 'student':
            query = "SELECT * FROM students WHERE email = %s"
        elif user_type == 'company':
            query = "SELECT * FROM companies WHERE email = %s"
        elif user_type == 'admin':
            query = "SELECT * FROM pc_admins WHERE email = %s"
        else:
            flash('Invalid user type', 'danger')
            return redirect(url_for('login'))
        
        user = execute_query(query, (email,), fetch_one=True)
        
        if user and check_password_hash(user['password_hash'], password):
            # Check if company account is activated
            if user_type == 'company' and not user.get('is_active'):
                flash('Your account is pending admin approval', 'warning')
                return redirect(url_for('login'))
            
            # Set session variables
            session['user_id'] = user['id']
            session['email'] = user['email']
            session['role'] = user_type
            
            if user_type == 'student':
                session['name'] = user['name']
                flash(f'Welcome, {user["name"]}!', 'success')
                return redirect(url_for('student_dashboard'))
            elif user_type == 'company':
                session['name'] = user['company_name']
                flash(f'Welcome, {user["company_name"]}!', 'success')
                return redirect(url_for('company_dashboard'))
            else:  # admin
                session['name'] = user['name']
                flash(f'Welcome, Admin {user["name"]}!', 'success')
                return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid email or password', 'danger')
            return redirect(url_for('login'))
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    flash('You have been logged out successfully', 'info')
    return redirect(url_for('index'))


@app.route('/student/signup', methods=['GET', 'POST'])
def student_signup():
    """Student registration page"""
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        roll_no = request.form.get('roll_no')
        email = request.form.get('email')
        password = request.form.get('password')
        branch = request.form.get('branch')
        year = int(request.form.get('year'))
        cgpa = float(request.form.get('cgpa'))
        phone = request.form.get('phone')
        skills = request.form.get('skills')
        
        # Validate year (only 3 and 4 allowed)
        if year not in Config.ELIGIBLE_YEARS:
            flash('Only year 3 and 4 students are eligible', 'danger')
            return redirect(url_for('student_signup'))
        
        # Check if email or roll number already exists
        existing_email = execute_query(
            "SELECT id FROM students WHERE email = %s",
            (email,),
            fetch_one=True
        )
        existing_roll = execute_query(
            "SELECT id FROM students WHERE roll_no = %s",
            (roll_no,),
            fetch_one=True
        )
        
        if existing_email:
            flash('Email already registered', 'danger')
            return redirect(url_for('student_signup'))
        
        if existing_roll:
            flash('Roll number already registered', 'danger')
            return redirect(url_for('student_signup'))
        
        # Hash password
        password_hash = generate_password_hash(password)
        
        # Insert student into database
        query = """
            INSERT INTO students 
            (name, roll_no, email, password_hash, branch, year, cgpa, phone, skills_text)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (name, roll_no, email, password_hash, branch, year, cgpa, phone, skills)
        
        result = execute_query(query, params)
        
        if result:
            flash('Registration successful! Please login', 'success')
            return redirect(url_for('login'))
        else:
            flash('Registration failed. Please try again', 'danger')
            return redirect(url_for('student_signup'))
    
    return render_template('student_signup.html', 
                          branches=Config.BRANCHES,
                          years=Config.ELIGIBLE_YEARS)


# ============================================
# STUDENT ROUTES
# ============================================

@app.route('/student/dashboard')
@student_required
def student_dashboard():
    """Student dashboard showing available jobs and applications"""
    student_id = session['user_id']
    
    # Get student info
    student = get_by_id('students', student_id)
    
    # Get student's applications with job details
    query = """
        SELECT a.*, jp.title, jp.job_type, jp.deadline, c.company_name, jp.status as job_status
        FROM applications a
        JOIN job_postings jp ON a.job_id = jp.id
        JOIN companies c ON jp.company_id = c.id
        WHERE a.student_id = %s
        ORDER BY a.applied_at DESC
    """
    applications = execute_query(query, (student_id,), fetch=True)
    
    # Get recent announcements
    announcements_query = """
        SELECT * FROM announcements
        ORDER BY created_at DESC
        LIMIT 5
    """
    announcements = execute_query(announcements_query, fetch=True)
    
    # Get interview invitations
    interview_query = """
        SELECT ii.*, i.interview_date, i.interview_time, i.location, i.meeting_link,
               jp.title, c.company_name
        FROM interview_invitations ii
        JOIN interviews i ON ii.interview_id = i.id
        JOIN job_postings jp ON i.job_id = jp.id
        JOIN companies c ON jp.company_id = c.id
        WHERE ii.student_id = %s
        ORDER BY i.interview_date ASC
    """
    interviews = execute_query(interview_query, (student_id,), fetch=True)
    
    return render_template('student_dashboard.html',
                          student=student,
                          applications=applications or [],
                          announcements=announcements or [],
                          interviews=interviews or [])


@app.route('/student/profile', methods=['GET', 'POST'])
@student_required
def student_profile():
    """Student profile management"""
    student_id = session['user_id']
    student = get_by_id('students', student_id)
    
    if request.method == 'POST':
        # Update profile
        phone = request.form.get('phone')
        skills = request.form.get('skills')
        cgpa = float(request.form.get('cgpa'))
        
        # Handle resume upload
        resume_filename = student['resume_filename']
        if 'resume' in request.files:
            file = request.files['resume']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(f"{student['roll_no']}_{file.filename}")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                resume_filename = filename
        
        # Update database
        query = """
            UPDATE students
            SET phone = %s, skills_text = %s, cgpa = %s, resume_filename = %s
            WHERE id = %s
        """
        execute_query(query, (phone, skills, cgpa, resume_filename, student_id))
        
        flash('Profile updated successfully', 'success')
        return redirect(url_for('student_profile'))
    
    return render_template('student_profile.html', student=student)


@app.route('/student/jobs')
@student_required
def student_jobs():
    """Browse available jobs with filters using normalized eligibility tables"""
    student_id = session['user_id']
    student = get_by_id('students', student_id)
    
    # Get filter parameters
    search = request.args.get('search', '')
    branch_filter = request.args.get('branch', '')
    job_type_filter = request.args.get('job_type', '')
    
    # Base query using JOINs with normalized junction tables
    # Show jobs matching student's eligibility (year, CGPA, branch)
    query = """
        SELECT DISTINCT jp.*, c.company_name,
               GROUP_CONCAT(DISTINCT jab_all.branch ORDER BY jab_all.branch) as allowed_branches_list,
               (SELECT COUNT(*) FROM applications WHERE job_id = jp.id) as total_applications,
               (SELECT COUNT(*) FROM applications WHERE job_id = jp.id AND student_id = %s) as already_applied
        FROM job_postings jp
        JOIN companies c ON jp.company_id = c.id
        JOIN job_allowed_years jay ON jp.id = jay.job_id
        JOIN job_allowed_branches jab_all ON jp.id = jab_all.job_id
        WHERE jp.status = 'Approved'
          AND jp.deadline >= CURDATE()
          AND jay.year = %s
          AND jp.min_cgpa <= %s
          AND EXISTS (
              SELECT 1 FROM job_allowed_branches jab_student
              WHERE jab_student.job_id = jp.id
              AND jab_student.branch = %s
          )
    """
    params = [student_id, student['year'], student['cgpa'], student['branch']]
    
    # Override with specific branch filter if user explicitly selects one
    if branch_filter:
        # Replace the EXISTS clause with explicit branch filter
        query = query.replace(
            "AND jab_student.branch = %s",
            "AND jab_student.branch = %s"
        )
        params[-1] = branch_filter  # Replace last param (student branch) with filter
    
    # Add search filter
    if search:
        query += " AND (jp.title LIKE %s OR c.company_name LIKE %s)"
        params.extend([f'%{search}%', f'%{search}%'])
    
    # Add job type filter
    if job_type_filter:
        query += " AND (jp.job_type = %s OR jp.job_type = 'Both')"
        params.append(job_type_filter)
    
    # Group by job_id since we're using GROUP_CONCAT for branches
    query += " GROUP BY jp.id ORDER BY jp.deadline ASC"
    
    jobs = execute_query(query, tuple(params), fetch=True)
    
    return render_template('student_jobs.html',
                          jobs=jobs or [],
                          student=student,
                          search=search,
                          branch_filter=branch_filter,
                          job_type_filter=job_type_filter,
                          branches=Config.BRANCHES,
                          job_types=Config.JOB_TYPES)


@app.route('/student/apply/<int:job_id>', methods=['POST'])
@student_required
def apply_job(job_id):
    """Apply to a job"""
    student_id = session['user_id']
    student = get_by_id('students', student_id)
    job = get_by_id('job_postings', job_id)
    
    if not job:
        flash('Job not found', 'danger')
        return redirect(url_for('student_jobs'))
    
    # Check deadline
    if job['deadline'] < datetime.now().date():
        flash('Application deadline has passed', 'danger')
        return redirect(url_for('student_jobs'))
    
    # Check if already applied
    existing_app = execute_query(
        "SELECT id FROM applications WHERE student_id = %s AND job_id = %s",
        (student_id, job_id),
        fetch_one=True
    )
    
    if existing_app:
        flash('You have already applied to this job', 'warning')
        return redirect(url_for('student_jobs'))
    
    # Check if resume uploaded
    if not student['resume_filename']:
        flash('Please upload your resume before applying', 'warning')
        return redirect(url_for('student_profile'))
    
    # Check branch eligibility using normalized junction table
    branch_eligible = execute_query(
        "SELECT 1 FROM job_allowed_branches WHERE job_id = %s AND branch = %s",
        (job_id, student['branch']),
        fetch_one=True
    )
    
    if not branch_eligible:
        flash('You are not eligible for this job (branch mismatch)', 'danger')
        return redirect(url_for('student_jobs'))
    
    # Check year eligibility
    year_eligible = execute_query(
        "SELECT 1 FROM job_allowed_years WHERE job_id = %s AND year = %s",
        (job_id, student['year']),
        fetch_one=True
    )
    
    if not year_eligible:
        flash('You are not eligible for this job (year mismatch)', 'danger')
        return redirect(url_for('student_jobs'))
    
    # Check CGPA eligibility
    if student['cgpa'] < job['min_cgpa']:
        flash(f'You are not eligible for this job (minimum CGPA: {job["min_cgpa"]})', 'danger')
        return redirect(url_for('student_jobs'))
    
    # Create application
    query = "INSERT INTO applications (student_id, job_id) VALUES (%s, %s)"
    result = execute_query(query, (student_id, job_id))
    
    if result:
        flash('Application submitted successfully!', 'success')
    else:
        flash('Application failed. Please try again', 'danger')
    
    return redirect(url_for('student_jobs'))


@app.route('/student/interview/<int:invitation_id>/<action>')
@student_required
def respond_interview(invitation_id, action):
    """Accept or decline interview invitation"""
    if action not in ['accept', 'decline']:
        flash('Invalid action', 'danger')
        return redirect(url_for('student_dashboard'))
    
    status = 'Accepted' if action == 'accept' else 'Declined'
    
    query = """
        UPDATE interview_invitations
        SET status = %s
        WHERE id = %s AND student_id = %s
    """
    execute_query(query, (status, invitation_id, session['user_id']))
    
    flash(f'Interview invitation {action}ed successfully', 'success')
    return redirect(url_for('student_dashboard'))


# ============================================
# COMPANY ROUTES
# ============================================

@app.route('/company/dashboard')
@company_required
def company_dashboard():
    """Company dashboard"""
    company_id = session['user_id']
    
    # Get company info
    company = get_by_id('companies', company_id)
    
    # Get company's job postings with application count
    query = """
        SELECT jp.*,
               (SELECT COUNT(*) FROM applications WHERE job_id = jp.id) as total_applications,
               (SELECT COUNT(*) FROM applications WHERE job_id = jp.id AND application_status = 'Selected') as selected_count
        FROM job_postings jp
        WHERE jp.company_id = %s
        ORDER BY jp.created_at DESC
    """
    jobs = execute_query(query, (company_id,), fetch=True)
    
    return render_template('company_dashboard.html',
                          company=company,
                          jobs=jobs or [])


@app.route('/company/job/new', methods=['GET', 'POST'])
@company_required
def company_new_job():
    """Create new job posting with normalized eligibility and transaction safety"""
    if request.method == 'POST':
        company_id = session['user_id']
        
        title = request.form.get('title')
        description = request.form.get('description')
        job_type = request.form.get('job_type')
        min_cgpa = float(request.form.get('min_cgpa'))
        branches_list = request.form.getlist('branches')
        years_list = request.form.getlist('years')
        deadline = request.form.get('deadline')
        num_openings = int(request.form.get('num_openings'))
        
        # Validate
        if not all([title, description, job_type, branches_list, years_list, deadline, num_openings]):
            flash('All fields are required', 'danger')
            return redirect(url_for('company_new_job'))
        
        # Use transaction for atomic job creation with eligibility
        from db import get_db_connection
        connection = get_db_connection()
        if not connection:
            flash('Database connection error', 'danger')
            return redirect(url_for('company_new_job'))
        
        try:
            cursor = connection.cursor()
            
            # Insert job posting
            query = """
                INSERT INTO job_postings
                (company_id, title, description, job_type, min_cgpa, deadline, num_openings, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 'Pending')
            """
            params = (company_id, title, description, job_type, min_cgpa, deadline, num_openings)
            cursor.execute(query, params)
            job_id = cursor.lastrowid
            
            # Insert into junction tables for branches
            for branch in branches_list:
                cursor.execute(
                    "INSERT INTO job_allowed_branches (job_id, branch) VALUES (%s, %s)",
                    (job_id, branch)
                )
            
            # Insert into junction tables for years
            for year in years_list:
                cursor.execute(
                    "INSERT INTO job_allowed_years (job_id, year) VALUES (%s, %s)",
                    (job_id, int(year))
                )
            
            # Commit transaction
            connection.commit()
            cursor.close()
            connection.close()
            
            flash('Job posted successfully! Waiting for admin approval', 'success')
            return redirect(url_for('company_dashboard'))
            
        except Exception as e:
            # Rollback on error
            connection.rollback()
            cursor.close()
            connection.close()
            print(f"Job creation error: {e}")
            flash('Job posting failed. Please try again', 'danger')
            return redirect(url_for('company_new_job'))
    
    return render_template('company_new_job.html',
                          branches=Config.BRANCHES,
                          years=Config.ELIGIBLE_YEARS,
                          job_types=Config.JOB_TYPES)


@app.route('/company/job/<int:job_id>/applications')
@company_required
def company_job_applications(job_id):
    """View applications for a specific job"""
    company_id = session['user_id']
    
    # Verify job belongs to this company
    job = execute_query(
        "SELECT * FROM job_postings WHERE id = %s AND company_id = %s",
        (job_id, company_id),
        fetch_one=True
    )
    
    if not job:
        flash('Job not found', 'danger')
        return redirect(url_for('company_dashboard'))
    
    # Get applications with student details
    query = """
        SELECT a.*, s.name, s.roll_no, s.email, s.branch, s.year, s.cgpa,
               s.phone, s.skills_text, s.resume_filename
        FROM applications a
        JOIN students s ON a.student_id = s.id
        WHERE a.job_id = %s
        ORDER BY a.applied_at DESC
    """
    applications = execute_query(query, (job_id,), fetch=True)
    
    return render_template('company_applications.html',
                          job=job,
                          applications=applications or [],
                          statuses=Config.APPLICATION_STATUSES)


@app.route('/company/application/<int:app_id>/status', methods=['POST'])
@company_required
def update_application_status(app_id):
    """Update application status"""
    new_status = request.form.get('status')
    
    if new_status not in Config.APPLICATION_STATUSES:
        flash('Invalid status', 'danger')
        return redirect(request.referrer)
    
    query = "UPDATE applications SET application_status = %s WHERE id = %s"
    execute_query(query, (new_status, app_id))
    
    flash(f'Application status updated to {new_status}', 'success')
    return redirect(request.referrer)


# ============================================
# ADMIN ROUTES
# ============================================

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    """Admin dashboard with statistics"""
    
    # Get statistics
    stats = {}
    
    # Total students
    stats['total_students'] = execute_query(
        "SELECT COUNT(*) as count FROM students", fetch_one=True
    )['count']
    
    # Total companies
    stats['total_companies'] = execute_query(
        "SELECT COUNT(*) as count FROM companies WHERE is_active = 1", fetch_one=True
    )['count']
    
    # Pending companies
    stats['pending_companies'] = execute_query(
        "SELECT COUNT(*) as count FROM companies WHERE is_active = 0", fetch_one=True
    )['count']
    
    # Total jobs
    stats['total_jobs'] = execute_query(
        "SELECT COUNT(*) as count FROM job_postings WHERE status = 'Approved'", fetch_one=True
    )['count']
    
    # Pending jobs
    stats['pending_jobs'] = execute_query(
        "SELECT COUNT(*) as count FROM job_postings WHERE status = 'Pending'", fetch_one=True
    )['count']
    
    # Total applications
    stats['total_applications'] = execute_query(
        "SELECT COUNT(*) as count FROM applications", fetch_one=True
    )['count']
    
    # Total placements
    stats['total_placements'] = execute_query(
        "SELECT COUNT(*) as count FROM applications WHERE application_status = 'Selected'", fetch_one=True
    )['count']
    
    # Recent applications
    recent_apps_query = """
        SELECT a.*, s.name as student_name, jp.title, c.company_name
        FROM applications a
        JOIN students s ON a.student_id = s.id
        JOIN job_postings jp ON a.job_id = jp.id
        JOIN companies c ON jp.company_id = c.id
        ORDER BY a.applied_at DESC
        LIMIT 10
    """
    recent_applications = execute_query(recent_apps_query, fetch=True)
    
    return render_template('admin_dashboard.html',
                          stats=stats,
                          recent_applications=recent_applications or [])


@app.route('/admin/companies')
@admin_required
def admin_companies():
    """Manage companies"""
    companies = get_all('companies', order_by='created_at DESC')
    return render_template('admin_companies.html', companies=companies or [])


@app.route('/admin/company/new', methods=['GET', 'POST'])
@admin_required
def admin_new_company():
    """Create new company account (admin-only creation)"""
    if request.method == 'POST':
        company_name = request.form.get('company_name')
        email = request.form.get('email')
        contact_person = request.form.get('contact_person')
        phone = request.form.get('phone')
        website = request.form.get('website')
        
        # Check if email exists
        existing = execute_query(
            "SELECT id FROM companies WHERE email = %s",
            (email,),
            fetch_one=True
        )
        
        if existing:
            flash('Email already registered', 'danger')
            return redirect(url_for('admin_new_company'))
        
        # Generate random password
        password = generate_random_password()
        password_hash = generate_password_hash(password)
        
        # Insert company (auto-approved)
        query = """
            INSERT INTO companies
            (company_name, email, password_hash, contact_person, phone, website, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, 1)
        """
        params = (company_name, email, password_hash, contact_person, phone, website)
        
        result = execute_query(query, params)
        
        if result:
            flash(f'Company created! Email: {email}, Password: {password} (Please share with company)', 'success')
            return redirect(url_for('admin_companies'))
        else:
            flash('Company creation failed', 'danger')
            return redirect(url_for('admin_new_company'))
    
    return render_template('admin_new_company.html')


@app.route('/admin/company/<int:company_id>/toggle')
@admin_required
def admin_toggle_company(company_id):
    """Activate/deactivate company account"""
    company = get_by_id('companies', company_id)
    
    if not company:
        flash('Company not found', 'danger')
        return redirect(url_for('admin_companies'))
    
    new_status = 0 if company['is_active'] else 1
    
    query = "UPDATE companies SET is_active = %s WHERE id = %s"
    execute_query(query, (new_status, company_id))
    
    status_text = 'activated' if new_status else 'deactivated'
    flash(f'Company {status_text} successfully', 'success')
    return redirect(url_for('admin_companies'))


@app.route('/admin/jobs')
@admin_required
def admin_jobs():
    """Manage job postings"""
    query = """
        SELECT jp.*, c.company_name
        FROM job_postings jp
        JOIN companies c ON jp.company_id = c.id
        ORDER BY jp.created_at DESC
    """
    jobs = execute_query(query, fetch=True)
    return render_template('admin_jobs.html', jobs=jobs or [])


@app.route('/admin/job/<int:job_id>/status/<status>')
@admin_required
def admin_job_status(job_id, status):
    """Approve or reject job posting"""
    if status not in Config.JOB_STATUSES:
        flash('Invalid status', 'danger')
        return redirect(url_for('admin_jobs'))
    
    query = "UPDATE job_postings SET status = %s WHERE id = %s"
    execute_query(query, (status, job_id))
    
    flash(f'Job {status.lower()} successfully', 'success')
    return redirect(url_for('admin_jobs'))


@app.route('/admin/announcements', methods=['GET', 'POST'])
@admin_required
def admin_announcements():
    """Manage announcements"""
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        admin_id = session['user_id']
        
        query = "INSERT INTO announcements (admin_id, title, content) VALUES (%s, %s, %s)"
        execute_query(query, (admin_id, title, content))
        
        flash('Announcement posted successfully', 'success')
        return redirect(url_for('admin_announcements'))
    
    announcements = get_all('announcements', order_by='created_at DESC')
    return render_template('admin_announcements.html', announcements=announcements or [])


@app.route('/admin/students/import', methods=['GET', 'POST'])
@admin_required
def admin_import_students():
    """Bulk import students from CSV"""
    if request.method == 'POST':
        if 'csv_file' not in request.files:
            flash('No file uploaded', 'danger')
            return redirect(url_for('admin_import_students'))
        
        file = request.files['csv_file']
        
        if file.filename == '':
            flash('No file selected', 'danger')
            return redirect(url_for('admin_import_students'))
        
        if not file.filename.endswith('.csv'):
            flash('Only CSV files are allowed', 'danger')
            return redirect(url_for('admin_import_students'))
        
        # Read CSV file
        stream = StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_reader = csv.DictReader(stream)
        
        success_count = 0
        error_count = 0
        
        for row in csv_reader:
            try:
                # Expected columns: roll_no,name,email,branch,year,cgpa,phone,skills
                roll_no = row.get('roll_no', '').strip()
                name = row.get('name', '').strip()
                email = row.get('email', '').strip()
                branch = row.get('branch', '').strip()
                year = int(row.get('year', 3))
                cgpa = float(row.get('cgpa', 0))
                phone = row.get('phone', '').strip()
                skills = row.get('skills', '').strip()
                
                # Generate random password
                password = generate_random_password()
                password_hash = generate_password_hash(password)
                
                # Check if student already exists
                existing = execute_query(
                    "SELECT id FROM students WHERE email = %s OR roll_no = %s",
                    (email, roll_no),
                    fetch_one=True
                )
                
                if existing:
                    error_count += 1
                    continue
                
                # Insert student
                query = """
                    INSERT INTO students
                    (name, roll_no, email, password_hash, branch, year, cgpa, phone, skills_text)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                params = (name, roll_no, email, password_hash, branch, year, cgpa, phone, skills)
                
                result = execute_query(query, params)
                
                if result:
                    success_count += 1
                    # In production, send email with password here
                    print(f"Student {email} created with password: {password}")
                else:
                    error_count += 1
                    
            except Exception as e:
                print(f"Error importing student: {e}")
                error_count += 1
        
        flash(f'Import complete: {success_count} students added, {error_count} errors', 'info')
        return redirect(url_for('admin_import_students'))
    
    return render_template('admin_import_students.html')


@app.route('/admin/interviews', methods=['GET', 'POST'])
@admin_required
def admin_interviews():
    """Manage interview schedules"""
    if request.method == 'POST':
        job_id = request.form.get('job_id')
        interview_date = request.form.get('interview_date')
        interview_time = request.form.get('interview_time')
        location = request.form.get('location')
        meeting_link = request.form.get('meeting_link')
        student_ids = request.form.getlist('students')
        
        # Create interview
        query = """
            INSERT INTO interviews (job_id, interview_date, interview_time, location, meeting_link)
            VALUES (%s, %s, %s, %s, %s)
        """
        interview_id = execute_query(query, (job_id, interview_date, interview_time, location, meeting_link))
        
        # Invite selected students
        if interview_id and student_ids:
            for student_id in student_ids:
                invite_query = """
                    INSERT INTO interview_invitations (interview_id, student_id)
                    VALUES (%s, %s)
                """
                execute_query(invite_query, (interview_id, student_id))
        
        flash('Interview scheduled and invitations sent', 'success')
        return redirect(url_for('admin_interviews'))
    
    # Get all jobs for dropdown
    jobs_query = """
        SELECT jp.id, jp.title, c.company_name
        FROM job_postings jp
        JOIN companies c ON jp.company_id = c.id
        WHERE jp.status = 'Approved'
        ORDER BY jp.created_at DESC
    """
    jobs = execute_query(jobs_query, fetch=True)
    
    # Get upcoming interviews
    interviews_query = """
        SELECT i.*, jp.title, c.company_name,
               COUNT(ii.id) as invited_count
        FROM interviews i
        JOIN job_postings jp ON i.job_id = jp.id
        JOIN companies c ON jp.company_id = c.id
        LEFT JOIN interview_invitations ii ON i.id = ii.interview_id
        WHERE i.interview_date >= CURDATE()
        GROUP BY i.id
        ORDER BY i.interview_date ASC
    """
    interviews = execute_query(interviews_query, fetch=True)
    
    return render_template('admin_interviews.html',
                          jobs=jobs or [],
                          interviews=interviews or [])


@app.route('/admin/interviews/<int:job_id>/shortlisted')
@admin_required
def get_shortlisted_students(job_id):
    """Get shortlisted students for a job (AJAX endpoint)"""
    query = """
        SELECT s.id, s.name, s.roll_no, s.branch, s.cgpa
        FROM students s
        JOIN applications a ON s.id = a.student_id
        WHERE a.job_id = %s AND a.application_status = 'Shortlisted'
        ORDER BY s.name
    """
    students = execute_query(query, (job_id,), fetch=True)
    
    from flask import jsonify
    return jsonify(students or [])


@app.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    """Serve uploaded files (resumes)"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


# ============================================
# MAIN ENTRY POINT
# ============================================

if __name__ == '__main__':
    # Test database connection before starting
    print("\n" + "="*50)
    print("NSUT Placement Portal - Starting Application")
    print("="*50)
    
    if test_connection():
        print("Starting Flask server on http://localhost:5000")
        print("="*50 + "\n")
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        print("\n" + "!"*50)
        print("ERROR: Could not connect to database!")
        print("Please ensure:")
        print("1. XAMPP is running")
        print("2. MySQL service is started")
        print("3. Database 'nsut_placement' is created")
        print("4. Configuration in .env is correct")
        print("!"*50 + "\n")
