---
layout: post
title: "Tragedi Flash Sale Sleman: Membedah Race Condition dan Distributed Lock dengan Redis"
subtitle: "Gimana caranya aku, Kak Myesha, dan Jovian nyelametin server dari serangan zombie checkout yang bikin overstock parah."
date: 2026-07-05 13:20:00 +0700
categories: [Engineering, Story]
tags: [Redis, Node.js, Race Condition, Backend, Microservices]
---

## Bab 1: Hujan, Kopi, dan Bencana di Sleman

Di luar jendela kamarku di Sleman, hujan turun deres banget. Bau tanah basah yang kena air hujan atau biasa disebut petrichor, nyampur sama wangi kopi robusta seduhanku yang udah mulai dingin. Jam di sudut layar MacBook-ku nunjukin pukul 23:55 WIB. Lima menit lagi, *flash sale* gede-gilaan dari klien *e-commerce* lokal yang lagi aku pegang backend-nya bakal dimulai. 

Aku, Devan, sebagai *mid-level backend engineer* yang ngerasa udah nerapin "best practices", ngerasa cukup pede. Aku udah nambahin *replica* database, nge-scale up *pods* di Kubernetes, dan nambahin *cache* di beberapa *endpoint* kritikal. "Semuanya bakal aman," batinku sambil nyeruput kopi yang rasanya makin pait.

Tepat pukul 00:00 WIB, *traffic* masuk kayak air bah. Dasbor Grafana di monitor kedua gue langsung merah semua. *CPU usage* naik drastis. Awalnya gue senyum simpul, bangga ngeliat infrastruktur yang gue bangun bisa nahan *load* yang lumayan brutal. Tapi senyum itu cuma bertahan sekitar 45 detik.

Tiba-tiba, *channel* Slack meledak. 

**[00:01] CS_Rina:** "@Devan, Mas! Ini kenapa yang beli *smartphone* promo stoknya minus?! Stok cuma ada 100, tapi yang berhasil checkout dan bayar udah 450 orang!!"

Darahku serasa berhenti ngalir. *What the hell?* Aku langsung buka terminal, *query* ke database *production* dengan tangan gemeteran.

```sql
SELECT id, name, stock FROM products WHERE id = 8891;
```

Hasilnya:
```text
id   | name               | stock
---- | ------------------ | ------
8891 | Smartphone Promo 1 | -350
```

Gila. Kacau parah. *Minus tiga ratus lima puluh?!* Perusahaan bisa rugi ratusan juta kalau harus *refund* atau nombokin barang ini. Keringat dingin mulai ngucur di dahiku, ngalahin dinginnya AC kamar. Otakku nge-blank. Di kodeku, udah jelas-jelas ada pengecekan stok sebelum *insert* order. Kenapa bisa tembus?!

Di tengah kepanikan itu, notifikasi Discord bunyi. Ada panggilan masuk dari Jovian, adikku yang paling bontot, yang lagi kerja *remote* sebagai anak *Data/DevOps* di Pante Raya. 

"Bang Dev! Abang liat log nggak?!" suara Jovian terdengar panik dari seberang sana. Malam jahanam di Sleman baru aja dimulai.


## Bab 2: Jeritan Log dari Pante Raya dan Misteri Race Condition

"Aku liat, Jov! Ini aku lagi buka DB, kok bisa minus gini anjir?!" balasku setengah teriak. Tanganku sibuk ngetik sana-sini, nyari letak kesalahan.

"Bang, aku lagi mantau Kibana dari tadi. Coba Abang cek log untuk *Product ID* 8891 di jam 00:00:02. Ada sekitar 500 *request* masuk di milidetik yang hampir bersamaan!" Suara Jovian terdengar bergetar, tapi dia berusaha ngasih data seakurat mungkin dari kamar kosannya yang sepi di Pante Raya. "Mereka semua ngelewatin validasi stok Abang!"

Aku langsung buka *source code* Node.js milikku. Ini kode *checkout* yang aku tulis dengan penuh rasa bangga beberapa hari yang lalu:

```javascript
// WARNING: KODE BERBAHAYA (DO NOT USE IN PRODUCTION)
async function processCheckout(userId, productId) {
    try {
        // 1. Cek stok saat ini
        const product = await db.query(
            'SELECT stock FROM products WHERE id = ?', 
            [productId]
        );
        
        const currentStock = product[0].stock;

        // 2. Validasi stok
        if (currentStock <= 0) {
            throw new Error("Maaf, barang sudah habis!");
        }

        // 3. Simulasi proses yang agak berat (kalkulasi diskon, dll)
        await doSomeHeavyCalculation();

        // 4. Kurangi stok dan buat order
        await db.query(
            'UPDATE products SET stock = stock - 1 WHERE id = ?', 
            [productId]
        );
        
        await db.query(
            'INSERT INTO orders (user_id, product_id, status) VALUES (?, ?, ?)', 
            [userId, productId, 'PAID']
        );

        return { status: 'SUCCESS', message: 'Checkout berhasil!' };
    } catch (error) {
        throw error;
    }
}
```

