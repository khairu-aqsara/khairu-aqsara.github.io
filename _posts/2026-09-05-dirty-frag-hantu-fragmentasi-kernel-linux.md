---
layout: post
title: "Dirty Frag: Ketika Fragmen Paket Membongkar Pintu Root di Kernel Linux"
subtitle: "Malam mencekam saat Devan, Kak Myesha, dan Jovian berpacu dengan waktu melawan exploit publik yang mengincar celah gelap di jantung kernel Linux."
date: 2026-09-05 23:40:00 +0700
categories: [Engineering, Security, Story]
tags: [Linux Kernel, CVE-2026-43284, CVE-2026-43500, Dirty Frag, Privilege Escalation, Security]
---

## Bab 1: Bisikan dari Forum Gelap Takengon

Sinyal internet di Takengon nggak pernah bisa diandalkan. Jovian udah tiga hari di sana, nemenin Ayah beres-beres kebun kopi peninggalan kakek, sambil kerja *remote* nyambi *laptop* yang baterainya udah mulai ngambek. Malam itu kabut turun lebih cepat dari biasanya, dan satu-satunya cahaya di kamar cuma dari layar *laptop* yang nampilin sebuah forum yang jarang dia buka: forum *underground* tempat *exploit developer* saling pamer *proof-of-concept*.

Dia awalnya cuma iseng *scrolling*. Tapi satu *thread* bikin jantungnya berhenti sepersekian detik.

`[RELEASE] DirtyFrag — full LPE chain, kernel <= backport window, PoC + writeup attached`

Nama penulisnya nggak asing buat orang yang ngikutin dunia *kernel security*: peneliti yang beberapa bulan lalu juga nemuin bug sekelas di *subsystem* jaringan. Jovian buka *thread*-nya, dan yang dia baca bikin bulu kuduknya berdiri. Ada tautan ke *repository* publik, ada video demo *exploit* yang jalan mulus dari *user* biasa ke `root` cuma dalam hitungan detik, dan yang paling bikin nggak enak: ada daftar komentar dari orang-orang yang udah nyoba di server orang lain, pamer *screenshot* `id` yang keluar `uid=0(root)`.

"Anjir," gumam Jovian sendirian di kamar yang dingin. Dia langsung buka Telegram, ketik cepat ke grup keluarga kerja: dia, Devan, dan Kak Myesha.

*"Bang, Kak, ada exploit LPE kernel Linux baru namanya Dirty Frag. PoC-nya udah publik. Server kita yang di Sleman kena nggak ya?"*

Devan yang malam itu lagi di kosannya di Sleman, lagi asik nonton ulang pertandingan bola, langsung ngerasa firasat nggak enak begitu notifikasi itu masuk. Dia buka pesannya, klik tautan yang dikirim Jovian, dan mulai baca cepat.

Yang bikin dia makin tegang bukan cuma karena ada *exploit* baru. Tapi karena dia inget, server *production client* yang dia pegang — server yang sama yang dulu pernah kena drama *polymorphic code* — jalan di atas *distro* dan versi kernel yang, setahu dia, belum pernah dia cek ulang sejak *deployment* terakhir berbulan-bulan lalu.

"Jov, kamu ada info CVE-nya nggak? Aku mau cek apa kernel kita kena," balas Devan, jarinya udah gemeteran ngetik.

*"Ada, Bang. CVE-2026-43284 sama CVE-2026-43500. Yang pertama di modul esp4/esp6 (xfrm, buat IPsec), yang kedua di rxrpc. Katanya dua-duanya digabung jadi satu rantai exploit."*

Devan langsung buka *laptop*-nya, SSH ke server *client*. Sebelum jari-jarinya sempat ngetik apapun, dia berhenti sejenak. Ini bukan cuma soal nyari *bug* di kode aplikasi kayak biasanya. Ini soal kernel — lapisan paling dalam dari sistem operasi, tempat semua *proses* dan semua *user* pada akhirnya harus percaya penuh. Kalau kernel bisa ditembus, nggak peduli seberapa rapi kode aplikasi di atasnya, semuanya runtuh.

