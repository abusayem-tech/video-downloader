@echo off
REM FFmpeg Installation Helper for Windows
REM This script helps you install FFmpeg on Windows

color 0A
echo ================================================================
echo          FFmpeg Installation Helper for Windows
echo ================================================================
echo.

echo This script will help you install FFmpeg for audio conversion.
echo.
echo OPTION 1: Install with Chocolatey (Recommended - Automatic)
echo --------------------------------------------------------
echo If you have Chocolatey installed, run:
echo.
echo   choco install ffmpeg
echo.
echo Don't have Chocolatey? Install it from: https://chocolatey.org
echo.
echo.
echo OPTION 2: Install with Winget (Windows 11 - Automatic)
echo --------------------------------------------------------
echo If you have Windows 11 or Windows 10 with App Installer:
echo.
echo   winget install ffmpeg
echo.
echo.
echo OPTION 3: Manual Installation (All Windows Versions)
echo --------------------------------------------------------
echo 1. Download FFmpeg from: https://ffmpeg.org/download.html
echo    - Click "Windows builds from gyan.dev"
echo    - Download "ffmpeg-release-essentials.zip"
echo.
echo 2. Extract the ZIP file to a folder (e.g., C:\ffmpeg)
echo.
echo 3. Add FFmpeg to PATH:
echo    - Right-click "This PC" ^> Properties
echo    - Click "Advanced system settings"
echo    - Click "Environment Variables"
echo    - Under "System variables", find "Path" and click "Edit"
echo    - Click "New" and add: C:\ffmpeg\bin
echo    - Click "OK" on all windows
echo.
echo 4. Restart your terminal/command prompt
echo.
echo 5. Test by running: ffmpeg -version
echo.
echo ================================================================
echo.
echo Would you like to try installing FFmpeg now?
echo.
echo [1] Try Winget installation (Windows 10/11)
echo [2] Try Chocolatey installation
echo [3] Open FFmpeg download page in browser
echo [4] Exit
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" goto winget
if "%choice%"=="2" goto choco
if "%choice%"=="3" goto browser
if "%choice%"=="4" goto end

echo Invalid choice. Exiting.
goto end

:winget
echo.
echo Attempting to install FFmpeg with Winget...
winget install ffmpeg
if %errorlevel% equ 0 (
    echo.
    echo FFmpeg installed successfully!
    echo Please restart your terminal and run: python setup_check.py
) else (
    echo.
    echo Winget installation failed. Try another option.
)
pause
goto end

:choco
echo.
echo Attempting to install FFmpeg with Chocolatey...
choco install ffmpeg -y
if %errorlevel% equ 0 (
    echo.
    echo FFmpeg installed successfully!
    echo Please restart your terminal and run: python setup_check.py
) else (
    echo.
    echo Chocolatey installation failed. Try another option.
)
pause
goto end

:browser
echo.
echo Opening FFmpeg download page in your browser...
start https://ffmpeg.org/download.html
echo.
echo After downloading and installing, run: python setup_check.py
pause
goto end

:end
echo.
echo Goodbye!

