import os
import re
import sys
import urllib.request

try:
    import instaloader
    import yt_dlp
except ImportError:
    print("[!] Library kurang. Menginstal otomatis...")
    os.system("pip install yt-dlp instaloader --break-system-packages")
    import instaloader
    import yt_dlp

BASE_STORAGE = "/sdcard/Download"
LINKS_FILE = os.path.join(BASE_STORAGE, "links.txt")
IG_STORAGE = os.path.join(BASE_STORAGE, "IG_Downloads")

def inisialisasi_folder():
    if not os.path.exists(BASE_STORAGE):
        os.makedirs(BASE_STORAGE)
    if not os.path.exists(IG_STORAGE):
        os.makedirs(IG_STORAGE)
    if not os.path.exists(LINKS_FILE):
        with open(LINKS_FILE, "w", encoding="utf-8") as f:
            f.write("# Taruh URL/Link Video di bawah ini (Satu link per baris)\n")
        print("[+] File links.txt berhasil dibuat di folder Download HP!")
        sys.exit(0)

def ambil_daftar_link():
    links = []
    if os.path.exists(LINKS_FILE):
        with open(LINKS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    links.append(line)
    return links

def download_youtube_tiktok(url):
    print(f"\n[*] Memproses (yt-dlp Direct MP4) -> {url}")
    ydl_opts = {
        'outtmpl': os.path.join(BASE_STORAGE, '%(title)s.%(ext)s'),
        'format': 'best[ext=mp4]/best', 
        'writeinfojson': False,
        'writedescription': False,
        'writeannotations': False,
        'writethumbnail': False,
        'quiet': False
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("[+] BERHASIL! Video utuh berekstensi .mp4 siap ditonton.")
    except Exception as e:
        print(f"[-] Gagal mengunduh: {e}")

def download_instagram(url):
    print(f"\n[*] Memproses (Instagram) -> {url}")
    match = re.search(r"/(?:p|reel|tv)/([A-Za-z0-9_-]+)", url)
    if not match:
        print("[-] URL Instagram tidak valid!")
        return
    shortcode = match.group(1)
    L = instaloader.Instaloader()
    try:
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        if post.is_video:
            video_url = post.video_url
            output_file = os.path.join(IG_STORAGE, f"{shortcode}.mp4")
            print("[*] Mengunduh murni file mp4...")
            urllib.request.urlretrieve(video_url, output_file)
            print(f"[+] BERHASIL! Masuk ke folder IG_Downloads.")
        else:
            print("[-] Konten ini bukan video!")
    except Exception as e:
        print(f"[-] Gagal mengunduh Instagram: {e}")

def main():
    print("=== AUTO MEDIA DOWNLOADER (FINAL DIRECT VERSION) ===")
    inisialisasi_folder()
    daftar_link = ambil_daftar_link()
    if not daftar_link:
        print(f"[-] File links.txt kosong!")
        return
    print(f"[+] Menemukan {len(daftar_link)} antrean video.")
    for link in daftar_link:
        if "instagram.com" in link:
            download_instagram(link)
        else:
            download_youtube_tiktok(link)
    print("\n[====== PROSES DOWNLOAD SELESAI ======]")

if __name__ == "__main__":
    main()
