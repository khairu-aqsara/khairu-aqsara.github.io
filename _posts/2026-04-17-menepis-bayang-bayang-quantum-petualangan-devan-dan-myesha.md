---
title: "Menepis Bayang-Bayang Quantum: Petualangan Devan dan Myesha di Labirin Kriptografi Masa Depan"
subtitle: "Belajar Post-Quantum Cryptography (PQC) sambil ngopi santai di Sleman"
date: 2026-04-17
categories: [Security, Cryptography]
tags: [PQC, Quantum Computing, Security, Tech Tale]
---

## Bab 1: Mendung di Sleman dan Ancaman yang Tak Terlihat

Sore itu, Sleman lagi agak sendu. Langit di atas Merapi ketutup mendung tipis, tapi udara di teras rumah masih kerasa gerah. Devan lagi asik nyeruput kopi jos-nya, matanya nggak lepas dari layar laptop yang penuh dengan barisan kode C++. Di sebelahnya, Myesha—kakaknya yang paling kritis soal urusan sekuriti—lagi baca-baca jurnal terbaru dari NIST.

"Van," celetuk Myesha tiba-tiba, bikin Devan hampir kesedak ampas kopi.

"Oit, nape Kak?" sahut Devan sambil ngelap bibirnya.

"Lu tau nggak sih, kalau algoritma RSA sama ECC yang kita bangga-banggain buat enkripsi NVR rakitan kita kemarin itu... sebenernya lagi di ujung tanduk?"

Devan ngerutin dahi. "Ujung tanduk gimana? Kan masih standar industri, Mes. AES-256, RSA-4096. Aman lah buat sepuluh-dua puluh tahun kedepan."

Myesha ngegeleng pelan. "Itu kalau kita ngomongin komputer klasik, Bang. Tapi masalahnya, perkembangan komputer kuantum itu cepet banget. Ada yang namanya Algoritma Shor. Kalau komputer kuantum dengan qubit yang cukup gede udah lahir, RSA sama ECC itu bakal pecah dalam hitungan detik. *Poof!* Ilang semua privasi kita."

Devan naruh gelas kopinya. Topik ini emang udah lama dia denger, tapi denger Myesha ngomong dengan nada seserius itu di sore yang tenang di Sleman ini bikin dia ngerasa... ada urgensi yang beda. "Jadi, kita harus gimana? Balik ke zaman tuker pesan pake kurir burung merpati?"

"Ya nggak lah, Van. Makanya ada yang namanya *Post-Quantum Cryptography* atau PQC. Ini bukan kriptografi yang jalan di komputer kuantum, tapi kriptografi klasik—yang jalan di komputer biasa kita—tapi didesain biar tahan banting lawan serangan komputer kuantum."

Devan manggut-manggut. "Oke, Kak. Kayaknya menarik nih buat kita bedah. Mumpung hujan belum turun, ceritain ke gue gimana cara kerjanya."

Myesha tersenyum, lalu mulai ngetik sesuatu di laptopnya. "Gini Dek, intinya kita butuh masalah matematika yang lebih ribet daripada sekadar faktorin bilangan prima gede..."

---

## Bab 2: Labirin Kisi-Kisi (Lattice-based Cryptography)

Myesha mulai jelasin kalau salah satu kandidat terkuat buat PQC itu namanya *Lattice-based Cryptography*. 

"Bayangin gini Van," kata Myesha sambil nunjuk ke ubin teras rumah mereka. "Ubin ini kan kotak-kotak rapi. Ini namanya kisi atau *lattice*. Di kriptografi klasik, kita mainan angka prima. Di *lattice*, kita mainan titik-titik di ruang multi-dimensi yang jumlah dimensinya bisa ribuan."

"Ribuan dimensi?" Devan geleng-geleng. "Ngebayangin tiga dimensi aja udah pusing gue."

"Nah, itu dia poinnya! Masalahnya namanya *Learning With Errors* atau LWE. Kita ngasih soal matematika berupa persamaan linear, tapi kita kasih sedikit 'noise' atau error yang acak. Buat komputer klasik, ini susah. Buat komputer kuantum, ini juga tetep susah karena mereka nggak punya algoritma sejenis Shor buat nyelesain masalah kisi-kisi ini."

Myesha nunjukin contoh kode sederhana dalam Python buat ngebayangin konsep LWE ini.

```python
import numpy as np

# Simulasi sederhana Learning With Errors (LWE)
def simulate_lwe():
    n = 10  # Dimensi rahasia
    q = 127 # Modulo (bilangan prima)
    
    # Kunci rahasia s
    s = np.random.randint(0, q, size=n)
    print(f"Secret Key (s): {s}")
    
    # Sampel acak A (matriks public)
    m = 20 # Jumlah sampel
    A = np.random.randint(0, q, size=(m, n))
    
    # Error/Noise (kecil aja)
    e = np.random.randint(-2, 3, size=m)
    
    # Hasil b = A*s + e (mod q)
    b = (np.dot(A, s) + e) % q
    
    print("\nPublic Key (A, b):")
    print(f"Matriks A (sebagian): \n{A[:2]}")
    print(f"Vektor b: {b}")
    
    # Tanpa tau s, susah banget buat nyari s cuma dari A dan b 
    # karena ada 'e' yang ngerusak polanya.
    return A, b, s

simulate_lwe()
```

