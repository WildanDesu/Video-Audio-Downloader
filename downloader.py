import os
import subprocess

# Fungsi untuk mengecek apakah sebuah perintah tersedia
def is_installed(command):
    return subprocess.call(f"command -v {command} > /dev/null 2>&1", shell=True) == 0

# Mengecek apakah dependensi terinstal
dependencies = {
    "yt-dlp": "yt-dlp",
    "ffmpeg": "ffmpeg",
    "instaloader": "instaloader"
}

missing = [pkg for pkg, cmd in dependencies.items() if not is_installed(cmd)]

# Jika ada yang belum terinstal, jalankan set_up.py
if missing:
    print(f"Dependensi berikut belum terinstal: {', '.join(missing)}")
    print("Menjalankan set_up.py untuk menginstal dependensi...\n")
    os.system("python set_up.py")

import sys
import yt_dlp
import instaloader

# Path penyimpanan
DOWNLOAD_PATH = "/sdcard/Download"

def clear_screen():
    os.system("clear")

def banner():
    print("==========================")
    print("     UNIVERSAL TOOLS")
    print("        VERSI 1.3")
    print("    Made By WildanDesu")
    print("==========================\n")

def menu():
    while True:
        clear_screen()
        banner()
        print("Menu:")
        print("1. Video/Audio Downloader")
        print("2. Ubah Video ke Audio")
        print("3. Keluar\n")
        pilihan = input("Pilih Opsi (1/2/3): ").strip()

        if pilihan == "1":
            video_audio_downloader()
        elif pilihan == "2":
            convert_video_to_audio()
        elif pilihan == "3":
            sys.exit()
        else:
            input("Pilihan tidak valid! Tekan Enter untuk kembali...")

def get_unique_filename(directory, filename, extension):
    """Tambahkan angka jika nama file sudah ada (1, 2, 3, ...)."""
    base_name = os.path.join(directory, filename)
    file_path = f"{base_name}{extension}"

    if not os.path.exists(file_path):
        return file_path  # Jika belum ada, langsung pakai

    i = 1
    while os.path.exists(f"{base_name}_{i}{extension}"):
        i += 1
    return f"{base_name}_{i}{extension}"

def video_audio_downloader():
    clear_screen()
    banner()
    url = input("Masukkan URL: ").strip()
    if not url:
        input("URL tidak boleh kosong! Tekan Enter untuk kembali...")
        return

    print("\nPilih Format Download:")
    print("1. Video (Mp4) (Default)")
    print("2. Audio (Mp3)")
    format_choice = input("Pilih Opsi (1/2) [Kosongkan dan Enter Untuk Default]: ").strip() or "1"

    if format_choice == "1":
        print("\nPilih Resolusi Video:")
        print("1. 1080p")
        print("2. 720p")
        print("3. 480p")
        print("4. Best (Default)")
        res_choice = input("Pilih Opsi (1/2/3/4) [Kosongkan dan Enter Untuk Default]: ").strip() or "4"

        resolutions = {
            "1": "bestvideo[height<=1080]+bestaudio/best",
            "2": "bestvideo[height<=720]+bestaudio/best",
            "3": "bestvideo[height<=480]+bestaudio/best",
            "4": "bestvideo+bestaudio/best"
        }
        format_string = resolutions.get(res_choice, "bestvideo+bestaudio/best")

        filename = input("\nGanti Nama Video (Kosongkan dan Enter Untuk Default): ").strip()
        download_video(url, format_string, filename)

    elif format_choice == "2":
        filename = input("\nGanti Nama Audio (Kosongkan dan Enter Untuk Default): ").strip()
        download_audio(url, filename)
    
    input("\nTekan Enter untuk kembali ke menu...")

def download_video(url, format_string, filename):
    if filename:
        file_path = get_unique_filename(DOWNLOAD_PATH, filename, ".mp4")
    else:
        file_path = f"{DOWNLOAD_PATH}/%(id)s.%(ext)s"  # Jika kosong, pakai ID

    ydl_opts = {
        'format': format_string,
        'outtmpl': file_path,
        'noplaylist': True,
        'merge_output_format': 'mp4'
    }

    print("\nSedang mengunduh video...")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
        except Exception as e:
            print(f"\nDownload gagal: {e}")
            if "instagram.com" in url:
                print("\nCoba menggunakan instaloader...")
                download_instagram(url, filename)

def download_audio(url, filename):
    if filename:
        file_path = get_unique_filename(DOWNLOAD_PATH, filename, ".mp3")
    else:
        file_path = f"{DOWNLOAD_PATH}/%(id)s.%(ext)s"  # Jika kosong, pakai ID

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': file_path,
        'noplaylist': True,
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}]
    }

    print("\nSedang mengunduh audio...")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
        except Exception as e:
            print(f"\nDownload gagal: {e}")
            if "instagram.com" in url:
                print("\nCoba menggunakan instaloader...")
                download_instagram(url, filename)

def convert_video_to_audio():
    clear_screen()
    banner()
    video_path = input("Silahkan masukkan path lokasi video yang ingin diubah: ").strip()
    if not os.path.exists(video_path):
        input("\nFile tidak ditemukan! Tekan Enter untuk kembali...")
        return

    filename = input("\nGanti Nama Audio (Kosongkan dan Enter Untuk Default): ").strip()
    if not filename:
        filename = os.path.splitext(os.path.basename(video_path))[0]

    audio_path = get_unique_filename(os.path.dirname(video_path), filename, ".mp3")

    print("\nMengonversi video ke audio...")
    command = f'ffmpeg -i "{video_path}" -q:a 0 -map a "{audio_path}" -y'
    process = subprocess.run(command, shell=True)

    if process.returncode == 0:
        print("\nKonversi selesai!")
    else:
        print("\nKonversi gagal!")

    input("\nTekan Enter untuk kembali ke menu...")

def download_instagram(url, filename):
    """Gunakan instaloader jika yt-dlp gagal."""
    loader = instaloader.Instaloader(dirname_pattern=DOWNLOAD_PATH)
    try:
        loader.download_post(instaloader.Post.from_shortcode(loader.context, url.split("/")[-2]), target=DOWNLOAD_PATH)
        print("\nDownload Instagram berhasil!")
    except Exception as e:
        print(f"\nDownload Instagram gagal: {e}")

if __name__ == "__main__":
    menu()
