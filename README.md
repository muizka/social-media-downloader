# Auto Media Downloader - Command Only

## ⚙️ Setup & Instalasi

### Pilihan A: One-Click (Salin Semua)
```bash
termux-setup-storage && pkg update -y && pkg upgrade -y && pkg install python ffmpeg git -y && git clone https://github.com && cd social-media-downloader && pip install -r requirements.txt --break-system-packages
```

### Pilihan B: Step-by-Step
```bash
termux-setup-storage
pkg update -y && pkg upgrade -y
pkg install python -y
pkg install ffmpeg -y
pkg install git -y
git clone https://github.com
cd social-media-downloader
pip install -r requirements.txt --break-system-packages
```

---

## 🛠️ Penggunaan

### Inisialisasi awal / Eksekusi Download
```bash
python main.py
```

### Jalankan Ulang di Lain Waktu
```bash
cd ~/social-media-downloader && python main.py
```

---

## 🛠️ Troubleshooting (Perbaikan Instan)
```bash
# Perbaiki izin memori
termux-setup-storage

# Paksa instal ulang ffmpeg jika audio rusak
pkg install ffmpeg --reinstall -y

# Update library downloader ke versi terbaru
pip install --upgrade yt-dlp instaloader --break-system-packages
```