Dia ketik pesan balik ke grup. "Oke. Aku mulai investigasi sekarang. Jov, kirim link *writeup*-nya. Kak Myesha, ada waktu buat *standby*? Ini kelihatannya bakal panjang."

Balasan dari Kak Myesha datang beberapa detik kemudian, singkat tapi tegas, khas seorang *Tech Lead* yang udah kenyang sama insiden tengah malam. "Standby. Kirim hasil `uname -a` sama `os-release` dulu. Jangan buru-buru ambil kesimpulan sebelum data lengkap."

Malam itu, tanpa mereka sadari, di sisi lain internet, ada proses *scanning* otomatis yang udah mulai jalan — menyisir jutaan alamat IP publik, mencari server yang portnya terbuka dan kernelnya belum di-*patch*. Perlombaan sudah dimulai, dan mereka bahkan belum tahu berapa lama waktu yang tersisa.


## Bab 2: Jejak di /proc dan Bayang-Bayang Dirty Pipe

Devan mulai dari dasar. Prinsip pertama dalam investigasi keamanan: jangan pernah asumsi, selalu verifikasi dengan data mentah dari sistem itu sendiri.

```bash
uname -a
cat /etc/os-release | head -5
cat /var/run/reboot-required 2>/dev/null || echo "tidak perlu reboot"
```

Hasilnya muncul di layar terminal:

```text
Linux prod-app-01 7.0.0-30-generic #30-Ubuntu SMP x86_64 GNU/Linux
NAME="Ubuntu"
VERSION="26.04 LTS (Nautical Narwhal)"
tidak perlu reboot
```

"Kernel 7.0.0-30-generic, Ubuntu 26.04 LTS," ketik Devan ke grup. "Nggak ada tanda butuh *reboot*, jadi ini kernel yang lagi aktif sekarang."

Balasan Kak Myesha masuk cepat. "Oke. Sekarang cek apakah modulnya termuat. `esp4`, `esp6`, sama `rxrpc`."

Devan ketik perintahnya.

```bash
lsmod | grep -E '^(esp|rxrpc|af_rxrpc)'
find /lib/modules/$(uname -r) -name 'esp*.ko*' -o -name 'rxrpc*.ko*'
```

`lsmod`-nya kosong. Nggak ada satupun dari ketiga modul itu yang lagi termuat di memori. Tapi `find` di direktori modul nunjukin hasil yang bikin dia makin waspada: `esp4.ko.zst`, `esp6.ko.zst`, `rxrpc.ko.zst`, semuanya ada, siap dimuat kapan saja.

"Modulnya kosong di `lsmod`, tapi ada di disk," lapor Devan.

"Itu justru yang bahaya," balas Kak Myesha. "Di Ubuntu, kedua modul itu bukan sesuatu yang harus dimuat manual sama *admin*. Mereka *auto-load* begitu ada *proses* yang manggil `socket()` dengan *family* yang sesuai — `AF_KEY` buat *trigger* `esp4`/`esp6`, atau `AF_RXRPC` buat `rxrpc`. Artinya, siapapun *user* biasa di server itu, tanpa hak `root` sekalipun, bisa manggil modul itu sendiri cuma dengan bikin *socket*. Nggak perlu `modprobe`, nggak perlu izin *admin*."

Devan diam sejenak, mencerna. Ini yang bikin *Dirty Frag* beda dari *bug* biasa. Bukan cuma soal ada *lubang* di kode kernel. Tapi *lubang* itu ada di jalur yang bisa dipicu langsung sama *user* paling rendah sekalipun di sistem.

"Kak, ini mirip kayak *Dirty Pipe* dulu ya?" tanya Devan, inget dia pernah baca soal itu waktu kuliah.

