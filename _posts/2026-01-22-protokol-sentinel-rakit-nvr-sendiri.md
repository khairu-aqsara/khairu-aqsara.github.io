--- 
layout: post
title: "Protokol Sentinel: Saat Rumah Kebobolan dan CCTV Cuma Jadi Pajangan"
subtitle: "Gas 3kg raib, rekaman bolong-bolong. Saatnya Devan ambil alih keamanan rumah dengan Nmap, Systemd, dan Samba Server."
tags: [security, nmap, ffmpeg, raspberry-pi, systemd, samba, tutorial]
author: Kuli Kode
---

Hujan di luar lagi deres-deresnya, tipe hujan yang bikin kaca jendela bergetar dan suasana hati jadi agak *mellow*. Harusnya sih, ini cuaca yang pas banget buat *coding* santai sambil nyruput kopi item panas. Tapi malem ini, rintik hujan di luar kalah berisik sama detak jantung Devan yang lagi emosi tingkat dewa.

"Hilang, Dev. Beneran hilang dua-duanya. Padahal baru beli kemarin sore," suara Kak Myesha kedengeran bergetar pas dia masuk ke ruang kerja Devan.

Devan nengok, mukanya langsung tegang. "Apa yang hilang, Kak? Jangan bilang..."

"Tabung gas kita, Diambil dari depan dapur," Kak Myesha duduk lemas di kursi kayu pojokan, mukanya pucet campur marah. "Gila ya, profesional nih malingnya, nyolong gas tanpa suara"

Devan langsung berdiri, tangannya ngepal. Ini bukan cuma soal kehilangan barang seharga beberapa puluh ribu. Ini soal privasi. Soal fakta bahwa ada orang asing, tangan-tangan kotor yang nggak diundang, masuk ke area pribadi mereka pas mereka lagi tidur pules. Itu yang bikin merinding.

"CCTV gimana, Kak?" tanya Devan, nyoba tetep logis meskipun darahnya lagi mendidih. "Kan kita pasang O-KAM Pro di teras sama di lorong samping."

Kak Myesha ngebanting pelan HP-nya ke meja kerja Devan. Layarnya nampilin aplikasi O-KAM Pro yang muter-muter *buffering*. "Itu dia masalahnya! Aku udah cek rekaman semalem dari jam 2 sampe jam 4 pagi. Isinya zonk! Kadang ada rekaman 10 detik, terus tiba-tiba lompat ke 10 menit kemudian. Pas kejadian... nggak ada rekamannya sama sekali!"

"Hah? Kok bisa?" Devan ngambil HP kakaknya, nge-scroll timeline yang warnanya biru-biru putus itu. "Motion detection-nya aktif kan?"

"Aktif! Tapi ya gitu, dia cuma rekam pas dia 'ngerasa' ada gerakan. Dan parahnya lagi, aku mau download rekamannya buat lapor ke grup warga aja susah banget. Harus di-*play* dulu di HP, terus di-*screen record*. Mau cabut memorinya (TF Card), kameranya tinggi banget, harus pake tangga lipat. Ribet bener dah!" Kak Myesha mijet keningnya frustrasi.

Devan ngeliat kamera CCTV putih tanpa merek yang nangkring di pojokan plafon. Kamera "Smart Home" murah meriah yang dulu mereka beli karena tergiur embel-embel "Artificial Intelligence" dan "Cloud Storage". Kenyataannya? Pas dibutuhin malah jadi pajangan doang.

"Cukup," kata Devan dingin. Dia ngerasa gagal ngelindungin kakaknya karena terlalu percaya sama teknologi kaleng-kaleng ini. "Kita nggak bisa ngandelin sistem bodoh ini lagi. Kita nggak tau IP-nya berapa, merek aslinya apa, atau datanya lari ke mana. Hari ini aku bakal bongkar protokolnya. Kita bikin mata yang beneran melek 24 jam."

