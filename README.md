# Social Media Downloader - Termux Dedicated

Script otomatisasi berbasis Python untuk mengunduh media dari YouTube, TikTok, dan Instagram langsung ke penyimpanan internal Android.

## ⚙️ Perintah Instalasi (One-Click Setup)

Jalankan rangkaian perintah berikut pada terminal Termux:
```bash
pkg update -y && pkg upgrade -y && pkg install python python-pip git ffmpeg -y && git clone https://github.com/muizka/social-media-downloader.git && cd ~/social-media-downloader && pip install -r requirements.txt --break-system-packages && termux-setup-storage && python main.py
```

## 📋 Tata Cara Penggunaan File links.txt

Setelah menjalankan perintah instalasi di atas, skrip akan otomatis membuat file antrean bernama `links.txt`. Ikuti langkah ini untuk mulai mendownload:

1. **Buka File Manager** di HP lu.
2. Masuk ke **Penyimpanan Internal** > folder **Download**.
3. Cari dan buka file bernama **`links.txt`** menggunakan aplikasi teks editor bawaan HP.
4. **Tempelkan (paste) URL/Link** video YouTube, TikTok, atau Instagram yang mau lu download.
5. Aturan pengisian: **Wajib satu link per baris** (jangan digabung dalam satu baris).
6. **Simpan (Save)** file `links.txt` tersebut setelah selesai mengisi link.

## 🔄 Penggunaan Sehari-hari

Kembali ke Termux, lalu jalankan perintah ini jika ingin mengeksekusi proses download atau menggunakannya lagi di lain waktu:
```bash
cd ~/social-media-downloader && python main.py
```
