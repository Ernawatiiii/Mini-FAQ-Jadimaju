# Qbox AI - Mini FAQ System (Take-Home Test AI Engineer)

Halo! Ini adalah **Qbox AI**, aplikasi web internal yang dibuat khusus untuk membantu tim Customer Service (CS) PT Jadi Maju Digital (Jadimaju). Aplikasi ini berfungsi untuk mengelola, menyaring, dan menjawab pertanyaan customer secara cepat dengan bantuan draf jawaban otomatis dari AI (Gemini).

Proyek ini dibangun untuk memenuhi *Technical Assessment* posisi **AI Engineer** di Jadimaju.

---

##  Link Akses & Akun Demo

- **Link GitHub:** `https://github.com/Ernawatiiii/Mini-FAQ-Jadimaju`
- **Link Live Web (Deployment):** (Aplikasi dijalankan secara lokal di komputer/localhost sesuai panduan Setup di bawah)
- **Akun Login Admin (Untuk Reviewer):**
  - **Halaman Login:** `/login`
  - **Username:** `admin`
  - **Password:** `jadimaju123`

---

## Tech Stack & Alasan Memilihnya

1. **Backend: Flask (Python)**
   - **Alasan:** Flask itu *micro-framework* yang sangat ringan dan gak ribet. Sangat cocok untuk bikin produk awal (MVP) secara cepat. Karena berbasis Python, integrasi dengan SDK Gemini AI jadi jauh lebih mudah dan lancar.
2. **Database: SQLite**
   - **Alasan:** SQLite sangat praktis karena berbasis file lokal (`faq.db`), jadi kita gak perlu pusing mikirin setup server database tambahan. Sangat cepat dan pas untuk skala aplikasi internal seperti ini.
3. **Frontend: Tailwind CSS**
   - **Alasan:** Bikin tampilan UI jadi modern, bersih, dan responsif dengan cepat tanpa perlu nulis file CSS terpisah dari nol.
4. **AI SDK: Google GenAI (`gemini-2.5-flash`)**
   - **Alasan:** Model Gemini 2.5 Flash ini pinter, prosesnya cepat (low latency), dan paling pas buat otomatisasi bikin teks draf jawaban.

---

##  Struktur Folder Proyek

```text
mini-faq-jadimaju/
│
├── app.py                # Kodingan utama backend Flask & logika AI
├── init_db.py            # Skrip buat bikin tabel database di awal
├── faq.db                # File database SQLite (tempat nyimpen data)
├── requirements.txt      # Daftar library Python yang harus di-install
├── .gitignore            # Biar file rahasia (seperti .env & venv) gak ikut ke-upload
├── .env                  # Tempat nyimpen API Key Gemini nya
└── templates/            # File tampilan HTML
    ├── index.html        # Halaman depan (Form input buat customer)
    ├── login.html        # Halaman login admin CS
    └── admin.html        # Dashboard utama buat admin mengelola FAQ

##Fitur Utama & Cara Kerjanya (app.py)
1. Form Pertanyaan Publik (/ dan /submit)
Customer memasukkan nama, email, dan pertanyaan. Sistem langsung nge-cek di sisi server: kalau ada kolom yang     kosong, data gak bakal kesimpen. Kalau lengkap, langsung masuk database dan muncul notifikasi sukses.

2. Keamanan Halaman Admin (/login dan /logout)
  Halaman dashboard admin (/admin), fungsi menjawab, dan fungsi menghapus data sudah dikunci pakai Session Flask. Kalau ada orang iseng mau buka langsung tanpa login, sistem bakal otomatis nendang mereka kembali ke halaman login.

3. Pencarian & Filter Dinamis di Dashboard
  Admin bisa mencari pertanyaan berdasarkan nama/email/isi teks, sekaligus memfilternya berdasarkan status (apakah "Sudah Dijawab" atau "Belum"). Semuanya diproses lewat kueri SQL (WHERE 1=1 dan LIKE) yang digabung jadi satu fungsi biar efisien.

4. Otomatisasi Draf Jawaban AI (Fitur Bonus)
- Begitu customer kirim pertanyaan, backend Flask langsung manggil API Gemini 2.5 Flash di latar belakang.
- UX Optimization: Prompt AI diatur ketat supaya Gemini ngasih jawaban teks polos (tanpa simbol markdown bintang  atau pagar # yang bikin berantakan) dan membaginya ke dalam paragraf pendek agar nyaman dibaca admin.
- One-Click Template: Di halaman admin ada tombol Use Draft Template berbasis JavaScript. Begitu diklik, draf dari Gemini langsung kesalin otomatis ke kotak jawaban admin. Admin tinggal edit sedikit, lalu klik kirim.

##Cara Menjalankan Proyek di Laptop Lokal
1. Clone repository ini:

   git clone [https://github.com/Ernawatiiii/Mini-FAQ-Jadimaju.git](https://github.com/Ernawatiiii/Mini-FAQ-Jadimaju.git)
   cd Mini-FAQ-Jadimaju

2. Bikin & aktifkan Virtual Environment:

   python3 -m venv venv
   source venv/bin/activate

3. Install semua library:

   pip install -r requirements.txt

4. Setup API Key: Bikin file .env di folder utama, lalu isi:

   GEMINI_API_KEY=isi_api_key_gemini_lo

5. Buat database awal & jalankan web:

   python3 init_db.py
   python3 app.py

- Buka browser di alamat http://127.0.0.1:5000.
##Tantangan & Rencana Pengembangan Ke Depan
**Tantangan yang Berhasil Diselesaikan:
  - Format AI yang Berantakan: Di awal, Gemini sering ngeluarin format markdown tebal (). Ini merusak tampilan kotak text admin. Masalah ini diselesaikan dengan memperketat instruksi (system prompt) agar outputnya wajib teks polos teratur.
Salah Klik Hapus: Biar data gak sengaja kehapus karena admin salah pencet, ditambahkan konfirmasi pop-up "Apakah Anda yakin?" lewat JavaScript pada tombol hapus.
**Ide Pengembangan Masa Depan:
  - Keamanan Password: Mengganti password admin yang masih ditulis manual di kode dengan sistem enkripsi beneran (Bcrypt).
  - Antrean AI (Celery/Redis): Biar loading web pas customer klik kirim gak kerasa lambat saat nungguin respon API Gemini.