## Bab 1: Interogasi Jaringan (Siapa Kalian Sebenarnya?)

Devan masuk ke "guanya"—kamar kerjanya yang penuh kabel dan aroma solder. Kak Myesha ngikutin, bawa segelas air putih dingin buat adiknya, sekaligus buat nenangin dirinya sendiri.

"Kak, langkah pertama kalau mau ngelawan musuh yang nggak kelihatan adalah... kenalan dulu. Kita harus tau CCTV ini sebenernya makhluk apa."

Devan buka terminal di MacBook-nya. Dia butuh **Nmap**.

"Pertama, kita cek dulu alamat rumah kita sendiri—maksudnya alamat IP laptop ini, biar kita tau kita ada di blok mana."

```bash
# Cek IP address sendiri
ifconfig | grep inet
```

Muncul angka `192.168.1.5`. Berarti jaringan lokal mereka ada di kisaran `192.168.1.0/24`.

"Nah, sekarang saatnya kita 'teriak' ke satu jaringan rumah: *WOI SIAPA AJA YANG ONLINE?!*"

```bash
# Scan santuy buat nyari siapa aja yang idup (Host Discovery)
sudo nmap -sn 192.168.1.0/24
```

Layar terminal langsung penuh tulisan. Ada HP-nya Kak Myesha, Smart TV, kulkas pinter, dan... ada dua IP yang namanya nggak jelas: `192.168.1.8` dan `192.168.1.14`.

"Liat nih, Kak. MAC Address-nya `Unknown` atau kadang `Generic`. Biasanya kalau barang bermerek kayak Samsung atau Apple, ketahuan. Ini *Generic Chinese Board*. Fix ini kameranya."

Sekarang Devan mau tau "pintu" (port) mana yang mereka buka. Apakah ada celah buat ngambil videonya secara paksa?

"Kita lakuin *Full Scan*. Aku mau tau OS-nya apa, dan pintu apa aja yang kebuka. Kita pake mode agresif `-A`."

```bash
# Scan agresif ke IP target buat nyari celah pintu masuk
# -p- artinya scan SEMUA port dari 1 sampe 65535 (jangan ada yang lolos)
sudo nmap -A -p- 192.168.1.14
```

Devan nunggu dengan tegang. Hasilnya keluar:

```text
PORT      STATE  SERVICE    VERSION
80/tcp    closed http
554/tcp   closed rtsp
8000/tcp  closed http-alt
10554/tcp open   tcpwrapped
10555/tcp open   tcpwrapped
MAC Address: 18:EF:3C:XX:XX:XX (Unknown)
OS details: Embedded Linux 2.6.X - 3.X
```

"Sialan," umpat Devan pelan. "Pintu utamanya (Port 554) ditutup rapet. Padahal itu standar video (RTSP). Tapi... liat port `10554` sama `10555` ini. Statusnya `tcpwrapped`. Ini pintu belakang yang disembunyiin."

## Bab 2: Membobol Rumah Sendiri (The RTSP Quest)

"Terus gimana? Kita tetep nggak bisa liat isinya dong?" tanya Kak Myesha lemas.

"Bisa. Tapi kita harus nebak kuncinya. Protokol video itu namanya RTSP. Kita harus nemuin URL lengkapnya."

Devan mulai fase *trial and error* pake **VLC Player**.

1.  Coba port standar: `rtsp://192.168.1.14:554/live` ❌ Gagal.
2.  Coba port tersembunyi tanpa password: `rtsp://192.168.1.14:10554/stream` ❌ Gagal.

"Password-nya apa ya, Kak? Inget nggak pas *setup* awal?"

"Kayaknya `admin` terus `888888` deh? Atau kosong?" Kak Myesha ragu.

Devan nyoba kombinasi password *default* kamera VStarcam (karena biasanya O-KAM itu *rebrand* dari sana).