"Jov, kodeku logikanya bener kok! Aku `SELECT` dulu, kalau stoknya di atas nol, baru aku `UPDATE`," kataku sambil gigit jari.

Jovian menghela napas panjang. "Bang... itu klasik *Race Condition*. Pas 500 *request* masuk barengan di milidetik yang sama, mereka semua ngejalanin *query* `SELECT` dan ngeliat stoknya masih 100. Belum sempet *request* pertama ngelakuin `UPDATE` buat ngurangin stok, *request* kedua sampai ke-500 udah keburu lolos blok `if (currentStock <= 0)`. Akhirnya? Semuanya ngurangin stok secara buta."

*Shit.* Bener juga. Aku ngerasa jadi *engineer* paling bodoh malam itu. Di lingkungan dengan konkurensi tinggi, *Read-Modify-Write* tanpa *locking* adalah resep bunuh diri. Dan aku baru aja neken tombol pemicu bomnya. 


## Bab 3: Solusi Naif dan Keputusasaan yang Makin Dalam

Mendengar penjelasan Jovian, aku ngerasa harus gerak cepat. "Oke, Jov. Abang bakal pasang Redis *Lock* sekarang. Mumpung *flash sale* sesi kedua mulai jam 01:00. Abang *hotfix* ke *production* sekarang."

Otakku bekerja cepat. Redis! Ya, Redis punya fitur `SETNX` (*Set if Not eXists*). Aku bisa pakai itu buat nge-lock *Product ID* biar cuma satu *request* yang bisa proses *checkout* dalam satu waktu.

Dengan jari gemetar, aku nulis kode perbaikan. Aku tambahin *lock* pakai Redis:

```javascript
// KODE HOTFIX SEMENTARA (MASIH BERBAHAYA)
async function processCheckoutWithNaiveLock(userId, productId) {
    const lockKey = `lock:product:${productId}`;
    
    // Set lock dengan TTL 5 detik
    const acquired = await redis.set(lockKey, 'locked', 'NX', 'EX', 5);
    
    if (!acquired) {
        throw new Error("Sistem sedang sibuk, silakan coba lagi (Error: Lock failed)");
    }

    try {
        const product = await db.query('SELECT stock FROM products WHERE id = ?', [productId]);
        
        if (product[0].stock <= 0) {
            throw new Error("Maaf, barang sudah habis!");
        }

        await doSomeHeavyCalculation(); // Anggap aja butuh waktu 6 detik

        await db.query('UPDATE products SET stock = stock - 1 WHERE id = ?', [productId]);
        await db.query('INSERT INTO orders ...');

        return { status: 'SUCCESS' };
    } finally {
        // Rilis lock setelah selesai
        await redis.del(lockKey);
    }
}
```

Aku *push* kodenya. *Pipeline* CI/CD jalan, dan *hotfix* *deploy* ke *production* jam 00:45. Aku nyender di kursi, ngusap wajah yang basah karena keringat. "Aman, Jov. Udah Abang pasang *lock* di Redis."

Tapi tragedi belum selesai. Pas jam 01:00 WIB, *flash sale* sesi kedua dibuka.

Awalnya lancar. Angka stok berkurang perlahan secara berurutan. Tapi masuk di menit kedua, tiba-tiba sistem *hang*. Orderan gagal semua. CS kembali ngamuk di Slack. 

Jovian teriak lagi di telepon, "Bang! Orderan nyangkut semua! Terus ada beberapa user yang komplain duitnya kepotong tapi pesanan gagal. Dan gawatnya lagi... *race condition*-nya masih terjadi buat beberapa *user*!"

"HAH?! Nggak mungkin! Kan udah Abang *lock* pakai `SETNX`?!" teriakku ngerasa frustrasi banget. Rasanya pengen banting MacBook. 

Dalam keputusasaan yang absolut, layar Discord-ku kedip-kedip. Ada *incoming call* lagi ke grup *voice channel* kita. Itu Kak Myesha. Kakak sulungku, *Tech Lead* di sebuah *unicorn* besar yang lagi pulkam nyari ketenangan di Takengon, Aceh Tengah.

"Kenapa pada teriak-teriak malam-malam, Dek?" suara Kak Myesha terdengar tenang banget, sangat kontras sama kepanikan gue dan Jovian. Di *background* suaranya, sesekali kedengeran suara jangkrik malam dari pegunungan Gayo.


## Bab 4: Kak Myesha dan Sihir Redlock yang Menyelamatkan

