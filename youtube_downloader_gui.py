#!/usr/bin/env python3
"""
YouTube Downloader - Windows GUI Application
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import sys
from pathlib import Path

try:
    import yt_dlp
except ImportError:
    print("Error: yt-dlp is not installed!")
    print("Please run: pip install -r requirements.txt")
    sys.exit(1)


class YouTubeDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Video/Audio Downloader")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        
        # Default download path
        self.download_path = str(Path.home() / "Downloads" / "YouTube")
        Path(self.download_path).mkdir(parents=True, exist_ok=True)
        
        # Currently downloading flag
        self.is_downloading = False
        
        self.setup_ui()
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="YouTube Downloader", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=10)
        
        # URL Entry
        ttk.Label(main_frame, text="YouTube URL:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.url_entry = ttk.Entry(main_frame, width=60)
        self.url_entry.grid(row=1, column=1, columnspan=2, pady=5, padx=5)
        
        # Download Type
        ttk.Label(main_frame, text="Download Type:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.download_type = tk.StringVar(value="video")
        type_frame = ttk.Frame(main_frame)
        type_frame.grid(row=2, column=1, columnspan=2, sticky=tk.W, pady=5)
        ttk.Radiobutton(type_frame, text="Video (MP4)", variable=self.download_type, 
                       value="video", command=self.update_quality_options).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(type_frame, text="Audio (MP3)", variable=self.download_type, 
                       value="audio", command=self.update_quality_options).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(type_frame, text="Playlist (Video)", variable=self.download_type, 
                       value="playlist_video", command=self.update_quality_options).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(type_frame, text="Playlist (Audio)", variable=self.download_type, 
                       value="playlist_audio", command=self.update_quality_options).pack(side=tk.LEFT, padx=5)
        
        # Quality Selection
        ttk.Label(main_frame, text="Quality:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.quality_var = tk.StringVar(value="best")
        self.quality_combo = ttk.Combobox(main_frame, textvariable=self.quality_var, 
                                         state="readonly", width=30)
        self.quality_combo['values'] = ("Best Quality", "1080p", "720p", "480p", "360p")
        self.quality_combo.grid(row=3, column=1, sticky=tk.W, pady=5, padx=5)
        
        # Download Path
        ttk.Label(main_frame, text="Save to:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.path_entry = ttk.Entry(main_frame, width=45)
        self.path_entry.insert(0, self.download_path)
        self.path_entry.grid(row=4, column=1, pady=5, padx=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_path).grid(row=4, column=2, pady=5)
        
        # Buttons Frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=3, pady=15)
        
        self.download_btn = ttk.Button(button_frame, text="Download", 
                                       command=self.start_download, width=20)
        self.download_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Get Video Info", 
                  command=self.get_video_info, width=20).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Clear Log", 
                  command=self.clear_log, width=15).pack(side=tk.LEFT, padx=5)
        
        # Progress Bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate', length=600)
        self.progress.grid(row=6, column=0, columnspan=3, pady=10)
        
        # Status Label
        self.status_label = ttk.Label(main_frame, text="Ready", foreground="green")
        self.status_label.grid(row=7, column=0, columnspan=3)
        
        # Log Text Area
        ttk.Label(main_frame, text="Log:").grid(row=8, column=0, sticky=tk.W, pady=5)
        self.log_text = scrolledtext.ScrolledText(main_frame, width=80, height=15, 
                                                  wrap=tk.WORD, state='disabled')
        self.log_text.grid(row=9, column=0, columnspan=3, pady=5)
        
        self.update_quality_options()
    
    def update_quality_options(self):
        """Update quality options based on download type"""
        dtype = self.download_type.get()
        if dtype in ["audio", "playlist_audio"]:
            self.quality_combo['values'] = ("320 kbps (High)", "192 kbps (Medium)", "128 kbps (Low)")
            self.quality_var.set("192 kbps (Medium)")
        else:
            self.quality_combo['values'] = ("Best Quality", "1080p", "720p", "480p", "360p")
            self.quality_var.set("Best Quality")
    
    def browse_path(self):
        """Browse for download directory"""
        folder = filedialog.askdirectory(initialdir=self.download_path)
        if folder:
            self.download_path = folder
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, folder)
            self.log(f"Download path changed to: {folder}")
    
    def log(self, message):
        """Add message to log"""
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
    
    def clear_log(self):
        """Clear log text"""
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state='disabled')
    
    def set_status(self, message, color="black"):
        """Update status label"""
        self.status_label.config(text=message, foreground=color)
    
    def get_format_string(self):
        """Get yt-dlp format string based on quality selection"""
        quality = self.quality_var.get()
        dtype = self.download_type.get()
        
        if dtype in ["audio", "playlist_audio"]:
            # Audio - return bitrate
            if "320" in quality:
                return "320"
            elif "128" in quality:
                return "128"
            else:
                return "192"
        else:
            # Video
            if quality == "Best Quality":
                return "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
            elif quality == "1080p":
                return "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]"
            elif quality == "720p":
                return "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720]"
            elif quality == "480p":
                return "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480]"
            elif quality == "360p":
                return "bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]/best[height<=360]"
            else:
                return "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
    
    def progress_hook(self, d):
        """Hook for download progress"""
        if d['status'] == 'downloading':
            try:
                percent = d.get('_percent_str', 'N/A').strip()
                speed = d.get('_speed_str', 'N/A').strip()
                self.set_status(f"Downloading: {percent} | Speed: {speed}", "blue")
            except:
                pass
        elif d['status'] == 'finished':
            self.set_status("Processing file...", "blue")
    
    def get_video_info(self):
        """Get video information"""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Warning", "Please enter a YouTube URL!")
            return
        
        self.log(f"Fetching info for: {url}")
        self.set_status("Fetching video info...", "blue")
        
        def fetch_info():
            try:
                with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                    info = ydl.extract_info(url, download=False)
                    title = info.get('title', 'N/A')
                    duration = info.get('duration', 0)
                    duration_str = f"{duration // 60}:{duration % 60:02d}"
                    uploader = info.get('uploader', 'N/A')
                    views = info.get('view_count', 'N/A')
                    
                    self.log("="*60)
                    self.log(f"Title: {title}")
                    self.log(f"Duration: {duration_str}")
                    self.log(f"Uploader: {uploader}")
                    self.log(f"Views: {views:,}" if isinstance(views, int) else f"Views: {views}")
                    self.log("="*60)
                    self.set_status("Video info retrieved", "green")
            except Exception as e:
                self.log(f"Error: {str(e)}")
                self.set_status("Error getting info", "red")
        
        threading.Thread(target=fetch_info, daemon=True).start()
    
    def start_download(self):
        """Start download in separate thread"""
        if self.is_downloading:
            messagebox.showinfo("Info", "Download already in progress!")
            return
        
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Warning", "Please enter a YouTube URL!")
            return
        
        download_path = self.path_entry.get().strip()
        if not download_path:
            messagebox.showwarning("Warning", "Please select a download path!")
            return
        
        # Create directory if doesn't exist
        try:
            Path(download_path).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            messagebox.showerror("Error", f"Cannot create directory: {str(e)}")
            return
        
        self.is_downloading = True
        self.download_btn.config(state='disabled')
        self.progress.start()
        
        # Start download in thread
        thread = threading.Thread(target=self.download, args=(url, download_path), daemon=True)
        thread.start()
    
    def download(self, url, download_path):
        """Perform the download"""
        dtype = self.download_type.get()
        format_str = self.get_format_string()
        
        self.log(f"Starting download: {url}")
        self.log(f"Type: {dtype}")
        self.log(f"Quality: {self.quality_var.get()}")
        self.log(f"Path: {download_path}")
        self.set_status("Downloading...", "blue")
        
        try:
            if dtype in ["audio", "playlist_audio"]:
                # Audio download
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': os.path.join(download_path, 
                                           '%(playlist)s/%(title)s.%(ext)s' if 'playlist' in dtype 
                                           else '%(title)s.%(ext)s'),
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': format_str,
                    }],
                    'progress_hooks': [self.progress_hook],
                }
            else:
                # Video download
                ydl_opts = {
                    'format': format_str,
                    'outtmpl': os.path.join(download_path, 
                                           '%(playlist)s/%(title)s.%(ext)s' if 'playlist' in dtype 
                                           else '%(title)s.%(ext)s'),
                    'merge_output_format': 'mp4',
                    'progress_hooks': [self.progress_hook],
                }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            self.log("Download completed successfully!")
            self.log(f"Saved to: {download_path}")
            self.set_status("Download complete!", "green")
            messagebox.showinfo("Success", "Download completed successfully!")
            
        except Exception as e:
            self.log(f"Error: {str(e)}")
            self.set_status("Download failed", "red")
            messagebox.showerror("Error", f"Download failed: {str(e)}")
        
        finally:
            self.is_downloading = False
            self.download_btn.config(state='normal')
            self.progress.stop()


def main():
    root = tk.Tk()
    app = YouTubeDownloaderGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

