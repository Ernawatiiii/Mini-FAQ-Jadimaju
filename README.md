# Qbox AI - Mini FAQ System (Take-Home Test AI Engineer)

Halo! Ini adalah **Qbox AI**, aplikasi web internal yang dibuat khusus untuk membantu tim Customer Service (CS) PT Jadi Maju Digital (Jadimaju). Aplikasi ini berfungsi untuk mengelola, menyaring, dan menjawab pertanyaan customer secara cepat dengan bantuan draf jawaban otomatis dari AI (Gemini).

Proyek ini dibangun untuk memenuhi *Technical Assessment* posisi **AI Engineer** di Jadimaju.

---

## Link Akses & Akun Demo

* **Link GitHub:** https://github.com/Ernawatiiii/Mini-FAQ-Jadimaju
* **Link Live Web (Deployment):** (Aplikasi dijalankan secara lokal di komputer/localhost sesuai panduan Setup di bawah)
* **Akun Login Admin (Untuk Reviewer):**
  * **Halaman Login:** /login
  * **Username:** admin
  * **Password:** jadimaju123

---

## Tech Stack & Alasan Memilihnya

1. **Backend: Flask (Python)**
   * **Alasan:** Flask itu micro-framework yang sangat ringan dan gak ribet. Sangat cocok untuk bikin produk awal (MVP) secara cepat. Karena berbasis Python, integrasi dengan SDK Gemini AI jadi jauh lebih mudah dan lancar.
2. **Database: SQLite**
   * **Alasan:** SQLite sangat praktis karena berbasis file lokal (faq.db), jadi kita gak perlu pusing mikirin setup server database tambahan. Sangat cepat dan pas untuk skala aplikasi internal seperti ini.
3. **Frontend: Tailwind CSS**
   * **Alasan:** Bikin tampilan UI jadi modern, bersih, dan responsif dengan cepat tanpa perlu nulis file CSS terpisah dari nol.
4. **AI SDK: Google GenAI (gemini-2.5-flash)**
   * **Alasan:** Model Gemini 2.5 Flash ini pinter, prosesnya cepat (low latency), dan paling pas buat otomatisasi bikin teks draf jawaban.

---

## Struktur Folder Proyek

```text
mini-faq-jadimaju/
├── app.py                # Kodingan utama backend Flask & logika AI
├── init_db.py            # Skrip buat bikin tabel database di awal
├── faq.db                # File database SQLite (tempat nyimpen data)
├── requirements.txt      # Daftar library Python yang harus di-install
├── .gitignore            # Biar file rahasia gak ikut ke-upload
├── .env                  # Tempat nyimpen API Key Gemini lo
└── templates/            # File tampilan HTML
    ├── index.html        # Halaman depan (Form input buat customer)
    ├── login.html        # Halaman login admin CS
    └── admin.html        # Dashboard utama buat admin mengelola FAQ