"Lo liat kan Bang? Di situ ada variabel `e` alias error. Tanpa `e`, komputer tinggal pake eliminasi Gaussian buat nyari `s`. Tapi gara-gara ada si `e` kecil itu, masalahnya jadi *NP-Hard*. Komputer kuantum pun bakal garuk-garuk kepala."

Devan ngeliatin kodenya dengan serius. "Jadi intinya kita nyembunyiin rahasia di dalam tumpukan persamaan linear yang udah 'dirusak' sedikit ya? Cerdas juga."

---

## Bab 3: Kode-Kode Rahasia dari Masa Lalu (Code-based Cryptography)

Gak lama kemudian, Jovian—adek mereka yang paling bontot—datang bawa sepiring pisang goreng anget. "Lagi bahas apa nih? Serius amat, ampe pisang goreng dicuekin," canda Jovian.

"Lagi bahas PQC, Dek," jawab Myesha. "Lagi jelasin ke Devan soal alternatif RSA."

Jovian duduk, ngambil satu pisang goreng. "Oalah, PQC. Kalian udah bahas McEliece belum? Itu kan barang antik yang sekarang jadi primadona lagi."

Devan noleh. "McEliece? Nama apa itu? Kayak nama merk sereal."

Jovian ketawa. "Itu nama Robert McEliece, yang nemuin kriptosistem berbasis kode koreksi error (*error-correcting codes*) tahun 1978. Bayangin, algoritma dari tahun 70-an, tapi ampe sekarang belum ada yang bisa nembus pake komputer kuantum."

"Kok bisa, Dek?" tanya Devan penasaran.

"Prinsipnya mirip kayak kita ngirim data lewat satelit," jelas Jovian. "Kadang datanya korup di jalan, makanya butuh kode buat benerin error itu, kayak kode Reed-Solomon atau kode Goppa. Nah, McEliece ini pinter. Dia pake kode yang sebenernya gampang dibenerin, tapi dia 'acak-acak' struktur kodenya pake matriks transformasi rahasia. Jadi buat orang luar, itu keliatan kayak kode acak yang susah banget dibenerin error-nya. Tapi buat yang pegang kunci rahasia, mereka bisa benerin error itu dengan gampang."

Jovian ngebuka terminal di HP-nya, nunjukin cuplikan logika dasarnya.

```python
# Pseudo-logic McEliece Encryption
def mceliece_concept():
    # 1. Pilih kode linear G yang bisa benerin error (misal Goppa Code)
    # 2. Rahasiakan G, tapi buat G' = S * G * P
    #    S = Matriks acak yang bisa di-inverse
    #    P = Matriks permutasi acak
    # 3. Public Key adalah G'.
    
    # Enkripsi:
    # m = pesan (vektor biner)
    # e = error acak yang disuntikkan
    # ciphertext c = m*G' + e
    
    # Dekripsi (hanya pemilik kunci rahasia):
    # 1. Hapus P dan S buat dapet kode aslinya
    # 2. Gunakan algoritma dekripsi kode Goppa buat hapus 'e'
    # 3. Dapet deh pesan aslinya 'm'
    pass

print("McEliece: Menyembunyikan struktur kode di balik transformasi acak.")
```

"Kekurangannya cuma satu," tambah Jovian. "Ukuran kunci publiknya gede banget, bisa sampe megabyte. Makanya dulu jarang dipake. Tapi sekarang, memori kan murah, jadi bukan masalah lagi."

---

## Bab 4: Isogeny dan Kurva Elliptic yang Lebih Ribet (Isogeny-based Cryptography)

Hujan mulai rintik-rintik di Berbah, tetangga sebelah Sleman. Suaranya mulai kedengeran di atap seng. Myesha makin semangat. 

"Ada lagi Van, Dek," lanjut Myesha. "Namanya *Isogeny-based Cryptography*. Ini sebenernya pengembangan dari ECC (Elliptic Curve Cryptography) yang kita pake sekarang. Tapi alih-alih cuma mainan titik di satu kurva, kita mainan 'peta' atau hubungan antar banyak kurva elliptic. Namanya *Isogeny*."

Devan nyoba nangkep maksudnya. "Jadi kita pindah-pindah dari satu kurva ke kurva lain gitu?"

"Bener banget! Bayangin kayak main petak umpet di sebuah labirin yang isinya ribuan kurva elliptic yang saling terhubung. Kita tau jalurnya, tapi musuh nggak tau gimana caranya nemuin jalur balik dari kurva A ke kurva B. Masalahnya namanya *Supersingular Isogeny Diffie-Hellman* (SIDH), meskipun baru-baru ini ada serangan yang bikin SIDH harus direvisi, tapi konsep dasarnya tetep jadi riset penting di PQC."

Myesha ngetik lagi, kali ini dia nyoba nunjukin gimana ribetnya struktur datanya kalau diimplementasiin.

