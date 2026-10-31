# Catatan evaluasi draf paper

Catatan historis sebelum revisi fokus enam fitur. Untuk versi saat ini, gunakan [six_billing_revision_notes.md](six_billing_revision_notes.md); identitas penulis dan gaya IEEE sudah diterapkan, dan hasil keluarga model lain dipindahkan ke lampiran.

Draf utama: [paper_draft_en.md](paper_draft_en.md). Disusun 23 Oktober 2026 dari eksperimen yang sudah selesai, bukan dari rencana pengembangan UAS. Draf ini berdiri sendiri; naskah lama, Google Docs, dan dokumen konsultasi tidak ditimpa.

## Bagian yang perlu dievaluasi penulis

1. **Fokus dan judul.** Paper berfokus pada sensitivitas dua mode TreeSHAP, hubungan ranking global dengan penjelasan individual, serta analisis margin dan magnitudo. Penambahan empat model menjadi bagian desain pembanding, bukan klaim utama kebaruan.
2. **Kontribusi.** Apakah fokus empiris tersebut sesuai kesepakatan dengan dosen? Draf tidak mengklaim pertama menggunakan TreeSHAP, pertama membandingkan dua mode, atau lebih unggul dari semua paper 2025.
3. **Hasil utama.** Perhatikan Tabel 4–5: frekuensi pergantian fitur teratas berbeda dari besar perubahan atribusi. Persentase setelah filter margin memiliki denominator baru dan tidak boleh dibaca sebagai hasil pada seluruh 1.000 observasi.
4. **Status evaluasi.** Test sudah pernah dilihat pada tahap sebelumnya. Paper menyatakan eksperimen eksploratif, bukan evaluasi konfirmatori dengan test baru. Dataset tetap sama sesuai keputusan penelitian.
5. **Bahasa dan format tujuan.** Draf menggunakan bahasa Inggris dan struktur paper umum. Nama penulis, afiliasi, email, serta gaya jurnal belum ditambahkan karena perlu identitas dan format tujuan yang disepakati.

## Catatan literatur sebelum pengumpulan

Metadata, abstrak, dan bagian sumber yang tersedia digunakan sesuai catatan audit lokal. Full text García-Céspedes dkk. (2025) belum berhasil diaudit secara lengkap. Jangan menyatakan perbedaan dataset atau rincian eksperimennya sebagai fakta pembeda tanpa pemeriksaan sumber primer tersebut. Pernyataan bahwa kontribusi kita belum pernah diteliti juga belum dapat dibuat dari cakupan audit sekarang.

Paper Lin–Wang berbeda dari paper García-Céspedes dkk. Lin–Wang menggunakan 100 model XGBoost pada dataset yang sama, sedangkan eksperimen kita baru tiga seed. Empat keluarga model memperluas dimensi pembanding, tetapi tidak otomatis mengungguli luas replikasi penelitian tersebut.

## Pemeriksaan yang telah dilakukan

- Lima tabel hasil dibentuk langsung dari `predictive_metrics.csv` dan `attribution_summary.csv`; dua tabel lainnya memuat protokol dataset dan model.
- Enam tautan grafik lokal ada dan dapat ditelusuri.
- Penomoran tabel, grafik, dan daftar referensi diperiksa.
- Pemeriksaan eksperimen sebelumnya lulus 266 cek; laporan ini tidak menggantikan validasi ilmiah desain.
- Hasil eksperimen korelasi terkontrol, dataset kedua, pengujian ukuran background, dan pengulangan seed lebih banyak tidak dinyatakan sudah dilakukan.

Laporan struktur draf: [paper_draft_validation.json](paper_draft_validation.json). Sumber hasil lengkap: [RESULTS.md](../experiments/revision_v1/RESULTS.md).
