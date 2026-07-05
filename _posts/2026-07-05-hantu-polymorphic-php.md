---
layout: post
title: "Mimpi Buruk Legacy Code: Ketika PHP Bermutasi Sendiri dan Bikin Server Jebol"
subtitle: "Kisah menegangkan saat aku, Kak Myesha, dan Jovian berhadapan dengan hantu polymorphic code yang menghancurkan production."
date: 2026-07-05 14:05:00 +0700
categories: [Engineering, Security, Story]
tags: [PHP, Polymorphic Code, Malware, Security, Legacy Code]
---

# Bab 1: Alarm Merah dari Pesisir Krui

Angin malam di Yogyakarta terasa lebih dingin dari biasanya. Di kamarku yang cuma diterangi lampu RGB dari balik monitor, aku (Devan) lagi sibuk ngerapihin *legacy code* PHP dari sebuah *client* agensi pemerintahan. Proyek ini baru aja di-handover ke aku sebulan yang lalu. Kode yang umurnya udah hampir satu dekade, minim dokumentasi, dan ditulis pakai gaya yang bikin *software engineer* zaman *now* pasti pengen nangis darah. 

Jam di sudut layar nunjukin pukul 21:00 WIB. Rencananya aku cuma mau *monitoring* santai sambil dengerin musik *lo-fi*. Tapi ketenangan itu hancur berantakan pas notifikasi Telegram-ku meledak dengan suara *ringtone* darurat. 

Itu dari Jovian, adik bungsuku. Anak *Data & DevOps* yang entah gimana ceritanya lagi dapet izin kerja *remote* dari pinggir pantai di Krui, Pesisir Barat Lampung. Sinyal di sana kadang kembang kempis, tapi malam ini suara panggilan *Voice Call* Telegram-nya jernih banget, dan nada suaranya penuh kepanikan.

"Bang Dev! Abang lagi buka server *client* yang pemerintahan itu nggak?!" suara Adik terdengar ngos-ngosan, seolah dia baru aja lari dari kejaran ombak Krui.

"Lagi buka, Jov. Kenapa emangnya? *Traffic* aman kok, *CPU usage* juga masih anteng di bawah 20 persen," jawabku santai sambil nyeruput es kopi susu yang es batunya udah mencair semua.

"Bukan *resource*-nya, Bang! Abang cek *dashboard* FIM (File Integrity Monitoring) di Wazuh sekarang! Server kita lagi diserang. File `index.php` di *root directory* berubah-ubah terus!" 

Aku langsung tersedak. Kopi susuku nyaris nyembur ke *keyboard* mekanikal kesayangan. FIM adalah sistem keamanan yang tugasnya mantau kalau ada perubahan file di *server*. Kalau file `index.php` berubah di *production* tanpa ada *pipeline deployment* yang jalan, itu cuma berarti satu hal: server di-hack, dan ada *malware* yang lagi nyuntikin kode jahat.

Dengan tangan gemeteran, aku buka *dashboard* keamanan. Benar aja, layar penuh dengan log merah.

```text
[ALERT] File integrity modification detected!
Path: /var/www/html/index.php
Old MD5: 3b4a5d7c...
New MD5: 9f8e2a1b...
Timestamp: 21:02:14
```

Detik berikutnya, muncul *alert* baru. MD5 *hash*-nya berubah lagi. Lima detik kemudian, berubah lagi. 

"Gila... file-nya berubah tiap ada *request* masuk, Jov!" kataku dengan suara bergetar. "Setiap kali ada *user* yang buka web, MD5 *hash* file `index.php` berubah. Ini *malware* jenis apa anjir? Kok bisa *real-time* gini?!"

"Aku nggak tau, Bang. Abang kan yang pegang *backend*-nya! Buruan matiin *web server*-nya sebelum *database* di-dump sama *hacker*-nya!" teriak Jovian dari ujung telepon. Suara deburan ombak Krui di latar belakangnya malah bikin suasana makin horor. Malam itu, aku merasa kayak lagi ada di film *thriller cyber-security*.