Aku langsung nyeritain semuanya dengan nada putus asa. Dari masalah awal *overstock*, sampai solusi `SETNX`-ku yang malah bikin sistem *deadlock* dan tetep bocor.

Kak Myesha cuma ketawa kecil. "Devan, Devan... Adik tau nggak kenapa solusi Redis `SETNX` kamu itu naif banget dan malah nambah masalah?"

"Kenapa, Kak? Kan kodenya udah aku kasih `EX 5` (Expire 5 detik), terus pas selesai aku `del` lock-nya," bantahku masih ngerasa bener.

"Coba bayangin skenario ini, Dek," kata Kak Myesha dengan nada mengayomi layaknya seorang mentor. "Gimana kalau proses `doSomeHeavyCalculation()` atau *query* database kamu ngalamin perlambatan dan makan waktu 6 detik?"

Aku mikir sejenak. "Ehm... ya prosesnya jalan terus?"

"Bener. Tapi inget, *lock* kamu di Redis kedaluwarsa dalam 5 detik. Berarti, di detik ke 5.1, Redis kamu udah nggak ada *lock*-nya. *Request* orang lain (Sebut aja User B) masuk, dan dia *berhasil* dapet *lock* baru karena *lock* lama udah *expire*." 

Jovian dari Pante Raya nyeletuk, "Oh! Berarti sekarang ada DUA proses yang jalan barengan masuk ke area kritikal dong, Kak?"

"Tepat 100 buat Jovian!" puji Kak Myesha. "Dan yang lebih parah, pas *request* punya Devan (User A) selesai di detik ke-6, kode kamu jalanin blok `finally { await redis.del(lockKey); }`. Padahal *lockKey* itu sekarang udah jadi miliknya User B! Akhirnya kamu ngehapus *lock* punya orang lain, bikin *request* User C bisa masuk lagi. Begitu terus sampai kiamat. Chaos total."

Aku mematung. Pantesan *race condition* tetep kejadian, dan sistem jadi *hang* karena *lock* kehapus sembarangan atau nyangkut kalau *service* mati di tengah jalan. "Terus Devan harus gimana, Kak? *Traffic* masih jalan nih..." suaraku melemah.

"Pakai *Distributed Lock* yang bener. Implementasi standarnya Redis itu namanya **Redlock**. Jangan bikin algoritma *locking* sendiri kalau lo belum paham betul soal *clock drift* dan *fencing token*," jelas Kak Myesha panjang lebar. "Coba buka npm, install `redlock` sama `ioredis`. Kakak pandu kodenya dari sini. Tarik napas dulu, gausah panik."

Dengan dipandu Kak Myesha dari Takengon, aku mulai merombak kode. Kak Myesha ngejelasin kalau `redlock` secara otomatis nge-handle validasi *ownership* dari sebuah *lock*. Jadi dia nggak bakal hapus *lock* punya orang lain. Dia juga punya fitur *retry* otomatis.

Berikut adalah kode penyelamat yang kami susun malam itu:

```javascript
const Client = require('ioredis');
const Redlock = require('redlock');

// Inisialisasi koneksi Redis
const redisClient = new Client({ 
    host: process.env.REDIS_HOST, 
    port: process.env.REDIS_PORT 
});

// Setup Redlock
const redlock = new Redlock(
    [redisClient], // Bisa masukin banyak instance Redis untuk high availability
    {
        driftFactor: 0.01, // Toleransi perbedaan waktu antar server (clock drift)
        retryCount: 15,    // Coba lock ulang 15 kali kalau gagal
        retryDelay: 200,   // Jeda 200ms setiap kali mencoba ulang
        retryJitter: 200,  // Random jitter untuk menghindari thundering herd
        automaticExtensionThreshold: 500 // Ekstensi otomatis jika proses belum selesai
    }
);

async function processCheckoutRobust(userId, productId) {
    const resource = `locks:checkout:product:${productId}`;
    const ttl = 5000; // 5 detik TTL awal
    let lock;

    try {
        // Redlock akan mencoba mendapatkan lock.
        // Jika gagal, dia akan otomatis retry sesuai konfigurasi di atas.
        lock = await redlock.acquire([resource], ttl);
        
        console.log(`Lock acquired by User ${userId} for Product ${productId}`);

        // 1. Cek stok
        const product = await db.query('SELECT stock FROM products WHERE id = ?', [productId]);
        
        if (product[0].stock <= 0) {
            throw new Error("Maaf, barang sudah habis!");
        }

        // 2. Simulasi proses berat yang tidak bisa diprediksi
        await doSomeHeavyCalculation();

        // PENTING: Kadang di proses panjang, kita butuh extend TTL lock manual
        // await lock.extend(5000); 

        // 3. Eksekusi query (sudah aman dari concurrent access)
        await db.query('UPDATE products SET stock = stock - 1 WHERE id = ?', [productId]);
        await db.query('INSERT INTO orders (user_id, product_id, status) VALUES (?, ?, ?)', [userId, productId, 'PAID']);

        return { status: 'SUCCESS', message: 'Order berhasil diamankan.' };
    } catch (error) {
        // Bedakan error lock timeout dengan error logic
        if (error.name === 'LockError') {
            throw new Error("Tingginya antrean. Silakan coba klik beli lagi!");
        }
        throw error;
    } finally {
        // 4. Rilis lock HANYA JIKA lock tersebut milik eksekusi ini
        if (lock) {
            try {
                await lock.release();
                console.log(`Lock released for Product ${productId}`);
            } catch (err) {
                console.error("Gagal melepaskan lock, tapi akan expire sendiri:", err);
            }
        }
    }
}
```

