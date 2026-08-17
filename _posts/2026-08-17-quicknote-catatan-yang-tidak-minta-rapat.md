---
layout: post
title: "QuickNote: Catatan Kecil yang Tidak Minta Rapat Panjang"
subtitle: "Kisah Devan, Myesha, dan Jovian membangun aplikasi note cepat karena menulis satu kalimat tidak seharusnya dimulai dari memilih workspace."
date: 2026-08-17 20:00:00 +0700
categories: [Engineering, Story, Productivity]
tags: [quicknote, tauri, rust, typescript, markdown, codemirror, autosave]
author: Kuli Kode
---

Ada jenis ide yang datang ketika kita sedang tidak siap. Ia muncul saat menunggu air mendidih, saat baru membuka terminal, atau saat tangan sudah memegang gagang pintu. Ide itu tidak selalu meminta dokumen rapi. Kadang ia hanya meminta satu tempat untuk ditulis sebelum menguap.

QuickNote lahir dari kebutuhan yang kecil itu. Ia bukan usaha untuk mengalahkan Obsidian, Notion, atau editor besar lain. Ia juga bukan ruang kerja digital yang ingin mengatur seluruh hidup penggunanya. QuickNote hanya ingin menjadi selembar kertas digital yang selalu dekat, bisa dibuka dalam hitungan detik, lalu menerima kalimat pertama tanpa meminta banyak syarat.

## Bab 1: Satu Kalimat yang Tersesat di Sleman

Malam di Sleman sedang tenang ketika Devan mendapat sebuah ide yang terlalu cepat untuk dipikirkan lama-lama. Ia duduk di meja kerja dekat jendela, dengan laptop terbuka, segelas teh yang mulai dingin, dan layar penuh tab. Ada tab dokumentasi, tab issue tracker, tab catatan rapat, tab aplikasi note, dan satu tab kosong yang entah sejak kapan tidak pernah ditutup.

Devan baru saja menemukan sebuah solusi untuk masalah kecil di salah satu proyeknya. Solusinya bukan terobosan besar. Ia hanya sebuah kalimat pendek tentang urutan pemeriksaan pada proses autosave. Kalimat itu penting karena mungkin akan menyelamatkan satu jam debugging pada minggu depan.

Ia ingin mencatatnya.

Masalahnya, mencatat kalimat itu terasa seperti memulai proyek baru.

Devan membuka aplikasi note yang biasa ia pakai. Aplikasi itu hebat. Di dalamnya ada workspace, folder, subfolder, tag, database, template, panel pencarian, panel backlink, dan beberapa tombol yang belum pernah ia sentuh. Aplikasi itu bisa menjadi rumah pengetahuan yang bagus. Untuk kebutuhan Devan malam itu, aplikasi tersebut terasa seperti gedung kantor yang meminta tamu mengisi formulir sebelum boleh menulis nomor telepon di secarik kertas.

Ia menggerakkan kursor ke ikon tambah. Muncul pilihan template. Ia menutupnya. Muncul pilihan lokasi. Ia menutupnya. Ia melihat panel kiri yang berisi puluhan catatan. Beberapa nama terdengar penting, tetapi tidak ada yang terasa tepat untuk satu kalimat kecil tadi.

"Aku cuma mau nulis satu baris," gumam Devan. "Kenapa rasanya seperti mau menyusun perpustakaan?"

Kalimat itu belum hilang dari kepalanya, tetapi tenaga untuk mengejar kalimat tersebut mulai habis. Ia akhirnya membuka file Markdown biasa di editor kode. Cara itu berhasil, tetapi juga tidak benar-benar nyaman. Ia harus mencari folder, membuat nama file, memilih apakah catatan ini masuk ke proyek tertentu, lalu menutup editor kode yang memiliki terlalu banyak hal di sekeliling teks.

Di tengah kebingungan itu, Myesha datang membawa dua cangkir teh. Kakaknya baru selesai membaca sesuatu dari ruang tengah. Ia melihat layar Devan, lalu melihat wajah adiknya yang tampak lebih lelah daripada masalah yang sedang ia pecahkan.

"Bang, kamu sedang memperbaiki bug atau sedang mencari rumah untuk satu kalimat?" tanya Myesha.

Devan memutar laptopnya. "Aku cuma mau mencatat satu ide. Aplikasi note yang kupakai terlalu lengkap. Editor kode terlalu ramai. File biasa memang gampang, tapi aku harus memikirkan tempat dan nama file. Kadang ide keburu hilang sebelum catatannya jadi."

Myesha duduk. Ia tidak langsung memberi solusi. Ia tahu Devan sering ingin membangun sesuatu sebelum masalahnya selesai diceritakan. Dari kamar sebelah, Jovian muncul sambil membawa roti panggang. Adik bungsu mereka punya kebiasaan masuk ke percakapan pada bagian yang paling menarik, biasanya tanpa membawa konteks dari awal.

"Kalau catatannya cuma satu, kenapa tidak pakai kertas?" tanya Jovian.

Devan menunjuk layar. "Karena aku ingin Markdown. Aku ingin bisa menyimpan kode, checklist, judul, dan catatan biasa. Aku juga ingin file-nya tetap punya aku. Bisa dibuka di editor lain, bisa dibackup, bisa dimasukkan ke Git."

"Berarti bukan aplikasi note yang besar," kata Jovian sambil duduk. "Kamu butuh kertas yang mengerti Markdown."

Kalimat Jovian terdengar sederhana, tetapi justru karena itu ia menempel di kepala Devan. Kertas yang mengerti Markdown. Bukan knowledge base. Bukan workspace. Bukan pengganti semua aplikasi. Hanya satu permukaan untuk menaruh sesuatu dengan cepat.

Myesha mengambil pulpen dan menulis di belakang struk belanja yang ada di meja.

```text
Open QuickNote
      -> editor langsung siap
      -> ketik
      -> Markdown tampil di tempat
      -> autosave
      -> tutup
      -> catatan tetap ada
```

"Kalau alurnya lebih panjang dari ini, kita harus punya alasan yang sangat kuat," ujar Myesha. "Pengguna tidak membuka aplikasi ini untuk mengelola dunia. Mereka membuka aplikasi ini karena ada sesuatu yang harus ditangkap sekarang."

Devan memandangi enam baris itu. Selama ini ia sering menganggap fitur sebagai bukti bahwa sebuah aplikasi serius. Semakin banyak kemampuan, semakin besar nilai yang ia bayangkan. Namun, pengalaman malam itu menunjukkan sisi lain. Setiap fitur yang tidak membantu kalimat pertama juga menambah jarak antara niat dan catatan.

"Jadi QuickNote bukan versi kecil dari Notion atau Obsidian?" tanya Devan.

"Bukan," jawab Myesha. "Dan kita harus berani mengatakan itu sejak awal. Obsidian bagus untuk jaringan pengetahuan, tautan antarhalaman, dan arsip yang tumbuh. Notion bagus untuk workspace, database, dan kolaborasi. QuickNote punya pekerjaan yang lebih sempit. Ia membuka pintu secepat mungkin, menerima satu note, lalu tidak mengganggu."

Jovian mengangkat tangan seperti sedang mengikuti kelas. "Kalau begitu, kita tidak perlu workspace, tab, plugin, sync, akun, database, dan server."

"Tepat," kata Myesha. "Bukan karena semua itu buruk. Kita menghapusnya karena semua itu bukan bagian dari pekerjaan QuickNote."

Devan mulai menulis daftar kebutuhan. Ia menulis satu note saja, file Markdown yang terlihat, editor yang siap mengetik, rendering Markdown langsung, autosave, shortcut global, dan kemampuan untuk tetap berjalan di menu bar. Ia juga menulis satu kalimat dengan huruf besar.

```text
Jangan pernah kehilangan karakter yang sudah diketik pengguna.
```

Kalimat itu membuat suasana berubah. Membuat editor sederhana memang mudah jika definisi sederhananya hanya tampilan kosong. Membuat editor yang tidak menghilangkan teks ketika aplikasi crash, ketika file berubah dari editor lain, atau ketika pengguna menekan tombol tutup membutuhkan keputusan yang lebih serius.

"Nah," kata Myesha, menunjuk daftar itu, "di sinilah aplikasi kecil mulai punya tanggung jawab besar. Tampilan boleh minimal. Perilaku penyimpanannya tidak boleh asal."

Devan mengangguk. Ia menghapus beberapa ide yang tadi ingin ia masukkan. Ia sempat membayangkan banyak folder otomatis, sistem tag, sinkronisasi cloud, dan halaman dashboard. Semua itu sekarang terasa seperti suara ramai di luar jendela. Ada manfaatnya, tetapi suara itu tidak dibutuhkan untuk menangkap satu kalimat.

Jovian membaca daftar tersebut. "Bang, bagaimana kalau note-nya disimpan di satu file yang benar-benar bisa kamu lihat? Bukan di database tersembunyi."

"Itu penting," jawab Devan. "Kalau besok aplikasi ini tidak dipakai lagi, catatanku tidak boleh ikut terkunci di dalam aplikasi."

"Berarti file itu sumber kebenarannya," kata Myesha. "Editor hanya cara yang nyaman untuk mengubah isi file. Markdown bukan format ekspor. Markdown adalah data utamanya."

Mereka berhenti sebentar. Di luar, suara kendaraan dari jalan kecil terdengar lalu menjauh. Lampu ruang kerja memantul di permukaan meja. Devan mengambil napas dan membuka terminal.

Ia membuat direktori proyek bernama `quick-note`. Nama itu tidak dibuat untuk terdengar besar. Nama tersebut sengaja langsung menyebut pekerjaan aplikasinya. QuickNote.

```bash
mkdir quick-note
cd quick-note
npm init -y
```

Jovian tertawa kecil. "Kalau nanti kita menambahkan dua puluh menu, aku akan mengingatkan nama proyek ini."

"Kalau menu itu membuat catatan lebih cepat, kita pertimbangkan," balas Devan.

Myesha menggeleng. "Bukan begitu cara kita menilainya. Pertanyaannya bukan apakah fitur itu keren. Pertanyaannya: apakah fitur itu membuat QuickNote lebih cepat, lebih sederhana, atau lebih nyaman untuk quick note?"

Pertanyaan tersebut lalu menjadi pagar pertama proyek. Setiap kali ada ide baru, mereka kembali ke kalimat yang sama. Jika jawabannya tidak jelas, ide itu tidak masuk. Jika jawabannya hanya "mungkin berguna nanti", ide itu juga tidak masuk. QuickNote tidak dibangun untuk memuaskan semua kebutuhan. Ia dibangun untuk menjaga momen kecil sebelum momen tersebut hilang.

Devan menatap kembali kalimat yang ingin ia simpan tadi. Ia mengetiknya untuk pertama kali di file `notes.md`.

```markdown
Urutan autosave harus menjaga versi yang sedang dibuka sebelum menulis versi baru.
```

Kalimat itu akhirnya tersimpan. Tidak ada workspace yang harus dipilih. Tidak ada folder yang harus ditentukan. Tidak ada dialog yang menanyakan template. Hanya teks, lalu file.

Namun, mereka belum tahu bahwa kalimat kecil itu akan membawa mereka ke masalah yang lebih dalam. Kalau aplikasi boleh terasa sederhana, bagaimana cara membuatnya tetap aman? Kalau file boleh diedit dari mana saja, bagaimana cara QuickNote tahu bahwa isinya berubah? Kalau pengguna menutup jendela ketika autosave masih berjalan, siapa yang harus menunggu?

Malam itu mereka belum menyelesaikan jawabannya. Devan baru memiliki nama proyek dan satu file kosong. Tetapi untuk pertama kalinya, masalahnya terasa jujur. Mereka tidak sedang mencoba membuat aplikasi yang bisa melakukan semuanya. Mereka sedang mencoba menghilangkan satu lapis hambatan antara pikiran dan catatan.

Di Sleman, menjelang tengah malam, tiga bersaudara itu menyepakati kalimat produk yang kemudian menjadi kompas mereka:

> **Type it. Close it. It's still there.**

Kalimatnya pendek. Tanggung jawab di baliknya tidak pendek sama sekali.

Sebelum tidur, mereka melakukan satu latihan yang tidak terlihat seperti pekerjaan engineering. Mereka masing-masing mengambil lima situasi ketika sebuah ide kecil pernah hilang. Devan menulis idenya di terminal, tetapi lupa menyimpan file. Myesha mendapat gagasan saat berada di antara dua meeting, lalu tidak ingin membuka aplikasi yang meminta login. Jovian menulis command di chat pribadi, lalu tidak bisa menemukannya dua hari kemudian.