# Bab 2: Jejak Hantu Polymorphic di Dalam File PHP

Aku nggak berani langsung matiin server karena ini web pelayanan publik yang lagi ada *campaign* pendaftaran *online*. Kalau aku *take down* sekarang tanpa bukti kuat, aku bisa kena denda penalti kontrak. Aku harus investigasi dulu.

Aku langsung buka terminal, SSH ke dalam server *production*, dan masuk ke direktori web. 

"Oke, Jov. Aku coba *download* dua versi dari file `index.php` di detik yang berbeda. Kita lihat apa yang di-inject sama *hacker*-nya," kataku mencoba tenang, padahal jantungku udah berdegup kencang.

Aku jalanin *command* di Linux untuk ngopi file-nya:

```bash
cp index.php index_v1.php
sleep 2
curl http://localhost/ > /dev/null
cp index.php index_v2.php
```

Setelah itu, aku ngejalanin perintah `diff` untuk ngeliat perbedaan antara kedua file tersebut. Apa yang muncul di layarku bikin dahiku berkerut keras. Aku kira aku bakal ngeliat kode `eval(base64_decode(...))` khas *malware* PHP, tapi ternyata beda jauh.

```diff
--- index_v1.php
+++ index_v2.php
@@ -140,5 +140,5 @@
 
 // POLYMORPHIC REGION
-/* poly:7a9f8e2b1c4d... */
-if (false) { /* junk:8f7e6d... */ }
+/* poly:1b2c3d4e5f6a... */
+if (false) { /* junk:2a3b4c... */ }
```

"Jov, kamu masih di sana?" tanyaku.

"Masih, Bang. Gimana? Ada *backdoor*?"

"Enggak ada *backdoor*. Logika kodenya sama sekali nggak berubah. Cuma ada sepotong kode aneh di paling bawah file. Kodenya masukin *comment* acak dan blok `if (false)` yang isinya *string hexadecimal* *random*. Ini apaan coba?"

Aku buka file `index.php` pakai Vim dan *scroll* sampai ke bagian terbawah. Di sanalah aku nemuin sebuah fungsi yang namanya bikin bulu kudukku berdiri: `mutate_self()`.

```php
<?php
// ... [Kode aplikasi utama klien di sini] ...

function generate_dead_code() {
    $nonce = bin2hex(random_bytes(8));
    // Dead code that never executes
    return "if (false) { /* junk:" . $nonce . " */ }\n";
}

function mutate_self() {
    $path = __FILE__;
    $code = file_get_contents($path);

    $marker = "/*POLY_MARKER*/";

    $pos = strpos($code, $marker);
    if ($pos === false) {
        return;
    }

    // Random comment + dead code block
    $randomComment = "/* poly:" . bin2hex(random_bytes(16)) . " */\n";
    $deadCode      = generate_dead_code();

    $replacement = $randomComment . $deadCode;

    // Mereplace marker lama dengan junk code baru, ditambah marker untuk next run
    $code = substr_replace($code, $replacement . $marker, $pos, strlen($marker));
    
    // MENYIMPAN KEMBALI KE FILE ITU SENDIRI
    file_put_contents($path, $code);
}

mutate_self();

// POLYMORPHIC REGION
/*POLY_MARKER*/
```

Otakku berusaha memproses apa yang baru aja aku baca. File PHP ini membaca *source code*-nya sendiri pakai `file_get_contents(__FILE__)`, nyari *string* penanda `/*POLY_MARKER*/`, menggantinya dengan komentar acak dan *dead code* (kode sampah yang nggak pernah dieksekusi), lalu menimpakan kembali kode tersebut ke file di *hardisk* pakai `file_put_contents()`.

"Jov... file ini nggak di-hack dari luar," ujarku pelan. "File ini bermutasi dengan sendirinya. Setiap kali diakses, dia mengubah struktur kodenya sendiri biar MD5 *hash*-nya berubah, tapi kelakuannya tetep sama."

