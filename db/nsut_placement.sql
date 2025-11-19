-- ============================================
-- NSUT Internship/Placement Portal Database
-- Database Management System Project
-- ============================================

-- Drop database if exists and create fresh
DROP DATABASE IF EXISTS nsut_placement;
CREATE DATABASE nsut_placement;
USE nsut_placement;

-- ============================================
-- TABLE 1: students
-- Stores student information and credentials
-- ============================================
CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    roll_no VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    branch ENUM('CSE', 'ECE', 'ME', 'MAC', 'CSAI', 'CSDS', 'BT', 'ITNS', 'ICE') NOT NULL,
    year INT NOT NULL CHECK (year IN (3, 4)),
    cgpa DECIMAL(3, 2) NOT NULL CHECK (cgpa >= 0 AND cgpa <= 10),
    phone VARCHAR(15),
    skills_text TEXT,
    resume_filename VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- TABLE 2: companies
-- Stores company/recruiter information
-- ============================================
CREATE TABLE companies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(150) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    contact_person VARCHAR(100),
    phone VARCHAR(15),
    website VARCHAR(200),
    is_active BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- TABLE 3: pc_admins
-- Stores Placement Cell admin credentials
-- ============================================
CREATE TABLE pc_admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- TABLE 4: job_postings
-- Stores job/internship postings by companies
-- ============================================
CREATE TABLE job_postings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    company_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    job_type ENUM('Internship', 'Full-time', 'Both') NOT NULL,
    min_cgpa DECIMAL(3, 2) NOT NULL CHECK (min_cgpa >= 0 AND min_cgpa <= 10),
    deadline DATE NOT NULL,
    num_openings INT NOT NULL,
    status ENUM('Pending', 'Approved', 'Rejected') DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
);

-- ============================================
-- TABLE 5: job_allowed_branches
-- Junction table for job eligibility by branch
-- Implements proper normalization (many-to-many)
-- ============================================
CREATE TABLE job_allowed_branches (
    id INT AUTO_INCREMENT PRIMARY KEY,
    job_id INT NOT NULL,
    branch ENUM('CSE', 'ECE', 'ME', 'MAC', 'CSAI', 'CSDS', 'BT', 'ITNS', 'ICE') NOT NULL,
    FOREIGN KEY (job_id) REFERENCES job_postings(id) ON DELETE CASCADE,
    UNIQUE KEY unique_job_branch (job_id, branch)
);

-- ============================================
-- TABLE 6: job_allowed_years
-- Junction table for job eligibility by year
-- Implements proper normalization (many-to-many)
-- ============================================
CREATE TABLE job_allowed_years (
    id INT AUTO_INCREMENT PRIMARY KEY,
    job_id INT NOT NULL,
    year INT NOT NULL CHECK (year IN (3, 4)),
    FOREIGN KEY (job_id) REFERENCES job_postings(id) ON DELETE CASCADE,
    UNIQUE KEY unique_job_year (job_id, year)
);

-- ============================================
-- TABLE 7: applications
-- Stores student applications to jobs
-- ============================================
CREATE TABLE applications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    job_id INT NOT NULL,
    application_status ENUM('Applied', 'Shortlisted', 'Interview', 'Selected', 'Rejected') DEFAULT 'Applied',
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES job_postings(id) ON DELETE CASCADE,
    UNIQUE KEY unique_application (student_id, job_id)
);

-- ============================================
-- TABLE 8: interviews
-- Stores interview schedule information
-- ============================================
CREATE TABLE interviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    job_id INT NOT NULL,
    interview_date DATE NOT NULL,
    interview_time TIME NOT NULL,
    location VARCHAR(255),
    meeting_link VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (job_id) REFERENCES job_postings(id) ON DELETE CASCADE
);

-- ============================================
-- TABLE 9: interview_invitations
-- Maps students to interview slots
-- ============================================
CREATE TABLE interview_invitations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    interview_id INT NOT NULL,
    student_id INT NOT NULL,
    status ENUM('Pending', 'Accepted', 'Declined') DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (interview_id) REFERENCES interviews(id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    UNIQUE KEY unique_invitation (interview_id, student_id)
);

