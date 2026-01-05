@echo off
REM Quick Start Script for YouTube Downloader

color 0B
echo ================================================================
echo          YouTube Downloader - Quick Start
echo ================================================================
echo.

REM Check if virtual environment exists
if exist .venv (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
) else (
    echo No virtual environment found. Using system Python...
)

echo.
echo Checking setup...
python setup_check.py

echo.
echo ================================================================
echo.
echo Press any key to start the YouTube Downloader...
pause >nul

python youtube_downloader.py

pause

