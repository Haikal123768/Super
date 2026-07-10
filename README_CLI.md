# CLI untuk Mengelola Aset Pribadi (ASSETS.csv)

File `assets_cli.py` adalah skrip Python kecil untuk mengelola file `ASSETS.csv` dan menambah transaksi ke `VIRTUAL-MONEY.md`.

Cara pakai (di terminal pada folder repo):

1. Jalankan daftar perintah:

```bash
python assets_cli.py list-assets
```

2. Tambah aset baru:

```bash
python assets_cli.py add-asset --name "Rekening Pribadi" --service gembe.x1 --account 081234 --balance 100000 --notes "Untuk kebutuhan"
```

3. Update saldo aset:

```bash
python assets_cli.py update-balance --id 1 --balance 120000
```

4. Tambah transaksi ke `VIRTUAL-MONEY.md` (ditambahkan ke tabel `Riwayat Transaksi`):

```bash
python assets_cli.py add-transaction --service gembe.x1 --type Top-up --amount 100000 --note "Top-up via bank" --balance_after 200000
```

Catatan keamanan:
- Jangan masukkan PIN, OTP, atau password ke file CSV atau Markdown.
- Simpan repositori ini privat.

Dependencies: hanya Python 3 (tidak perlu paket tambahan).
