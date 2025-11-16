# Manual Test Checklist - NSUT Placement Portal

## Pre-Testing Setup

- [ ] XAMPP MySQL service is running
- [ ] Database `nsut_placement` is created and populated with seed data
- [ ] Flask application is running on `http://localhost:5000`
- [ ] No console errors visible

---

## Test Suite 1: Admin Functionality

### 1.1 Admin Login
- [ ] Navigate to `http://localhost:5000/login`
- [ ] Select "Placement Cell Admin" as user type
- [ ] Email: `admin@nsut.ac.in`
- [ ] Password: `admin123`
- [ ] Click Login
- [ ] **Expected:** Redirect to admin dashboard
- [ ] **Expected:** Welcome message displays

### 1.2 View Dashboard Statistics
- [ ] On admin dashboard, verify these statistics are visible:
  - [ ] Total Students count
  - [ ] Total Active Companies count
  - [ ] Total Approved Jobs count
  - [ ] Total Placements count
- [ ] **Expected:** All numbers are non-zero (from seed data)

### 1.3 Create Company Account
- [ ] Click "Companies" in navigation
- [ ] Click "Add New Company" button
- [ ] Fill form:
  - Company Name: `Test Company Ltd`
  - Email: `testcompany@example.com`
  - Contact Person: `John Smith`
  - Phone: `9876543210`
  - Website: `https://testcompany.com`
- [ ] Click "Create Company Account"
- [ ] **Expected:** Success message with auto-generated password
- [ ] **Note down the password for later use**
- [ ] **Expected:** Company appears in companies list with "Active" status

### 1.4 Approve Job Posting
- [ ] Click "Jobs" in navigation
- [ ] Find a job with "Pending" status
- [ ] Click "Approve" button
- [ ] **Expected:** Status changes to "Approved"
- [ ] **Expected:** Success message displays

### 1.5 Post Announcement
- [ ] Click "Announcements" in navigation
- [ ] Fill form:
  - Title: `Test Announcement`
  - Content: `This is a test announcement for placement portal.`
- [ ] Click "Post Announcement"
- [ ] **Expected:** Announcement appears in list below
- [ ] **Expected:** Success message displays

### 1.6 Schedule Interview
- [ ] Click "Dashboard" then scroll to find interview scheduling
- [ ] Or navigate to interview management
- [ ] Select a job from dropdown
- [ ] **Expected:** Shortlisted students load (if any)
- [ ] Set interview date (future date)
- [ ] Set interview time
- [ ] Enter location or meeting link
- [ ] Select student(s) to invite
- [ ] Click "Schedule Interview"
- [ ] **Expected:** Success message
- [ ] **Expected:** Interview appears in upcoming list

### 1.7 Logout
- [ ] Click user dropdown in top-right
- [ ] Click "Logout"
- [ ] **Expected:** Redirect to home page
- [ ] **Expected:** Logout message displays

---

## Test Suite 2: Student Functionality

### 2.1 Student Registration
- [ ] Navigate to `http://localhost:5000/student/signup`
- [ ] Fill registration form:
  - Name: `Test Student`
  - Roll No: `2021TEST001`
  - Email: `teststudent@nsut.ac.in`
  - Password: `test123`
  - Branch: Select `CSE`
  - Year: Select `4`
  - CGPA: `8.5`
  - Phone: `9999888877`
  - Skills: `Python, Java, React`
- [ ] Click "Register"
- [ ] **Expected:** Success message
- [ ] **Expected:** Redirect to login page

### 2.2 Student Login
- [ ] On login page, select "Student" as user type
- [ ] Email: `teststudent@nsut.ac.in`
- [ ] Password: `test123`
- [ ] Click Login
- [ ] **Expected:** Redirect to student dashboard
- [ ] **Expected:** Welcome message with student name

### 2.3 Update Profile
- [ ] Click "Profile" in navigation
- [ ] Update CGPA to `8.7`
- [ ] Update skills to add `Machine Learning`
- [ ] Click "Update Profile"
- [ ] **Expected:** Success message
- [ ] **Expected:** Changes reflected on page