-- ============================================
-- TABLE 10: announcements
-- Stores announcements by PC Admin
-- ============================================
CREATE TABLE announcements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    admin_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (admin_id) REFERENCES pc_admins(id) ON DELETE CASCADE
);

-- ============================================
-- SEED DATA - PC Admin (Default Account)
-- Email: admin@nsut.ac.in
-- Password: admin123
-- ============================================
INSERT INTO pc_admins (name, email, password_hash) VALUES
('Placement Cell Admin', 'admin@nsut.ac.in', 'scrypt:32768:8:1$1WYJ6IvvzMi78YWf$6e7df3da5349f45335cd02f7af7d5c6409e41822f4a089968bdaa5bf912e4c7dd410b3af4a53eadd6ae4678674183bfe011947068a4294ad8e2848ffc58e9514');

-- Note: The password_hash above is a placeholder. In the actual Flask app, 
-- we will use werkzeug.security.generate_password_hash('admin123') 
-- For now, you can manually update this after first run or use the app to create admin

-- ============================================
-- SEED DATA - Companies (3 sample companies)
-- All companies pre-approved by admin
-- ============================================
INSERT INTO companies (company_name, email, password_hash, contact_person, phone, website, is_active) VALUES
('Google India', 'hr@google.com', 'scrypt:32768:8:1$hash_placeholder', 'Sundar Pichai', '9876543210', 'https://careers.google.com', TRUE),
('Microsoft Corporation', 'recruitment@microsoft.com', 'scrypt:32768:8:1$hash_placeholder', 'Satya Nadella', '9876543211', 'https://careers.microsoft.com', TRUE),
('Amazon Web Services', 'jobs@amazon.com', 'scrypt:32768:8:1$hash_placeholder', 'Andy Jassy', '9876543212', 'https://amazon.jobs', TRUE);

-- Note: Passwords will be set properly when companies are created via admin panel
-- For testing, you can manually set passwords using Flask app

-- ============================================
-- SEED DATA - Students (10 sample students)
-- All students are in year 3 or 4
-- ============================================
INSERT INTO students (name, roll_no, email, password_hash, branch, year, cgpa, phone, skills_text, resume_filename) VALUES
('Rahul Sharma', '2021CSE001', 'rahul.sharma@nsut.ac.in', 'scrypt:32768:8:1$hash_placeholder', 'CSE', 4, 8.5, '9999000001', 'Python, Java, Machine Learning, Django', 'rahul_sharma_resume.pdf'),
('Priya Singh', '2021CSAI002', 'priya.singh@nsut.ac.in', 'scrypt:32768:8:1$hash_placeholder', 'CSAI', 4, 9.2, '9999000002', 'Data Science, Python, R, Deep Learning, TensorFlow', 'priya_singh_resume.pdf'),
('Amit Kumar', '2021ECE003', 'amit.kumar@nsut.ac.in', 'scrypt:32768:8:1$hash_placeholder', 'ECE', 3, 7.8, '9999000003', 'Embedded Systems, C++, IoT, Arduino', 'amit_kumar_resume.pdf'),
('Sneha Gupta', '2021CSDS004', 'sneha.gupta@nsut.ac.in', 'scrypt:32768:8:1$hash_placeholder', 'CSDS', 4, 8.9, '9999000004', 'Data Analytics, SQL, Python, Tableau, Power BI', 'sneha_gupta_resume.pdf'),
('Vikram Malhotra', '2021MAC005', 'vikram.m@nsut.ac.in', 'scrypt:32768:8:1$hash_placeholder', 'MAC', 3, 8.1, '9999000005', 'Mathematics, Python, Optimization, MATLAB', 'vikram_malhotra_resume.pdf'),
('Anjali Verma', '2021BT006', 'anjali.verma@nsut.ac.in', 'scrypt:32768:8:1$hash_placeholder', 'BT', 4, 8.7, '9999000006', 'Bioinformatics, Python, R, Genomics', 'anjali_verma_resume.pdf'),
('Rohan Patel', '2021ITNS007', 'rohan.patel@nsut.ac.in', 'scrypt:32768:8:1$hash_placeholder', 'ITNS', 3, 7.5, '9999000007', 'Cybersecurity, Networking, Ethical Hacking, Linux', 'rohan_patel_resume.pdf'),
('Kavya Reddy', '2021ICE008', 'kavya.reddy@nsut.ac.in', 'scrypt:32768:8:1$hash_placeholder', 'ICE', 4, 8.3, '9999000008', 'Control Systems, MATLAB, PLC Programming', 'kavya_reddy_resume.pdf'),
('Arjun Mehta', '2021ME009', 'arjun.mehta@nsut.ac.in', 'scrypt:32768:8:1$hash_placeholder', 'ME', 3, 7.9, '9999000009', 'CAD/CAM, SolidWorks, AutoCAD, Manufacturing', 'arjun_mehta_resume.pdf'),
('Divya Chopra', '2021CSE010', 'divya.chopra@nsut.ac.in', 'scrypt:32768:8:1$hash_placeholder', 'CSE', 4, 9.0, '9999000010', 'Full Stack Development, React, Node.js, MongoDB', 'divya_chopra_resume.pdf');

