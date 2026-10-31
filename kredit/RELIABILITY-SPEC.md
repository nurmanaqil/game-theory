# Perbaikan keterlacakan eksperimen

## Batas perubahan

Tidak mengubah data, split, konfigurasi ilmiah, angka hasil, atau laporan historis. Tidak retrain dalam pekerjaan ini. PDF dan Google Docs pengguna tetap menjadi sumber redaksi tersendiri; versi revisi paper dibuat sebagai salinan.

## Persyaratan dan langkah

1. Checkpoint hanya boleh dimuat jika fingerprint data training, konfigurasi, seed, versi runtime, dan hash file cocok. Checkpoint lama tanpa metadata harus ditolak, bukan dianggap valid. Uji dengan file sintetis sebelum integrasi.
2. Jalur verifier ditentukan dari lokasi script. Missing artifacts dilaporkan sebelum model dimuat. Laporan baru tidak menimpa `final_quality_report.json`; status review visual tidak ditulis sebagai hasil otomatis.
3. Pertahankan artefak historis dan pisahkan output eksperimen baru melalui `TREESHAP_OUTPUT_DIR`. Tolak folder hasil historis ketika menjalankan pipeline yang telah diubah.
4. Selaraskan README dengan XGBoost dan sediakan petunjuk environment serta artefak yang belum tersedia.
5. Buat salinan paper dari PDF terbaru dengan abstrak lebih singkat dan tepat, versi dependency, serta batas reproduksi yang jelas. Jangan mengubah angka tabel atau menyatakan pemeriksaan penuh telah dilakukan.

## Verifikasi

Jalankan unittest fingerprint (perubahan data/config/file dan metadata hilang), compile Python, verifier dari luar root proyek pada paket yang tidak lengkap, serta cek bahwa hash laporan historis tidak berubah. Pemeriksaan numerik CSV sudah dicatat terpisah dalam `paper/review/PROJECT-AUDIT-CHECKS.json`.
