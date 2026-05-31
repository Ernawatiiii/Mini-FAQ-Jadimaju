import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, session
from google import genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = 'super-secret-key-qbox-ai'

client = genai.Client()

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    search_query = request.args.get('search', '').strip()
    conn = get_db_connection()
    
    if search_query:
        daftar_faq = conn.execute(
            'SELECT * FROM faq WHERE email = ? ORDER BY id DESC',
            (search_query,)
        ).fetchall()
    else:
        daftar_faq = []
        
    conn.close()
    return render_template('index.html', daftar_faq=daftar_faq, search_query=search_query)

@app.route('/submit', methods=['POST'])
def submit_pertanyaan():
    nama = request.form['nama']
    email = request.form['email']
    isi_pertanyaan = request.form['isi_pertanyaan']

    if not nama or not email or not isi_pertanyaan:
        flash('Semua kolom wajib diisi!')
        return redirect(url_for('index'))

    # PROMPT PREMIUM: Memaksa Gemini membuat layout pointer yang sangat bersih ke bawah
    prompt_instruksi = (
        "Kamu adalah AI Engineer pembantu admin untuk platform Qbox AI dari PT Jadi Maju Digital.\n"
        "Gunakan informasi profil internal perusahaan kita di bawah ini untuk menjawab:\n"
        "- Nama Perusahaan: PT Jadi Maju Digital (Jadimaju).\n"
        "- Deskripsi: Wadah atau ruang bertumbuh bagi para akademisi dan talent digital.\n"
        "- Produk Utama: Qbox AI, sebuah sistem manajemen FAQ otomatis berbasis kecerdasan buatan.\n\n"
        "TUGAS KAMU:\n"
        "Jawab pertanyaan customer di bawah ini dengan ramah, profesional, dan solutif.\n\n"
        "ATURAN FORMAT JAWABAN (SANGAT KETAT):\n"
        "1. Awali dengan salam pembuka dan 1 paragraf pendek sebagai pengantar.\n"
        "2. Jika memberikan poin-poin strategi/langkah, gunakan penomoran biasa (1., 2., 3.).\n"
        "3. Setiap poin harus ditulis berjarak. Formatnya wajib: Nomor. JUDUL POIN UTAMA (Gunakan Huruf Kapital Untuk Judul Poin Ini).\n"
        "4. Kalimat penjelasan untuk poin tersebut HARUS ditaruh di baris baru di bawah judul poinnya (Gunakan baris baru / enter), TIDAK BOLEH ditulis menyambung ke samping.\n"
        "5. Berikan jarak 2 kali enter (baris kosong) sebelum masuk ke nomor poin berikutnya agar teks tidak menumpuk padat.\n"
        "6. JANGAN gunakan simbol markdown seperti bintang-bintang (** atau *) untuk menebalkan teks karena aplikasi tidak mendukung markdown render.\n"
        "7. Akhiri jawaban dengan kalimat penutup yang menyemangati dan ramah.\n\n"
        f"Pertanyaan Customer: {isi_pertanyaan}"
    )

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt_instruksi,
        )
        draft_ai = response.text.strip() if response.text else "Silakan ketik jawaban manual."
    except Exception as e:
        print(f"Error Gemini: {e}")
        draft_ai = "Maaf, draf otomatis gagal dibuat."

    conn = get_db_connection()
    conn.execute(
        'INSERT INTO faq (nama, email, isi_pertanyaan, draft_jawaban_ai) VALUES (?, ?, ?, ?)',
        (nama, email, isi_pertanyaan, draft_ai)
    )
    conn.commit()
    conn.close()

    flash(f'Pertanyaan berhasil dikirim! Halo {nama}, demi keamanan data, draf jawaban Anda hanya bisa dilihat di bawah ini menggunakan email Anda ({email}). Jangan lupa catat atau ingat email Anda untuk cek validasi resmi admin nanti ya!')
    return redirect(url_for('index', search=email))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'jadimaju123':
            session['logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Username atau password salah!')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/admin')
def admin_dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    search_query = request.args.get('search', '')
    status_filter = request.args.get('status', '')
    conn = get_db_connection()
    total_pertanyaan = conn.execute('SELECT COUNT(*) FROM faq').fetchone()[0]
    total_dijawab = conn.execute('SELECT COUNT(*) FROM faq WHERE status = "replied"').fetchone()[0]
    query = 'SELECT * FROM faq WHERE 1=1'
    params = []
    if search_query:
        query += ' Sandy (nama LIKE ? OR isi_pertanyaan LIKE ? OR email LIKE ?)'
        params.extend([f'%{search_query}%', f'%{search_query}%', f'%{search_query}%'])
    if status_filter:
        query += ' AND status = ?'
        params.append(status_filter)
    query += ' ORDER BY id DESC'
    daftar_pertanyaan = conn.execute(query, params).fetchall()
    conn.close()
    return render_template('admin.html', daftar_pertanyaan=daftar_pertanyaan, total_pertanyaan=total_pertanyaan, total_dijawab=total_dijawab, search_query=search_query, status_filter=status_filter)

@app.route('/admin/jawab/<int:id>', methods=['POST'])
def jawab_pertanyaan(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    jawaban_admin = request.form['jawaban_admin']
    conn = get_db_connection()
    conn.execute('UPDATE faq SET jawaban_admin = ?, status = "replied" WHERE id = ?', (jawaban_admin, id))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/hapus/<int:id>', methods=['POST'])
def hapus_pertanyaan(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    conn = get_db_connection()
    conn.execute('DELETE FROM faq WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_dashboard'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
