---
layout: post
title: "Neraka Satu Sen: Ketika PHP Gagal Menghitung 0.1 + 0.2 dan Dana Petani Kopi Gayo Nyaris Tercecer"
subtitle: "Kisah satu malam panik aku, Jovian, dan Kak Myesha memburu float sinting, intval yang licik, dan ID raksasa yang menguap jadi kabut."
date: 2026-09-11 21:15:00 +0700
categories: [Engineering, Story]
tags: [PHP, Floating Point, IEEE 754, BCMath, GMP, Backend]
---

## Bab 1: Selisih Sepele yang Berbau Kopi Gayo

Malam itu gerimis turun rintik-rintik di Sleman. Aku, Devan, duduk di depan laptop dengan secangkir kopi Gayo seduhan yang kebetulan masih ada stoknya—hadiah dari klien kami. Jam di pojok layar nunjukin pukul 23:47 WIB. Tiga belas menit lagi, *batch settlement* harian bakal jalan, dan tugasnya cuma satu: memindahkan dana hasil penjualan klien kami ke rekening mereka, rapi, utuh, tanpa kurang setiap sen pun.

Klien yang aku maksud bukan sembarang klien. Namanya Kooperatif Kete Gayo Sejahtera, gabungan petani kopi di Takengon, Aceh Tengah. Mereka menjual biji kopi hijau ke *roastery* di Eropa, pembayarannya masuk lewat *payment gateway* dalam dolar, lalu platform tempat aku kerja yang mengurus konversi, potongan biaya, dan pencairan ke rekening koperasi. Setiap tanggal 11, dana petani wajib cair. Tanggal, bukan pilihan.

Aku pernah ke Takengon sekali pas *onboarding* proyek ini. Aku masih ingat wajah Bu Rai, pengurus koperasi yang menyeduh kopi di dapurnya sambil bilang, "Uang ini, Dik, bukan uang perusahaan. Ini uang sekolah anak-anak petani." Sejak hari itu, aku tidak pernah berani menganggap *settlement* ini pekerjaan rutin yang membosankan.

Tepat pukul 00:00 WIB, *batch settlement* berjalan. Aku menyeruput kopi, santai, nggak curiga apa-apa. Dua menit kemudian, layarku berubah warna. Bukan merah *error*—justru itu yang bikin merinding. Dashboard *reconciliation* hijau semua, *batch* sukses, tidak ada *exception* di log. Tapi di panel kanan, ada satu angka yang melawan semua kehijauan itu:

```text
Settlement Batch #20260911  ............  SUCCESS
Transactions processed ................ 14.206
Manual review queue ................... 3.412  ( spike +3.398 )
Reconciliation gap .................... -$184.06
```

Tiga ribu empat ratus dua belas transaksi tiba-tiba masuk *antrian review manual*. Dan yang lebih parah: selisih rekonsiliasi minus seratus delapan puluh empat dolar enam sen. Uang yang hilang itu bukan uang platform. Itu uang petani.

Notifikasi Slack meledak.

**[00:04] Sinta (CS):** "Mas Devan, checker-nya kok nandain ribuan transaksi jadi anomali? Ada merchant telepon, katanya dana koperasi mereka kok berkurang."

Aku belum sempat bales, *incoming call* masuk. Jovian, adik bungsuku, anak *Data & DevOps* yang lagi kerja *remote* di Krui, Pesisir Barat Lampung—kampung halaman ibu kami. Di latar belakangnya kedengeran deburan ombak.

"Bang Dev! Aku liat Grafana, *queue* review manual meledak dari nol ke tiga ribuan dalam satu *batch*!" suaranya ngos-ngosan. "Abang pegang apa tadi malam? *Deploy* nggak?"

"Nggak ada *deploy*, Jov. Kode nggak tersentuh, *config* nggak tersentuh," jawabku. Suaraku sendiri mulai bergetar. "Dan itu yang bikin aku takut. Nggak ada yang berubah, tapi angkanya berubah."

Aku tatap layar yang bermandikan angka hijau—angka-angka yang seharusnya jadi bagian paling jujur dari sistem komputer. Semua *status* sukses, semua log normal, tapi dana petani kurang $184.06. Malam itu aku sadar, musuh kami bukan *hacker*, bukan *downtime*, bukan *traffic*. Musuh kami malam itu adalah matematika.

