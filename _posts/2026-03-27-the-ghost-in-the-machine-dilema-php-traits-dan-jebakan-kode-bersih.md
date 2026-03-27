---
layout: post
title: "The Ghost in the Machine: Dilema PHP Traits dan Jebakan Kode yang 'Terlalu Bersih'"
subtitle: "Mempelajari Mengapa 'DRY' Tanpa Arah Bisa Menjadi Racun dalam Arsitektur PHP Modern"
date: 2026-03-27 15:30:00 +0700
categories: [tech, php, architecture]
tags: [php, laravel, clean-code, refactoring, solid-principles, traits, composition]
author: Kuli Kode
---

Di dunia pengembangan perangkat lunak, ada sebuah mantra yang sering diucapkan dengan nada suci: "Don't Repeat Yourself" atau DRY. Bagi pengembang PHP, mantra ini sering kali menemukan perwujudannya dalam sebuah fitur bernama *Traits*. Ia menjanjikan keajaiban: kemampuan untuk menyisipkan fungsionalitas ke dalam kelas tanpa harus terjebak dalam hierarki pewarisan (*inheritance*) yang kaku. Namun, seperti halnya setiap jalan pintas dalam arsitektur sistem, *Traits* membawa hantu-hantu yang sering kali baru menampakkan diri saat sistem sudah terlalu besar untuk diperbaiki tanpa rasa sakit yang luar biasa.

Baru-baru ini, sebuah artikel di Dev.to berjudul "Why I Avoid PHP Traits (And What I Use Instead)" memicu perdebatan panas di meja kerja kami. Penulisnya berargumen bahwa *Traits* adalah sebuah *design smell*—sebuah tanda bahwa ada yang salah dengan rancangan kita. Secara umum, aku cenderung setuju. Tapi, seperti kebanyakan hal dalam hidup, kebenaran mutlak jarang sekali hitam atau putih.

Ini adalah kisah tentang bagaimana tim kami—Devan, Myesha, dan Jovian—terjebak dalam labirin *Traits*, dan bagaimana kami akhirnya menemukan jalan keluar yang lebih elegan tanpa harus membuang semua alat yang kami miliki.

## Bab 1: Kilauan Emas di Ujung Jari (Godaan DRY)

Sore itu, suasana kantor terasa hangat oleh aroma kopi yang baru diseduh. Jovian, yang sedang bersemangat mengejar *deadline* fitur *Payment Gateway* baru, tampak sangat puas dengan dirinya sendiri. Di layar monitornya, sebuah *Controller* PHP yang biasanya panjang dan berantakan kini tampak ramping dan estetik. Hanya ada beberapa baris kode di dalamnya.

"Lihat ini, Kak Devan," seru Jovian, memutar kursinya dengan penuh kemenangan. "Cuma sepuluh baris! Semuanya bersih, berkat *Traits*."

Jovian menunjukkan kodenya dengan bangga. Ia telah menciptakan sebuah sistem di mana hampir setiap fungsionalitas umum—mulai dari validasi, *logging*, respons JSON, hingga otorisasi—dibungkus ke dalam *Traits*.

```php
<?php

namespace App\Http\Controllers;

use App\Traits\ValidatesRequest;
use App\Traits\RespondsWithJson;
use App\Traits\Loggable;
use App\Traits\AuthenticatesUser;

class PaymentController extends Controller
{
    use ValidatesRequest, RespondsWithJson, Loggable, AuthenticatesUser;

    public function process(Request $request)
    {
        $this->logInfo("Memulai proses pembayaran...");
        
        $data = $this->validateInput($request, [
            'amount' => 'required|numeric',
            'gateway' => 'required|string',
        ]);

        $user = $this->getCurrentUser();
        
        // Logika bisnis yang sangat tipis
        $status = $this->paymentService->handle($user, $data);

        return $this->successResponse($status, "Pembayaran berhasil diproses");
    }
}
```

Bagi mata yang tidak terlatih, ini tampak seperti puncak dari *Clean Code*. Tidak ada duplikasi. Kode itu terbaca seperti bahasa manusia. Jovian merasa telah menemukan rahasia suci produktivitas. Ia tidak perlu lagi menulis ulang `return response()->json(...)` atau memanggil *Logger* secara manual. Cukup gunakan satu baris `use`, dan kelasnya secara ajaib memiliki kekuatan baru.

