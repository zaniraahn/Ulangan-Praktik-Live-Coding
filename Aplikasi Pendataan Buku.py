import json
import os
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, IntPrompt
from rich.panel import Panel
from rich.text import Text

console = Console()

# File untuk menyimpan data buku
DATA_FILE = "buku_perpustakaan.json"

# Fungsi untuk memuat data dari file
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

# Fungsi untuk menyimpan data ke file
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Fungsi untuk menampilkan menu utama
def main_menu():
    console.print(Panel.fit("[bold blue]Aplikasi Pendataan Buku Perpustakaan[/bold blue]", border_style="blue"))
    console.print("\n[1] Tambah Buku")
    console.print("[2] Lihat Daftar Buku")
    console.print("[3] Edit Data Buku")
    console.print("[4] Hapus Buku")
    console.print("[5] Pencarian Buku")
    console.print("[6] Peminjaman Buku")
    console.print("[7] Pengembalian Buku")
    console.print("[8] Keluar")
    choice = IntPrompt.ask("\nPilih menu", choices=["1", "2", "3", "4", "5", "6", "7", "8"])
    return choice

# Fungsi untuk menambah buku
def tambah_buku(data):
    console.print("\n[bold green]Tambah Buku Baru[/bold green]")
    id_buku = Prompt.ask("ID Buku")
    judul = Prompt.ask("Judul Buku")
    penulis = Prompt.ask("Penulis")
    tahun = IntPrompt.ask("Tahun Terbit")
    kategori = Prompt.ask("Kategori")
    status = "Tersedia"

    buku = {
        "id_buku": id_buku,
        "judul": judul,
        "penulis": penulis,
        "tahun": tahun,
        "kategori": kategori,
        "status": status
    }
    data.append(buku)
    save_data(data)
    console.print("[green]Buku berhasil ditambahkan![/green]")

# Fungsi untuk melihat daftar buku
def lihat_daftar_buku(data):
    console.print("\n[bold cyan]Daftar Buku[/bold cyan]")
    if not data:
        console.print("[red]Tidak ada buku dalam daftar.[/red]")
        return

    table = Table(title="Daftar Buku Perpustakaan")
    table.add_column("ID Buku", style="cyan", no_wrap=True)
    table.add_column("Judul", style="magenta")
    table.add_column("Penulis", style="green")
    table.add_column("Tahun", justify="right")
    table.add_column("Kategori", style="yellow")
    table.add_column("Status", style="red")

    for buku in data:
        table.add_row(
            buku["id_buku"],
            buku["judul"],
            buku["penulis"],
            str(buku["tahun"]),
            buku["kategori"],
            buku["status"]
        )
    console.print(table)

# Fungsi untuk edit buku
def edit_buku(data):
    console.print("\n[bold yellow]Edit Data Buku[/bold yellow]")
    id_buku = Prompt.ask("Masukkan ID Buku yang ingin diedit")
    for buku in data:
        if buku["id_buku"] == id_buku:
            console.print(f"Data saat ini: {buku}")
            buku["judul"] = Prompt.ask("Judul baru", default=buku["judul"])
            buku["penulis"] = Prompt.ask("Penulis baru", default=buku["penulis"])
            buku["tahun"] = IntPrompt.ask("Tahun baru", default=buku["tahun"])
            buku["kategori"] = Prompt.ask("Kategori baru", default=buku["kategori"])
            save_data(data)
            console.print("[green]Data buku berhasil diupdate![/green]")
            return
    console.print("[red]Buku dengan ID tersebut tidak ditemukan.[/red]")

# Fungsi untuk hapus buku
def hapus_buku(data):
    console.print("\n[bold red]Hapus Buku[/bold red]")
    id_buku = Prompt.ask("Masukkan ID Buku yang ingin dihapus")
    for i, buku in enumerate(data):
        if buku["id_buku"] == id_buku:
            confirm = Prompt.ask(f"Yakin hapus buku '{buku['judul']}'? (y/n)", choices=["y", "n"])
            if confirm == "y":
                del data[i]
                save_data(data)
                console.print("[green]Buku berhasil dihapus![/green]")
            return
    console.print("[red]Buku dengan ID tersebut tidak ditemukan.[/red]")

# Fungsi untuk pencarian buku
def pencarian_buku(data):
    console.print("\n[bold purple]Pencarian Buku[/bold purple]")
    query = Prompt.ask("Masukkan kata kunci (judul, penulis, atau kategori)").lower()
    results = [buku for buku in data if query in buku["judul"].lower() or query in buku["penulis"].lower() or query in buku["kategori"].lower()]
    if results:
        table = Table(title=f"Hasil Pencarian untuk '{query}'")
        table.add_column("ID Buku", style="cyan", no_wrap=True)
        table.add_column("Judul", style="magenta")
        table.add_column("Penulis", style="green")
        table.add_column("Tahun", justify="right")
        table.add_column("Kategori", style="yellow")
        table.add_column("Status", style="red")
        for buku in results:
            table.add_row(
                buku["id_buku"],
                buku["judul"],
                buku["penulis"],
                str(buku["tahun"]),
                buku["kategori"],
                buku["status"]
            )
        console.print(table)
    else:
        console.print("[red]Tidak ada buku yang cocok dengan kata kunci tersebut.[/red]")

# Fungsi untuk peminjaman buku
def peminjaman_buku(data):
    console.print("\n[bold orange]Peminjaman Buku[/bold orange]")
    id_buku = Prompt.ask("Masukkan ID Buku yang ingin dipinjam")
    for buku in data:
        if buku["id_buku"] == id_buku:
            if buku["status"] == "Tersedia":
                buku["status"] = "Dipinjam"
                save_data(data)
                console.print("[green]Buku berhasil dipinjam![/green]")
            else:
                console.print("[red]Buku sedang dipinjam.[/red]")
            return
    console.print("[red]Buku dengan ID tersebut tidak ditemukan.[/red]")

# Fungsi untuk pengembalian buku
def pengembalian_buku(data):
    console.print("\n[bold orange]Pengembalian Buku[/bold orange]")
    id_buku = Prompt.ask("Masukkan ID Buku yang ingin dikembalikan")
    for buku in data:
        if buku["id_buku"] == id_buku:
            if buku["status"] == "Dipinjam":
                buku["status"] = "Tersedia"
                save_data(data)
                console.print("[green]Buku berhasil dikembalikan![/green]")
            else:
                console.print("[red]Buku sudah tersedia.[/red]")
            return
    console.print("[red]Buku dengan ID tersebut tidak ditemukan.[/red]")

# Fungsi utama
def main():
    data = load_data()
    while True:
        choice = main_menu()
        if choice == 1:
            tambah_buku(data)
        elif choice == 2:
            lihat_daftar_buku(data)
        elif choice == 3:
            edit_buku(data)
        elif choice == 4:
            hapus_buku(data)
        elif choice == 5:
            pencarian_buku(data)
        elif choice == 6:
            peminjaman_buku(data)
        elif choice == 7:
            pengembalian_buku(data)
        elif choice == 8:
            console.print("[bold blue]Terima kasih telah menggunakan aplikasi![/bold blue]")
            break
        console.print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    main()