### 2.4 Upload Resume
- [ ] On Profile page
- [ ] Click "Choose File" under Resume
- [ ] Select a PDF file (max 2MB)
- [ ] Click "Update Profile"
- [ ] **Expected:** Success message
- [ ] **Expected:** Current resume link appears
- [ ] Click resume link
- [ ] **Expected:** PDF opens in new tab

### 2.5 Browse Jobs
- [ ] Click "Jobs" in navigation
- [ ] **Expected:** List of approved jobs displays
- [ ] **Expected:** Only jobs matching student's eligibility shown
- [ ] Test search: Enter company name in search box
- [ ] Click "Filter"
- [ ] **Expected:** Filtered results display

### 2.6 Apply to Job
- [ ] On Jobs page, find an eligible job
- [ ] Click "Apply Now" button
- [ ] **Expected:** Success message
- [ ] **Expected:** Button changes to "Already Applied"
- [ ] Click "Dashboard" in navigation
- [ ] **Expected:** Application appears in "My Applications" table

### 2.7 View Interview Invitation
- [ ] If interview invitation exists (from admin test)
- [ ] On dashboard, find interview in schedule
- [ ] Click "Accept" button
- [ ] **Expected:** Status changes to "Accepted"
- [ ] **Expected:** Success message

### 2.8 Logout
- [ ] Click user dropdown, select Logout
- [ ] **Expected:** Redirect to home page

---

## Test Suite 3: Company Functionality

### 3.1 Company Login
- [ ] Navigate to login page
- [ ] Select "Company Recruiter" as user type
- [ ] Email: Use the company created earlier (e.g., `testcompany@example.com`)
- [ ] Password: Use the auto-generated password noted earlier
- [ ] Click Login
- [ ] **Expected:** Redirect to company dashboard
- [ ] **Expected:** Welcome message with company name

### 3.2 Post New Job
- [ ] Click "Post Job" in navigation
- [ ] Fill job posting form:
  - Job Title: `Software Developer Intern`
  - Description: `Looking for talented interns with strong coding skills...`
  - Job Type: `Internship`
  - Min CGPA: `7.0`
  - Allowed Branches: Check `CSE`, `CSAI`, `CSDS`
  - Allowed Years: Check `3`, `4`
  - Deadline: Select a future date (e.g., 30 days from now)
  - Number of Openings: `5`
- [ ] Click "Submit Job Posting"
- [ ] **Expected:** Success message (pending admin approval)
- [ ] **Expected:** Redirect to dashboard
- [ ] **Expected:** New job appears with "Pending" status

### 3.3 View Applications
- [ ] On company dashboard, find a job with applications
- [ ] Click "View Applications" button
- [ ] **Expected:** List of applications displays
- [ ] **Expected:** Student details visible (name, roll no, branch, CGPA)
- [ ] **Expected:** Resume link available (if student uploaded)

### 3.4 Update Application Status
- [ ] On applications page, find an application
- [ ] Change status dropdown to "Shortlisted"
- [ ] **Expected:** Status updates automatically
- [ ] **Expected:** Success message displays
- [ ] Change another application to "Interview"
- [ ] **Expected:** Status updates

### 3.5 Logout
- [ ] Click user dropdown, select Logout
- [ ] **Expected:** Redirect to home page

---

## Test Suite 4: Edge Cases & Validation

### 4.1 Duplicate Registration
- [ ] Try to register student with existing email
- [ ] **Expected:** Error message "Email already registered"

### 4.2 Invalid Login
- [ ] Try login with wrong password
- [ ] **Expected:** Error message "Invalid email or password"

### 4.3 Apply Without Resume
- [ ] Login as new student (without resume)
- [ ] Try to apply to a job
- [ ] **Expected:** Warning message to upload resume first

### 4.4 Apply After Deadline
- [ ] Login as admin
- [ ] Create job with past deadline
- [ ] Approve the job
- [ ] Login as student
- [ ] **Expected:** Job does not appear in available jobs list

### 4.5 File Upload Validation
- [ ] Try to upload non-PDF file as resume
- [ ] **Expected:** Error or file not accepted
- [ ] Try to upload PDF larger than 2MB
- [ ] **Expected:** Error message about file size

