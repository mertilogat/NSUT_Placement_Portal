# NSUT Placement Portal - Viva Preparation Notes

## Project Overview

**Project Title:** NSUT Internship/Placement Portal  
**Subject:** Database Management System (DBMS)  
**Technology Stack:** Flask (Python), MySQL, HTML/CSS/Bootstrap

---

## 1. Database Design

### Purpose
To create a centralized system for managing internship and placement activities at NSUT, facilitating interaction between students, companies, and the placement cell.

### Key Design Decisions

1. **Normalization:** Database follows Third Normal Form (3NF)
   - Eliminates data redundancy
   - Ensures data integrity
   - No transitive dependencies

2. **Referential Integrity:** All foreign keys use ON DELETE CASCADE
   - Automatic cleanup of related records
   - Maintains database consistency

3. **Data Types:**
   - ENUM for fixed options (branch, status, job_type)
   - DECIMAL(3,2) for CGPA (precise calculations)
   - TIMESTAMP for automatic date tracking

4. **Constraints:**
   - CHECK constraints for CGPA (0-10 range)
   - UNIQUE constraints on email and roll_no
   - NOT NULL on critical fields

---

## 2. Entity-Relationship Model

### Entities (8 Tables)

1. **students** - Student profiles and credentials
2. **companies** - Company/recruiter accounts
3. **pc_admins** - Placement cell administrators
4. **job_postings** - Job/internship listings
5. **applications** - Job applications by students
6. **interviews** - Interview schedules
7. **interview_invitations** - Student-interview mapping
8. **announcements** - Admin announcements

### Relationships

- **Companies (1) → Job Postings (M)** - One company posts many jobs
- **Job Postings (1) → Applications (M)** - One job receives many applications
- **Students (1) → Applications (M)** - One student applies to many jobs
- **Job Postings (1) → Interviews (M)** - One job has many interview slots
- **Interviews (1) → Invitations (M)** - One interview invites many students
- **Students (1) → Invitations (M)** - One student receives many invitations
- **Admins (1) → Announcements (M)** - One admin posts many announcements

### Cardinality
- All relationships are **One-to-Many** (1:M)
- **Many-to-Many** relationships resolved through junction tables
  - Students ↔ Jobs (via applications)
  - Students ↔ Interviews (via interview_invitations)

---

## 3. Five Important SQL Queries

### Query 1: List Students Eligible for a Specific Job (JOIN)

**Purpose:** Find all students who applied to a specific job with their details

```sql
SELECT s.name, s.roll_no, s.branch, s.cgpa, a.application_status
FROM students s 
JOIN applications a ON s.id = a.student_id 
WHERE a.job_id = 1;
```

**Explanation:**
- Uses INNER JOIN to combine students and applications tables
- Filters by specific job_id
- Returns student details along with application status
- Demonstrates: JOIN, WHERE clause

---

### Query 2: Count Applications per Job (Aggregate Function)

**Purpose:** Get statistics on how many applications each job received

```sql
SELECT jp.title, c.company_name, COUNT(a.id) as total_applications 
FROM job_postings jp 
LEFT JOIN applications a ON jp.id = a.job_id 
LEFT JOIN companies c ON jp.company_id = c.id 
GROUP BY jp.id, jp.title, c.company_name;
```

**Explanation:**
- Uses LEFT JOIN to include jobs with zero applications
- Multiple table joins (3 tables)
- COUNT aggregate function
- GROUP BY to get counts per job
- Demonstrates: Multiple JOINs, Aggregation, GROUP BY

---

### Query 3: Find Students with Scheduled Interviews (Complex JOIN)

**Purpose:** Get list of students with accepted interview invitations and details

```sql
SELECT s.name, s.email, i.interview_date, i.interview_time, 
       jp.title, c.company_name
FROM students s 
JOIN interview_invitations ii ON s.id = ii.student_id 
JOIN interviews i ON ii.interview_id = i.id 
JOIN job_postings jp ON i.job_id = jp.id 
JOIN companies c ON jp.company_id = c.id 
WHERE ii.status = 'Accepted'
ORDER BY i.interview_date ASC;
```

**Explanation:**
- Chain of 5 table JOINs
- Filters for accepted invitations only
- Orders by interview date
- Demonstrates: Multi-table JOINs, WHERE filtering, ORDER BY

---

### Query 4: Get Placement Statistics (Subquery & Aggregate)

**Purpose:** Calculate total number of students who got placed

```sql
SELECT 
    COUNT(DISTINCT s.id) as total_placed_students,
    COUNT(DISTINCT a.job_id) as total_jobs_with_selections,
    AVG(s.cgpa) as avg_cgpa_of_placed_students
FROM students s
JOIN applications a ON s.id = a.student_id
WHERE a.application_status = 'Selected';
```

**Explanation:**
- COUNT(DISTINCT) to avoid duplicate counting
- AVG() aggregate function for average CGPA
- Filters only selected applications
- Demonstrates: DISTINCT, Multiple aggregates, WHERE

---

### Query 5: Find Jobs Closing Soon (Date Functions)

**Purpose:** Alert students about jobs with deadlines approaching

```sql
SELECT jp.title, c.company_name, jp.deadline, jp.num_openings,
       DATEDIFF(jp.deadline, CURDATE()) as days_remaining
FROM job_postings jp 
JOIN companies c ON jp.company_id = c.id 
WHERE jp.deadline BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 30 DAY) 
  AND jp.status = 'Approved'
ORDER BY jp.deadline ASC;
```