"Bang, seriusan? Bukannya itu definisi dari *Polymorphic Malware*?!" seru Jovian. "Dulu aku pernah baca di jurnal kampus. *Polymorphic code* itu teknik yang dipakai sama virus kayak Storm Worm atau *ransomware* biar lolos dari *scanning Antivirus* yang pakai metode *signature-based*!"

Benar kata Adik. Teknik ini memang sering banget diasosiasikan dengan *malware*. Tapi pertanyaannya, kenapa *developer* sebelumnya naruh kode gila kayak gini di *framework* pelayanan publik?! Sebelum aku sempat mikir lebih jauh, tragedi yang sesungguhnya akhirnya terjadi.


# Bab 3: Tragedi Fatal di Puncak Jam Sibuk

Tepat pukul 21:30 WIB, *campaign* pendaftaran publik dari pihak kementerian disebar lewat *broadcast* WhatsApp ke ribuan warga. Dalam hitungan detik, *traffic* yang tadinya tenang, mendadak meledak. Jumlah *request* per detik (RPS) naik dari 5 menjadi 500.

Aku lagi sibuk baca fungsi `mutate_self()` ketika tiba-tiba terminal SSH-ku jadi *lag*. 

"Bang Dev! *Error* 500! *Internal Server Error* di semua halaman!" teriak Jovian.

Aku panik. Aku coba muat ulang halamannya di *browser*. Bener aja, layar putih kosong dengan tulisan hitam kecil di pojok kiri atas:

`Parse error: syntax error, unexpected end of file in /var/www/html/index.php on line 412`

"Astaga! Kodenya putus di tengah jalan!" pekikku. Aku buru-buru ngecek isi file `index.php` di server. Dan tebak apa yang terjadi? Ukuran filenya berubah dari 15 KB menjadi cuma 4 KB! Sebagian besar kode intinya hilang, kepotong begitu aja! Aplikasinya lumpuh total.

Grup WhatsApp proyek langsung dihujani pesan dari pihak klien. *Client* panik karena pendaftaran gagal diakses. Aku ngerasa dunia mau runtuh. Gimana caranya file kode bisa kepotong sendiri?!

Aku menatap layar dengan mata nanar, dan detik itu juga logika *Computer Science*-ku jalan. *Race Condition*.

Bayangin, fungsi `mutate_self()` melakukan operasi *Read-Modify-Write* pada file `index.php`. Ketika ada 1 *request*, itu nggak masalah. Tapi ketika ada 500 *request* di milidetik yang sama, ratusan proses PHP mencoba melakukan `file_put_contents()` secara bersamaan ke file yang sama. Nggak ada mekanisme *File Locking* (`flock()`). Akibatnya, ada proses yang belum selesai nulis, tapi proses lain udah nimpa, bikin filenya hancur berantakan dan *corrupt*!

Aku harus ngebenerin ini secepatnya. Aku ambil file *backup* dari *repository* Git lokal di laptopku, lalu nge-upload ulang ke server buat nimpain file yang rusak. Aplikasi hidup lagi. Tapi aku tau, selama fitur mutasi itu masih ada, aplikasinya bakal hancur lagi dalam hitungan menit gara-gara *traffic* yang masih tinggi.

Dalam kondisi mental yang udah setengah *burnout*, aku memutuskan untuk ngelakuin hal yang selalu aku lakuin kalau otak udah *stuck*: nelpon Kak Myesha.


# Bab 4: Panggilan Darurat ke Berbah dan Penjelasan Sang Tech Lead

Aku mendial nomor Kak Myesha lewat Telegram. Kakak perempuanku yang satu ini adalah seorang *Tech Lead* *backend* di salah satu perusahaan *unicorn*. Kebetulan *weekend* ini dia lagi ambil cuti dan pulang kampung ke rumah nenek di daerah Berbah, Sleman, Yogyakarta—nggak terlalu jauh dari kosanku, tapi aku nggak mungkin nyetir ke sana dalam kondisi server lagi berdarah-darah.

"Halo, Dek Devan? Tumben malam-malam nelpon. Ada apa? Server meledak?" sapa Kak Myesha dengan nada santai khas *Tech Lead* yang udah sering makan asam garam *production incident*. Sayup-sayup terdengar suara jangkrik dari pekarangan rumah Berbah.