Dia ketik URL ini: `rtsp://admin:888888@192.168.1.14:10555/tcp/av0_0`

*Enter.*

Layar VLC loading sebentar... dan MUNCUL! Gambar lorong samping rumah yang gelap tapi jelas.

"DAPET!" seru Devan. "Port 10555, user `admin`, password `888888`, path `/tcp/av0_0`. Ini kuncinya!"

## Bab 3: Merakit Sang Penjaga (Hardware Setup)

"Sekarang, kita butuh alat yang melek 24 jam buat ngerekam ini. Laptopku nggak mungkin nyala terus," kata Devan sambil ngeluarin **Raspberry Pi 5** dan **SSD 256GB**.

"Pertama, kita siapin SSD-nya. Kita format pake **exFAT** aja biar kalau darurat bisa Kakak colok ke Windows atau Mac."

Devan nyolok SSD ke Raspberry Pi, terus masuk ke terminal Pi.

```bash
# Cek dulu drive-nya yang mana (biasanya /dev/sda)
sudo fdisk -l

# Masuk ke tool partisi
sudo fdisk /dev/sda
# (Di dalem fdisk: hapus partisi lama 'd', bikin baru 'n', simpen 'w')

# Format jadi exFAT
sudo mkfs.exfat /dev/sda1
```

Terus Devan bikin folder "gudang" dan masang SSD-nya di sana.

```bash
sudo mkdir -p /mnt/cctv_storage
# Kita butuh UUID biar mounting-nya permanen
sudo blkid
```

Devan ngopi kode aneh (UUID) dari layar, terus ngedit file `/etc/fstab` biar SSD-nya otomatis nyantol pas nyala.

```text
UUID=6915-704C /mnt/cctv_storage exfat defaults,auto,users,rw,nofail 0 0
```

"Sip. Gudang penyimpanan siap. Kapasitas 256GB, cukup buat 10 hari *full recording* dua kamera."

## Bab 4: Membuat Layanan Abadi (Systemd Service)

"Dulu aku suka pake *Cron Job* buat jalanin skrip otomatis, Kak. Tapi buat keamanan, itu kurang *badass*," kata Devan sambil ngetik skrip perekam.

"Kenapa?"

"Kalau *Cron*, dia cuma jalanin sekali pas nyala. Kalau tiba-tiba programnya *crash* atau *error* di tengah jalan, dia bakal mati dan nggak bangun lagi. Kita bakal kehilangan rekaman tanpa sadar."

Devan nunjukin layar. "Kita bakal pake **Systemd**. Ini standar industri server. Kalau programnya mati, Systemd bakal ngehidupin lagi secara otomatis dalam 5 detik. Kayak zombie yang nggak bisa mati."

Devan bikin file skrip dulu di `/usr/local/bin/cctv_record.sh`:

```bash
#!/bin/bash
STORAGE="/mnt/cctv_storage"
CAM_SAMPING="rtsp://admin:888888@192.168.1.14:10555/tcp/av0_0"
CAM_DEPAN="rtsp://admin:888888@192.168.1.8:10554/tcp/av0_0"

# Rekam Kamera Samping (Potong tiap 1 jam)
ffmpeg -i "$CAM_SAMPING" -c copy -f segment -segment_time 3600 \
  -strftime 1 "$STORAGE/Samping_%Y-%m-%d_%H-%M-%S.mp4" &

# Rekam Kamera Depan
ffmpeg -i "$CAM_DEPAN" -c copy -f segment -segment_time 3600 \
  -strftime 1 "$STORAGE/Depan_%Y-%m-%d_%H-%M-%S.mp4" &

# Auto-delete video > 5 hari
find "$STORAGE" -name "*.mp4" -mtime +5 -delete

wait
```

Setelah skripnya jadi dan bisa dieksekusi (`chmod +x`), Devan bikin "mantra" Systemd-nya di `/etc/systemd/system/cctv.service`:

