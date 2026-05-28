# Social Media Downloader - Termux Dedicated

Script otomatisasi berbasis Python untuk mengunduh media dari YouTube, TikTok, dan Instagram langsung ke penyimpanan internal Android.

## ⚙️ Perintah Instalasi (One-Click Setup)

Jalankan rangkaian perintah berikut pada terminal Termux:
```bash
pkg update -y && pkg upgrade -y && pkg install python python-pip git ffmpeg -y && git clone https://github.com/muizka/social-media-downloader.git && cd ~/social-media-downloader && pip install -r requirements.txt --break-system-packages && termux-setup-storage && python main.py
```

## 🔄 Penggunaan Sehari-hari

Jalankan perintah ini jika ingin mengunduh lagi di lain waktu:
```bash
cd ~/social-media-downloader && python main.py
```
