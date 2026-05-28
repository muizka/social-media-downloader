import os
import re
import sys
import urllib.request

# Cek & Install library otomatis jika belum ada
try:
    import instaloader
    import yt_dlp
except ImportError:
    print("[!] Library kurang. Menginstal otomatis...")
    os.system("pip install yt-dlp instaloader --break-system-packages")
    import instaloader
    import yt_dlp

# Path Penyimpanan Folder Download Internal HP Android
BASE_STORAGE = "/sdcard/Download"
LINKS_FILE = os.path.join(BASE_STORAGE, "links.txt")
IG_STORAGE = os.path.join(BASE_STORAGE, "IG_Downloads")

def inisialisasi_folder():
    """Membuat folder dan file links.txt otomatis jika belum ada"""
    if not os.path.exists(BASE_STORAGE):
        os.makedirs(BASE_STORAGE)
    if not os.path.exists(IG_STORAGE):
        os.makedirs(IG_STORAGE)
        
    if not os.path.exists(LINKS_FILE):
        print(f"[*] Membuat file konfigurasi di: {LINKS_FILE}")
        with open(LINKS_FILE, "w", encoding="utf-8") as f:
            f.write("# Taruh URL/Link Video di bawah ini (Satu link per baris)\n")
            f.write("# Contoh:\n# https://www.youtube.com/watch?v=xxxxxx\n")
        print("[+] File links.txt berhasil dibuat! Silakan isi link dulu lalu jalankan ulang.")
        sys.exit(0)

def ambil_daftar_link():
    """Membaca list link dari file links.txt"""
    links = []
    if os.path.exists(LINKS_FILE):
        with open(LINKS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    links.append(line)
    return links

def download_youtube_tiktok(url):
    """Download YouTube/TikTok dan PAKSA JAHIT AUDIO VIDEO via FFmpeg"""
    print(f"\n[*] Memproses (yt-dlp) -> {url}")
    
    ydl_opts = {
        # Lokasi output langsung ke folder Download internal
        'outtmpl': os.path.join(BASE_STORAGE, '%(title)s.%(ext)s'),
        
        # Ambil video MP4 terbaik dan audio M4A terbaik, lalu gabungkan
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best',
        
        # Paksa FFmpeg melakukan penggabungan menjadi format tunggal .mp4
        'merge_output_format': 'mp4',
        
        # Bersihkan file sampah teks/json/thumbnail
        'writeinfojson': False,
        'writedescription': False,
        'writeannotations': False,
        'writethumbnail': False,
        
        # Beri tahu yt-dlp lokasi binary FFmpeg secara tegas di Termux
        'ffmpeg_location': '/data/data/com.termux/files/usr/bin/ffmpeg',
        'quiet': False
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("[+] BERHASIL! Video dan Audio sudah dijahit menjadi satu file .mp4")
    except Exception as e:
        print(f"[-] Gagal mengunduh/menggabungkan: {e}")

def download_instagram(url):
    """Download Instagram MURNI VIDEO MP4 TANPA FILE TEXT & JPG SAMPAH"""
    print(f"\n[*] Memproses (Instaloader Instagram) -> {url}")
    
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
            
            print("[*] Mengunduh file video mp4 langsung...")
            urllib.request.urlretrieve(video_url, output_file)
            print(f"[+] BERHASIL! Video Instagram disimpan di folder IG_Downloads.")
        else:
            print("[-] Konten ini bukan video!")
    except Exception as e:
        print(f"[-] Gagal mengunduh Instagram: {e}")

def main():
    print("=== AUTO MEDIA DOWNLOADER (FIXED FFMEG MERGE) ===")
    inisialisasi_folder()
    daftar_link = ambil_daftar_link()
    
    if not daftar_link:
        print(f"[-] File links.txt kosong! Isi link video dulu di folder Download/links.txt")
        return

    print(f"[+] Menemukan {len(daftar_link)} antrean video.")
    
    for link in daftar_link:
        if "instagram.com" in link:
            download_instagram(link)
        else:
            download_youtube_tiktok(link)
            
    print("\n[====== SEMUA PROSES DOWNLOAD SELESAI ======]")

if __name__ == "__main__":
    main()
