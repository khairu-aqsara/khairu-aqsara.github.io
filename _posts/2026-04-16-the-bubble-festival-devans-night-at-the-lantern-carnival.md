---
layout: post
title: "Festival Bubble Sort: Malam Devan di Karnaval Lentera"
subtitle: "Ketika mengurutkan ribuan lentera mengajarkan arti kesabaran yang sebenarnya"
date: 2026-04-16 00:00:00 +0700
categories: [tech, software-development, algorithms]
tags: [python, algorithms, bubble-sort, sorting, problem-solving, learning]
author: Kuli Kode
---

Malam itu udara Jakarta terasa berat,baunya campur antara aroma jagung panggang dan minyak tanah. Devan lagi duduk di tengah ribuan lentera, tangannya capek banget karena baru aja selesein ratusan lentera. Karnaval Lentera anual punya tugassimpel tapi berat: urutin lentera berdasarkan ukuran buat booth penilaian. Ada tiga ribu lentera, dari yang super kecil kayak lampu teh sampai yang gede banget kayak lentera langit, tersebar di tanah kayak chaos total. HP dia bergetar—ketika pesan dari Myesha, partner coding-nya, nanya "Gimana setup-nya? Ada yang bisa dibantu?"

Devan ngelihat gunung kertas dan bambu di hadapannya,tau-tiba jadi nervous. Dia punya tiga jam sebelum hakim datang. Otaknya yang biasa mikir dalam loops dan conditions, langsung kepikiran cara paling primitif yang manusia bisa lakuin. Bukan quicksort atau merge sort—justru cara paling natural yang orang punya buat bikin order dari kekacauan. Terus inget deh sama pelajaran Pak Rahman, mentor mereka dulu. Waktu itu diajarin tentang Bubble Sort, algoritma yang super sederhana sampe anak kecil juga bisa ngerti. Tapi Pak Rahman pernah punya warning: simplicity itu pedang bermata dua—gampang dipelajarin tapi susah dikuasain.

## Bab 1: Kekacauan Tiga Ribu Lentera

Lapangan bersinar kayak langit yang jatuh, lentera-lentera dengan berbagai ukuran dan warna tergeletak dalam pola yang mutlak nggak predictable. Devan disuruh ngaturin lentera berdasarkan ukuran karena, kata organizadores karnaval, "Kau kan orang teknology, pasti tau cara ngatur barang." Asumsi bahwa bisa coding sama dengan bisa ngurutin benda fisik adalah fallacy yang lagi banget Devan rasain. Dia ambil lentera merah gede, terus lampu teh kecil, terus lentera kertas ukuran sedang, terus realize kalau dia nggak punya sistem sama sekali.

Insting pertama dia adalah ambil lentera terbesar terus taruh di depan, terus cari yang terbesar kedua, terus terbesar ketiga. Ini tuh yang потом disebut selection sort, meskipun Devan belum tau nama itu. Dia kerja frenzy selama dua puluh menit, keringat mengalir meski udara malam dingin. Dia berhasil mengurutkan sekitar dua ratus lentera sebelum berhenti, ngelihat hasilnya, dan realize kalau dia kehilangan puluhan lentera. Mungkin kehembus angin dari arah kios makanan, atau gimana gitu. Lapangan masih berantakan, dan sekarang dia juga exhaustion.

> "Di tengah kesulitan tersembunyi peluang." — Albert Einstein

Devan duduk di atas kardus kosong, ambil HP dan cari di google "caranya urutin barang dengan efisien." Dia scroll artikel tentang Big O notation, tutorial tentang kompleksitas algoritma, sampe ketemu sesuatu yang bikin dia pause: animasi sederhana bubble sort, dengan elemen perlahan "menggelembung" ke posisi yang benar. Terpesona. Konsepnya elegan dalam kesederhanaannya—bandingkan item-item yang bersebelahan, tukar kalau urutannya salah, dan ulang sampe seluruh list terurut. Kayak gelembung udara naik ke permukaan air, makanya dinamain bubble sort. Dia tonton animasi itu tiga kali, terus lihat lapangan lentera三千 dengan mata baru.

## Bab 2: Pass Pertama

Devan mulai berjalan di baris pertama lentera, memperlakukan setiap pasang sebagai perbandingan. Dia ambil lentera sedang, lihat ukurannya, terus bandingin sama yang di sebelahnya. Kalau yang sedang lebih besar dari tetangganya, dia akan tukar posisi mereka. Kalau nggak, dia lanjut. Prosesnya melelahkan tapi entah gimana jadi meditatif. Dengan setiap langkah, setiap perbandingan dan pertukaran, dia bisa lihat lentera-lentera terbesar bergerak ke depan barisan secara gradual.