"Mirip di *root cause class*-nya, beda di jalur masuknya," jelas Kak Myesha. "*Dirty Pipe*, ditemuin Max Kellermann tahun 2022, itu soal *flag* yang salah di struktur *pipe buffer* — bikin data yang harusnya cuma bisa dibaca, malah bisa ditimpa lewat trik `splice()`. Tahun 2025 muncul *Copy Fail*, varian baru lewat modul `algif_aead`, pola bugnya serupa: proses *page cache* nggak ngecek ulang izin tulis sebelum data ke-*commit* ke *disk*. Nah, *Dirty Frag* ini generasi ketiga dari keluarga *bug class* yang sama, cuma jalurnya lewat *fragmentasi* paket jaringan di `esp4`/`esp6`, digabung sama *bug* kedua di `rxrpc` yang bikin rantainya jadi *reliable* dan bisa nembus mitigasi yang udah dipasang buat *Copy Fail*."

"Jadi... intinya kernel salah nyimpen *reference* ke halaman memori yang seharusnya *read-only*, terus ngizinin ditulis ulang?" tanya Devan, mencoba menyederhanakan.

"Persis," jawab Kak Myesha. "Bayangin *page cache* itu kayak rak buku bersama. Setiap file yang dibaca sistem, halamannya disimpan di rak itu biar nggak perlu baca ulang dari *disk* tiap kali. Normalnya, kalau kamu cuma punya izin baca ke sebuah buku, kamu nggak boleh corat-coret halamannya. Bug di `esp4`/`esp6` bikin proses *reassembly* paket ESP yang terfragmentasi salah nandain sebuah halaman di rak itu sebagai 'boleh ditulis', padahal harusnya nggak. Bug di `rxrpc` nambahin cara buat *attacker* dapetin *reference* ke halaman spesifik yang dia mau, termasuk halaman milik file `root` kayak `/etc/passwd` atau *binary* `SUID`. Gabungan dua bug ini bikin *user* biasa bisa nulis apa aja ke file yang seharusnya cuma bisa dia baca."

Devan merinding. Kalau penjelasan itu benar, dan kalau server *client* mereka rentan, siapapun yang punya akun *shell* biasa di server itu — bahkan akun *service* yang paling terbatas sekalipun — bisa jadi `root` dalam hitungan detik.

"Oke," ketik Devan, jarinya makin cepat. "Aku lanjut cek prasyaratnya."


## Bab 3: Prasyarat yang Terkabul dan Detak Jantung yang Berpacu

Devan tau, sebuah *bug* di kernel nggak otomatis jadi *exploitable* kalau prasyaratnya nggak terpenuhi. Dia buka lagi *writeup* yang dikirim Jovian, nyari bagian "Requirements". Ada dua hal yang disebut: modul harus tersedia sebagai *loadable module* (sudah dikonfirmasi tadi), dan *user namespace* tanpa hak istimewa harus diizinkan.

```bash
grep -E 'CONFIG_XFRM_ESP|CONFIG_AF_RXRPC' /boot/config-$(uname -r)
sysctl kernel.unprivileged_userns_clone 2>/dev/null
sysctl user.max_user_namespaces 2>/dev/null
```

Hasilnya nongol satu per satu, dan tiap baris terasa kayak detak jam yang makin cepat.

```text
CONFIG_XFRM_ESP=m
CONFIG_AF_RXRPC=m
kernel.unprivileged_userns_clone = 1
user.max_user_namespaces = 63846
```

"Kak, Jov, semua kotak dicentang," ketik Devan, suaranya di dalam kepala udah kayak alarm kebakaran. "`=m` buat dua-duanya, artinya modul tersedia. `unprivileged_userns_clone` diset `1`. Ini standar *default* di Ubuntu buat dukung *container* kayak Docker tanpa `root`, tapi ini juga persis prasyarat yang dibutuhin *exploit*-nya."

