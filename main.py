import os
import re
import sys
import shutil
import time

try:
    import yt_dlp
    import instaloader
except (ImportError, ModuleNotFoundError):
    os.system("pip install yt-dlp instaloader --break-system-packages")
    import yt_dlp
    import instaloader

# Konfigurasi Direktori Utama Penyimpanan Android
BASE_STORAGE = "/sdcard/Download"
LINKS_FILE = os.path.join(BASE_STORAGE, "links.txt")
IG_STORAGE = os.path.join(BASE_STORAGE, "IG_Downloads")
TT_STORAGE = os.path.join(BASE_STORAGE, "TikTok_Downloads")
YT_STORAGE = os.path.join(BASE_STORAGE, "YouTube_Downloads")

def inisialisasi_sistem():
    """Membuat folder-folder penyimpanan jika belum ada di internal HP"""
    try:
        if not os.path.exists(BASE_STORAGE): os.makedirs(BASE_STORAGE, exist_ok=True)
        if not os.path.exists(IG_STORAGE): os.makedirs(IG_STORAGE, exist_ok=True)
        if not os.path.exists(TT_STORAGE): os.makedirs(TT_STORAGE, exist_ok=True)
        if not os.path.exists(YT_STORAGE): os.makedirs(YT_STORAGE, exist_ok=True)
    except PermissionError:
        print("[-] ERROR: Akses memori ditolak! Silakan ketik: termux-setup-storage")
        sys.exit(1)
        
    if not os.path.exists(LINKS_FILE):
        with open(LINKS_FILE, "w", encoding="utf-8") as f:
            f.write("# RIXZ ENGINEERING - SOCIAL MEDIA DOWNLOADER\n# Masukkan URL di bawah ini (Satu link per baris):\n\n")
        print(f"[+] File antrean kosong berhasil dibuat di: {LINKS_FILE}")
        sys.exit(0)

def ambil_antrean_links():
    antrean = []
    if os.path.exists(LINKS_FILE):
        with open(LINKS_FILE, "r", encoding="utf-8") as f:
            for baris in f:
                baris = baris.strip()
                if baris and not baris.startswith("#"): antrean.append(baris)
    return antrean

def download_yt_tt(url):
    """Engine yt-dlp pintar untuk memisahkan folder TikTok dan YouTube"""
    if "tiktok.com" in url:
        print(f"\n[*] Memproses URL (TikTok Engine) -> {url}")
        target_folder = TT_STORAGE
        platform_name = "TikTok"
    else:
        print(f"\n[*] Memproses URL (YouTube Engine) -> {url}")
        target_folder = YT_STORAGE
        platform_name = "YouTube"

    ydl_opts = {
        'outtmpl': os.path.join(target_folder, '%(title)s.%(ext)s'),
        'format': 'best[ext=mp4]/best',
        'quiet': False, 'no_warnings': True
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download([url])
        print(f"[+] SUKSES: Berkas MP4 berhasil diunduh ke folder {platform_name}_Downloads.")
    except Exception as e: 
        print(f"[-] Error saat mengunduh dari {platform_name}: {e}")

def download_ig(url):
    """Engine Instaloader dengan pengubah nama kustom berbasis Username + Caption"""
    print(f"\n[*] Memproses URL (Instagram) -> {url}")
    match = re.search(r"/(?:p|reel|tv)/([A-Za-z0-9_-]+)", url)
    if not match:
        print("[-] LINK ERROR: URL Instagram tidak valid!")
        return
        
    shortcode = match.group(1)
    bot = instaloader.Instaloader(
        dirname_pattern=IG_STORAGE, download_geotags=False,
        download_comments=False, save_metadata=False, compress_json=False,
        post_metadata_txt_pattern=""
    )
    
    try:
        print("[*] Mengambil data dari Instagram...")
        post = instaloader.Post.from_shortcode(bot.context, shortcode)
        
        if post.is_video:
            username = post.owner_username
            caption = post.caption if post.caption else ""
            
            # Sanitasi nama agar aman dari karakter ilegal di Android
            caption_bersih = re.sub(r'[^a-zA-Z0-9\s]', '', caption)
            kata_caption = caption_bersih.split()
            potongan_judul = "_".join(kata_caption[:5]) if kata_caption else "Video"
            
            nama_baru_simpel = f"{username}_{potongan_judul}"
            
            print(f"[+] Pemilik: @{username}")
            print(f"[*] Mengunduh video mentah...")
            bot.download_post(post, target=IG_STORAGE)
            
            print("[*] Mengganti nama file & menghapus file sampah...")
            time.sleep(2) # Jeda penulisan file OS
            
            file_direname = False
            for item in os.listdir(IG_STORAGE):
                item_path = os.path.join(IG_STORAGE, item)
                
                if shortcode in item and item.endswith(".mp4"):
                    target_path = os.path.join(IG_STORAGE, f"{nama_baru_simpel}.mp4")
                    if os.path.exists(target_path):
                        target_path = os.path.join(IG_STORAGE, f"{nama_baru_simpel}_{int(time.time())}.mp4")
                    
                    os.rename(item_path, target_path)
                    file_direname = True
                    print(f"[+] BERHASIL DIUBAH -> {os.path.basename(target_path)}")
                
                elif os.path.isfile(item_path) and not item.endswith(".mp4"):
                    os.remove(item_path)
            
            if not file_direname:
                print("[-] Peringatan: File video mentah tidak ditemukan untuk di-rename.")
        else:
            print("[-] Skip: Konten bukan video.")
    except Exception as e:
        print(f"[-] Engine Error Instagram: {e}")

def main():
    print("========================================================")
    print("      RIXZ ENGINEERING - SOCIAL MEDIA DOWNLOADER        ")
    print("========================================================")
    inisialisasi_sistem()
    daftar = ambil_antrean_links()
    if not daftar:
        print(f"[-] Isi link dulu di: {LINKS_FILE}")
        return
    print(f"[+] Memproses {len(daftar)} tautan...")
    for url in daftar:
        if "instagram.com" in url: download_ig(url)
        else: download_yt_tt(url)
    print("\n[=================== PROSES SELESAI ===================]")

if __name__ == "__main__":
    main()
