---
layout: post
title: "Membangun TCP/IP Stack dari Nol: Menyelami Ethernet dan ARP dengan Python"
subtitle: "Belajar jaringan komputer sambil bernostalgia dan menguatkan ikatan persaudaraan di bawah rintik hujan Sleman."
date: 2026-07-18 19:00:00 +0700
categories: [Networking, Python]
tags: [tcp-ip, ethernet, arp, python, tutorial, kehidupan]
---

**Bab 1: Hujan Deras di Sleman dan Sebuah Tantangan**

Hujan menderas mengguyur kawasan Sleman malam ini. Rintiknya yang berjatuhan di atas atap genteng menciptakan simfoni alam yang ritmis, sebuah nyanyian pengantar tidur bagi sebagian orang, namun menjadi teman begadang bagi mereka yang sedang bergelut dengan baris-baris kode. Di sudut ruang tengah yang hangat oleh cahaya lampu kuning keemasan, Devan tampak duduk membungkuk di depan layar laptopnya. Wajahnya berkerut, matanya menatap tajam ke arah deretan teks di editor kode. Jari-jemarinya yang biasanya lincah menari di atas keyboard kini tampak kaku. Ia menghela napas panjang, sebuah helaan yang sarat akan rasa frustrasi dan kelelahan. Di layarnya terpampang sebuah artikel panjang berbahasa Inggris tentang cara membangun TCP/IP stack menggunakan bahasa C. Konsep tentang pointer, *memory allocation*, dan *struct* yang rumit seolah membuat kepalanya berputar.

"Susah banget sih ini," gumam Devan pelan, setengah berbisik pada dirinya sendiri. Tangannya mengacak-acak rambutnya yang sudah mulai gondrong. Ia merasa seperti sedang mendaki gunung yang terlalu tinggi tanpa persiapan yang matang. Di tengah rasa putus asanya, aroma harum pisang goreng tiba-tiba menyelinap masuk ke rongga hidungnya.

Dari arah dapur, muncul Myesha, sang kakak perempuan yang selalu menjadi sosok pelindung dan penenang di rumah itu. Myesha membawa sebuah nampan berisi sepiring pisang goreng panas dan dua cangkir teh manis yang uapnya masih mengepul. Ia meletakkan nampan itu perlahan di atas meja kecil di samping Devan.

"Kenapa, Bang? Kok mukanya ditekuk gitu kayak baju belum disetrika?" sapa Myesha dengan nada lembut namun terselip sedikit candaan yang khas. Ia menarik kursi kayu dan duduk di sebelah adiknya, ikut menatap layar laptop yang penuh dengan kode-kode berwarna-warni.

Devan menoleh, tatapannya menyiratkan rasa lelah yang mendalam. "Ini lho, Kak. Aku lagi nyoba belajar gimana sebenarnya jaringan komputer itu bekerja dari dasar banget. Maksudnya, selama ini kan kalau kita bikin aplikasi, kita tinggal pakai library *socket* atau HTTP *client*, terus semua data ajaib aja gitu bisa nyampe ke *server*. Aku pengen tahu rahasia di baliknya. Aku nemu tutorial bagus dari Saminiir tentang bikin TCP/IP stack pakai C, tapi... sintaks C ini bikin pusing, Kak. Aku nggak terlalu terbiasa mainan pointer tingkat rendah begini."

Myesha tersenyum simpul. Tangannya yang hangat menepuk pelan bahu Devan. Sentuhan seorang kakak yang selalu berhasil meruntuhkan dinding kecemasan di hati adik-adiknya. "Bang, ingat nggak waktu kita masih kecil dulu pas lagi liburan di Takengon? Waktu itu Abang nyoba benerin radio tua punya Papah yang rusak. Abang nangis gara-gara kabelnya rumit banget dan Abang nggak ngerti harus nyambungin yang mana. Tapi ujung-ujungnya, setelah dipelajari pelan-pelan tanpa panik, Abang berhasil kan bikin radionya bunyi lagi?"

