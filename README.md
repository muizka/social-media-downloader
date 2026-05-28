# Auto Media Downloader (Termux Android Dedicated)

Script otomatisasi berbasis Python untuk mengunduh video dari **YouTube**, **TikTok** (tanpa watermark), dan **Instagram** (Post/Reels) secara massal (*batch*) langsung dari file konfigurasi teks di penyimpanan internal HP Android.

---

## 📋 Persyaratan Sistem
* Aplikasi **Termux** versi terbaru (Disarankan dari F-Droid atau GitHub).
* Koneksi internet aktif.
* Izin akses penyimpanan internal sudah diberikan.

---

## ⚙️ Persiapan Awal & Perintah Setup (Wajib)

### 1. Izin Akses Penyimpanan
Jalankan perintah ini di Termux dan pilih **Allow/Izinkan** pada pop-up yang muncul:
```bash
termux-setup-storage
one klik
pkg update -y && pkg upgrade -y && pkg install python ffmpeg git -y && git clone [https://github.com/muizka/social-media-downloader.git](https://github.com/muizka/social-media-downloader.git) && cd social-media-downloader && pip install --upgrade pip && pip install -r requirements.txt
step by step
# 1. Memperbarui indeks paket dan melakukan upgrade package bawaan Termux
pkg update -y && pkg upgrade -y

# 2. Menginstal Python environment (Bahasa pemrograman utama script)
pkg install python -y

# 3. Menginstal FFmpeg (Penting untuk menggabungkan video & audio kualitas tinggi pada YouTube)
pkg install ffmpeg -y

# 4. Menginstal Git tool (Untuk mengunduh source code dari GitHub)
pkg install git -y

# 5. Mengkloning repositori project ini ke dalam lokal Termux
git clone [https://github.com/muizka/social-media-downloader.git](https://github.com/muizka/social-media-downloader.git)

# 6. Masuk ke dalam direktori/folder project yang baru diunduh
cd social-media-downloader

# 7. Memperbarui pip installer ke versi terbaru
pip install --upgrade pip

# 8. Menginstal seluruh library Python eksternal (yt-dlp & instaloader) yang ada di requirements.txt
pip install -r requirements.txt