Mereka tidak menghitung berapa banyak fitur yang dimiliki aplikasi note yang sedang dipakai. Mereka menghitung langkah sebelum kalimat pertama muncul. Membuka launcher. Mencari nama aplikasi. Menunggu window. Memilih workspace. Memilih folder. Menentukan jenis halaman. Menutup template. Menulis judul. Baru setelah itu menulis isi. Setiap langkah terlihat kecil. Jika semua langkah dijumlahkan pada saat pikiran sedang cepat, jumlahnya menjadi alasan untuk menyerah.

Myesha membuat tabel sederhana.

| Kebutuhan | Langkah yang ingin dihapus |
|---|---|
| Menulis ide | Memilih workspace sebelum mengetik |
| Menyimpan kode | Membuat dokumen khusus untuk potongan pendek |
| Membuat checklist | Membuka panel dan template |
| Menemukan catatan | Mengingat folder yang tepat |
| Menutup aplikasi | Menekan save manual atau menunggu indikator |

"Kita bukan sedang membuat orang malas mengatur catatan," jelas Myesha. "Kita sedang mengakui bahwa mengatur dan menangkap adalah dua fase yang berbeda."

Devan menyukai pembagian itu. Selama ini ia memaksa fase menangkap untuk mengikuti aturan fase mengatur. Ia ingin ide baru langsung punya tempat permanen. Padahal, banyak ide perlu tidur dulu sebelum diketahui nilainya. Catatan cepat menjadi ruang transit. Ia tidak harus langsung rapi agar berguna.

Jovian mengusulkan satu percobaan. Ia menyalakan stopwatch, membuka aplikasi note yang lengkap, dan mencoba menulis kalimat berikut:

```text
Besok cek apakah retry pada save bisa memakai generation counter.
```

Stopwatch berhenti setelah beberapa langkah. Ia lalu mengulang dengan file Markdown biasa. Kali ini langkahnya lebih sedikit, tetapi ia harus memikirkan folder dan nama file. Terakhir, ia menggambarkan QuickNote yang belum ada: shortcut, window, cursor, dan satu file tetap.

"Yang kita kejar bukan membuat stopwatch menjadi nol," kata Jovian. "Kita ingin langkah pertama tidak terasa seperti keputusan besar."

Percobaan itu juga menunjukkan bahaya dari definisi "cepat" yang terlalu dangkal. Aplikasi dapat dibuka cepat, tetapi jika pengguna harus mengurus struktur sebelum mengetik, pengalaman tetap lambat. Aplikasi dapat memiliki shortcut, tetapi jika shortcut membuka dashboard penuh, perhatian tetap pecah. Kecepatan QuickNote bukan hanya waktu startup. Kecepatan adalah jarak mental antara pikiran dan teks.

Myesha meminta Devan menulis prinsip tersebut dalam bahasa yang dapat dipakai saat code review. Mereka memilih beberapa kalimat pendek:

- Editor siap ketika window muncul.
- Note utama adalah file Markdown yang terlihat.
- Tampilan boleh pintar, tetapi source tetap plain text.
- Fitur tambahan harus muncul ketika diminta.
- Shutdown harus menunggu pending write.
- Kegagalan tidak boleh menghapus versi pengguna atau versi eksternal.

Devan menganggap prinsip terakhir paling mahal. Ia pernah kehilangan catatan karena aplikasi crash setelah menganggap save selesai. Catatan itu hanya berisi beberapa command, tetapi waktu untuk mengingat dan menulis ulang jauh lebih mahal daripada ukuran filenya. Sejak saat itu, ia tidak lagi menganggap small note sebagai small risk.

Mereka juga membahas apakah satu note berarti satu file selamanya. Myesha menjawab tidak. Versi pertama memegang satu note karena satu note memberi fokus yang tegas. Pengguna tetap dapat memindahkan atau mengganti file. Ia dapat memakai `notes.md`, `meeting.md`, atau file yang berada di folder proyek. Yang tidak ada adalah katalog internal yang membuat aplikasi harus mengetahui semua halaman.

"Kalau kita menyimpan daftar semua file, kita mulai membangun workspace," ujar Myesha. "Begitu kita membangun workspace, akan muncul folder, tab, recent files, dan banyak keputusan lain."

Devan tertawa. "Satu feature bisa memanggil saudara-saudaranya."

"Dan saudara-saudaranya membawa sepupu," tambah Jovian.

Mereka sadar bahwa scope creep tidak selalu datang sebagai permintaan besar. Ia sering datang sebagai jawaban yang tampak masuk akal untuk satu edge case. Pengguna ingin membuka file lain, maka dibuat recent files. Pengguna ingin melihat beberapa note, maka dibuat tab. Pengguna ingin mengelompokkan note, maka dibuat folder. Pengguna ingin mencari semua note, maka dibuat index. Setiap jawaban bisa berguna, tetapi rangkaiannya mengubah produk.

Karena itu, QuickNote menyediakan pemilihan path tanpa menjadikan daftar file sebagai pusat interface. File picker boleh muncul saat pengguna memintanya. Setelah file dipilih, editor kembali menjadi fokus. Tidak ada sidebar yang terus mengingatkan semua kemungkinan.

Ketika jam sudah lewat tengah malam, Devan menutup laptop. Ia tidak merasa sudah membangun banyak hal. Ia baru membuat dokumen kebutuhan, satu prototipe kecil, dan sebuah slogan. Namun, ia merasa memiliki batas yang sebelumnya tidak ada.

Di perjalanan menuju kamar, ia melewati ruang keluarga dan melihat secarik struk belanja yang dipakai Myesha untuk menggambar alur. Di bagian bawah struk, ada catatan lain yang ditulis dengan cepat:

```text
Jangan membuat user mengurus alat ketika yang mereka butuhkan hanya tempat.
```

Kalimat itu menjadi bagian dari cerita QuickNote. Aplikasi ini bukan tempat untuk semua pekerjaan. Ia adalah tempat kecil yang siap sebelum pengguna sempat menyesal karena tidak mencatat.

## Bab 2: Editor yang Membiarkan Markdown Bernapas

Pagi berikutnya, Devan membuka proyek QuickNote dengan semangat yang masih rapuh. Ide semalam terasa masuk akal ketika dibicarakan, tetapi implementasi sering memiliki cara sendiri untuk membongkar keyakinan. Ia mulai dari pertanyaan paling dasar: apa yang sebenarnya dilihat pengguna ketika aplikasi dibuka?

Jawaban awalnya adalah layar kosong dengan kursor yang langsung berkedip. Tidak ada sidebar. Tidak ada file explorer. Tidak ada tab. Tidak ada preview pane. Tetapi layar kosong bukan berarti editor tidak punya kemampuan. Pengguna tetap membutuhkan heading, daftar, checklist, code block, link, gambar lokal, dan callout. Mereka hanya tidak ingin melihat semua alat tersebut sepanjang waktu.

Devan pernah memakai editor Markdown yang memisahkan source dan preview. Ia mengetik di satu sisi, lalu memindahkan mata ke sisi lain untuk melihat hasilnya. Pola itu masuk akal untuk banyak situasi, tetapi tidak cocok dengan niat QuickNote. QuickNote ingin membuat Markdown terasa seperti teks biasa yang memiliki sedikit keajaiban.

Myesha datang setelah sarapan. Ia membaca catatan desain yang dibuat Devan. "Kamu ingin syntax Markdown hilang ketika tidak sedang diedit, tetapi file tetap menyimpan syntax-nya?"

"Iya, Kak. Kalau barisnya `**penting**`, pengguna melihat kata penting dengan gaya tebal ketika kursor ada di tempat lain. Saat kursor masuk ke baris itu, tanda `**` muncul lagi supaya teks tetap mudah diedit."

Jovian yang sedang duduk di lantai langsung menyela. "Jadi syntax-nya seperti tulisan pensil yang ditutup kertas transparan. Ketika disentuh, kertasnya dibuka."

"Analogi itu cukup bagus," kata Myesha. "Yang penting, sumbernya tidak berubah hanya karena tampilan berubah."

Mereka memilih CodeMirror 6. Keputusan itu bukan karena nama library tersebut terdengar canggih. Mereka memilihnya karena dokumen perlu tetap menjadi sumber Markdown yang sama, dengan posisi cursor, selection, dan undo history yang mengacu pada sumber tersebut. Editor rich-text yang menyimpan model lain akan berisiko menulis ulang format pengguna ketika melakukan serialisasi.

Devan menulis keputusan itu di dokumentasi proyek. Ia ingin alasan teknisnya terlihat jelas. Kalau suatu hari ada orang yang bertanya mengapa QuickNote tidak memakai editor rich-text, jawabannya tidak boleh hanya "karena sudah terlanjur".

```typescript
import { EditorState } from "@codemirror/state";
import { EditorView, keymap } from "@codemirror/view";
import { markdown, markdownLanguage } from "@codemirror/lang-markdown";

const state = EditorState.create({
  doc: "",
  extensions: [
    markdown({ base: markdownLanguage }),
    EditorView.lineWrapping,
    keymap.of([]),
  ],
});

const view = new EditorView({
  state,
  parent: document.querySelector("#editor")!,
});
```

Contoh itu terlihat kecil, tetapi ia sudah menyimpan beberapa prinsip. Dokumen dimulai dari string Markdown. Grammar Markdown bekerja pada dokumen yang sama. Editor mengambil alih DOM tanpa membutuhkan framework UI besar. Tidak ada langkah konversi dari rich text ke Markdown di belakang layar.

Devan lalu mengembangkan editor sebenarnya. Ia menambahkan history, selection, search, line wrapping, syntax highlighting, format bar yang hanya muncul ketika ada selection, dan renderer live. Mereka tidak menaruh toolbar permanen karena toolbar permanen akan mengambil ruang dari satu hal yang paling penting: teks.

Myesha mengingatkan agar implementasi tidak terjebak pada tampilan saja. "Kalau editor menampilkan teks tebal, tetapi kemudian menulis ulang spasi dan newline saat save, kita gagal menjaga file pengguna. Tampilan boleh berubah. Source harus tetap dihormati."

Pernyataan itu menjadi masalah yang mereka temukan pada percobaan awal. Ketika file dibaca ulang dari disk, Devan mengganti seluruh isi dokumen dengan `view.dispatch`. Dispatch tersebut memicu listener perubahan dokumen. Listener menganggap perubahan itu berasal dari pengguna. QuickNote lalu menandai note sebagai dirty dan langsung menjadwalkan autosave.

Secara visual, semuanya terlihat baik. Secara perilaku, aplikasi membaca file lalu menulisnya kembali seolah-olah pengguna baru saja mengetik. Saat pengguna memilih file lain, isi file baru bahkan sempat disimpan menggunakan hash file lama. Sistem backend kemudian mengira ada perubahan eksternal dan membuat conflict copy untuk file yang tidak pernah disentuh siapa pun.

Jovian menemukan gejalanya saat menguji pergantian file. "Bang, aku baru pilih `meeting.md`, tetapi muncul `meeting.conflict...md`. Padahal file itu baru dibuka."

Devan menatap log. "Editor menganggap replace document sebagai input pengguna."

Myesha meminta mereka memisahkan dua jenis perubahan. Ada perubahan yang benar-benar dibuat pengguna. Ada perubahan yang dilakukan aplikasi untuk menampilkan isi dari disk. Keduanya mengubah dokumen, tetapi hanya yang pertama boleh memicu autosave.

CodeMirror menyediakan Annotation untuk membedakan keduanya. Devan membuat penanda bernama `programmatic`, lalu memasangnya pada transaksi yang berasal dari aplikasi.

```typescript
import { Annotation } from "@codemirror/state";

const programmatic = Annotation.define<boolean>();

const updateListener = EditorView.updateListener.of((update) => {
  const applicationEdit = update.transactions.some(
    (transaction) => transaction.annotation(programmatic) === true,
  );

  if (update.docChanged && !applicationEdit) {
    onUserChange(update.state.doc.toString());
  }
});

function replaceDocument(view: EditorView, content: string): void {
  const cursor = Math.min(view.state.selection.main.head, content.length);

  view.dispatch({
    changes: {
      from: 0,
      to: view.state.doc.length,
      insert: content,
    },
    selection: { anchor: cursor },
    annotations: programmatic.of(true),
  });
}
```