Devan tertunduk, senyum kecil mulai menghiasi bibirnya mengingat kenangan masa kecil di dataran tinggi Gayo itu. Udara sejuk Takengon selalu membawa ketenangan. 

"Belajar sesuatu yang mendasar memang selalu terasa seperti merakit radio tua, Bang. Kalau bahasa C bikin Abang pusing karena *memory management*-nya, kenapa kita nggak coba pakai bahasa yang Abang lebih kuasai? Pakai Python, misalnya?" usul Myesha dengan mata berbinar.

"Python? Emang bisa ya, Kak, mainan *low-level networking* pakai Python?" tanya Devan, setengah tidak percaya namun ada percik harapan di nada suaranya.

"Tentu saja bisa! Konsep jaringannya kan sama, mau pakai C atau Python. Yang penting itu logika dan pemahaman protokolnya. Python punya modul bawaan seperti `struct` dan *file descriptor* yang cukup buat ngakses alat virtual di Linux," jelas Myesha sabar. 

Tiba-tiba, dari arah kamar tidur, muncul sesosok anak laki-laki dengan mata yang masih setengah mengantuk. Jovian, adik bungsu mereka, berjalan gontai sambil membawa selimutnya. "Ada apa sih ini malem-malam ribut-ribut... Wah! Pisang goreng!" Matanya langsung melek begitu melihat piring di atas meja. Jovian dengan sigap mengambil satu potong dan mengunyahnya dengan lahap.

"Ini nih, Abang Devan lagi pusing belajar jaringan komputer," kata Myesha sambil mengelus rambut Jovian yang berantakan. "Tapi tenang, malam ini kita bakal bedah bareng-bareng. Kita mulai dari bawah, dari Ethernet dan ARP."

Hujan di luar sana seolah memberikan restunya. Suara rintiknya menjadi *backsound* yang sempurna. Di ruangan yang hangat itu, tiga bersaudara ini bersiap untuk memulai sebuah petualangan intelektual. Devan merasa energi baru mengalir di nadinya. Ia menghapus layar terminalnya, membuka file Python baru yang masih kosong. Malam ini, ia tidak lagi merasa berjuang sendirian. Ada Kak Myesha yang siap membimbingnya, dan ada Dik Jovian yang siap meramaikan suasana (dan menghabiskan pisang goreng). Mari kita mulai petualangan membangun fondasi komunikasi digital ini.


**Bab 2: Membuka Gerbang dengan TUN/TAP Device**

Langkah pertama dalam perjalanan panjang memahami *networking stack* adalah menemukan cara untuk mencegat atau menangkap lalu lintas jaringan secara langsung dari sistem operasi. Myesha mengambil secarik kertas dan pulpen, mulai menggambar sebuah diagram sederhana untuk Devan dan Jovian.

"Jadi begini, Bang, Dik," Myesha mulai menjelaskan dengan intonasi layaknya seorang guru yang sedang bercerita. "Kalau kita mau bikin protokol jaringan sendiri di level aplikasi (userspace), kita butuh 'pintu' atau gerbang ajaib yang menghubungkan program kita dengan jaringan yang sebenarnya di sistem operasi Linux atau MacOS. Nah, pintu ini namanya TUN atau TAP device."

Jovian yang sedang asyik mengunyah mengernyitkan dahi. "TUN? TAP? Kayak suara air keran bocor aja, Kak. Tap... tap... tap..." kelakarnya.

Myesha tertawa renyah. "Bisa dibilang begitu, Dik! TAP itu ibarat keran yang mengalirkan data mentah. Secara teknis, TAP beroperasi di Layer 2 (Data Link Layer), yang artinya data yang mengalir dari keran itu masih berupa *frame* Ethernet utuh lengkap dengan informasi alamat fisiknya (MAC Address). Kalau TUN, dia beroperasi di Layer 3 (Network Layer), jadi data yang keluar adalah paket IP. Karena kita mau membangun dari fondasi paling bawah, yaitu Ethernet, kita harus pakai TAP."

