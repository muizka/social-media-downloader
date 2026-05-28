Mantap, ini draf final `README.md` yang sudah dirapikan total sesuai dengan format yang kamu inginkan. Semua link yang ganda otomatis dibersihkan agar tampilannya bersih dan profesional saat di-upload ke GitHub.

### 📄 Isi Lengkap File `README.md`

```markdown
# Auto Media Downloader (Termux Android Dedicated)

Script otomatisasi berbasis Python untuk mengunduh video dari **YouTube**, **TikTok** (tanpa watermark), dan **Instagram** (Post/Reels) secara massal (*batch*) langsung dari file konfigurasi teks di penyimpanan internal HP Android.

---

## 📋 Persyaratan Sistem (Prerequisites)

Sebelum melakukan setup, pastikan perangkat kamu memenuhi kriteria berikut:
* Aplikasi **Termux** versi terbaru (Disarankan unduh via F-Droid atau GitHub, jangan versi Play Store karena sudah *deprecated*).
* Koneksi internet yang stabil untuk mengunduh package sistem.
* Ruang penyimpanan internal yang cukup untuk menyimpan hasil unduhan video.

---

## ⚙️ Persiapan Awal & Perintah Setup (Wajib)

Sebelum program bisa berjalan, aplikasi Termux harus diberi izin untuk mengakses memori internal HP kamu agar bisa membaca konfigurasi `links.txt` dan menyimpan video hasil download ke galeri.

### 1. Berikan Izin Akses Penyimpanan (Storage Permission)
Jalankan perintah ini di Termux:
```bash
termux-setup-storage

```

* **Catatan Penting:** Ketika pop-up persetujuan sistem Android muncul di layar ponsel kamu, pastikan untuk memilih **Allow** atau **Izinkan**. Jika tidak, Termux akan mengalami error *Permission Denied*.

### 2. Perintah Setup Sistem & Instalasi Lengkap

Kamu bisa memilih salah satu dari dua metode di bawah ini untuk mengonfigurasi seluruh kebutuhan program:

#### Pilihan A: One-Click (Salin & Tempel Sekaligus)

Salin seluruh baris perintah di bawah ini, tempel ke Termux, lalu tekan enter. Semua proses update, install tools, clone repo, hingga install library akan berjalan otomatis sampai selesai:

```bash
pkg update -y && pkg upgrade -y && pkg install python ffmpeg git -y && git clone [https://github.com/muizka/social-media-downloader.git](https://github.com/muizka/social-media-downloader.git) && cd social-media-downloader && pip install --upgrade pip && pip install -r requirements.txt

```

#### Pilihan B: Manual (Baris demi Baris)

Jika ingin mengeksekusi dan memantau jalannya proses instalasi satu per satu, gunakan daftar perintah berikut:

```bash
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

```

---

## 🛠️ Alur Lengkap Cara Penggunaan

Setelah seluruh rangkaian perintah setup di atas berhasil diselesaikan, ikuti panduan langkah demi langkah di bawah ini untuk memulai proses pengunduhan:

### Langkah 1: Inisialisasi Environment Lokal

Jalankan script utama untuk pertama kalinya guna memicu pembuatan file konfigurasi teks pada memori internal secara otomatis:

```bash
python main.py

```

* **Keterangan:** Program akan mendeteksi bahwa file konfigurasi belum tersedia di HP kamu, kemudian otomatis membuat folder atau file bernama `links.txt` di direktori **Penyimpanan Internal > Download**.

### Langkah 2: Memasukkan Tautan (URL) Target

1. Keluar sejenak dari Termux (jangan dikeluarkan dari *recent apps*).
2. Buka aplikasi **File Manager** atau **Pengelola File** bawaan HP Android kamu.
3. Masuk ke direktori **Penyimpanan Internal** (Internal Storage) > buka folder **Download**.
4. Buka file bernama `links.txt` menggunakan aplikasi teks editor bawaan HP.
5. Tempel (*paste*) semua URL video target (YouTube, TikTok, atau Instagram) yang ingin kamu unduh.
6. **Aturan Penulisan:** Pastikan hanya memasukkan **satu link per baris**. Anda bisa memasukkan banyak link sekaligus (Multi-download).
7. Simpan (*Save*) perubahan pada file tersebut.

### Langkah 3: Eksekusi Proses Unduhan

Kembali ke aplikasi Termux, lalu jalankan kembali perintah utama berikut:

```bash
python main.py

```

* **Keterangan:** Script akan otomatis membaca isi file `links.txt`, memvalidasi jenis platform link tersebut, melakukan *bypass* enkripsi, dan mengunduh video satu per satu. Semua file video yang berhasil diunduh akan langsung tersimpan di folder Download internal HP sehingga langsung terdeteksi oleh Galeri foto kamu.

---

## 🔄 Perintah Penggunaan Sehari-hari (Daily Use)

Jika di kemudian hari kamu ingin mengunduh video baru lagi, kamu **tidak perlu lagi** mengulang langkah instalasi atau setup dari awal. Kamu cukup melakukan prosedur cepat ini:

1. Modifikasi atau perbarui daftar tautan video di file `Download/links.txt` melalui File Manager HP kamu (hapus link lama yang sudah selesai didownload).
2. Buka aplikasi Termux, lalu langsung ketik perintah *shortcut* berikut:

```bash
cd ~/social-media-downloader && python main.py

```

---

## 🛠️ Troubleshooting (Penanganan Masalah)

* **Error: `ModuleNotFoundError` saat menjalankan `main.py**`
* *Penyebab:* Library pendukung belum terinstall sempurna atau terputus di tengah jalan.
* *Solusi:* Jalankan kembali perintah `pip install -r requirements.txt` di dalam folder project.


* **Error: `Permission Denied` atau File Tidak Ditemukan**
* *Penyebab:* Termux kehilangan akses ke storage internal Android karena kebijakan manajemen memori OS.
* *Solusi:* Jalankan ulang perintah `termux-setup-storage`, lalu pastikan status perizinan aplikasi Termux di pengaturan sistem Android berada pada posisi "Izinkan Mengakses File".


* **Masalah: Video YouTube resolusi 1080p ke atas tidak memiliki audio**
* *Penyebab:* Paket encoder FFmpeg belum terpasang atau mengalami korup di Termux.
* *Solusi:* Jalankan perintah `pkg install ffmpeg -y` untuk memastikan pustaka penggabung audio-video telah aktif.



---

## 📌 Fitur Utama Script

* **Mendukung Multi-Platform:** Deteksi otomatis tanpa perlu memilih menu secara manual untuk YouTube, TikTok, dan Instagram.
* **TikTok No-Watermark:** Mengunduh berkas video murni langsung dari CDN TikTok tanpa ada logo/watermark yang mengganggu.
* **High-Quality YouTube Audio/Video Muxing:** Otomatis mengambil stream video tertinggi dan stream audio terbaik lalu menyatukannya menjadi format `.mp4`.
* **Rapi & Terstruktur:** Konten Instagram akan dikelompokkan secara terpisah di dalam folder khusus pada jalur `Penyimpanan Internal/Download/IG_Downloads`.

```

```