## Bab 2: Ketika 0.1 + 0.2 Menolak Menjadi 0.3

Aku mulai bedah *queue* anomali. Kalau ada tiga ribu transaksi ditandai, pasti ada pola. Aku *group* berdasarkan tipe transaksi, dan polanya langsung kelihatan: hampir semuanya transaksi *bundle* promo—paket mini sachet kopi 10 gram plus stik gula aren yang dijual roastery Eropa sebagai sampel. Harga sachetnya $0.10, gula arennya $0.20, dan *bundle*-nya dijual $0.30.

Aku buka file `ReconciliationGuard.php`, *service* yang tugasnya mastiin jumlah komponen sama dengan total yang dikirim gateway. Ini potongannya:

```php
<?php
// ReconciliationGuard.php — Pemeriksa invariant settlement

$bundleTotal = (float) $gatewayPayload['total'];   // gateway kirim string "0.30"
$partsTotal  = $itemSachet->price + $itemAren->price; // 0.10 + 0.20

if ($partsTotal === $bundleTotal) {
    $status = 'CLEAN';
} else {
    $status = 'ANOMALY';
    // masuk antrian review manual
}
```

Jedag. Di situ letak masalahnya. Aku buka terminal dan jalankan reproduksi sekejap pakai `php -r`:

```php
var_dump(0.1 + 0.2 === 0.3);
// bool(false)
```

`false`. Perhitungan paling dasar yang diajarkan SD, ditolak mentah-mentah oleh PHP. Aku tahu kasus ini—ini bahkan contoh *quiz* buat *junior developer*—tapi melihatnya menyandera ribuan transaksi berisi dana petani itu rasa yang lain.

"Bang, itu kan klasik banget, *floating point*," kata Jovian lewat telepon, nyaris menguap. "IEEE 754 kan, Abang udah tau."

"Iya, Jov, tapi dengarin aku dulu," jawabku. "Tau teorinya itu satu hal. Liat teori itu nyandera duit orang lain itu hal yang beda. Dan ini baru lapisan pertama."

Aku jelaskan pelan-pelan, sekaligus buat diriku sendiri biar logikanya nyambung. Tipe `float` di PHP itu *platform-dependent*, tapi hampir selalu memakai format **IEEE 754 binary64**: ada satu *bit* tanda, ada *exponent*, dan ada 53 *bit* presisi biner. Manual PHP menyebut hasil praktisnya sekitar 14 digit desimal presisi, dengan *maximum relative rounding error* orde `1.11e-16`. Kata kuncinya satu: **biner**.

Float itu menyimpan jumlah hingga dari pangkat dua. Pecahan seperti `0.5` (sama dengan 1/2) atau `0.125` (1/8) punya representasi biner berhingga, jadi bisa disimpan **eksak**. Tapi `0.1` (1/10) tidak. Representasi binernya mengulang diri selamanya—persis seperti `1/3` yang di desimal jadi `0.3333333...` tanpa ujung. Karena nggak mungkin disimpan utuh, PHP menyimpan nilai biner *terdekat* yang bisa direpresentasikan.

Kita bisa bikin aproksimasi itu kelihatan dengan mencetak cukup banyak digit:

```php
printf("%.17g\n", 0.1);       // 0.10000000000000001
printf("%.17g\n", 0.2);       // 0.20000000000000001
printf("%.17g\n", 0.1 + 0.2); // 0.30000000000000004
```

Di situ terlihat `0.1` yang tersimpan sebenarnya sedikit *lebih besar* dari sepersepuluh, `0.2` juga sedikit lebih besar, dan jumlah keduanya mendarat di `0.30000000000000004`—bukan di nilai biner terdekat dari `0.3`. Dua sisi pembanding `===` di `ReconciliationGuard` kami tiba di dua titik biner yang berbeda, maka hasilnya `false`, maka ribuan transaksi dituduh anomali.

Dan perbaikannya untuk gejala ini sebenarnya sederhana: jangan bandingkan float pakai kesetaraan ketat, bandingkan pakai toleransi:

```php
var_dump(abs((0.1 + 0.2) - 0.3) < 1e-12); // bool(true)
```