"Aku bisa membuat sepuluh *controller* seperti ini dalam sejam," tambah Jovian, sambil menyesap kopinya.

Devan hanya tersenyum tipis, sebuah senyum yang mengandung campuran antara apresiasi dan kekhawatiran yang tersembunyi. Ia melihat melampaui keindahan baris kode itu. Ia melihat ketergantungan yang tersembunyi. Ia melihat *Traits* yang saling bertumpuk seperti kartu-kartu yang tidak stabil.

"Terlihat sangat efisien, Jo," kata Devan tenang. "Tapi, pernahkah kamu bertanya-tanya, apa yang terjadi jika `ValidatesRequest` dan `RespondsWithJson` sama-sama ingin mendefinisikan variabel `$config`? Atau bagaimana jika kita ingin mengetes `PaymentController` ini tanpa harus memuat seluruh mekanisme otentikasi yang ada di dalam `AuthenticatesUser`?"

Jovian mengerutkan kening. "Ah, itu kan masalah nanti, Kak. Lagian, kita bisa pakai `insteadof` kalau ada konflik nama."

Namun, di sudut ruangan, Myesha sedang menatap layar monitornya dengan ekspresi yang sangat berbeda. Ia sedang mencoba menulis *unit test* untuk fitur yang baru saja dikerjakan Jovian, dan ia tampak seperti orang yang sedang mencoba mengurai benang kusut di dalam kegelapan. Baginya, kilauan emas yang dibanggakan Jovian hanyalah awal dari sebuah mimpi buruk arsitektural.

Myesha menghela napas panjang. Ia tahu bahwa kode yang tampak "bersih" di permukaan sering kali menyembunyikan kekacauan yang jauh lebih besar di bawahnya. Dan benar saja, hantu-hantu itu mulai berbisik di balik dinding-dinding kelas yang ramping itu.

## Bab 2: Bisikan di Balik Dinding (Tabrakan State)

Masalah pertama muncul justru saat tim sedang melakukan integrasi fitur *Audit Trail*. Jovian menambahkan satu lagi *Trait* bernama `Auditable` ke hampir seluruh *Controller* mereka. Rencananya sederhana: setiap tindakan pengguna harus dicatat secara otomatis ke dalam database audit.

Namun, sesuatu yang aneh terjadi. Tiba-tiba saja, fungsi *logging* yang sebelumnya berjalan lancar mulai menghasilkan data yang sampah. Pesan log yang seharusnya berisi detail transaksi malah berisi informasi mentah tentang konfigurasi database.

"Kenapa `Loggable` tiba-tiba jadi rusak?" keluh Jovian, jarinya menari liar di atas keyboard mencoba mencari tahu penyebabnya.

Myesha menghampiri meja Jovian. "Aku sudah cek, Jo. Masalahnya bukan di kodenya, tapi di *state*-nya."

Ia membuka dua file *Trait* secara berdampingan. Di dalam `Loggable`, Jovian mendefinisikan sebuah properti:

```php
trait Loggable {
    protected $context = 'general';

    protected function logInfo($message) {
        // Menggunakan $this->context untuk menentukan prefix log
        Log::info("[{$this->context}] " . $message);
    }
}
```

Dan di dalam `Auditable` yang baru saja ditambahkan:

```php
trait Auditable {
    protected $context = [];

    protected function recordAudit($action) {
        // Menggunakan $this->context untuk menyimpan payload audit
        Audit::create([
            'action' => $action,
            'payload' => $this->context
        ]);
    }
}
```

"Lihat?" Myesha menunjuk ke layar. "Keduanya menggunakan properti bernama `$context`. Karena *Traits* secara teknis adalah bagian dari kelas yang menggunakannya, mereka berbagi ruang memori yang sama. Saat `PaymentController` memanggil `use Loggable, Auditable;`, terjadi tabrakan. `Auditable` menimpa `$context` milik `Loggable` yang tadinya string menjadi array, atau sebaliknya."

Ini adalah masalah klasik *The Diamond Problem* yang sering menghantui bahasa yang mendukung *multiple inheritance* atau fitur serupa. PHP memang tidak mengizinkan pewarisan ganda, namun *Traits* memberikan ilusi tersebut, lengkap dengan segala risikonya.

