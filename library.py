inventaris = {}
peminjaman = {}  # Existing structure
anggota = {}  # New structure for library members
from datetime import datetime, timedelta  # Added for time handling


def tambah_buku(judul: str, jumlah_salinan: int, lokasi_rak: str):
    inventaris[judul] = {"jumlah_salinan": jumlah_salinan, "lokasi_rak": lokasi_rak}
    print(f"Buku '{judul}' berhasil ditambahkan.")

def hapus_buku(judul: str) -> None:
    if judul in inventaris:
        del inventaris[judul]
        print(f"Buku '{judul}' berhasil dihapus dari inventaris.")
    else:
        print(f"Buku '{judul}' tidak ditemukan di inventaris.")

def tampilkan_inventaris():
    print("Inventaris Buku:")
    for judul, detail in inventaris.items():
        print(f"- {judul}: {detail['jumlah_salinan']} salinan, lokasi rak: {detail['lokasi_rak']}")

def cari_buku(query: str) -> None:
    hasil_cocok = {judul: detail for judul, detail in inventaris.items() if query.lower() in judul.lower()}
    if hasil_cocok:
        print("Hasil pencarian:")
        for judul, detail in hasil_cocok.items():
            print(f"- {judul}: {detail['jumlah_salinan']} salinan, lokasi rak: {detail['lokasi_rak']}")
    else:
        print("Tidak ada buku yang cocok dengan kata kunci ini.")

def jumlah_total_salinan() -> None:
    total = sum(detail["jumlah_salinan"] for detail in inventaris.values())
    print(f"Total seluruh salinan buku di inventaris: {total}")


def update_salinan(judul: str, jumlah_baru: int) -> None:
    if judul in inventaris:
        inventaris[judul]["jumlah_salinan"] = jumlah_baru
        print(f"Jumlah salinan buku '{judul}' berhasil diupdate.")
    else:
        print(f"Buku '{judul}' tidak ditemukan.")


batas_pinjam_hari = 7  # Lama batas pengembalian (hari)
denda_per_hari = 50000

def pinjam_buku(judul: str, nama_peminjam: str, alamat: str, nomor_hp: str) -> None:
    if judul in inventaris and inventaris[judul]["jumlah_salinan"] > 0:
        if judul not in peminjaman:
            peminjaman[judul] = []

        max_tanggal_pengembalian = (datetime.now() + timedelta(days=batas_pinjam_hari)).strftime("%Y-%m-%d %H:%M:%S")
        inventaris[judul]["jumlah_salinan"] -= 1
        peminjaman[judul].append({
                "nama_peminjam": nama_peminjam,
                "alamat": alamat,
                "nomor_hp": nomor_hp,
                "tanggal_peminjaman": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "batas_pengembalian": max_tanggal_pengembalian,
                "tanggal_pengembalian": None
        })


        print(f"Buku '{judul}' berhasil dipinjam oleh {nama_peminjam}.")
    else:
        print(f"Buku '{judul}' tidak tersedia atau stok habis.")


def kembalikan_buku(judul: str, nama_peminjam: str) -> None:
    # denda_per_hari already defined globally; removed duplicate
    if judul in peminjaman and any(
        entry["nama_peminjam"] == nama_peminjam and entry["tanggal_pengembalian"] is None for entry in peminjaman[judul]
    ):
        for entry in peminjaman[judul]:
            if entry["nama_peminjam"] == nama_peminjam and entry["tanggal_pengembalian"] is None:
                tanggal_pengembalian = datetime.now()
                entry["tanggal_pengembalian"] = tanggal_pengembalian.strftime("%Y-%m-%d %H:%M:%S")
                batas_pengembalian = datetime.strptime(entry["batas_pengembalian"], "%Y-%m-%d %H:%M:%S")
                if tanggal_pengembalian > batas_pengembalian:
                    selisih_hari = (tanggal_pengembalian - batas_pengembalian).days
                    denda = selisih_hari * denda_per_hari
                    print(f"Peringatan: Buku dikembalikan terlambat. Denda sebesar Rp.{denda:,}.")
                break

        inventaris[judul]["jumlah_salinan"] += 1
        peminjaman[judul] = [entry for entry in peminjaman[judul] if entry["tanggal_pengembalian"]]

        print(f"Buku '{judul}' berhasil dikembalikan oleh {nama_peminjam}.")
    else:
        print(f"Buku '{judul}' tidak sedang dipinjam oleh {nama_peminjam}.")