Dia buat pass pertama lengkap melintasi seluruh lapangan, dan yah, lentera terbesar sudah menggelembung ke depan. Tapi pas lihat sisanya, dia lihat lentera-lentera kecil udah jadi混lagi. Algoritma belum selesai—butuh multiple passes. Devan mulai pass kedua, bergerak lebih pelan sekarang, ngerti ritme prosesnya. Lentera terbesar yang tersisa bergerak ke posisi dua. Pass ketiga mendorong yang ketiga terbesar ke posisi tiga.

Sampai pass keempat, Devan berhenti. Dia ambil HP dan cek waktu—satu jam sudah berlalu, dan dia baru ngurutin beberapa posisi pertama. Dengan kecepatan ini, dia butuh tiga ribu passes, masing-masing pass butuh sejam. Itu bakal jadi tiga ribu jam, atau sekitar 125 hari. Hakim bakal dateng dalam tiga jam, bukan 125 hari. Ada yang salah fundamental dari pendekatan dia.

```python
# Bubble sort naif - implementasi pertama Devan
def bubble_sort_naif(lentera):
    n = len(lentera)
    passes = 0
    
    for i in range(n):
        for j in range(n - 1):
            if lentera[j] > lentera[j + 1]:
                # Tukar lentera yang bersebelahan
                lentera[j], lentera[j + 1] = lentera[j + 1], lentera[j]
                passes += 1
                
        # Setelah setiap pass, elemen terbesar ada di posisi final
        print(f"Pass {i + 1} selesai: {passes} pertukaran dilakukan")
    
    return lentera
```

Kode itu look exactly sama dengan yang dia lakukan di lapangan—membandingkan setiap pasang, menukar kalau perlu, mengulang. Dan seperti upaya fisiknya, itu sangat tidak efisien. Dia membuat n passes melalui n elemen, menghasilkan n² perbandingan. Untuk tiga ribu lentera, itu sembilan juta perbandingan. Bahkan satu perbandingan per detik, itu butuh lebih dari 100 hari. Algoritmanya benar, tapi tidak praktis untuk deadline dia.

> "Optimasi premature adalah akar dari segala kejahatan." — Donald Knuth

Devan realize kalau dia terlalu fokus make algoritma jalan sampe lupa考慮 dia menggunakan algoritma itu dengan benar atau tidak. Bubble sort dinamain sesuai cara elemen "menggelembung" ke posisi yang benar, tapi itu bukan berarti dia harus buat pass penuh untuk setiap elemen. Optimasi yang dia butuhkan sudah built-in ke algoritma—cuma belum dia realize.

## Bab 3: Realisasi di Tengah Malam

Tengah malam approaches, dan Devan belum banyak kemajuan. Dia duduk surrounded by lentera, laptop di pangkuannya, staring di kode bubble sort. Myesha sudah messaging lagi: " gimana? perlu bantuan?" Dia ketik "iya" tiga kali terus hapus masing-masing. Dia pengen figured sendiri. Pasti ada cara lebih baik, dan jawabannya somewhere di algoritma itu sendiri.

Dia pikirin apa yang terjadi selama setiap pass. Setelah pass pertama, elemen terbesar pasti di posisi final. Setelah pass kedua, yang kedua terbesar sudah fixed. Setelah pass ketiga, yang ketiga terbesar sudah di tempat. Dia nggak perlu bandingin elemen-elemen itu lagi! Setiap pass secara otomatis fixed minimal satu elemen—yang terbesar di bagian yang belum terurut. Dia waste perbandingan dengan membandingkan elemen yang sudah tersorted.

Devan ambil lentera dan gambar lapangan di tanah dengan stick. Dia mark posisi satu sampai sepuluh dan taruh "ukuran" acak di setiap posisi (direpresentasikan angka). Terus trace algoritma bubble sort dengan jarinya, tapi kali ini berhenti di batas yang belum terurut. Pass pertama, dia hanya bandingkan sampai posisi sembilan (bukan sepuluh), karena posisi terakhir sudah dijamin punya elemen terbesar. Pass kedua, hanya sampe posisi delapan. Optimasi jadi jelas—in loop yang mengecil dengan setiap outer iteration.

```python
# Bubble sort yang dioptimasi - breakthrough Devan
def bubble_sort_teroptimasi(lentera):
    n = len(lentera)
    
    for i in range(n):
        # Setelah setiap pass, elemen i terakhir sudah tersorted
        # Jadi kita hanya perlu membandingkan sampai n - i - 1
        swapped = False
        
        for j in range(n - i - 1):
            if lentera[j] > lentera[j + 1]:
                lentera[j], lentera[j + 1] = lentera[j + 1], lentera[j]
                swapped = True
        
        # Jika tidak ada pertukaran, array sudah terurut
        if not swapped:
            break
            
        print(f"Pass {i + 1} selesai: {i + 1} elemen terbesar terurut")
    
    return lentera
```

