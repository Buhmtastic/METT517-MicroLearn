@echo off
chcp 65001 > nul
echo ========================================
echo MicroLearn AI - Initial Setup
echo ========================================
echo.

echo [1/3] Creating Python virtual environment...
cd backend
python -m venv venv
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH.
    echo Python 3.8 or higher is required.
    pause
    exit /b 1
)

echo [2/3] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo [3/3] Installing required packages... (This may take a few minutes)
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Package installation failed
    pause
    exit /b 1
)

cd ..
echo.
echo ========================================
echo Setup completed successfully!
echo Now run 'MicroLearn.bat' to start the app.
echo ========================================
echo.
pause
