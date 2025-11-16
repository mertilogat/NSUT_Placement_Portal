# NSUT Placement Portal - ER Diagram Documentation

## Database Entity-Relationship Overview

This document explains the database structure for the NSUT Internship/Placement Portal system.

---

## Entities and Attributes

### 1. **STUDENTS**
Primary entity representing student users.

**Attributes:**
- `id` (PK): Unique identifier
- `name`: Full name of student
- `roll_no` (UNIQUE): University roll number
- `email` (UNIQUE): Official NSUT email
- `password_hash`: Encrypted password
- `branch`: Department (CSE, ECE, ME, MAC, CSAI, CSDS, BT, ITNS, ICE)
- `year`: Current year (3 or 4 only - eligible for placements)
- `cgpa`: Current CGPA (0-10 scale)
- `phone`: Contact number
- `skills_text`: Comma-separated skills
- `resume_filename`: Uploaded resume PDF filename
- `created_at`: Registration timestamp

---

### 2. **COMPANIES**
Represents recruiting companies/organizations.

**Attributes:**
- `id` (PK): Unique identifier
- `company_name`: Official company name
- `email` (UNIQUE): Company recruiter email
- `password_hash`: Encrypted password
- `contact_person`: Recruiter name
- `phone`: Contact number
- `website`: Company website URL
- `is_active`: Account activation status (approved by admin)
- `created_at`: Registration timestamp

---

### 3. **PC_ADMINS**
Placement Cell administrators.

**Attributes:**
- `id` (PK): Unique identifier
- `name`: Admin name
- `email` (UNIQUE): Admin email
- `password_hash`: Encrypted password
- `created_at`: Account creation timestamp

**Default Admin:**
- Email: admin@nsut.ac.in
- Password: admin123 (change after first login)

---

### 4. **JOB_POSTINGS**
Job/internship opportunities posted by companies.

**Attributes:**
- `id` (PK): Unique identifier
- `company_id` (FK): Reference to companies table
- `title`: Job title
- `description`: Detailed job description
- `job_type`: Internship / Full-time / Both
- `min_cgpa`: Minimum CGPA requirement
- `allowed_branches`: Comma-separated branch codes
- `allowed_years`: Comma-separated years (e.g., "3,4")
- `deadline`: Application deadline date
- `num_openings`: Number of positions available
- `status`: Pending / Approved / Rejected (by PC admin)
- `created_at`: Job posting timestamp

---

### 5. **APPLICATIONS**
Student applications to job postings.

**Attributes:**
- `id` (PK): Unique identifier
- `student_id` (FK): Reference to students table
- `job_id` (FK): Reference to job_postings table
- `application_status`: Applied / Shortlisted / Interview / Selected / Rejected
- `applied_at`: Application submission timestamp
- `updated_at`: Last status update timestamp

**Constraints:**
- UNIQUE(student_id, job_id) - prevents duplicate applications

---

### 6. **INTERVIEWS**
Interview events scheduled for jobs.

**Attributes:**
- `id` (PK): Unique identifier
- `job_id` (FK): Reference to job_postings table
- `interview_date`: Date of interview
- `interview_time`: Time of interview
- `location`: Physical location (if on-campus)
- `meeting_link`: Virtual meeting link (if online)
- `created_at`: Schedule creation timestamp

---

### 7. **INTERVIEW_INVITATIONS**
Maps students to interview slots.

**Attributes:**
- `id` (PK): Unique identifier
- `interview_id` (FK): Reference to interviews table
- `student_id` (FK): Reference to students table
- `status`: Pending / Accepted / Declined
- `created_at`: Invitation timestamp

**Constraints:**
- UNIQUE(interview_id, student_id) - prevents duplicate invitations

---

### 8. **ANNOUNCEMENTS**
General announcements by PC Admin.

**Attributes:**
- `id` (PK): Unique identifier
- `admin_id` (FK): Reference to pc_admins table
- `title`: Announcement title
- `content`: Announcement text
- `created_at`: Publication timestamp

---

## Relationships

### 1. **COMPANIES → JOB_POSTINGS** (One-to-Many)
- One company can post multiple jobs
- **Foreign Key:** job_postings.company_id → companies.id
- **ON DELETE CASCADE:** Deleting a company removes all its job postings

### 2. **STUDENTS → APPLICATIONS** (One-to-Many)
- One student can submit multiple applications
- **Foreign Key:** applications.student_id → students.id
- **ON DELETE CASCADE:** Deleting a student removes all their applications