Devan mengangguk paham. "Berarti, tugas pertama kita di Python adalah membuat atau membuka *device* TAP ini, kan? Kalau di C tutorial ini, dia pakai `open("/dev/net/tap", O_RDWR)` terus dilanjut pakai perintah `ioctl`. Di Python gimana caranya, Kak?"

"Tepat sekali, Bang!" seru Myesha bangga. "Di Python, kita bisa menggunakan modul `os` untuk membuka file *device* dan modul `fcntl` untuk melakukan perintah `ioctl`. *Ioctl* (Input/Output Control) itu ibarat panel kendali rahasia di mana kita bisa menyetel konfigurasi keran TAP kita tadi."

Devan segera memosisikan jari-jarinya di atas keyboard dan mulai mengetik dengan panduan Myesha.

```python path=null start=null
import os
import fcntl
import struct

# Konstanta ajaib dari kernel Linux
TUNSETIFF = 0x400454ca
IFF_TAP = 0x0002
IFF_NO_PI = 0x1000

def tun_alloc(dev_name='tap0'):
    # Membuka gerbang utama ke TUN/TAP device
    fd = os.open('/dev/net/tap', os.O_RDWR)
    
    # Kita perlu membuat struktur data C (ifreq) menggunakan modul struct.
    # Struktur ini butuh nama device (16 bytes) dan flag (2 bytes).
    # IFF_NO_PI sangat penting agar kernel tidak menambahkan ekstra informasi
    # di depan frame Ethernet kita.
    ifr = struct.pack('16sH', dev_name.encode('utf-8'), IFF_TAP | IFF_NO_PI)
    
    # Memanggil ioctl untuk mendaftarkan interface kita
    ifr = fcntl.ioctl(fd, TUNSETIFF, ifr)
    
    # Mengambil nama device yang sebenarnya terdaftar
    real_dev_name = ifr[:16].strip(b'\x00').decode('utf-8')
    print(f"Berhasil membuka antarmuka jaringan: {real_dev_name}")
    
    return fd, real_dev_name

# Tes jalankan
if __name__ == '__main__':
    fd, nama_tap = tun_alloc('tap0')
```

Devan menjalankan kode tersebut (perlu akses `sudo` di Linux), dan teks `Berhasil membuka antarmuka jaringan: tap0` muncul di layar terminal. Matanya terbelalak kegirangan. "Wah! Berhasil, Kak! Gila, ternyata di Python jauh lebih ringkas ya. Enggak perlu repot inisialisasi *struct* manual kayak di C!"

Jovian menunjuk ke arah baris `TUNSETIFF = 0x400454ca`. "Kak, angka `0x400454ca` itu apa? Kok kayak mantra dukun gitu?"

"Itu namanya *magic number*, Dik," jawab Myesha tersenyum. "Di dalam sistem operasi Linux, setiap perintah kendali untuk perangkat keras punya kode unik tersendiri. Angka itu sudah disepakati oleh pembuat Linux. Anggap saja itu nomor pin brankas untuk membuka pintu TAP kita."

Hati Devan yang sebelumnya diselimuti awan mendung kini mulai cerah. Pemahamannya mulai terbentuk. Ia menyadari bahwa di balik keajaiban koneksi internet yang ia gunakan setiap hari, terdapat komponen-komponen kecil yang saling bekerja sama, ibarat organ-organ di dalam tubuh manusia. Ia sudah berhasil membuat "keran" datanya. Langkah selanjutnya adalah melihat air apa yang mengalir dari keran tersebut.


**Bab 3: Anatomi Sebuah Frame Ethernet**