Aku ceritain semuanya secepat kilat. Mulai dari log MD5 Wazuh yang merah, kode yang mengubah dirinya sendiri, sampai insiden file *corrupt* akibat *race condition*. Jovian juga ikut masuk ke dalam *conference call* buat nambahin detail dari sisi FIM.

Bukannya panik, Kak Myesha malah tertawa pelan. "Ya ampun... aku kira apaan. Itu bukan di-hack, Devan, Jovian. *Developer* sebelum kamu itu lagi nyoba bikin sistem pelindung kode (*code obfuscation*) atau semacam DRM (*Digital Rights Management*) ala kadarnya."

"Hah? DRM gimana maksudnya, Kak?" tanyaku bingung sambil nahan napas, mataku tetap ngawasin log *access* di monitor lain.

Kak Myesha mulai ngejelasin pelan-pelan layaknya ngajar di kelas kampus. "Kalian berdua tau kan konsep *Self-Modifying Code*? Di bahasa yang dikompilasi secara *native*, kode ini mengubah instruksinya sendiri di memori buat optimasi, kayak *Just-In-Time* (JIT) compiler. Tapi di dunia keamanan, teknik ini dipakai sebagai *Polymorphic Code*."

"Iya, Kak! Kayak yang aku bilang ke Bang Dev tadi, itu kan teknik *malware*!" sela Jovian dari Krui.

"Tepat, Adikku pinter," puji Kak Myesha. "*Malware* kayak Storm Worm, CryptoWall, atau Virut pakai mesin mutasi buat mengubah wujud kode mereka di setiap infeksi. Logika jahatnya sama, tapi karena wujudnya berubah—entah itu ditambahin *junk code*, di-*encode* ulang, atau strukturnya diacak—*hash* MD5 atau SHA-nya bakal selalu baru. Antivirus jadul yang cuma nyocokin daftar *hash blacklist* (*signature-based*) nggak bakal bisa nangkap mereka."

"Tapi Kak," potongku, "ini kan aplikasi pemerintahan. Ngapain *developer*-nya masukin teknik *malware* ke mari?!"

"Ini sering kejadian di *legacy software*," desah Kak Myesha. "Agensi lama mungkin pengen melindungi IP (*Intellectual Property*) mereka. Mereka bikin *script* yang seolah-olah 'hidup' dan bermutasi. Tujuannya biar kalau kodenya dibajak atau disalin sama pihak klien tanpa izin, jejak *hash*-nya beda-beda, dan bikin susah orang yang mau *reverse engineering*. Tapi sayangnya, cara mereka nerapin di PHP itu **salah besar**."

"Jelas salah besar! Tadi kodenya hancur gara-gara *race condition* pas `file_put_contents`!" omelku gemas.

"Nah, itu poinnya, Dek," tegas Kak Myesha. "Di PHP, *self-modifying code* di level file itu ide yang sangat, sangat buruk untuk *web development* normal. Pertama, kayak yang kamu alamin, masalah *Concurrency*. Tanpa *lock* yang benar, file bakal *corrupt*. Kedua, *Maintainability*. Gimana caranya kamu nge-*track* kode di Git kalau file-nya berubah tiap detik di server *production*? Ketiga, *Security Flag*. Teknik polimorfik ini terang-terangan bakal bikin alarm keamanan kayak Wazuh atau FIM menjerit-jerit karena kelakuannya identik 100% dengan *malware*."

Penjelasan Kak Myesha bikin pikiranku langsung jernih. Pantas saja semuanya jadi berantakan. Ini murni masalah salah kaprah *engineering*. "Terus solusinya gimana, Kak? Aku apus aja kan fungsi mutasinya?"


# Bab 5: Eksorsisme Kode dan Pelajaran Pahit Sebagai Engineer

"Iya, basmi habis fungsi `mutate_self()` itu," instruksi Kak Myesha tegas. "Kalau klien butuh proteksi IP atau *obfuscation*, pakai *tools obfuscator* PHP sungguhan di fase *build* sebelum di-*deploy*, bukan ngubah kode secara *runtime* pakai PHP *built-in function*. Dan satu lagi, Devan..."

