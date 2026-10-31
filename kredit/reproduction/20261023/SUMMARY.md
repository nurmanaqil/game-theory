# Hasil reproduksi tahap pertama

Tanggal: 23 Oktober 2026. Status: **PASS**.

Sebanyak 38 pemeriksaan utama lulus, ditambah fit ulang encoder train-only yang cocok pada train, validation, dan test. Pemeriksaan utama memerlukan 9.50 menit, di luar persiapan environment dan encoder terpisah.

## Hasil

- Raw dan 16 checksum preprocessing sesuai catatan.
- Grouped split, urutan baris, encoding, dan label ketiga partisi cocok.
- Probabilitas validation/test, threshold terpilih, metrik, dan confusion counts cocok.
- Konfigurasi forest terpilih dilatih ulang; probabilitas test cocok dalam toleransi. Waktu fit sekitar 5.58 detik. Seluruh lima kandidat belum dilatih ulang.
- Seluruh 1.000 observasi TreeSHAP dihitung ulang untuk dua mode pada background awal, lalu dua background interventional tambahan. Array SHAP, baseline, dan additivity cocok.
- Ketidaksepakatan fitur teratas kembali 422/1.000, 400/1.000, dan 365/1.000. Spearman kembali 0,7714; 1,0000; 0,8286.
- Seluruh 86 file historis pada raw, processed, artifacts, modeling, dan treeshap tetap sama menurut SHA-256. Artefak baru berada di folder reproduksi.

## Batas pemulihan

Python lokal 3.14.7 menjalankan paket cp314 dari salinan environment lama melalui .pth relatif di .venv_local. Belum instalasi bersih; folder dependency lama tetap diperlukan. Manifest mencatat versi aktual. Encoder direproduksi dengan clone dan fit train-only pada eksekusi terpisah; laporan utamanya tidak mengklaim langkah tambahan itu sebagai bagian proses yang sama.

Belum dilakukan pencarian ulang semua kandidat, audit ulang paper pembanding, model baru, atau eksperimen seed tambahan. Keberhasilan tahap ini memverifikasi fondasi numerik, bukan membuktikan kebaruan maupun kelayakan operasional kredit.

## Target 25 Oktober

Perbandingan empat model dan analisis TreeSHAP terfokus masih masuk akal sebagai sasaran kerja, berdasarkan biaya komputasi forest saat ini. Runtime model lain belum terukur; XGBoost belum terpasang. Sediakan waktu untuk pilot kompatibilitas dan perbedaan satuan raw, pemeriksaan literatur, pembahasan, dan integrasi naskah.

Urutan yang disarankan: 23 Oktober menetapkan protokol revisi; 24 Oktober model/pilot/analisis utama; 25 Oktober pemeriksaan angka, klaim, gambar, referensi, dan naskah. Ini rencana kerja bersyarat, bukan jaminan mutu setara jurnal. Prioritaskan pertanyaan dan bukti yang terkontrol sebelum memperbanyak kombinasi background, seed, atau dataset.