Setelah *file descriptor* (`fd`) untuk perangkat TAP berhasil dibuat, Devan memiliki akses untuk membaca dan menulis data mentah ke jaringan. Namun, data yang mengalir dari TAP bukanlah teks biasa. Ia adalah sekumpulan bait (*bytes*) biner yang terlihat seperti karakter-karakter aneh jika dicetak langsung ke layar.

Myesha mengambil selembar kertas baru. Ia menggambar sebuah kotak panjang persegi panjang dan membaginya menjadi beberapa sekat.

"Sekarang, mari kita bedah anatomi dari sebuah *Frame Ethernet*, Bang. Ketika sebuah komputer mengirim data di jaringan lokal (LAN), data tersebut dibungkus di dalam sebuah amplop yang kita sebut Frame Ethernet. Amplop ini sangat penting."

Myesha menulis angka-angka di atas sekat yang ia gambar.
"Sekat pertama, ukurannya 6 *byte*. Ini adalah **Destination MAC Address** (Alamat MAC Tujuan).
Sekat kedua, ukurannya juga 6 *byte*. Ini adalah **Source MAC Address** (Alamat MAC Pengirim).
Sekat ketiga, ukurannya 2 *byte*. Ini adalah **EtherType**.
Sisanya, adalah isi suratnya atau yang disebut **Payload**."

Jovian menggaruk kepalanya. "MAC Address itu apa sih, Kak? Alamat rumah ya?"

"Benar banget, Dik Jovian yang pintar!" Myesha mencubit pipi adiknya pelan. "Adik ingat nggak waktu kita mudik ke rumah kakek di Krui, Pesisir Barat? Waktu itu kita mau kirim bingkisan buat kerabat di kampung sebelah. Kalau kita cuma nulis nama 'Pak Tono' di paketnya, tukang pos pasti bingung karena yang namanya Tono itu banyak. Kita harus nulis alamat fisiknya yang jelas dan permanen: Jalan Nelayan No. 4, Krui. Nah, MAC Address itu adalah 'alamat fisik' yang tertanam permanen di dalam kartu jaringan komputer atau HP kita. Setiap perangkat di dunia punya MAC Address yang unik dan berbeda-beda."

"Oh, jadi biar paketnya nggak nyasar ke komputer tetangga ya?" tanya Jovian lagi.

"Betul sekali. Lalu, bagian **EtherType** itu ibarat cap pos yang ngasih tahu apa isi surat di dalam amplop ini. Apakah ini surat tentang IP (Internet Protocol), atau surat tentang ARP (Address Resolution Protocol). Dari angka 2 *byte* ini, program kita nanti bakal tahu cara membaca isi pesannya."

Devan langsung paham dengan analogi tersebut. "Berarti total *header* amplop ini ukurannya adalah 6 + 6 + 2 = 14 byte ya, Kak? Kalau begitu, untuk membaca *header* ini di Python, kita bisa potong 14 byte pertama dari data yang masuk, lalu kita *unpack* pakai `struct`."

Myesha mengangguk antusias. "Betul! Coba Abang tulis kodenya. Hati-hati dengan urutan bit-nya (*endianness*). Jaringan selalu menggunakan format *Big-Endian*, jadi di format `struct` Python, Abang harus pakai tanda seru `!` di depannya."

Devan segera memodifikasi *script*-nya. Ia menambahkan fungsi untuk memecah data *header* Ethernet.