### 3. **JOB_POSTINGS → APPLICATIONS** (One-to-Many)
- One job posting can receive multiple applications
- **Foreign Key:** applications.job_id → job_postings.id
- **ON DELETE CASCADE:** Deleting a job removes all applications to it

### 4. **JOB_POSTINGS → INTERVIEWS** (One-to-Many)
- One job can have multiple interview slots
- **Foreign Key:** interviews.job_id → job_postings.id
- **ON DELETE CASCADE:** Deleting a job removes all interview schedules

### 5. **INTERVIEWS → INTERVIEW_INVITATIONS** (One-to-Many)
- One interview slot can have multiple student invitations
- **Foreign Key:** interview_invitations.interview_id → interviews.id
- **ON DELETE CASCADE:** Deleting an interview removes all invitations

### 6. **STUDENTS → INTERVIEW_INVITATIONS** (One-to-Many)
- One student can receive multiple interview invitations
- **Foreign Key:** interview_invitations.student_id → students.id
- **ON DELETE CASCADE:** Deleting a student removes all their invitations

### 7. **PC_ADMINS → ANNOUNCEMENTS** (One-to-Many)
- One admin can create multiple announcements
- **Foreign Key:** announcements.admin_id → pc_admins.id
- **ON DELETE CASCADE:** Deleting an admin removes their announcements

---

## Cardinality Summary

```
COMPANIES (1) ──────< (M) JOB_POSTINGS
STUDENTS (1) ──────< (M) APPLICATIONS
JOB_POSTINGS (1) ──────< (M) APPLICATIONS
JOB_POSTINGS (1) ──────< (M) INTERVIEWS
INTERVIEWS (1) ──────< (M) INTERVIEW_INVITATIONS
STUDENTS (1) ──────< (M) INTERVIEW_INVITATIONS
PC_ADMINS (1) ──────< (M) ANNOUNCEMENTS
```

---

## Normalization

The database follows **Third Normal Form (3NF)**:

1. **1NF:** All attributes contain atomic values
2. **2NF:** No partial dependencies (all non-key attributes depend on entire primary key)
3. **3NF:** No transitive dependencies (no non-key attribute depends on another non-key attribute)

---

## Indexes

**Primary Keys:** Automatically indexed on all tables
**Unique Constraints:** Automatically indexed
- students.roll_no
- students.email
- companies.email
- pc_admins.email
- UNIQUE(student_id, job_id) in applications
- UNIQUE(interview_id, student_id) in interview_invitations

**Recommended Additional Indexes for Performance:**
```sql
CREATE INDEX idx_job_deadline ON job_postings(deadline);
CREATE INDEX idx_job_status ON job_postings(status);
CREATE INDEX idx_app_status ON applications(application_status);
CREATE INDEX idx_student_branch_year ON students(branch, year);
```

---

## Business Rules Enforced

1. **Students:** Only year 3 and 4 students are eligible (CHECK constraint)
2. **CGPA:** Must be between 0 and 10 (CHECK constraint)
3. **Unique Applications:** Student cannot apply to same job twice
4. **Unique Invitations:** Student cannot be invited to same interview twice
5. **Referential Integrity:** All foreign keys maintain data consistency
6. **Cascade Deletes:** Related records are automatically cleaned up

---

## Sample Queries (For Viva)

See `db/nsut_placement.sql` file for 5 sample queries demonstrating:
- JOINs across multiple tables
- Aggregate functions (COUNT, GROUP BY)
- Date filtering
- Subqueries and complex conditions

---

## ER Diagram Visual Representation

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│  STUDENTS   │────<────│ APPLICATIONS │────>────│JOB_POSTINGS │
└─────────────┘         └──────────────┘         └─────────────┘
      │                                                  │
      │                                                  │
      │                 ┌──────────────┐                │
      └────────<────────│  INTERVIEW   │────<───────────┘
                        │  INVITATIONS │
                        └──────────────┘
                               │
                               │
                        ┌──────────────┐
                        │  INTERVIEWS  │
                        └──────────────┘
                               │
                               │
                        ┌──────────────┐
                        │JOB_POSTINGS  │
                        └──────────────┘
                               │
                               │
                        ┌──────────────┐
                        │  COMPANIES   │
                        └──────────────┘

                        ┌──────────────┐         ┌──────────────┐
                        │  PC_ADMINS   │────<────│ANNOUNCEMENTS │
                        └──────────────┘         └──────────────┘
```

---

**End of ER Diagram Documentation**
