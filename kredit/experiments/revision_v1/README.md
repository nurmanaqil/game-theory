# Hasil historis revision_v1

Folder ini menyimpan hasil eksperimen 23 Oktober 2026. Pipeline yang diperbaiki pada 31 Oktober tidak boleh menulis ulang folder ini. Untuk output baru dan aturan checkpoint, ikuti [REPRODUCTION.md](../../REPRODUCTION.md). Perintah eksekusi dan helper di bawah merupakan catatan workflow historis, bukan petunjuk menjalankan pipeline baru pada folder ini.

Laporan numerik baru: `verification_report_current.json`. Laporan historis: `final_quality_report.json`. Salinan proyek saat ini belum menyertakan model/encoder joblib dan array NPZ; status historis PASS tidak berarti paket ini lengkap.

# Menjalankan eksperimen revisi

Semua output berada di folder ini. Dataset dan split tetap; output historis di luar folder ini tidak ditimpa. Status selesai diverifikasi oleh manifest.json, analysis_checks.json, dan final_quality_report.json: semuanya PASS. Pemeriksaan akhir mencakup 266 pemeriksaan numerik/skema/tautan.

## Berkas utama

- protocol.md: pertanyaan, kandidat, aturan seleksi, seed/background, metrik, dan amendemen toleransi teknis.
- literature_positioning.md: perbandingan sumber literatur dan batas akses full text.
- RESULTS.md: ringkasan hasil dalam bahasa Indonesia (dibuat setelah eksperimen lengkap).
- paper_methods_results_en.md: draf bagian metode/hasil untuk integrasi naskah.
- figures/: gambar PNG/PDF; grafik menyatakan unit per keluarga.
- manifest.json, analysis_checks.json: pemeriksaan penyelesaian dan integritas.

## Perintah dari root proyek

```powershell
& .\kredit\.venv_local\Scripts\python.exe -u .\kredit\run_revision_experiments.py
& .\kredit\.venv_local\Scripts\python.exe .\kredit\analyze_revision_experiments.py
& .\kredit\.venv_local\Scripts\python.exe .\kredit\write_revision_sections.py
```

Untuk eksekusi paralel, jalankan script pertama empat kali dengan argumen random_forest, extra_trees, gradient_boosting, atau xgboost. Masing-masing menulis worker_tables dan family_manifest dalam folder keluarga yang berbeda. Setelah semuanya selesai, jalankan merge_revision_experiments.py, kemudian dua script analisis/naskah di atas. Jangan menjalankan mode sekuensial dan paralel bersamaan pada folder yang sama.

Checkpoint model dan SHAP disimpan untuk melanjutkan pekerjaan. Eksekusi ulang memuat checkpoint dan membentuk ulang tabel; waktu fit_or_load mencampur operasi load dan fit dan tidak boleh dipakai untuk mengklaim keunggulan runtime algoritme. Catatan waktu training kandidat awal ada di prefit_timing.json. Dua background RF seed 42 memakai hasil yang telah direproduksi; sumbernya dicatat di reuse_provenance.json.

Dependency baru XGBoost 3.4.1 ada di kredit/.extension_deps dan diprioritaskan melalui sys.path oleh script eksperimen. Paket inti tetap berasal dari environment lokal yang dijelaskan di kredit/REPRODUCTION.md. Requirements keseluruhan ada di kredit/requirements_revision.txt; instalasi bersih semua versi belum diuji.

Tabel per-observasi serta seluruh model/NPZ berada di <keluarga>/seed_<seed>/. Threshold berasal dari validation untuk setiap fitted model. Test sudah pernah dibaca dalam proyek awal; ini analisis pengembangan eksploratif. Panduan konsultasi historis dan Google Docs tidak otomatis disinkronkan.

Pemeriksaan numerik akhir dapat diulang dengan `kredit/verify_revision_results.py`. Folder menyimpan log upaya awal/interupsi dan metadata_serialization_repair.json: helper sempat menyimpan nama kolom sebagai object dtype; diperbaiki menjadi Unicode tanpa mengubah array SHAP numerik. Hanya laporan final yang berstatus PASS menjadi bukti penyelesaian.