```python path=null start=null
def format_mac_address(mac_bytes):
    # Mengubah format byte menjadi string MAC Address yang mudah dibaca,
    # misalnya: aa:bb:cc:dd:ee:ff
    return ':'.join(f'{b:02x}' for b in mac_bytes)

def parse_ethernet_frame(data):
    # Header Ethernet ukurannya pasti 14 byte
    eth_length = 14
    
    # Mengambil 14 byte pertama dari data
    eth_header = data[:eth_length]
    
    # Kita menggunakan struct.unpack untuk membedah data binernya.
    # '!' menandakan jaringan menggunakan format Big-Endian.
    # '6s' berarti 6 byte string (untuk MAC tujuan)
    # '6s' berarti 6 byte string (untuk MAC pengirim)
    # 'H' berarti unsigned short integer ukuran 2 byte (untuk EtherType)
    unpacked_data = struct.unpack('!6s6sH', eth_header)
    
    dmac_bytes = unpacked_data[0]
    smac_bytes = unpacked_data[1]
    ethertype = unpacked_data[2]
    
    # Format agar rapi
    dmac = format_mac_address(dmac_bytes)
    smac = format_mac_address(smac_bytes)
    
    # Sisanya adalah isi surat sebenarnya (payload)
    payload = data[eth_length:]
    
    return dmac, smac, ethertype, payload
```

"Wah, indah sekali kodenya," puji Myesha. "Di sini Abang bisa lihat betapa kuatnya Python. Fungsi `struct.unpack('!6s6sH', ...)` ini benar-benar nyawa dari proses *parsing*. Bayangkan kalau kita harus menghitung bit-nya satu per satu. Dengan cara ini, kita sudah punya alamat pengirim, penerima, dan tipe pesannya dalam sekejap."

Devan tersenyum lega. Rasa stresnya berangsur-angsur menghilang berganti dengan rasa penasaran yang menggebu-gebu. Ia merasa seperti seorang detektif yang baru saja menemukan kunci sandi rahasia untuk membaca pesan-pesan tersembunyi yang bertebangan di udara.


**Bab 4: Membongkar Paket (Ethernet Parsing) di Python**

Malam semakin larut. Rintik hujan di Sleman perlahan mulai mereda, menyisakan hawa dingin yang menusuk tulang. Namun, kehangatan di ruang tengah keluarga ini justru semakin menebal. Jovian yang tadinya semangat makan pisang goreng kini mulai merapat ke sofa, membungkus tubuhnya rapat-rapat dengan selimut sambil sesekali menguap, namun matanya tetap tertuju pada layar laptop sang kakak.

"Oke, kita sudah punya keran airnya (TAP), dan kita juga sudah punya saringan airnya (fungsi `parse_ethernet_frame`). Sekarang, gimana caranya kita ngalirin airnya terus-terusan dan lihat apa aja yang lewat?" tanya Devan, memecah kesunyian.

Myesha mengambil cangkir tehnya, menyesapnya perlahan sebelum menjawab. "Sederhana, Bang. Kita buat sebuah perulangan tanpa henti (*infinite loop*). Di dalam perulangan itu, kita suruh sistem untuk terus membaca data dari *file descriptor* TAP yang sudah kita buka tadi. Setiap kali ada paket lewat, kita tangkap, kita *parse*, lalu kita cetak isinya ke layar."

Devan segera mengetik blok kode utama. Ia menggunakan metode `os.read(fd, buffer_size)` untuk menarik data dari jaringan.

```python path=null start=null
# Melanjutkan dari script sebelumnya...

def main():
    # 1. Buka device TAP
    fd, tap_name = tun_alloc('tap0')
    print(f"Mulai mendengarkan lalu lintas di {tap_name}...\n")
    
    try:
        # 2. Perulangan tanpa akhir untuk mendengarkan paket
        while True:
            # Membaca paket dari TAP (ukuran buffer 65535 byte)
            raw_data = os.read(fd, 65535)
            
            # Jika ada data yang masuk, kita parse
            if raw_data:
                dmac, smac, ethertype, payload = parse_ethernet_frame(raw_data)
                
                # Kita ubah ethertype menjadi nilai hex agar lebih gampang dikenali
                ethertype_hex = hex(ethertype)
                
                print(f"[ETHERNET] Pengirim: {smac} -> Tujuan: {dmac} | Tipe: {ethertype_hex} | Panjang: {len(raw_data)} bytes")
                
    except KeyboardInterrupt:
        print("\nSelesai mendengarkan. Menutup koneksi.")
        os.close(fd)

if __name__ == '__main__':
    main()
```