"Itu maksudnya apa buat *attacker*, Bang?" tanya Jovian dari Takengon, suaranya sedikit gemetar karena sinyal yang naik-turun.

"Itu artinya," jawab Devan pelan, "*attacker* nggak butuh akses `root` buat mulai. Dia cukup punya *shell* biasa — bisa lewat akun *low-privilege* yang kebobol dari aplikasi web, bisa lewat *reverse shell* dari *vulnerability* lain yang lebih kecil. Begitu dia punya *shell* itu, dia bisa bikin *user namespace* sendiri, yang di dalamnya dia 'serasa' jadi `root`. Dari situ, dia bisa manggil `socket(AF_KEY, ...)` buat mancing `esp4`/`esp6` ke-*load*, sama `socket(AF_RXRPC, ...)` buat `rxrpc`. Dua-duanya jalan tanpa perlu hak `root` beneran, karena dia lagi 'main' di dalam *namespace*-nya sendiri."

Kak Myesha nambahin, "Dan di Ubuntu, kombinasi ini justru bikin server jadi target yang empuk banget. Banyak *distro* lain mematikan `unprivileged_userns_clone` demi keamanan, tapi Ubuntu ninggalin *default*-nya nyala demi kompatibilitas *container tooling*. Itu sebabnya banyak *writeup* soal *Dirty Frag* nyebut Ubuntu sebagai *platform* paling rentan buat rantai ini."

Devan ngerasa keringat dingin ngalir di punggungnya. Sambil dia ngetik, dia buka *tab* lain, ngecek `log auth` server, ngeliat siapa aja yang lagi *login*. Nggak ada yang aneh — untuk sekarang. Tapi dia tau, itu cuma soal waktu sebelum *scanner* otomatis yang tadi malem dibicarain Jovian sampai ke alamat IP server mereka.

"Aku lanjut cek apakah *fix*-nya udah masuk lewat *backport* Ubuntu," ketik Devan. "Ini bagian paling penting. Kalau udah ada, kita cuma perlu pastikan versinya cocok. Kalau belum, kita harus mitigasi manual sekarang juga."

Dia buka terminal lagi, jantungnya berdegup kayak lagi lari maraton.


## Bab 4: Berburu Bukti di Changelog dan Angka yang Tidak Berbohong

Devan tau satu hal penting dari pengalaman-pengalaman sebelumnya: jangan pernah percaya *cache* lokal. *Package* `linux-image` di Ubuntu suka nyimpen dokumentasi *changelog* yang udah lama nggak diperbarui, atau cuma nyimpen *changelog* dari *paket* `linux-signed` yang isinya cuma soal *repackaging*, bukan detail *security patch* yang sebenarnya. Sumber yang benar cuma satu: server resmi `changelogs.ubuntu.com`.

```bash
timeout 25 curl -s "https://changelogs.ubuntu.com/changelogs/pool/main/l/linux/linux_$(dpkg-query -W -f='${Version}' linux-image-$(uname -r) | sed 's/^[0-9.]*-//')/changelog" > /tmp/cl.txt
grep -n 'CVE-2026-43284\|CVE-2026-43500' /tmp/cl.txt
```

Layar terminal diem sejenak, *loading*. Devan nahan napas. Lalu, dua baris muncul.

```text
142:    * SAUCE: xfrm: esp4/esp6: fix out-of-bounds write during fragment
        reassembly (CVE-2026-43284)
298:    * SAUCE: rxrpc: fix use-after-free leading to arbitrary page
        reference (CVE-2026-43500)
```

"Ketemu, Kak! Dua-duanya disebut di *changelog*!" ketik Devan cepat. "Tapi aku belum tau ini masuk di *build* mana persisnya."

"Bagus, itu artinya *fix*-nya udah pernah di-*backport*," balas Kak Myesha. "Sekarang kamu harus tau *build* nomor berapa yang pertama kali nyebut *fix* itu, terus bandingin sama *build* yang lagi jalan sekarang."