Jovian membaca kode itu cukup lama. "Kak, ini seperti memberi stempel pada paket. Isinya berubah, tetapi penerima tahu paketnya datang dari gudang, bukan dari pelanggan."

"Benar," kata Myesha. "Dan stempel ini bukan hiasan. Ia menjaga batas antara membaca dan menulis."

Batas itu penting karena QuickNote memakai source Markdown sebagai pusat aplikasi. Editor membaca source. Renderer memberi gaya pada source. Persistence menerima string source. Backend menyimpan string source. Tidak ada lapisan yang boleh memutuskan bahwa format pengguna perlu diperbaiki hanya karena library memiliki format yang berbeda.

Mereka juga menetapkan aturan reveal. Cursor pada baris inline akan menampilkan tanda Markdown di baris tersebut. Cursor di dalam fenced code block, blockquote, atau table akan menampilkan seluruh block. Selection yang membentang beberapa baris tidak otomatis membuka syntax karena teks yang berubah panjang ketika mouse sedang bergerak akan sulit dipilih.

Aturan itu terdengar seperti detail kecil. Namun, detail kecil menentukan apakah editor terasa tenang atau menyebalkan. Jika tanda syntax selalu terlihat, editor akan terasa seperti code editor. Jika tanda syntax tidak pernah terlihat, pengguna akan kesulitan mengubah format. QuickNote harus berada di tengah: hasilnya enak dilihat, source-nya tetap dekat ketika dibutuhkan.

Mereka menguji beberapa contoh.

```markdown
# Catatan Pagi

Ide ini **penting** dan perlu ditindaklanjuti.

- [ ] Cek alur autosave
- [x] Tulis keputusan editor

    ```typescript
    const message = "catatan kecil";
    ```
```

Ketika cursor berada di paragraf pertama, syntax bold terlihat. Ketika cursor pindah ke judul, paragraf kembali tampil seperti kalimat biasa. Ketika cursor masuk ke code block, tanda fence dan bahasa blok terlihat agar pengguna dapat mengeditnya tanpa menebak-nebak.

Devan sempat ingin menambahkan mode preview khusus karena itu pola yang banyak dipakai. Myesha menolaknya dengan alasan yang sederhana. "Preview terpisah mengajarkan pengguna bahwa source dan hasil adalah dua tempat berbeda. Kita ingin pengguna mengetik di satu tempat dan melihat hasil di tempat yang sama."

"Kalau begitu, QuickNote mirip Typora?" tanya Jovian.

"Dalam rasa interaksinya, iya. Dalam cakupannya, tidak," jawab Myesha. "Kita mengambil pelajaran dari pengalaman live preview. Kita tidak menyalin semua fitur editor itu."

Pembedaan tersebut kembali menjaga mereka dari scope yang melebar. Mereka ingin pengalaman yang sudah dipahami pengguna, bukan daftar fitur yang tidak habis-habis. QuickNote boleh mendukung code block dan gambar lokal karena keduanya sering muncul dalam quick note. QuickNote tidak perlu menjadi sistem publikasi lengkap.

Saat editor mulai terasa nyaman, masalah berikutnya muncul: shortcut. Devan ingin `Cmd/Ctrl + B` untuk bold, `Cmd/Ctrl + I` untuk italic, `Cmd/Ctrl + K` untuk link, `Cmd/Ctrl + S` untuk flush, dan `Esc` untuk menutup panel. Ia juga ingin tombol `Cmd/Ctrl + Enter` membantu keluar dari code block, quote, table, atau callout.

Jovian mencoba semua shortcut itu dengan cepat. Ia menekan `Ctrl + B`, menulis kalimat, membuka search, lalu menekan `Esc`. Tidak ada panel permanen yang tertinggal. Tidak ada dialog yang memaksa fokus pindah. Editor selalu kembali menjadi permukaan utama.

"Aku suka bagian ini," kata Jovian. "Fitur muncul ketika diminta, lalu pergi ketika sudah selesai."

Myesha menambahkan satu catatan. "Itu juga berlaku untuk format bar. Ia boleh muncul di atas selection, tetapi jangan berubah menjadi furniture yang tinggal di layar."

Devan mencatat kata furniture tersebut. Ia tahu interface sering menjadi penuh karena setiap komponen yang pernah dibuat akhirnya dianggap harus selalu terlihat. QuickNote memilih sebaliknya. Default screen harus hampir kosong. Save state adalah satu-satunya chrome permanen, dan statusnya cukup satu kata: `idle`, `saving`, `saved`, atau `error`.

Menjelang sore, editor pertama sudah bisa mengetik Markdown. Ia belum bisa menyimpan ke file, tetapi rasanya sudah mendekati tujuan awal. Devan membuka aplikasi, melihat cursor langsung siap, menulis daftar pendek, lalu menutup browser preview.

Ia tersenyum, tetapi Myesha belum ikut tersenyum.

"Editor-nya sudah bisa menerima ide," kata Myesha. "Sekarang kita harus memastikan ide itu tidak hilang ketika aplikasi melakukan pekerjaan yang tidak terlihat."

Devan tahu maksudnya. Menampilkan teks adalah bagian yang mudah dilihat. Menjaga teks melewati waktu, crash, perubahan eksternal, dan tombol close adalah bagian yang tidak terlihat sampai semuanya terlambat.

Di meja kerja yang sama, mereka membuka file baru bernama `persistence.ts`. Kursor berkedip di baris pertama. QuickNote baru saja selesai belajar bagaimana membuat Markdown bernapas. Berikutnya, ia harus belajar bagaimana menjaganya tetap hidup.

Sebelum beralih ke persistence, mereka menghabiskan satu jam hanya untuk menguji rasa editor. Pengujian itu tidak masuk ke laporan benchmark. Mereka duduk bergantian di depan window dan menulis kalimat tanpa melihat source code. Myesha menulis catatan meeting. Jovian menulis command dengan code fence. Devan menulis paragraf yang memiliki bold, link, dan checklist.

Mereka mencari gangguan kecil. Apakah cursor melompat ketika syntax tersembunyi? Apakah menekan Enter di daftar meneruskan marker dengan benar? Apakah Backspace pada awal item menghapus marker secara mengejutkan? Apakah selection berubah posisi ketika format bar muncul? Apakah baris panjang tetap nyaman dibaca ketika window dipersempit?

Jovian menemukan bahwa sebuah selection yang panjang membuat teks berubah ukuran ketika cursor bergerak. Ia menggeser mouse perlahan dan melihat target selection bergeser. "Kalau syntax dibuka saat selection ada, aku bisa kehilangan posisi yang ingin kupilih."

Myesha mencatat aturan yang kemudian mereka pertahankan: selection tidak membuka marks. Hanya cursor tunggal yang mengaktifkan reveal. Aturan itu bukan sekadar keputusan estetika. Ia menjaga manipulasi teks tetap dapat diprediksi.

Devan menemukan masalah lain pada gambar. Gambar lokal perlu tampil inline, tetapi URL remote tidak boleh diambil karena QuickNote offline-first dan tidak membuat network request. Mereka memilih resolver yang menerima path relatif terhadap folder note. Backend mengizinkan directory note yang aktif, bukan seluruh disk. Dengan begitu, tampilan mengikuti file tanpa membuka akses yang tidak perlu.

Mereka menguji file yang dibuka di aplikasi lain. File tersebut berisi syntax yang belum didukung QuickNote. Renderer tidak boleh menghapus atau mengubah syntax itu. Teks asing tetap berada di source. Pengguna dapat membuka file tersebut di editor yang lebih lengkap tanpa menemukan bagian yang diam-diam hilang.

Hal ini menguatkan keputusan bahwa parser dan renderer bukan pemilik dokumen. Mereka hanya pembaca dan pelukis. Saat parser tidak mengenal construct tertentu, source tetap aman. Prinsip ini membuat QuickNote lebih rendah hati. Ia tidak berjanji memahami semua Markdown yang mungkin dibuat di dunia.

"Kalau renderer kita tidak mengerti sesuatu, jangan menghukum file," kata Myesha. "Tampilkan apa yang bisa kita tampilkan. Simpan source seperti semula."

Devan lalu membuat daftar uji yang berasal dari kebiasaan nyata, bukan dari demo yang sempurna:

- Menempelkan stack trace panjang tanpa format.
- Menulis checklist kosong lalu mencentangnya.
- Membuat code block tanpa info string.
- Memakai code block dengan bahasa yang belum pernah dipakai sebelumnya.
- Menekan Enter tiga kali di dalam list.
- Memindahkan cursor dari akhir file ke awal file.
- Membuka file yang hanya berisi newline.
- Membuka file besar yang berisi 200.000 karakter.

Pada dokumen besar, mereka mengukur waktu dari keystroke hingga painted frame. Target typical document berada di bawah 16 milidetik, sedangkan stress document dipakai untuk menguji batas. CodeMirror membantu karena editor tidak perlu membangun ulang seluruh DOM untuk setiap karakter. Language grammar juga dimuat sesuai kebutuhan. Bahasa untuk fenced block tidak ikut membebani startup sebelum dipakai.

Jovian bertanya apakah target itu penting untuk quick note yang biasanya pendek. Devan menjawab bahwa ukuran kecil bukan alasan untuk membiarkan latency tumbuh tanpa batas. Hari ini note mungkin berisi tiga baris. Besok pengguna bisa menyimpan transkrip meeting atau daftar troubleshooting yang panjang. Source tetap harus dapat diandalkan.

Myesha mengingatkan mereka agar tidak mengejar angka dengan mengorbankan perilaku. "Kecepatan bukan hanya benchmark. Jika cursor terasa berpindah ke tempat yang salah, pengguna tetap merasakan aplikasi lambat karena mereka harus memperbaiki akibatnya."

Pada akhir sesi, mereka menghapus satu animasi pembuka yang sebelumnya terlihat menarik. Animasi itu menunda cursor muncul sekitar 300 milidetik. Secara visual, window tampak lebih hidup. Secara pengalaman, pengguna menunggu sebelum mengetik.

"QuickNote tidak perlu menyambut pengguna," kata Devan. "Ia perlu langsung memberi keyboard."

Keputusan itu sederhana, tetapi ia memperjelas karakter aplikasi. Tidak ada onboarding. Tidak ada layar kosong dengan tips. Tidak ada tutorial yang muncul sebelum note pertama. Dokumentasi tersedia di luar alur utama. Di dalam window, pengguna mendapat editor.

Ketika mereka menutup prototipe, Myesha meminta satu hal. "Simpan contoh source yang kita pakai untuk test. Jangan hanya test tampilan akhir. Kita harus memastikan file yang masuk dan file yang keluar tetap bisa dipahami."

Devan setuju. Mereka menyimpan contoh Markdown dengan trailing newline, spasi ganda, code fence, callout, dan link. Setiap contoh menjadi pengingat bahwa formatting pengguna adalah bagian dari data, bukan sampah yang boleh dirapikan.

Baru setelah semua itu mereka membuka `persistence.ts`. Editor sudah cukup nyaman untuk menerima catatan. Kini catatan tersebut harus bisa melewati proses save tanpa kehilangan identitasnya.

## Bab 3: Autosave, Hash, dan Janji Tidak Menghilangkan Teks

Kalau seseorang mendengar kata autosave, biasanya yang terbayang adalah timer sederhana. Setiap ada perubahan, aplikasi menunggu sebentar lalu memanggil fungsi save. Devan juga berpikir begitu pada awalnya. Ia membuat listener perubahan, memasang `setTimeout`, dan menulis isi editor ke file.

Versi pertama tampak berhasil. Devan mengetik kalimat, menunggu, lalu melihat file berubah. Ia mengetik lagi. File berubah lagi. Ia menutup aplikasi. Semuanya terlihat aman.

Myesha meminta pengujian yang lebih keras. "Apa yang terjadi kalau Devan mengetik terus selama dua menit?"

"Timer akan terus di-reset. Setelah berhenti, baru save," jawab Devan.

"Berarti kalau seseorang sedang mengetik panjang tanpa berhenti, perubahan bisa tinggal di memori selama dua menit?"

Devan terdiam. Ia sadar bahwa debounce saja tidak cukup. Autosave perlu dua batas. Batas pertama adalah jeda pendek setelah pengguna berhenti mengetik. Batas kedua adalah waktu maksimum sejak aktivitas mengetik dimulai. Dengan begitu, continuous typing tidak bisa menunda write tanpa batas.

