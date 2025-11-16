"""
NSUT Placement Portal - Project Validation
This script validates the project structure is complete
"""

import os
import sys

print("=" * 70)
print(" NSUT PLACEMENT PORTAL - PROJECT STATUS")
print("=" * 70)
print()

# Check essential files
essential_files = [
    "app.py",
    "config.py",
    "db.py",
    "requirements.txt",
    "README.md",
    "viva_notes.md",
    "MANUAL_TEST_CHECKLIST.md",
    "db/nsut_placement.sql",
    "db/ER_DIAGRAM_EXPLANATION.md"
]

print("📁 Checking Project Files...")
print("-" * 70)
all_present = True
for file_path in essential_files:
    exists = os.path.exists(file_path)
    status = "✅" if exists else "❌"
    print(f"{status} {file_path}")
    if not exists:
        all_present = False

print()

# Check templates
template_count = len([f for f in os.listdir("templates") if f.endswith(".html")])
print(f"📄 HTML Templates: {template_count} files")

# Check static assets
if os.path.exists("static/images/nsut_logo.png"):
    print("🖼️  NSUT Logo: Present")
else:
    print("⚠️  NSUT Logo: Missing")

print()
print("=" * 70)
print(" IMPORTANT: THIS PROJECT REQUIRES LOCAL XAMPP SETUP")
print("=" * 70)
print()
print("⚠️  This project uses MySQL database which is NOT available in Replit.")
print()
print("📖 To run this project:")
print("   1. Download this project as ZIP from Replit")
print("   2. Install XAMPP on your local machine")
print("   3. Follow detailed instructions in README.md")
print()
print("📚 Documentation Available:")
print("   • README.md - Complete setup instructions")
print("   • viva_notes.md - Viva preparation guide")
print("   • MANUAL_TEST_CHECKLIST.md - Testing guide")
print("   • REPLIT_DEPLOYMENT_NOTE.md - Deployment info")
print()
print("=" * 70)
print()

if all_present:
    print("✅ All essential files are present!")
    print("✅ Project is ready for download and local deployment")
    sys.exit(0)
else:
    print("⚠️  Some files are missing. Please check the file list above.")
    sys.exit(1)