Devan nulis satu baris `awk` buat nyari *build number* yang pertama kali nyebut tiap CVE.

```bash
awk '/^linux \(7\.0\.0-/ {v=$0} /CVE-2026-43284/ {print "fix CVE-2026-43284 masuk di: " v}' /tmp/cl.txt
awk '/^linux \(7\.0\.0-/ {v=$0} /CVE-2026-43500/ {print "fix CVE-2026-43500 masuk di: " v}' /tmp/cl.txt
```

```text
fix CVE-2026-43284 masuk di: linux (7.0.0-26.26) noble; urgency=medium
fix CVE-2026-43500 masuk di: linux (7.0.0-26.26) noble; urgency=medium
```

Kedua *fix* itu masuk di *build* `7.0.0-26.26`. Devan langsung bandingin dengan versi yang lagi jalan di server.

```bash
dpkg-query -W -f='${Version}\n' linux-image-$(uname -r)
```

```text
7.0.0-30.30
```

Devan menatap layar itu lama. Angka `30.30` lebih besar dari `26.26`. Dia hitung ulang tiga kali, takut salah baca di tengah tekanan.

"Kak... Jov..." ketiknya pelan, hampir nggak percaya. "Kernel yang lagi jalan itu `7.0.0-30.30`. *Fix*-nya masuk di `7.0.0-26.26`. Itu artinya... server kita udah bawa *patch*-nya. Kita **aman**."

Ada jeda beberapa detik di grup, sebelum Jovian ngetik balasan penuh kelegaan. *"ASTAGA. Aku kira kita bakal begadang nge-patch darurat tengah malem gini. Alhamdulillah."*

Tapi Kak Myesha, dengan gaya khasnya yang selalu skeptis sebelum yakin seratus persen, ngetik balasan yang bikin Devan langsung tegang lagi. "Jangan lega dulu. Itu baru satu server. Berapa banyak *server* lain yang kamu pegang buat *client* ini? Kamu pernah cek semuanya, atau cuma yang ini?"

Devan kebekap. Dia baru sadar, mereka nggak cuma punya satu *server*. Ada empat *server* lain, dua di antaranya *server staging* yang jarang disentuh, dan dua lagi *server backup* yang kadang nggak dapat *patch* rutin karena dianggap "nggak penting". Detak jantungnya kembali cepat.

"Aku cek satu-satu sekarang," ketiknya, keringat mulai netes lagi.


## Bab 5: Empat Pintu, Satu yang Terbuka Lebar

Devan buka *terminal multiplexer*-nya, bikin empat *pane* buat *SSH* ke empat *server* sekaligus. Server pertama dan kedua, hasilnya sama kayak yang pertama tadi: versi `7.0.0-30.30`, aman. Server ketiga, *staging*, sama juga.

Tapi *pane* keempat — *server backup* yang jarang disentuh — nunjukin sesuatu yang bikin dia berdiri dari kursi.

```text
$ dpkg-query -W -f='${Version}\n' linux-image-$(uname -r)
7.0.0-24.24
```

`7.0.0-24.24`. Lebih kecil dari `7.0.0-26.26`, *build* tempat *fix* itu masuk. Server ini nggak pernah dapat pembaruan sejak tiga bulan lalu.

"KETEMU!" ketik Devan panik. "Server *backup*-nya. Versi `24.24`. Itu di bawah `26.26`. Server ini **rentan**!"

Dia langsung ngulang Step 2 dan Step 3 di server itu. Modul `esp4`, `esp6`, `rxrpc` semuanya tersedia sebagai *module*. `unprivileged_userns_clone` juga diset `1`. Semua syarat *Dirty Frag* terpenuhi, penuh, sempurna, tanpa halangan.

