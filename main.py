import os
import re
import sys
import shutil
import time

# ========================================================
# 🛡️ LAYER 1: PENGAMANAN DEPENDENSI OTOMATIS
# ========================================================
try:
    import yt_dlp
    import instaloader
except (ImportError, ModuleNotFoundError) as library_error:
    print(f"[*] Komponen sistem hilang ({library_error}). Menginisialisasi perbaikan...")
    try:
        os.system("pip install yt-dlp instaloader --break-system-packages")
        import yt_dlp
        import instaloader
        print("[+] Semua library berhasil dipasang ke sistem.")
    except Exception as critical_pip_error:
        print(f"[-] FATAL: Gagal memasang dependensi otomatis: {critical_pip_error}")
        print("[-] Silakan jalankan manual: pip install yt-dlp instaloader --break-system-packages")
        sys.exit(1)

# Konfigurasi Jalur Penyimpanan Internal Android
BASE_STORAGE = "/sdcard/Download"
LINKS_FILE = os.path.join(BASE_STORAGE, "links.txt")
IG_STORAGE = os.path.join(BASE_STORAGE, "IG_Downloads")

def inisialisasi_sistem():
    """Memvalidasi dan menyiapkan direktori lingkungan eksekusi (LAYER 2)"""
    try:
        if not os.path.exists(BASE_STORAGE):
            os.makedirs(BASE_STORAGE, exist_ok=True)
        if not os.path.exists(IG_STORAGE):
            os.makedirs(IG_STORAGE, exist_ok=True)
    except PermissionError as perm_err:
        print(f"[-] ERROR PERIZINAN: Akses memori ditolak Android: {perm_err}")
        print("[-] Silakan ketik perintah ini di Termux: termux-setup-storage")
        sys.exit(1)
    except Exception as e:
        print(f"[-] Gagal menginisialisasi folder penyimpanan: {e}")
        sys.exit(1)

    try:
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
            print(f"[+] File antrean baru berhasil dibuat di: {LINKS_FILE}")
            print("[*] Silakan isi URL video di file tersebut terlebih dahulu.")
            sys.exit(0)
    except Exception as e:
        print(f"[-] Gagal membuat file antrean links.txt: {e}")
        sys.exit(1)

def ambil_antrean_links():
    """Membaca daftar URL dari links.txt dengan aman (LAYER 3)"""
    antrean = []
    try:
        if os.path.exists(LINKS_FILE):
            with open(LINKS_FILE, "r", encoding="utf-8") as f:
                for baris in f:
                    baris = baris.strip()
                    if baris and not baris.startswith("#"):
                        antrean.append(baris)
        return antrean
    except UnicodeDecodeError:
        print("[-] Kesalahan pembacaan file: Pastikan links.txt bertipe teks UTF-8 murni.")
        return []
    except Exception as e:
        print(f"[-] Gagal membaca file antrean: {e}")
        return []