"Nah, coba Abang jalankan *script*-nya sekarang," instruksi Myesha.

Devan menjalankan `sudo python main.py`. Terminalnya seketika menampilkan teks bahwa program sedang mendengarkan lalu lintas. Tetapi, layarnya diam. Tidak ada paket yang lewat.

"Kok sepi, Kak?" tanya Devan heran.

"Coba buka terminal satu lagi, Bang. Terus coba kasih perintah `ping` ke alamat IP sembarang, atau coba Abang ping interface `tap0` milik Abang sendiri. Saat sistem operasi mencoba mengirim sesuatu lewat antarmuka TAP, program Python kita pasti akan menangkapnya," jelas Myesha.

Di terminal baru, Devan mengetikkan `ping 10.0.0.2`. Seketika, di terminal Python-nya, teks berhamburan dengan cepat!

```text
[ETHERNET] Pengirim: c2:a4:11:22:33:44 -> Tujuan: ff:ff:ff:ff:ff:ff | Tipe: 0x806 | Panjang: 42 bytes
[ETHERNET] Pengirim: c2:a4:11:22:33:44 -> Tujuan: ff:ff:ff:ff:ff:ff | Tipe: 0x806 | Panjang: 42 bytes
[ETHERNET] Pengirim: c2:a4:11:22:33:44 -> Tujuan: ff:ff:ff:ff:ff:ff | Tipe: 0x806 | Panjang: 42 bytes
```

"Wahhhh! Nangkap, Kak! Gila, keren banget!" Devan nyaris melompat dari kursinya saking senangnya. Matanya berbinar menatap baris-baris log yang muncul. Rasa lelahnya sirna sepenuhnya.

"Lihat alamat tujuannya, Bang," Myesha menunjuk ke layar dengan jarinya yang lentik. "`ff:ff:ff:ff:ff:ff` itu namanya MAC Address *Broadcast*. Artinya, komputer Abang lagi teriak-teriak ke semua orang di jaringan lokal. Terus, lihat tipe pesannya: `0x806`. Abang tahu itu artinya apa?"

Devan mengernyitkan alis, mencoba mengingat-ingat kembali bacaannya. "Kalau dari tutorial tadi... ah! `0x0806` itu adalah kode untuk tipe ARP (Address Resolution Protocol), kan?"

"Tepat sekali 100 nilai untuk Abang!" balas Myesha. "Karena komputer Abang mau nge-ping `10.0.0.2`, dia tahu alamat IP-nya, tapi dia nggak tahu alamat MAC fisiknya. Makanya, dia ngirim paket ARP *broadcast*, yang teriak 'Eh, tolong dong! Siapa pun yang punya IP 10.0.0.2, kasih tahu aku apa MAC Address kamu!'. Ini adalah konsep inti dari jaringan lokal, Bang."

Jovian yang mengantuk pun ikut tersenyum melihat kehebohan abangnya. "Berarti kayak Om Budi yang dulu pas di Berbah nyariin alamat rumah tetangga baru pake toa masjid ya, Kak? Tanya ke semua warga biar dikasih tahu letaknya di mana."

"Persis banget, Dik!" tawa Myesha pecah. Analogi yang sangat membumi dari seorang anak kecil. Terkadang konsep teknologi tingkat tinggi sebenarnya meniru cara komunikasi manusia sehari-hari. Sangat manusiawi dan sederhana jika dipahami maknanya. Devan kini menyadari bahwa baris-baris kode biner yang menakutkan itu pada hakikatnya hanyalah bentuk terjemahan digital dari sifat dasar makhluk sosial yang saling mencari dan menyapa.


**Bab 5: Address Resolution Protocol (ARP) - Si Pencari Alamat**