```javascript
// Ilustrasi konseptual Isogeny-based Key Exchange
const isogenyExchange = () => {
    console.log("Memulai Pertukaran Kunci Berbasis Isogeny...");
    
    // Alice memilih kurva awal E_0 dan melakukan 'random walk' 
    // lewat isogeny phi_A menuju kurva E_A
    let aliceSecretPath = "jalur_rahasia_alice_lewat_isogeny";
    let alicePublicKey = "Kurva_E_A";
    
    // Bob melakukan hal yang sama menuju kurva E_B
    let bobSecretPath = "jalur_rahasia_bob_lewat_isogeny";
    let bobPublicKey = "Kurva_E_B";
    
    // Alice menerima E_B, lalu lewat jalur rahasianya sendiri 
    // dia sampai ke kurva E_AB
    // Bob menerima E_A, lalu lewat jalur rahasianya dapet kurva E_BA
    
    // Teorema matematika menjamin E_AB == E_BA (kurva yang isomorfis)
    console.log("Shared Secret: Nilai j-invariant dari kurva hasil pertemuan.");
}

isogenyExchange();
```

"Yang keren dari Isogeny ini adalah ukuran kuncinya paling kecil di antara kandidat PQC lain. Jadi cocok banget buat perangkat IoT atau NVR kita yang memorinya terbatas," tambah Myesha.

---

## Bab 5: Masa Depan di Takengon dan Kesimpulan Kita

Malam makin larut. Kopi udah abis, pisang goreng pun tinggal remah-remahnya. Devan, Myesha, dan Jovian masih asik diskusi. Mereka ngebayangin gimana kalau nanti mereka pulang ke kampung halaman di Takengon, Bener Meriah, atau main ke Krui, dan semua sistem di sana udah pake PQC.

"Intinya Kak, Dek," kata Devan sambil nutup laptopnya. "Dunia sekuriti itu nggak pernah berhenti. Dulu kita pikir RSA itu abadi, ternyata ada komputer kuantum. Besok mungkin ada lagi teknologi baru yang lebih gila."

Devan mengangguk. "Gue jadi sadar, PQC itu bukan cuma soal matematika yang rumit. Ini soal kita, sebagai *kuli kode*, harus selalu satu langkah di depan. Kita nggak boleh nyaman sama apa yang kita punya sekarang."

"Bener banget," sela Myesha. "NIST udah mulai standarisasi beberapa algoritma kayak CRYSTALS-Kyber buat enkripsi dan CRYSTALS-Dilithium buat digital signature. Kita harus mulai belajar cara integrasiin itu ke library-library yang kita pake."

Devan berdiri, ngeregangin badannya. "Oke, besok kita coba pasang Kyber di sistem autentikasi projekan kita. Sekarang, waktunya tidur. Besok pagi kita harus ke Pante Raya ada urusan keluarga kan?"

Myesha dan Jovian ketawa. "Siap!"

Sore di Sleman itu ditutup dengan pemahaman baru. Bahwa di balik ketenangan desa, ada perang digital yang nggak pernah usai, dan mereka siap buat jadi bagian dari barisan pertahanannya.

---

### Contoh Implementasi Sederhana: Menggunakan Library PQC (Simulasi)

Buat kalian yang mau coba, di dunia nyata kita nggak nulis algoritmanya dari nol (bahaya banget kalau ada bug!). Kita pake library yang udah di-audit kayak `liboqs` atau wrapper-nya.

```python
# Simulasi penggunaan Kyber (KEM - Key Encapsulation Mechanism)
# Catatan: Ini adalah pseudo-code yang merepresentasikan library OQS

# import oqs # Gunakan library Open Quantum Safe

def pqc_demo():
    print("--- Simulasi CRYSTALS-Kyber ---")
    
    # 1. Inisialisasi KEM (Key Encapsulation Mechanism)
    # kem = oqs.KeyEncapsulation("Kyber512")
    
    # 2. Alice generate key pair
    # public_key = kem.generate_keypair()
    print("Alice: Generate Public Key (Lattice-based)...")
    
    # 3. Bob dapet public key Alice, lalu buat shared secret
    # ciphertext, shared_secret_bob = kem.encapsulate(public_key)
    print("Bob: Mengenkapsulasi rahasia menggunakan Public Key Alice...")
    
    # 4. Alice terima ciphertext dari Bob, lalu buka pake private key-nya
    # shared_secret_alice = kem.decapsulate(ciphertext)
    print("Alice: Mendekapsulasi ciphertext buat dapet Shared Secret...")
    
    # Sekarang Alice dan Bob punya Shared Secret yang sama 
    # dan AMAN dari komputer kuantum.
    print("Hasil: Shared Secret Alice == Shared Secret Bob")
    print("Koneksi Aman Terjalin!")

pqc_demo()
```

Kriptografi itu kayak kopi jos di Sleman ini, Kak. Kelihatannya item dan biasa aja, tapi pas lo aduk dan lo rasain, ada proses 'pembakaran' ampas yang bikin rasanya unik dan kuat. PQC adalah arang panas yang bakal jagain data kita tetep 'anget' dan aman di masa depan.

Sampai jumpa di artikel berikutnya, tetaplah ngoding dan jangan lupa bahagia!
