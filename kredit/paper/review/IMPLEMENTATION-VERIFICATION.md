# Verifikasi perbaikan 31 Oktober 2026

## Diterapkan

- `checkpoint_integrity.py`: fingerprint input/config/runtime dan checksum checkpoint, divalidasi sebelum deserialisasi model atau pemuatan array.
- `run_revision_experiments.py`: sidecar provenance model/array baru dan pemisahan output lewat `TREESHAP_OUTPUT_DIR`; folder historis/default ditolak.
- `verify_revision_results.py`: path relatif script, preflight artefak, laporan baru terpisah, status visual `NOT_PERFORMED` pada pemeriksaan otomatis yang selesai.
- README dan petunjuk reproduksi: fokus XGBoost, keterbatasan salinan, serta pemisahan workflow lama/baru.
- `../paper_draft_revised_en.md`: revisi terpisah berbasis MD lokal. Lihat `../REVISION-NOTES.md` sebelum menerapkan ke PDF atau Google Docs terbaru.

## Hasil pemeriksaan yang dijalankan

1. Enam unittest lulus: menerima checkpoint utuh; menolak metadata hilang, perubahan data, konfigurasi, runtime, dan isi checkpoint. Tes memakai file sintetis tanpa deserialisasi model.
2. Compile tiga modul Python yang diubah/ditambahkan lulus.
3. Verifier dipanggil dari folder `paper/`, menghasilkan exit 2 / `INCOMPLETE` dengan 45 path model/array wajib yang hilang. Ini perilaku yang diharapkan, bukan verifikasi numerik penuh yang gagal.
4. SHA-256 `final_quality_report.json` sama sebelum dan sesudah verifier berjalan.
5. Pemanggilan pipeline dengan output default ditolak sebelum pelatihan berjalan.
6. Seluruh tautan gambar pada salinan revisi Markdown dapat ditemukan; abstrak berjumlah 169 kata.

Tidak ada retraining, rekalkulasi SHAP, clean install dependency, atau uji resume model riset secara penuh. Paket biner belum tersedia dan runtime eksperimen tidak direkonstruksi. Pemeriksaan CSV terdahulu tetap terpisah pada `PROJECT-AUDIT-CHECKS.json`; angka paper tidak diganti.

Manifest lama mencatat hash script lama. Hash pipeline sekarang berbeda karena kode diperbaiki; manifest historis sengaja tidak diperbarui. Eksperimen baru harus memiliki manifest baru pada direktori output tersendiri.
