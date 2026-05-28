import os
import re
import sys
import yt_dlp
import instaloader

# Konfigurasi Path Penyimpanan Internal HP (Folder Download)
STORAGE_INTERNAL = "/storage/emulated/0/Download"
CONFIG_FILE = "links.txt"
PATH_TARGET_TXT = os.path.join(STORAGE_INTERNAL, CONFIG_FILE)

def bersihkan_layar():
    os.system('cls' if os.name == 'nt' else 'clear')

def cek_akses_penyimpanan():
    """Memeriksa apakah Termux memiliki izin akses ke penyimpanan internal HP."""
    if not os.path.exists(STORAGE_INTERNAL):
        print("\n" + "="*50)
        print("❌ ERROR: TIDAK DAPAT MENGAKSES PENYIMPANAN INTERNAL!")
        print("="*50)
        print("Solusi:")
        print("1. Jalankan perintah 'termux-setup-storage' di Termux.")
        print("2. Berikan izin akses file/media untuk aplikasi Termux.")
        print("="*50 + "\n")
        return False
    return True

def inisialisasi_file_txt():
    """Membuat file links.txt otomatis di folder Download jika belum ada."""
    if not os.path.exists(PATH_TARGET_TXT):
        try:
            with open(PATH_TARGET_TXT, "w", encoding="utf-8") as f:
                f.write("# ========================================================\n")
                f.write("# RIXZ ENGINEERING - SOCIAL MEDIA DOWNLOADER\n")
                f.write("# ========================================================\n")
                f.write("# Masukkan URL di bawah ini (Satu link per baris):\n")
                f.write("# Contoh:\n")
                f.write("# https://www.youtube.com/watch?v=xxxxxx\n")
                f.write("# https://vt.tiktok.com/xxxxxx/\n")
                f.write("# https://www.instagram.com/reel/xxxxxx/\n")
                f.write("# ========================================================\n\n")
            print(f"✅ Berhasil membuat file template di: {PATH_TARGET_TXT}")
            print("💡 Silakan isi file tersebut dengan link video sebelum menjalankan kembali.")
        except Exception as e:
            print(f"❌ Gagal membuat file template: {e}")

def ambil_daftar_link():
    """Membaca dan memfilter link dari file links.txt."""
    if not os.path.exists(PATH_TARGET_TXT):
        return []
        
    with open(PATH_TARGET_TXT, "r", encoding="utf-8") as f:
        baris = f.readlines()
        
    # Ambil baris yang bukan comment (#) dan bukan baris kosong
    links = [b.strip() for b in baris if b.strip() and not b.strip().startswith('#')]
    return links

def download_yt_tiktok(url):
    """Mengunduh video dari YouTube atau TikTok menggunakan yt-dlp."""
    ydl_opts = {
        # Menyimpan langsung ke folder Download internal HP
        'outtmpl': os.path.join(STORAGE_INTERNAL, '%(title)s.%(ext)s'),
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'quiet': False,
        'no_warnings': True,
    }
    try:
        print(f"\n[+] Memproses YouTube/TikTok: {url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("✨ Sukses Terunduh!")
        return True
    except Exception as e:
        print(f"❌ Gagal Mengunduh YT/TikTok: {e}")
        return False

def download_instagram(url):
    """Mengunduh post/reel dari Instagram menggunakan instaloader."""
    # Menyimpan hasil ke dalam folder khusus di dalam folder Download internal
    L = instaloader.Instaloader(
        download_videos=True,
        download_comments=False,
        save_metadata=False,
        dirname_pattern=os.path.join(STORAGE_INTERNAL, 'IG_Downloads')
    )
    try:
        print(f"\n[+] Memproses Instagram: {url}")
        # Ekstrak shortcode dari URL
        match = re.search(r"/(p|reels|reel)/([a-zA-Z0-9__-]+)", url)
        if not match:
            print("❌ URL Instagram tidak valid atau struktur tautan salah.")
            return False
            
        shortcode = match.group(2)
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        
        print(f"[+] Mengunduh konten dari kreator: @{post.owner_profile.username}")
        L.download_post(post, target=shortcode)
        print("✨ Sukses Terunduh (Disimpan di folder Download/IG_Downloads)!")
        return True
    except Exception as e:
        print(f"❌ Gagal Mengunduh Instagram: {e}")
        return False

def main():
    bersihkan_layar()
    print("="*60)
    print("        RIX-Z ENGINEERING | MULTI-DOWNLOADER BOT        ")
    print("        Platform: YouTube, TikTok, & Instagram          ")
    print("="*60)
    
    if not cek_akses_penyimpanan():
        sys.exit(1)
        
    inisialisasi_file_txt()
    links = ambil_daftar_link()
    
    if not links:
        print(f"\nℹ️ File '{CONFIG_FILE}' di folder Download masih kosong.")
        print("   Silakan paste link video terlebih dahulu di file tersebut.")
        print("="*60 + "\n")
        sys.exit(0)
        
    total_link = len(links)
    print(f"\n🚀 Menemukan {total_link} tautan antrean di {CONFIG_FILE}.\n")
    
    sukses = 0
    gagal = 0
    
    for indeks, url in enumerate(links, 1):
        print(f"\n[{indeks}/{total_link}] " + "-"*45)
        
        # Validasi platform berdasarkan string URL
        if "instagram.com" in url:
            hasil = download_instagram(url)
        elif "youtube.com" in url or "youtu.be" in url or "tiktok.com" in url:
            hasil = download_yt_tiktok(url)
        else:
            print(f"⚠️ URL tidak didukung atau salah ketik: {url}")
            hasil = False
            
        if hasil:
            sukses += 1
        else:
            gagal += 1
            
    print("\n" + "="*60)
    print("🎉 SEMUA PROSES DOWNLOAD SELESAI!")
    print(f"📊 Ringkasan: Berhasil [{sukses}] | Gagal [{gagal}]")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
