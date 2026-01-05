#!/usr/bin/env python3
"""
Setup Checker for YouTube Downloader
Verifies all requirements are installed correctly
"""

import sys
import subprocess
import os

# Fix Windows console encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass


def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)


def check_python():
    """Check Python version"""
    print("\n[*] Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"[OK] Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"[FAIL] Python {version.major}.{version.minor}.{version.micro} - Need Python 3.7 or higher")
        return False


def check_yt_dlp():
    """Check if yt-dlp is installed"""
    print("\n[*] Checking yt-dlp...")
    try:
        import yt_dlp
        version = yt_dlp.version.__version__
        print(f"[OK] yt-dlp {version}")
        return True
    except ImportError:
        print("[FAIL] yt-dlp is NOT installed")
        print("       Install with: pip install -r requirements.txt")
        return False


def check_ffmpeg():
    """Check if FFmpeg is installed"""
    print("\n[*] Checking FFmpeg...")
    try:
        result = subprocess.run(
            ['ffmpeg', '-version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"[OK] {version_line}")
            return True
        else:
            print("[FAIL] FFmpeg found but not working properly")
            return False
    except FileNotFoundError:
        print("[WARN] FFmpeg is NOT installed")
        print("       Note: FFmpeg is optional but needed for audio (MP3) downloads")
        print("       See README.md for installation instructions")
        return False
    except Exception as e:
        print(f"[FAIL] Error checking FFmpeg: {str(e)}")
        return False


def check_internet():
    """Check internet connection"""
    print("\n[*] Checking internet connection...")
    try:
        import urllib.request
        urllib.request.urlopen('https://www.youtube.com', timeout=5)
        print("[OK] Internet connection active")
        return True
    except:
        print("[WARN] No internet connection detected")
        print("       Internet is required for downloading videos")
        return False


def check_download_directory():
    """Check if download directory is accessible"""
    print("\n[*] Checking download directory...")
    from pathlib import Path
    downloads_dir = Path.home() / "Downloads" / "YouTube"
    try:
        downloads_dir.mkdir(parents=True, exist_ok=True)
        print(f"[OK] Download directory ready: {downloads_dir}")
        return True
    except Exception as e:
        print(f"[FAIL] Cannot create download directory: {str(e)}")
        return False


def main():
    """Main function"""
    print_header("YouTube Downloader - Setup Checker")
    
    results = {
        'Python': check_python(),
        'yt-dlp': check_yt_dlp(),
        'FFmpeg': check_ffmpeg(),
        'Internet': check_internet(),
        'Download Directory': check_download_directory()
    }
    
    print_header("Summary")
    
    all_ok = True
    for component, status in results.items():
        if component == 'FFmpeg':
            # FFmpeg is optional
            symbol = "[OK]" if status else "[WARN]"
            status_text = "Installed" if status else "Optional (needed for MP3)"
        else:
            symbol = "[OK]" if status else "[FAIL]"
            status_text = "Ready" if status else "MISSING"
            if not status and component != 'FFmpeg':
                all_ok = False
        
        print(f"{symbol} {component}: {status_text}")
    
    print("\n" + "="*60)
    
    if all_ok:
        print("\n[SUCCESS] All required components are ready!")
        print("          You can now run: python youtube_downloader.py")
    else:
        print("\n[WARNING] Some required components are missing.")
        print("          Please install missing components and run this check again.")
    
    if not results['FFmpeg']:
        print("\n[NOTE] Without FFmpeg, you can still download videos (MP4)")
        print("       but audio-only downloads (MP3) will not work.")
        print("       Run: install_ffmpeg.bat for installation help")
    
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Check interrupted by user.")
        sys.exit(0)