"Berarti tinggal ganti `===` jadi cek toleransi, Bang?" tanya Jovian.

"Belum," jawabku pendek. "*Queue* meledak itu cuma gejala, Jov. Gejalanya murah. Yang bikin rekap koperasi beda $184.06 itu luka yang lebih dalam, dan aku udah curiga di mana letaknya."

Aku buka satu file lagi. File yang menyentuh uang secara langsung. Dan begitu aku lihat baris-barisnya, kopiku yang udah dingin itu rasanya makin pait.

## Bab 3: intval, Sang Pencuri Sen yang Halus

Inilah luka yang kuduga. Sistem *ledger* warisan dari vendor lama memang sudah benar menyimpan uang dalam **minor unit**—dolar disimpan sebagai sen, bilangan bulat murni. Konsepnya bagus, itu malah *best practice*. Tapi pintu masuknya yang salah. Setiap harga dari *merchant feed*—yang datang sebagai angka pecahan—dikonversi ke sen begini:

```php
<?php
// PriceConverter.php — warisan vendor lama
$cents = (int) ($unitPrice * 100);
```

Tebak apa yang terjadi dengan harga `$0.58`? Aku jalankan:

```php
$value = 0.58 * 100;
echo $value, "\n";             // 58
var_dump(intval($value));      // int(57)
var_dump((int) $value);        // int(57)
```

Aku tatap layar lama sekali. `echo` bilang 58, tapi begitu dikonversi ke *integer* dia jadi 57. Kembar palsu. Nilai yang *ditampilkan* dan nilai yang *tersimpan* itu dua hal yang berbeda: `0.58` nggak bisa disimpan eksak dalam biner, dia disimpan sebagai bilangan biner terdekat yang *sedikit lebih kecil* dari 0.58. Ketika dikali seratus, hasilnya bukan 58 tapi `57.99999999999999...`. Dan di sinilah sifat licik `intval()` dan *cast* `(int)` menguak wajahnya: **mereka bukan membulatkan ke bilangan terdekat, mereka memotong bagian pecahan dengan pembulatan ke arah nol**. Sisa `0.99999...` itu dibuang begitu aja. Satu sen. Hilang. Setiap kali harga segitu lewat, satu sen petani menguap tanpa jejak, tanpa *log error*, tanpa *exception*. Pencuri paling halus yang pernah aku temui.

Dengan emosi campur aduk—panik, malu, marah ke diri sendiri—aku mencoba *quick fix* yang (nanti kusadari) naif banget. "Mungkin cuma masalah presisi tampilan," batinku. "Kan bisa diatur di `php.ini`." Aku *set* `precision` tinggi supaya PHP "menghitung dengan benar":

```php
$sum = 0.1 + 0.2;

ini_set('precision', '17');
echo $sum, "\n";            // 0.30000000000000004

ini_set('precision', '14');
echo $sum, "\n";            // 0.3

var_dump($sum === 0.3);     // bool(false)
```

Gagal total. Nilai tampilannya berubah-ubah mengikuti *setting*, tapi perbandingannya tetap `false`. Kenapa `echo` tadi nunjukin `58` padahal tersimpannya `57.99...`? Karena pencetakan dengan `echo` memakai *directive* `precision`—dia mengatur **berapa digit yang dipakai saat float diubah jadi string**, lalu membulatkan teksnya. Digit-digit pamungkas "disembunyikan" di balik pembulatan tampilan. Konversi ke *integer* nggak pakai teks itu; dia membaca float yang tersimpan langsung, dan nilai tersimpan itu memang sedikit di bawah 58.

PHP juga punya *directive* terpisah bernama `serialize_precision`—terlepas dari namanya, dia mengatur representasi teks float dari `serialize()`, `json_encode()`, sampai `var_dump()`. Jadi `precision` dan `serialize_precision` itu **bukan fitur matematika**. Mereka cuma tukang *makeup*. Nggak ada satu *switch* di `php.ini` pun yang bisa mengubah float biner jadi desimal eksak.