Yang bikin makin ngeri, server *backup* ini bukan sekadar *server* mati suri. Server ini masih jalan sebagai *replica database* buat *disaster recovery*, dan yang lebih parah, server ini punya beberapa akun *developer* lama — termasuk mantan *kontraktor* yang kontraknya udah habis enam bulan lalu, tapi akunnya belum sempat dihapus karena dianggap "nggak kritis".

"Kak Myesha, ini bahaya banget," ketik Devan, jarinya gemeteran hebat sekarang. "Server ini punya akun-akun lama yang seharusnya udah nggak aktif. Kalau salah satu dari akun itu, atau siapapun yang berhasil nyusup lewat *credential* bocor, dapet *shell* biasa di sini... dia bisa langsung jadi `root` pakai *Dirty Frag*. Dan dari `root` di server *backup*, dia punya akses penuh ke *database replica*, yang isinya sama persis kayak data *production*."

"Ini yang aku takutin dari awal," balas Kak Myesha, nada suaranya berubah serius total, nggak ada lagi canda. "Server yang dianggep 'nggak penting' justru sering jadi *jalan belakang* yang paling gampang ditembus, karena semua orang lupa ngawasinnya. Sekarang, jangan buang waktu buat analisis lebih jauh. Langsung eksekusi mitigasi. SEKARANG."

Devan cek log *auth* di server itu sekali lagi, dan matanya membelalak. Ada percobaan *login SSH* gagal dari alamat IP asing, berulang-ulang, dalam pola yang khas *bruteforce* otomatis, dimulai sekitar dua jam yang lalu — persis nggak lama setelah *thread* di forum yang dibaca Jovian mulai ramai. Entah kebetulan, entah memang server mereka udah masuk daftar target *scanner*, tapi satu hal jelas: mereka nggak punya waktu lagi buat berdebat.


## Bab 6: Menutup Pintu Sebelum Sang Tamu Tak Diundang Tiba

Devan langsung buka *writeup* mitigasi resmi dari peneliti yang nemuin *bug* ini. Mitigasinya sederhana secara konsep: putus jalur masuknya. Kalau modul `esp4`, `esp6`, dan `rxrpc` nggak bisa dimuat sama sekali, rantai *exploit*-nya nggak punya jalan buat jalan, apapun *bug*-nya.

```bash
sh -c "printf 'install esp4 /bin/false\ninstall esp6 /bin/false\ninstall rxrpc /bin/false\n' > /etc/modprobe.d/dirtyfrag.conf; rmmod esp4 esp6 rxrpc 2>/dev/null; echo 3 > /proc/sys/vm/drop_caches; true"
```

Perintah itu ngelakuin tiga hal sekaligus: nulis aturan `install <modul> /bin/false` yang bikin sistem nolak muatin modul itu meskipun ada *proses* yang manggil `socket()` yang biasanya bikin modul itu *auto-load*; ngehapus modul yang mungkin udah kepalang termuat; dan ngebersihin *page cache* biar nggak ada sisa *state* mencurigakan yang nyangkut.

Devan tekan *Enter*. Jantungnya berdebar kayak dia lagi nunggu bom dijinakkan.

```text
rmmod: ERROR: Module esp4 is not currently loaded
rmmod: ERROR: Module esp6 is not currently loaded
rmmod: ERROR: Module rxrpc is not currently loaded
```

Wajar, karena tadi memang belum ada yang manggil ketiga modul itu. Tapi yang penting, sekarang `/etc/modprobe.d/dirtyfrag.conf` udah aktif. Devan verifikasi sekali lagi dengan nyoba manggil *socket* jenis itu dari akun biasa.

```bash
python3 -c "import socket; socket.socket(socket.AF_KEY, socket.SOCK_RAW, 2)"
```

```text
PermissionError: [Errno 1] Operation not permitted
```

Modulnya nggak bisa dimuat lagi. Jalur masuknya tertutup. Devan menghembuskan napas panjang yang udah dia tahan entah berapa lama.

