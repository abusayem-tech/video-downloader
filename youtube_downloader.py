#!/usr/bin/env python3
"""
YouTube Video/Audio Downloader
A simple script to download YouTube videos or audio using yt-dlp
"""

import os
import sys
from pathlib import Path

try:
    import yt_dlp
except ImportError:
    print("Error: yt-dlp is not installed!")
    print("Please install it using: pip install -r requirements.txt")
    sys.exit(1)


def get_download_path():
    """Get the downloads directory path"""
    downloads_dir = Path.home() / "Downloads" / "YouTube"
    downloads_dir.mkdir(parents=True, exist_ok=True)
    return str(downloads_dir)


def choose_custom_path():
    """Let user choose a custom download path"""
    print("\n" + "="*60)
    print("Choose Download Location:")
    print("="*60)
    print(f"\n1. Default: {get_download_path()}")
    print("2. Custom path")
    
    choice = input("\nEnter your choice (1-2): ").strip()
    
    if choice == '2':
        custom_path = input("\nEnter custom path (e.g., C:\\MyVideos): ").strip()
        if custom_path:
            try:
                path_obj = Path(custom_path)
                path_obj.mkdir(parents=True, exist_ok=True)
                print(f"✅ Using custom path: {custom_path}")
                return str(path_obj)
            except Exception as e:
                print(f"❌ Error with custom path: {e}")
                print(f"Using default path instead.")
                return get_download_path()
    
    return get_download_path()


def get_available_formats(url):
    """Get available video formats for a URL"""
    try:
        ydl_opts = {'quiet': True, 'no_warnings': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            
            # Filter for video+audio or video-only formats
            video_formats = []
            seen_resolutions = set()
            
            for f in formats:
                if f.get('vcodec') != 'none':  # Has video
                    resolution = f.get('resolution', 'unknown')
                    height = f.get('height', 0)
                    fps = f.get('fps', 0)
                    ext = f.get('ext', 'unknown')
                    format_id = f.get('format_id', '')
                    filesize = f.get('filesize', 0)
                    
                    if height and height not in seen_resolutions:
                        seen_resolutions.add(height)
                        video_formats.append({
                            'format_id': format_id,
                            'resolution': f"{height}p",
                            'ext': ext,
                            'fps': fps,
                            'filesize': filesize,
                            'height': height
                        })
            
            # Sort by height (quality)
            video_formats.sort(key=lambda x: x['height'], reverse=True)
            return video_formats[:10]  # Return top 10 qualities
            
    except Exception as e:
        print(f"❌ Error getting formats: {e}")
        return []


def choose_video_quality(url):
    """Let user choose video quality"""
    print("\n⏳ Fetching available qualities...")
    formats = get_available_formats(url)
    
    if not formats:
        print("⚠️  Could not fetch qualities. Using best quality.")
        return 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
    
    print("\n" + "="*60)
    print("Available Video Qualities:")
    print("="*60)
    print("\n0. Best Quality (Auto)")
    
    for idx, fmt in enumerate(formats, 1):
        size_str = f" (~{fmt['filesize'] // (1024*1024)}MB)" if fmt['filesize'] else ""
        fps_str = f" {fmt['fps']}fps" if fmt['fps'] else ""
        print(f"{idx}. {fmt['resolution']}{fps_str} ({fmt['ext']}){size_str}")
    
    print("\n" + "="*60)
    
    try:
        choice = input(f"\nChoose quality (0-{len(formats)}): ").strip()
        choice_num = int(choice)
        
        if choice_num == 0:
            return 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
        elif 1 <= choice_num <= len(formats):
            selected = formats[choice_num - 1]
            # Format string to get the specific quality
            format_str = f"bestvideo[height<={selected['height']}][ext=mp4]+bestaudio[ext=m4a]/best[height<={selected['height']}]"
            print(f"✅ Selected: {selected['resolution']}")
            return format_str
        else:
            print("⚠️  Invalid choice. Using best quality.")
            return 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
    except:
        print("⚠️  Invalid input. Using best quality.")
        return 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'


def choose_audio_quality():
    """Let user choose audio quality/bitrate"""
    print("\n" + "="*60)
    print("Choose Audio Quality:")
    print("="*60)
    print("\n1. High (320 kbps)")
    print("2. Medium (192 kbps) - Recommended")
    print("3. Low (128 kbps)")
    
    choice = input("\nEnter your choice (1-3, default 2): ").strip()
    
    quality_map = {
        '1': '320',
        '2': '192',
        '3': '128'
    }
    
    quality = quality_map.get(choice, '192')
    print(f"✅ Selected: {quality} kbps")
    return quality


def download_video(url, download_path, format_string=None):
    """Download video with chosen quality"""
    if format_string is None:
        format_string = choose_video_quality(url)
    
    print(f"\n📥 Downloading video from: {url}")
    print(f"📁 Saving to: {download_path}\n")
    
    ydl_opts = {
        'format': format_string,
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
        'progress_hooks': [progress_hook],
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("\n✅ Video downloaded successfully!")
        print(f"📁 Location: {download_path}")
    except Exception as e:
        print(f"\n❌ Error downloading video: {str(e)}")


def download_audio(url, download_path, quality=None):
    """Download audio only in MP3 format with chosen quality"""
    if quality is None:
        quality = choose_audio_quality()
    
    print(f"\n📥 Downloading audio from: {url}")
    print(f"📁 Saving to: {download_path}\n")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': quality,
        }],
        'progress_hooks': [progress_hook],
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"\n✅ Audio downloaded successfully!")
        print(f"📁 Location: {download_path}")
    except Exception as e:
        print(f"\n❌ Error downloading audio: {str(e)}")


