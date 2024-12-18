from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Data penyimpanan sederhana
inventaris = {}
anggota = []
peminjaman = []


@app.route("/")
def home():
    """Halaman utama."""
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Pendaftaran anggota."""
    if request.method == "POST":
        nama = request.form.get("nama")
        kontak = request.form.get("kontak")
        if nama in [a["nama"] for a in anggota]:  # Mencegah entry ganda
            return "Anggota sudah terdaftar!", 400
        anggota.append({"nama": nama, "kontak": kontak})
        return redirect("/register")
    return render_template("register.html", anggota=anggota)

    app.route("/register", methods=["GET", "POST"])


@app.route("/loan", methods=["GET", "POST"])
def loan():
        """Peminjaman dan pengembalian buku."""
        if request.method == "POST":
            action = request.form.get("action")
            judul = request.form.get("judul")
            nama = request.form.get("nama")

            # Validate input
            if not judul or not nama:
                return "Data tidak lengkap!", 400

            if action == "pinjam":
                # Check if the book exists and is available
                if judul not in inventaris or inventaris[judul]["jumlah"] == 0:
                    return "Buku tidak tersedia!", 400

                # Check if the user has already borrowed this book
                if any(p["judul"] == judul and p["nama"] == nama for p in peminjaman):
                    return "Buku sudah dipinjam oleh anggota ini!", 400

                inventaris[judul]["jumlah"] -= 1
                peminjaman.append({"judul": judul, "nama": nama})

            elif action == "kembali":
                # Handle book return
                for p in peminjaman:
                    if p["judul"] == judul and p["nama"] == nama:
                        peminjaman.remove(p)
                        inventaris[judul]["jumlah"] += 1
                        break
                else:
                    return "Peminjaman tidak ditemukan!", 400

            return redirect("/loan")

        return render_template("loan.html", peminjaman=peminjaman, inventaris=inventaris)


@app.route("/sop")
def sop():
    """SOP perpustakaan."""
    return render_template("sop.html")

@app.route("/books", methods=["GET", "POST"])
def books():
    """Manajemen inventaris buku."""
    if request.method == "POST":
        judul = request.form.get("judul")
        jumlah = int(request.form.get("jumlah"))
        lokasi = request.form.get("lokasi")
        inventaris[judul] = {"jumlah": jumlah, "lokasi": lokasi}
        return redirect("/books")
    return render_template("books.html", inventaris=inventaris)


print("Daftar Route yang Terdaftar:")
for rule in app.url_map.iter_rules():
    print(f"{rule.endpoint}: {rule.rule}")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")