def download_yt_tt(url):
    """Download YT/TikTok format single-stream MP4 (LAYER 4)"""
    print(f"\n[*] Memproses URL (yt-dlp Engine) -> {url}")
    
    ydl_opts = {
        'outtmpl': os.path.join(BASE_STORAGE, '%(title)s.%(ext)s'),
        'format': 'best[ext=mp4]/best',
        'writeinfojson': False,
        'writedescription': False,
        'writeannotations': False,
        'writethumbnail': False,
        'quiet': False,
        'no_warnings': True
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("[+] SUKSES: Berkas MP4 berhasil diunduh ke folder Download.")
    except yt_dlp.utils.DownloadError as download_err:
        print(f"[-] LINK RUSAK / ERROR DOWNLOAD: Konten tidak ditemukan atau koneksi putus: {download_err}")
    except Exception as unexpected_err:
        print(f"[-] Terjadi kesalahan tak terduga pada engine yt-dlp: {unexpected_err}")

def download_ig(url):
    """Download Instagram Reel dengan format nama akun + deskripsi bersih (LAYER 5)"""
    print(f"\n[*] Memproses URL (Instaloader Engine) -> {url}")
    
    match = re.search(r"/(?:p|reel|tv)/([A-Za-z0-9_-]+)", url)
    if not match:
        print("[-] STRUKTUR LINK ERROR: URL Instagram tidak valid!")
        return
        
    shortcode = match.group(1)
    bot = instaloader.Instaloader(
        dirname_pattern=IG_STORAGE,
        download_geotags=False,
        download_comments=False,
        save_metadata=False,
        compress_json=False,
        post_metadata_txt_pattern=""
    )
    
    try:
        print("[*] Menghubungi server Instagram...")
        post = instaloader.Post.from_shortcode(bot.context, shortcode)
        
        if post.is_video:
            username = post.owner_username
            caption = post.caption if post.caption else ""
            
            # 🛡️ FILTER SANITASI: Bersihkan emoji dan simbol terlarang dari caption
            caption_bersih = re.sub(r'[^a-zA-Z0-9\s]', '', caption)
            # Ambil maksimal 5 kata pertama agar penamaan file tidak kepanjangan
            kata_caption = caption_bersih.split()
            potongan_deskripsi = "_".join(kata_caption[:5]) if kata_caption else "Video"
            
            # Penggabungan format nama baru: username_potongan_caption
            nama_simpel = f"{username}_{potongan_deskripsi}"
            
            print(f"[+] Pemilik konten terdeteksi: @{username}")
            print(f"[*] Menyiapkan nama file baru: {nama_simpel}.mp4")
            
            try:
                bot.download_post(post, target=IG_STORAGE)
            except Exception as download_fault:
                print(f"[-] Gagal melakukan stream unduhan: {download_fault}")
                return
            
            # 🧹 SISTEM HARD-CLEAN & RENAME OTOMATIS
            print("[*] Mengorganisir berkas dan menghapus file metadata...")
            time.sleep(1) # Jeda aman memastikan sistem operasi selesai menulis berkas
            
            try:
                target_baru = os.path.join(IG_STORAGE, f"{nama_simpel}.mp4")
                
                for item in os.listdir(IG_STORAGE):
                    item_path = os.path.join(IG_STORAGE, item)
                    if os.path.isfile(item_path):
                        # Cari file video bawaan asli instaloader (mengandung shortcode dan berakhiran UTC.mp4)
                        if shortcode in item and item.endswith(".mp4") and "UTC" in item:
                            # Proteksi jika nama file sudah ada agar tidak saling menimpa
                            if os.path.exists(target_baru):
                                target_baru = os.path.join(IG_STORAGE, f"{nama_simpel}_{int(time.time())}.mp4")
                            os.rename(item_path, target_baru)
                        # Hapus paksa semua file liar non-MP4 (.jpg, .txt, .json)
                        elif not item.endswith(".mp4"):
                            os.remove(item_path)
                            
                print(f"[+] SUKSES: Video murni tersimpan sebagai -> {os.path.basename(target_baru)}")
            except OSError as os_cleanup_error:
                print(f"[-] Peringatan saat merapikan nama file: {os_cleanup_error}")
        else:
            print("[-] FORMAT DITOLAK: Konten target bukan berformat Video / Reel.")
            
    except instaloader.exceptions.ConnectionException as conn_err:
        print(f"[-] KONEKSI ERROR: Gagal terhubung ke Instagram, periksa jaringan: {conn_err}")
    except instaloader.exceptions.BadCredentialsException:
        print("[-] AKSES DITOLAK: Akun bersifat privat atau butuh session login.")
    except Exception as general_ig_error:
        print(f"[-] Engine Mendeteksi Error: {general_ig_error}")

def main():
    print("========================================================")
    print("      RIXZ ENGINEERING - SOCIAL MEDIA DOWNLOADER        ")
    print("========================================================")
    
    inisialisasi_sistem()
    daftar_download = ambil_antrean_links()
    
    if not daftar_download:
        print(f"[-] Antrean kosong. Silakan isi URL target Anda di: {LINKS_FILE}")
        return
        
    print(f"[+] Menemukan {len(daftar_download)} target di dalam daftar antrean.")
    
    for url in daftar_download:
        try:
            if "instagram.com" in url:
                download_ig(url)
            else:
                download_yt_tt(url)
        except KeyboardInterrupt:
            print("\n[!] Eksekusi dihentikan paksa oleh pengguna (CTRL+C).")
            sys.exit(0)
        except Exception as loop_error:
            print(f"[-] Terjadi kesalahan fatal saat memproses link {url}: {loop_error}")
            continue 
            
    print("\n[=================== PROSES SELESAI ===================]")

if __name__ == "__main__":
    main()