"Tapi aku bisa mengganti namanya, kan?" bela Jovian.

"Ya, kamu bisa menggantinya hari ini," balas Myesha tegas. "Tapi bagaimana dengan besok? Bagaimana jika kita punya lima *trait*? Sepuluh? Setiap kali kamu menambahkan *trait* baru, kamu sedang bermain judi dengan seluruh properti yang sudah ada di kelas tersebut. Kamu tidak punya enkapsulasi di sini. Semuanya terbuka dan saling menimpa."

Jovian terdiam. Ia mulai menyadari bahwa "kemudahan" yang ia banggakan sebenarnya adalah sebuah bom waktu. *Traits* bukan sekadar alat bantu; mereka adalah parasit yang menempel pada kelas inangnya, mengonsumsi ruang nama yang sama tanpa ada batas yang jelas.

Keadaan semakin memburuk ketika mereka menyadari bahwa kesalahan ini bukan hanya pada properti, tapi juga pada metode. Jika dua *trait* memiliki nama metode yang sama, PHP akan memaksamu untuk memilih salah satu menggunakan sintaks `insteadof` yang sangat kaku. Kode yang tadinya ramping kini mulai dipenuhi dengan deklarasi-deklarasi administratif hanya untuk mencegah mereka saling bunuh.

```php
class PaymentController extends Controller {
    use Loggable, Auditable {
        Auditable::recordAction insteadof Loggable;
        Loggable::logAction as logGeneral;
    }
    // ...
}
```

"Ini bukan lagi *Clean Code*," gumam Jovian lesu. "Ini adalah birokrasi kode."

Devan, yang sejak tadi mendengarkan dari kejauhan, akhirnya angkat bicara. "Masalahnya, Jo, adalah kita menggunakan *Traits* untuk mengelola logika bisnis yang memiliki *state*. *Traits* seharusnya digunakan untuk *behavior* murni, atau lebih baik lagi, tidak digunakan sama sekali jika komposisi bisa menyelesaikan masalah itu dengan lebih jujur."

Tapi perdebatan ini baru saja dimulai. Karena jika tabrakan *state* adalah sebuah gangguan, maka masalah yang dihadapi Myesha di bagian pengujian adalah sebuah bencana besar yang mengancam integritas seluruh sistem.

## Bab 3: Labirin Tanpa Pintu (Kutukan Pengujian)

Myesha adalah tipe pengembang yang percaya bahwa kode yang tidak bisa dites adalah kode yang belum selesai. Dan baginya, *Traits* yang dibuat oleh Jovian adalah sebuah labirin tanpa pintu masuk yang jelas.

Malam itu, Myesha masih berada di kantor, ditemani oleh suara detak jam dinding dan cahaya biru dari monitornya. Ia sedang mencoba membuat *Unit Test* untuk `PaymentService` yang sayangnya, juga menggunakan beberapa *Traits* "ajaib" buatan Jovian.

"Bagaimana caranya aku mem-mock sesuatu yang tidak ada di sana?" gerutu Myesha.

Masalah utama dengan *Traits* adalah mereka menyembunyikan dependensi. Ketika sebuah kelas menggunakan *Trait*, dependensi yang dibutuhkan oleh *Trait* tersebut sering kali tidak terlihat dari konstruktor kelas inang.

```php
trait AuthenticatesUser {
    public function getCurrentUser() {
        // Mengandalkan helper global atau fasad Laravel
        return Auth::user() ?? throw new \Exception("Unauthorized");
    }
}

class PaymentService {
    use AuthenticatesUser;

    public function process($amount) {
        $user = $this->getCurrentUser();
        // ... logika proses pembayaran
    }
}
```

Dalam contoh di atas, `PaymentService` tampak seperti tidak membutuhkan dependensi apa pun. Namun, secara internal, ia bergantung sepenuhnya pada status otentikasi global. Saat Myesha ingin mengetes logika pembayaran tanpa harus melibatkan seluruh mekanisme *session* dan *database* pengguna, ia menemui jalan buntu.

