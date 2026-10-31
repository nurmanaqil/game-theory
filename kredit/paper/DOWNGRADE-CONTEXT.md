# Konteks penyederhanaan paper menjadi minipaper

Tanggal: 31 Oktober 2026.

## Arti dan status downgrade

Dokumen ini memakai istilah **downgrade sebagai penyederhanaan cakupan dan penyajian paper untuk minipaper**, berdasarkan konteks percakapan. Jika yang dimaksud adalah penurunan versi Python, library, atau model, perubahan tersebut **belum dilakukan**.

Status penyederhanaan paper: **sebagian sudah dilakukan, belum menjadi pemangkasan menyeluruh**. Jangan menyebut PDF terbaru sudah dipersingkat atau seluruh revisi sudah diterapkan ke Google Docs.

## Yang sudah dilakukan

1. Fokus penelitian telah dipersempit pada sensitivitas atribusi BILL_AMT1–BILL_AMT6. Catatan fokus awal tersedia di [six_billing_revision_notes.md](six_billing_revision_notes.md), bertanggal 23 Oktober 2026; penyempitan ini sudah ada sebelum audit terakhir.
2. Empat classifier tetap digunakan untuk seleksi berdasarkan AP validasi. XGBoost menjadi objek analisis utama; keluarga lain hanya konteks pendukung, bukan empat tujuan penelitian yang sama besar.
3. PAY_AMT tidak menjadi pembahasan utama. Outputnya tetap disimpan sebagai hasil eksplorasi.
4. Dalam [salinan revisi 31 Oktober](paper_draft_revised_en.md), abstrak dipadatkan menjadi 169 kata, hubungan 23 prediktor dengan 89 input diperjelas, dan kontribusi diposisikan sebagai studi kasus eksploratif.
5. Klaim dibatasi sesuai bukti: tidak mengklaim algoritme baru, penyebab kausal korelasi, mode SHAP paling benar, atau generalisasi populasi.

## Yang tidak diturunkan atau dihapus

- Seluruh 23 prediktor asli tetap digunakan model, menjadi 89 input setelah encoding. Enam fitur merupakan fokus analisis, bukan pengurangan input pelatihan.
- Dataset, pembagian train/validation/test, konfigurasi terpilih, jumlah pohon, serta angka hasil tetap sama.
- Analisis 1.000 observasi, tiga background pada seed utama, dan tiga seed pelatihan tidak dibatalkan.
- Versi dependency tidak diubah; tidak ada instalasi ulang atau retraining.
- Hasil eksperimen dan laporan historis tidak dihapus untuk membuat penelitian terlihat lebih sederhana.

## Yang belum dilakukan

- Pemangkasan seluruh isi menjadi naskah singkat dengan batas halaman tertentu. Rubrik/batas halaman dosen belum tersedia.
- Pengurangan delapan tabel atau lima gambar secara menyeluruh. Salinan revisi masih mempertahankan struktur dan tabel utama sumber MD.
- Sinkronisasi ke PDF atau Google Docs. Salinan revisi bersumber dari MD lokal; PDF memuat redaksi pengguna yang perlu dibandingkan sebelum diganti.
- Ekspor PDF/DOCX baru dari salinan revisi.

## Arah penyederhanaan berikutnya

Jika minipaper harus lebih singkat, pertahankan tujuan penelitian, ringkasan split dan encoding, konfigurasi dua mode, hasil utama, keterbatasan, dan referensi yang benar-benar digunakan. Padatkan pengulangan angka serta kualifikasi; pindahkan rincian kandidat model dan hasil keluarga pendukung ke lampiran. Metode minimum yang dibutuhkan untuk memahami hasil tidak boleh dihapus.

Temuan inti yang harus tetap jelas: ranking global sama, tetapi leading billing feature berbeda pada 149/1.000 observasi; setelah kedua margin >0,05, disagreement terdapat pada 60/764 observasi. Kedua persentase memakai denominator berbeda dan bukan ukuran error prediksi.

## Bahan pengembangan UAS

- Replikasi training dan background yang lebih luas serta variasi ukuran background.
- Eksperimen sintetis dengan dependensi yang dikendalikan.
- Evaluasi pada data baru yang belum diperiksa sebelumnya.
- Analisis perpindahan fitur teratas, perubahan tanda, dan contoh individual.
- Grouped-player Shapley sebagai pertanyaan tambahan yang berbeda dari menjumlahkan atribusi fitur saat ini.

Semua butir pengembangan tersebut merupakan rencana, bukan hasil yang boleh ditulis seolah telah dijalankan. Penyederhanaan minipaper tidak mengubah standar atribusi sumber atau membuktikan bahwa naskah bebas plagiarisme maupun ditulis tanpa AI.