Aku kepal tangan. Jam udah lewat 02.00 WIB. Aku hitung ulang manual pakai kalkulator HP: volume transaksi bulan ini memang memuat ribuan konversi harga-harga pecahan macam `$0.58`. Terkumpul dari konversi-konversi itu, sen-sen yang terpotong menjumlah ke `$184.06`. Pas dengan *gap* rekonsiliasi. Angkanya cocok sampai sen terakhir, dan kecocokan itu rasanya seperti pengakuan bersalah.

Aku mulai tulis *hotfix* paling aman dulu: kalau konversi float-ke-*integer* benar-benar dibutuhkan, bulatkan dulu sebelum dipotong:

```php
$value = 0.58 * 100;
var_dump((int) round($value)); // int(58)
```

`round()` dulu, baru *cast*. Satu sen selamat. Tapi dalam hati aku tahu ini masih tambal sulam—dan aku benar. Pas aku siap-siap *re-run* *batch* refund, bencana yang jauh lebih aneh datang menyambut.

## Bab 4: ID Sebesar Gunung yang Menguap Jadi Kabut

Kebijakan platform mengharuskan semua dana yang tertahan di *antrian anomali* tetap aman, dan sebagian transaksi menunggu *refund* ke pembeli. Aku jalankan ulang *batch refund* dengan kode *hotfix* barusan. Tidak lama, *job*-nya berhenti sendiri dengan *report* yang bikin alisku naik:

```text
[REFUND FAILED] transaction_id=9223372036854775808  reason=transaction not found
[REFUND FAILED] transaction_id=9223372036854775811  reason=transaction not found
[REFUND FAILED] transaction_id=9223372036854775840  reason=transaction not found
```

"Transaksi nggak ketemu?" gumamku. "ID-nya jelas-jelas ada di *payload* gateway."

Aku cek *payload* mentahnya. Dan di situ aku lihat sesuatu yang bikin bulu kuduk meremang: ID transaksi gateway kami itu bilangan bulat 64-bit *unsigned*—tipenya `uint64`, ID jenis *snowflake*. Beberapa ID-nya lebih besar dari batas *integer* PHP. Aku uji intuisiku langsung:

```php
var_dump(PHP_INT_MAX);      // int(9223372036854775807)
var_dump(PHP_INT_MAX + 1);  // float(9.223372036854776E+18)
```

Dan kini momen *quiz* kedua yang bikin aku terdiam. Aku pikir, ya sudah, integer mah bukan urusan *floating point*. Ini pasti aman. Aku jalankan:

```php
var_dump((9223372036854775808 - 1) === 9223372036854775807);      // bool(false)
var_dump(((PHP_INT_MAX + 1) - 1) === PHP_INT_MAX);                // bool(false)
```

`false`. Dua-duanya `false`. Aku ngerasa dunia matematika berkhianat. Tapi logikanya begini, dan ini yang bikin aku merinding paling dalam malam itu: di PHP, *integer* itu bertanda (*signed*) dan *platform-dependent*; di *build* 64-bit, rentangnya berhenti di `9223372036854775807` (`PHP_INT_MAX`). Menurut aturan *overflow* di manual, **literal atau hasil operasi yang lewat dari rentang itu otomatis berubah jadi float**.

Bingo. Float *binary64* punya *range* cukup untuk menampung angka sebesar itu—tapi *presisinya* nggak cukup untuk membedakan setiap *integer* di sekitarnya. Presisi float cuma 53 *bit*, sedangkan `2^63` butuh 63 *bit* untuk disimpan utuh. Jadi begitu `9223372036854775808` lahir sebagai float, digit-digit rendahnya hilang, diganti jadi perkiraan. Begitu bilangan itu jadi float, **mengubahnya kembali tidak akan pernah bisa memanggil pulang digit-digit yang hilang**. ID gunung itu menguap jadi kabut, dan kabut nggak bisa di-*grep*.

"Jov!" teriakku ke telepon. "Cek log refund yang gagal, semua yang gagal ID-nya di atas `9223372036854775807` nggak?"

Sebentar suara ketikan terdengar di seberang sana, diselingi deburan ombak Krui. "Iya, Bang! Pattern-nya persis gini! Yang sukses semua di bawah `PHP_INT_MAX`, yang gagal semua di atasnya!"

Aku trace lebih dalam. ID itu masuk lewat *webhook* JSON dari gateway. Dan `json_decode()` PHP, menemui angka yang nggak muat di *integer*, diam-diam mengubahnya jadi float:

