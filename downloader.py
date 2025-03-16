import os
import sys
import subprocess
import yt_dlp
import instaloader
import time
from tqdm import tqdm

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

def progress_bar(duration):
    for _ in tqdm(range(duration), desc="Proses...", unit="s"):
        time.sleep(1)

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

        resolutions = {"1": "1080", "2": "720", "3": "480", "4": "best"}
        resolution = resolutions.get(res_choice, "best")

        filename = input("\nGanti Nama Video (Kosongkan dan Enter Untuk Default): ").strip()
        download_video(url, resolution, filename)

    elif format_choice == "2":
        filename = input("\nGanti Nama Audio (Kosongkan dan Enter Untuk Default): ").strip()
        download_audio(url, filename)
    
    input("\nTekan Enter untuk kembali ke menu...")

def download_video(url, resolution, filename):
    ydl_opts = {
        'format': f'bestvideo[height<={resolution}]+bestaudio/best',
        'outtmpl': f"{DOWNLOAD_PATH}/%(id)s.%(ext)s" if not filename else f"{DOWNLOAD_PATH}/{filename}.%(ext)s",
        'noplaylist': True,
        'merge_output_format': 'mp4'
    }

    print("\nSedang mengunduh video...")
    progress_bar(5)  # Simulasi progress bar selama 5 detik

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
            print("\nDownload berhasil!")
        except Exception as e:
            print(f"\nDownload gagal: {e}")
            if "instagram.com" in url:
                print("\nCoba menggunakan instaloader...")
                download_instagram(url, filename)

def download_audio(url, filename):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f"{DOWNLOAD_PATH}/%(id)s.%(ext)s" if not filename else f"{DOWNLOAD_PATH}/{filename}.%(ext)s",
        'noplaylist': True,
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}]
    }

    print("\nSedang mengunduh audio...")
    progress_bar(5)  # Simulasi progress bar selama 5 detik

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
            print("\nDownload berhasil!")
        except Exception as e:
            print(f"\nDownload gagal: {e}")
            if "instagram.com" in url:
                print("\nCoba menggunakan instaloader...")
                download_instagram(url, filename)

def download_instagram(url, filename):
    loader = instaloader.Instaloader(download_videos=True, download_pictures=False)
    try:
        print("\nMengunduh dari Instagram...")
        progress_bar(5)  # Simulasi progress bar selama 5 detik
        loader.download_profile(url.split("/")[-2], profile_pic=False)
        print("\nDownload Instagram berhasil!")
    except Exception as e:
        print(f"\nGagal mengunduh dari Instagram: {e}")

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

    audio_path = os.path.join(os.path.dirname(video_path), f"{filename}.mp3")

    print("\nMengonversi video ke audio...")
    progress_bar(5)  # Simulasi progress bar selama 5 detik

    command = f'ffmpeg -i "{video_path}" -q:a 0 -map a "{audio_path}" -y'
    process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if process.returncode == 0:
        print("\nKonversi berhasil!")
    else:
        print("\nKonversi gagal!")

    input("\nTekan Enter untuk kembali ke menu...")

if __name__ == "__main__":
    menu()
