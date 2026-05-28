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
```

### 2. Perintah Setup & Instalasi Lengkap

#### Pilihan A: One-Click (Salin & Tempel Sekaligus)
```bash
pkg update -y && pkg upgrade -y && pkg install python ffmpeg git -y && git clone https://github.com && cd social-media-downloader && pip install -r requirements.txt --break-system-packages
```

#### Pilihan B: Step by Step (Manual)
```bash
# 1. Memperbarui indeks paket dan melakukan upgrade package bawaan Termux
pkg update -y && pkg upgrade -y

# 2. Menginstal Python environment (Bahasa pemrograman utama script)
pkg install python -y

# 3. Menginstal FFmpeg (Penting untuk menggabungkan video & audio kualitas tinggi pada YouTube)
pkg install ffmpeg -y

# 4. Menginstal Git tool (Untuk mengunduh source code dari GitHub)
git clone https://github.com

# 5. Masuk ke dalam direktori/folder project yang baru diunduh
cd social-media-downloader

# 6. Menginstal seluruh library Python eksternal (yt-dlp & instaloader) dengan flag wajib Termux
pip install -r requirements.txt --break-system-packages
```

---

## 🛠️ Cara Penggunaan

### Langkah 1: Inisialisasi & Instalasi Library
Pastikan semua library terpasang terlebih dahulu, kemudian jalankan script pertama kali untuk membuat file antrean otomatis:
```bash
pip install -r requirements.txt --break-system-packages && python main.py
```
Script akan membuat file `links.txt` secara otomatis di folder **Download** internal HP lu.

### Langkah 2: Isi Link Video
1. Buka File Manager HP > Folder **Download**.
2. Buka file `links.txt`.
3. Tempel URL video (YouTube, TikTok, atau Instagram), **satu link per baris**.
4. Simpan file tersebut.

### Langkah 3: Eksekusi Download
Kembali ke Termux dan jalankan perintah:
```bash
pip install -r requirements.txt --break-system-packages && python main.py
```
Video akan otomatis terdownload dan muncul di Galeri HP lu.

---

## 🔄 Perintah Penggunaan Harian
Jika ingin mendownload lagi di lain waktu, cukup jalankan rangkaian perintah ini agar library tetap aman dan skrip langsung berjalan:
```bash
cd ~/social-media-downloader && pip install -r requirements.txt --break-system-packages && python main.py
```

---

## 🛠️ Troubleshooting (Solusi Masalah)

* **Video YouTube Terpisah Antara Gambar & Audio (Tidak Menyatu):**
  Ah, kalau hasil download video YouTube resolusi tinggi (1080p ke atas) hasilnya terpisah antara video dan audio (nggak menyatu), itu tandanya **FFmpeg belum terinstal sempurna** atau **Termux belum bisa membaca path FFmpeg** di HP lu.
  
  Library `yt-dlp` yang lu pakai di dalam script Python itu butuh FFmpeg sebagai "tukang jahit" otomatis untuk menyatukan berkas video (*stream* gambar HD) dan berkas audio (*stream* suara) setelah proses download selesai.

  **Cara Beresinnya (Eksekusi di Termux):**
  Gak perlu bongkar kode `main.py` lu, cukup jalankan dua perintah perbaikan ini secara berurutan di Termux:

  **Langkah 1: Instal ulang FFmpeg sampai bersih**
  ```bash
  pkg install ffmpeg --reinstall -y
  ```
  *(Tunggu sampai proses instalasi selesai 100% dan pastikan tidak ada error di terminal).*

  **Langkah 2: Update juga library `yt-dlp` lu ke versi terbaru**
  ```bash
  pip install --upgrade yt-dlp --break-system-packages
  ```

  **🚀 Cara Tes Hasilnya**
  Setelah dua langkah di atas selesai, silakan jalankan kembali script downloader lu:
  ```bash
  pip install -r requirements.txt --break-system-packages && python main.py
  ```
  Jika FFmpeg sudah terinstal dengan benar, lu bakal melihat proses tambahan di terminal setelah download selesai berupa tulisan **`[Merger] Merging formats into "mp4"`**. Itu tandanya video dan audionya sudah sukses dijahit jadi satu file utuh yang siap lu tonton di galeri!

* **Error: Installing pip is forbidden:** Python Termux melarang upgrade pip. Lewati perintah upgrade pip dan langsung gunakan flag `--break-system-packages`.

* **ModuleNotFoundError (instaloader/yt-dlp):** Jalankan perintah `pip install yt-dlp instaloader --break-system-packages` untuk memaksa instalasi library.

* **Gagal Baca File:** Jalankan `termux-setup-storage` ulang untuk memastikan izin akses memori aktif.

---

## 📌 Fitur Utama
* **TikTok No-Watermark:** Video bersih tanpa logo TikTok.
* **YouTube HQ:** Download resolusi tinggi (1080p ke atas) dengan audio jernih.
* **Instagram Auto-Folder:** Konten IG dipisahkan secara rapi di folder `IG_Downloads`.