```ini
[Unit]
Description=CCTV Sentinel Recording Service
After=network.target

[Service]
ExecStart=/usr/local/bin/cctv_record.sh
Restart=always
RestartSec=5
User=pi

[Install]
WantedBy=multi-user.target
```

"Liat baris `Restart=always` ini, Kak? Ini jaminannya. Mau badai, mau error, dia bakal bangkit lagi."

Devan ngaktifin servisnya:

```bash
sudo systemctl enable cctv
sudo systemctl start cctv
```

## Bab 5: Berbagi Mata (Samba Server)

Sistem udah jalan. Lampu SSD kedip-kedip sibuk.

"Terus, kalau Kakak mau liat rekamannya gimana? Harus cabut SSD-nya?" tanya Kak Myesha.

"Nggak dong. Itu kuno. Kita bikin SSD ini jadi folder jaringan yang bisa diakses dari laptop Kakak lewat WiFi. Namanya **Samba Server**."

Devan install paketnya di Raspberry Pi:

```bash
sudo apt install samba samba-common-bin -y
```

Terus dia edit konfigurasi di `/etc/samba/smb.conf`, nambahin blok ini di paling bawah:

```ini
[CCTV]
path = /mnt/cctv_storage
writeable = yes
browseable = yes
public = yes
create mask = 0777
directory mask = 0777
force user = pi
```

"Terakhir, kita kasih password biar aman."

```bash
sudo smbpasswd -a pi
# Masukin password baru buat akses file
sudo systemctl restart smbd
```

"Coba Kakak buka Finder di Mac, tekan `Cmd+K`, terus ketik `smb://192.168.1.X` (IP Raspberry Pi)."

Kak Myesha nyoba. Tiba-tiba muncul folder `CCTV_Gudang`. Pas diklik, isinya berderet file video `.mp4` yang baru aja kerekam. Dia klik salah satu, dan videonya langsung keputer di laptopnya tanpa perlu copy-paste, tanpa perlu internet, tanpa perlu cabut kabel.

"Gila..." Kak Myesha geleng-geleng kepala. "Ini sih lebih canggih dari aplikasi aslinya, Dev. Aku bisa nonton sambil tiduran di kamar tanpa nunggu *loading* server China."

Devan senyum puas. "Sekarang rumah kita aman, Kak. Gas yang ilang biarin aja, tapi mulai malam ini, nggak ada satu debu pun yang gerak di rumah ini tanpa ijin kita."

Hujan udah reda. Di layar laptop Kak Myesha, rekaman CCTV berjalan mulus, menampilkan halaman rumah yang tenang. Di pojokan, Raspberry Pi 5 bekerja dalam diam, dijaga oleh Systemd yang setia, menyimpan memori ke SSD, dan membagikannya lewat Samba.

Protokol Sentinel aktif. Dan malam ini, mereka bisa tidur nyenyak.

---

### Rangkuman Teknis (Cheat Sheet):

1.  **Nmap Full Scan**: Gunakan `sudo nmap -A -p- <IP>` untuk membongkar port tersembunyi (seperti 10554/10555) yang sering dipakai vendor CCTV "bandel".
2.  **RTSP Discovery**: Jangan nyerah kalau port 554 tertutup. Coba port tinggi (8000-10000) dengan path umum seperti `/tcp/av0_0` atau `/live`.
3.  **Storage**: Format SSD ke **exFAT** untuk fleksibilitas maksimal, pasang via `/etc/fstab` menggunakan UUID agar mounting stabil.
4.  **Automation**: Tinggalkan Cron. Gunakan **Systemd Service** (`Restart=always`) untuk layanan kritis seperti CCTV. Ini memastikan *uptime* maksimal.
5.  **Access**: Gunakan **Samba** (`smb.conf`) untuk mempermudah akses file rekaman dari perangkat lain (Windows/Mac/Android) dalam satu jaringan lokal tanpa cabut-pasang hardware.