Mereka memilih debounce 400 milidetik dan batas maksimum 5 detik. Angka tersebut bukan janji bahwa semua disk akan menulis dalam waktu persis itu. Angka itu adalah perilaku yang mudah diuji: setelah pengguna diam selama 400 milidetik, QuickNote menulis; selama pengguna terus mengetik, QuickNote tetap menulis paling lambat setelah lima detik.

```typescript
const DEBOUNCE_MS = 400;
const MAX_INTERVAL_MS = 5000;

schedule(content: string): void {
  if (this.stopped) return;

  this.content = content;
  this.dirty = true;
  this.hooks.onState("saving");

  if (this.debounceTimer !== null) {
    window.clearTimeout(this.debounceTimer);
  }

  this.debounceTimer = window.setTimeout(() => {
    this.debounceTimer = null;
    void this.write();
  }, DEBOUNCE_MS);

  if (this.maxTimer === null) {
    this.maxTimer = window.setTimeout(() => {
      this.maxTimer = null;
      void this.write();
    }, MAX_INTERVAL_MS);
  }
}
```

Jovian menatap dua timer tersebut. "Kenapa status langsung `saving`, padahal write belum mulai?"

"Karena status itu bicara kepada pengguna," jawab Myesha. "Saat perubahan belum ada di disk, pengguna perlu tahu bahwa aplikasi sedang memegang pekerjaan penyimpanan. Nama status boleh sederhana, tetapi maknanya harus jujur."

Devan lalu menambahkan `flush`. `Cmd/Ctrl + S` harus menulis perubahan sekarang. Window kehilangan focus harus memicu flush. Proses keluar harus meminta frontend menunggu hingga flush selesai sebelum aplikasi benar-benar berhenti. `flush` juga harus menunggu write yang sedang berjalan, lalu memeriksa apakah masih ada perubahan baru.

Masalah concurrency muncul tidak lama kemudian. Devan mengetik lagi ketika write pertama masih berjalan. Jika QuickNote memakai snapshot yang sama untuk semua proses, perubahan kedua bisa tertimpa oleh hasil write pertama. Mereka membutuhkan aturan sederhana: setiap write mengambil `pending` dari content saat itu. Ketika write selesai, QuickNote membandingkan content terbaru dengan `pending`. Jika berbeda, note tetap dirty dan write berikutnya dijadwalkan.

```typescript
private write(): Promise<void> {
  if (this.stopped || !this.dirty) return Promise.resolve();
  if (this.inflight) return this.inflight;

  this.clearTimers();
  const pending = this.content;
  const generation = this.generation;
  this.hooks.onState("saving");

  this.inflight = this.backend
    .noteSave(pending, this.baseHash)
    .then((result) => {
      if (generation !== this.generation) return;

      this.baseHash = result.hash;
      this.dirty = this.content !== pending;
      this.hooks.onState(this.dirty ? "saving" : "saved");

      if (result.conflictFile) {
        this.hooks.onConflict(result.conflictFile);
      }

      if (this.dirty) this.schedule(this.content);
    })
    .catch((error: unknown) => {
      if (generation !== this.generation) return;
      this.hooks.onState("error");
      this.hooks.onError(String(error));
    })
    .finally(() => {
      this.inflight = null;
    });

  return this.inflight;
}
```

Devan merasa kode itu mulai terlihat seperti sistem yang lebih serius daripada tampilan aplikasinya. Ia tertawa kecil. "Aplikasi ini kelihatan kosong, tetapi kelas persistence-nya sudah punya timer, state, hash, generation, dan conflict."

"Kesederhanaan yang dirasakan pengguna sering membutuhkan kerumitan yang disembunyikan dengan baik," kata Myesha. "Yang penting kerumitannya punya alasan."

Hash menjadi bagian penting dari cerita. QuickNote tidak hanya menulis content. Ia menyimpan hash dari versi file yang terakhir diketahui. Sebelum menulis versi baru, backend membaca isi file saat ini dan membandingkan hash tersebut dengan `baseHash`. Jika berbeda, berarti ada program lain yang sudah mengubah file.

Perubahan eksternal tidak selalu merupakan masalah. Jika editor QuickNote sedang bersih, aplikasi bisa memuat ulang isi baru. Jika editor sedang dirty, situasinya menjadi conflict. QuickNote tidak boleh memilih diam-diam antara versi pengguna dan versi eksternal. Ia menyimpan versi eksternal sebagai conflict copy, lalu menulis versi yang sedang diedit pengguna ke file utama.

```rust
pub fn save(path: &Path, content: &str, base_hash: &str) -> Result<NoteSave> {
    let mut conflict_file = None;

    if path.exists() {
        let current = fs::read_to_string(path)
            .map_err(|e| Error::io("cannot read", path, e))?;

        if hash(&current) != base_hash {
            let copy = conflict_path(path);
            fs::write(&copy, &current)
                .map_err(|e| Error::io("cannot write", &copy, e))?;
            conflict_file = copy
                .file_name()
                .map(|name| name.to_string_lossy().into_owned());
        }
    }

    atomic_write(path, content)?;

    Ok(NoteSave {
        hash: hash(content),
        conflict_file,
    })
}
```

Jovian menunjuk pada bagian `fs::write(&copy, &current)`. "Jadi versi dari editor lain tidak hilang. Ia dipindahkan ke file di sampingnya."

"Ya," jawab Devan. "File utama tetap versi yang sedang kita tulis. Versi eksternal ada sebagai bukti yang bisa dibandingkan."

Myesha menambahkan bahwa keputusan ini berbeda dari merge otomatis. QuickNote adalah alat untuk quick note, bukan sistem kolaborasi. Merge otomatis bisa terlihat pintar, tetapi pada teks kecil pun ia dapat membuat perubahan sulit dilacak. Menyimpan dua versi lebih mudah dijelaskan dan lebih aman untuk prinsip mereka: tidak ada teks yang dibuang diam-diam.

Mereka lalu memikirkan write yang terputus. Menulis langsung ke `notes.md` memiliki risiko file berhenti di tengah. Jika proses mati setelah sebagian bytes tertulis, file utama bisa rusak. Mereka memilih atomic write: tulis ke file sementara, flush ke disk, lalu rename ke tujuan.

Namun, satu file sementara ternyata belum cukup. Jika nama `.tmp` langsung dipakai untuk menulis bytes, crash di tengah `write_all` dapat meninggalkan `.tmp` yang lebih baru tetapi isinya terpotong. Pada launch berikutnya, mekanisme recovery bisa menganggap file itu lengkap dan mempromosikannya menjadi note utama.

Myesha menggambar tiga nama di kertas.

```text
notes.md.writing  -> bytes sedang ditulis, tidak pernah dipulihkan
notes.md.tmp      -> bytes sudah lengkap dan sudah di-flush
notes.md          -> note yang sedang dipakai
```

"Rename dari `.writing` ke `.tmp` adalah tanda bahwa isi sudah lengkap," jelasnya. "Recovery hanya boleh mempromosikan `.tmp` jika timestamp-nya lebih baru. File `.writing` selalu dibuang karena kita tidak tahu apakah ia lengkap."

```rust
pub fn atomic_write(path: &Path, content: &str) -> Result<()> {
    let writing = writing_path(path);
    let tmp = tmp_path(path);

    let filled = (|| -> Result<()> {
        let mut file = File::create(&writing)
            .map_err(|e| Error::io("cannot write", &writing, e))?;
        file.write_all(content.as_bytes())
            .map_err(|e| Error::io("cannot write", &writing, e))?;
        file.sync_all()
            .map_err(|e| Error::io("cannot flush", &writing, e))
    })();

    if let Err(error) = filled {
        drop(fs::remove_file(&writing));
        return Err(error);
    }

    fs::rename(&writing, &tmp)
        .map_err(|e| Error::io("cannot stage", &tmp, e))?;
    fs::rename(&tmp, path)
        .map_err(|e| Error::io("cannot replace", path, e))?;
    Ok(())
}
```

Devan membaca fungsi tersebut beberapa kali. Ia menyukai bagian yang tidak terlihat oleh pengguna. Pengguna tidak perlu tahu nama `.writing` atau `.tmp`. Mereka hanya perlu tahu bahwa ketika aplikasi menulis, file utama tidak sengaja dibiarkan dalam keadaan setengah jadi.

Sore itu mereka membuat test untuk hash, atomic write, file parent yang belum ada, staging file yang harus hilang setelah write, dan content kosong. Mereka juga membuat test untuk `Persistence`: schedule harus menulis setelah debounce, continuous typing harus dipotong oleh max interval, flush harus menunggu inflight write, dan reset harus memindahkan state ke file baru.

Test `reset` lahir dari bug yang sulit ditemukan. QuickNote awalnya membuat satu instance persistence untuk satu sesi. Ketika pengguna memilih file lain, isi dan hash baru dimasukkan ke editor, tetapi persistence tetap menyimpan hash file sebelumnya. Write pertama pada file baru dianggap conflict. Lebih buruk lagi, jika file sebelumnya read-only dan persistence dinonaktifkan, file baru tetap tidak pernah bisa disimpan karena flag `stopped` tidak pernah dibersihkan.

Mereka memperbaikinya dengan `reset(content, hash)`. Method itu membersihkan timer, menaikkan `generation`, mengganti content dan base hash, menghapus dirty flag, membatalkan stopped state, lalu mengembalikan status ke `saved`.

```typescript
reset(content: string, hash: string): void {
  this.clearTimers();
  this.generation++;
  this.content = content;
  this.baseHash = hash;
  this.dirty = false;
  this.stopped = false;
  this.hooks.onState("saved");
}
```

Jovian bertanya tentang `generation`. Devan menjelaskan dengan analogi dua surat. Write lama untuk file A bisa saja masih berjalan ketika pengguna pindah ke file B. Kalau hasil write lama tiba setelah reset, hash yang dikembalikan hanya valid untuk file A. `generation` membuat QuickNote mengabaikan hasil yang sudah tidak memiliki konteks.

"Jadi bukan hanya isi yang harus berpindah," kata Jovian. "Identitas pekerjaan yang sedang berjalan juga harus berpindah."

"Benar," jawab Myesha. "State lama yang masuk ke state baru adalah sumber bug yang tidak terlihat."

Malamnya, mereka menjalankan skenario yang lebih menegangkan. Devan membuka `notes.md`, mengetik daftar tugas, lalu Jovian mengubah file tersebut dari editor lain. Devan mengetik lagi sebelum QuickNote sempat save. Setelah 400 milidetik, QuickNote membaca hash baru, menyimpan versi eksternal sebagai `notes.conflict-20260817-...md`, lalu menulis versi Devan ke file utama.

Tidak ada dialog besar yang menghalangi pengetikan. QuickNote hanya menampilkan notice line bahwa conflict copy sudah dibuat. Pengguna dapat melanjutkan pekerjaannya, lalu membandingkan dua file ketika punya waktu.

Mereka juga menguji file yang dihapus. Awalnya `note_check` mengembalikan `changed: false` ketika path tidak ada. Pada keystroke berikutnya, autosave akan membuat ulang file tanpa memberi tahu apa pun. Dari sudut pandang pengguna, file seolah-olah muncul kembali dengan sendirinya. Sekarang backend mengembalikan `missing: true`. Frontend menampilkan notice, lalu menulis kembali isi editor ke path tersebut.

Devan menyandarkan punggungnya. "Semakin kita menjaga catatan agar tidak hilang, semakin banyak keadaan yang harus kita akui."

Myesha tersenyum. "Itulah kenapa aplikasi kecil tidak boleh dianggap remeh. Ukuran interface bukan ukuran tanggung jawabnya."

Di akhir hari, QuickNote mulai memenuhi janji utamanya. Pengguna mengetik, aplikasi autosave, file tetap plain Markdown, dan kegagalan tidak langsung berubah menjadi kehilangan teks. Devan melihat satu kata `saved` di sudut layar.

Kata itu kecil. Ia hanya terlihat setelah semua pekerjaan yang rumit selesai. Tetapi bagi pengguna, satu kata tersebut membawa ketenangan. Mereka tidak perlu memikirkan timer, hash, rename, atau conflict. Mereka hanya perlu tahu bahwa kalimat yang baru saja ditulis masih ada.

