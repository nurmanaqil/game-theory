# Hasil Aqil: apa yang dikeluarkan dan apa yang masuk paper

## Status

Preprocessing, split tetap, encoding train-only, analisis korelasi train, dan bahan metode selesai. Belum melatih model atau menghitung TreeSHAP.

## Apa yang di-drop?

- ID dikeluarkan dari X, tetap ada pada metadata.
- Target dipisahkan sebagai y, bukan dihapus dari penelitian.
- Tidak ada baris dihapus. Tagihan negatif, pembayaran nol, label berbeda pada profil sama, serta enam tagihan berkorelasi tetap disimpan.
- EDUCATION: 345 observasi menjadi unknown; 331 kode 5/6 berubah ke 0, sementara 14 kode 0 sudah unknown. MARRIAGE 0 tetap unknown.

## Pembagian aktual

| Partition | Observations | Non-default | Default | Default share |
| --- | --- | --- | --- | --- |
| Train | 18005 | 14054 | 3951 | 21.94% |
| Validation | 5997 | 4631 | 1366 | 22.78% |
| Test | 5998 | 4679 | 1319 | 21.99% |

Profil identik dihitung ulang setelah recoding: 108 baris dalam 52 kelompok. Tidak ada kelompok yang tersebar ke lebih dari satu split. Matriks model memiliki 89 kolom hasil encoding dari 23 fitur asal.

## Output untuk paper

Buka `paper/dataset_preprocessing.md` sebagai bahan paper aktif. Sesuaikan penomoran tabel, gambar, dan sitasi dengan naskah bersama. Draf awal dengan sitasi D1-D5 tersimpan di `paper/archive/dataset_preprocessing_legacy.md`. Gambar PNG/PDF di `paper/figures/` siap dimasukkan. Tabel CSV di `paper/tables/` adalah sumber angka untuk tabel naskah, bukan semua wajib ditampilkan.

Bagian ini dapat ditulis sebagai pekerjaan yang sudah dilakukan. Klaim performa Random Forest, fitur terpenting, atau perbedaan TreeSHAP belum boleh ditambahkan sebelum eksperimen model.

## Output untuk Irfan

Gunakan `processed/encoded/X_train.csv` dan `y_train.csv` untuk pelatihan. Validation dipakai memilih pengaturan/threshold. Test disisihkan untuk evaluasi akhir. Jangan melakukan split baru atau fit ulang encoder pada gabungan data. Urutan baris X, y, dan metadata konsisten; jangan mengurutkan salah satunya secara terpisah.

Contoh pembacaan:

```python
from pathlib import Path
import pandas as pd
base = Path('kredit/processed/encoded')
X_train = pd.read_csv(base / 'X_train.csv')
y_train = pd.read_csv(base / 'y_train.csv')['default.payment.next.month']
X_val = pd.read_csv(base / 'X_validation.csv')
y_val = pd.read_csv(base / 'y_validation.csv')['default.payment.next.month']
```

## Output untuk Yahya

Gunakan input model dalam urutan `artifacts/feature_schema.json`. Background TreeSHAP interventional harus berasal dari train. Gunakan `feature_map.csv` untuk menjumlahkan atribusi signed indikator kategori kembali ke fitur asal sebelum ringkasan feature-level. Penjumlahan indikator untuk pelaporan tidak otomatis sama dengan Shapley dari permainan fitur yang digabung. Semua BILL_AMT tetap satu kolom numerik.

## Struktur hasil

- `processed/semantic/`: fitur dengan nama asal sesudah pemetaan; untuk audit/EDA.
- `processed/encoded/`: X dan y siap model, tanpa ID atau index tambahan.
- `processed/metadata/`: ID, grup profil, fold, dan membership split.
- `artifacts/`: preprocessor, skema, feature map, konfigurasi, checksum, dan hasil verifikasi.
- `paper/`: teks metode, tabel, gambar.
- `Paket_Aqil_untuk_Irfan.zip`: paket lokal untuk handoff dan reproduksi.

## Batas dan perhatian

Kode kategori yang tidak jelas diperlakukan konservatif. Data historis Taiwan bukan pembuktian untuk nasabah Indonesia saat ini. Pengelompokan profil hanya mengatasi kesamaan fitur yang teramati. Kategori validation/test yang tidak dijumpai di train dicatat di `paper/tables/unseen_categories.csv`; kebijakan ignore dipertahankan dan encoder tidak diperbarui dari held-out data.

## Verifikasi

30/30 pemeriksaan lulus: checksum raw tetap, tidak ada grup lintas-split, encoder hanya mengikuti kategori train, alignment ID/label benar, nilai finite, urutan fitur sama, dan artefak hasil simpan dapat dibaca ulang.