"Aku tidak bisa melakukan *Dependency Injection* ke dalam *Trait*," keluh Myesha kepada Devan yang baru saja kembali dari pantry. "Jadi, setiap kali aku mengetes `PaymentService`, aku terpaksa harus berurusan dengan `Auth::user()`. Aku harus melakukan *mocking* pada *Static Facade*, yang kita semua tahu betapa rapuhnya itu. Ini bukan *Unit Test* lagi; ini hampir jadi *Integration Test* yang dipaksakan."

Devan mengangguk paham. Ia menarik kursi di sebelah Myesha. "Itulah alasan mengapa artikel di Dev.to itu menyebut *Traits* sebagai *hidden coupling*. Mereka menghubungkan kelasmu dengan dunia luar secara sembunyi-sembunyi melalui pintu belakang. Dan karena mereka bukan objek yang bisa berdiri sendiri, kamu tidak bisa menggantinya dengan implementasi palsu (*fake*) saat pengujian."

Myesha menunjukkan kodenya yang penuh dengan *mocking* yang rumit. "Lihat ini, Dev. Hanya untuk mengetes satu fungsi kecil, aku harus menyiapkan sepuluh baris kode untuk memanipulasi lingkungan global agar *Trait* itu tidak meledak. Dan jika besok Jovian mengubah cara kerja `getCurrentUser()` di dalam *Trait*, tes ini akan tetap hijau padahal aplikasinya mungkin rusak, atau sebaliknya, tesnya merah padahal logikanya benar."

Kesulitan pengujian ini adalah tanda nyata dari rusaknya prinsip *Single Responsibility*. Sebuah kelas seharusnya tahu apa yang ia butuhkan untuk bekerja, dan dunia luar seharusnya bisa memberikannya melalui pintu depan (konstruktor). *Traits* melanggar perjanjian ini. Mereka menyuntikkan kebutuhan ke dalam kelas tanpa memberitahu siapa pun.

"Lalu, apa solusinya?" tanya Myesha frustrasi. "Apakah kita harus kembali ke cara lama dengan menulis ulang semua kode itu di setiap kelas? Bukankah itu yang ingin kita hindari dengan DRY?"

"DRY bukan berarti kita tidak boleh menulis kode yang sama," jawab Devan bijak. "DRY berarti setiap pengetahuan dalam sistem harus memiliki representasi tunggal, otoritatif, dan tidak ambigu. Dan representasi itu tidak harus selalu berupa *Trait*. Sering kali, sebuah *Service Class* sederhana yang diinjeksikan jauh lebih baik daripada *Trait* yang disuntikkan."

Devan kemudian mulai membuka beberapa referensi di browsernya, termasuk artikel yang mereka diskusikan. Ia tahu bahwa inilah saatnya bagi tim untuk benar-benar memahami perbedaan antara penggunaan kembali kode (*code reuse*) yang sehat dan yang beracun.

"Ayo kita kumpulkan Jovian besok pagi," ajak Devan. "Kita perlu melakukan refaktor besar-besaran sebelum sistem ini menjadi monster yang tak terkendali."

Malam itu berakhir dengan rencana besar di kepala Devan. Ia tahu bahwa Jovian tidak salah sepenuhnya—ia hanya terlalu bersemangat dengan kemudahan yang ditawarkan oleh fitur tersebut tanpa menyadari biaya jangka panjangnya. Dan besok, mereka akan belajar bagaimana membangun sistem yang tidak hanya ramping di mata, tapi juga sehat di jantungnya.

## Bab 4: Kebijaksanaan Sang Arsitek (Vonis Devan)

Pagi harinya, suasana di ruang rapat terasa sedikit tegang. Jovian tampak gelisah, sementara Myesha sudah siap dengan tumpukan catatan tentang kegagalan tes dan tabrakan *state*. Devan berdiri di depan papan tulis putih, memegang spidol hitam dengan tenang.

"Oke, mari kita bicara jujur," buka Devan. "Aku sudah membaca artikel 'Why I Avoid PHP Traits' berkali-kali semalam. Penulisnya benar tentang satu hal besar: *Traits* sering kali digunakan sebagai tempat sampah bagi pengembang yang malas berpikir tentang desain objek yang benar."

Jovian menunduk, tapi Devan segera melanjutkan.

