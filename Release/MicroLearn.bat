@echo off
chcp 65001 > nul
echo ========================================
echo MicroLearn AI - Starting...
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "backend\venv\" (
    echo ERROR: Virtual environment not found.
    echo Please run 'setup.bat' first to complete the initial setup.
    echo.
    pause
    exit /b 1
)

REM Check if frontend build exists
if not exist "frontend\build\index.html" (
    echo WARNING: Frontend build files not found.
    echo Please copy React build files to 'frontend\build\' folder.
    echo.
    echo Press any key to continue...
    pause
)

echo [1/2] Activating virtual environment...
call backend\venv\Scripts\activate.bat

echo [2/2] Starting MicroLearn AI server...
echo.
echo ========================================
echo Server is running!
echo Open your browser and go to: http://localhost:8000
echo.
echo Press Ctrl+C to stop the server.
echo ========================================
echo.

REM Wait 3 seconds and open browser
timeout /t 3 /nobreak > nul
start http://localhost:8000

REM Start the server (using port 8000) from the Release directory
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000

REM After server stops
echo.
echo MicroLearn AI has been stopped.
pause