Mereka membuat simulasi kegagalan yang lebih dekat dengan kehidupan sehari-hari. Devan memulai save lalu mematikan proses sebelum rename. Myesha mengubah isi file dari editor lain tepat ketika autosave menunggu. Jovian menghapus file dari Finder, lalu mengetik satu karakter di QuickNote. Semua skenario itu terasa berlebihan sampai mereka sadar bahwa pengguna tidak pernah memilih waktu yang nyaman untuk kegagalan.

Pada simulasi pertama, file `.writing` tertinggal. Saat aplikasi dibuka kembali, recovery membuang file tersebut lalu membaca note utama. Tidak ada potongan teks yang dipromosikan secara keliru. Pada simulasi kedua, conflict copy dibuat sebelum versi Devan ditulis. Pada simulasi ketiga, notice menyebut file hilang dan isi editor dipulihkan ke path tersebut setelah pengguna diberi tahu.

Jovian mengusulkan agar notice memakai dialog modal supaya pengguna pasti melihatnya. Myesha menolak. "Notice yang menutup jalan mengetik bertentangan dengan tujuan QuickNote. Cukup tampilkan satu baris. Pengguna dapat melihatnya tanpa kehilangan cursor."

Keputusan itu membuat error handling lebih menantang. Pesan harus cukup jelas, tetapi tidak boleh mengisi layar. Mereka memilih kalimat seperti `Conflict copy created: notes.conflict-...md` dan `Note file was missing and was restored`. Tidak ada stack trace di permukaan utama. Detail tetap masuk ke log developer atau error yang dapat dibaca saat debugging.

Devan memperhatikan bahwa status `saving` dapat bertahan jika disk lambat. Ia hampir menambahkan spinner. Myesha bertanya apakah spinner membantu pengguna memutuskan sesuatu. Jawabannya tidak. Mereka mempertahankan satu kata yang berubah menjadi `saved` ketika operasi selesai. Jika ada error, status `error` mendapat warna yang menarik perhatian.

Satu kata memaksa mereka untuk disiplin. `saved` tidak boleh ditampilkan sebelum backend mengembalikan hash baru. `saving` tidak boleh hilang hanya karena timer selesai jika write masih inflight. `error` tidak boleh menghapus dirty state karena kegagalan harus dapat dicoba lagi. Status visual harus mengikuti state nyata, bukan sekadar urutan event yang diharapkan.

Mereka juga menulis test untuk kegagalan promise. Backend palsu menolak `noteSave`. Persistence harus memanggil `onError`, mempertahankan content, dan membiarkan autosave berikutnya mencoba lagi. Test tersebut menemukan bug kecil: timer baru tidak dijadwalkan setelah error karena `inflight` sudah di-reset terlalu cepat. Mereka memperbaiki lifecycle-nya sebelum menambah fitur lain.

Myesha menyebutnya sebagai prinsip "dirty berarti masih ada pekerjaan". Selama content editor berbeda dari snapshot yang berhasil ditulis, QuickNote tidak boleh menganggap pekerjaan selesai. Prinsip ini juga berlaku ketika pengguna mengetik saat write berjalan. Snapshot lama boleh berhasil, tetapi content terbaru tetap harus membuat note dirty.

Devan menulis diagram alur di papan.

```text
user change
    -> content terbaru
    -> dirty
    -> debounce atau max interval
    -> snapshot pending
    -> compare disk dengan baseHash
    -> conflict copy jika perlu
    -> atomic write
    -> hash baru
    -> saved atau retry
```

Diagram itu membantu Jovian memahami bahwa autosave bukan satu fungsi `save()`. Ia adalah percakapan antara editor, scheduler, filesystem, dan state. Masing-masing harus mengembalikan informasi yang cukup untuk langkah berikutnya.

Mereka membahas hash FNV-1a. Hash tersebut bukan untuk keamanan dan bukan untuk mendeteksi serangan. Ia hanya cara cepat untuk membandingkan versi satu file kecil. Karena tujuan hash adalah versi, bukan autentikasi, mereka tidak perlu memakai hash cryptographic yang lebih mahal. Nama dan komentar kode menjelaskan batas penggunaan tersebut.

"Kalau orang membaca fungsi `hash`, mereka harus tahu apa yang tidak dijamin fungsi itu," kata Myesha. "Jangan membuat nama sederhana terdengar seperti perlindungan yang lebih besar."

Devan menyadari bahwa dokumentasi inline menjadi penting justru pada kode yang tampak sederhana. Komentar pada `atomic_write` menjelaskan mengapa ada tiga nama file. Komentar pada `generation` menjelaskan mengapa hasil write lama tidak boleh memperbarui hash file baru. Komentar pada `reset` menjelaskan mengapa semua field yang menggambarkan file lama harus dibersihkan.

Jovian bertanya apakah komentar sebanyak itu tidak membuat kode terlihat panjang. Devan menjawab bahwa mereka menetapkan batas code line, bukan batas reasoning. Komentar yang menjelaskan keputusan lebih murah daripada developer berikutnya mengulang bug yang sama.

Setelah persistence stabil, mereka menguji perubahan file ketika editor sedang clean. QuickNote memanggil `noteCheck` ketika window mendapatkan focus. Jika hash berbeda dan tidak ada dirty edit, content baru dimuat ke editor dengan `programmatic` annotation. Jika hash sama, tidak ada pekerjaan. Jika file hilang, notice ditampilkan.

Skenario clean dan dirty sengaja dipisah. Pada clean edit, pengguna mungkin ingin melihat perubahan dari editor lain. Pada dirty edit, QuickNote tidak boleh menimpa tulisan yang belum tersimpan. Sebaliknya, write path akan melindungi versi eksternal sebagai conflict copy.

Myesha menekankan bahwa dialog merge bukan kebutuhan untuk V1. "Kita tidak boleh menyamakan keamanan dengan banyak pilihan. Conflict copy memberikan dua versi lengkap. Pengguna bisa memilih dengan tenang."

Malam berikutnya, Devan membuka conflict copy yang dibuat oleh test. Ia melihat versi eksternal masih utuh. Ia menggabungkan satu baris secara manual, lalu menyimpan hasilnya sebagai note utama. Tidak ada magic. Tidak ada keputusan otomatis yang sulit dijelaskan. Hanya dua file plain Markdown dan kontrol tetap di tangan pengguna.

Pada titik itu, janji QuickNote berubah dari slogan menjadi perilaku yang dapat diuji. `Type it` berarti editor langsung siap dan source tetap dekat. `Close it` berarti window dapat disembunyikan atau proses dapat flush dengan benar. `It's still there` berarti file utama, recovery, conflict, dan retry memiliki jalur yang masuk akal.

Devan menutup laptop. Kali ini ia tidak memeriksa folder secara manual. Ia percaya pada status `saved`, tetapi bukan kepercayaan kosong. Kepercayaan itu dibangun oleh timer yang memiliki batas, hash yang memiliki arti jelas, write yang atomic, dan test yang pernah membuat kegagalan terjadi dengan sengaja.

## Bab 4: Aplikasi yang Bersembunyi di Menu Bar

Editor dan persistence sudah memiliki bentuk. Sekarang mereka harus menyelesaikan pertanyaan tentang cara membuka QuickNote. Kalau pengguna memang membutuhkan catatan cepat, mereka tidak boleh mencari aplikasi melalui banyak langkah. QuickNote harus menunggu dekat, tetapi tidak boleh mengambil perhatian ketika tidak dipakai.

Devan sempat membuat versi yang hidup seperti aplikasi desktop biasa. Ada icon di Dock, taskbar button, dan window yang muncul ketika proses dimulai. Secara teknis itu bekerja. Secara pengalaman, ia terasa seperti aplikasi yang meminta ruang tetap di depan pengguna.

Jovian mengusulkan menu bar. "Kalau QuickNote hanya perlu dipanggil saat ada ide, letakkan dia di dekat jam dan Wi-Fi. Tidak perlu memenuhi Dock."

Myesha menyetujui, tetapi ia langsung menambahkan satu syarat. "Close dan quit harus berbeda. Menutup window hanya menyembunyikan window. Quit harus flush dulu, baru proses berhenti. Kalau proses langsung mati, autosave yang sedang berjalan bisa terpotong."

Perbedaan itu menjadi bagian penting dari arsitektur. QuickNote harus resident. Ketika window disembunyikan, proses tetap hidup dan global shortcut masih terdaftar. Dengan begitu, `Ctrl+N` bisa membuka window dari aplikasi mana pun tanpa cold start.

Pada macOS, mereka ingin tidak ada icon Dock. Mereka memakai activation policy accessory saat runtime dan `LSUIElement` pada `Info.plist` untuk aplikasi yang sudah dibundle. Pada Windows dan Linux, `skipTaskbar` membantu menghilangkan taskbar button. Setiap keputusan memiliki konteks platform sendiri.

Devan awalnya mengira satu konfigurasi cukup. Myesha memintanya menguji `tauri dev` dan aplikasi bundle. Hasilnya berbeda. Runtime policy mengurus proses development, sedangkan `Info.plist` dibaca oleh aplikasi macOS yang sudah dibundle.

"Satu hasil visual bisa membutuhkan dua keputusan di dua tempat," kata Myesha. "Yang penting kita menulis alasan masing-masing, bukan hanya menyalin konfigurasi sampai kebetulan tampil benar."

Tray icon juga memiliki detail kecil. Icon menu bar memakai template glyph agar macOS dapat memberi warna sesuai tema menu bar. Left click mengubah visibility window. Right click menampilkan menu untuk membuka note atau quit. Tidak ada menu panjang karena menu bar bukan tempat memindahkan semua fitur aplikasi.

Global shortcut menjadi pintu utama. Versi awal memakai kombinasi yang terlalu panjang. Devan menggantinya menjadi `Ctrl+N` pada setiap platform agar mudah diingat. Mereka tahu kombinasi tersebut mengambil fungsi dari aplikasi lain, terutama pada macOS, sehingga settings harus bisa menggantinya.

Bug shortcut muncul ketika pengguna memasukkan kombinasi baru yang invalid. Implementasi lama menghapus shortcut lama lebih dulu, lalu mencoba parse dan register shortcut baru. Jika kombinasi baru gagal, QuickNote tidak memiliki shortcut sama sekali. Window yang tersembunyi menjadi sulit dibuka.

Jovian menemukan bug itu dengan memasukkan accelerator yang salah. Ia menutup window, lalu menekan `Ctrl+N`. Tidak ada apa pun.

"Bang, shortcut-nya mati total," katanya.

Devan langsung ingin memperbaiki dengan unregister ulang. Myesha menghentikannya. "Jangan menghapus shortcut yang sedang bekerja sebelum shortcut baru hidup. Parse dan register dulu. Setelah berhasil, baru unregister yang lama."

```rust
#[tauri::command]
pub fn set_global_shortcut(
    app: AppHandle,
    state: State<AppState>,
    accelerator: String,
) -> bool {
    let Ok(shortcut) = Shortcut::from_str(&accelerator) else {
        return false;
    };

    let manager = app.global_shortcut();

    state
        .with_shortcut(|current| {
            if *current == Some(shortcut) {
                return true;
            }

            if manager.register(shortcut).is_err() {
                return false;
            }

            if let Some(previous) = current.take() {
                drop(manager.unregister(previous));
            }

            *current = Some(shortcut);
            true
        })
        .unwrap_or(false)
}
```

Kode tersebut menjaga shortcut lama tetap hidup ketika shortcut baru gagal didaftarkan. `AppState` menyimpan accelerator yang benar-benar terdaftar, bukan hanya nilai yang terakhir diminta pengguna. Jika aplikasi lain sudah memakai kombinasi itu, QuickNote dapat menolak perubahan tanpa kehilangan pintu masuk yang lama.

Mereka kemudian membedah alur frontend dan backend. Frontend TypeScript tidak boleh mengetahui cara membaca path OS, membuat file temporary, atau mengatur tray. Backend Rust tidak boleh mengetahui detail cursor, selection, atau syntax rendering. Keduanya berbicara melalui interface `Backend`.

```typescript
export interface Backend {
  noteLoad(): Promise<NoteLoad>;
  noteSave(content: string, baseHash: string): Promise<NoteSave>;
  noteCheck(baseHash: string): Promise<NoteCheck>;
  noteSetPath(path: string): Promise<NoteLoad>;
  configLoad(): Promise<Config>;
  configSave(config: Config): Promise<void>;
  sessionLoad(): Promise<Session>;
  sessionSave(cursorOffset: number, scrollTop: number): Promise<void>;
}
```

