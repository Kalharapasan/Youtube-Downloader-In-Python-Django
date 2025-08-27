# YouTube & Facebook Video Downloader (Django)

A modern web application to download YouTube videos, YouTube playlists, and Facebook videos in various formats and qualities. Built with Django and yt-dlp.

<img width="702" height="419" alt="image" src="https://github.com/user-attachments/assets/8ea99703-a852-4692-a86e-9d18cf5b0fd1" />


## Features
- Download single YouTube videos, YouTube playlists (as zip), and Facebook videos
- Choose video quality (720p, 1080p, 1440p, 4K) and format (MP4, MP3, WebM)
- Simple, responsive web UI
- Progress and error feedback

## Requirements
- Python 3.8+
- Django 4.x or 5.x
- yt-dlp
- ffmpeg (must be installed and in your system PATH)

## Setup
1. **Clone the repository:**
   ```
   git clone <your-repo-url>
   cd Youtube-Downloader-In-Python-Django
   ```
2. **Create and activate a virtual environment:**
   ```
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/Mac:
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```
   If `requirements.txt` is missing, install manually:
   ```
   pip install django yt-dlp
   ```
4. **Install ffmpeg:**
   - Download from https://www.gyan.dev/ffmpeg/builds/
   - Extract and add the `bin` folder to your system PATH
   - Verify with `ffmpeg -version`

5. **Run migrations:**
   ```
   python manage.py migrate
   ```
6. **Start the server:**
   ```
   python manage.py runserver
   ```
7. **Open in your browser:**
   - Go to http://127.0.0.1:8000/

## Usage
- Select the download type (YouTube Video, Playlist, or Facebook Video)
- Paste the URL
- Choose quality and format
- Click Download

## Troubleshooting
- **ffmpeg not found:**
  - Ensure ffmpeg is installed and its `bin` directory is in your PATH
- **Format not available:**
  - Try a different quality or format
- **Permission errors:**
  - Run your terminal as administrator

## License
MIT

## Credits
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [ffmpeg](https://ffmpeg.org/)
- Django
