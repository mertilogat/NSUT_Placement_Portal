@echo off
echo ================================================
echo NSUT Placement Portal - Starting Application
echo ================================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing/updating dependencies...
pip install -r requirements.txt

echo.
echo ================================================
echo Starting Flask application...
echo Access the portal at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo ================================================
echo.

python app.py

pause
