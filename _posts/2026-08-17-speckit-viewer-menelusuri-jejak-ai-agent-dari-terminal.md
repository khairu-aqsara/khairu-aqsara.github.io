---
layout: post
title: "speckit-viewer: Menelusuri Jejak AI Agent dari Terminal"
subtitle: "Kisah Devan, Myesha, dan Jovian membuat dashboard dua pane untuk membaca artefak GitHub Spec Kit tanpa meninggalkan terminal."
date: 2026-08-17 21:30:00 +0700
categories: [AI, Engineering, Go, Story]
tags: [github-spec-kit, ai-agent, spec-driven-development, go, bubble-tea, tui, terminal, developer-tools]
author: Kuli Kode
---

Ada masa ketika terminal terasa seperti rumah sendiri. Devan bisa bekerja berjam-jam di sana tanpa merasa membutuhkan jendela lain. Ia membuka editor, menjalankan test, membaca log, membuat branch, menjalankan command dari dokumentasi, lalu kembali menulis kode. Semua terasa dekat. Semua terasa cepat.

Masalahnya muncul ketika AI Agent mulai ikut bekerja di dalam rumah itu.

AI Agent dapat membaca repository, membuat rencana, menulis spesifikasi, memecah pekerjaan menjadi task, lalu mengubah banyak file dalam satu rangkaian kerja. [GitHub Spec Kit](https://github.com/github/spec-kit) membantu memberi bentuk pada rangkaian tersebut. Artefaknya disimpan sebagai file Markdown yang dapat dibaca manusia dan agent. Secara konsep, semuanya terasa rapi.

Namun, ketika Devan benar-benar bekerja dari terminal, kerapian itu tidak selalu mudah dilihat. Ia harus berpindah dari satu file ke file lain. Ia harus mengingat folder feature. Ia harus mencari `spec.md`, membuka `plan.md`, membaca `tasks.md`, lalu menghitung sendiri berapa task yang telah selesai. Kalau proyek sudah memiliki banyak feature, terminal yang awalnya terasa seperti rumah berubah menjadi lorong panjang dengan terlalu banyak pintu.

Dari rasa lelah itulah [`speckit-viewer`](https://github.com/khairu-aqsara/speckit-viewer) dibuat. Bukan untuk menggantikan GitHub Spec Kit. Bukan juga untuk menjalankan agent baru. Alat ini hanya ingin memberi peta pada artefak yang sudah ada, supaya Devan bisa memahami posisi setiap feature tanpa meninggalkan terminal.

## Bab 1: Terminal yang Penuh Jejak tetapi Tidak Punya Peta

Malam di Sleman berjalan pelan. Hujan baru saja berhenti, tetapi air masih menetes dari ujung atap dan jatuh ke halaman dengan suara teratur. Devan duduk di depan laptop dengan terminal memenuhi layar. Di sisi kiri ada editor berbasis terminal. Di sisi kanan ada beberapa tab shell. Satu tab menjalankan test. Satu tab menyimpan output dari AI Agent. Tab lain menunggu command berikutnya.

Ia baru saja meminta agent membantu membangun sebuah feature. Permintaannya tidak rumit jika dibaca sebagai kalimat. Ia ingin menambahkan alur persetujuan untuk sebuah aplikasi internal. Agent kemudian membuat beberapa dokumen. Ada spesifikasi kebutuhan. Ada rencana implementasi. Ada model data. Ada catatan riset. Ada daftar task. Semua dokumen tersebut berada di dalam folder feature yang memiliki nomor dan nama kebab-case.

Devan senang melihat hasilnya. Setidaknya, agent tidak langsung menulis kode tanpa menjelaskan arah. File-file Markdown itu memberi kesempatan untuk memeriksa keputusan sebelum implementasi berjalan terlalu jauh. Masalahnya baru terasa ketika ia ingin menelusuri semua dokumen tersebut.

Ia mulai dengan command sederhana.

```bash
find specs -maxdepth 2 -type f | sort
```

Terminal mencetak banyak nama file. Devan memperbesar ukuran jendela, lalu mencoba membaca daftar tersebut. Ia menemukan `spec.md` dari satu feature, kemudian `plan.md` dari feature lain, lalu kembali ke `tasks.md` dari feature pertama. Matanya mulai melakukan pekerjaan yang seharusnya dapat dibantu oleh alat.

"Aku cuma mau tahu feature ini sedang berada di tahap apa," gumam Devan.

Myesha datang dari dapur membawa teh hangat. Kakaknya tidak langsung duduk. Ia berdiri di belakang kursi Devan dan membaca sebagian output terminal yang bergerak terlalu cepat.

"Bang, tahapnya sudah ditulis di file?" tanya Myesha.

"Tidak benar-benar," jawab Devan. "Ada file yang tersedia, ada checkbox di `tasks.md`, tapi tidak ada field status yang bisa kubaca langsung. Aku harus menyimpulkan sendiri. Kalau `spec.md` ada, mungkin baru specified. Kalau sudah ada `plan.md`, berarti planned. Kalau task mulai dicentang, berarti implementing. Kalau semua selesai, berarti implemented."

Jovian masuk sambil membawa kabel charger. Ia mendengar bagian terakhir dari percakapan itu.

"Jadi statusnya seperti menebak apakah orang sudah makan hanya dari piring dan sendok yang ada di meja?" tanya Jovian.

Myesha tersenyum. "Kurang lebih begitu, Dik. Kita tidak menemukan label status yang pasti. Kita melihat bukti yang tersedia, lalu membuat kesimpulan yang berguna."

Devan memutar laptopnya sedikit agar kedua saudaranya bisa melihat. Ia membuka folder hasil kerja agent.

```text
specs/
├── 003-payroll/
│   ├── spec.md
│   ├── plan.md
│   ├── research.md
│   ├── data-model.md
│   ├── tasks.md
│   ├── quickstart.md
│   ├── checklists/
│   │   └── requirements.md
│   └── contracts/
│       └── payslip.md
└── 007-trivial-toggle/
    └── spec.md
```

"Struktur seperti ini sebenarnya enak," kata Devan. "Semua keputusan agent tidak hilang di chat. Tapi ketika aku membukanya dari terminal biasa, aku harus memahami folder ini sebagai satu sistem. Aku harus tahu feature mana, file mana, dan status mana."

Myesha menarik kursi dan duduk di sampingnya. Ia selalu tahu bahwa keluhan Devan sering membawa pertanyaan desain yang lebih besar. Devan bukan sedang mengeluh karena Markdown sulit dibaca. Ia sedang berhadapan dengan masalah navigasi.

"Kalau setiap feature punya banyak artefak, kita perlu melihatnya sebagai satu unit," kata Myesha. "Jangan mulai dari file. Mulai dari feature. Tampilkan feature, tampilkan fase yang dapat disimpulkan, lalu izinkan kita membuka artefaknya."

Kalimat itu membuat Devan berhenti mengetik. Ia membuka catatan kecil dan menulis beberapa baris.

```text
project root
    -> scan specs/
    -> group files by feature
    -> infer workflow phase
    -> show feature dashboard
    -> browse artifacts
```

"Itu bukan file browser biasa," kata Jovian sambil menunjuk catatan tersebut. "File browser hanya bertanya file mana yang mau dibuka. Ini bertanya feature mana yang sedang dikerjakan dan bukti apa yang tersedia."

Devan mengangguk. Ia mulai melihat masalahnya dengan bentuk yang berbeda. Selama ini ia menganggap kesulitan tersebut sebagai persoalan membuka terlalu banyak file. Padahal, yang hilang adalah model mental. GitHub Spec Kit mengubah proses pengembangan menjadi kumpulan artefak yang saling berhubungan. `spec.md` bukan file acak. Ia menjelaskan kebutuhan. `plan.md` mengubah kebutuhan menjadi arah teknis. `tasks.md` memecah arah tersebut menjadi pekerjaan. `research.md`, `data-model.md`, `quickstart.md`, checklist, dan contract memberi konteks tambahan.

Jika semua file itu dibaca satu per satu tanpa navigasi yang memahami hubungan mereka, Devan tetap dapat melihat teksnya, tetapi ia kehilangan cerita besarnya.

Di situlah AI Agent membuat persoalan ini terasa lebih kuat. Ketika manusia menulis satu file dalam satu sesi, ia mungkin masih ingat alasannya. Ketika agent membuat atau mengubah beberapa artefak, konteksnya bisa tersebar di command, output, commit, dan dokumen. Devan perlu cara untuk memeriksa hasil kerja agent sebagai satu proses.

Myesha mengambil kertas dari meja. Ia menggambar dua kolom.

| Cara lama | Cara yang dibutuhkan Devan |
|---|---|
| Mencari semua Markdown | Melihat semua feature |
| Membuka file satu per satu | Membuka artefak dari feature terpilih |
| Menghitung checkbox manual | Melihat progress task |
| Menebak fase dari folder | Melihat fase hasil inferensi |
| Berpindah antar command | Tetap berada di terminal |

"Yang kita buat tidak perlu memiliki semua kemampuan IDE," ujar Myesha. "Ia harus menyelesaikan satu rasa sakit dengan baik."

Devan kembali melihat terminal. Ia memakai terminal bukan karena tidak menyukai interface grafis. Ia memakai terminal karena sebagian besar pekerjaannya sudah berada di sana. Git, test, log, editor, command dari agent, dan tools lain sudah berjalan melalui keyboard. Jika ia harus membuka aplikasi tambahan hanya untuk membaca progress Spec Kit, alurnya terputus.

Rasa terputus itu bukan hanya soal dua detik tambahan. Ketika seseorang sedang membaca rencana agent, perhatian berada pada urutan keputusan. Membuka aplikasi lain, mencari repository, memilih folder, dan menunggu index dapat memindahkan perhatian ke hal lain. Setelah kembali, seseorang mungkin masih melihat file yang sama, tetapi tidak lagi memiliki pertanyaan yang sama.

"Berarti targetnya bukan membuat tampilan paling indah," kata Devan. "Targetnya menjaga konteks tetap dekat dengan tempat kerja."

"Betul," jawab Myesha. "Dan karena kamu bekerja dari terminal, tampilan terminal bukan kompromi. Itu adalah konteks utama."

Malam itu Devan membuat repository baru di dalam folder eksperimen.

```bash
mkdir speckit-viewer
cd speckit-viewer
go mod init github.com/wenkhairu/speckit-viewer
```

Ia memilih nama `speckit-viewer` karena nama tersebut mengatakan pekerjaan alat ini dengan cukup jujur. `speckit` adalah domain artefaknya. `viewer` adalah batasnya. Alat ini melihat, merender, dan membantu navigasi. Ia tidak mengaku sebagai engine Spec Kit. Ia tidak mengaku sebagai orchestrator AI Agent.

Jovian menatap nama repository itu.

"Kalau nanti alatnya bisa mengubah task, namanya masih viewer?" tanyanya.

Devan terdiam. Pertanyaan kecil itu membuka godaan besar. Ia memang dapat membayangkan tombol untuk mencentang task. Ia dapat membayangkan editor Markdown. Ia dapat membayangkan command untuk menjalankan agent. Ia bahkan dapat membayangkan sinkronisasi status dengan issue tracker.

Myesha mengangkat alis.

"Jangan masukkan semua kemungkinan ke versi pertama," katanya. "Kalau alat ini mulai mengubah file, tanggung jawabnya berubah. Kalau ia menjalankan agent, risiko dan scope-nya berubah lagi. Kita mulai dari membaca."

Devan menulis batas tersebut di README yang masih kosong.

```text
speckit-viewer reads a Spec Kit project and presents its artifacts in a
terminal dashboard. It does not run an AI Agent and it does not replace
the Spec Kit workflow.
```

Kalimat itu menjadi pagar pertama. Pagar tersebut penting karena AI tooling mudah bertumbuh ke banyak arah. Setiap kali seseorang melihat artefak yang dapat dibaca, muncul keinginan untuk mengeditnya. Setiap kali melihat task yang belum selesai, muncul keinginan untuk menjalankannya. Namun, kebutuhan awal Devan lebih sederhana: ia ingin memahami apa yang sudah dibuat agent sebelum memutuskan tindakan berikutnya.

Di sini ada pelajaran yang sering terlupakan ketika membangun alat untuk developer. Masalah utama bukan selalu kurangnya data. Sering kali data sudah ada dalam jumlah berlimpah. Yang kurang adalah susunan yang membantu manusia menjawab pertanyaan berikutnya.

Pertanyaan Devan malam itu tidak berbunyi, "Tampilkan semua file." Pertanyaannya berbunyi, "Feature ini sudah sampai mana, dokumen apa yang menjadi buktinya, dan di mana aku harus membaca lebih lanjut?"

Itulah alasan `speckit-viewer` lahir. Ia lahir bukan karena terminal tidak mampu membuka Markdown. Terminal sangat mampu. Ia lahir karena manusia perlu melihat hubungan antarfile tanpa kehilangan alur kerja yang sudah mereka pilih.

Sebelum tidur, Devan menutup beberapa tab terminal yang tidak lagi diperlukan. Ia belum memiliki dashboard. Ia belum memiliki parser. Ia bahkan belum memiliki satu baris UI. Tetapi ia sudah memiliki masalah yang lebih jelas.

Myesha mematikan lampu dapur. "Besok mulai dari bentuk datanya," katanya. "Kalau modelnya benar, tampilan akan punya tempat untuk berdiri."

Jovian menguap. "Kalau modelnya salah?"

"Kita akan melihatnya lebih cepat," jawab Myesha.

Di layar laptop, repository baru itu hanya memiliki `go.mod` dan README pendek. Tidak ada yang tampak mengesankan. Namun, di dalam keheningan terminal, Devan merasa lebih tenang. Untuk pertama kalinya, kesulitan menelusuri pekerjaan AI Agent tidak lagi hanya berupa rasa pusing. Ia sudah berubah menjadi masalah yang dapat dipetakan.

Ia lalu mencoba menjelaskan rasa pusing tersebut dengan lebih tepat. Selama ini ia sering menyebutnya sebagai "terlalu banyak file", tetapi jumlah file bukan satu-satunya masalah. Dalam project kecil, sepuluh file dapat terasa ringan jika hubungan antarfile jelas. Dalam project yang lebih besar, empat file dapat terasa berat jika setiap file harus ditemukan melalui pencarian manual.

Masalahnya juga bukan karena Devan tidak tahu command. Ia tahu `find`, `rg`, `less`, `git log`, dan editor yang dapat membuka file dengan cepat. Ia dapat merangkai pipeline shell untuk menemukan semua `tasks.md`. Ia bahkan dapat membuat script kecil untuk menghitung checkbox. Tetapi setiap command hanya menjawab satu bagian pertanyaan. Satu command menemukan file. Command berikutnya membuka isi. Command lain menghitung progress. Setelah itu, Devan masih harus mengingat hubungan hasil command tadi dengan feature yang sedang ia periksa.

AI Agent memperbesar beban tersebut karena agent dapat menghasilkan banyak artefak dalam satu sesi. Saat manusia menulis dokumen secara perlahan, perubahan konteks biasanya dapat diingat. Saat agent menghasilkan `spec.md`, `plan.md`, `research.md`, dan `tasks.md` dalam rangkaian command, pemilik project perlu membaca kembali semua artefak itu dengan mata yang segar. Ia perlu memastikan bahwa rencana memang berasal dari kebutuhan, task memang berasal dari rencana, dan keputusan riset tidak hilang di tengah perpindahan file.

Ada juga rasa cemas yang lebih halus. Ketika agent berkata bahwa sebuah feature sudah direncanakan, Devan ingin tahu bukti yang mendukung kalimat tersebut. Ketika agent berkata beberapa pekerjaan sudah selesai, ia ingin melihat task mana yang dicentang. Ia tidak ingin menerima kesimpulan sebagai kotak hitam. Ia ingin melihat jalurnya kembali ke Markdown.

"Jadi viewer harus memberi ringkasan, tetapi ringkasan itu harus selalu punya pintu menuju sumbernya," kata Devan.

Myesha mengangguk. "Ringkasan tanpa sumber mudah menjadi laporan. Ringkasan dengan sumber bisa menjadi navigasi."

Perbedaan antara laporan dan navigasi menjadi salah satu batas desain yang paling penting. Laporan biasanya berhenti pada kesimpulan. Navigasi membantu seseorang bergerak dari kesimpulan menuju detail. Dashboard `speckit-viewer` tidak hanya menulis `Implementing 3/6`. Pengguna dapat menekan Enter, memperluas feature, membuka `tasks.md`, dan membaca enam task tersebut.

Devan menulis daftar non-goal agar ide yang datang belakangan tidak menggeser tujuan pertama.

```text
Non-goal untuk MVP:
- menjalankan AI Agent
- mengedit artefak Spec Kit
- mengubah checkbox dari viewer
- menyimpan status tambahan di database
- menjadi pengganti editor kode
- menyinkronkan status dengan issue tracker
```

Daftar itu tidak berarti semua ide tersebut buruk. Beberapa mungkin berguna pada masa depan. Namun, masing-masing akan membawa model permission dan sumber kebenaran yang baru. Jika viewer dapat mengubah checkbox, pengguna perlu tahu siapa yang mengubah file. Jika viewer menyimpan status di database, status tersebut dapat berbeda dari isi Markdown. Jika viewer menjalankan agent, viewer tidak lagi hanya bertanggung jawab atas pembacaan.

Jovian melihat daftar itu lalu tertawa kecil. "Non-goal lebih panjang daripada goal."

"Itu normal," jawab Myesha. "Batas yang tidak ditulis akan mudah dilupakan ketika kita sedang bersemangat."

Devan teringat beberapa project lain yang pernah ia buat. Banyak project dimulai dari satu masalah yang jujur, lalu melebar karena developer ingin menjawab semua kemungkinan. Pada akhirnya, feature awal memang ada, tetapi pengalaman utamanya menjadi berat. Ia tidak ingin `speckit-viewer` berubah menjadi platform manajemen project yang kebetulan berjalan di terminal.

Ia ingin pengguna dapat menjalankan satu command, melihat feature, membaca artefak, lalu kembali ke pekerjaan utama. Jika seseorang perlu memeriksa kode, mereka masih dapat berpindah ke editor. Jika seseorang perlu meminta agent melanjutkan pekerjaan, mereka masih dapat memakai tool agent. Viewer hanya menjaga tahap memahami tetap ringan.

Setelah daftar non-goal selesai, Devan membuat beberapa pertanyaan penerimaan.

```text
1. Apakah project root tanpa specs/ memberi pesan yang membantu?
2. Apakah feature dengan hanya spec.md tetap terlihat?
3. Apakah file tambahan membuat scanner gagal?
4. Apakah pengguna dapat bergerak dari feature ke artefaknya?
5. Apakah progress task dapat diperiksa tanpa menghitung manual?
6. Apakah isi Markdown tetap dapat dibaca dalam bentuk aslinya?
```

Pertanyaan tersebut menjaga fokus mereka ketika mulai menulis kode. Ia juga membuat tujuan MVP dapat diuji oleh orang lain. Devan tidak perlu berkata bahwa viewer "terasa lebih baik" tanpa menjelaskan alasannya. Ia dapat menunjukkan alur yang harus bekerja.

Malam itu, mereka membicarakan perbedaan antara bekerja dengan browser dan bekerja dari terminal. Browser menawarkan ruang visual yang luas. Ia cocok untuk banyak informasi yang harus terlihat bersamaan. Terminal menawarkan kedekatan dengan process dan file. Ia cocok ketika pengguna ingin menggabungkan membaca, menjalankan, dan mengubah project dalam satu lingkungan.

Tidak ada interface yang selalu lebih baik. Ada konteks yang berbeda. Devan tidak sedang mencoba meyakinkan semua orang untuk memakai terminal. Ia sedang mengakui cara kerjanya sendiri. Karena sebagian besar pekerjaannya sudah berada di terminal, alat pembaca Spec Kit juga harus hadir di sana.

Myesha mengambil contoh lain. Ketika agent sedang berjalan dalam satu tab, Devan dapat membuka tab lain untuk viewer. Ia dapat memeriksa progress tanpa menghentikan agent. Jika ada dokumen yang belum sesuai, ia dapat kembali ke output agent atau editor dengan konteks yang masih dekat. Tidak ada proses ekspor, upload, atau import.

"Ini seperti menaruh jendela di ruangan yang sama," kata Myesha. "Bukan membangun rumah baru untuk melihat apa yang sedang terjadi di rumah lama."

Analogi itu menguatkan pilihan mereka. `speckit-viewer` bukan portal terpisah. Ia adalah jendela terminal pada repository yang sedang dikerjakan. Karena itu, path relatif dan breadcrumb menjadi penting. Pengguna harus tahu bahwa teks yang sedang dibaca berasal dari `specs/003-payroll/tasks.md`, bukan dari salinan yang tersimpan di tempat lain.

Devan menambahkan satu prinsip terakhir di catatannya.

```text
Open the source where it lives. Summarize only what the source can show.
```

Ia membaca kalimat tersebut beberapa kali. Rasa cemasnya belum hilang sepenuhnya. Membuat alat untuk memahami AI Agent berarti berurusan dengan ekspektasi yang tinggi. Viewer tidak akan dapat menjawab semuanya. Tetapi viewer dapat menjawab bagian yang menjadi tanggung jawabnya: file apa yang ada, feature apa yang mengandung file tersebut, dan task mana yang dicentang.

Di situlah kejujuran menjadi bentuk pengalaman pengguna. Jika viewer tidak tahu, ia menampilkan `Unknown`. Jika file belum ada, ia tidak mengarang file. Jika parser hanya mengenali sebagian format, ia tetap memberi akses ke raw Markdown. Transparansi semacam itu mungkin terasa sederhana, tetapi justru memberi ruang bagi manusia untuk mengambil keputusan.

Ketika lampu ruang kerja dimatikan, Devan merasa project ini sudah memiliki lebih dari sekadar nama. Ia memiliki masalah yang jelas, goal yang sederhana, non-goal yang tegas, dan pertanyaan penerimaan yang dapat diperiksa. Besok mereka akan menulis scanner. Namun, sebenarnya mereka sudah mulai membangun alat itu malam ini, ketika mereka sepakat bahwa melihat proses AI Agent tidak boleh membutuhkan proses lain yang sama melelahkannya.

Dan setiap masalah yang dapat dipetakan biasanya sudah memiliki jalan pertama untuk diselesaikan.

## Bab 2: Dari Folder Markdown Menjadi Model yang Bisa Dibaca

Pagi di Sleman membawa cahaya yang tipis ke meja kerja Devan. Ia membuka kembali repository `speckit-viewer` dengan kepala yang masih menyimpan percakapan semalam. Myesha benar. Sebelum membangun dashboard, ia harus menentukan bagaimana proyek tersebut memahami sebuah Spec Kit project.

Pertanyaan pertama terlihat sederhana: apa yang harus dipindai?

Jawaban paling aman adalah folder `specs/`. GitHub Spec Kit menyimpan feature di dalam folder dengan pola seperti `NNN-name`, misalnya `003-payroll` atau `031-employee-payroll`. Di dalamnya terdapat beberapa artefak Markdown. Tidak semua feature memiliki file yang sama. Sebagian baru memiliki `spec.md`. Sebagian sudah memiliki rencana, riset, model data, task, checklist, atau contract. Template juga dapat berubah mengikuti versi Spec Kit.

Devan sempat ingin membuat daftar nama file yang wajib ada. Ia menulis aturan seperti ini.

```text
spec.md
plan.md
tasks.md
research.md
data-model.md
quickstart.md
```

Namun, Myesha menghapus kata "wajib".

"Kalau `plan.md` belum ada, feature tidak boleh dianggap rusak," katanya. "Mungkin agent memang baru menyelesaikan spesifikasi. Alat kita harus membaca keadaan yang ada, bukan memaksa semua feature terlihat seperti template lengkap."

Catatan itu menjadi keputusan penting. Scanner harus toleran. Ia perlu mengenali file yang dikenal, tetapi tidak boleh gagal hanya karena ada file lain atau ada file yang belum dibuat. Format Spec Kit adalah dokumen hidup. Versi template dapat berubah. Project pengguna juga dapat memiliki artefak tambahan.

Devan lalu membuat model domain yang tipis. Ia tidak ingin model ini bergantung pada UI. Model tersebut hanya perlu menjelaskan feature, file, dan project.

```go
// Package model holds the shared domain types for a scanned Spec Kit project.
package model

type FileKind int

const (
	FileOther FileKind = iota
	FileSpec
	FilePlan
	FileTasks
	FileResearch
	FileDataModel
	FileQuickstart
	FileChecklist
	FileContract
)

type SpecKitFile struct {
	Kind FileKind
	Rel  string
	Abs  string
}

type Feature struct {
	ID    string
	Slug  string
	Name  string
	Dir   string
	Files []SpecKitFile
}

type Project struct {
	Root             string
	ConstitutionPath string
	Features         []Feature
}
```

Kode tersebut tidak memiliki warna, border, keyboard shortcut, atau detail Bubble Tea. Itu memang sengaja. Model domain harus dapat dipakai oleh scanner, phase inference, test, dan UI tanpa membuat semua bagian proyek saling mengetahui urusan masing-masing.

Jovian membaca struct `Feature` dari layar.

"Kenapa punya `ID`, `Slug`, dan `Name` sekaligus? Bukankah semuanya berasal dari nama folder?"

Devan menjawab sambil menunjukkan folder `031-employee-payroll`.

"ID adalah `031`. Slug adalah `employee-payroll`. Name adalah `Employee Payroll`. Masing-masing punya pekerjaan. ID penting untuk identitas feature dan sorting. Slug penting untuk path. Name lebih nyaman untuk ditampilkan kepada manusia."

Myesha menambahkan, "Satu hal yang kelihatan kecil seperti pemisahan ini menghindari banyak logika string di UI. UI tidak perlu memotong nama folder setiap kali ingin menampilkan judul."

Scanner kemudian menjadi lapisan yang mengubah filesystem menjadi model. Kode intinya menggunakan regular expression untuk mengenali folder feature, lalu berjalan ke dalam folder tersebut untuk mengumpulkan path relatif.

```go
var featureDirRe = regexp.MustCompile(`^(\d+)-(.+)$`)

func BuildFeature(dirName string, rels []string) (model.Feature, bool) {
	m := featureDirRe.FindStringSubmatch(dirName)
	if m == nil {
		return model.Feature{}, false
	}
	f := model.Feature{
		ID:   m[1],
		Slug: m[2],
		Name: titleFromSlug(m[2]),
	}
	sorted := append([]string(nil), rels...)
	sort.Strings(sorted)
	for _, rel := range sorted {
		f.Files = append(f.Files, model.SpecKitFile{
			Kind: ClassifyFile(rel),
			Rel:  rel,
		})
	}
	return f, true
}
```

Ada dua hal yang membuat fungsi ini berharga. Pertama, ia pure. Ia tidak membaca disk. Ia hanya menerima nama folder dan daftar path, lalu menghasilkan `Feature`. Kedua, ia tidak membuat asumsi bahwa semua file harus dikenal. `ClassifyFile` memetakan file yang penting untuk viewer, sementara file yang belum dipahami tetap menjadi `FileOther`.

```go
func ClassifyFile(rel string) model.FileKind {
	dir, base := "", rel
	if i := strings.IndexByte(rel, '/'); i >= 0 {
		dir, base = rel[:i], rel[i+1:]
	}
	if !strings.HasSuffix(base, ".md") || strings.Contains(base, "/") {
		return model.FileOther
	}
	switch dir {
	case "":
		switch base {
		case "spec.md":
			return model.FileSpec
		case "plan.md":
			return model.FilePlan
		case "tasks.md":
			return model.FileTasks
		case "research.md":
			return model.FileResearch
		case "data-model.md":
			return model.FileDataModel
		case "quickstart.md":
			return model.FileQuickstart
		}
	case "checklists":
		return model.FileChecklist
	case "contracts":
		return model.FileContract
	}
	return model.FileOther
}
```

Devan menyukai keputusan `FileOther`. Dalam banyak tools, file yang tidak dikenal sering dianggap gangguan. Di sini file tidak dikenal tetap dapat dibaca. Viewer hanya belum memberikan perlakuan khusus kepadanya. Perbedaan itu membuat alat lebih tahan terhadap perubahan template.

Saat ia menjalankan scanner terhadap fixture, hasilnya mulai memiliki bentuk.

```text
Project
└── Feature 003 Employee Payroll
    ├── spec.md
    ├── plan.md
    ├── data-model.md
    ├── research.md
    ├── tasks.md
    ├── quickstart.md
    ├── checklists/requirements.md
    └── contracts/payslip.md
```

Ia lalu menambahkan feature yang hanya memiliki `spec.md`. Test tersebut penting karena feature baru harus tetap terlihat di dashboard. Jika scanner hanya bekerja pada folder yang lengkap, viewer akan menyembunyikan bagian paling awal dari proses.

"Feature yang baru punya spesifikasi bukan feature yang gagal," ujar Myesha. "Itu feature yang sedang berada di titik awal. Viewer harus membantu kita melihat titik awal itu."

Kata "melihat" kembali muncul. Devan mulai memahami bahwa alat ini tidak perlu menghakimi. Ia tidak perlu memberi pesan merah untuk setiap ketidaksempurnaan. Ia cukup memberi informasi yang jujur tentang apa yang tersedia.

Setelah model domain dan scanner bekerja, Devan memikirkan constitution. Spec Kit dapat memiliki `.specify/memory/constitution.md`, yaitu dokumen yang menyimpan prinsip dan aturan project. Dokumen tersebut tidak berada di dalam folder feature, tetapi tetap penting ketika seseorang ingin memahami mengapa agent membuat keputusan tertentu.

Scanner mengingat path constitution jika file tersebut ada.

```go
constitution := filepath.Join(root, ".specify", "memory", "constitution.md")
if _, err := os.Stat(constitution); err == nil {
	project.ConstitutionPath = constitution
}
```

Keputusan ini membuat constitution dapat dibuka dari navigator tanpa membuat scanner berpura-pura bahwa ia adalah feature. `Project` memiliki constitution. `Feature` memiliki artefaknya. Setiap konsep berada di tempat yang sesuai.

Jovian lalu meminta contoh command yang akan dipakai pengguna.

"Kalau aku sudah berada di root project, cukup `speckit`?"

"Iya," jawab Devan. "Path default-nya current directory. Kalau mau membuka project lain, beri path."

Entry point di `main.go` dibuat sesingkat mungkin.

```go
func main() {
	root := "."
	if len(os.Args) > 1 {
		if os.Args[1] == "--version" || os.Args[1] == "-v" {
			fmt.Println("speckit", version)
			return
		}
		root = os.Args[1]
	}

	root, err := filepath.Abs(root)
	if err != nil {
		fatal(err)
	}

	app, err := ui.New(root, version)
	if err != nil {
		fmt.Fprintf(os.Stderr, "speckit: %v\n", err)
		fmt.Fprintln(os.Stderr,
			"Point speckit at a Spec Kit project root (a folder containing specs/).")
		os.Exit(1)
	}
	if _, err := tea.NewProgram(app).Run(); err != nil {
		fatal(err)
	}
}
```

Pesan error-nya juga bagian dari pengalaman. Kalau pengguna menjalankan `speckit` dari folder yang salah, program tidak boleh hanya mencetak error filesystem yang panjang. Ia perlu memberi petunjuk bahwa path yang dipilih harus memiliki `specs/`.

Myesha menyebutnya sebagai "error yang menghormati konteks". Pengguna sedang mencoba melihat project. Mereka tidak membutuhkan stack trace yang tidak membantu. Mereka membutuhkan informasi tentang bentuk folder yang benar.

Di tahap ini, Devan mulai menyadari mengapa ia merasa nyaman dengan terminal. Terminal memberikan transparansi. Ia dapat melihat path, command, output, dan error secara langsung. Namun, transparansi saja tidak cukup ketika data memiliki struktur yang saling berhubungan. `speckit-viewer` harus mempertahankan transparansi itu sambil menambahkan orientasi.

Scanner juga harus bersikap hati-hati terhadap path. Ia membaca project yang dipilih pengguna, tetapi tidak perlu menjelajahi seluruh filesystem. Root project menentukan batas. `specs/` menjadi pintu masuk. Setiap feature menjadi batas berikutnya. File disimpan sebagai absolute path untuk dibaca ketika dipilih, dan relative path untuk ditampilkan sebagai breadcrumb.

Pemisahan absolute dan relative path itu mudah dianggap sebagai detail kecil. Sebenarnya, keduanya menjawab kebutuhan yang berbeda. Absolute path dibutuhkan operasi filesystem. Relative path dibutuhkan manusia. Jika UI menampilkan path absolute yang panjang, layar cepat penuh oleh direktori lokal. Jika scanner hanya menyimpan relative path, UI tidak tahu file mana yang harus dibuka. Model `SpecKitFile` menyimpan keduanya supaya setiap lapisan tidak perlu menebak ulang.

Jovian bertanya apakah scanner harus mengikuti symbolic link.

Devan membuka dokumentasi `filepath.WalkDir` dan berpikir sebentar. "Untuk MVP, kita tidak perlu membuat aturan khusus. Yang penting scanner tidak keluar dari root secara tidak terduga dan error dari satu entry tidak membuat semua feature gagal."

Myesha menyukai jawaban itu karena tidak membuat janji yang belum didukung. Banyak keputusan keamanan dan portability muncul ketika tool membaca filesystem. Tetapi project ini bukan file indexer umum. Ia memiliki scope yang kecil. Scope tersebut membuat keputusan awal lebih mudah dipertanggungjawabkan.

Mereka juga mendiskusikan penamaan feature. Regex `^(\d+)-(.+)$` menerima folder numeric prefix dengan slug setelah tanda hubung. Folder seperti `templates` diabaikan. Folder seperti `003-payroll` diterima. Keputusan ini membuat scanner tidak salah menganggap folder lain di dalam `specs/` sebagai feature.

"Kalau sebuah project punya folder `archive`, kita tidak ingin folder itu tiba-tiba muncul sebagai feature," kata Myesha. "Nama folder bukan hanya data. Ia juga sinyal struktur."

Namun, mereka tidak memaksakan slug tertentu selain pola umum. `003-payroll`, `031-employee-payroll`, dan nama lain yang mengikuti pola dapat dipindai. Scanner menghasilkan title dengan mengubah tanda hubung menjadi spasi dan mengkapitalkan huruf awal kata. Hasilnya tidak dimaksudkan sebagai editor judul. Ia hanya menjadi nama yang nyaman dibaca di dashboard.

Deterministic sorting juga mendapat perhatian. `os.ReadDir` dan filesystem tidak boleh menjadi sumber urutan yang tidak stabil di layar. Feature diurutkan berdasarkan ID. File di dalam feature diurutkan berdasarkan relative path. Jika urutan berubah-ubah antara dua run, pengguna akan merasa viewer tidak dapat dipercaya meskipun datanya sama.

Devan menulis contoh kecil untuk menjelaskan mengapa sorting penting.

```text
Run pertama: 003, 007, 031
Run kedua:   031, 003, 007
```

Perbedaan tersebut mungkin tidak memengaruhi fungsi parser, tetapi memengaruhi memori pengguna. Orang yang sedang menelusuri pekerjaan AI Agent sering kembali ke feature yang sama. Posisi yang stabil mengurangi beban untuk mencari ulang.

Model domain yang tipis juga membantu test. `BuildFeature` dapat diberi daftar path tanpa membuat folder sementara. Test dapat memeriksa bahwa file terurut, `File(model.FileTasks)` menemukan task, dan `PresentKinds` memberi jenis yang benar. Filesystem walk tetap memiliki test terpisah untuk memastikan project fixture dibaca.

Myesha menyebut pemisahan itu sebagai batas antara keputusan dan mekanisme. `BuildFeature` memutuskan bagaimana nama folder dan path menjadi feature. `Scan` mengurus bagaimana data tersebut didapat dari disk. Jika kelak input datang dari archive atau remote workspace, fungsi pure masih dapat digunakan.

Devan tidak ingin menjanjikan dukungan remote. Ia hanya melihat manfaat desain tersebut. Kode yang tidak bergantung pada disk lebih mudah dipahami. Ia juga lebih mudah diuji tanpa membuat test berjalan lambat.

Constitution mendapat perlakuan yang sama. Viewer tidak mengubahnya menjadi feature palsu. Ia menyimpannya di `Project.ConstitutionPath`, lalu UI menampilkan row khusus `§ Constitution` jika file tersebut ada. Dengan cara ini, pengguna dapat membuka aturan project dari tempat yang sama tanpa mengacaukan tabel feature.

"Kenapa constitution tidak masuk dashboard?" tanya Jovian.

"Karena dashboard menjawab progress feature," kata Devan. "Constitution bukan feature. Ia adalah konteks yang memengaruhi semua feature."

Pemisahan tersebut membuat navigator memiliki tiga jenis entry: dashboard, constitution, dan feature. Feature dapat diperluas menjadi file. Setiap jenis entry punya action yang berbeda, tetapi semuanya tetap berada dalam satu list.

Devan mulai melihat manfaat model yang tidak terlalu pintar. Model tidak perlu tahu cara menggambar `§`. Model tidak perlu tahu warna phase. Model hanya menyimpan path dan jenis. UI dapat mengubahnya menjadi pengalaman visual. Jika warna berubah, scanner tidak perlu disentuh. Jika file kind baru ditambahkan, UI dapat menanganinya tanpa mengubah cara folder dipindai.

Pada sore hari, mereka sengaja menaruh file yang tidak dikenal ke fixture.

```text
specs/003-payroll/
├── notes.md
└── diagram.png
```

Scanner tetap selesai. `notes.md` dan `diagram.png` menjadi `FileOther`. File tersebut masih dapat muncul di navigator dan dibuka, meskipun tidak memiliki parsing khusus. Perilaku itu memberi pilihan kepada pengguna. Viewer tidak memaksa semua artefak mengikuti daftar yang diketahui oleh versi saat ini.

Devan merasa lega karena keputusan tersebut menurunkan risiko terhadap perubahan versi Spec Kit. Ia tahu template dapat menambah atau mengganti nama dokumen. Jika scanner gagal pada setiap nama baru, viewer akan cepat usang. Jika scanner toleran, viewer tetap memberi nilai walaupun sebagian file belum diberi badge khusus.

Tentu saja, toleran bukan berarti ceroboh. Folder yang tidak menyerupai feature tetap diabaikan. File tetap dicatat dengan path yang tepat. Error saat root tidak memiliki `specs/` tetap disampaikan. Toleransi harus berjalan bersama batas yang jelas.

Myesha menyimpulkan prinsip scanner dalam satu kalimat.

"Kenali struktur yang penting. Pertahankan data yang tidak dikenal. Gagal hanya ketika project root memang tidak sesuai."

Kalimat tersebut kemudian terlihat di banyak bagian project. Parser tidak gagal hanya karena section non-task. Phase inference tidak gagal hanya karena tasks belum dapat dibaca. UI tetap dapat menampilkan feature yang baru memiliki satu file. Semua lapisan memilih degradasi yang dapat dipahami daripada error total.

Devan juga menolak keinginan untuk menambahkan metadata buatan ke setiap `Feature`. Ia sempat ingin menyimpan `Status`, `LastModified`, dan `Summary` langsung dari hasil scanner. Setelah dipikirkan, dua field pertama dapat menimbulkan kesan yang tidak tepat, sedangkan summary membutuhkan proses lain yang belum menjadi tanggung jawab scanner. Ia menghapusnya dari model awal.

Keputusan tersebut membuat model terasa lebih biasa, tetapi justru lebih jujur. `Feature` menjelaskan apa yang dapat diketahui dari nama folder dan file yang ada. Phase inference memiliki tempat sendiri karena phase bukan property asli folder. UI memiliki view model sendiri karena phase label, progress bar, dan expanded state adalah kebutuhan tampilan. Setiap lapisan dapat berubah tanpa membuat semua lapisan membawa data yang bukan miliknya.

Myesha menyebut pendekatan itu sebagai memisahkan fakta dan pembacaan. Path file adalah fakta. Jenis file adalah pembacaan scanner. Phase adalah pembacaan yang lebih jauh. Label berwarna adalah cara UI menyampaikan pembacaan tersebut. Jika sebuah pembacaan berubah, sumber faktanya tetap dapat diperiksa.

Pemisahan ini juga membantu ketika seseorang membandingkan dua keadaan project. Misalnya, agent menambahkan `plan.md` tetapi belum membuat `tasks.md`. Scanner akan melihat file baru. Inference akan berpindah dari `Specified` ke `Planned`. Dashboard hanya menampilkan perubahan label. Pengguna tetap dapat membuka kedua file dan melihat apa yang berubah di antara sesi agent.

Jika project dihapus atau dipindahkan, absolute path lama tidak boleh dipakai tanpa rescan. Itulah alasan `R` dan startup scan menjadi bagian dari pengalaman. Viewer tidak menyimpan index permanen yang dapat basi. Ia memulai dari root yang sedang dipilih dan membaca keadaan filesystem yang berlaku sekarang.

Devan menyadari bahwa pilihan ini cocok dengan cara kerja AI Agent. Agent dapat membuat perubahan cepat. Viewer harus memeriksa keadaan terbaru, bukan mengandalkan kesimpulan dari sesi kemarin. File system menjadi sumber yang sederhana dan terlihat. Tidak ada mekanisme tersembunyi yang harus dipercaya selain permission membaca file yang memang sudah dimiliki pengguna.

Dashboard bukan tempat untuk menyembunyikan file. Navigator bukan tempat untuk mengubah source. Renderer bukan tempat untuk mengarang status. Semua komponen hanya menyusun bukti yang sudah ada.

Devan menulis prinsip lain.

```text
The viewer may summarize a project, but it must not invent project state.
```

Kalimat itu akan diuji ketika mereka mulai menentukan fase feature. Tidak ada status yang dapat dibaca langsung. Ada file dan checkbox. Mereka harus membuat inferensi yang berguna, tetapi tetap jujur.

Sore itu, ketika cahaya matahari mulai turun di Berbah, scanner sudah bisa membaca project fixture. Feature tampil dalam urutan ID. File tampil dalam urutan path. Constitution dapat ditemukan. File tambahan tidak membuat proses gagal.

Belum ada UI. Belum ada warna. Belum ada progress bar. Namun, bagian yang paling sulit sudah mulai memiliki bentuk: proyek yang tadinya hanya kumpulan folder Markdown sekarang menjadi `Project`, `Feature`, dan `SpecKitFile` yang dapat dipahami kode.

Jovian melihat hasil test yang hijau.

"Sekarang project-nya sudah bisa bercerita?"

"Belum," kata Devan. "Sekarang ia baru bisa memperkenalkan diri."

Myesha tersenyum. "Cerita dimulai ketika kita membaca fasenya."

## Bab 3: Fase yang Tidak Pernah Ditulis Secara Langsung

Malam berikutnya, Devan membawa pertanyaan paling mengganggu ke meja makan. Ia sudah dapat memindai feature. Ia sudah dapat mengelompokkan artefak. Tetapi dashboard yang hanya menampilkan nama feature belum menyelesaikan masalah utama.

Ia ingin melihat fase.

Dalam alur Spec Kit, orang biasanya berbicara tentang spesifikasi, rencana, task, dan implementasi. Namun, di folder project tidak selalu ada field seperti berikut.

```yaml
phase: implementing
progress: 72/128
```

Yang tersedia adalah bukti tidak langsung. `spec.md` menunjukkan spesifikasi sudah ada. `plan.md`, `research.md`, atau `data-model.md` menunjukkan pekerjaan perencanaan telah berjalan. `tasks.md` menunjukkan task telah dihasilkan. Checkbox di dalamnya menunjukkan sebagian progress implementasi.

Devan menulis daftar kondisi di papan kecil.

| Bukti yang tersedia | Fase yang ditampilkan |
|---|---|
| `spec.md` saja | Specified |
| File perencanaan tersedia | Planned |
| `tasks.md`, belum ada task selesai | Tasks Generated |
| Sebagian task selesai | Implementing |
| Semua task selesai | Implemented |

Jovian membaca tabel itu dengan serius.

"Kalau semua task selesai tetapi kode belum ada, apakah benar-benar implemented?"

Devan tidak langsung menjawab. Pertanyaan itu memang valid. Checkbox adalah representasi rencana, bukan bukti bahwa production code sudah aman. `speckit-viewer` tidak boleh menyatakan lebih dari yang dapat dibuktikan oleh artefak.

Myesha menaruh sendoknya.

"Label `Implemented` di sini berarti semua task dalam `tasks.md` sudah dicentang. Itu bukan audit production. Kita harus menjelaskan arti labelnya."

Kejujuran semantik menjadi penting. Viewer boleh membantu orientasi, tetapi tidak boleh membuat pengguna percaya bahwa heuristik adalah sumber kebenaran. Dalam README, phase inference dijelaskan sebagai hasil dari file yang ada dan rasio checkbox.

Sebelum menghitung checkbox, Devan harus membaca bentuk `tasks.md`. Ia menemukan baris seperti ini di project nyata.

```markdown
## Phase 1: Setup

- [x] T001 Create module skeleton
- [X] T002 [P] Configure lint rules

## Phase 3: User Story 1 - Generate payslip 🎯 MVP

- [x] T003 [P] [US1] Add payslip table schema
- [ ] T004 [US1] Implement payslip renderer
- [ ] T005 Wire cron task
```

Ada beberapa detail yang mudah terlewat. Checkbox dapat menggunakan `[x]` atau `[X]`. Task memiliki ID `T001`. Marker `[P]` menunjukkan pekerjaan paralel. Marker `[US1]` menunjukkan user story. Phase dapat muncul dalam urutan yang tidak selalu naik. Ada section `Dependencies` yang bukan phase. Ada phase dengan suffix `🎯 MVP`.

Devan sempat mempertimbangkan parser Markdown penuh. Ia dapat membangun AST dan membaca seluruh struktur dokumen. Myesha mengingatkan agar ia tidak membangun lebih dari yang dibutuhkan.

"Kita hanya perlu membaca bentuk task yang memiliki aturan cukup jelas," kata Myesha. "Line-based state machine sudah cukup. Parser tidak perlu memahami setiap kemungkinan Markdown. Ia perlu mengambil informasi yang dipakai dashboard."

Devan membuat struct parser.

```go
type Task struct {
	ID       string
	Done     bool
	Parallel bool
	Story    string
	Text     string
}

type TaskPhase struct {
	Title  string
	Number int
	MVP    bool
	Tasks  []Task
}

type TasksDocument struct {
	Phases []TaskPhase
}

func (d TasksDocument) Total() int {
	n := 0
	for _, p := range d.Phases {
		n += len(p.Tasks)
	}
	return n
}

func (d TasksDocument) Checked() int {
	n := 0
	for _, p := range d.Phases {
		for _, t := range p.Tasks {
			if t.Done {
				n++
			}
		}
	}
	return n
}
```

Regex utama hanya menerima task line dengan ID yang sesuai.

```go
var (
	taskLineRe    = regexp.MustCompile(`^\s*- \[([ xX])\]\s+(T\d{3})\s+(.*)$`)
	parallelRe    = regexp.MustCompile(`^\[P\]\s*`)
	storyRe       = regexp.MustCompile(`^\[(US\d+)\]\s*`)
	phaseHeaderRe = regexp.MustCompile(`^##\s+Phase\s+(\d+)\s*:?\s*(.*)$`)
	anyHeaderRe   = regexp.MustCompile(`^##\s+(.*)$`)
)
```

Kemudian parser berjalan baris demi baris. Ketika melihat phase header, parser menyimpan phase saat ini. Ketika melihat heading lain, parser membuat section sementara. Section tersebut hanya masuk hasil jika memiliki task atau memiliki nomor phase. Dengan cara ini, `Dependencies` yang tidak memiliki task akan dibuang, tetapi phase kosong tetap dapat dipertahankan.

```go
func ParseTasks(content string) TasksDocument {
	var doc TasksDocument
	var current *TaskPhase

	flush := func() {
		if current != nil && (len(current.Tasks) > 0 || current.Number > 0) {
			doc.Phases = append(doc.Phases, *current)
		}
		current = nil
	}

	for _, line := range strings.Split(content, "\n") {
		if m := phaseHeaderRe.FindStringSubmatch(line); m != nil {
			flush()
			num, _ := strconv.Atoi(m[1])
			title := strings.TrimSpace(strings.TrimPrefix(line, "##"))
			current = &TaskPhase{
				Title: title,
				Number: num,
				MVP: strings.Contains(title, "🎯 MVP"),
			}
			continue
		}

		if m := anyHeaderRe.FindStringSubmatch(line); m != nil {
			flush()
			current = &TaskPhase{Title: strings.TrimSpace(m[1])}
			continue
		}

		m := taskLineRe.FindStringSubmatch(line)
		if m == nil {
			continue
		}

		task := Task{ID: m[2], Done: m[1] == "x" || m[1] == "X"}
		rest := m[3]
		if loc := parallelRe.FindString(rest); loc != "" {
			task.Parallel = true
			rest = rest[len(loc):]
		}
		if sm := storyRe.FindStringSubmatch(rest); sm != nil {
			task.Story = sm[1]
			rest = rest[len(sm[0]):]
		}
		task.Text = strings.TrimSpace(rest)
		if current == nil {
			current = &TaskPhase{}
		}
		current.Tasks = append(current.Tasks, task)
	}

	flush()
	return doc
}
```

Jovian memperhatikan marker `[P]` dan `[US1]` yang hilang dari `Text`.

"Kenapa tidak membiarkannya saja di teks?"

"Karena UI ingin memberi gaya berbeda," jawab Devan. "`[P]` dapat menjadi badge parallel. `[US1]` dapat menjadi badge story. Isi task menjadi lebih mudah dibaca kalau metadata dan kalimatnya memiliki bentuk sendiri."

Keputusan kecil ini membuat checklist terasa lebih seperti alat navigasi daripada salinan Markdown biasa. Pengguna dapat melihat task, tetapi juga dapat membaca struktur yang biasanya tenggelam di antara tanda kurung.

Setelah parser selesai, Devan membuat fungsi inference.

```go
type Phase int

const (
	Unknown Phase = iota
	Specified
	Planned
	TasksGenerated
	Implementing
	Implemented
)

type Result struct {
	Phase   Phase
	Checked int
	Total   int
}

func Infer(present map[model.FileKind]bool, tasks *parser.TasksDocument) Result {
	if present[model.FileTasks] && tasks != nil {
		checked, total := tasks.Checked(), tasks.Total()
		r := Result{Checked: checked, Total: total}
		switch {
		case total == 0 || checked == 0:
			r.Phase = TasksGenerated
		case checked == total:
			r.Phase = Implemented
		default:
			r.Phase = Implementing
		}
		return r
	}
	if present[model.FilePlan] || present[model.FileResearch] ||
		present[model.FileDataModel] {
		return Result{Phase: Planned}
	}
	if present[model.FileSpec] {
		return Result{Phase: Specified}
	}
	return Result{Phase: Unknown}
}
```

Urutan kondisi tersebut penting. Jika `tasks.md` tersedia, parser task menjadi bukti yang lebih kuat daripada sekadar keberadaan `plan.md`. Feature dengan semua dokumen dan `tasks.md` yang belum memiliki checkbox selesai harus tampil sebagai `Tasks Generated`, bukan hanya `Planned`. Feature dengan sebagian checkbox selesai tampil sebagai `Implementing` bersama angka progress. Feature dengan semua task selesai tampil sebagai `Implemented`.

Namun, ada edge case yang harus dijaga. Bagaimana jika `tasks.md` ada tetapi gagal dibaca atau parser belum menghasilkan dokumen? Dalam test, kondisi itu tidak boleh membuat program panik. Jika `tasks` bernilai nil, inference dapat turun ke bukti file yang tersedia. Hasilnya mungkin `Specified` atau `Planned`, bukan karena program tahu semuanya, tetapi karena program mengakui keterbatasan bacaan saat itu.

Myesha menyebut ini sebagai graceful degradation.

"Alat pembaca yang baik tidak langsung berhenti ketika salah satu halaman tidak terbuka," katanya. "Ia memberi apa yang bisa diberikan dan tidak mengarang bagian yang hilang."

Devan kemudian menulis test table-driven.

```go
func TestInfer(t *testing.T) {
	cases := []struct {
		name      string
		present   map[model.FileKind]bool
		tasks     *parser.TasksDocument
		want      Phase
		wantLabel string
	}{
		{"no files", kinds(), nil, Unknown, "Unknown"},
		{"spec only", kinds(model.FileSpec), nil,
			Specified, "Specified"},
		{"spec+plan", kinds(model.FileSpec, model.FilePlan), nil,
			Planned, "Planned"},
		{"tasks none checked", kinds(model.FileSpec,
			model.FilePlan, model.FileTasks), tasksDoc(0, 5),
			TasksGenerated, "Tasks Generated"},
		{"tasks partly checked", kinds(model.FileSpec,
			model.FilePlan, model.FileTasks), tasksDoc(72, 56),
			Implementing, "Implementing 72/128"},
		{"tasks all checked", kinds(model.FileSpec,
			model.FilePlan, model.FileTasks), tasksDoc(4, 0),
			Implemented, "Implemented"},
	}
	for _, c := range cases {
		t.Run(c.name, func(t *testing.T) {
			got := Infer(c.present, c.tasks)
			if got.Phase != c.want {
				t.Errorf("Phase = %v, want %v", got.Phase, c.want)
			}
			if got.Label() != c.wantLabel {
				t.Errorf("Label() = %q, want %q", got.Label(), c.wantLabel)
			}
		})
	}
}
```

Test tersebut memberi Devan rasa aman. Ia tidak sedang menulis aturan yang hanya terlihat benar pada satu project. Ia sedang mengunci beberapa keadaan penting. Feature baru. Feature terencana. Task belum dikerjakan. Task sebagian selesai. Task selesai seluruhnya.

Ia juga membuat fixture yang meniru bentuk project nyata. Fixture tersebut memiliki checkbox campuran `[x]` dan `[X]`, phase dengan nomor yang tidak berurutan, section dependency, marker parallel, dan marker user story. Meniru kasus nyata penting karena parser yang dibuat dari contoh terlalu bersih sering gagal ketika bertemu dokumen yang benar-benar ditulis oleh manusia atau agent dalam beberapa tahap.

"Kenapa phase bisa tidak berurutan?" tanya Jovian.

"Karena dokumen dapat diedit dan phase baru bisa ditambahkan belakangan," jawab Myesha. "Parser tidak boleh mengurutkan ulang isi dokumen hanya karena angka phase-nya terlihat aneh. Ia membaca urutan yang ditulis."

Pelajaran itu lebih besar dari `tasks.md`. Artefak AI Agent bukan output sekali jadi yang selalu rapi. Ia adalah dokumen yang tumbuh. Agent dapat menambahkan phase. Manusia dapat mengubah checkbox. Template dapat berubah. Viewer perlu bekerja dengan kenyataan tersebut.

Devan lalu mencoba beberapa keadaan yang lebih membingungkan. Sebuah `tasks.md` dapat memiliki phase header tanpa task. Sebuah task dapat muncul sebelum heading apa pun. Sebuah section dapat memiliki bullet biasa yang tidak memakai format task ID. Sebuah phase dapat memakai nomor `4` setelah phase `3`, lalu dokumen kembali ke phase `2` karena agent menambahkan catatan lama. Tidak semua bentuk itu indah, tetapi semuanya mungkin terjadi pada dokumen yang sedang berkembang.

Parser tidak mencoba memperbaiki dokumen tersebut. Ia tidak memindahkan phase. Ia tidak menambahkan task yang hilang. Ia tidak mengubah `[X]` menjadi `[x]` di source. Ia hanya membaca baris yang dapat dikenali dan mempertahankan urutan yang ditemukan. Sikap ini penting karena viewer bukan formatter. Jika viewer memperbaiki source secara diam-diam, pengguna dapat kehilangan perbedaan yang justru ingin diperiksa.

"Kalau source kelihatan berantakan, raw mode harus memperlihatkan bahwa ia memang berantakan," kata Myesha. "Kerapian checklist boleh menjadi tampilan. Kerapian itu tidak boleh menyamar sebagai isi asli."

Devan menyimpan dua bentuk informasi. `currentRaw` berisi teks asli file. `currentTasks` berisi hasil parse. Checklist memakai hasil parse. Raw mode memakai `currentRaw`. Ketika file di-rescan, parser dijalankan lagi. Dengan cara itu, tampilan khusus dan sumber selalu dapat dibandingkan.

Perbandingan tersebut juga berguna ketika agent baru saja mengubah dokumen. Jika checkbox berubah tetapi phase tidak berubah seperti yang diharapkan, Devan dapat menekan `r` untuk kembali ke raw Markdown dan memeriksa header. Jika task tidak muncul, ia dapat melihat apakah ID task mengikuti format yang dipahami parser. Viewer membantu diagnosis tanpa menyembunyikan aturan yang dipakai.

Mereka menambahkan dokumentasi singkat pada label fase. `Specified` berarti `spec.md` ada. `Planned` berarti file perencanaan tersedia tanpa tasks yang berhasil dibaca. `Tasks Generated` berarti `tasks.md` ada tetapi belum memiliki task selesai atau total task nol. `Implementing` berarti sebagian task selesai. `Implemented` berarti semua task yang berhasil diparse dicentang.

Penjelasan tersebut mungkin terdengar berulang, tetapi kata-kata pada label dapat memengaruhi keputusan manusia. Orang dapat melihat `Implemented` lalu berhenti memeriksa. Karena itu, README dan post perlu menerangkan bahwa label tersebut adalah phase hasil inferensi. Ia bukan pemeriksaan terhadap source code, test, deployment, atau production behavior.

Jovian membuat perbandingan lain.

"Ini seperti melihat daftar pekerjaan rumah. Kalau semua kotak dicentang, kita tahu daftar itu selesai. Kita belum tahu apakah hasilnya bagus sebelum melihat jawabannya."

"Tepat," jawab Devan. "Viewer memberitahu keadaan daftar, bukan memberi nilai pada hasil akhirnya."

Perbedaan tersebut membuat alat lebih aman untuk dipakai bersama workflow AI Agent. Manusia tetap menjadi pemeriksa terakhir. Agent dapat menulis task. Viewer dapat menunjukkan task. Developer dapat memeriksa kode. Test dapat menguji perilaku. Setiap lapisan memiliki tanggung jawab yang berbeda.

Test parser kemudian menjadi catatan tentang kontrak minimal. Test tidak hanya memeriksa happy path. Ia memeriksa input kosong, phase tanpa task, task tanpa header, bullet biasa, checkbox uppercase, marker parallel, marker story, dan section yang harus dibuang. Jika template Spec Kit berubah, test akan membantu Devan melihat bagian mana yang tidak lagi cocok.

Ada rasa tenang ketika test tersebut hijau. Bukan karena parser sudah memahami semua Markdown. Ia tidak akan pernah memahami semua variasi tanpa menjadi parser Markdown yang lengkap. Rasa tenang datang karena batas yang dipilih sudah terlihat. Ketika parser menerima `T001`, ia tahu apa yang dilakukan. Ketika parser melewati baris yang tidak dikenali, ia tidak menyembunyikan source. Ketika inference tidak dapat menyimpulkan fase, ia kembali ke hasil yang paling jujur.

Devan menyadari bahwa AI tooling membutuhkan kebiasaan seperti ini. Ketika output dibuat otomatis, orang sering ingin membuat ringkasan otomatis juga. Ringkasan dapat menghemat waktu, tetapi ia berisiko menghapus detail yang menjadi alasan keputusan. `speckit-viewer` mengambil pendekatan yang lebih konservatif. Ia merangkum struktur filesystem dan checkbox, tetapi tetap membawa pengguna ke file Markdown asli.

Myesha menatap layar parser.

"Kita tidak perlu membuat AI kedua untuk menjelaskan output AI pertama," katanya. "Kadang parser deterministik yang sederhana lebih mudah dipercaya."

Kalimat itu terasa tepat bagi Devan. Project ini memang berhubungan dengan AI Agent, tetapi tidak semua bagian harus menggunakan AI. Scanner deterministik lebih cocok untuk struktur folder. Parser regex lebih cocok untuk task line yang formatnya jelas. Phase inference berbasis aturan lebih mudah dijelaskan daripada skor yang tidak terlihat.

Hal tersebut bukan penolakan terhadap AI. Ia adalah pilihan tempat. AI Agent membantu menghasilkan dan mengubah artefak. `speckit-viewer` membantu manusia melihat artefak secara konsisten. Dua alat tersebut dapat hidup berdampingan karena pekerjaan mereka berbeda.

Ketika papan kecil penuh dengan catatan fase, Devan menghapus beberapa kata yang terlalu besar. Ia mengganti "status implementasi" menjadi "phase hasil inferensi". Ia mengganti "project selesai" menjadi "semua task tercentang". Ia mengganti "agent berhasil" menjadi "artefak dapat dibaca".

Myesha melihat perubahan itu dan tersenyum.

"Nama yang tepat menjaga kita dari kesimpulan yang terlalu cepat."

Malam itu mereka menutup parser dengan sebuah kesepakatan. `speckit-viewer` boleh memberi manusia pandangan yang lebih cepat. Ia tidak boleh membuat manusia berhenti berpikir. Fase adalah lampu penunjuk. Source tetap jalan yang harus dilihat.

Sebelum berpindah ke UI, Devan membuat satu percobaan manual. Ia menyalin `tasks.md` ke tiga versi. Versi pertama tidak memiliki checkbox selesai. Versi kedua memiliki satu checkbox selesai dari lima task. Versi ketiga memiliki semua checkbox selesai. Ia ingin melihat apakah label berubah dengan urutan yang masuk akal.

Hasilnya sesuai harapan. Versi pertama menjadi `Tasks Generated`. Versi kedua menjadi `Implementing 1/5`. Versi ketiga menjadi `Implemented`. Perubahan itu terasa sederhana, tetapi ia memberi bentuk pada perjalanan feature. Ketika agent mengerjakan task satu per satu, dashboard tidak perlu menebak narasi baru. Ia cukup membaca rasio yang ada.

Devan kemudian mengubah phase header tanpa mengubah task. Label phase tetap sama karena phase inference bergantung pada keberadaan file dan checkbox, bukan nama deskriptif phase. Keputusan ini memang berarti dashboard tidak akan menganalisis apakah judul phase mengatakan "Polish", "MVP", atau "Deployment". Ia hanya menampilkan informasi yang benar-benar memiliki aturan yang jelas.

Myesha mendukung batas tersebut. "Semakin luas makna yang ingin kita ambil dari bahasa bebas, semakin besar peluang viewer salah. Kalau kita ingin memahami judul phase, itu perlu fitur parser yang berbeda dan kontrak yang berbeda."

Jovian bertanya apakah badge MVP tetap berguna. Devan menjawab bahwa parser menyimpan `MVP` pada `TaskPhase` karena informasi itu eksplisit dan mudah dikenali dari suffix `🎯 MVP`. Badge tersebut dapat membantu manusia melihat phase yang dianggap penting, tanpa mengubah phase utama feature.

Percobaan ini mengajarkan satu hal tentang ringkasan deterministik. Ringkasan tidak harus mengetahui semua konteks untuk tetap berguna. Ia cukup memilih subset fakta yang stabil. Dalam kasus ini, subset tersebut adalah file yang hadir, task yang berhasil diparse, checkbox selesai, dan marker yang jelas.

Jika sebuah project membutuhkan status yang lebih kaya, project tersebut dapat menambahkan sistem lain. `speckit-viewer` tidak menghalangi hal itu. Ia hanya tidak berpura-pura bahwa data yang belum ada sudah tersedia. Batas itu membuat pengguna dapat memakai labelnya dengan pemahaman yang sama.

Di tengah pengerjaan, Devan menjalankan command yang paling membuatnya bersemangat.

```text
Feature                         Phase              Progress
003 Employee Payroll            Implementing       ████░░░░░░ 3/6
007 Trivial Toggle              Specified           —
```

Data itu belum tampil di terminal dengan benar, tetapi ia sudah dapat dibayangkan. Dari satu tabel, Devan bisa tahu feature mana yang membutuhkan perhatian. Ia tidak perlu membuka semua `tasks.md` hanya untuk menemukan pekerjaan yang masih berjalan.

Namun, Myesha menahan kegembiraan itu.

"Jangan sebut progress ini sebagai progress implementasi yang absolut," katanya. "Sebut sebagai progress task. Nama yang tepat membuat ekspektasi tetap tepat."

Devan mengubah pikirannya. Dashboard akan menampilkan fase dan progress task. Detail pada README akan menjelaskan bahwa phase berasal dari file yang tersedia dan rasio checkbox. Label singkat tidak boleh menjadi alasan untuk menyembunyikan mekanisme di belakangnya.

Kejelasan seperti ini terasa penting ketika alat berhubungan dengan AI Agent. Agent sering bekerja melalui banyak langkah yang sulit dilihat dalam satu layar. Manusia harus dapat membedakan fakta, ringkasan, dan inferensi. `spec.md` adalah fakta dokumen. `tasks.md` adalah fakta checkbox. `Implementing 3/6` adalah ringkasan berdasarkan fakta tersebut. Viewer tidak boleh membuat ringkasan terdengar seperti audit penuh.

Malam semakin larut. Devan menutup editor dan memandangi papan.

"Sekarang kita sudah punya cara membaca fase," katanya. "Tetapi pengguna masih harus melihat semua hasilnya dari satu pane."

Jovian menunjuk dua kolom di kertas Myesha.

"Kalau begitu, buat dua pane. Di kiri pilih feature. Di kanan baca file."

Ide itu terdengar sederhana. Tetapi seperti biasa, interface yang sederhana membutuhkan banyak keputusan agar tidak terasa membingungkan. Besok mereka harus membuat terminal menjadi dashboard.

## Bab 4: Dua Pane, Satu Terminal, dan Markdown yang Bisa Bernapas

Devan memulai babak UI dengan satu syarat yang tidak boleh dilanggar: `speckit-viewer` harus tetap terasa seperti alat terminal. Ia tidak ingin memindahkan pengguna ke browser. Ia tidak ingin membuat layar penuh dengan tombol yang meniru aplikasi desktop. Ia ingin dua pane yang memberi orientasi cepat dan ruang baca yang cukup.

Myesha membuat sketsa.

```text
┌──────────────────────── speckit-viewer ────────────────────────┐
│                                                                 │
│  ┌────────────── Navigator ──────────────┐ ┌── Content ───────┐ │
│  │ ⌂ Dashboard                            │ │ # Feature        │ │
│  │ § Constitution                         │ │                  │ │
│  │ ▸ 003 Employee Payroll · Implementing  │ │ User stories...  │ │
│  │ ▾ 007 Trivial Toggle · Specified       │ │                  │ │
│  │     spec.md                            │ │                  │ │
│  │     plan.md                            │ │                  │ │
│  └────────────────────────────────────────┘ └──────────────────┘ │
│  ↑↓ nav · Enter open · Tab switch pane · / filter · q quit      │
└─────────────────────────────────────────────────────────────────┘
```

"Kiri untuk menjawab di mana kita berada," ujar Myesha. "Kanan untuk membaca mengapa kita berada di sana."

Mereka memilih Go dan ekosistem Charm. Alasannya praktis. Go dapat menghasilkan binary tunggal. Bubble Tea memberikan pola model, update, dan view untuk TUI. Bubbles menyediakan list, table, viewport, dan progress. Glamour merender Markdown di terminal. Lip Gloss memberi style dan layout.

Versi library harus konsisten. Repository memakai `charm.land/bubbletea/v2`, `charm.land/bubbles/v2`, `charm.land/glamour/v2`, dan `charm.land/lipgloss/v2`. Devan sempat mencoba import path lama dari `github.com/charmbracelet/...`, lalu menemukan masalah vanity path. Ia mencatat pengalaman itu supaya orang lain tidak mengulang kebingungan yang sama.

```go
require (
	charm.land/bubbles/v2 v2.1.1
	charm.land/bubbletea/v2 v2.0.8
	charm.land/glamour/v2 v2.0.1
	charm.land/lipgloss/v2 v2.0.6
)
```

Entry point UI membuat aplikasi dari root yang sudah discan.

```go
type App struct {
	root     string
	version  string
	project  model.Project
	features []featureVM

	screen screen
	focus  focusZone
	theme  theme

	nav list.Model
	dash table.Model
	vp   viewport.Model

	expanded map[int]bool

	currentPath  string
	currentRaw   string
	currentKind  model.FileKind
	currentTasks *parser.TasksDocument
	rawMode      bool
}

func New(root, version string) (*App, error) {
	a := &App{
		root: root,
		version: version,
		theme: newTheme(true),
		expanded: map[int]bool{},
	}
	if err := a.rescan(); err != nil {
		return nil, err
	}
	a.initWidgets()
	return a, nil
}
```

`App` memiliki dua screen: dashboard dan browse. Browse memiliki dua focus zone: navigator dan content. State tersebut tidak diletakkan di global variable. Semua keputusan tampilan menjadi bagian dari model, sehingga `Update` dapat mengubahnya berdasarkan message dan `View` dapat menggambar keadaan terbaru.

Dashboard dibuat sebagai table. Setiap row menyimpan ID, nama, phase label, dan progress. Progress bar menggunakan karakter terminal, bukan gambar besar. Bentuknya sederhana, tetapi cukup untuk menjawab pertanyaan pertama.

```go
func dashboardRows(features []featureVM) []table.Row {
	rows := make([]table.Row, 0, len(features))
	for _, f := range features {
		progress := "—"
		if f.Tasks != nil && f.PhaseResult.Total > 0 {
			progress = progressCell(
				f.PhaseResult.Checked,
				f.PhaseResult.Total,
			)
		}
		rows = append(rows, table.Row{
			f.ID,
			f.Name,
			f.PhaseResult.Label(),
			progress,
		})
	}
	return rows
}

func progressCell(checked, total int) string {
	const width = 10
	filled := checked * width / total
	bar := ""
	for i := range width {
		if i < filled {
			bar += "█"
		} else {
			bar += "░"
		}
	}
	return fmt.Sprintf("%s %d/%d", bar, checked, total)
}
```

Devan menyukai progress bar tersebut karena tidak berusaha menjadi grafik. Ia hanya memberi perbandingan visual yang mudah dipindai. Jika seseorang ingin angka pasti, angka tetap berada di sampingnya.

Dari dashboard, Enter membuka `spec.md` feature yang dipilih. Ini adalah keputusan navigasi yang terasa kecil tetapi penting. Ketika seseorang memilih feature, content pane tidak boleh kosong. `spec.md` adalah dokumen yang paling masuk akal sebagai pintu pertama karena ia menjelaskan apa yang sedang dibangun.

Browse menggunakan `bubbles/list`. Bubbles tidak memiliki tree widget yang mereka butuhkan, jadi Devan membuat list datar yang dapat dibangun ulang. Feature menjadi satu row. Ketika Enter ditekan pada feature, file-file feature disisipkan sebagai row indentasi. State expanded disimpan di map.

```go
func buildNavEntries(
	features []featureVM,
	hasConstitution bool,
	expanded map[int]bool,
) []list.Item {
	items := []list.Item{
		navEntry{
			kind: navDashboard,
			title: "⌂ Dashboard",
			filter: "dashboard",
		},
	}
	if hasConstitution {
		items = append(items, navEntry{
			kind: navConstitution,
			title: "§ Constitution",
			filter: "constitution",
		})
	}
	for i, f := range features {
		arrow := "▸"
		if expanded[i] {
			arrow = "▾"
		}
		items = append(items, navEntry{
			kind: navFeature,
			featureIdx: i,
			title: fmt.Sprintf(
				"%s %s · %s  %s",
				arrow, f.ID, f.Name, f.PhaseResult.Label(),
			),
			filter: fmt.Sprintf("%s %s %s", f.ID, f.Slug, f.Name),
		})
		if !expanded[i] {
			continue
		}
		for j, file := range f.Files {
			items = append(items, navEntry{
				kind: navFile,
				featureIdx: i,
				fileIdx: j,
				title: "    " + file.Rel,
				filter: fmt.Sprintf("%s %s", f.ID, file.Rel),
			})
		}
	}
	return items
}
```

Jovian memperhatikan bahwa list dibangun ulang ketika feature di-expand.

"Kalau list dibangun ulang, cursor bisa pindah?"

"Bisa," jawab Devan. "Karena itu kita mencari key entry yang sama dan mengembalikan cursor ke sana."

Key entry dibuat dari kind, feature index, dan file index. Setelah `SetItems`, aplikasi berjalan melalui item baru untuk menemukan key tersebut.

```go
func (a *App) rebuildNav(selectKey string) tea.Cmd {
	items := buildNavEntries(
		a.features,
		a.project.ConstitutionPath != "",
		a.expanded,
	)
	cmd := a.nav.SetItems(items)
	for i, item := range items {
		if e, ok := item.(navEntry); ok && e.key() == selectKey {
			a.nav.Select(i)
			break
		}
	}
	return cmd
}
```

Ada detail lain yang hampir membuat filter rusak. Filtering pada `bubbles/list` berjalan asynchronous. Ketika pengguna mengetik `/`, list menghasilkan command. Ketika isi list berubah melalui `SetItems`, command lain dapat dibutuhkan untuk menjalankan ulang filter aktif. Kalau root model hanya menangani key dan resize, message dari list tidak pernah sampai ke widget.

Devan menemukan masalah itu saat menguji filter `trivial`. Ia mengetik `/`, lalu `trivial`. Hasilnya kadang kosong setelah feature di-expand. Bukan karena data hilang, tetapi karena command list tidak dikembalikan ke event loop.

Myesha menunjuk bagian `Update`.

"Tidak semua message adalah milik aplikasi. Sebagian milik widget. Root model harus meneruskannya."

```go
func (a *App) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {
	case tea.BackgroundColorMsg:
		a.theme = newTheme(msg.IsDark())
		a.refreshContent()
		return a, nil
	case tea.WindowSizeMsg:
		a.width, a.height = msg.Width, msg.Height
		a.layout()
		a.refreshContent()
		return a, nil
	case tea.KeyPressMsg:
		return a.handleKey(msg)
	case tea.MouseWheelMsg:
		return a.handleWheel(msg)
	}

	var cmd tea.Cmd
	a.nav, cmd = a.nav.Update(msg)
	return a, cmd
}
```

Bug seperti ini menarik karena tampilan awal terlihat benar. Dashboard tampil. Browse tampil. Keyboard dasar bekerja. Namun, satu alur asynchronous dapat membuat fitur filter terasa tidak dapat dipercaya. TUI bukan hanya tentang menggambar string. Ia memiliki event loop, widget state, command, dan message routing.

Content pane memakai Glamour untuk merender Markdown. Wrap width harus dihitung dari ukuran pane. Ketika terminal berubah ukuran, Markdown harus dirender ulang karena lebar baris berubah.

```go
func renderMarkdown(content string, width int, isDark bool) string {
	style := "light"
	if isDark {
		style = "dark"
	}
	if width < 10 {
		width = 10
	}
	r, err := glamour.NewTermRenderer(
		glamour.WithStandardStyle(style),
		glamour.WithWordWrap(width),
	)
	if err != nil {
		return content
	}
	out, err := r.Render(content)
	if err != nil {
		return content
	}
	return out
}
```

`tasks.md` mendapat perlakuan khusus. Ketika dibuka, mode default adalah checklist. Phase memiliki progress bar sendiri. Task selesai memakai tanda `✓`. Task yang belum selesai memakai simbol lain. Marker `[P]` dan `[US1]` tampil sebagai badge. Ketika pengguna menekan `r`, viewer beralih ke raw Markdown.

Keputusan toggle ini menjawab dua kebutuhan yang berbeda. Checklist cocok untuk scan cepat. Raw Markdown cocok ketika pengguna perlu membaca struktur asli, menyalin isi, atau memeriksa detail formatting yang tidak terlihat pada tampilan khusus.

```go
func (a *App) refreshContent() {
	if a.currentPath == "" {
		a.vp.SetContent(
			"Select a file from the navigator.\n\n" +
				"Enter expands a feature; Enter on a file opens it here.",
		)
		return
	}
	contentWidth := a.contentPaneWidth() - 2
	if a.currentKind == model.FileTasks &&
		!a.rawMode && a.currentTasks != nil {
		a.vp.SetContent(renderChecklist(
			*a.currentTasks,
			contentWidth,
			a.theme,
		))
		return
	}
	a.vp.SetContent(renderMarkdown(
		a.currentRaw,
		contentWidth,
		a.theme.isDark,
	))
}
```

![Dashboard speckit-viewer dengan daftar feature dan fase](/assets/img/speckit-viewer/dashboard.png)

*Tampilan dashboard `speckit-viewer` dari gambar yang disediakan repository GitHub project.*

Dashboard itu adalah alasan mengapa gambar dari repository terasa penting untuk post ini. Ia memperlihatkan bentuk masalah yang ingin diselesaikan. Ketika pembaca hanya melihat daftar folder, mereka mungkin membayangkan file browser biasa. Ketika melihat table feature, phase, dan progress, tujuan viewer menjadi lebih mudah dipahami.

![Checklist tasks.md dengan progress per phase](/assets/img/speckit-viewer/tasks.png)

*Tampilan checklist `tasks.md` dari gambar yang disediakan repository GitHub project.*

Gambar kedua memperlihatkan perbedaan antara membaca daftar checkbox mentah dan membaca checklist yang memiliki phase progress. Viewer tidak mengubah isi file. Ia hanya menampilkan informasi yang sama dengan susunan yang lebih dekat dengan pertanyaan manusia.

Devan kemudian menambahkan status bar. Di sisi kiri, breadcrumb menunjukkan path seperti `specs/003-payroll/tasks.md`. Di sisi kanan, shortcut membantu pengguna mengingat action. Ketika terminal sempit, hint dikurangi dari kanan agar version tetap terlihat.

```text
↑↓ nav · Enter open · Tab switch pane · / filter · r raw
R refresh · d dashboard · c constitution · q quit · speckit dev
```

Status bar tersebut terasa seperti detail visual, tetapi ia menjaga alat tetap discoverable. Terminal memang cepat bagi pengguna yang sudah hafal command. Namun, viewer juga perlu membantu pengguna yang baru membukanya. Shortcut yang terlihat mengurangi kebutuhan untuk membuka README setiap kali lupa tombol.

Respons terhadap perubahan ukuran terminal juga menjadi perhatian. Banner ASCII hanya tampil ketika jendela cukup lebar dan tinggi. Pane memiliki ukuran yang dihitung ulang. Content re-render. Viewport dapat kembali ke atas ketika width berubah karena mempertahankan posisi scroll secara sempurna akan menambah kompleksitas yang tidak dibutuhkan MVP.

Myesha mengingatkan bahwa batas MVP harus dijaga.

"Kita tidak perlu draggable divider sekarang. Sidebar fixed width cukup. Kita tidak perlu file watcher sekarang. Tombol `R` sudah memberi refresh manual."

Devan awalnya ingin menggunakan `fsnotify` supaya perubahan dari agent langsung terlihat. Ide tersebut memang menarik. Ketika agent mengubah `tasks.md`, viewer dapat memperbarui progress tanpa command tambahan. Tetapi auto-refresh juga membawa pertanyaan baru: apakah content sedang dibaca ketika file berubah? Apakah scroll berpindah? Apakah perubahan terlalu sering membuat UI bergetar?

Mereka menunda file watcher. Bukan karena kebutuhan tersebut tidak penting, tetapi karena versi pertama harus membuktikan alur dasar lebih dulu. `R` cukup untuk menunjukkan bahwa dokumen adalah living document dan viewer dapat membaca ulang keadaan terbaru.

Saat semua bagian tersambung, Devan membuka project fixture. Ia menekan Enter pada dashboard. Navigator terbuka. Ia menekan Enter pada feature. File muncul. Ia memilih `tasks.md`. Checklist tampil. Ia menekan `r`. Markdown mentah muncul. Ia menekan `Tab`, mengetik `/trivial`, lalu memilih hasilnya. Setiap action terasa dekat dengan terminal yang selama ini ia gunakan.

Jovian mencoba mouse wheel.

"Di dashboard, scroll turun tiga row. Di sidebar, cursor berpindah. Di content, viewport scroll sendiri."

"Benar," jawab Devan. "Viewport menangani wheel secara native. Table dan list perlu kita terjemahkan menjadi cursor movement."

Mereka juga menguji terminal yang sempit. Banner harus hilang ketika ruang tidak cukup. Column name harus memiliki batas minimum agar tetap terbaca. Hint di status bar harus berkurang dari kanan jika tidak ada ruang. Content pane harus tetap memiliki lebar minimum supaya Glamour tidak menghasilkan baris yang terlalu rusak.

Devan sempat ingin menjaga semua hint tetap tampil. Hasilnya adalah status bar yang terpotong pada terminal kecil. Ia akhirnya memilih version tetap terlihat dan hint dikurangi berdasarkan ruang yang tersedia. Pilihan ini terdengar tidak penting sampai seseorang membuka viewer dari split pane terminal yang sempit. Pada saat itu, layout bukan sekadar hiasan. Layout menentukan apakah tool masih dapat dipakai.

Tema terang dan gelap juga perlu mengikuti terminal. Bubble Tea mengirim `BackgroundColorMsg` setelah aplikasi meminta background color. App memakai message tersebut untuk memilih theme dan Glamour standard style. Karena renderer Markdown dibuat berdasarkan mode gelap atau terang, content harus dirender ulang ketika theme berubah.

```go
func (a *App) Init() tea.Cmd {
	return tea.RequestBackgroundColor
}
```

Devan menyukai pola ini karena `App` tidak perlu menebak warna terminal dari environment. Ia meminta informasi kepada runtime, lalu menyesuaikan style. Jika style renderer gagal dibuat, fungsi render mengembalikan content asli. Fallback tersebut memastikan error styling tidak menghilangkan isi dokumen.

Ada juga pertanyaan tentang kapan file dibaca. `rescan` membaca struktur project dan parsing `tasks.md` untuk setiap feature. File detail baru dibaca ketika pengguna membukanya. Pendekatan lazy ini menjaga startup tetap ringan pada project yang memiliki banyak artefak. Scanner tahu path semua file, tetapi tidak perlu memuat semua isi Markdown ke memory sebelum pengguna memilihnya.

Ketika pengguna menekan `R`, project dipindai ulang. Feature list dibangun lagi. Dashboard mendapat row baru. Jika file yang sedang terbuka masih ada, content dibaca ulang. Jika `tasks.md` sedang terbuka, parser dijalankan lagi agar checklist dan phase progress ikut berubah.

```go
func (a *App) reloadCurrent() {
	if content, err := os.ReadFile(a.absOfCurrent()); err == nil {
		a.currentRaw = string(content)
		if a.currentKind == model.FileTasks {
			doc := parser.ParseTasks(a.currentRaw)
			a.currentTasks = &doc
		}
		a.refreshContent()
	}
}
```

Alur tersebut membuat refresh manual memiliki arti yang jelas. Ia bukan sekadar menggambar ulang layar. Ia membaca ulang sumber, mem-parsing ulang dokumen yang relevan, lalu merender ulang content. Ketika agent mengedit file di tab lain, Devan dapat memeriksa perubahan dengan satu tombol.

Jovian ingin tombol refresh diberi label `sync`.

"Jangan," kata Myesha. "Sync terdengar seperti dua sistem saling mengirim data. `R` hanya melakukan rescan dari filesystem. Sebut sesuai yang dilakukan."

Kata itu mengingatkan Devan untuk tidak memperbesar kemampuan melalui label. `R` adalah refresh. Ia tidak memanggil agent. Ia tidak menyimpan perubahan. Ia tidak menyelesaikan conflict. Ia hanya membaca keadaan terbaru dari disk.

Navigasi keyboard juga dibuat dengan aturan yang dapat diprediksi. `d` kembali ke dashboard. `c` membuka constitution jika tersedia. `Tab` berpindah antara navigator dan content. `/` memulai filter dari browse screen, bahkan ketika focus sedang berada di content. `Enter` membuka row yang dipilih atau memperluas feature. `q` keluar.

Saat `tasks.md` terbuka, `r` tidak berarti refresh. Ia berarti toggle raw dan checklist. Konflik shortcut ini dapat diterima karena action tersebut hanya berlaku dalam konteks tasks content. Di luar konteks itu, `r` tidak melakukan apa-apa. Shortcut yang memiliki scope jelas lebih mudah diingat daripada satu command global yang mencoba melakukan banyak hal.

Devan lalu meminta Myesha dan Jovian menguji tanpa membaca source code. Myesha mencari feature payroll. Jovian mencoba filter. Mereka beberapa kali menekan tombol yang salah, mengubah focus, dan membuka file yang tidak dikenal. Hasilnya menunjukkan bagian yang perlu diperbaiki bukan hanya kode, tetapi juga petunjuk di status bar dan pesan content kosong.

"Kalau belum ada file yang dibuka, tulisan ini cukup membantu," kata Myesha sambil membaca `Select a file from the navigator`. "Pengguna tahu harus menekan Enter."

Uji sederhana itu mengingatkan Devan bahwa TUI tidak memiliki mouse pointer yang selalu menjelaskan target. Focus harus terlihat dari border pane. Cursor harus memiliki posisi yang mudah dipahami. Shortcut harus tersedia ketika dibutuhkan. Interface yang minim visual tetap membutuhkan affordance.

Setelah sesi tersebut, Devan tidak menambahkan banyak widget. Ia hanya memperbaiki jalur utama: dashboard ke feature, feature ke file, file ke content, tasks ke checklist atau raw. Setiap tambahan dinilai dari pertanyaan yang sama: apakah ini membantu pengguna menelusuri artefak AI Agent?

Jika jawabannya tidak, ide itu masuk catatan masa depan. Catatan tersebut mencakup draggable divider, file watcher dengan `fsnotify`, wrapper npm, dan kemungkinan pencarian isi dokumen. Semua ide itu masuk akal. Namun, MVP harus lebih dulu membuat navigasi dasar terasa dapat dipercaya.

Batas tersebut juga membuat sesi pertama lebih mudah dijelaskan kepada pengguna baru. Mereka tidak perlu mempelajari konsep workspace, project database, atau konfigurasi sync. Mereka hanya perlu berada di root yang memiliki `specs/`, menjalankan binary, lalu memakai `↑`, `↓`, `Enter`, dan `Tab`. Jika mereka lupa, status bar memberi petunjuk yang cukup.

Devan merasa inilah kelebihan interface yang memiliki satu pekerjaan utama. Setiap tombol dapat dikaitkan dengan perjalanan membaca. Dashboard membantu memilih feature. Navigator membantu memilih artefak. Viewport membantu membaca. `r` memberi dua cara melihat `tasks.md`. `R` membaca perubahan terbaru. Tidak ada tombol yang mengharuskan pengguna memahami konsep internal Bubble Tea.

Perbedaan kecil itu menunjukkan bahwa TUI memiliki bahasa interaksi sendiri. Tidak semua widget menerima event dengan cara yang sama. Aplikasi harus mengarahkan input berdasarkan screen dan posisi pointer.

Malam itu, `speckit-viewer` mulai terlihat seperti alat yang dijanjikan namanya. Ia tidak menyelesaikan pekerjaan feature. Ia tidak menjalankan agent. Ia tidak menulis ulang Markdown. Tetapi ia membuat peta yang bisa dibaca tanpa meninggalkan terminal.

Devan menatap dua gambar hasil screenshot yang kemudian masuk ke README. Ia merasa lega bukan karena tampilannya sudah sempurna, melainkan karena masalah awalnya kini memiliki jawaban yang bisa disentuh. Ia tidak lagi harus mengingat semua path sebelum memahami project. Ia dapat mulai dari dashboard, memilih feature, lalu masuk ke artefak yang relevan.

Di luar, hujan mulai turun lagi. Terminal tetap menyala. Untuk pertama kalinya sejak mulai memakai GitHub Spec Kit, Devan merasa file-file yang dibuat AI Agent tidak lagi seperti jejak kaki yang tersebar. Jejak itu sudah memiliki peta.

## Bab 5: Membaca Kerja AI Agent tanpa Kehilangan Kendali

Pagi setelah UI selesai, Devan tidak langsung menambah feature baru. Ia kembali ke pertanyaan yang membuat `speckit-viewer` ada sejak awal: apakah alat ini benar-benar membantu memahami kerja AI Agent?

Ia membuat simulasi sederhana. Ia mengambil project fixture yang memiliki dua feature. Feature pertama memiliki dokumen lengkap dan beberapa task yang sudah selesai. Feature kedua hanya memiliki `spec.md`. Lalu ia membuka viewer dan membayangkan dirinya baru saja kembali ke project setelah beberapa jam pergi.

Dashboard memberikan jawaban awal.

```text
ID    Name                 Phase          Progress
003   Employee Payroll     Implementing   █████░░░░░ 3/6
007   Trivial Toggle       Specified      —
```

Dari sini ia tahu dua hal. Feature `003` bukan sekadar ada. Ia sudah memiliki task dan sebagian task selesai. Feature `007` baru berada di tahap spesifikasi. Ia belum perlu membuka semua file untuk membuat keputusan pertama.

Devan memilih `003`. `spec.md` terbuka. Ia membaca tujuan feature, user story, acceptance scenario, dan batasan. Setelah itu ia memperluas feature dari navigator dan membuka `plan.md`. Karena sidebar tetap berada di kiri, ia tidak kehilangan posisi. Ia dapat berpindah dari spesifikasi ke rencana dengan satu keyboard.

Kemudian ia membuka `tasks.md`. Checklist memperlihatkan phase dan task yang belum selesai. Ia melihat task dengan badge `[US1]` dan `[P]`. Ia dapat membedakan task paralel dari task yang memiliki urutan tertentu. Jika ingin memeriksa sintaks asli, ia menekan `r`.

Alur itu tidak menghilangkan kebutuhan untuk berpikir. Ia hanya mengurangi pekerjaan mekanis yang mengganggu berpikir.

Myesha memandang percobaan tersebut dari belakang kursi.

"Apa yang berubah dari cara kamu bekerja sebelum ada viewer?"

Devan menjawab setelah beberapa saat.

"Sebelumnya aku mulai dari path. Sekarang aku mulai dari pertanyaan. Aku ingin tahu feature mana yang belum selesai, lalu viewer membawaku ke file yang menjadi bukti."

Perubahan itu terdengar kecil, tetapi berpengaruh pada cara membaca hasil AI Agent. Ketika agent menghasilkan banyak file, manusia dapat merasa harus memeriksa semuanya dalam urutan file. Padahal, pemeriksaan yang baik biasanya dimulai dari tujuan, keputusan, dan pekerjaan tersisa. Dashboard memberi urutan tersebut tanpa menutup akses kepada file asli.

Di sini penting untuk menjelaskan apa yang tidak dilakukan `speckit-viewer`. Ia tidak menilai apakah isi `spec.md` benar. Ia tidak memeriksa apakah implementasi kode sesuai task. Ia tidak menjalankan command dari `plan.md`. Ia tidak mengubah checkbox. Ia tidak mengirim pesan ke AI Agent. Ia tidak mengetahui apakah semua task benar-benar selesai di production.

Batas ini bukan kekurangan yang harus disembunyikan. Batas ini adalah bagian dari desain.

Jika viewer mengedit `tasks.md`, ia harus menangani konflik ketika agent juga menulis file. Jika viewer menjalankan agent, ia harus mengelola permission, output, cancellation, dan error. Jika viewer mengklaim implementasi sudah selesai berdasarkan checkbox, ia dapat memberi rasa aman palsu. Dengan tetap menjadi viewer, project menjaga tanggung jawabnya tetap sempit dan dapat diuji.

Jovian menyebutnya seperti papan peta di ruang kerja.

"Peta tidak mengemudikan kendaraan. Peta hanya membantu kita tahu posisi dan arah."

"Benar," kata Myesha. "Dan karena peta tidak mengemudikan kendaraan, kita masih harus melihat jalan yang sebenarnya."

Analogi itu cocok untuk AI Agent. Agent dapat membantu mengubah ide menjadi dokumen dan kode. Manusia tetap perlu membaca spesifikasi, memahami rencana, memeriksa task, menjalankan test, dan menilai dampaknya. `speckit-viewer` berada di tengah alur tersebut sebagai alat orientasi.

Devan lalu memikirkan distribusi. Ia bekerja dari terminal, tetapi tidak ingin setiap orang harus clone source lalu menjalankan `go run .`. Repository menyiapkan beberapa jalan.

Dengan Go, pengguna dapat memasang binary dari source.

```bash
```

README juga menyediakan Homebrew untuk macOS dan Linux.

```bash
brew install khairu-aqsara/tap/speckit
```

Ada install script untuk mengunduh release sesuai operating system dan arsitektur.

```bash
curl -fsSL https://raw.githubusercontent.com/khairu-aqsara/speckit-viewer/main/install.sh | sh
```

Dan setelah terpasang, penggunaan dasarnya singkat.

```bash
speckit [path]
```

Tanpa path, program memakai current directory. Dengan path, program dapat membuka project Spec Kit lain.

Distribusi binary dibantu GoReleaser. Konfigurasinya menargetkan darwin, linux, dan windows dengan amd64 serta arm64. Build memakai `CGO_ENABLED=0`, sehingga hasilnya dapat menjadi executable yang lebih mudah dipindahkan. Binary bernama `speckit`, sedangkan module repository tetap `github.com/wenkhairu/speckit-viewer`.

```yaml
builds:
  - main: .
    binary: speckit
    env:
      - CGO_ENABLED=0
    ldflags:
      - -s -w -X main.version={{.Version}}
    goos: [darwin, linux, windows]
    goarch: [amd64, arm64]