-- Note: Passwords are placeholders. Students will be created with auto-generated passwords
-- and emailed to them (or set via CSV import)

-- ============================================
-- SEED DATA - Job Postings (5 sample jobs)
-- All jobs are approved for testing
-- ============================================
INSERT INTO job_postings (company_id, title, description, job_type, min_cgpa, deadline, num_openings, status) VALUES
(1, 'Software Engineering Intern', 'Join Google as a Software Engineering Intern. Work on cutting-edge projects in cloud computing, AI/ML, and distributed systems. Required skills: Strong programming in C++/Java/Python, data structures, algorithms.', 'Internship', 7.5, '2025-12-31', 10, 'Approved'),
(1, 'Full Stack Developer', 'Full-time position for experienced developers. Build scalable web applications using modern frameworks. Required: React, Node.js, cloud platforms.', 'Full-time', 8.0, '2025-11-30', 5, 'Approved'),
(2, 'Data Science Internship', 'Microsoft is hiring Data Science interns to work on Azure ML projects. Analyze large datasets, build predictive models, and deploy ML solutions. Required: Python, ML algorithms, statistics.', 'Internship', 8.0, '2026-01-15', 8, 'Approved'),
(3, 'Cloud Solutions Architect', 'Join AWS as a Cloud Solutions Architect. Design and implement cloud infrastructure for enterprise clients. Required: AWS certification preferred, networking, security.', 'Full-time', 7.0, '2025-12-15', 6, 'Approved'),
(2, 'AI/ML Research Intern', 'Work with Microsoft Research on cutting-edge AI projects. Publish papers, develop new algorithms. Required: Strong mathematics, deep learning, research experience.', 'Internship', 8.5, '2026-02-28', 4, 'Approved');

-- ============================================
-- SEED DATA - Job Allowed Branches
-- Populate junction table with branch eligibility
-- ============================================
INSERT INTO job_allowed_branches (job_id, branch) VALUES
(1, 'CSE'), (1, 'CSAI'), (1, 'CSDS'), (1, 'ITNS'),
(2, 'CSE'), (2, 'CSAI'), (2, 'CSDS'),
(3, 'CSAI'), (3, 'CSDS'), (3, 'CSE'), (3, 'MAC'),
(4, 'CSE'), (4, 'ITNS'), (4, 'ECE'),
(5, 'CSAI'), (5, 'CSE'), (5, 'MAC');

-- ============================================
-- SEED DATA - Job Allowed Years
-- Populate junction table with year eligibility
-- ============================================
INSERT INTO job_allowed_years (job_id, year) VALUES
(1, 3), (1, 4),
(2, 4),
(3, 3), (3, 4),
(4, 4),
(5, 3), (5, 4);

-- ============================================
-- SEED DATA - Sample Applications
-- Some students have already applied to jobs
-- ============================================
INSERT INTO applications (student_id, job_id, application_status) VALUES
(1, 1, 'Applied'),
(2, 3, 'Shortlisted'),
(3, 4, 'Applied'),
(4, 3, 'Interview'),
(5, 3, 'Applied'),
(6, 5, 'Shortlisted'),
(7, 4, 'Applied'),
(8, 1, 'Applied'),
(9, 2, 'Rejected'),
(10, 2, 'Selected');