**Explanation:**
- CURDATE() gets current date
- DATE_ADD() adds 30 days
- DATEDIFF() calculates remaining days
- BETWEEN for date range
- Multiple WHERE conditions with AND
- Demonstrates: Date functions, BETWEEN, Complex WHERE

---

## 4. Application Architecture

### Three-Tier Architecture

1. **Presentation Layer (Frontend)**
   - HTML templates (Jinja2)
   - Bootstrap 5 for styling
   - Minimal JavaScript for interactivity

2. **Application Layer (Backend)**
   - Flask web framework
   - Session-based authentication
   - Password hashing (bcrypt)
   - File upload handling

3. **Data Layer (Database)**
   - MySQL database
   - Direct SQL queries (no ORM)
   - Prepared statements for security

---

## 5. Security Measures

1. **Password Security**
   - Passwords hashed using `werkzeug.security.generate_password_hash()`
   - Never stored in plain text
   - Uses strong hashing algorithm (scrypt)

2. **SQL Injection Prevention**
   - All queries use prepared statements with parameter binding
   - Example: `execute_query("SELECT * FROM students WHERE id = %s", (student_id,))`
   - Never concatenate user input directly into SQL

3. **Session Management**
   - Flask sessions with secret key
   - Session timeout automatic
   - Role-based access control

4. **File Upload Security**
   - Only PDF files allowed
   - Maximum file size: 2 MB
   - Filenames sanitized using `secure_filename()`

---

## 6. Key Features Explanation

### Role-Based Access Control

Three user roles with distinct permissions:

1. **Student**
   - Browse and apply to jobs
   - Update profile and resume
   - View application status
   - Respond to interview invitations

2. **Company**
   - Post job openings (pending admin approval)
   - View and manage applications
   - Update application status

3. **Placement Cell Admin**
   - Approve/reject jobs and companies
   - Create company accounts
   - Bulk import students via CSV
   - Schedule interviews
   - Post announcements
   - View all statistics

### Automatic Deadline Enforcement

- System checks `job.deadline >= CURDATE()` before allowing applications
- Past deadlines automatically prevent new applications
- Frontend displays deadline prominently

### Application Workflow

```
Applied → Shortlisted → Interview → Selected/Rejected
```

- Company/Admin can update status
- Students track progress in real-time
- Email notifications (can be integrated)

---

## 7. Technology Justification

### Why Flask?
- Lightweight and easy to understand
- No complex ORM hiding SQL queries
- Perfect for demonstrating database concepts
- Widely used in industry

### Why MySQL?
- Industry-standard relational database
- Excellent for learning SQL
- Strong data integrity features
- Easy to install via XAMPP

### Why No ORM?
- Project requirement: demonstrate SQL knowledge
- Direct SQL queries are visible and explainable
- Easier to understand for academic purposes
- Clear separation between application and database logic

---

## 8. Challenges & Solutions

### Challenge 1: Many-to-Many Relationships
**Solution:** Created junction tables (applications, interview_invitations)

### Challenge 2: Password Management
**Solution:** Auto-generate passwords for CSV imports, use bcrypt hashing

### Challenge 3: File Storage
**Solution:** Store files in filesystem, save filename in database

### Challenge 4: Eligibility Checking
**Solution:** Application-layer validation based on CGPA, branch, year

---

## 9. Future Enhancements

1. Email notification system
2. Advanced analytics and reports
3. Multi-round interview support
4. Resume parsing
5. Offer letter management
6. Alumni placement tracking

---

## 10. Viva Questions & Answers

**Q1: Why did you use prepared statements?**  
A: To prevent SQL injection attacks by separating SQL code from user data.

**Q2: What is normalization and what form is your database in?**  
A: Normalization eliminates redundancy. My database is in 3NF with no transitive dependencies.

**Q3: Explain CASCADE DELETE**  
A: When a parent record is deleted, all related child records are automatically deleted to maintain referential integrity.

**Q4: How do you ensure password security?**  
A: Passwords are hashed using bcrypt (scrypt algorithm) before storing. Plain text passwords are never saved.

**Q5: What is the difference between INNER JOIN and LEFT JOIN?**  
A: INNER JOIN returns only matching records from both tables. LEFT JOIN returns all records from left table plus matching records from right table.

**Q6: How do you handle file uploads?**  
A: Validate file type (PDF only), check size (max 2MB), use `secure_filename()` for safety, store in uploads folder, save filename in database.

**Q7: Explain your authentication system**  
A: Flask sessions store user_id and role after login. Decorators check authentication before allowing access to protected routes.

**Q8: What are ENUM types and why use them?**  
A: ENUM restricts a column to a predefined set of values, ensuring data consistency and preventing invalid entries.

**Q9: How do aggregate functions work?**  
A: Functions like COUNT(), AVG(), SUM() operate on multiple rows and return a single value, often used with GROUP BY.

**Q10: What is the purpose of indexes?**  
A: Indexes speed up data retrieval by creating a sorted reference to data, automatically created on PRIMARY KEYs and UNIQUE columns.

---

## Conclusion

This project demonstrates:
✅ Database design and normalization  
✅ Complex SQL queries with JOINs and aggregations  
✅ Referential integrity and constraints  
✅ Web application development  
✅ Security best practices  
✅ Real-world problem solving  

**Key Takeaway:** A well-designed database is the foundation of any robust application!

---

**Good Luck with Your Viva! 🎯**
