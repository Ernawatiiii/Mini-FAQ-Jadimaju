import sqlite3

def inisialisasi_database():
    koneksi = sqlite3.connect('faq.db')
    cursor = koneksi.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pertanyaan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            email TEXT NOT NULL,
            isi_pertanyaan TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            draft_jawaban_ai TEXT,
            jawaban_admin TEXT,
            tanggal_dibuat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    koneksi.commit()
    koneksi.close()
    print("🚀 Database faq.db dan tabel berhasil dibuat!")

if __name__ == '__main__':
    inisialisasi_database()
