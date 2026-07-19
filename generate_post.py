import os

filepath = "_posts/2026-07-19-revolusi-wiki-llm-myesha-devan-jovian.md"

content = """---
title: "Revolusi LLM Wiki: Mengatasi Context Debt di Tengah Hujan Sleman"
subtitle: "Membangun sistem wiki persisten dari abu RAG dan log.md yang kacau."
date: 2026-07-19 13:30:00 +0700
categories: [engineering, architecture, ai]
tags: [wiki, llm, karpathy, design, obsidian, myesha, devan, jovian]
---

Kisah ini tentang bagaimana sebuah ide brilian dari Andrej Karpathy dirombak dan disempurnakan menjadi arsitektur _knowledge base_ tingkat lanjut yang siap menghadapi tantangan sistem skala besar. Di tengah gemuruh hujan di Sleman, tiga bersaudara—Myesha, Devan, dan Jovian—kembali memecahkan kebuntuan teknologi yang mengganggu produktivitas mereka.

## Chapter 1: Kekacauan di Kedai Kopi Sleman

Sore itu di Sleman, rintik hujan turun membasahi kaca jendela sebuah kedai kopi bergaya industrial tempat Devan sering menghabiskan akhir pekannya. Aroma kopi arabika yang disangrai dengan sempurna menguar di udara, berpadu dengan wangi tanah basah atau *petrichor* yang selalu membawa nuansa nostalgia. Namun, kedamaian suasana itu sama sekali tidak tercermin di wajah Devan. Pemuda yang selalu bertindak pragmatis ini tampak mengusap wajahnya dengan kasar, matanya menatap tajam ke arah layar laptop yang menampilkan aplikasi VS Code dengan tema gelap. 

Di layar tersebut, terbuka sebuah file bernama `log.md` yang berasal dari salah satu repositori kerjanya. File itu adalah sebuah monster. Angka di sebelah kiri layar menunjukkan bahwa file tersebut telah melampaui belasan ribu baris. Setiap kali Devan mencoba melakukan pencarian, laptopnya sedikit tersendat. Ini adalah catatan dari berbagai pengerjaan yang dia lakukan, mulai dari proyek `Terus-eLearning` hingga `Krenovator`.

"Kenapa setiap kali aku butuh konteks dari proyek bulan lalu, aku harus menggali tumpukan baris teks yang sama sekali tidak terstruktur ini?" gerutu Devan pelan, namun cukup keras untuk didengar oleh dirinya sendiri. Ia menyesap Americano dinginnya yang perlahan mulai kehilangan rasa. 

Selama ini, Devan sangat bergantung pada sistem *Retrieval-Augmented Generation* (RAG) konvensional untuk mengelola dan menanyakan informasi dari tumpukan catatannya kepada LLM (Large Language Model). Alurnya selalu sama: ia mengunggah koleksi file atau mengarahkan direktori, LLM akan memecah file menjadi beberapa *chunk*, mengambil bagian yang relevan saat ada *query*, lalu menghasilkan jawaban. 

Awalnya, metode ini terasa seperti sihir. Tapi seiring berjalannya waktu, Devan mulai menyadari kelemahan fatalnya. Setiap kali ia mengajukan pertanyaan yang kompleks—pertanyaan yang membutuhkan sintesis dari lima atau enam dokumen berbeda—LLM harus mencari dan menyusun kembali fragmen-fragmen itu dari awal. Tidak ada akumulasi pengetahuan. Pengetahuan hanya ditemukan kembali, dipakai sesaat, lalu dilupakan. 

"Ini seperti mempekerjakan seorang asisten super cerdas yang mengidap amnesia jangka pendek," batin Devan. Ia menamai masalah ini sebagai *Context Debt*—utang konteks. Semakin banyak proyek yang ia tangani secara paralel—Krenovator, Moodle-HQ, Terus-eLearning—semakin besar utang konteks yang harus ia bayar setiap kali berpindah konteks. LLM tidak pernah membangun pemahaman yang persisten. Tidak ada halaman referensi silang yang diperbarui, tidak ada *timeline* yang terhubung, semuanya hanya kumpulan teks mati yang menunggu dipanggil oleh algoritma *embedding*. Hatinya terasa lelah, seolah ia sedang membangun istana pasir yang selalu tersapu ombak setiap kali sesi _chat_ dengan LLM berakhir.

```bash path=null start=null
# Contoh pencarian yang membuat frustrasi
grep -rn "PDF export error" ~/Workspace/Terus-eLearning/dev-notes/
# Hasilnya: ratusan baris log dari berbagai hari tanpa konteks yang utuh
```

Devan menghela napas panjang. Ia butuh solusi. Ia butuh sistem di mana pengetahuannya tidak hanya sekadar disimpan, tetapi dirawat, dihubungkan, dan dikembangkan seiring berjalannya waktu.

## Chapter 2: Dik Jovian dan "Kitab Suci" Karpathy

Suara lonceng di atas pintu kedai kopi bergemerincing. Jovian, adik bungsu mereka yang selalu up-to-date dengan tren teknologi terbaru, masuk sambil mengibaskan sisa air hujan dari payungnya. Berbeda dengan Devan yang sedang stres berat, wajah Jovian tampak berseri-seri penuh semangat. Ia mengenakan hoodie hitam kebesarannya dan langsung duduk di hadapan Devan.

"Bang Devan! Wajahmu kusut banget kayak server *down* pas *flash sale* akhir tahun," goda Jovian sambil tertawa kecil. Ia segera memesan Iced Latte melalui kode QR di meja.

Devan hanya tersenyum kecut. "Aku lagi krisis *knowledge management*, Dik. Sistem notes dan RAG yang kubangun ini malah bikin aku kerja dua kali. Semua file log.md dari proyek Krenovator dan Terus-eLearning kecampur aduk dan ukurannya udah nggak masuk akal."

Mendengar itu, mata Jovian langsung berbinar. Ia mengeluarkan laptop stikernya dengan antusias. "Bang, kamu masih terjebak di era RAG transien! Kamu belum baca *gist* viral dari Andrej Karpathy bulan April 2026 kemarin? Dunia udah bergerak ke LLM Wiki, Bang!"

Devan mengernyitkan dahi. "LLM Wiki? Sama kayak Wikipedia biasa?"

"Bukan!" seru Jovian. "Konsep dari Karpathy ini benar-benar membalik cara kita menggunakan LLM. Kebanyakan orang menggunakan LLM seperti *search engine* canggih lewat RAG. Karpathy bilang, kita harus menggunakan LLM sebagai *compiler*. Daripada menyuruh LLM mencari potongan teks mentah setiap kali kita nanya, kita suruh LLM membangun dan merawat sebuah *wiki* secara inkremental!"

Jovian memutar layar laptopnya, menunjukkan sebuah dokumen Markdown dari *gist* Andrej Karpathy. "Ini adalah 'Kitab Suci' baru untuk agen AI. Karpathy membaginya menjadi tiga lapis arsitektur. Pertama, **Raw sources**—ini adalah file mentah kita, PDF, artikel, log *meeting*. Sifatnya *immutable*, nggak boleh diubah. Kedua, **The wiki**—direktori berisi file Markdown yang di-generate oleh LLM. Ketiga, **The schema**—file seperti `CLAUDE.md` atau `AGENTS.md` yang berisi aturan main untuk si agen LLM."

Jovian menenggak lattes-nya sejenak. "Jadi begini cara kerjanya, Bang. Ada tiga operasi utama: *Ingest*, *Query*, dan *Lint*. Waktu Abang masukin dokumen baru, LLM nggak cuma *indexing* buat nanti dicari. LLM akan membaca dokumen itu, mengekstrak informasi kuncinya, membuat halaman ringkasan, memperbarui halaman entitas terkait, mencatat kontradiksi dengan data lama, dan menambah log aktivitas. Pengetahuan itu *di-compile* sekali, lalu dirawat. Referensi silangnya otomatis terbangun!"

```markdown path=null start=null
# Contoh log.md milik Karpathy
## [2026-06-18] ingest | Analysis of the PDF error
- Memperbarui halaman [[PDF Export]]
- Mengubah asumsi pada [[Report Generation]]
```

"Karpathy menggunakan dua file sakti untuk navigasi," lanjut Jovian, jarinya menunjuk-nunjuk layar. "`index.md` sebagai katalog orientasi konten, dan `log.md` sebagai rekaman kronologis *append-only*. Jadi, waktu kita *Query*, LLM tinggal baca *index* dan *synthesize* jawaban dari halaman wiki yang udah jadi, bukan dari raw dokumen yang masih mentah. Kalau jawabannya bagus, LLM akan otomatis *file back* jawaban itu jadi halaman baru di Wiki!"

Devan menatap layar itu dengan saksama. Hatinya yang tadi mendung kini sedikit terang. Konsep ini brilian. Ia tidak lagi harus berurusan dengan memori LLM yang amnesia. Pengetahuannya akan *compounding*—berakumulasi seperti bunga majemuk di bank. Tapi, saat matanya terpaku pada bagian `index.md` dan `log.md` dari Karpathy, insting *engineering* Devan menyala. Ia menyadari ada celah yang bersembunyi di balik sistem tersebut jika diterapkan pada skalanya.

## Chapter 3: Kak Myesha Memecah Kebuntuan

Tepat saat Devan sedang memikirkan kelemahan sistem Karpathy, sebuah suara lembut dan penuh wibawa menyapa mereka. "Seru sekali diskusinya. Boleh Kakak ikut bergabung?"

Myesha, sang kakak perempuan, berdiri di sana dengan senyum hangat khasnya. Ia baru saja tiba dari sebuah pertemuan di pusat kota Yogyakarta. Penampilannya rapi namun tetap kasual, memancarkan aura kebijaksanaan seorang *senior architect* yang sudah malang melintang menghadapi berbagai badai sistem IT. Myesha memesan secangkir teh *chamomile* hangat untuk mengusir hawa dingin Sleman.

"Kak Myesha!" sapa Jovian semangat. "Ini lho, aku lagi jelasin konsep LLM Wiki dari Andrej Karpathy ke Bang Devan. Keren banget kan, Kak?"

Myesha duduk, menyesap tehnya perlahan, lalu menatap layar laptop Jovian. Matanya yang tajam langsung menangkap esensi dari dokumen tersebut. Ia mengangguk pelan. "Ide Karpathy ini sangat revolusioner, Dik Jovian. Mengubah paradigma LLM dari sekadar pembaca menjadi penulis dan perawat *knowledge base*. Ini memecahkan masalah utang konteks yang Devan keluhkan."

Myesha beralih menatap Devan. "Tapi Kakak lihat dari ekspresimu, Dev, kamu merasa ada yang kurang pas?"

Devan tersenyum tipis. Kakaknya memang selalu bisa membaca pikirannya. "Benar, Kak. Konsep Karpathy menggunakan satu file `log.md` global dan satu `index.md` global. Untuk riset personal pada satu topik, pendekatan ini sempurna. Tapi aku memegang banyak proyek sekaligus, Kak. Moodle-HQ, Krenovator, Terus-eLearning, dan proyek pribadiku. Kalau aku memusatkan semuanya pada satu `log.md` dan satu `index.md`, dalam beberapa bulan file itu akan jadi raksasa yang nggak bisa di-*maintain*. Persis seperti masalah awalku."

Myesha mengangguk setuju. "Tepat sekali. Di dunia korporat atau untuk pekerjaan *multi-project*, satu file indeks global adalah sebuah *bottleneck*. Itu akan menciptakan konflik saat terjadi pembaruan paralel, dan mengaburkan batas antara proyek yang satu dengan yang lain."

Myesha mengeluarkan tabletnya dan mulai menggambar sesuatu di layar. "Kita tidak boleh menelan mentah-mentah sistem Karpathy. Kita harus mengadaptasinya. Masalah utamamu, Devan, adalah kamu memiliki *wiki root* yang terpisah-pisah untuk setiap *workspace*, dan sebuah file `log.md` datar yang mencampur aduk segalanya. Kita harus menyatukannya, namun dengan struktur yang jelas."

Myesha menunjukkan sketsa desain terbarunya. Desain itu berjudul `Design spec for the Company/Project wiki system`. 

"Dengar baik-baik," ucap Myesha dengan nada serius namun merangkul. "Mulai sekarang, *Root* dari wiki kita hanya ada satu: `/Users/wenkhairu/Documents/Wiki/`. Ini menggantikan semua *routing* per-workspace lama yang tersebar di komputer. Kita tidak akan memigrasikan log lama yang kacau. Kita mulai dari lembaran baru."

## Chapter 4: Arsitektur Baru yang Menyembuhkan

Myesha mulai menjabarkan arsitekturnya dengan detail yang membuat Devan dan Jovian terpukau. Ini bukan sekadar teori, melainkan sebuah rekayasa struktur data yang memperhitungkan skalabilitas dan kemudahan navigasi.

"Intensi kita adalah menggabungkan navigasi dan *work log* menjadi satu artefak. Kita membunuh ide `log.md` global," kata Myesha mantap. "Struktur utamanya adalah *Company* yang diikuti oleh *Project*. *Company* diambil langsung dari path *workspace* kamu. Kalau kamu sedang bekerja di `~/Workspace/Terus-eLearning/howc/moodle-5/...`, maka Company adalah `Terus-eLearning`, dan Project adalah direktori pertama di bawahnya, yaitu `howc`."

"Kalau kerjaan *ad-hoc* atau nulis *script* doang gimana, Kak?" tanya Jovian kritis.

"Masukkan ke dalam `Personal/<short-topic>/`," jawab Myesha cepat. "Jangan pernah membuat *bucket* aneh bernama 'no project'. Semuanya harus masuk ke dalam sebuah *project slot*."

Myesha lalu menjelaskan tata letak filenya. "Di Root, kita punya `index.md` yang sifatnya murni navigasi. Tidak ada tanggal di sini. Hanya *link* dari Company ke Project. Kecil, dan jarang bertambah panjang."

```markdown path=null start=null
# Contoh Root index.md
- Krenovator
  - [[Krenovator/inventory-ai-web/index]]
- Terus-eLearning
  - [[Terus-eLearning/howc/index]]
- Personal
  - [[Personal/dotfiles/index]]
```

"Nah, keajaibannya ada di level *Project*," Myesha tersenyum. "File `<Company>/<Project>/index.md` adalah pengganti `log.md` milik Karpathy. File ini adalah gabungan antara *TOC* (Daftar Isi) dan *log* harian untuk satu proyek tertentu. Ini *lean*, sangat ramping. Hanya H1, lalu *heading* berisi tanggal `YYYY-MM-DD`, dan di bawahnya adalah *link* ke halaman detail."

Devan terbelalak. "Tunggu, Kak. Lalu teks untuk *link*-nya apa? Bikin ringkasan manual lagi?"

"Tidak, Dev," Myesha menggelengkan jarinya. "Teks untuk *link* tersebut diambil persis dari *value* `Summary` yang ada di *frontmatter* halaman detailnya. Satu sumber kebenaran, digunakan di dua tempat."

Myesha kemudian menuliskan spesifikasi mutlak untuk *Frontmatter* di setiap halaman Wiki. Ini adalah pondasi agar LLM agen mereka tidak berhalusinasi dan tetap terstruktur.

```yaml path=null start=null
---
title: Human-readable title
Summary: A short summary that represents this page at a glance
Tags:
  - best-practices
Created At: 2026-07-19T05:24:41
Last Updated: 2026-07-19T06:38:41
Sources:
  - "[[raw/source-name]]"
Related:
  - "[[Terus-eLearning/howc/other-page]]"
---
```

Myesha menjelaskan aturannya bagai seorang dosen yang sedang menguji mahasiswanya. "Waktu pembuatan harus menggunakan *wall-clock time* yang nyata, misalnya `2026-05-20T08:07:08`, jangan pernah menggunakan format palsu seperti `T00:00:00`. *Tags* harus *lowercase* dan dipisah dengan tanda hubung. Dan yang terpenting: *Wikilinks* di dalam frontmatter harus diapit tanda kutip ganda!"

Jovian mengangguk-angguk paham. "Dan untuk referensi silangnya, Kak?"

"Aturannya ketat," tegas Myesha. "Pertama, tautan dua arah wajib hukumnya. Jika halaman A menunjuk halaman B di `Related`, halaman B harus memuat A. Kedua, konsep abstrak mendapatkan halamannya sendiri *hanya* jika ia muncul di tiga atau lebih halaman berbeda. Jika konsep itu lahir, letakkan di proyek yang paling relevan atau di `Personal/<concept-name>`. Dengan begini, LLM agen kita akan terus merangkai graf pengetahuan tanpa duplikasi."

Terakhir, Myesha membahas visualisasi. "Karena kita manusia yang butuh gambaran visual, ketika sebuah halaman butuh diagram—seperti *flowchart* atau diagram arsitektur—kita tidak boleh lagi menggunakan *ASCII art* yang rentan rusak. Gunakan **Mermaid** *fenced block*."

```mermaid path=null start=null
flowchart LR
  A[Raw Source] --> B{Agent Ingest}
  B -->|Summarize| C[Project Index]
  B -->|Extract| D[Entity Pages]
  C --> E(Knowledge Base)
  D --> E
```

Devan menyandarkan punggungnya di kursi. Beban berat yang sejak tadi menekan dadanya seakan menguap begitu saja. Desain Myesha ini memecahkan segalanya. Menyempurnakan ide brilian Karpathy dengan struktur taksonomi hierarkis yang mutlak diperlukan untuk mengelola proyek berskala besar.

## Chapter 5: Menyatu dalam Harmoni

Mendengar penjelasan mendalam dari Kak Myesha, Devan langsung membuka kembali editor kodenya. Dengan energi yang baru, ia segera merombak file `CLAUDE.md` miliknya untuk mengintegrasikan skema arsitektur baru ini. Jovian membantunya mengonfigurasi skrip otomatisasi awal untuk inisialisasi folder `/Users/wenkhairu/Documents/Wiki/`.

Ketiga kakak beradik itu tenggelam dalam pekerjaan mereka selama beberapa saat. Suara ketikan *keyboard* beradu harmonis dengan ritme hujan di luar sana. Terdapat perasaan magis ketika melihat alat-alat teknologi canggih seperti LLM akhirnya tunduk pada struktur logis dan terorganisir yang dibangun oleh nalar manusia.

Devan mencoba melakukan instruksi *ingest* pada sebuah dokumen spesifikasi lama dari proyek `inventory-ai-web` miliknya. Dalam hitungan detik, agen LLM di komputernya membaca file mentah tersebut, mengekstrak esensinya, memperbarui `Krenovator/inventory-ai-web/index.md` dengan tanggal hari ini `2026-07-19`, dan membuat tautan lintas-halaman dengan sangat rapi. Pengetahuannya kini memiliki rumah permanen yang tertata apik, tidak ada lagi file log global raksasa yang menyiksa memori laptopnya. 

"Berhasil, Kak!" seru Devan lega. "Konteks proyekku sekarang hidup dan punya *timeline* masing-masing per-proyek. LLM-nya berjalan lancar membangun jaringan pengetahuannya sendiri sesuai skema yang Kakak buat."

Jovian menepuk bahu abangnya. "Gitu dong, Bang! Sekarang kalau kita lagi jalan-jalan ke Krui buat nengok kampung halaman Ibu, atau mudik ke Takengon, Abang nggak perlu lagi pusing nyari catetan proyek."

Myesha tersenyum lembut, menyeruput sisa teh *chamomile* miliknya. "Teknologi AI seperti LLM memang memiliki potensi yang luar biasa besar, Devan, Jovian. Tapi mereka tetap butuh arahan, batasan, dan arsitektur yang bijaksana agar potensinya benar-benar bisa dimanfaatkan. Sama seperti sebuah rumah, sebagus apa pun perabotannya, tanpa fondasi yang kuat, semuanya akan berantakan."

Di luar jendela kedai kopi di Sleman itu, hujan akhirnya mereda. Awan kelabu mulai menyingkir, membiarkan bias cahaya senja keemasan menyelinap masuk menerangi meja mereka. Utang konteks yang menghantui Devan telah dibayar lunas. Berkat "Kitab Suci" Karpathy yang diretas dengan kearifan struktural Myesha, serta semangat eksplorasi Jovian, ketiganya kembali membuktikan bahwa tidak ada masalah teknologi yang tidak bisa diselesaikan jika mereka memikirkannya bersama-sama sebagai sebuah keluarga.
"""

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

