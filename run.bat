@echo off
title NEXUS-ZERO Industrial Closed-Loop Manufacturing System
color 0B
cls
echo =====================================================================
echo  NEXUS-ZERO // CLOSED-LOOP ZERO-DEFECT MANUFACTURING SYSTEM
echo  Edge AI Automated Optical Inspection ^& PLC Machine Controller
echo =====================================================================
echo.
echo [1/3] Checking Python installation...
python --version
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    pause
    exit /b
)

echo.
echo [2/3] Verifying core dependencies...
python -m pip install -r requirements.txt --quiet

echo.
echo [3/3] Launching Gigafactory Command Center on localhost:8501...
echo ---------------------------------------------------------------------
echo  Localhost URL: http://localhost:8501
echo  To connect your Mobile Phone via USB:
echo    - Launch DroidCam or Iriun Webcam on PC ^& Phone (USB Mode)
echo    - In UI, select "Mobile Phone Camera via USB" and choose Index 1 or 2
echo ---------------------------------------------------------------------
echo.
python -m streamlit run app.py --server.port=8501 --server.headless=false

pause