Implementasi Tauri memanggil command Rust. Implementasi browser memakai `localStorage` sebagai stand-in untuk filesystem ketika frontend dikembangkan tanpa desktop shell. Perbedaan itu membantu test editor tanpa menjalankan seluruh aplikasi Tauri. Yang penting, interface-nya sama sehingga `Persistence` dapat diuji menggunakan backend palsu.

Devan menyukai perubahan tersebut. Sebelumnya bridge berisi singleton module-level yang harus diinisialisasi dengan urutan tertentu. Jika seseorang memanggil fungsi sebelum `initBridge`, aplikasi bisa melempar error. Sekarang `initBridge()` mengembalikan satu object `Backend`. Dependency yang dibutuhkan kelas persistence masuk melalui constructor.

```typescript
const backend = initBridge();

const persistence = new Persistence(
  backend,
  loaded.content,
  loaded.hash,
  {
    onState: (state) => setSaveState(state),
    onReload: (content) => replaceDocument(editor, content),
    onConflict: (file) => showNotice(`Conflict copy: ${file}`),
    onMissing: () => showNotice("Note file was missing and was restored"),
    onError: (message) => showNotice(message),
  },
);
```

Jovian menunjuk pada callback `onReload`. "Ini yang menghubungkan disk ke editor, tetapi `replaceDocument` harus membawa annotation programmatic dari bab kemarin."

"Betul," jawab Devan. "Layer-nya terpisah, tetapi aturan di antaranya harus jelas."

Pemisahan itu membuat struktur frontend menjadi beberapa modul kecil. `boot` menyiapkan aplikasi. `wiring` menghubungkan callback. `lifecycle` menangani focus, hide, flush, dan exit. `shortcuts` mendaftarkan shortcut editor. `font-size` mengurus pengaturan ukuran teks. `context` menyediakan state yang dibutuhkan callback.

Mereka sengaja tidak memakai framework UI untuk versi pertama. Editor sudah menguasai DOM melalui CodeMirror. Sisa interface hanya status line, find panel, settings sheet, dan notice line. Framework dapat ditambahkan nanti tanpa menyentuh editor atau persistence jika kebutuhan itu benar-benar muncul.

Settings menjadi bagian kecil tetapi penting. Pengguna dapat mengubah theme, font size, path note, shortcut, dan always on top. Konfigurasi disimpan di `config.json`. Session seperti cursor offset, scroll position, dan window geometry disimpan di `session.json`. Catatan tidak disimpan di dua file tersebut.

Pemisahan ini menjawab satu ketakutan Devan. "Kalau folder state dihapus, apakah note ikut hilang?"

"Tidak," kata Myesha. "Folder state hanya menyimpan kenyamanan sesi. Note berada di path yang terlihat dan configurable. Jika state dihapus, yang hilang hanya posisi cursor, ukuran window, dan pilihan lain."

Default note berada di `~/QuickNote/notes.md`. Pengguna dapat memindahkannya ke folder lain, membukanya di editor berbeda, melakukan backup, atau memasukkannya ke Git. QuickNote tidak menyembunyikan data penting di application data directory.

Mereka menguji path pada volume eksternal dan menemukan masalah asset scope. Konfigurasi static Tauri hanya mengizinkan `$HOME/**`. Gambar lokal yang berada di luar `$HOME` gagal dirender. Solusinya bukan membuka semua filesystem. Command `allow_note_directory` hanya menambahkan folder yang memuat note aktif ke asset protocol scope.

```rust
pub fn allow_note_directory(app: &AppHandle, note: &Path) {
    if let Some(parent) = note.parent() {
        drop(app.asset_protocol_scope().allow_directory(parent, true));
    }
}
```

Jovian mengangguk. "Scope-nya tetap sempit. Ia mengikuti note aktif, bukan memberi WebView akses ke semua folder."

Keputusan itu cocok dengan sifat offline dan private QuickNote. Aplikasi tidak memiliki akun, cloud, telemetry, atau network request. Gambar remote tidak diambil dari internet. Gambar lokal boleh tampil inline karena file-nya ada di sekitar note. URL remote tetap menjadi link bergaya biasa.

Menjelang sore, mereka menghadapi alur quit. Tray menu, shortcut `Cmd/Ctrl + Q`, dan event runtime dapat meminta proses berhenti pada waktu yang hampir sama. Jika masing-masing memulai timer flush sendiri, aplikasi bisa mengirim beberapa event dan memanggil exit berkali-kali.

`AppState` mendapatkan method `begin_exit`. Method itu memeriksa dan mengubah flag `exiting` di bawah lock yang sama. Hanya pemanggil pertama yang mendapat `true`. Pemanggil berikutnya mendapat `false` dan tidak memulai ulang sequence.

```rust
pub fn begin_exit(&self) -> Result<bool> {
    let mut exiting = self.exiting.lock().map_err(|_| Error::Lock)?;

    if *exiting {
        return Ok(false);
    }

    *exiting = true;
    Ok(true)
}
```

Sequence-nya jelas. Backend mencegah exit, mengirim event `flush-and-exit`, frontend memanggil `persistence.flush()`, lalu frontend memanggil `ready_to_exit`. Ada fallback timer dua detik agar proses tidak menunggu selamanya jika WebView gagal merespons.

"Dua detik itu seperti pagar terakhir," kata Myesha. "Kita memberi waktu untuk menyelesaikan write, tetapi proses tidak boleh menggantung tanpa akhir."

Devan menguji quit saat status masih `saving`. Ia menekan shortcut quit segera setelah mengetik. Status berubah menjadi saved, lalu aplikasi keluar. Ia membuka QuickNote lagi dengan `Ctrl+N`. Catatan kembali dengan cursor dan scroll position yang sama.

Saat window ditutup dengan `Cmd/Ctrl + W`, proses tidak keluar. Icon tray tetap ada. Ketika `Ctrl+N` ditekan dari terminal, browser, atau aplikasi lain, QuickNote kembali muncul dengan cursor siap mengetik. Pengalaman itu memenuhi tujuan awal mereka: catatan tidak perlu dicari. Ia hanya perlu dipanggil.

Malamnya, Devan duduk di ruang tengah bersama Myesha dan Jovian. Mereka melihat aplikasi yang sekarang tampak hampir terlalu sederhana. Satu kolom teks. Satu status word. Tidak ada menu besar.

Jovian tersenyum. "Kalau orang hanya melihat layarnya, mereka tidak akan tahu ada Rust, CodeMirror, hash, recovery, conflict copy, dan global shortcut di belakangnya."

"Itu bukan masalah," jawab Devan. "Kalau semua bagian itu bekerja, pengguna memang tidak perlu memikirkannya."

Myesha menyesap teh. "Engineering yang baik tidak selalu membuat pengguna melihat lebih banyak. Kadang ia membuat pengguna punya lebih sedikit hal untuk dikhawatirkan."

QuickNote akhirnya memiliki bentuk utuh. Ia berada di menu bar. Ia membuka window dengan shortcut. Ia menyimpan satu file Markdown. Ia menjaga file itu dari write setengah jadi dan perubahan eksternal. Ia menyimpan state kenyamanan tanpa mengambil kepemilikan atas note.

Mereka menguji resident behavior pada beberapa kebiasaan pengguna. Pengguna pertama menekan tombol close karena mengira ingin menyembunyikan window. QuickNote tetap muncul di menu bar dan tidak kehilangan shortcut. Pengguna kedua menekan quit dari tray. Frontend mendapat waktu untuk flush. Pengguna ketiga menekan quit hampir bersamaan dengan event sistem. `begin_exit` memastikan hanya satu alur yang berjalan.

Pada percobaan awal, shortcut global membuat masalah lain. `Ctrl+N` bekerja di dalam QuickNote, tetapi tidak selalu bekerja saat aplikasi lain sedang aktif. Registrasi shortcut ternyata bergantung pada lifecycle plugin Tauri dan urutan setup. Devan menambahkan logging, lalu memastikan registration dilakukan setelah state tersedia dan sebelum window disembunyikan.

Jovian menyebut global shortcut sebagai "tombol pintu dari luar rumah". Jika tombol itu tidak bekerja ketika QuickNote bersembunyi, aplikasi akan terasa hilang. Karena itu, shortcut bukan fitur tambahan. Ia bagian dari identitas resident app.

Mereka menetapkan shortcut default sederhana, tetapi tetap menulis risiko di settings. Pada macOS, kombinasi `Ctrl+N` dapat memiliki arti berbeda di text field aplikasi lain. Pengguna harus dapat menggantinya. QuickNote tidak menyembunyikan tradeoff tersebut. Pengaturan menampilkan accelerator aktif dan memberikan kesempatan untuk memilih kombinasi lain.

Settings sheet juga tidak dibuat menjadi halaman konfigurasi besar. Ia hanya muncul ketika diminta. Pengguna dapat mengubah path note, tema, ukuran font, always on top, dan shortcut. Setelah save, window kembali ke editor. Jika accelerator baru gagal didaftarkan, nilai lama tetap menjadi nilai aktif dan config tidak boleh menipu pengguna dengan menampilkan kombinasi yang sebenarnya tidak hidup.

Devan menemukan bug ketika konfigurasi path note berubah. Backend memuat file baru, tetapi frontend masih menggunakan image resolver dari folder lama. Gambar relatif menjadi rusak. Mereka memperbarui resolver melalui `Compartment`, sama seperti font size. Ketika file berpindah, renderer mendapat directory baru tanpa menghancurkan editor dan undo history.

Myesha menyebut ini sebagai contoh bahwa file path bukan sekadar string. Path memengaruhi asset scope, image resolution, base hash, read-only state, dan session. Perpindahan note harus diperlakukan sebagai perpindahan context yang lengkap.

```text
select new note
    -> flush note lama
    -> load note baru
    -> allow directory note baru
    -> reset persistence dengan content dan hash baru
    -> replace editor secara programmatic
    -> update image resolver
    -> restore cursor dan scroll yang relevan
```

Devan menyimpan alur itu di catatan desain. Mereka pernah menganggap memilih file hanya operasi UI, lalu bug hash lama dan resolver lama muncul bersamaan. Diagram tersebut mengingatkan bahwa operasi kecil di permukaan bisa menyentuh beberapa state di bawahnya.

Mereka juga memeriksa kebijakan offline. Tauri asset protocol memang memberi akses untuk gambar lokal, tetapi tidak boleh berubah menjadi alasan untuk mengambil remote image. Resolver membedakan path lokal dan URL remote. Path lokal dapat diteruskan ke asset protocol. URL remote tetap dipaint sebagai link. Tidak ada fetch tersembunyi.

Jovian melakukan pengujian dengan mematikan Wi-Fi. Editor tetap bisa dibuka. Note tetap bisa dibaca. Autosave tetap berjalan. Syntax highlighting tidak menunggu jaringan. Settings tetap bekerja. Satu-satunya hal yang hilang adalah layanan luar yang memang tidak pernah menjadi bagian QuickNote.

"Offline bukan mode error di sini," kata Myesha. "Offline adalah keadaan normal."

Kalimat itu memengaruhi banyak keputusan. Tidak ada akun berarti tidak ada login sebelum mengetik. Tidak ada cloud berarti path file dapat dilihat dan dibackup sendiri. Tidak ada telemetry berarti aplikasi tidak perlu menunggu koneksi atau mengirim event. Tidak ada database berarti format note dapat dibaca dengan tool apa pun.

Devan lalu menguji penghapusan folder application state. Ia memindahkan `config.json` dan `session.json`, lalu membuka QuickNote. Aplikasi membuat konfigurasi default dan note tetap berada di path-nya. Cursor kembali ke awal dan ukuran window kembali ke default, tetapi isi note selamat.

Jovian lega. "Bagian ini harus ada di README. Orang perlu tahu folder mana yang aman dihapus."

Mereka menulis dokumentasi path dengan jelas: note berada di `~/QuickNote/notes.md` secara default; config dan session berada di direktori aplikasi; note tidak pernah dipindahkan ke direktori state. Dokumentasi itu membantu pengguna membedakan data utama dari kenyamanan sesi.

