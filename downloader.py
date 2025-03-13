import os
import yt_dlp
import instaloader

# Lokasi penyimpanan video/audio
SAVE_PATH = "/storage/emulated/0/Download/"
os.makedirs(SAVE_PATH, exist_ok=True)

def download_video(url, audio_only=False, custom_filename=None):
    """Mengunduh video atau audio dari YouTube, TikTok, dan Facebook"""

    # Menentukan format penyimpanan
    if custom_filename:
        output_filename = os.path.join(SAVE_PATH, f"{custom_filename}.%(ext)s")
    else:
        output_filename = os.path.join(SAVE_PATH, "%(id)s.%(ext)s")

    ydl_opts = {
        'format': 'bestaudio/best' if audio_only else 'best',
        'outtmpl': output_filename,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }] if audio_only else []
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def download_instagram(url, custom_filename=None):
    """Mengunduh video dari Instagram"""
    
    loader = instaloader.Instaloader(dirname_pattern=SAVE_PATH)
    post_shortcode = url.split("/")[-2]

    try:
        loader.download_post(instaloader.Post.from_shortcode(loader.context, post_shortcode), target="Instagram")
        print("✅ Unduhan selesai!")
    except Exception as e:
        print(f"❌ Gagal mengunduh: {e}")

if __name__ == "__main__":
    print("\n===== Universal Video & Audio Downloader =====\n")

    # Memasukkan URL
    url = input("Masukkan URL video: ").strip()

    # Menampilkan opsi format unduhan secara vertikal dengan keterangan tambahan
    print("\nPilih format unduhan:")
    print("1. Video (Default)")
    print("2. Audio (MP3)")
    print("   Kosongkan dan tekan Enter untuk memilih opsi 1 (Video)")

    # Memilih format (default: Video)
    pilihan = input("Masukkan pilihan (1/2): ").strip()
    audio_only = True if pilihan == "2" else False

    # Memasukkan nama file (default: ID)
    custom_filename = input("Masukkan nama file (kosongkan untuk default): ").strip()
    custom_filename = custom_filename if custom_filename else None

    # Menjalankan proses unduhan
    download_video(url, audio_only=audio_only, custom_filename=custom_filename)
