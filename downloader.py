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
        'outtmpl': os.path.join(SAVE_PATH, '%(id)s.%(ext)s'),
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

    try:
        loader.download_post(instaloader.Post.from_shortcode(loader.context, post_shortcode), target="Instagram")
        print("✅ Unduhan Instagram berhasil!")
    except Exception as e:
        print(f"❌ Error saat mengunduh: {e}")

if _name_ == "_main_":
    print("=== Universal Video & Audio Downloader ===")

    # Meminta input URL
    video_url = input("Masukkan URL video: ").strip()

    if not video_url:
        print("❌ URL tidak boleh kosong!")
        exit()

    # Menentukan pilihan unduhan
    print("\n1. Download Video (Default)")
    print("2. Download Audio (MP3)")
    choice = input("Pilih mode (tekan Enter untuk Video): ").strip()

    # Proses unduhan berdasarkan pilihan
    if "instagram.com" in video_url:
        download_instagram(video_url)
    elif choice == "2":
        download_video(video_url, audio_only=True)
    else:
        download_video(video_url)