"Adik perhatiin baik-baik, Dev," pesan Kak Myesha. "Di blok `finally`, objek `lock` itu punya *unique identifier*. Jadi method `.release()` nggak bakal ngehapus kunci milik *request* lain. Dan parameter `retryCount` ngebantu *user* nggak langsung nerima *error*, tapi sistem kamu nunggu sejenak di *background* sebelum nyoba ambil *lock* lagi."

Aku ngangguk paham. Kode ini jauh lebih elegan dan matematis. Aku langsung *commit*, *push*, dan deploy *hotfix* v2 ke server.


## Bab 5: Pagi yang Damai dan Pelajaran Seumur Hidup

Jarum jam nunjukin pukul 03:30 WIB. Di layar Kibana milik Jovian di Pante Raya, garis grafik mulai stabil. Nggak ada lagi *error log* merah. Nggak ada lagi pesanan yang jebol batas stok. Ratusan *request* yang masuk barengan berhasil diantrekan dengan mulus oleh sistem Redlock. Kalaupun ada yang *timeout*, *user* dapet pesan yang jelas buat nyoba lagi, bukannya bikin database kacau.

Aku nyender lemas di kursi. Suara hujan di Sleman udah berubah jadi gerimis kecil yang menenangkan. Perasaan lega yang luar biasa mengalir di dadaku.

"Bang... aman bang," suara Jovian terdengar lirih, nyaris ketiduran di depan laptopnya. "Grafik order sukses landai, stok berhenti di angka 0. Nggak ada *minus stock* lagi."

"Syukurlah," helaan napasku panjang banget. Aku ngerasa utang nyawa sama Kak Myesha. "Kak Yesh... *thank you* banget ya. Asli, kalau nggak ada Kakak, aku besok pagi pasti udah dipanggil HRD buat tanda tangan surat pengunduran diri atau ganti rugi ratusan juta."

Terdengar suara seruputan kopi dari seberang telepon. Di Takengon, langit mungkin udah mulai agak terang. "Santai, Dek. Kakak juga dulu pernah bikin *bug* yang lebih parah dari ini waktu masih junior. Namanya juga *engineer*, belajar dari *production incident* itu cara paling ampuh buat naik level," balas Kak Myesha dengan nada lembutnya yang selalu bikin hati adek-adeknya tenang. 

"Tapi inget, ini pelajaran penting buat kalian berdua," lanjutnya. Jovian yang tadinya ngantuk langsung setengah melek denger nada serius kakaknya. "*Concurrency* dan *distributed system* itu nggak bisa di-handle pakai logika *procedural* biasa. Jangan pernah berasumsi blok kode kalian bakal dieksekusi secara terisolasi, kecuali kalian yang mengisolasinya sendiri."

Aku tersenyum kecil. "Siap, *Tech Lead*. Nggak bakal aku sepelein lagi urusan *locking*."

"Bagus. Besok kalau Kakak turun ke Jogja, Adik harus traktir Kakak Kopi Merapi. Bawa Jovian juga kalau dia lagi libur dari Pante Raya, kita kumpul di Sleman," canda Kak Myesha.

"Pasti, Kak. *All you can eat* buat Kakak," janjiku tulus.

Kami bertiga ngobrol santai beberapa menit sebelum akhirnya pamit buat tidur. Malam itu, di antara dinginnya sisa hujan Sleman, heningnya kosan di Pante Raya, dan sejuknya udara pagi Takengon, aku sadar betapa berharganya punya saudara yang juga *partner in crime* di dunia *coding*. 

Malam jahanam itu berakhir manis. Server selamat, dan yang pasti, *skill set* backend-ku resmi naik satu level berkat tragedi *flash sale* ini. Dan buat kalian yang baca ini: tolong, demi kewarasan hidup kalian, jangan pernah bikin *custom distributed lock* pakai `SETNX` polosan kalau kalian nggak mau nggak tidur semalaman. Pakailah alat yang sudah teruji seperti Redlock!
