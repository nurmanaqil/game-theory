# Catatan revisi fokus enam fitur tagihan

Revisi 23 Oktober 2026. Catatan ini menggantikan arahan editorial lama di paper_review_notes.md untuk versi paper saat ini.

## Alur yang digunakan

1. BILL_AMT1-BILL_AMT6 menjadi objek penelitian atribusi.
2. Empat model dibandingkan berdasarkan AP validasi untuk memilih fungsi prediksi yang akan dijelaskan. XGBoost terpilih; perbandingan model bukan tujuan akhir penelitian.
3. Model menggunakan seluruh 23 prediktor setelah encoding menjadi 89 input. TreeSHAP dihitung untuk semua input, kemudian enam atribusi tagihan ditelaah. Ini bukan model enam prediktor atau permainan Shapley dengan satu pemain gabungan tagihan.
4. Hasil utama membahas tiap fitur, ranking global, fitur teratas per nasabah, margin, magnitudo, background, dan tiga seed XGBoost.
5. Konfigurasi model dan atribusi keluarga lain menjadi lampiran. Hasil PAY_AMT tetap tersimpan dalam output eksperimen, tetapi tidak menjadi pembahasan utama.

## Temuan utama

- Ranking global sama antarmode, tetapi fitur tagihan teratas berbeda pada 149 dari 1.000 nasabah.
- Dengan margin kedua mode > 0,05: 60 dari 764 nasabah (7,85%). Denominator berbeda; ini bukan penurunan error prediksi.
- BILL_AMT1 memiliki rata-rata atribusi absolut terbesar; BILL_AMT4 memiliki rata-rata perubahan absolut berpasangan terbesar. Kedua ukuran menjawab pertanyaan berbeda.
- Atribusi XGBoost menggunakan log-odds, bukan persentase probabilitas.

## Format dan batas klaim

Nama dan NIM keempat penulis sudah dicocokkan dengan spreadsheet Kelompok Teori Game A 2026, Sheet1 baris 21-24. Sitasi mengikuti urutan kemunculan IEEE. PDF satu kolom, Times New Roman 12 pt, spasi isi 1,5; bukan klaim mengikuti seluruh template konferensi IEEE. Afiliasi dan email tidak dikarang.

Test pernah dilihat; evaluasi eksploratif. Korelasi tidak dimanipulasi, sehingga tidak ada klaim kausal. Tiga seed dan tiga background berukuran 100 tidak membuktikan kestabilan populasi atau konvergensi. Full text García-Céspedes dkk. belum diaudit lengkap; tidak ada klaim penelitian pertama. Lin-Wang memiliki 100 seed XGBoost; tiga seed kita tidak mengungguli luas replikasinya.

Revisi memakai hasil yang sudah tersedia dan tidak melatih ulang model. Naskah lama tersimpan di [archive/paper_draft_en_before_six_billing_focus.md](archive/paper_draft_en_before_six_billing_focus.md). Dokumen konsultasi dan Google Docs tidak diubah. Laporan struktur ada di [paper_focus_validation.json](paper_focus_validation.json).
