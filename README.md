# Auto Media Downloader - Command Only

## ⚙️ Setup & Instalasi

### Pilihan A: One-Click (Salin Semua)
```bash
termux-setup-storage && pkg update -y && pkg upgrade -y && pkg install tur-repo -y && pkg update -y && pkg install python ffmpeg git -y && git clone https://github.com/muizka/social-media-downloader.git && cd social-media-downloader && pip install -r requirements.txt --break-system-packages
```

### Pilihan B: Step-by-Step
```bash
termux-setup-storage
pkg update -y && pkg upgrade -y
pkg install tur-repo -y && pkg update -y
pkg install python ffmpeg git -y
git clone https://github.com/muizka/social-media-downloader.git
cd social-media-downloader && pip install -r requirements.txt --break-system-packages
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

### Solusi Video & Audio YouTube Terpisah
```bash
pkg install ffmpeg --reinstall -y && pip install --upgrade yt-dlp --break-system-packages
```

### Solusi ModuleNotFoundError
```bash
pip install yt-dlp instaloader --break-system-packages
```

### Solusi Izin Akses Folder Ditolak
```bash
termux-setup-storage
```
