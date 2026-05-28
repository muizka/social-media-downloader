import os
import re
import sys

# Cek & Install library otomatis jika belum ada (Biar gak ModuleNotFoundError)
try:
    import instaloader
    import yt_dlp
except ImportError:
    print("[!] Library kurang. Menginstal otomatis...")
    os.system("pip install yt-dlp instaloader --break-system-packages")
    import instaloader
    import yt_dlp

# Path Penyimpanan Folder Download Internal HP Android
STORAGE_PATH = "/sdcard/Download"
LINKS_FILE = os.path.join(STORAGE_PATH, "links.txt")

def inisialisasi_file():
    """Membuat file links.txt otomatis jika belum ada di folder Download"""
    if not os.path.exists(LINKS_FILE):
        print(f"[*] Membuat file konfigurasi di: {LINKS_FILE}")
        with open(LINKS_FILE, "w", encoding="utf-8") as f:
            f.write("# Taruh URL/Link Video di bawah ini (Satu link per baris)\n")
            f.write("# Contoh:\n# https://www.tiktok.com/@xyz/video/1234567\n")
        print("[+] File links.txt berhasil dibuat! Silakan isi link dulu lalu jalankan ulang.")
        sys.exit(0)

def ambil_daftar_link():
    """Membaca list link dari file links.txt"""
    links = []
    with open(LINKS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                links.append(line)
    return links

def download_youtube_tiktok(url):
    """Download YouTube atau TikTok MURNI VIDEO TANPA TEKS SAMPAH"""
    print(f"\n[*] Memproses (yt-dlp) -> {url}")
    ydl_opts = {
        'outtmpl': os.path.join(STORAGE_PATH, '%(title)s.%(ext)s'),
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', # Paksa gabung video+audio mp4
        'merge_output_format': 'mp4',
        # MATIKAN SEMUA FITUR DOWNLOAD TEKS/METADATA SAMPAH
        'writeinfojson': False,
        'writedescription': False,
        'writeannotations': False,
        'writethumbnail': False,
        'quiet': False
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("[+] Berhasil diunduh ke folder Download!")
    except Exception as e:
        print(f"[-] Gagal mengunduh: {e}")

def download_instagram(url):
    """Download Instagram MURNI VIDEO TANPA FILE _UTC.txt ATAU .json"""
    print(f"\n[*] Memproses (Instaloader Instagram) -> {url}")
    
    # Ambil Shortcode dari URL Instagram
    match = re.search(r"/(?:p|reel|tv)/([A-Za-z0-9_-]+)", url)
    if not match:
        print("[-] URL Instagram tidak valid atau shortcode tidak ditemukan!")
        return
    
    shortcode = match.group(1)
    
    # Setel Instaloader super ketat agar TIDAK BIKIN FILE SAMPAH
    L = instaloader.Instaloader(
        dirname_pattern=STORAGE_PATH,        # Langsung lempar ke folder Download
        download_geotags=False,              # Gak usah download lokasi
        download_comments=False,             # Gak usah download komentar
        save_metadata_json=False,            # MATIKAN FILE .json
        download_pictures=False              # Gak usah download foto/thumbnail tambahan
    )
    # MATIKAN FILE CAPTION (_UTC.txt)
    L.post_metadata_txt_pattern = "" 

    try:
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        if post.is_video:
            L.download_post(post, target=STORAGE_PATH)
            print("[+] Video Instagram berhasil diunduh ke folder Download!")
            
            # Bersihkan sisa-sisa file gambar/txt liar jika instaloader bandel meloloskannya
            for file in os.listdir(STORAGE_PATH):
                if file.startswith(shortcode) and not file.endswith(".mp4"):
                    try:
                        os.remove(os.path.join(STORAGE_PATH, file))
                    except:
                        pass
        else:
            print("[-] Konten bukan video!")
    except Exception as e:
        print(f"[-] Gagal mengunduh Instagram: {e}")

def main():
    print("=== AUTO MEDIA DOWNLOADER (TERMUX CLEAN VERSION) ===")
    inisialisasi_file()
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
