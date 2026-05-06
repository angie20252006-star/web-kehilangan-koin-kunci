from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Sistem Kehilangan Koin & Kunci Drawer ATMI</title>

<style>
body {
  margin: 0;
  font-family: 'Poppins', sans-serif;
  height: 100vh;
  background: url("/static/atmi.jpg") no-repeat center/cover;
  display: flex;
  justify-content: center;
  align-items: center;
}

body::before {
  content: "";
  position: absolute;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.65);
}

.card {
  position: relative;
  z-index: 2;
  width: 420px;
  padding: 30px;
  border-radius: 20px;
  backdrop-filter: blur(15px);
  background: rgba(255,255,255,0.08);
  box-shadow: 0 0 30px rgba(0,255,255,0.25);
  text-align: center;
}

button {
  padding: 10px;
  margin: 5px;
  border: none;
  border-radius: 10px;
  background: #0072ff;
  color: white;
  cursor: pointer;
}

.danger {
  background: red;
}

.back {
  background: gray;
}

h3, p {
  color: white;
}
</style>
</head>

<body>

<div class="card">
<h2 style="color:#00eaff;">Sistem Kehilangan Koin & Kunci Drawer ATMI</h2>

{% if step == 1 %}
<form method="post">
  <input name="nama" placeholder="Nama"><br><br>
  <input name="nim" placeholder="NIM"><br><br>
  <button name="step" value="2">Lanjut</button>
</form>

{% elif step == 2 %}
<form method="post">
  <input type="hidden" name="nama" value="{{nama}}">
  <input type="hidden" name="nim" value="{{nim}}">
  <h3>Pilih Kehilangan</h3>
  <button name="item" value="koin">Koin</button>
  <button name="item" value="kunci drawer">Kunci Drawer</button>
  <input type="hidden" name="step" value="3">
</form>

<form method="post">
  <button class="back" name="step" value="1">⬅ Kembali</button>
</form>

{% elif step == 3 %}
<form method="post">
  <input type="hidden" name="nama" value="{{nama}}">
  <input type="hidden" name="nim" value="{{nim}}">
  <input type="hidden" name="item" value="{{item}}">
  
  <h3>
    {% if warning %}
      {{ warning }}
    {% else %}
      Sudah tanya di grup besar ATMI?
    {% endif %}
  </h3>

  <button name="step" value="4">✔ Sudah</button>
  <button class="danger" name="step" value="3">✖ Belum</button>

  <input type="hidden" name="warning" value="Tanyakan dulu di grup besar ATMI!!">
</form>

<form method="post">
  <button class="back" name="step" value="2">⬅ Kembali</button>
</form>

{% elif step == 4 %}
<form method="post">
  <input type="hidden" name="nama" value="{{nama}}">
  <input type="hidden" name="nim" value="{{nim}}">
  <input type="hidden" name="item" value="{{item}}">
  
  <h3>
    {% if warning2 %}
      {{ warning2 }}
    {% else %}
      Sudah cari di lingkungan kampus ATMI?
    {% endif %}
  </h3>

  <button name="step" value="5">✔ Sudah</button>
  <button class="danger" name="step" value="4">✖ Belum</button>

  <input type="hidden" name="warning2" value="Carilah dilingkungan kampus ATMI terlebih dahulu!!">
</form>

<form method="post">
  <button class="back" name="step" value="3">⬅ Kembali</button>
</form>

{% elif step == 5 %}
<form method="post">
  <input type="hidden" name="nama" value="{{nama}}">
  <input type="hidden" name="nim" value="{{nim}}">
  <input type="hidden" name="item" value="{{item}}">

  <h3>Proses Penggantian {{item}}</h3>

  {% if item == "kunci drawer" %}
    <p>1. Pergi ke kabeng untuk meminta form keterangan hilang kunci drawer.</p>
    <p>2. Konfirmasi dan minta tanda tangan ke kabeng sesuai prodi kamu.</p>
    <p>3. Lakukan pembayaran di finance.</p>
    <p>4. Serahkan kwitansi ke kabeng sesuai prodi kamu.</p>
 {% else %}
  <p>1. Konfirmasi kepada kabeng bahwa koin telah hilang.</p>
  <p>2. Ambil form penggantian di kabeng sesuai prodi kamu.</p>
  <p>3. Meminta tanda tangan pada setiap penjaga yang sedang bertugas dikamar alat di kampus gonzaga,arrupe,dan kampus 1.</p>
  <p>4. Serahkan form ke finance agar mendapat kwitansi.</p>
  <p>5. Serahkan kwitansi kepada kabeng sesuai prodi untuk dimintai tanda tangan.</p>
  <p>6. Setelah ditandatanganin serahkan kwitansi kepada finance untuk melakukan pembayaran.</p>
{% endif %}

  <button name="step" value="6">Lanjut</button>
</form>

<form method="post">
  <button class="back" name="step" value="4">⬅ Kembali</button>
</form>

{% elif step == 6 %}
<h3 style="color:#00eaff;">
📄Contoh Form Penggantian {{ "Kunci" if item == "kunci drawer" else "Koin" }}
</h3>

{% if item == "koin" %}
  <img src="/static/form_koin.png" style="width:100%; border-radius:10px; margin-top:10px;">
{% else %}
  <img src="/static/form_kunci.png" style="width:100%; border-radius:10px; margin-top:10px;">
{% endif %}

<form method="post">
  <input type="hidden" name="nama" value="{{nama}}">
  <input type="hidden" name="nim" value="{{nim}}">
  <input type="hidden" name="item" value="{{item}}">
  <button name="step" value="7">Lanjut</button>
</form>

<form method="post">
  <button class="back" name="step" value="5">⬅ Kembali</button>
</form>

{% elif step == 7 %}
<h3 style="color:#00ffcc;">✅ Berhasil</h3>

<p>{{nama}}</p>
<p>{{nim}}</p>

<p>
Pengajuan {{item}} sedang diproses, bertanggungjawablah dengan koin atau kunci drawer masing-masing.
</p>

<form method="post">
  <button name="step" value="1">🔄 Ulangi</button>
</form>
{% endif %}

</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    step = 1
    nama = ""
    nim = ""
    item = ""
    warning = ""
    warning2 = ""

    if request.method == "POST":
        step = int(request.form.get("step", 1))
        nama = request.form.get("nama", "")
        nim = request.form.get("nim", "")
        item = request.form.get("item", "")
        warning = request.form.get("warning", "")
        warning2 = request.form.get("warning2", "")

    return render_template_string(
        HTML,
        step=step,
        nama=nama,
        nim=nim,
        item=item,
        warning=warning,
        warning2=warning2
    )

if __name__ == "__main__":
    app.run(debug=True)