"Tapi," Devan menekankan kata itu, "aku merasa penulisnya juga sedikit terlalu ekstrem. Mengatakan bahwa *Traits* harus dihindari sepenuhnya sama saja dengan mengatakan kita harus membuang palu karena kita pernah memukul jari sendiri dengannya. Masalahnya bukan pada palunya, tapi pada kecenderungan kita untuk menganggap semua masalah adalah paku."

Devan menggambar sebuah diagram besar di papan tulis. Di satu sisi, ia menulis "Traits", dan di sisi lain "Composition".

"Kapan *Traits* menjadi racun?" tanya Devan retoris. "Satu: Ketika mereka menyimpan *state* atau variabel. Dua: Ketika mereka memiliki dependensi tersembunyi. Tiga: Ketika mereka berisi logika bisnis yang kompleks."

Ia kemudian menuliskan sebuah kode di papan tulis, versi yang lebih sehat dari apa yang sedang mereka kerjakan.

"Alih-alih `RespondsWithJson` sebagai *Trait*, kenapa kita tidak menggunakan sebuah *Response Factory* atau *Presenter*?" Devan menulis:

```php
class PaymentController {
    public function __construct(
        private PaymentService $paymentService,
        private JsonResponseFactory $response
    ) {}

    public function process(Request $request) {
        $result = $this->paymentService->handle($request->all());
        return $this->response->success($result);
    }
}
```

"Lihat perbedaannya?" Devan menoleh ke Jovian. "Di sini, `JsonResponseFactory` adalah objek nyata. Ia bisa dites sendiri. Ia bisa diinjeksikan. Ia tidak berbagi memori dengan *Controller*. Jika kita ingin mengubah cara kita merespons API, kita hanya perlu mengubah satu kelas, dan kontraknya jelas."

Jovian mengangguk pelan. "Tapi Kak, bagaimana dengan hal-hal kecil seperti `HasSlug` atau `SoftDeletes` di Laravel? Itu kan pakai *Traits* dan sangat membantu."

"Nah, di situlah letak nuansanya," jawab Devan sambil tersenyum. "*Traits* sangat bagus untuk apa yang aku sebut sebagai 'Horizontal Code Reuse' untuk hal-hal yang bersifat *boilerplate* teknis, bukan logika bisnis. `SoftDeletes` adalah contoh yang bagus karena ia bukan logika bisnis utama aplikasi kita; itu adalah fitur infrastruktur database. Ia tidak butuh dependensi luar yang rumit. Ia hanya menambahkan beberapa metode pembantu ke model."

Devan kemudian menjelaskan bahwa ada dua jenis *Traits*: *Behavioral Traits* dan *Service Traits*.

"Kita harus membuang semua *Service Traits*—yaitu *trait* yang sebenarnya adalah sebuah layanan tapi dipaksakan menjadi *trait* agar terlihat praktis. Kita harus menggantinya dengan *Composition* melalui *Dependency Injection*," tegas Devan.

"Dan untuk *Behavioral Traits*?" tanya Myesha.

"Kita simpan, tapi dengan aturan ketat," kata Devan. "Mereka harus *stateless* sebisa mungkin. Mereka tidak boleh tahu tentang dunia luar (seperti `Auth` atau `Session`). Mereka hanya boleh mengoperasikan data yang diberikan kepada mereka atau data yang memang dimiliki oleh kelas inang berdasarkan kontrak yang jelas."

Vonis Devan jelas: tim harus melakukan audit terhadap seluruh *Traits* mereka. Mana yang harus naik kelas menjadi *Service*, dan mana yang boleh tetap menjadi *Trait* sebagai asisten kecil yang tidak berbahaya. Ini adalah proses menyakitkan yang akan memakan waktu beberapa hari, tapi Devan tahu ini adalah harga yang harus dibayar untuk menebus utang teknis mereka.

Jovian mulai merasa lebih lega. Ia tidak merasa kodenya sampah, ia hanya merasa sekarang ia punya panduan yang lebih jelas tentang kapan harus menggunakan "keajaiban" dan kapan harus menggunakan "kerajinan tangan" yang lebih presisi.

"Ayo kita mulai refaktor dari `PaymentController`," ajak Jovian dengan semangat baru. "Aku ingin melihat bagaimana rasanya punya kode yang tidak hanya tipis, tapi juga kuat."

## Bab 5: Simfoni yang Harmonis (Refaktor dan Jalan Tengah)