"Mitigasi udah aktif di server *backup*," ketiknya ke grup. "Jalur *auto-load* buat ketiga modul udah diputus. Sekarang aku mau langsung *upgrade* paket kernelnya biar dapet *fix* permanen, bukan cuma mitigasi sementara."

```bash
ls /boot/vmlinuz-*
sudo apt update && sudo apt install --only-upgrade linux-image-generic linux-headers-generic -y
sudo reboot
```

Server itu *restart*, dan lima menit yang terasa kayak lima jam kemudian, Devan bisa *SSH* lagi. Dia ngulang Step 1 buat konfirmasi.

```bash
uname -a
dpkg-query -W -f='${Version}\n' linux-image-$(uname -r)
```

```text
Linux prod-backup-01 7.0.0-31-generic #31-Ubuntu SMP x86_64 GNU/Linux
7.0.0-31.31
```

`7.0.0-31.31`. Jauh di atas `7.0.0-26.26`, *build* tempat *fix* resmi masuk. Server itu sekarang bener-bener aman, bukan cuma dimitigasi sementara.

Jam nunjukin pukul 02:47 dini hari. Di Takengon, Jovian udah nyaris ketiduran sambil mantengin *log* server dari *laptop*-nya yang baterainya tinggal 12 persen. Di Berbah, Kak Myesha masih terjaga, sesekali ngecek *dashboard monitoring* dari jauh buat mastiin nggak ada anomali baru. Dan di Sleman, Devan bersandar lemas di kursinya, menatap terminal yang sekarang menampilkan angka-angka yang tenang dan konsisten.

"Makasih ya, Kak, Jov," ketik Devan. "Kalau Jovian nggak nemu *thread* itu semalem, atau kalau Kak Myesha nggak maksa aku cek semua server, mungkin kita baru sadar server *backup* itu kena pas udah kebobol beneran."

"Justru itu pelajarannya, Devan," balas Kak Myesha. "*Vulnerability* paling berbahaya itu bukan yang ada di server yang paling sering kamu liat. Tapi yang ada di server yang kamu lupain. Mulai sekarang, semua server — termasuk yang *backup*, yang *staging*, yang keliatannya 'nggak penting' — harus masuk daftar *patch* rutin yang sama. Dan setiap kali ada CVE baru yang nyebut *kernel module*, jangan cuma cek satu server yang paling gampang diakses. Cek semuanya, satu per satu, tanpa kecuali."

"Siap, Kak," jawab Devan, sambil nutup semua *pane* terminal-nya satu per satu, memastikan tiap server udah dalam kondisi aman sebelum dia akhirnya bisa tidur.

Di luar sana, *scanner* otomatis yang malam itu ikut menyisir alamat IP mereka pindah ke target lain, mencari pintu lain yang masih terbuka. Tapi untuk server-server mereka, malam itu, semua pintu sudah dikunci rapat sebelum sang tamu tak diundang sempat mengetuk.


## Referensi

- [V4bel/dirtyfrag](https://github.com/V4bel/dirtyfrag) — *writeup* resmi peneliti, *proof-of-concept*, dan tabel versi terdampak.
- [Patch mainline xfrm-ESP (CVE-2026-43284)](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=f4c50a4034e62ab75f1d5cdd191dd5f9c77fdff4)
- [Patch mainline RxRPC (CVE-2026-43500)](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=aa54b1d27fe0c2b78e664a34fd0fdf7cd1960d71)
- [Ubuntu Security CVE tracker](https://ubuntu.com/security/CVE-2026-43284)
- [Dirty Pipe](https://dirtypipe.cm4all.com/) — nenek moyang *bug class* ini (Max Kellermann, 2022).
- [Copy Fail](https://copy.fail/) — varian pendahulu di 2025, mitigasinya tidak menutup jalur *Dirty Frag*.