```php
$payload = '{"transaction_id": 9223372036854775808}';
$id = json_decode($payload)->transaction_id;
var_dump($id); // float(9.2233720368548E+18)
```

ID yang sudah jadi kabut itu lalu kupakai buat manggil API refund. Gateway mencari `9223372036854775808` dan menemukan permintaan untuk angka lain yang mirip. Responsnya wajar saja: *transaction not found*. Dana refund nyangkut di *limbo*. Ditambah ribuan transaksi yang masih tertahan di *antrian anomali*, dana petani makin jauh dari rekening koperasi.

Aku bersandar. Jam 02:40 WIB. Dua neraka berbeda dalam satu malam: sen yang dicuri halus, dan ID yang menguap jadi kabut. Aku mulai ngerasa jadi *engineer* paling gagal di Sleman malam itu.

"Bang," suara Jovian lembut, beda dari nada paniknya tadi. "Abang masih ngeyel nggak mau nelpon Kak Myesha?"

Aku ketawa kecil, getir. "Sudah jam segini, Dik. Mana berani aku ganggu."

"Bang. Kak Myesha itu Kakak kita. Abang nelpon, nanti aku ikutan *conference*. Kita nggak nyender sendirian."

Aku mendial. Di sisi lain, suara itu angkat di dering kedua—tenang, seperti biasa.

"Halo, Dek Devan? Dik Jovian juga kan? Ada apa malam-malam? Tumben pada ngeramein *voice channel*," sapa Kak Myesha, Kakak sulung kami, *Tech Lead backend* di sebuah *unicorn*, yang kebetulan lagi ambil cuti di rumah nenek kami di Berbah, Sleman. Sayup-sayup kudengar suara jangkrik pekarangan Berbah, kontras sekali sama ombak Krui dan deg-degan kosanku.

Aku ceritakan semuanya. Antrian anomali, `$184.06`, `intval` pencuri sen, `precision` yang cuma tukang *makeup*, dan ID gunung yang jadi kabut. Hening sebentar. Lalu Kak Myesha ketawa pelan—bukan ketawa ngejek, ketawa yang kayak lagi inget kenangan lama.

"Kalian kena *trifecta* klasik, Dek," katanya. "Tiga penyakit yang paling sering saya temui di *code review*: membandingkan float dengan `===`, *blind cast* float ke *integer*, dan *integer overflow* jadi float. Tarik napas. Semua ini ada jalannya. Dan kalian beruntung kena malam ini, bukan pas tanggal gajian *merchant* besar."

"Justru ini tanggal 11, Kak. Ini malam pencairan dana petani," jawabku lirih.

Hening lagi, lebih panjang. "Oke," suaranya berubah serius. "Buka catatan kalian. Kita bereskan satu-satu, dari akar masalahnya: **pilih representasi angkanya dulu, baru hitung**."

## Bab 5: Zuhur dari String: BCMath, GMP, dan Kopi yang Akhirnya Sampai

Kata Kak Myesha, semua kebingungan malam itu bermuara ke satu kalimat yang akhirnya kami tulis besar di catatan tim: **kebenaran hasil hitung itu ditentukan sebelum hitung-hitungan dimulai, saat kita memilih representasinya.** Tidak ada *switch* ajaib di `php.ini`. Yang ada cuma pilihan: angka ini mau diperlakukan sebagai perkiraan, atau sebagai nilai eksak?

"Pertama," lanjut Kak Myesha, "float itu bukan musuh. Dia ringkas, cepat, dan pas buat besaran yang memang **aproksimasi**: statistik, rata-rata, prediksi. Tapi aturannya, jangan pernah bandingkan pakai kesetaraan ketat. Pakai batas toleransi yang masuk akal buat domain kalian:"

```php
$actual   = 0.1 + 0.2;
$expected = 0.3;

var_dump(abs($actual - $expected) < 1e-12); // bool(true)
```

"Tapi ingat, `1e-12` itu bukan angka sakti," tegas Kak Myesha. "Toleransi harus datang dari domain—dari skala nilai yang kalian proses. Konstanta `PHP_FLOAT_EPSILON` pun bukan obat untuk semua magnitudo; dia cuma menjelaskan jarak antar float yang bisa direpresentasikan di sekitar `1.0`. Antrian anomali kalian tinggal ganti `===` dengan cek toleransi—itu yang tadi Devan bilang."