Kini mereka telah mencapai gerbang terakhir dari petualangan malam itu. Mereka berhasil menangkap paket, membedah bungkus luarnya (Ethernet), dan mengidentifikasi bahwa paket di dalamnya adalah paket pencari alamat alias ARP. Tugas terakhir adalah membongkar isi dari surat ARP tersebut agar mereka bisa membaca detail pertanyaannya.

"Myesha, aku paham sekarang," kata Devan penuh percaya diri. "Kalau tipe paketnya adalah `0x0806`, berarti isi `payload` yang kita tangkap tadi bukanlah data sembarangan, melainkan sebuah struktur ARP. Aku ingat formatnya dari dokumentasi."

Myesha mengangguk, mempersilakan adiknya untuk merangkai kode berikutnya. "Lanjutkan, Bang. Bedah isi dari struktur ARP-nya."

Devan merenung sejenak, mengingat dokumentasi yang tadi membuat kepalanya pusing saat ditulis dalam bahasa C. Di dalam paket ARP untuk protokol IPv4, terdapat beberapa field penting: tipe *hardware* (2 byte), tipe protokol (2 byte), ukuran *hardware* (1 byte), ukuran protokol (1 byte), *opcode* atau jenis operasi (2 byte). Setelah itu, barulah diikuti oleh data utama: MAC pengirim (6 byte), IP pengirim (4 byte), MAC target (6 byte), dan IP target (4 byte).

"Panjang banget ya format *struct*-nya," gumam Devan. "Berarti format `struct.unpack`-nya bakal panjang nih. Kita coba susun: `!HHBBH6s4s6s4s`. Bener nggak, Kak?"

"Sempurna," puji Myesha tersenyum lembut. "Jangan lupa, alamat IP yang bentuknya 4 byte biner itu harus diubah menjadi format angka titik (desimal beritik) seperti `192.168.1.1` biar gampang dibaca. Abang bisa pakai library `socket.inet_ntoa` bawaan Python."

Jari-jemari Devan kembali menari dengan kecepatan penuh. Kini ia tidak lagi kebingungan. Pikirannya sudah jernih. Logikanya mengalir selaras dengan struktur data jaringan.

```python path=null start=null
import socket

# ... fungsi sebelumnya ...

def parse_arp_packet(payload):
    # Struktur ARP untuk IPv4 berukuran 28 byte
    # H: unsigned short (2 bytes)
    # B: unsigned char (1 byte)
    # 6s: string 6 byte (MAC)
    # 4s: string 4 byte (IP)
    arp_header = payload[:28]
    
    arp_data = struct.unpack('!HHBBH6s4s6s4s', arp_header)
    
    hw_type = arp_data[0]
    pro_type = arp_data[1]
    hw_size = arp_data[2]
    pro_size = arp_data[3]
    opcode = arp_data[4] # 1 untuk Request, 2 untuk Reply
    
    smac = format_mac_address(arp_data[5])
    # Mengubah 4 byte biner IP ke string
    sip = socket.inet_ntoa(arp_data[6]) 
    
    dmac = format_mac_address(arp_data[7])
    dip = socket.inet_ntoa(arp_data[8])
    
    return opcode, smac, sip, dmac, dip

# Update perulangan utama kita di fungsi main()
def main():
    fd, tap_name = tun_alloc('tap0')
    print(f"Mulai mendengarkan lalu lintas di {tap_name}...\n")
    
    try:
        while True:
            raw_data = os.read(fd, 65535)
            if raw_data:
                dmac, smac, ethertype, payload = parse_ethernet_frame(raw_data)
                
                # Jika ethertype adalah 0x0806, berarti ini adalah paket ARP
                if ethertype == 0x0806:
                    opcode, arp_smac, arp_sip, arp_dmac, arp_dip = parse_arp_packet(payload)
                    
                    if opcode == 1:
                        operasi = "REQUEST"
                    elif opcode == 2:
                        operasi = "REPLY"
                    else:
                        operasi = f"UNKNOWN ({opcode})"
                        
                    print("--------------------------------------------------")
                    print(f"[*] TERDETEKSI PAKET ARP {operasi}")
                    print(f"    Siapa yang punya IP {arp_dip} ?")
                    print(f"    Tolong beritahu {arp_sip} (di MAC: {arp_smac})")
                    print("--------------------------------------------------")
                    
    except KeyboardInterrupt:
        print("\nSelesai mendengarkan. Menutup koneksi.")
        os.close(fd)

if __name__ == '__main__':
    main()
```