"Apa, Kak?"

"Kenapa *web server* (user `www-data`) punya izin buat nulis alias *write access* ke file `.php`?!" omel Kak Myesha, kali ini nadanya lebih mirip kakak yang lagi marahin adiknya yang ketahuan bolos sekolah. "Secara *security best practice*, *web server* itu cuma boleh punya hak *read-only* ke file *source code*. Dia cuma boleh nulis di *folder* khusus kayak `/storage/` atau `/logs/`. Kalau dari awal *file permission*-nya benar, fungsi `file_put_contents(__FILE__)` itu bakal melempar *error Permission Denied*, dan *source code* kamu nggak bakal hancur!"

Deg. Bener banget. Aku langsung tampar jidatku sendiri. Ini kesalahan *deployment* klasik yang sering terjadi di *server* jadul: semua *file permission* diset `777` atau *ownership*-nya dipegang sepenuhnya sama *web server* demi kepraktisan. 

"I... iya, Kak. File *permission*-nya emang belum sempet aku rapihin sejak di-handover," kataku meringis malu. 

Dengan kecepatan penuh, aku ngelakuin proses eksorsisme atau pembersihan kode. Aku hapus fungsi `mutate_self()`, hapus blok `/*POLY_MARKER*/`, dan nyimpen kode intinya aja yang murni dan bersih. 

Lalu, di terminal Linux, aku benerin struktur keamanannya.

```bash
# Mengembalikan ownership ke user deployer, bukan web-server
sudo chown -R devan:www-data /var/www/html/

# Set permission: Folder 755, File 644 (Web server cuma bisa read)
sudo find /var/www/html -type d -exec chmod 755 {} \;
sudo find /var/www/html -type f -exec chmod 644 {} \;
```

Setelah kode bersih di-*deploy* dan *permission* diamankan, aku ngetik perintah untuk ngerestart layanan PHP-FPM.

"Oke, *deployed*," gumamku sambil menghembuskan napas yang terasa berat banget.

Di Pesisir Barat sana, Jovian memantau *dashboard*. "Bang Dev... log FIM di Wazuh udah hijau semua. Nggak ada lagi peringatan perubahan MD5. CPU juga anteng. Angka pendaftaran masuk lancar."

Aku bersandar lemas di kursi. Jam udah nunjukin pukul 23:15 WIB. Insiden mematikan yang cuma berlangsung sekitar 45 menit itu rasanya nguras energi setara dengan *coding* seharian penuh.

"Makasih banyak ya, Kak Myesha. Kalau Kakak nggak jelasin soal *polymorphic code* buat *obfuscation*, mungkin aku bakal mikir servernya beneran kena *malware* dan ngambil keputusan gegabah buat *wipe* ulang OS-nya," ucapku tulus.

"Sama-sama, Abang Devan. Besok-besok, kalau nanganin *legacy code*, jangan cuma diliatin fitur bisnisnya aja. *Review* juga hal-hal aneh di ujung-ujung file. Dan ingat *golden rule* kita: Jangan biarin kode bermutasi sendiri di *production* kecuali kamu lagi bikin *compiler* atau nulis *malware*," kata Kak Myesha sambil terkekeh. "Udah sana pada tidur. Jovian, jangan begadang di pinggir pantai ntar masuk angin!"

"Siap, Kakak!" jawab Jovian riang.

Panggilan pun ditutup. Di tengah malam Sleman yang sunyi, aku natep barisan kode yang sekarang udah diam tak bergerak. MD5 *hash*-nya tetap statis, kokoh, dan konsisten. Tragedi hantu *polymorphic* PHP ini akhirnya selesai. Pelajaran penting buat kita semua: sepintar apapun kita nyari jalan pintas buat ngelindungin kode, jangan sampai sistem yang kita buat itu justru jadi bom waktu yang bakal meledak di muka kita sendiri saat jam sibuk.

Dan satu lagi... *set file permission* server-mu dengan benar, demi Tuhan!