"Kedua, dan ini yang menggigit kalian di konversi sen: **jangan pernah *blind cast* float ke *integer***. `intval()` dan `(int)` itu memotong ke arah nol, bukan membulatkan. Kalau kalian memang butuh bilangan bulat terdekat dari hasil hitung float, panggil `round()` dulu:"

```php
var_dump((int) round(0.58 * 100)); // int(58)
```

"Ketiga—dan ini yang paling penting buat kalian: **uang itu nggak boleh melewati float sama sekali**. Kalau nilainya punya satuan terkecil yang pasti—seperti sen—simpan satuan terkecil itu sebagai *integer*, dan konversinya harus eksak dari awal. Parse dari *string* desimal yang tervalidasi di *boundary*, bukan dari float yang udah sakit:"

```php
$unitPriceInCents = 58;   // diparse dari string harga, BUKAN (int) (0.58 * 100)
$quantity = 3;

$totalInCents = $unitPriceInCents * $quantity;
var_dump($totalInCents);  // int(174)
```

"Kalau nilai yang di-*scale* berpotensi lewat `PHP_INT_MAX`, jangan bersikukuh sama *integer* native. Pakai representasi presisi berhingga dari awal. Di sinilah *extension* inti PHP masuk," kata Kak Myesha, dan aku dengar dia mulai menikmati ngajarnya. "Untuk desimal presisi tinggi, ada **BCMath**. Dia kerjakan aritmetika desimal *arbitrary-precision*, dan fungsi tradisionalnya menerima **dan mengembalikan string**—jadi input desimal nggak perlu lewat float biner dulu:"

```php
var_dump(bcadd('0.1', '0.2', 1));   // string(3) "0.3"
var_dump(bcmul('0.58', '100', 0));  // string(2) "58"
```

"Kalau server kalian udah di PHP 8.4 ke atas, ada obyek `BcMath\Number` yang *immutable* dan mendukung operator aritmetika biasa, jadi kodenya lebih enak dibaca:"

```php
use BcMath\Number;

$sum = new Number('0.1') + new Number('0.2');
echo $sum, "\n"; // 0.3
```

"Dengar baik-baik ini, Dek," Kak Myesha menekankan tiap katanya. "**Tanda kutipnya itu penting**. Bangun perhitungan dari *string* desimal seperti `'0.1'`, BUKAN dari float yang mungkin udah kehilangan presisi. Float yang udah sakit itu kalau belakangan diubah jadi nilai BCMath, presisi aslinya nggak akan bisa direkonstruksi. Sakitnya udah keburu terlanjur." Aku angguk-angguk sendirian di kamar. Bagian itu persis mengenai `PriceConverter` kami.

"Terus ID gunung kami, Kak?" sela Jovian. "Yang lewat dari `PHP_INT_MAX`?"

"Untuk bilangan bulat berukuran berapa pun, pakai **GMP**," jawab Kak Myesha. "Dia kerja dengan *integer* dengan panjang *arbitrary*. Catat ya, dia nggak aktif secara *default* dan butuh *library* GMP eksternal—koordinasi sama tim *infra* kalian. Dan liat, dia bisa hitung contoh yang bikin kalian panik tadi tanpa meluber jadi float:"

```php
$number = gmp_init('9223372036854775808', 10);
$result = gmp_sub($number, '1');

echo gmp_strval($result), "\n"; // 9223372036854775807
```

"Inputnya juga harus *string*, Dik Jovian. Kalau kalian nulis `9223372036854775808` sebagai *literal* numerik PHP, PHP sudah keburu mengubahnya jadi float **sebelum** GMP menyentuhnya—dan itu udah terlambat. Di *boundary* JSON pun sama: pakai `JSON_BIGINT_AS_STRING` supaya angka yang nggak muat di *integer* diterima sebagai *string*, bukan dijadikan float diam-diam:"

```php
$payload = '{"transaction_id": 9223372036854775808}';

$data = json_decode($payload, true, 512, JSON_BIGINT_AS_STRING);
var_dump($data['transaction_id']); // string(19) "9223372036854775808"
```

