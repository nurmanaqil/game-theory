# Posisi penelitian revisi terhadap literatur

Pemeriksaan 23 Oktober 2026. Catatan ini membedakan metadata/abstrak/teks yang dapat diakses dari pemeriksaan full text lengkap. Ini bukan systematic literature review dan belum mendukung klaim penelitian pertama.

## Dua paper 2025 yang berbeda

| Sumber | Bukti yang dapat diverifikasi | Hubungan dengan proyek |
|---|---|---|
| García-Céspedes, Alias-Carrascosa, Moreno (2025), On Machine Learning models explainability in the banking sector: the case of SHAP. DOI 10.1080/01605682.2025.2485263 | Halaman penerbit dan abstrak terindeks menyebut perbandingan interventional/path-dependent serta perubahan penjelasan ketika distribusi portfolio berubah. Catatan kaki sumber menyebut keterbatasan output probabilitas pada path-dependent. Full text lengkap gagal diakses melalui konektor (403). | Perbandingan mode dan sensitivitas referensi sudah diteliti. Penelitian kita tidak dapat mengklaim kedua ide ini sebagai metode baru. Rincian dataset Home Credit ditemukan dalam indeks salinan penulis, tetapi belum diperiksa ulang dari full text primer; jangan memakai perbedaan dataset sebagai fondasi kebaruan. |
| Lin dan Wang (2025), SHAP Stability in Credit Risk Management: A Case Study in Credit Card Default Model. DOI 10.3390/risks13120238 | Teks terindeks penerbit menyebut UCI Taiwan 30.000 nasabah, 100 model XGBoost dengan seed berbeda, dan Kendall W untuk ranking global. | Dataset dan pengulangan seed sudah pernah digunakan. Tiga seed kita lebih terbatas untuk audit variasi training, bukan mengungguli keluasan 100 seed. Mode eksplisit paper ini belum diaudit tuntas; tidak boleh digabung dengan klaim paper pertama. |

Sumber primer:
- https://www.tandfonline.com/doi/abs/10.1080/01605682.2025.2485263
- https://www.mdpi.com/2227-9091/13/12/238

Penelitian terdekat lain yang sudah dicatat: Nikoltchovska dkk. (2026), Correlations Matter in Explanations for Energy Systems, DOI 10.1007/s13218-026-00904-4. Desain sintetis dan kasus nyata serta perbandingan explainer sudah ada. Full text tidak diaudit ulang dalam tahap ini.

## Pertanyaan dan kontribusi yang dapat dipertanggungjawabkan

Fokus revisi adalah hubungan kesimpulan global, keputusan fitur teratas per observasi, dan magnitudo perbedaan dalam perbandingan dua mode pada empat keluarga model. Perbedaan pemenang ditelaah bersama margin dua atribusi tertinggi untuk membedakan ketidakstabilan urutan yang hampir seri. Variasi seed model dipisahkan dari variasi background; keduanya tidak difaktorialkan seluruhnya.

Pembeda yang diuji, bukan klaim novelty yang sudah terbukti:

1. Perbandingan berpasangan lintas empat keluarga pohon dengan setting sumber data/evaluasi yang tetap.
2. Analisis hubungan ranking global dan top-feature individual, disertai margin pemenang dan magnitudo perbedaan.
3. Perbandingan deskriptif tagihan dan pembayaran, dengan korelasi dihitung hanya pada train.
4. Pemeriksaan satuan raw setiap model, baseline, dan additivity; magnitudo probabilitas tidak dicampur dengan margin log-odds.

Judul kerja: **Mode Sensitivity of TreeSHAP Attributions across Tree-Based Credit Default Models: Global Rankings, Local Agreement, and Winner Margins**.

Klaim yang dihindari: algoritme baru; SHAP sepenuhnya berbeda dari TreeSHAP; yang pertama membandingkan mode; dataset baru otomatis novelty; tiga seed membuktikan ketahanan populasi; perbedaan kedua kelompok disebabkan korelasi; lebih baik dari paper jurnal secara keseluruhan.

## Keputusan ruang lingkup

Dataset dan split lama tetap. Test telah dilihat pada tahap sebelumnya; eksperimen adalah pengembangan eksploratif dengan protokol dibekukan sebelum hasil revisi. Penambahan konfigurasi dari hasil test dilarang. Jika laporan saat ini akan diposisikan sebagai evaluasi konfirmatori, diperlukan rancangan validasi baru yang disepakati dan tidak boleh disebut sudah dilakukan.

## Acuan implementasi

TreeExplainer: https://shap.readthedocs.io/en/latest/generated/shap.TreeExplainer.html
GradientBoostingClassifier 1.7.2: https://scikit-learn.org/1.7/modules/generated/sklearn.ensemble.GradientBoostingClassifier.html
XGBoost: https://xgboost.readthedocs.io/en/stable/parameter.html

Dokumentasi online dapat lebih baru dari versi terpasang; manifest eksperimen mencatat versi aktual. Pilot kompatibilitas XGBoost 3.4.1 dan SHAP 0.54.1 pada 20 observasi merekonstruksi raw margin di kedua mode dalam toleransi 1e-6. Tidak mengubah log-odds SHAP individual dengan sigmoid.
