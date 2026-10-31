# Revisi 31 Oktober 2026

## Naskah yang dapat direview

`paper_draft_revised_en.md` adalah salinan revisi dari `game-theory/kredit/paper/paper_draft_en.md`, bukan transkripsi PDF terbaru atau sinkronisasi Google Docs. PDF pengguna memiliki perubahan redaksi tersendiri; jangan menggantinya seluruhnya tanpa membandingkan kedua versi. Sumber MD aktif dan PDF asli dipertahankan.

Perubahan pada salinan:

- Abstrak dipadatkan; model terlatih dan sampel penjelasan dibedakan secara eksplisit.
- Hubungan 23 prediktor asli dengan 89 input hasil encoding diperjelas.
- Ditambahkan paragraf pembeda desain terhadap studi perbankan dan stabilitas lintas training.
- Versi eksperimen serta lokasi protokol/manifest/CSV dicantumkan.
- Laporan historis 266 checks dibedakan dari audit CSV saat ini dan paket biner yang belum lengkap.
- Angka hasil, tabel, penelitian yang sudah dilakukan, dan batas klaim dipertahankan.

Grafik 5 belum digambar ulang: file pembuat grafik fokus tidak tersedia pada salinan ini. Caption masih menjelaskan bahwa garis antar-background bukan kurva konvergensi. Rentang halaman referensi Shapley juga tidak diubah otomatis karena edisi perlu dicocokkan.

Untuk PDF/Google Docs, terapkan abstrak baru, kejelasan encoding, dan paragraf reproduksibilitas dengan mempertahankan redaksi pengguna lainnya. Belum dibuat ekspor PDF/DOCX dari revisi ini.

## Perbaikan kode dan dokumentasi

- Pipeline baru menolak folder output historis dan memerlukan `TREESHAP_OUTPUT_DIR` terpisah.
- Checkpoint model/SHAP baru memiliki metadata input, konfigurasi, runtime, dan checksum; reuse tanpa provenance ditolak.
- Verifier memakai path berbasis lokasi script, melaporkan artefak hilang sebelum import dependency opsional, menulis laporan baru terpisah, dan tidak mengklaim review visual otomatis.
- README sudah menyatakan XGBoost sebagai model utama dan menunjukkan artefak yang belum ikut tersalin. Petunjuk reproduksi membedakan environment lama dari salinan saat ini.

Laporan historis tidak diubah. Perubahan script sengaja membuat hash script saat ini berbeda dari hash pipeline historis pada manifest; manifest lama tetap menjelaskan eksperimen lama. Jangan memperbarui hash historis hanya agar tampak cocok.
