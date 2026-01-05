# YouTube Video/Audio Downloader

A simple and user-friendly Python script to download YouTube videos and audio files offline.

## Features

✨ **Key Features:**
- Download videos in MP4 format with **quality selection** (360p to 4K)
- Download audio only in MP3 with **bitrate selection** (128/192/320 kbps)
- **Custom download path** - save files anywhere you want
- Download entire playlists (video or audio)
- View video information before downloading
- View available qualities and formats
- Progress tracking with speed and ETA
- Automatic organization of downloads
- User-friendly interactive menu

## Requirements

- Python 3.7 or higher
- Internet connection (for downloading)
- FFmpeg (optional, but recommended for audio conversion)

## Installation

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Install FFmpeg (Optional but Recommended)

FFmpeg is needed for audio extraction and conversion to MP3.

**Windows:**
1. Download FFmpeg from: https://ffmpeg.org/download.html
2. Extract the files
3. Add the `bin` folder to your system PATH

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

## Usage

### Run the script:

```bash
python youtube_downloader.py
```

### Menu Options:

1. **Download Video (MP4)** - Choose quality from available options (360p to 4K)
2. **Download Audio Only (MP3)** - Choose bitrate (128/192/320 kbps)
3. **Download Playlist (Video)** - Downloads all videos from a playlist
4. **Download Playlist (Audio)** - Downloads audio with quality selection
5. **Get Video Info** - Display video information without downloading
6. **Change Download Path** - Set custom folder for downloads
7. **Exit** - Close the program

### Examples:

**Single Video:**
- Choose option 1 or 2
- Paste the YouTube URL (e.g., `https://www.youtube.com/watch?v=dQw4w9WgXcQ`)
- Wait for the download to complete

**Playlist:**
- Choose option 3 or 4
- Paste the playlist URL (e.g., `https://www.youtube.com/playlist?list=PLxxxxxx`)
- All videos will be downloaded to a folder named after the playlist

## Download Location

**Default location:**
- **Windows:** `C:\Users\YourUsername\Downloads\YouTube\`
- **macOS/Linux:** `/Users/YourUsername/Downloads/YouTube/`

**Custom location:**
- Use menu option **6** to set any folder you want
- Examples: `C:\MyVideos`, `D:\Downloads`, `E:\Media`
- Path can be changed anytime during use

## Features Explanation

### Video Quality
- **Choose your quality**: 360p, 480p, 720p, 1080p, 4K (if available)
- See file size estimates before downloading
- FPS information displayed (30fps, 60fps)
- Automatically merges video and audio streams
- Output format: MP4 (widely compatible)

### Audio Quality
- **Choose your bitrate**: 128, 192, or 320 kbps
- Higher bitrate = better quality + larger file
- 192 kbps recommended for most use cases
- 320 kbps for music and studio quality
- 128 kbps perfect for podcasts
- Converts to MP3 format

### Progress Tracking
- Real-time download progress
- Download speed indicator
- Estimated time remaining (ETA)

## Troubleshooting

### "yt-dlp is not installed" Error
```bash
pip install yt-dlp
```

### Audio conversion not working
Install FFmpeg (see Installation Step 2 above)

### "Unable to extract" errors
- Check if the URL is correct
- Some videos may be restricted or unavailable in your region
- Try updating yt-dlp: `pip install --upgrade yt-dlp`

### Permission errors
- Run the script with administrator/sudo privileges
- Check if the Downloads folder is writable

## Legal Notice

⚠️ **Important:** Please respect copyright laws and YouTube's Terms of Service. Only download videos that you have permission to download or that are in the public domain. This tool is for educational and personal use only.

## Updates

To update yt-dlp to the latest version:

```bash
pip install --upgrade yt-dlp
```

## License

This project is open source and available for personal use.

## Support

For issues or questions:
- Check the troubleshooting section above
- Visit the yt-dlp documentation: https://github.com/yt-dlp/yt-dlp

---

**Enjoy downloading! 🎉**