Begitu Devan mengeksekusi *script* finalnya dan kembali menjalankan perintah `ping 10.0.0.2` dari terminal lain, output yang sangat indah dan manusiawi tampil di layarnya:

```text
--------------------------------------------------
[*] TERDETEKSI PAKET ARP REQUEST
    Siapa yang punya IP 10.0.0.2 ?
    Tolong beritahu 10.0.0.1 (di MAC: c2:a4:11:22:33:44)
--------------------------------------------------
```

Sebuah helaan napas panjang keluar dari mulut Devan. Bukan lagi helaan keputusasaan, melainkan helaan kepuasan tiada tara. Perasaan luar biasa ketika deretan misteri dari tumpukan biner akhirnya bisa terbaca dan memiliki arti.

Jovian bertepuk tangan pelan dari atas sofa. "Wah, Abang keren! Komputernya nanya bahasa manusia sekarang!" 

Myesha bersandar pada sandaran kursi kayu, menatap adiknya dengan tatapan bangga yang tak terlukiskan. Hujan di luar benar-benar telah berhenti, menyisakan kesunyian malam Sleman yang syahdu dan damai. Udara dingin yang menyelinap masuk dari sela-sela jendela tak lagi terasa menusuk, terkalahkan oleh kehangatan ikatan batin ketiga bersaudara itu.

"Abang Devan baru saja menyelesaikan langkah paling sulit dalam memahami inti dari jaringan," ucap Myesha pelan. "Banyak orang cuma tahu pakai library tingkat atas, tapi mereka buta akan apa yang terjadi di fondasinya. Dengan mengerti bahwa setiap paket dikemas dalam Ethernet, dan setiap IP butuh diterjemahkan menjadi MAC lewat ARP, Abang sudah menancapkan tiang pancang ilmu *networking* yang sangat kuat. Besok-besok kalau Abang belajar hal lain, semuanya bakal terasa lebih masuk akal."

"Makasih banyak ya, Kak Myesha," balas Devan dengan senyum tulus. "Ternyata kalau dipelajari pelan-pelan pakai perumpamaan, apalagi pakai Python yang *syntax*-nya lebih ramah ketimbang C, semuanya jadi masuk akal. Nggak menakutkan kayak di tutorial tadi."

Myesha mengangguk mengiyakan. Ia berdiri dan perlahan mengambil piring pisang goreng yang sudah ludes tak bersisa, lalu mematikan lampu tengah agar tidak terlalu menyilaukan. 

Jovian sudah meringkuk manis di sofa, napasnya teratur, tenggelam dalam bunga tidurnya. Mungkin di dalam mimpinya, ia sedang bermain menjadi tukang pos pembawa surat berformat MAC Address di pedesaan Pante Raya. 

Malam ini, di sebuah sudut kota Sleman, sejarah kecil tercipta di balik layar laptop Devan. Membangun sesuatu dari nol selalu menakutkan di awal. Namun, dengan keberanian untuk membongkar kerumitan menjadi bagian-bagian kecil, dan dukungan dari orang-orang tersayang, hal-hal yang tampaknya mustahil selalu bisa diurai. Pada akhirnya, baik itu protokol jaringan TCP/IP maupun hubungan antarmanusia, semuanya berpusat pada satu hal yang sama: bagaimana kita bisa terhubung dan saling mengerti satu sama lain.
