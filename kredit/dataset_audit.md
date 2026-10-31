# Audit dataset kredit: langkah 1-3

Penanggung jawab: Nurman Aqil Wicaksono (L0124139). Tanggal penyusunan awal: 20 Oktober 2026.

## Status

Snapshot raw, notebook audit, kamus 25 variabel, dan keputusan pembersihan selesai. Belum membuat split, dataset bersih, encoding, model, atau TreeSHAP. Semua pemeriksaan keutuhan sumber lulus.

| Ukuran | Hasil |
| --- | --- |
| Baris | 30000 |
| Kolom | 25 |
| Fitur prediksi (tanpa ID/target) | 23 |
| Sel kosong | 0 |
| ID unik | 30000 |
| Baris dihapus/diubah | 0 |

## Target

| kode | jumlah | persen | arti |
| --- | --- | --- | --- |
| 0 | 23364 | 77.88 | Tidak gagal bayar |
| 1 | 6636 | 22.12 | Gagal bayar |

Baseline selalu memprediksi kelas mayoritas mencapai 77.88% accuracy; ini perhitungan proporsi kelas, bukan model yang sudah dilatih.

## Temuan yang perlu dibawa ke preprocessing

- EDUCATION 0/5/6: 345 baris. Kelak digabung sebagai unknown; kode 4 tetap others.
- MARRIAGE 0: 54 baris. Tetap kategori unknown.
- Tagihan negatif: 1930 nasabah, 3932 sel. Dipertahankan.
- Profil fitur raw identik: 108 baris dalam 52 kelompok, termasuk 21 kelompok dengan target berbeda. Tidak dihapus otomatis.
- Tidak ada kolom konstan. Setiap prediktor memiliki variasi teramati; ini belum bukti daya prediksi.
- Kolom nominal tetap kategori walau dibaca sebagai integer. Nilai ekstrem belum difilter, dan distribusi kelas belum diubah.

## Keutuhan dan asal data

SHA-256 sumber asli dan snapshot: `a0f0ab49d6326671d6cd83be5c88dcf18007025fe9a53ecd699119c871176ca1`. Snapshot: `raw/UCI_Credit_Card.csv`. Manifest memuat URL sumber, ukuran, dan waktu pencatatan; tanggal unduh/versi Kaggle belum diketahui dan tidak dikarang. Kesamaan byte terhadap unduhan resmi belum diverifikasi.

## Cara menjalankan

Buka `01_dataset_audit.ipynb` dan jalankan sel berurutan dengan Python, pandas, dan numpy. Alternatif dari folder proyek: `python kredit/audit_dataset.py`. Notebook memanggil fungsi transparan di `audit_dataset.py`, sehingga file script perlu tetap berada di folder yang sama.

Notebook yang disertakan telah dieksekusi berurutan menggunakan Python (bukan kernel Jupyter pada lingkungan ini). Output sel berasal dari eksekusi tersebut. Jika salinan raw berbeda dari sumber, proses berhenti tanpa menimpanya.

## Hasil untuk Aqil

- `data_dictionary.md`: definisi setiap kolom dan sumbernya.
- `data_cleaning_decisions.md`: temuan, perlakuan, dan alasan.
- `audit/`: tabel frekuensi, profil kolom, penanda per baris, grup identik, statistik numerik, kebijakan JSON, dan verifikasi.

## Pekerjaan berikutnya

Terapkan pemetaan kategori deterministik ke salinan kerja, bentuk ulang grup profil tanpa ID/target, lalu buat train/validation/test dengan menjaga grup dan mendekati proporsi kelas. Fit encoder hanya pada train. Korelasi untuk pemilihan fokus riset dihitung pada train, bukan memakai hasil audit seluruh data untuk memilih fitur. Tahap berikutnya belum dijalankan.

## Bahan Dataset dan Preprocessing

Dataset lokal memiliki 30,000 observasi dengan 23 prediktor, satu identifier, dan satu target biner. Target positif berjumlah 6,636 (22.12%). Audit menemukan 0 sel kosong dan 0 nilai nonfinite. Kode kategori yang dokumentasinya tidak lengkap, tagihan negatif, dan profil fitur identik ditandai untuk perlakuan eksplisit. Data mentah dipertahankan dan snapshot diverifikasi menggunakan SHA-256. Pada tahap audit ini tidak ada baris dibuang maupun nilai ditransformasikan. Prosedur split dan encoding harus dijelaskan dalam bentuk sudah dilakukan hanya setelah tahap tersebut benar-benar dijalankan.

## Referensi

- [S1: UCI Default of Credit Card Clients](https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients)
- [S2: Kaggle mirror: uciml/default-of-credit-card-clients-dataset](https://www.kaggle.com/datasets/uciml/default-of-credit-card-clients-dataset)
- [S3: Lin dan Wang (2025), preprint, Tabel 1 dan bagian Data Source and Cleaning](https://arxiv.org/pdf/2508.01851)
