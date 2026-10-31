# Audit proyek dan usulan revisi

31 Oktober 2026. Dibaca bersama `REVIEW-MINIPAPER.md`. Audit ini memperbarui catatan sebelumnya setelah folder `game-theory/` tersedia. Kode eksperimen, paper, dan dokumen Google tidak diubah.

## Hasil verifikasi

- Protokol, requirements, manifest, tabel, CSV per observasi, dan laporan historis 266 checks tersedia. Hash script `run_revision_experiments.py` dan protokol cocok dengan manifest.
- Dihitung ulang 160 kombinasi pemeriksaan ringkasan atribusi dari 40 CSV lokal (empat keluarga, variasi seed/background, dua kelompok fitur, empat cutoff). Seluruh count, disagreement, mean L1, dan mean absolute group-total difference yang diperiksa sesuai tabel.
- Dihitung ulang AP, ROC-AUC, precision, recall, F1, dan Brier dari 24 CSV prediksi. Metrik cocok dengan toleransi 1e-12 untuk metrik selain Brier, dan 1e-8 untuk Brier. Selisih Brier maksimum sekitar 1,55e-10, tidak mengubah angka paper.
- Hasil XGBoost utama tetap 149/1.000 disagreement dan mean L1 0,105068996. Variasi background menghasilkan 149, 137, dan 121 disagreement; seed 73 menghasilkan 171.
- Pada salinan workspace ini ditemukan **nol NPZ dan nol joblib**. Belum dapat menjalankan ulang prediksi model, additivity, atau perhitungan TreeSHAP. Laporan 266 checks adalah artefak historis yang sudah ada, bukan 266 checks yang semuanya dijalankan ulang dalam audit ini.
- Lingkungan audit menggunakan NumPy 2.4.2, pandas 3.0.2, scikit-learn 1.8.0; berbeda dari lingkungan eksperimen dalam manifest. Audit hanya membaca CSV, tidak retrain.

Hasil terstruktur: `PROJECT-AUDIT-CHECKS.json`.

## Kode dan dokumentasi yang sebaiknya diedit

| Prioritas | Lokasi | Temuan dan usulan |
|---|---|---|
| Tinggi untuk reproduksi | Folder artefak eksperimen | Sertakan model `model.joblib`, 32 array `shap_*.npz`, dan encoder tersimpan sesuai manifest. Ketiadaan salinan bukan bukti eksperimen tidak dilakukan, tetapi menghalangi reproduksi penuh di sini. |
| Sedang | `game-theory/README.md`, pembuka dan Status proyek | Masih menyatakan model utama Random Forest dan seed tambahan belum dilakukan. Bagian revisi sudah menjelaskan hasil baru, tetapi pembuka tetap menyesatkan. Jadikan XGBoost/fokus enam tagihan sebagai status aktif; tandai RF sebagai tahap historis. Tautan draf aktif sebaiknya ke `kredit/paper/paper_draft_en.md`. |
| Sedang | `kredit/verify_revision_results.py:45` | Field `plots_visually_reviewed: 5` ditulis sebagai konstanta oleh script numerik. Menjalankan script tidak membuktikan review visual baru. Pisahkan catatan review manual beserta tanggal/reviewer dari hasil pemeriksaan otomatis. |
| Sedang | `kredit/verify_revision_results.py:5` | Root memakai `Path('kredit').resolve()`, sehingga bergantung pada current working directory. Gunakan lokasi script sebagai dasar path agar bisa dipanggil dari lokasi lain. |
| Sedang | `kredit/run_revision_experiments.py:93` dan jalur checkpoint | Model kandidat dimuat bila file ada, tanpa pemeriksaan lengkap bahwa data, parameter, dan versi masih sama. Tambahkan fingerprint input/config/environment sebelum reuse agar perubahan konfigurasi tidak diam-diam memakai model lama. Belum ditemukan bukti hal ini mengubah hasil tersimpan saat ini. |
| Sedang | Pembacaan CSV prediksi untuk audit | Parser pandas default menyebabkan satu label di batas threshold berubah pada delapan berkas validation. Dengan `float_precision='round_trip'`, seluruh label cocok kembali. Gunakan pembacaan ini saat memverifikasi probabilitas float64 dari CSV; simpan dtype asal untuk output float32. Jangan mengubah threshold atau angka paper untuk mengatasi artefak parser. |
| Rendah | `requirements_revision.txt` dan `REPRODUCTION.md` | Versi sudah tersedia. Environment lokal yang disebut README tidak ikut tersalin. Dokumentasikan instalasi bersih dan jalur artefak yang benar untuk salinan proyek ini. Keberhasilan clean install belum diuji. |

Nomor baris merujuk file saat audit. Usulan di atas belum diterapkan.

## Bagian paper yang sebaiknya diedit

1. **Abstrak PDF halaman 1:** ubah kalimat ambigu “model fit on 1000 test observations” menjadi “Both modes explain the same fitted XGBoost model on 1,000 fixed test observations.” Draf MD lokal sudah memiliki redaksi yang lebih jelas daripada PDF. Jangan menimpa seluruh PDF/Google Docs dari MD karena redaksi pengguna dapat berbeda.
2. **Abstrak PDF dan MD:** perjelas 23 prediktor asli menjadi 89 input setelah encoding. Contoh: “The model uses all 23 original predictors, represented by 89 encoded input columns.”
3. **VI. Limitations and Reproducibility:** tambahkan lokasi lampiran/repository yang dapat diakses dosen dan versi paket dari manifest. Klaim 266 checks memiliki laporan pendukung, tetapi jangan menyebut audit sekarang sebagai reproduksi penuh. Sebelum membagikan paket reproduksi, lengkapi file biner yang masih kurang.
4. **II.C Related research:** ringkas perbedaan desain terhadap studi terdahulu secara konkret. Pertahankan kontribusi sebagai studi kasus sensitivitas; tidak perlu memaksakan klaim algoritme baru.
5. **Gambar 5:** pertimbangkan titik tanpa garis karena seed merupakan kategori, bukan urutan konvergensi. Ini perbaikan presentasi, bukan kesalahan hasil.
6. **Abstrak/diskusi:** padatkan pengulangan kualifikasi tanpa menghapus keterbatasan penting. Tidak ada alasan dari audit CSV ini untuk mengganti angka utama atau melatih ulang seluruh model sekarang.

## Keputusan untuk minipaper dan UAS

Minipaper dapat tetap memakai desain dan hasil sekarang dengan revisi penjelasan serta kelengkapan lampiran. Banyak seed/background, eksperimen dependensi terkontrol, evaluasi baru yang belum diperiksa, dan grouped-player Shapley merupakan pengembangan UAS. Jangan menyajikannya sebagai eksperimen yang sudah dilakukan.

Audit kode ini memperkuat keterlacakan hasil, tetapi tidak menentukan siapa yang menulis teks, tidak menghasilkan persentase AI, dan tidak menggantikan pemeriksaan kemiripan sumber.
