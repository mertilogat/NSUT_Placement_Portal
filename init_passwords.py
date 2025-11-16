"""
Helper script to generate password hashes for manual database updates
Run this to get properly formatted password hashes for the seed data
"""

from werkzeug.security import generate_password_hash

print("=" * 60)
print("NSUT Placement Portal - Password Hash Generator")
print("=" * 60)
print()

# Generate hash for admin password
admin_password = "admin123"
admin_hash = generate_password_hash(admin_password)

print("DEFAULT ADMIN CREDENTIALS:")
print(f"Email: admin@nsut.ac.in")
print(f"Password: {admin_password}")
print(f"Hash: {admin_hash}")
print()

# Generate hash for test company password
company_password = "company123"
company_hash = generate_password_hash(company_password)

print("TEST COMPANY CREDENTIALS:")
print(f"Password: {company_password}")
print(f"Hash: {company_hash}")
print()

# Generate hash for test student password
student_password = "student123"
student_hash = generate_password_hash(student_password)

print("TEST STUDENT CREDENTIALS:")
print(f"Password: {student_password}")
print(f"Hash: {student_hash}")
print()

print("=" * 60)
print("INSTRUCTIONS:")
print("=" * 60)
print()
print("After importing db/nsut_placement.sql, run these SQL commands")
print("to set proper passwords for testing:")
print()
print("-- Update admin password")
print(f"UPDATE pc_admins SET password_hash = '{admin_hash}' WHERE id = 1;")
print()
print("-- Update company passwords (for testing)")
print(f"UPDATE companies SET password_hash = '{company_hash}' WHERE id IN (1,2,3);")
print()
print("-- Update student passwords (for testing)")
print(f"UPDATE students SET password_hash = '{student_hash}' WHERE id IN (1,2,3,4,5,6,7,8,9,10);")
print()
print("=" * 60)
print()
print("Or just register new accounts through the web interface!")
print()