Tapi ada satu optimasi lagi yang dia missing, yang butuh thinking tentang data itu sendiri. Bagaimana kalau list lentera hampir terurut, dengan hanya beberapa elemen di tempat yang salah? Bagaimana kalau sebagian besar kerja sudah selesai?

## Bab 4: Balapan Melawan Waktu

Devan lihat lapangan lentera lagi, sekarang dengan mata baru. Dia bukan lagi melihat chaos—dia melihat list yang hampir terurut yang hanya butuh beberapa pertukaran strategis. Lentera-lentera terbesar sudah di dekat depan, yang terkecil di belakang. Bagaimana kalau dia bisa detect kapan list sudah terurut dan berhenti?

Dia modifikasi algoritma mental sekali lagi. Bagaimana kalau, setelah setiap pass, dia tracking apakah ada pertukaran yang terjadi? Jika pass selesai dengan nol pertukaran, itu berarti setiap pasang berdekatan sudah dalam urutan yang benar, yang berarti seluruh list terurut. Dia bisa berhenti. Optimasinya elegan dalam kesederhanaannya—kayak cek apakah sungai sudah berhenti mengalir daripada mengukur setiap tetes air.

```python
# Bubble sort sepenuhnya dioptimasi dengan early termination
def bubble_sort_early_termination(lentera):
    n = len(lentera)
    
    for i in range(n):
        swapped = False
        
        # Optimasi kunci: perkecil jendela perbandingan
        # Setelah i passes, elemen i terakhir sudah tersorted
        for j in range(n - i - 1):
            if lentera[j] > lentera[j + 1]:
                # Tukar jika elemen dalam urutan yang salah
                lentera[j], lentera[j + 1] = lentera[j + 1], lentera[j]
                swapped = True
        
        # Early termination: jika tidak ada pertukaran, array terurut
        if not swapped:
            print(f"Array terurut setelah {i + 1} passes!")
            break
    
    return lentera
```

Algoritma baru bakal mengurangi jumlah perbandingan secara signifikan. Dalam worst case (terbalik terurut), masih butuh n² perbandingan, tapi dalam best case (sudah terurut), hanya butuh n perbandingan—satu pass dan selesai. Dalam skenario hampir terurut, yang tepat seperti yang Devan hadapi, bakal selesai dalam beberapa passes.

> "Kode terbaik adalah tidak ada kode sama sekali. Kode kedua terbaik adalah kode yang bekerja dengan efisien." — Jeff Atwood

Devan berdiri, regang punggungnya yang sakit, dan lihat jam. Jam 1 pagi. Dia punya dua jam tersisa. Dia mulai pendekatan baru, berjalan melalui lapangan tapi sekarang dengan sistem. Dia bakal buat passes melalui bagian yang belum terurut, dan setelah setiap pass, dia bakal cek apakah ada pertukaran. Jika tidak ada pertukaran, dia bakal berhenti karena lentera akan terurut. Selain itu, dia bakal perkecil bagian yang belum terurut setelah setiap pass, tau kalau lentera terbesar yang belum terurut sudah menemukan rumahnya.

## Bab 5: Dorongan Terakhir

Jam 1:30 pagi, Devan mulai proses pengurutan yang dioptimasi. Dia bergerak melalui lentera dengan determinasi yang fierce, tapi juga ada ketenangan yang aneh. Setiap pass lebih cepat dari pass sebelumnya karena lebih sedikit lentera untuk dibandingkan. Dia bisa melihat yang terbesar naik ke depan, kayak gelembung di dalam gelas air. Lapangan mulai berubah dari chaos ke order di depan matanya.

Pass satu selesai: ratusan pertukaran. Pass dua: lebih sedikit pertukaran. Pass tiga: lebih sedikit lagi. Sampe pass lima, dia hanya membuat segelintir pertukaran. Sampe pass enam, dia buat nol pertukaran. Lentera-lentera terurut. Dia cek jam—1:47 pagi. Dia sudah melakukan dalam kurang dari satu jam apa yang dia pikir bakal butuh hari. Algoritma работает, tapi lebih penting lagi, dia ngerti kenapa bekerja. Dia sudah internalisasi konsep batas yang mengecil, early termination, dan power dari optimasi sederhana.