-- ============================================
-- SEED DATA - Sample Interviews
-- Interview schedules for shortlisted students
-- ============================================
INSERT INTO interviews (job_id, interview_date, interview_time, location, meeting_link) VALUES
(3, '2025-12-01', '10:00:00', 'Conference Room A, NSUT', 'https://meet.google.com/abc-defg-hij'),
(5, '2025-12-05', '14:00:00', NULL, 'https://teams.microsoft.com/meet/xyz123');

-- ============================================
-- SEED DATA - Interview Invitations
-- Inviting shortlisted students to interviews
-- ============================================
INSERT INTO interview_invitations (interview_id, student_id, status) VALUES
(1, 2, 'Accepted'),
(1, 4, 'Pending'),
(2, 6, 'Accepted');

-- ============================================
-- SEED DATA - Sample Announcements
-- Placement cell announcements
-- ============================================
INSERT INTO announcements (admin_id, title, content) VALUES
(1, 'Welcome to Placement Season 2025-26', 'The placement season has officially started. Please ensure your profiles are updated with latest resume and CGPA. Good luck to all students!'),
(1, 'Resume Workshop on December 20', 'We are organizing a resume building workshop on December 20, 2025. All students are encouraged to attend. Venue: Auditorium, Time: 2:00 PM'),
(1, 'Google Campus Drive Update', 'Google will be conducting on-campus interviews from January 15-17, 2026. Shortlisted students will be notified via email.');

-- ============================================
-- USEFUL QUERIES FOR VIVA DEMONSTRATION
-- ============================================

-- Query 1: List all students eligible for a specific job (with JOIN)
-- SELECT s.name, s.roll_no, s.branch, s.cgpa 
-- FROM students s 
-- JOIN applications a ON s.id = a.student_id 
-- WHERE a.job_id = 1;

-- Query 2: Count applications per job
-- SELECT jp.title, c.company_name, COUNT(a.id) as total_applications 
-- FROM job_postings jp 
-- LEFT JOIN applications a ON jp.id = a.job_id 
-- LEFT JOIN companies c ON jp.company_id = c.id 
-- GROUP BY jp.id;

-- Query 3: Find students with interviews scheduled
-- SELECT s.name, s.email, i.interview_date, i.interview_time, jp.title 
-- FROM students s 
-- JOIN interview_invitations ii ON s.id = ii.student_id 
-- JOIN interviews i ON ii.interview_id = i.id 
-- JOIN job_postings jp ON i.job_id = jp.id 
-- WHERE ii.status = 'Accepted';

-- Query 4: Get placement statistics
-- SELECT 
--     COUNT(DISTINCT s.id) as total_placed_students,
--     COUNT(DISTINCT a.job_id) as total_jobs_with_selections
-- FROM students s
-- JOIN applications a ON s.id = a.student_id
-- WHERE a.application_status = 'Selected';

-- Query 5: Find jobs closing soon (within 30 days)
-- SELECT jp.title, c.company_name, jp.deadline, jp.num_openings 
-- FROM job_postings jp 
-- JOIN companies c ON jp.company_id = c.id 
-- WHERE jp.deadline BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 30 DAY) 
-- AND jp.status = 'Approved';

-- Query 6: Find all jobs eligible for a specific branch and year (demonstrates normalization)
-- SELECT jp.title, c.company_name, jp.min_cgpa, jp.deadline,
--        GROUP_CONCAT(DISTINCT jab.branch) as allowed_branches,
--        GROUP_CONCAT(DISTINCT jay.year) as allowed_years
-- FROM job_postings jp
-- JOIN companies c ON jp.company_id = c.id
-- JOIN job_allowed_branches jab ON jp.id = jab.job_id
-- JOIN job_allowed_years jay ON jp.id = jay.job_id
-- WHERE jab.branch = 'CSE' AND jay.year = 4 AND jp.status = 'Approved'
-- GROUP BY jp.id;

-- ============================================
-- END OF DATABASE SCHEMA
-- ============================================
