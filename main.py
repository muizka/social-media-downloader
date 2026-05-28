import os
import re
import sys
import shutil

# Memastikan library utama terpasang sempurna
try:
    import yt_dlp
    import instaloader
except ImportError:
    print("[!] Library pendukung tidak ditemukan. Menginstal otomatis...")
    os.system("pip install yt-dlp instaloader --break-system-packages")
    import yt_dlp
    import instaloader

# Konfigurasi Path Penyimpanan Android
BASE_STORAGE = "/sdcard/Download"
LINKS_FILE = os.path.join(BASE_STORAGE, "links.txt")
IG_STORAGE = os.path.join(BASE_STORAGE, "IG_Downloads")

def inisialisasi_sistem():
    """Menyiapkan folder dan file konfigurasi awal"""
    if not os.path.exists(BASE_STORAGE):
        os.makedirs(BASE_STORAGE)
    if not os.path.exists(IG_STORAGE):
        os.makedirs(IG_STORAGE)
        
    if not os.path.exists(LINKS_FILE):
        with open(LINKS_FILE, "w", encoding="utf-8") as f:
            f.write("# ========================================================\n")
            f.write("# RIXZ ENGINEERING - SOCIAL MEDIA DOWNLOADER\n")
            f.write("# ========================================================\n")
            f.write("# Masukkan URL di bawah ini (Satu link per baris):\n")
            f.write("# Contoh:\n")
            f.write("# https://www.youtube.com/watch?v=xxxxxx\n")
            f.write("# https://vt.tiktok.com/xxxxxx/\n")
            f.write("# https://www.instagram.com/reel/xxxxxx/\n")
            f.write("# ========================================================\n\n")
        print(f"[+] File konfigurasi sukses dibuat di: {LINKS_FILE}")
        print("[*] Silakan isi link video terlebih dahulu lalu jalankan ulang script.")
        sys.exit(0)

def ambil_antrean_links():
    """Membaca daftar URL dari links.txt"""
    antrean = []
    if os.path.exists(LINKS_FILE):
        with open(LINKS_FILE, "r", encoding="utf-8") as f:
            for baris in f:
                baris = baris.strip()
                if baris and not baris.startswith("#"):
                    antrean.append(baris)
    return antrean

def download_yt_tt(url):
    """Download YT/TikTok menggunakan format single-stream MP4"""
    print(f"\n[*] Memproses URL (yt-dlp) -> {url}")
    
    ydl_opts = {
        'outtmpl': os.path.join(BASE_STORAGE, '%(title)s.%(ext)s'),
        # Mengambil single file MP4 terbaik yang sudah include audio + video
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
        print("[+] Sukses: Berkas MP4 berhasil diamankan.")
    except Exception as e:
        print(f"[-] Eror saat mengunduh YT/TikTok: {e}")

def download_ig(url):
    """Download Instagram Reel/Post dan hapus paksa file sampah metadata"""
    print(f"\n[*] Memproses URL (Instaloader) -> {url}")
    
    # Ekstraksi shortcode unik dari URL
    match = re.search(r"/(?:p|reel|tv)/([A-Za-z0-9_-]+)", url)
    if not match:
        print("[-] Eror: Struktur URL Instagram tidak valid!")
        return
        
    shortcode = match.group(1)
    bot = instaloader.Instaloader(
        dirname_pattern=IG_STORAGE,
        download_geotags=False,
        download_comments=False,
        save_metadata=False,
        compress_json=False
    )
    
    try:
        post = instaloader.Post.from_shortcode(bot.context, shortcode)
        if post.is_video:
            print("[*] Mengunduh target berkas video...")
            bot.download_post(post, target=IG_STORAGE)
            
            # Sistem Hard-Clean: Sapu bersih semua file non-MP4 yang lolos
            print("[*] Menjalankan pembersihan berkas sampah...")
            for item in os.listdir(IG_STORAGE):
                item_path = os.path.join(IG_STORAGE, item)
                if os.path.isfile(item_path):
                    # Jika file tidak berakhiran .mp4, hapus instan
                    if not item.endswith(".mp4"):
                        os.remove(item_path)
            print("[+] Sukses: Hanya menyisakan file video MP4 murni.")
        else:
            print("[-] Skip: Konten tersebut bukan merupakan format video.")
    except Exception as e:
        print(f"[-] Eror saat mengunduh Instagram: {e}")

def main():
    print("========================================================")
    print("      RIXZ ENGINEERING - SOCIAL MEDIA DOWNLOADER        ")
    print("========================================================")
    
    inisialisasi_sistem()
    daftar_download = ambil_antrean_links()
    
    if not daftar_download:
        print(f"[-] Antrean kosong. Silakan isi URL target di: {LINKS_FILE}")
        return
        
    print(f"[+] Menemukan {len(daftar_download)} target di dalam antrean.")
    
    for url in daftar_download:
        if "instagram.com" in url:
            download_ig(url)
        else:
            download_yt_tt(url)
            
    print("\n[=================== PROSES SELESAI ===================]")

if __name__ == "__main__":
    main()