Pada malam terakhir implementasi menu bar, Devan mencoba menutup aplikasi dengan tiga cara: menekan `Cmd/Ctrl + W`, memilih Quit dari tray, dan menekan `Cmd/Ctrl + Q`. Ia memperhatikan ketiganya memiliki makna yang berbeda tetapi tetap mudah diingat. W menyembunyikan window. Q keluar setelah flush. Tray menyediakan pilihan yang sama tanpa membuka editor.

Myesha menambahkan satu pertanyaan terakhir. "Kalau pengguna menutup laptop saat write berlangsung?"

Mereka tidak dapat mengendalikan semua keadaan sistem. Namun, atomic write, flush on blur, flush on exit, dan recovery marker memberi perlindungan yang masuk akal. Mereka menulis batas itu secara jujur. QuickNote berusaha tidak kehilangan teks, tetapi tidak mengklaim dapat mengalahkan kerusakan hardware atau filesystem yang gagal total.

Kejujuran tersebut penting. Aplikasi yang menyimpan data pribadi harus menjelaskan apa yang dijaga dan apa yang berada di luar kendali. Kesan aman yang palsu lebih berbahaya daripada batas yang terang.

Setelah menu bar bekerja, mereka mengurangi lagi interface. Ada beberapa tombol debug yang tertinggal di window. Tombol itu berguna saat development, tetapi tidak memiliki tempat di produk. Mereka memindahkan fungsi yang dibutuhkan ke shortcut dan settings, lalu menghapus tombol permanen.

Jovian mengamati perubahan itu. "Setiap kali kita memperbaiki sistem di belakang, tampilan malah menjadi lebih kosong."

"Itu tanda yang baik untuk QuickNote," kata Devan. "Kerja kerasnya seharusnya mengurangi beban yang harus dilihat pengguna."

Mereka membuat screenshot final. Satu kolom di tengah. Teks Markdown yang tampil live. Status `saved` di sudut. Tidak ada panel lain. Di atas layar, icon menu bar terlihat kecil, hampir seperti tidak ada.

Myesha menyimpan screenshot itu bukan untuk menunjukkan semua fitur. Ia menyimpannya untuk mengingat batas. Jika suatu hari interface mulai penuh lagi, mereka dapat membandingkannya dengan gambar tersebut dan bertanya apa yang berubah.

Tetapi mereka masih harus menjawab satu pertanyaan yang tidak kalah penting. Mengapa aplikasi ini perlu ada jika Obsidian, Notion, dan editor lain sudah tersedia?

## Bab 5: Bukan Pengganti, Melainkan Pintu Masuk

Beberapa hari setelah QuickNote bisa dipakai, Devan memperlihatkannya kepada beberapa teman. Reaksi pertama hampir selalu sama. Mereka membuka window yang kosong, mengetik beberapa baris, lalu bertanya, "Folder-nya di mana?"

Devan menjelaskan bahwa QuickNote memakai satu file utama. Temannya bertanya lagi, "Bagaimana membuat workspace?"

"Tidak ada workspace."

"Kalau plugin?"

"Tidak ada plugin."

"Kalau sync?"

"Tidak ada sync bawaan. File-nya bisa kamu backup atau taruh di sistem yang memang kamu percaya."

Sebagian orang terlihat bingung. Sebagian lain terlihat lega. Devan mulai memahami bahwa minimal bukan hanya soal menghapus tombol. Minimal berarti menetapkan batas yang mungkin terasa tidak lengkap bagi seseorang, tetapi justru menjaga fokus bagi orang lain.

Myesha meminta mereka menulis dengan jelas apa yang bukan tujuan QuickNote. Mereka tidak ingin pengguna mengira aplikasi ini hendak mengganti alat yang sudah bagus. Obsidian tetap cocok untuk knowledge base pribadi yang memiliki backlink, graph, folder, dan banyak halaman. Notion tetap cocok untuk workspace, database, template, dan kolaborasi. VS Code tetap cocok untuk proyek kode yang memerlukan banyak file, terminal, extension, dan debugging.

QuickNote punya ruang yang lebih kecil. Ia cocok ketika seseorang ingin mencatat ide, daftar TODO, command, potongan kode, hasil meeting, draft pesan, checklist belanja, atau sesuatu yang belum tahu akan menjadi apa.

"Catatan sementara juga tetap punya nilai," kata Jovian. "Tidak semua teks harus langsung menjadi halaman permanen."

Devan teringat kebiasaan lamanya. Ia sering menolak menulis ide karena belum tahu akan disimpan di mana. Ia ingin setiap catatan memiliki kategori yang tepat, nama yang bagus, dan hubungan dengan catatan lain. Keinginan itu bagus untuk pengetahuan yang sudah matang. Untuk pikiran yang baru muncul, tuntutan tersebut terlalu berat.

QuickNote memberi tempat untuk fase sebelum organisasi. Teks dapat tetap satu file sampai pengguna memutuskan apa yang harus dilakukan. Jika ternyata hanya catatan sementara, ia tetap berguna. Jika berubah menjadi dokumen penting, pengguna dapat memindahkannya ke sistem lain karena formatnya plain Markdown.

Mereka membuat beberapa skenario penggunaan.

Skenario pertama terjadi saat Devan sedang debugging. Ia menemukan bahwa urutan pemeriksaan hash harus terjadi sebelum `noteSave`, bukan sesudahnya. Ia menekan `Ctrl+N`, mengetik tiga baris, lalu kembali ke terminal. Ia tidak membuka editor besar, tidak membuat issue, dan tidak berpindah workspace. Catatan itu menunggu di file yang sama.

```markdown
## Autosave investigation

- Compare disk content with `baseHash` before writing.
- Keep the external version as a conflict copy.
- Update `baseHash` only after the write belongs to the current generation.
```

Skenario kedua terjadi ketika Myesha mengikuti meeting singkat. Ia perlu mencatat keputusan sebelum pembicaraan berganti topik. QuickNote terbuka di atas layar, lalu ia menulis heading dan checklist. Tidak ada format khusus yang harus dipilih. Markdown langsung terlihat rapi. Setelah meeting, ia dapat memindahkan bagian penting ke dokumen tim.

Skenario ketiga terjadi pada Jovian saat ia sedang belajar. Ia ingin menyimpan command dan satu penjelasan pendek. Code block memberi syntax highlighting, tetapi file tetap teks biasa. Jika ia membuka file tersebut di editor lain, isinya tidak berubah menjadi format yang hanya dimengerti QuickNote.

Skenario keempat lebih emosional. Pada suatu malam di Sleman, Devan mendengar kabar dari kampung ayahnya di Takengon. Ia ingin menulis beberapa kalimat sebelum menelepon keluarga. Ia tidak sedang mencari sistem arsip. Ia hanya membutuhkan permukaan yang tidak bertanya banyak.

Ia membuka QuickNote, mengetik, dan menutup window. Tidak ada suara notifikasi. Tidak ada dialog. Kalimat tersebut aman di file. Teknologi tidak menghapus rasa cemas yang ia bawa, tetapi teknologi juga tidak menambah pekerjaan baru ketika pikirannya sedang penuh.

Myesha melihatnya dari pintu. Ia tidak bertanya isi catatan. Ia hanya bertanya apakah sudah tersimpan.

Devan melihat status `saved`. "Sudah, Kak."

Momen itu membuat definisi QuickNote menjadi lebih jelas. Aplikasi ini bukan tentang jumlah fitur. Ia tentang mengurangi keputusan pada saat pengguna hanya ingin menjaga satu pikiran.

Tentu, batas kecil tetap memerlukan kualitas teknis. Mereka tidak boleh memakai kata sederhana sebagai alasan untuk mengabaikan test. Repository QuickNote sekarang memiliki TypeScript typecheck, oxlint, Prettier, Vitest, dan test Rust. Mereka menetapkan batas ukuran file dan fungsi agar alasan desain tetap mudah dibaca.

Perubahan struktural itu membantu mereka merawat proyek. `main.ts` tidak lagi menjadi file raksasa. Modul editor dipisah menjadi render blocks, inline, marks, images, callouts, dan builder. Theme dipisah dari editor. Bridge dipisah dari persistence. Rust memisahkan note, storage, settings, state, window, tray, dan commands.

Jovian bertanya apakah pemisahan itu tidak bertentangan dengan prinsip minimal.

"Tidak," jawab Myesha. "Minimal untuk pengguna tidak berarti satu file besar untuk developer. Pengguna membutuhkan interface yang tenang. Developer membutuhkan batas modul yang jelas. Dua kebutuhan itu tidak sama."

Mereka menjalankan pemeriksaan proyek.

```bash
npm run typecheck
npm run lint
npm run format:check
npm run test
```

Test tidak hanya mencari error sintaks. Test persistence memastikan reset tidak membawa hash file lama. Test atomic write memastikan staging file tidak tersisa. Test shortcut memastikan hanya satu caller yang memulai exit. Test editor memastikan perubahan programmatic tidak memicu autosave. Test renderer memastikan callout, table, image, dan code block tetap tampil sesuai source.

Devan menambahkan test untuk conflict. Ia menulis content pertama, mengubah file dari luar, lalu menulis content kedua dari QuickNote. Ia memastikan file utama berisi versi pengguna dan conflict copy berisi versi eksternal. Ia memastikan dua conflict yang terjadi pada detik yang sama tidak saling menimpa karena nama file menggunakan counter ketika timestamp sama.

Myesha menambahkan test untuk note yang dihapus. Setelah `missing: true`, notice harus muncul dan editor harus tetap menyimpan content ketika path dibuat kembali. Ia tidak ingin aplikasi memperbaiki keadaan secara diam-diam lalu membuat pengguna tidak tahu bahwa ada file yang hilang.

Jovian menguji shortcut. Ia memakai `Ctrl+N` untuk membuka dan menyembunyikan window. Ia mencoba accelerator yang invalid. Shortcut lama tetap bekerja. Ia mencoba kombinasi yang sudah dipakai aplikasi lain. QuickNote menolak perubahan dan menyimpan kombinasi yang sebelumnya terdaftar.

Setiap test membuat aplikasi menjadi sedikit lebih lambat untuk dikembangkan, tetapi membuat pengguna memiliki lebih sedikit alasan untuk takut. Itu tradeoff yang mereka terima. Aplikasi yang hanya menyimpan catatan cepat tidak boleh membuat pengguna bertanya apakah catatannya masih ada.

Pada tahap ini, seseorang mengusulkan fitur cloud sync. Usulan itu terdengar masuk akal. Banyak orang memakai beberapa device. Satu file lokal memiliki batas. Devan menulisnya di daftar ide, lalu membawa pertanyaan Myesha: apakah sync membuat QuickNote lebih cepat, lebih sederhana, atau lebih nyaman untuk quick note?

Jawabannya tidak sederhana. Sync bisa nyaman, tetapi juga menambah akun, server, login, konflik jaringan, status koneksi, dan pertanyaan privasi. Semua itu mungkin layak untuk produk lain. Untuk versi QuickNote sekarang, mereka memilih tidak menambahkannya. Pengguna dapat menaruh file di mekanisme sinkronisasi yang sudah mereka pahami, dengan risiko dan aturan yang terlihat.

Usulan workspace juga ditolak. Workspace akan membantu sebagian pengguna, tetapi akan menghidupkan kembali pintu yang ingin mereka tutup. Folder otomatis, tab, plugin, dan database memiliki manfaat. QuickNote tidak mengatakan manfaat tersebut tidak ada. QuickNote hanya mengatakan bahwa kebutuhan itu berada di luar pekerjaannya.

Devan menulis kalimat tersebut di README.

```text
QuickNote is not Notion, Obsidian, or VS Code.
It holds one note and tries to make that one note feel effortless.
```

Kalimat itu bukan permintaan maaf. Itu adalah kontrak. Pengguna tahu apa yang akan mereka dapatkan dan apa yang tidak perlu mereka harapkan.

Di rumah, Myesha membuat teh. Jovian membuka issue tracker dan membersihkan beberapa issue yang sudah tidak sesuai scope. Devan melihat layar QuickNote. Status di sudut masih satu kata. Window masih hampir kosong. Icon masih duduk tenang di menu bar.

"Kak," kata Devan, "apakah aplikasi ini terlalu kecil?"

Myesha menatapnya. "Kecil dibanding apa?"

"Dibanding aplikasi note yang bisa mengatur database, graph, plugin, dan semuanya."

"QuickNote tidak menang dengan menjadi lebih besar," jawab Myesha. "Ia menang kalau pengguna bisa menangkap pikiran sebelum pikiran itu hilang."

