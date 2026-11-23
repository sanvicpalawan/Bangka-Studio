@echo off
cd /d "%~dp0"
where py >nul 2>&1
if %errorlevel%==0 (
  py -3 STUDIO.py
) else (
  where python >nul 2>&1
  if %errorlevel%==0 (
    python STUDIO.py
  ) else (
    echo Python 3 was not found. Install Python 3, then run START-STUDIO.bat again.
  )
)
echo.
echo Press any key to close this window.
pause >nul