def tampilkan_pinjaman():
    print("Daftar Peminjaman:")
    for judul, daftar_peminjam in peminjaman.items():
        print(f"Buku: {judul}")
        if daftar_peminjam:
            for entry in daftar_peminjam:

                print(f"  Dipinjam oleh {entry['nama_peminjam']} pada {entry['tanggal_peminjaman']}, batas pengembalian: {entry['batas_pengembalian']}", end="")

                if entry['tanggal_pengembalian']:
                    print(f", dikembalikan pada {entry['tanggal_pengembalian']}")
                else:
                    print("")

def tampilkan_sop() -> None:
    print("SOP Peminjaman dan Pengembalian Buku:")
    print("- Peminjaman buku memiliki batas waktu selama 7 hari.")
    print("- Denda sebesar Rp.50,000 per hari berlaku jika buku dikembalikan terlambat.")
    print("- Harap menjaga kondisi buku tetap baik.")

def tambah_anggota(nama_anggota: str, kontak: str):
    if nama_anggota in anggota:
        print(f"Anggota dengan nama '{nama_anggota}' sudah terdaftar.")
    else:
        anggota[nama_anggota] = {"kontak": kontak}
        print(f"Anggota '{nama_anggota}' berhasil ditambahkan.")
def tampilkan_anggota() -> None:
    if not anggota:
        print("Belum ada anggota yang terdaftar.")
    else:
        print("Daftar Anggota Perpustakaan:")
        for nama, detail in anggota.items():
            print(f"- {nama}: kontak: {detail['kontak']}")
def main() -> None:
    tampilkan_sop()
    print("\n" + "-" * 40)
    while True:
        print("\n" + "-" * 40 + "\nMenu:")
        print("Manajemen Buku:")
        print("  1. Tambah buku")
        print("  2. Tampilkan Semua Buku")
        print("  3. Total seluruh salinan di inventaris")
        print("  4. Update jumlah salinan")
        print("  5. Cari buku")
        print("  6. Hapus buku dari inventaris")
        print("\nPeminjaman:")
        print("  7. Pinjam buku")
        print("  8. Daftar peminjaman")
        print("\nPengembalian:")
        print("  9. Kembalikan buku")
        print("\nAnggota:")
        print("  10. Tambah anggota")
        print("  11. Tampilkan daftar anggota")
        print("\nLain-lain:")
        print("  12. SOP peminjaman dan pengembalian")
        print("  13. Keluar")


        pilihan = input("Pilih menu (1-13): ")
        if pilihan == "1":
            judul = input("Masukkan judul buku: ")
            jumlah = int(input("Masukkan jumlah salinan: "))
            lokasi = input("Masukkan lokasi rak: ")
            tambah_buku(judul, jumlah, lokasi)
        elif pilihan == "2":
            tampilkan_inventaris()
        elif pilihan == "3":
            jumlah_total_salinan()
        elif pilihan == "4":
            judul = input("Masukkan judul buku: ")
            jumlah = int(input("Masukkan jumlah baru salinan: "))
            update_salinan(judul, jumlah)
        elif pilihan == "5":
            query = input("Masukkan kata kunci pencarian: ")
            cari_buku(query)
        elif pilihan == "6":
            judul = input("Masukkan judul buku yang akan dihapus: ")
            hapus_buku(judul)
        elif pilihan == "7":
            judul = input("Masukkan judul buku: ")
            nama_peminjam = input("Masukkan nama peminjam: ")
            alamat = input("Masukkan alamat peminjam: ")
            nomor_hp = input("Masukkan nomor HP peminjam: ")
            pinjam_buku(judul, nama_peminjam, alamat, nomor_hp)
        elif pilihan == "8":
            tampilkan_pinjaman()
        elif pilihan == "9":
            judul = input("Masukkan judul buku: ")
            nama_peminjam = input("Masukkan nama peminjam: ")
            kembalikan_buku(judul, nama_peminjam)
        elif pilihan == "10":
            nama = input("Masukkan nama anggota: ")
            kontak = input("Masukkan kontak anggota: ")
            tambah_anggota(nama, kontak)
        elif pilihan == "11":
            tampilkan_anggota()
        elif pilihan == "12":
            tampilkan_sop()
        elif pilihan == "13":
            print("Terima kasih! Program selesai.")
            break



if __name__ == "__main__":
    main()