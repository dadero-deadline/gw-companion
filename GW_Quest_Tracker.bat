@echo off
REM Offline build + open static file (no server)
cd /d "%~dp0"

REM Build the latest HTMLs
set GW_COMPANION_BUILD_ONLY=1
python gw_tracker.py --build-only

REM Open the local static page
start "" "%CD%\index.html"
exit /b 0