def download_playlist(url, download_path, audio_only=False, format_string=None, audio_quality='192'):
    """Download entire playlist with quality options"""
    print(f"\n📥 Downloading playlist from: {url}")
    print(f"📁 Saving to: {download_path}\n")
    
    if audio_only:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(download_path, '%(playlist)s/%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': audio_quality,
            }],
            'progress_hooks': [progress_hook],
        }
    else:
        if format_string is None:
            format_string = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
        ydl_opts = {
            'format': format_string,
            'outtmpl': os.path.join(download_path, '%(playlist)s/%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'progress_hooks': [progress_hook],
        }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"\n✅ Playlist downloaded successfully!")
        print(f"📁 Location: {download_path}")
    except Exception as e:
        print(f"\n❌ Error downloading playlist: {str(e)}")


def progress_hook(d):
    """Display download progress"""
    if d['status'] == 'downloading':
        try:
            percent = d.get('_percent_str', 'N/A')
            speed = d.get('_speed_str', 'N/A')
            eta = d.get('_eta_str', 'N/A')
            print(f"\rProgress: {percent} | Speed: {speed} | ETA: {eta}", end='', flush=True)
        except:
            pass
    elif d['status'] == 'finished':
        print("\n🔄 Processing file...")


def get_video_info(url):
    """Get video information without downloading"""
    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            print("\n" + "="*60)
            print(f"Title: {info.get('title', 'N/A')}")
            print(f"Duration: {info.get('duration', 0) // 60} minutes {info.get('duration', 0) % 60} seconds")
            print(f"Views: {info.get('view_count', 'N/A'):,}")
            print(f"Uploader: {info.get('uploader', 'N/A')}")
            print(f"Upload Date: {info.get('upload_date', 'N/A')}")
            print("="*60 + "\n")
    except Exception as e:
        print(f"❌ Error getting video info: {str(e)}")


def display_menu(current_path):
    """Display the main menu"""
    print("\n" + "="*60)
    print("🎥 YouTube Video/Audio Downloader 🎵")
    print("="*60)
    print("\n1. Download Video (MP4) - With Quality Selection")
    print("2. Download Audio Only (MP3) - With Quality Selection")
    print("3. Download Playlist (Video)")
    print("4. Download Playlist (Audio)")
    print("5. Get Video Info")
    print("6. Change Download Path")
    print("7. Exit")
    print(f"\n📁 Current Path: {current_path}")
    print("="*60)


def main():
    """Main function"""
    download_path = get_download_path()
    
    while True:
        display_menu(download_path)
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == '7':
            print("\n👋 Thank you for using YouTube Downloader! Goodbye!")
            break
        
        if choice == '6':
            download_path = choose_custom_path()
            continue
        
        if choice not in ['1', '2', '3', '4', '5']:
            print("\n❌ Invalid choice! Please enter a number between 1-7.")
            continue
        
        url = input("\nEnter YouTube URL: ").strip()
        
        if not url:
            print("❌ URL cannot be empty!")
            continue
        
        if choice == '1':
            # Video with quality selection
            download_video(url, download_path)
        elif choice == '2':
            # Audio with quality selection
            download_audio(url, download_path)
        elif choice == '3':
            # Playlist video - ask for quality
            print("\n⚠️  Note: Quality will apply to all videos in playlist")
            use_quality = input("Choose quality for each video? (y/n, default n): ").strip().lower()
            if use_quality == 'y':
                # For playlists, we'll use best quality by default
                # User can modify the code to get first video for quality reference
                print("Using best quality for all videos in playlist")
                download_playlist(url, download_path, audio_only=False)
            else:
                download_playlist(url, download_path, audio_only=False)
        elif choice == '4':
            # Playlist audio - ask for quality
            audio_quality = choose_audio_quality()
            download_playlist(url, download_path, audio_only=True, audio_quality=audio_quality)
        elif choice == '5':
            get_video_info(url)
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Download interrupted by user. Exiting...")
        sys.exit(0)

