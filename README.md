# Auto Media Downloader - Command Only

## ⚙️ Setup & Instalasi

### Pilihan A: One-Click (Salin Semua)
```bash
termux-setup-storage && pkg update -y && pkg upgrade -y && pkg install python ffmpeg git -y && git clone https://github.com/muizka/social-media-downloader.git && cd social-media-downloader && pip install --upgrade pip && pip install -r requirements.txt
```

### Pilihan B: Step-by-Step
```bash
termux-setup-storage
pkg update -y && pkg upgrade -y
pkg install python -y
pkg install ffmpeg -y
pkg install git -y
git clone https://github.com/muizka/social-media-downloader.git
cd social-media-downloader
pip install --upgrade pip
pip install -r requirements.txt
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
pip install --upgrade yt-dlp instaloader
```