"Satu catatan biar kalian nggak salah obat: GMP itu representasi *integer*, dia nggak bisa menyimpan `0.1`. Dia bisa nanganin nilai *fixed-scale* kalau aplikasinya nyimpen tiap jumlah sebagai *integer* satuan minor. Tapi kalau skala desimalnya itu bagian dari datanya—seperti harga dan biaya kalian—BCMath biasanya lebih jelas," tutup Kak Myesha. "Oh iya, satu kabar baik: ekosistem ini terus jalan. PHP 8.6 aja nambahin `gmp_prev_prime` dan `gmp_powm_sec` di GMP. Bahasanya hidup, dan kita semua ikut hidup bareng dia."

Kami pamit, dan aku langsung kerja. *Refactor*-nya jelas:

1. `ReconciliationGuard`: perbandingan `===` diganti cek toleransi `1e-9` (skala dolar kami, disepakati dari domain—bukan angka sakti).
2. `PriceConverter`: harga masuk sebagai **string** dari *feed*, divalidasi, lalu dikonversi ke sen lewat `bcmul($priceString, '100', 0)`. Tidak ada lagi `(int) ($float * 100)`.
3. *Ledger*: semua saldo tetap *integer* sen, sejak lahir.
4. *Webhook* gateway: `json_decode(..., JSON_BIGINT_AS_STRING)`, ID divalidasi sebagai *string* digit, dan API *client* refund dikirim tanpa pernah menyentuh float.

Aku *deploy*, jalankan ulang *batch*, dan duduk tegang ngeliat log. Baris demi baris lewat hijau. *Queue* anomali turun dari 3.412 ke 0. Rekap *gateway* sama *ledger* cocok. Selisih rekonsiliasi: **$0.00**.

```text
Settlement Batch #20260911 (rerun) ......  SUCCESS
Transactions processed .................  14.206
Manual review queue ....................  0
Reconciliation gap .....................  $0.00
```

Jam 04.30 WIB, aku bersandar lemas. Gimana gelapnya malam itu, segitulah terangnya rasanya begitu angka itu muncul. Slack berdentar.

**[04:37] Sinta (CS):** "Mas! Bu Rai dari koperasi telepon, katanya rekap dari pihak mereka sama laporan platform sekarang cocok persis. Dia kirim foto petani angkat karung kopi, sambil bilang makasih banyak."

Foto itu datang: pria-pria dan ibu-ibu di halaman pengeringan kopi Takengon, senyum lebar, karung-karung hijau di belakang mereka. Aku tatap lama. Sen-sen yang tadi pagi tersebar menguap entah ke mana-mana, malam itu aku kembalikan satu-satu ke pemiliknya. Rasanya, secara matematika sederhana, itu pekerjaan *engineer* paling penting yang pernah aku lakukan.

"Abang Devan berhasil, Kak!" seru Jovian di *conference* yang masih nyala. "Dana petani cair semua!"

"Bagus," jawab Kak Myesha, dan aku bisa *dengar* senyumnya. "Sekarang tidur. Dan satu lagi: Devan, kirim saya kopi Gayo satu kilo. Kakak baru aja nyelametin `$184.06`, setidaknya dibayar pakai kopi yang asli dari Takengon."

"Siap, Kakak!" jawabku sambil ketawa, matanya udah berat, tapi hatinya ringan.

Sebelum aku tutup laptop, aku tulis satu kalimat di catatan tim, buat kami, dan buat siapa pun yang suatu hari kena *trifecta* yang sama: **angka itu nggak pernah bohong. Yang bohong itu representasinya—maka pilih representasinya dengan benar sebelum kamu mulai berhitung.** Jangan pernah *blind cast* float ke *integer*, jangan bandingkan float dengan `===`, jangan percaya `precision` di `php.ini` sebagai alat hitung, dan jangan biarkan angka raksasa lewat pintu JSON tanpa jadi *string*.

Di luar, gerimis Sleman udah berhenti. Di layar, MD5—eh, maksudku, *reconciliation gap*-nya tetap `$0.00`. Kopi Gayo di cup-ku udah habis, tapi aromanya masih ada. Dan malam ini, aku tidur dengan satu sen yang utuh di hati.