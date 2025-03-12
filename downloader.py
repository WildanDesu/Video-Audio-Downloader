import os
import yt_dlp
import instaloader

# Lokasi penyimpanan video/audio
SAVE_PATH = "/storage/emulated/0/Download/"  
os.makedirs(SAVE_PATH, exist_ok=True)

def download_video(url, audio_only=False):
    """Mengunduh video atau audio dari YouTube, TikTok, dan Facebook"""
    ydl_opts = {
        'format': 'bestaudio/best' if audio_only else 'best',
        'outtmpl': os.path.join(SAVE_PATH, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }] if audio_only else []
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def download_instagram(url):
    """Mengunduh video dari Instagram"""
    loader = instaloader.Instaloader(dirname_pattern=SAVE_PATH)
    post_shortcode = url.split("/")[-2]