```

Version disisipkan melalui `ldflags`. Karena itu `speckit --version` dapat menampilkan versi release, sedangkan build lokal menampilkan `dev` jika tidak diberi nilai lain.

Jovian menunjuk install script.

"Script ini juga harus berhati-hati kalau `/usr/local/bin` tidak writable."

Devan membuka script tersebut. Script memeriksa OS dengan `uname`, memetakan arsitektur seperti `x86_64` atau `arm64`, mengambil tag release terbaru dari GitHub API, mengunduh archive, lalu memasang binary. Jika directory install tidak writable, script mencoba membuatnya dengan `sudo` dan memindahkan binary setelah itu.

"Distribution bukan hanya membuat binary," kata Myesha. "Ia membuat jalur dari niat pengguna sampai command yang bisa dijalankan."

Kalimat tersebut membuat Devan melihat project secara lebih utuh. Ia bukan hanya membangun UI. Ia membuat alat yang harus dipahami, dipasang, dijalankan, dan dipercaya.

Bagian kepercayaan terutama datang dari test. Core project memiliki test untuk scanner, parser, dan phase inference. Test scanner memeriksa bahwa folder dengan pola numeric prefix diterima, folder biasa ditolak, file dikenali, dan feature diurutkan berdasarkan ID. Test parser memeriksa checkbox campuran, badge parallel, user story, phase kosong, task tanpa header, dan section non-task. Test phase memeriksa semua kondisi inferensi.

UI juga memiliki test untuk filter flow. Test tersebut tidak hanya memanggil fungsi filter. Ia mensimulasikan pesan Bubble Tea, menjalankan command yang dikembalikan widget, mengetik query, menerapkan hasil, lalu melakukan expand. Test itu menangkap bug yang tidak terlihat pada unit test parser.

Devan menyukai pembagian test tersebut.

"Pure logic diuji dengan input kecil. UI diuji melalui message flow. Kita tidak perlu menjadikan semua test sebagai screenshot test."

Myesha mengangguk. "Pisahkan hal yang bisa dipastikan dari hal yang perlu dirasakan. Parser dapat dipastikan dengan assertion. Kenyamanan layout tetap perlu dilihat di terminal."

Repository juga memiliki fixture `minimal-project` dan `full-project`. Fixture minimal menunjukkan project kecil dengan feature yang memiliki `spec.md`, `plan.md`, dan `tasks.md`. Fixture penuh memiliki dokumen tambahan, checklist, contract, constitution, dan feature yang hanya memiliki spesifikasi. Dengan dua bentuk itu, viewer diuji pada project yang tidak seragam.

Variasi tersebut penting karena AI Agent tidak selalu menghasilkan urutan yang sama. Satu prompt dapat menghasilkan semua artefak. Prompt lain mungkin berhenti setelah spesifikasi. Manusia juga dapat mengedit dokumen di antara langkah agent. Viewer yang hanya bekerja pada project lengkap akan gagal pada momen yang justru paling membutuhkan orientasi.

Setelah memeriksa test, Devan menjalankan alur terhadap project nyata yang memiliki banyak feature. Ia melihat puluhan row muncul. Fase dapat disimpulkan. Constitution dapat dibuka. Spec dan tasks dapat dibaca. Ia tidak perlu membuat fixture baru untuk setiap ukuran project.

Ia lalu mengubah satu checkbox di `tasks.md` dari belum selesai menjadi selesai. Viewer masih terbuka. Ia menekan `R`.

Progress berubah.

```text
Implementing 3/4
```

menjadi:

```text
Implemented
```

Tidak ada watcher. Tidak ada event kompleks. Hanya rescan manual. Tetapi perubahan itu cukup untuk memperlihatkan karakter penting dokumen Spec Kit: living document. File dapat berubah sementara viewer terbuka. Viewer harus memiliki cara untuk membaca keadaan terbaru.

Devan merasa ada sesuatu yang berubah di dalam dirinya. Dulu ia melihat file AI Agent sebagai hasil akhir yang harus dibaca setelah semua proses selesai. Sekarang ia melihat file tersebut sebagai permukaan kerja yang dapat dipantau. `spec.md`, `plan.md`, dan `tasks.md` menjadi jejak keputusan yang dapat dikunjungi ulang.

Ia teringat rasa lelah di awal. Saat itu terminal terasa seperti lorong. Sekarang terminal tetap penuh teks, tetapi ia memiliki beberapa tanda arah. Dashboard menunjukkan feature. Phase menunjukkan ringkasan. Navigator menunjukkan hubungan file. Content pane menjaga isi asli. Checklist menunjukkan progress task. Tombol `R` mengakui bahwa dokumen masih dapat berubah.

Jovian duduk di lantai dan menatap layar.

"Bang, apakah setelah ada viewer kamu jadi tidak perlu membaca kode?"

"Tetap perlu," jawab Devan. "Viewer hanya membantuku menemukan konteks sebelum membaca kode."

Myesha menambahkan, "Itu perbedaan antara melihat dan memahami. Alat dapat membantu melihat lebih cepat. Memahami tetap membutuhkan manusia."

Kalimat itu menjadi penutup yang tepat untuk project ini. `speckit-viewer` dibuat karena Devan merasa kesulitan menelusuri implementasi AI Agent dengan GitHub Spec Kit, terutama karena ia menghabiskan sebagian besar waktu di terminal. Jawabannya bukan memaksa diri keluar dari terminal. Jawabannya adalah membuat terminal mampu menunjukkan struktur yang selama ini tersembunyi di antara file.

Dari project ini, ada beberapa pelajaran yang mereka bawa pulang.

Pertama, artefak AI Agent perlu diperlakukan sebagai dokumen kerja, bukan output sementara. Jika spesifikasi, rencana, riset, model data, dan task disimpan sebagai Markdown, manusia memiliki kesempatan untuk memeriksa proses, bukan hanya hasil akhir.

Kedua, alat navigasi tidak harus mengambil alih workflow. Viewer yang membaca dengan jujur dapat lebih berguna daripada alat besar yang ingin menjalankan semua hal. Scope sempit membuat perilaku lebih mudah dipahami.

Ketiga, status dapat diinferensikan jika sumber data tidak memiliki field status. Namun, inferensi harus diberi nama dan batas yang jelas. `Implementing 3/6` berarti tiga dari enam task dicentang. Itu tidak berarti production sudah selesai. Bahasa interface perlu menghormati perbedaan tersebut.

Keempat, terminal adalah interface yang serius. Ia dapat memiliki dashboard, dua pane, filter, progress bar, syntax rendering, mouse wheel, dan responsive layout. Ia tidak harus menjadi salinan aplikasi web. Ia dapat menggunakan kekuatan terminal: keyboard, path, process, dan kedekatan dengan repository.

Kelima, rasa sulit menelusuri pekerjaan sering berasal dari kurangnya peta, bukan kurangnya data. Devan sudah memiliki file-file yang dibutuhkan sejak awal. Ia hanya membutuhkan cara untuk melihat hubungan dan posisi file tersebut.

Dalam penggunaan sehari-hari, alur yang paling berguna justru tidak panjang. Devan membuka repository yang sedang dikerjakan, menjalankan `speckit .`, melihat dashboard, lalu memilih feature dengan phase yang ingin diperiksa. Ia membaca `spec.md` untuk mengingat tujuan. Ia membuka `plan.md` untuk memahami keputusan teknis. Ia membuka `tasks.md` untuk melihat pekerjaan yang tersisa. Jika agent masih berjalan di tab lain, ia menekan `R` setelah agent menyelesaikan satu langkah besar.

Alur itu membuat review menjadi lebih teratur. Devan tidak lagi menerima hasil agent sebagai satu paket besar yang harus dipercayai sekaligus. Ia dapat memeriksa urutannya. Spesifikasi menjawab kebutuhan. Rencana menjawab pendekatan. Task menjawab pekerjaan. Checklist menjawab keadaan daftar. Code review dan test tetap menjawab implementasi sebenarnya.

Myesha menyebut pembagian itu sebagai tangga kepercayaan. Setiap artefak memberi satu pijakan. Tidak semua pijakan membuktikan pijakan berikutnya, tetapi semuanya membantu manusia naik tanpa melompat dalam gelap.

"Agent tetap bisa salah," katanya. "Viewer tidak menghilangkan risiko itu. Viewer membuat kesalahan lebih mudah ditemukan karena dokumen tidak tersebar."

Devan memikirkan kata "ditemukan". Itulah manfaat yang paling realistis dari tool ini. Ia tidak dapat menjamin kualitas prompt. Ia tidak dapat menjamin kualitas kode. Ia tidak dapat menjamin bahwa checkbox benar-benar diperbarui oleh proses implementasi. Namun, ia dapat mengurangi peluang bahwa manusia melewatkan dokumen penting hanya karena path-nya terlalu banyak.

Project ini juga mengajarkan bahwa developer tool perlu memiliki jalan keluar yang jelas. Karena viewer hanya membaca filesystem, pengguna dapat keluar kapan saja dan kembali ke editor. Tidak ada database yang harus diekspor. Tidak ada workspace yang mengunci dokumen. Tidak ada format proprietary. Jika binary dihapus, file Spec Kit tetap menjadi Markdown biasa.

Jovian menyukai bagian itu.

"Berarti viewer tidak menjadi rumahnya. Ia hanya menjadi jendela."

"Iya," jawab Devan. "Rumahnya tetap repository."

Pernyataan tersebut membantu menjaga hubungan antara tool dan source. Ketika alat developer menyimpan salinan data, salinan itu dapat menjadi sumber kebingungan baru. `speckit-viewer` memilih membaca source saat dibutuhkan. Ia menyimpan state UI seperti feature yang diperluas dan file yang terbuka, tetapi tidak membuat salinan permanen dari artefak.

Ada kemungkinan masa depan untuk file watcher, search isi, atau integrasi dengan agent. Namun, semua kemungkinan itu harus menjawab pertanyaan yang sama: apakah ia membantu manusia bergerak dari hasil kerja agent menuju keputusan yang lebih baik? Jika tidak, ia hanya menambah permukaan aplikasi.

Devan menutup daftar future work setelah menulis tiga item terakhir.

```text
Future work yang perlu alasan kuat:
- fsnotify untuk refresh otomatis
- pencarian isi Markdown
- wrapper npm untuk npx
```

Ia tidak menulis "AI summary". Bukan karena summary AI tidak dapat dibuat, tetapi karena project ini sedang berusaha menjaga hubungan langsung dengan source. Menambahkan summary generatif akan membawa pertanyaan baru tentang cache, akurasi, prompt, dan apakah ringkasan tersebut dapat dipercaya. Mungkin ada tempat untuk itu pada tool lain. Untuk viewer ini, raw Markdown dan ringkasan deterministik sudah cukup sebagai awal.

Malam semakin sepi. Devan membuka GitHub repository dari browser hanya untuk melihat README yang sudah memiliki dua screenshot. Gambar dashboard menunjukkan feature dan phase. Gambar checklist menunjukkan task per phase. Tidak ada gambar yang mencoba menjual project sebagai sesuatu yang lebih besar dari kenyataannya.

Ia merasa itu cocok. Project ini dibuat dari rasa kesulitan yang sederhana. Ia tidak membutuhkan klaim besar. Ia hanya ingin menjawab satu pertanyaan yang sering muncul ketika bekerja dengan AI Agent: "Sebenarnya project ini sedang berada di mana?"

Sekarang jawabannya bisa dimulai dari dashboard. Dari sana, manusia masih perlu membaca. Masih perlu bertanya. Masih perlu memeriksa kode. Masih perlu menjalankan test. Tetapi langkah pertamanya tidak lagi berupa pencarian tanpa peta.

Malam terakhir pada minggu itu, mereka bertiga duduk di ruang kerja. Tidak ada hujan besar. Hanya suara kipas laptop dan beberapa command yang selesai dijalankan.

Devan membuka `speckit-viewer` sekali lagi.

```bash
speckit .
```

Dashboard muncul. Banner ASCII tampil sebentar sebelum ruang kerja memenuhi layar. Devan memilih feature. Myesha membaca `spec.md`. Jovian membuka `tasks.md` dan menekan `r` hanya untuk melihat apa yang berubah dari checklist ke Markdown mentah.

Tidak ada yang terlihat spektakuler bagi orang yang tidak mengalami masalah awalnya. Hanya tabel, list, progress bar, dan dokumen Markdown di terminal. Namun, bagi Devan, interface kecil itu menghapus jarak mental yang selama ini mengganggu.

Ia tidak lagi merasa harus mengingat seluruh repository sebelum dapat mulai membaca. Ia tidak lagi harus membuka sepuluh file untuk mengetahui feature mana yang sedang berjalan. Ia tidak lagi harus menghitung checkbox dengan mata. Ia juga tidak lagi menganggap terminal sebagai tempat yang hanya cocok untuk command singkat.

Myesha menutup laptopnya.

"Jadi, apa nama pelajaran minggu ini?" tanya Myesha.

Devan berpikir sebentar.

"Kalau AI Agent meninggalkan banyak jejak, kita tidak selalu membutuhkan lebih banyak log. Kadang kita membutuhkan peta yang membuat jejak itu bisa dibaca."

Jovian mengangguk sambil mengembalikan kabel charger ke tempatnya.

"Dan kalau petanya ada di terminal, kita tidak perlu pindah rumah."

Di Sleman, layar `speckit-viewer` tetap menyala beberapa menit lebih lama. Bukan karena Devan masih tersesat, tetapi karena ia akhirnya dapat melihat perjalanan project-nya sendiri. Di antara `spec.md`, `plan.md`, `tasks.md`, dan baris-baris kode yang dibuat agent, ada cerita tentang keputusan, keraguan, pekerjaan yang sudah selesai, dan pekerjaan yang masih menunggu.

Viewer itu tidak mengambil alih cerita tersebut. Ia hanya menyalakan lampu di lorongnya.

Dan kadang, untuk kembali memegang kendali atas pekerjaan yang besar, lampu kecil seperti itu sudah cukup.

Kalau kamu ingin melihat implementasi, screenshot, fixture, dan perkembangan project-nya secara langsung, repository `speckit-viewer` tersedia di [GitHub](https://github.com/khairu-aqsara/speckit-viewer). Silakan mampir, baca README-nya, lalu lihat bagaimana sebuah rasa kesulitan kecil di terminal bisa berubah menjadi alat yang membantu membaca jejak kerja AI Agent.
