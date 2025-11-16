# Replit Deployment Note

## Important Information

This **NSUT Placement Portal** project is specifically designed to run on **local XAMPP** environment with MySQL database, as per the DBMS project requirements.

### Why This Project Cannot Run on Replit

1. **MySQL Requirement:** The project uses MySQL database, which is not available in standard Replit stacks
2. **XAMPP Design:** The application is designed to connect to XAMPP's MySQL instance (localhost)
3. **Academic Requirements:** The project must demonstrate direct SQL queries without ORMs, designed for local teacher demonstration

### How to Use This Project

This Replit workspace serves as a **code repository and development environment** where you can:

✅ **View and edit all code files**  
✅ **Review the complete project structure**  
✅ **Download the entire project as ZIP**  
✅ **Push to GitHub for version control**  
✅ **Study the implementation**

### To Actually Run the Project

You **must** deploy it locally on your machine with XAMPP. Follow these steps:

#### Option 1: Download from Replit

1. Click the three dots menu (⋮) in Replit
2. Select **"Download as ZIP"**
3. Extract on your local machine
4. Follow the detailed instructions in `README.md`

#### Option 2: Clone via Git

1. Push this Replit project to GitHub:
   ```bash
   # In Replit Shell
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. On your local machine:
   ```bash
   git clone YOUR_GITHUB_REPO_URL
   cd nsut-placement-portal
   ```

3. Follow the setup instructions in `README.md`

### Local Setup Requirements

Once you have the files locally, you need:

1. **XAMPP** (for Apache + MySQL)
   - Download: https://www.apachefriends.org/

2. **Python 3.7+**
   - Download: https://www.python.org/downloads/

3. Follow step-by-step instructions in **README.md**

### Quick Start After Download

```bash
# 1. Start XAMPP MySQL service

# 2. Import database
mysql -u root -p < db/nsut_placement.sql

# 3. Set up Python environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# 4. Run application
python app.py

# 5. Open browser
http://localhost:5000
```

### Files Available in This Repository

All project files are ready and complete:

- ✅ Complete database schema (`db/nsut_placement.sql`)
- ✅ Flask application (`app.py`)
- ✅ All HTML templates
- ✅ Configuration files
- ✅ Comprehensive documentation
- ✅ Setup scripts (Windows & Linux)
- ✅ Viva preparation notes
- ✅ Testing checklist

### Database Schema Available

Even though MySQL isn't running here, you can:
- View the complete schema in `db/nsut_placement.sql`
- Study the ER diagram documentation in `db/ER_DIAGRAM_EXPLANATION.md`
- Review all SQL queries in `viva_notes.md`

### Teacher Demonstration

For your teacher's viva:

1. **Download this project** from Replit as ZIP
2. **Set up XAMPP** on demonstration computer
3. **Run the application** locally following `README.md`
4. **Use** `MANUAL_TEST_CHECKLIST.md` for demonstration flow
5. **Refer to** `viva_notes.md` for Q&A preparation

### Alternative: PostgreSQL Version (If Needed)

If you need a version that runs on Replit (for development/preview), I can create an alternative version using PostgreSQL. However, note that:
- It won't use XAMPP
- It won't demonstrate the exact local setup required for your project
- The MySQL version is what you should submit

---

## Summary

**This Replit workspace is your code repository.**  
**Download it and run it on your local XAMPP setup for the actual application.**

All files are complete and ready for local deployment! 🚀

---

**For detailed setup instructions, see: `README.md`**
