from flask import Flask, render_template, request, redirect, url_for, flash, session
from connectdb import Database
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = "alfendio"

@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/profil')
def profil(): 
    if 'username' in session:
        return render_template('profil.html')
    else:
        return redirect(url_for('login'))

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for("home"))
    conn = Database('ksb-2022')
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        if conn.select("SELECT * FROM users WHERE username = '{}' AND password = '{}'".format(username, password)):
            session['username'] = username
            session['password'] = password
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/insertAdmin', methods=['GET', 'POST'])
def insertAdmin():
    if 'username' not in session:
        return redirect(url_for("login"))
    conn = Database('ksb-2022')
    id = request.form['id']
    fullname = request.form['fullname']
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    conn.execute("INSERT INTO users (id, fullname, username, password, email) VALUES (%s,%s,%s,%s,%s)", (id, fullname, username, password, email))
    flash('Tambah admin sukses!')
    return redirect(url_for("tampilAdmin"))
   
@app.route('/read')
def read():
    if 'username' not in session:
        return redirect(url_for("login"))    
    conn = Database('ksb-2022')
    result = conn.select("select * from tabel_barang_672019222")
    return render_template ('index.html', database = result)

@app.route('/tampilKategori')
def tampilKategori():
    if 'username' not in session:
        return redirect(url_for("login"))
    conn = Database('ksb-2022')
    result = conn.select("select * from tabel_kategori_672019222")
    return render_template ('readKategori.html', database = result)

@app.route('/tambah_kategori', methods=['POST'])
def tambah_kategori():
    if 'username' not in session:
        return redirect(url_for("login"))   
    conn = Database('ksb-2022')
    id_kategori = request.form['fid_kategori']
    nama_kategori = request.form['fnama_kategori']
    conn.execute("INSERT INTO tabel_kategori_672019222 (id_kategori, nama_kategori) VALUES (%s,%s)", (id_kategori, nama_kategori))
    flash('Tambah kategori sukses!')
    return redirect(url_for("tampilKategori"))

@app.route('/deleteKategori/<id_kategori>', methods = ['GET', 'POST'])
def delete_kategori(id_kategori):
    if 'username' not in session: 
        return redirect(url_for("login"))    
    conn = Database('ksb-2022')
    conn.execute("DELETE FROM tabel_kategori_672019222 WHERE id_kategori = %s" , (id_kategori,))
    #flash('Delete sukses!')
    return redirect(url_for('tampilKategori'))

@app.route('/editKategori', methods = ['GET'])
def edit_kategori():
    if 'username' not in session:
        return redirect(url_for("login"))    
    idtampung = request.args.get('id_kategori')    
    conn = Database('ksb-2022')
    result = conn.select("SELECT * FROM tabel_kategori_672019222 WHERE id_kategori = {0}".format(idtampung))
    print (result)
    return render_template('editKategori.html', kategori = result)

@app.route('/updateKategori/<id_kategori>', methods=['POST'])
def update_kategori(id_kategori):
    if 'username' not in session:
        return redirect(url_for("login"))   
    conn = Database('ksb-2022')
    id_kategori = request.form['id_kategori']
    nama_kategori = request.form['fnama_kategori']
    conn.execute("UPDATE tabel_kategori_672019222 SET nama_kategori=%s" + "WHERE id_kategori=%s" % (nama_kategori),(id_kategori))
    flash('Update sukses!')
    return redirect(url_for("tampilKategori"))

@app.route('/tampilAdmin')
def tampilAdmin():
    if 'username' not in session:
        return redirect(url_for("login"))
    conn = Database('ksb-2022')
    result = conn.select("select * from users")
    return render_template ('iniAdmin.html', database = result)

@app.route('/updateAdmin/<id>', methods=['POST'])
def update_admin(id):
    if 'username' not in session: #no session aman
        return redirect(url_for("login"))
    conn = Database('ksb-2022')
    id = request.form['id']
    fullname = request.form['fullname']
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    conn.execute("UPDATE users SET fullname=%s, username=%s, password=%s, email=%s" + "WHERE id=%s" % (id), (fullname, username, password, email))
    flash('Update sukses!')
    return redirect(url_for("tampilAdmin"))

@app.route('/editAdmin', methods = ['GET'])
def edit_admin():
    if 'username' not in session:
        return redirect(url_for("login"))    
    idtampung = request.args.get('id')    
    conn = Database('ksb-2022')
    result = conn.select("SELECT * FROM users WHERE id = {0}".format(idtampung))
    print (result)
    return render_template('editAdmin.html', admin = result)

@app.route('/deleteAdmin/<id>', methods = ['GET', 'POST'])
def delete_admin(id):
    if 'username' not in session: #no session aman
        return redirect(url_for("login"))    
    conn = Database('ksb-2022')
    conn.execute("DELETE FROM users WHERE id = %s" , (id,))
    flash('Delete sukses!')
    return redirect(url_for('tampilAdmin'))

@app.route('/edit', methods = ['GET'])
def edit_barang():
    if 'username' not in session:
        return redirect(url_for("login"))    
    idtampung = request.args.get('id')    
    conn = Database('ksb-2022')
    result = conn.select("SELECT * FROM tabel_barang_672019222 WHERE id = {0}".format(idtampung))
    print (result)
    return render_template('edit.html', barang = result)

@app.route('/update/<id>', methods=['POST'])
def update_barang(id):
    if 'username' not in session:
        return redirect(url_for("login"))   
    conn = Database('ksb-2022')
    id = request.form['id']
    nama = request.form['fnama']
    id_kategori = request.form['fkategori']
    satuan = request.form['fsatuan']
    jumlah = request.form['fjumlah']
    tanggal = request.form['tanggal']
    conn.execute("UPDATE tabel_barang_672019222 SET nama=%s, id_kategori=%s, satuan=%s, jumlah=%s, tanggal=%s" + "WHERE id=%s" % (id), (nama, id_kategori, satuan, jumlah, tanggal))
    flash('Update sukses!')
    return redirect(url_for("read"))

@app.route('/tambah_barang', methods=['POST'])
def tambah_barang():
    if 'username' not in session:
        return redirect(url_for("login"))   
    conn = Database('ksb-2022')
    id = request.form['id']
    nama = request.form['fnama']
    id_kategori = request.form['fkategori']
    satuan = request.form['fsatuan']
    jumlah = request.form['fjumlah']
    tanggal = request.form['tanggal']
    conn.execute("INSERT INTO tabel_barang_672019222 (id, nama, id_kategori, satuan, jumlah, tanggal) VALUES (%s,%s,%s,%s,%s,%s)", (id, nama, id_kategori, satuan, jumlah, tanggal))
    flash('Tambah barang sukses!')
    return redirect(url_for("read"))

@app.route('/delete/<id>', methods = ['GET', 'POST'])
def delete_barang(id):
    if 'username' not in session:
        return redirect(url_for("login"))   
    conn = Database('ksb-2022')
    conn.execute("DELETE FROM tabel_barang_672019222 WHERE id = %s" , (id,))
    flash('Delete sukses!')
    return redirect(url_for('read'))

@app.route('/logout') 
def logout():
    if 'username' not in session:
        return redirect(url_for("login"))   
    session.pop('username', None)
    session.pop('password', None)
    return redirect(url_for('login'))


if __name__ =="__main__" :
    app.run(debug=True)