Jovian ikut berbicara dari sofa. "Kalau seseorang membuka QuickNote dan langsung mengetik tanpa merasa sedang mengurus aplikasi, berarti kita sudah berhasil."

Devan tersenyum. Ia mengingat malam pertama. Ia hanya ingin menyimpan satu kalimat tentang autosave. Saat itu, satu kalimat terasa sulit karena aplikasi yang tersedia meminta terlalu banyak keputusan. Sekarang ia memahami bahwa kebutuhan tersebut bukan keluhan terhadap aplikasi besar. Ia hanya membutuhkan alat dengan pekerjaan yang berbeda.

Notion tidak menjadi buruk karena QuickNote ada. Obsidian tidak menjadi kurang berguna. Editor kode tidak kehilangan tempatnya. QuickNote hanya mengisi celah kecil di antara pikiran yang muncul dan sistem yang sudah rapi.

Celakanya, celah itu sering menjadi tempat ide mati.

Satu klik yang terlalu jauh. Satu dialog yang terlalu banyak. Satu folder yang belum dipilih. Satu nama file yang belum ditemukan. Satu detik ragu. Setelah itu, ide hilang bersama distraksi berikutnya.

QuickNote mencoba memotong rangkaian tersebut. `Ctrl+N` membuka pintu. Cursor sudah siap. Markdown tampil tanpa pane kedua. Autosave menjaga perubahan. Atomic write menjaga file dari hasil setengah jadi. Conflict copy menjaga versi eksternal. Menu bar menjaga aplikasi tetap dekat tanpa meminta seluruh layar.

Semua keputusan itu mengarah ke satu pekerjaan yang sama: membuat catatan cepat terasa ringan, tetapi tetap dapat dipercaya.

Menjelang malam, Devan menulis catatan terakhir untuk hari itu.

```markdown
QuickNote tidak perlu menjadi rumah bagi semua pengetahuan.
Ia cukup menjadi tempat aman untuk pikiran yang baru datang.
```

Ia menutup window. Status berubah menjadi `saved`. Icon QuickNote tetap berada di menu bar. Myesha mematikan lampu ruang kerja. Jovian menyimpan roti terakhir ke dapur.

Di luar, Sleman kembali tenang. Tidak ada pengumuman besar. Tidak ada peluncuran yang mengubah dunia. Hanya satu aplikasi kecil yang terus menunggu di dekat jam, siap menerima kalimat berikutnya.

Dan mungkin memang itu alasan utama QuickNote ada.

Bukan untuk menggantikan Obsidian.

Bukan untuk mengalahkan Notion.

Bukan untuk menjadi editor yang mengurus semua hal.

QuickNote ada karena terlalu banyak aplikasi note membuat catatan sederhana terasa seperti proyek. Ia ada untuk pembuatan note cepat, ketika pengguna belum butuh organisasi, kolaborasi, plugin, atau graph. Ia ada untuk momen ketika satu kalimat lebih penting daripada semua struktur yang mungkin mengelilinginya.

Ketik. Tutup. Catatan tetap ada.

Kadang, aplikasi yang paling berguna bukan aplikasi yang paling banyak melakukan hal. Kadang, aplikasi yang paling berguna adalah aplikasi yang tahu kapan harus berhenti mengganggu.

Mereka lalu membuat halaman kontribusi untuk menjaga keputusan itu tetap hidup. Setiap feature baru harus melewati satu pertanyaan: apakah feature ini membuat QuickNote lebih cepat, lebih sederhana, atau lebih nyaman untuk quick note? Pertanyaan tersebut tidak melarang perubahan. Ia meminta perubahan membawa alasan yang dapat dipertanggungjawabkan.

Jika seseorang mengusulkan tag, mereka perlu menjelaskan apakah tag mempercepat pencarian satu note atau justru membuat pengguna mengatur note sebelum menulis. Jika seseorang mengusulkan tab, mereka perlu menjelaskan apakah tab mengurangi langkah atau mengubah QuickNote menjadi workspace. Jika seseorang mengusulkan sync, mereka perlu menjelaskan dampaknya pada offline-first, privacy, dan conflict handling.

Dengan cara itu, scope bukan hanya keputusan di kepala tiga bersaudara. Scope menjadi bagian dari repository. README menjelaskan apa yang dilakukan. Product requirements menjelaskan mengapa keputusan dibuat. Test menjaga perilaku yang dianggap penting. Comment di source menjelaskan bagian yang mudah disalahpahami.

Devan membuka README dan membaca bagian `What QuickNote is not`. Ia merasa bagian itu sama penting dengan daftar feature. Pengguna perlu tahu bahwa aplikasi ini tidak memiliki workspace, tab, plugin, sync, akun, atau database. Developer juga perlu tahu bahwa menambahkan salah satu komponen tersebut bukan perubahan kecil yang berdiri sendiri. Ia membawa model produk baru.

Myesha menambahkan kalimat lain: "QuickNote holds one note and tries to make that one note feel effortless." Ia ingin kata `one` tetap ada. Satu note adalah batas yang memberi aplikasi karakternya.

Jovian menguji apakah batas itu membuat file sulit dibawa ke sistem lain. Ia menyalin `notes.md` ke folder proyek, membukanya di editor kode, dan memasukkannya ke Git. Heading, checklist, dan code block tetap utuh. Ia membuka file tersebut dari editor lain, mengubah satu baris, lalu membiarkan QuickNote memproses conflict copy.

Semua data tetap berada di tempat yang bisa disentuh pengguna. Tidak ada ekspor khusus yang harus dilakukan sebelum pindah aplikasi. Format yang terbuka menjadi jembatan antara aplikasi kecil dan tool yang lebih besar.

Devan membayangkan masa depan catatan mereka. Beberapa kalimat akan tetap tinggal di `notes.md`. Beberapa akan dipindahkan ke wiki. Beberapa akan berubah menjadi issue. Beberapa akan dihapus karena sudah tidak penting. QuickNote tidak perlu menentukan hasilnya. Ia cukup menjaga fase awal tetap murah.

Itu membuat aplikasi ini berbeda dari sistem pengetahuan. Sistem pengetahuan meminta pengguna memelihara hubungan, struktur, dan konteks. QuickNote memberi pengguna tempat untuk menunda keputusan tersebut. Keduanya dapat hidup berdampingan. Bahkan, sistem pengetahuan yang baik sering membutuhkan tempat penampungan sebelum materi baru disusun.

Di rumah mereka, Myesha membuat kebiasaan baru. Setiap kali ide datang saat mengerjakan hal lain, ia menekan shortcut, menulis satu atau dua kalimat, lalu menyembunyikan window. Ia tidak memaksa dirinya mengatur catatan saat itu juga. Pada akhir hari, ia membaca file dan memutuskan mana yang perlu dipindahkan.

Devan melakukan hal yang sama ketika debugging. Ia tidak lagi membuat dokumen baru hanya untuk mencatat satu hipotesis. Jovian memakai QuickNote untuk menyimpan command yang belum cukup matang menjadi dokumentasi. Ketiganya memakai aplikasi dengan cara berbeda, tetapi mereka berbagi satu pengalaman: catatan pertama tidak lagi memiliki biaya mental yang besar.

Suatu pagi, mereka membahas kemungkinan membawa QuickNote ke Windows dan Linux. Build untuk platform tersebut dapat dibuat dari source yang sama, walau jalur signing dan packaging berbeda. Mereka tidak menjanjikan pengalaman platform yang identik pada setiap detail. Mereka ingin core behavior tetap sama: file terbuka, editor siap, autosave berjalan, shortcut configurable, dan data lokal tetap milik pengguna.

Jovian bertanya apakah release unsigned akan membuat onboarding lebih sulit. Devan mencatatnya sebagai pekerjaan distribusi, bukan alasan untuk mengubah model aplikasi. Mereka dapat menjelaskan warning sistem operasi di dokumentasi sambil menjaga kode tetap lintas platform.

Myesha mengingatkan agar mereka tidak menggunakan roadmap untuk mengubah janji saat ini. "Rencana masa depan boleh ada. Tetapi pengguna hari ini harus bisa memahami QuickNote tanpa membaca seluruh rencana."

Devan lalu menulis ringkasan pendek untuk halaman proyek:

```markdown
QuickNote is a local-first Markdown desktop app for quick notes.
It is a digital sheet of paper that is always available.
It is not a replacement for a knowledge base or a workspace.
```

Ringkasan itu terasa tenang. Tidak ada klaim bahwa QuickNote akan mengubah cara semua orang bekerja. Tidak ada janji bahwa satu aplikasi dapat menyelesaikan seluruh masalah catatan. Hanya batas, tujuan, dan cara kerja.

Repositori [github.com/khairu-aqsara/quicknote](https://github.com/khairu-aqsara/quicknote) menyimpan kode, README, dan pagar yang sama untuk setiap ide baru. Pembaca yang ingin ikut menjaga pagar itu boleh datang lewat issue atau pull request.

Malam terakhir, mereka makan bersama. Percakapan bergeser dari kode ke hal-hal yang lebih biasa. Myesha bercerita tentang rumah keluarga di Krui. Jovian mengingat perjalanan ke Pante Raya. Devan menyebut bahwa beberapa ide terbaiknya muncul ketika ia sedang tidak duduk di depan meja kerja.

"Berarti QuickNote harus siap bukan hanya saat kita sedang serius," kata Jovian. "Ia harus siap ketika ide muncul di antara dua hal."

"Itulah arti selalu tersedia," jawab Myesha. "Bukan berarti selalu meminta perhatian."

Devan memikirkan perbedaan itu. Aplikasi yang selalu terbuka dapat terasa mengganggu jika terus menampilkan badge dan notifikasi. QuickNote memilih menjadi resident tanpa menjadi noisy. Ia ada di menu bar, bukan di tengah pekerjaan. Ia muncul ketika dipanggil, lalu mundur ketika selesai.

Setelah makan, Devan kembali ke meja dan menulis satu catatan terakhir. Ia tidak membuat heading. Ia tidak memasang tag. Ia tidak memilih folder. Ia hanya menulis:

```markdown
Catatan cepat adalah pintu, bukan rumah terakhir.
```

Ia membaca kalimat itu. Ada kemungkinan kalimat tersebut akan dipindah ke halaman lain. Ada kemungkinan ia hanya menjadi penutup proyek. Dua kemungkinan itu tidak perlu diputuskan malam itu.

QuickNote sudah melakukan pekerjaannya.

Pagi berikutnya, aplikasi dibuka dari menu bar. Cursor langsung berada di editor. Status menunjukkan `saved`. Devan mengetik kalimat baru, menutup window, dan melanjutkan pekerjaan lain. Tidak ada perasaan bahwa ia baru saja memulai sistem besar. Tidak ada perasaan bahwa ia harus mengurus aplikasi.

Di situlah nilai QuickNote akhirnya terasa. Bukan ketika ia menampilkan daftar feature. Bukan ketika codebase-nya berhasil melewati semua test. Nilainya terlihat ketika aplikasi menghilang dari pikiran pengguna setelah membantu mereka menyimpan sesuatu.

Ia melakukan sedikit, tetapi melakukannya dengan niat yang jelas.

Kalau suatu hari Devan membutuhkan graph, ia akan membuka Obsidian. Kalau ia membutuhkan database atau kolaborasi, ia akan membuka Notion. Kalau ia perlu mengedit banyak file, ia akan membuka VS Code. Tidak ada konflik di antara tool tersebut. QuickNote hanya menjadi tempat pertama ketika ide belum memiliki bentuk yang pasti.

Dan ketika ide itu sudah matang, pengguna bebas membawanya pergi. File Markdown tetap berada di tangan mereka. Tidak ada dinding yang membuat catatan harus tinggal selamanya di QuickNote.

Tiga bersaudara itu tidak membangun aplikasi yang ingin menjadi pusat semua hal. Mereka membangun sebuah pintu kecil di dekat tempat mereka bekerja. Pintu itu tidak menjanjikan pemandangan luas. Ia hanya mudah dibuka, tidak mengunci pemiliknya, dan menutup tanpa meninggalkan barang di luar.

Di Sleman, malam kembali turun. Icon kecil QuickNote tetap menyala di menu bar. Mungkin besok ada ide baru. Mungkin hanya checklist pendek. Mungkin potongan kode yang nanti dibuang. Apa pun bentuknya, editor akan siap.

Ketik.

Tutup.

Catatan tetap ada.