Proses refaktor tidaklah mudah. Selama tiga hari berikutnya, kantor mereka dipenuhi dengan diskusi intens, perubahan ribuan baris kode, dan ribuan tes yang perlahan-lahan berubah dari merah menjadi hijau dengan cara yang lebih jujur.

Mereka mulai dengan membongkar `AuthenticatesUser`. Alih-alih sebuah *Trait*, mereka menciptakan sebuah *Contract* bernama `IdentityService`.

```php
interface IdentityService {
    public function getAuthenticatedUser(): User;
}

class SessionIdentityService implements IdentityService {
    public function getAuthenticatedUser(): User {
        return Auth::user() ?? throw new UnauthorizedException();
    }
}
```

Kini, di dalam `PaymentService`, mereka menyuntikkan layanan ini melalui konstruktor.

```php
class PaymentService {
    public function __construct(
        private IdentityService $identity,
        private PaymentGateway $gateway
    ) {}

    public function process($amount) {
        $user = $this->identity->getAuthenticatedUser();
        return $this->gateway->charge($user, $amount);
    }
}
```

Saat Myesha mencoba mengetesnya kembali, wajahnya tampak jauh lebih ceria. "Lihat ini, Jo! Aku bisa membuat `MockIdentityService` yang selalu mengembalikan *user* palsu tanpa harus menyentuh database atau sesi sama sekali. Tesnya berjalan dalam hitungan milidetik!"

Jovian pun melihat manfaatnya. Meskipun ia harus menulis sedikit lebih banyak kode di bagian konstruktor, ia tidak lagi pusing dengan tabrakan nama variabel atau metode. Semuanya terisolasi dengan rapi di dalam objeknya masing-masing.

Namun, mereka tidak membuang semua *Traits*. Mereka tetap menyimpan `InteractsWithTimestamps` dan menciptakan *Trait* baru bernama `HasLogPrefix` yang sangat sederhana, hanya mengembalikan string prefix berdasarkan nama kelas, tanpa menyimpan *state* apa pun.

"Jadi, kesimpulannya apa?" tanya Jovian saat mereka melakukan *deployment* terakhir di hari Jumat sore.

Devan menutup laptopnya dan berdiri. "Kesimpulannya adalah: *Traits* adalah alat untuk menyatukan *boilerplate*, bukan untuk menyatukan logika. Jika kamu merasa perlu menggunakan *Trait* untuk menyembunyikan kompleksitas, kemungkinan besar kamu sedang menyembunyikan masalah desain arsitektur."

Ia menepuk bahu Jovian. "Artikel di Dev.to itu benar bahwa *Traits* adalah jebakan. Tapi bagi mereka yang tahu cara memasang umpan dan menjaga jarak, ia tetap bisa menjadi alat yang berguna. Jangan membenci *Traits*, tapi jangan pernah mempercayai mereka dengan rahasia bisnismu."

Sore itu, Jakarta kembali diguyur hujan, tapi kali ini suaranya terdengar merdu di telinga tim. Mereka telah melewati badai arsitektural dan keluar sebagai tim yang lebih dewasa. Kode mereka kini bukan lagi sekadar barisan teks yang ramping, tapi sebuah simfoni yang harmonis antara kemudahan dan ketegasan arsitektur.

Hantu di dalam mesin itu telah pergi, digantikan oleh struktur yang kokoh dan transparan. Dan bagi seorang pengembang, tidak ada perasaan yang lebih melegakan daripada mengetahui bahwa setiap baris kode yang ia tulis hari ini tidak akan menjadi beban bagi dirinya di masa depan.

---

**Catatan Akhir:**
Mempelajari arsitektur adalah perjalanan tentang belajar kapan harus berkata "tidak" pada kemudahan. *Traits* memberikan godaan "DRY" yang instan, namun *Composition* memberikan ketenangan jangka panjang. Jika kamu sedang mempertimbangkan untuk membuat sebuah *Trait* baru besok pagi, berhentilah sejenak. Tanyakan pada dirimu: "Apakah ini benar-benar bagian dari perilaku objek ini, ataukah ini adalah sebuah layanan yang menyamar?"

Jawabanmu akan menentukan apakah kodenya akan menjadi warisan berharga atau justru menjadi hantu yang menghantuimu di malam hari.