```python
# Menguji bubble sort yang dioptimasi
import random
import time

# Buat list 1000 "ukuran" lentera acak (1-100)
ukuran_lentera = [random.randint(1, 100) for _ in range(1000)]

print("Mulai bubble sort pada 1000 elemen...")
start_time = time.time()

lentera_terurut = bubble_sort_early_termination(ukuran_lentera)

end_time = time.time()
print(f"Pengurutan selesai dalam {end_time - start_time:.4f} detik")

# Verifikasi pengurutan berhasil dengan benar
print(f"10 ukuran pertama: {lentera_terurut[:10]}")
print(f"10 ukuran terakhir: {lentera_terurut[-10:]}")
print(f"Terurut: {all(lentera_terurut[i] <= lentera_terurut[i+1] for i in range(len(lentera_terurut)-1))}")
```

Kode itu, ketika dijalankan, bakal menunjukkan exactly apa yang terjadi di lapangan. Dalam worst case, bubble sort butuh waktu O(n²), tapi dengan optimasi—early termination dan mengecilkan batas—bisa jauh lebih cepat dalam praktik. Untuk data hampir terurut, bisa mendekati waktu O(n). Itu power dari memahami algoritma, bukan hanya mengimplementasikannya.

## Bab 6: Fajar Pemahaman

Ketika hakim tiba jam 6 pagi, mereka menemukan lapangan lentera yang sempurna terorganisir, diurutkan dari terkecil hingga terbesar. Mereka mengagumi presisi, bertanya pada Devan bagaimana dia bisa melakukan keajaiban dalam waktu sesingkat itu. Dia tersenyum dan bilang dia menggunakan algoritma yang nature itself sepertinya mengerti—cara gelembung udara naik melalui air, cara kartu-kartu yang terurut menemukan tempatnya di tumpukan.

Karnaval sukses besar. Lentera-lentera Devan terpajang dengan sempurna, menarik kekaguman ribuan pengunjung. Tapi lebih penting lagi, dia sudah belajar satu pelajaran yang akan stay dengannya sepanjang karir programmingnya. Bubble sort sering dianggap tidak efisien, alat pengajaran untuk pemula, curiosity dari sejarah ilmu komputer. Tapi seperti semua tools, nilainya tergantung bagaimana dan kapan lo gunain.

> "Pengetahuan tidak ada nilainya kecuali kamu把它 masukkan ke dalam praktik." — Anton Chekhov

Ketika dia ketemu sama Myesha dan Jovian minggu berikutnya, dia share pengalamannya. Mereka ketawa tentang karnaval lentera, tapi point Devan serius. Bubble sort sempurna untuk dataset kecil, untuk data hampir terurut, untuk tujuan pendidikan, dan untuk situasi di mana memory space terbatas. Itu algoritma in-place, hanya butuh ruang ekstra O(1). Itu stabil, meaning elemen-elemen equal mempertahankan urutan relatifnya. Properti-properti ini membuatnya berharga dalam konteks spesifik, meskipun bukan tool pilihan untuk mengurutkan jutaan record.

## Epilog: Algoritma di Kode

Bulan kemudian, Devan menemukan dirinya debugging sistem lawas di tempat kerja. Sistem itu menggunakan fungsi pengurutan sederhana yang menyebabkan masalah performa dengan dataset besar. Rekan kerjanya menyarankan menggantinya dengan algoritma yang lebih efisien kayak quicksort atau mergesort. Tapi Devan ingat lapangan lentera, tengah malam, dan gentle bubble sort yang sudah menyelamatkan karnaval.

Dia investigasi dan menemukan bahwa data yang diurutkan biasanya kecil (kurang dari lima puluh elemen) dan hampir terurut oleh user behavior. Dalam konteks ini, bubble sort dengan early termination actually lebih cepat dari algoritma yang lebih kompleks karena overhead-nya yang rendah. Solusinya bukan mengganti algoritma—tapi mengaplikasikan optimasi yang tepat untuk konteks yang tepat.

```python
# Python's built-in sorted() menggunakan Timsort - algoritma hybrid
# Tapi memahami bubble sort membantu kamu tau kapan yang sederhana lebih baik

# Takeaway: setiap algoritma punya tempatnya
# Bubble sort untuk pendidikan, data kecil, data hampir terurut
# Quick sort untuk dataset besar
# Merge sort untuk pengurutan stabil dan paralel
# Timsort (default Python) untuk pola data dunia nyata
```

Kode itu akhirnya dioptimasi, tapi optimasinya bukan yang orang expect. Itu pemahaman lebih deep tentang konteks masalah, seperti yang Pak Rahman ajarin. Trick terbesar yang bisa dimainkan algoritma adalah tau kapan harus dipakai. Bubble sort bukan mati—dia menunggu momennya, menggelembung tepat di bawah permukaan, siap naik ketika waktunya tepat.