### 4.6 Duplicate Application
- [ ] Login as student
- [ ] Apply to a job
- [ ] Try to apply to same job again
- [ ] **Expected:** Error message "Already applied"

### 4.7 Unauthorized Access
- [ ] Logout all users
- [ ] Try to access `http://localhost:5000/admin/dashboard` directly
- [ ] **Expected:** Redirect to login with warning message
- [ ] Try to access `http://localhost:5000/student/jobs` without login
- [ ] **Expected:** Redirect to login

---

## Test Suite 5: Data Integrity

### 5.1 Foreign Key Constraints
- [ ] Login to phpMyAdmin
- [ ] Go to `nsut_placement` database
- [ ] Try to manually delete a company that has job postings
- [ ] **Expected:** Related job postings are also deleted (CASCADE)
- [ ] Verify in application that jobs are gone

### 5.2 Unique Constraints
- [ ] Try to insert student with duplicate roll_no via SQL
- [ ] **Expected:** Error due to UNIQUE constraint

### 5.3 Check Constraints
- [ ] Try to insert student with CGPA > 10 via SQL
- [ ] **Expected:** Error due to CHECK constraint

---

## Test Suite 6: Admin CSV Import

### 6.1 Prepare CSV File
- [ ] Create file `test_students.csv` with content:
```csv
roll_no,name,email,branch,year,cgpa,phone,skills
2021CSV001,Alice Johnson,alice@nsut.ac.in,CSE,3,8.2,9988776655,Python Java
2021CSV002,Bob Wilson,bob@nsut.ac.in,ECE,4,7.8,9988776656,C++ Arduino
```

### 6.2 Import CSV
- [ ] Login as admin
- [ ] Navigate to student import page
- [ ] Upload the CSV file
- [ ] Click "Import Students"
- [ ] **Expected:** Success message with count (e.g., "2 students added")
- [ ] **Check console output** for generated passwords
- [ ] Navigate to database or try logging in with imported student
- [ ] **Expected:** Students can login with generated passwords

---

## Test Suite 7: Performance & UI

### 7.1 Page Load Times
- [ ] All pages load within 2 seconds
- [ ] No broken images or missing CSS
- [ ] NSUT logo displays correctly on all pages

### 7.2 Responsive Design
- [ ] Resize browser window to mobile size
- [ ] **Expected:** Layout adjusts properly
- [ ] Navigation collapses to hamburger menu
- [ ] Tables become scrollable

### 7.3 Navigation Flow
- [ ] All navigation links work correctly
- [ ] Clicking logo returns to home page
- [ ] Breadcrumbs (if any) work correctly

---

## Test Summary

### Pass Criteria
- [ ] All admin functions work correctly
- [ ] All student functions work correctly
- [ ] All company functions work correctly
- [ ] All edge cases handled gracefully
- [ ] Data integrity maintained
- [ ] No critical errors in console
- [ ] UI is clean and functional

### Known Limitations (Document these)
1. Email functionality not implemented (passwords printed to console)
2. Calendar view for interviews is basic
3. No export functionality for reports

---

## Bug Report Template

If you find any issues, document them like this:

**Bug #:** [Number]  
**Severity:** [Critical/High/Medium/Low]  
**Component:** [Admin/Student/Company/Database]  
**Steps to Reproduce:**  
1. Step 1
2. Step 2
3. Step 3

**Expected Behavior:** [What should happen]  
**Actual Behavior:** [What actually happens]  
**Error Message:** [If any]  
**Screenshot:** [If applicable]

---

## Completion Checklist

- [ ] All test suites completed
- [ ] All major features working
- [ ] Database integrity verified
- [ ] Security measures tested
- [ ] Documentation reviewed
- [ ] Ready for demonstration

---

**Testing Completed By:** _______________  
**Date:** _______________  
**Total Pass Rate:** _____ / _____  
**Status:** ☐ Pass ☐ Fail ☐ Needs Review

---

**Project is ready for viva demonstration! ✅**
