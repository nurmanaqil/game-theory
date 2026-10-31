# Protokol revisi eksperimen v1

Ditetapkan 23 Oktober 2026 sebelum melihat hasil eksperimen revisi. Ini studi pengembangan setelah test lama pernah diperiksa, bukan evaluasi konfirmasi pada test yang belum disentuh. Artefak historis tidak ditimpa.

## Pertanyaan dan cakupan

1. Bagaimana perbedaan interventional dan tree-path-dependent muncul pada empat keluarga model pohon?
2. Apakah pergantian fitur tagihan teratas didominasi kasus hampir seri atau disertai perbedaan magnitudo?
3. Bagaimana pola berubah pada tiga background dan tiga seed training yang telah ditentukan?

Dataset, semantic recoding, 89 kolom encoded, dan grouped split lama dipertahankan. Tidak menyeleksi fitur menggunakan test. Analisis utama BILL_AMT1-6, analisis pendukung PAY_AMT1-6 dan importance 23 fitur asal. Korelasi kelompok hanya dihitung dari train. Tidak mengklaim efek kausal korelasi.

## Training dan seleksi

Empat keluarga: RandomForestClassifier, ExtraTreesClassifier, GradientBoostingClassifier, XGBClassifier. Tiga kandidat per keluarga; ini anggaran jumlah konfigurasi yang sama, bukan anggaran waktu atau bukti optimum. RF sebelumnya memiliki pencarian historis lebih banyak; seleksi revisi hanya mengikuti kandidat di bawah. Semua tanpa class resampling atau pembobotan kelas. Encoder dan split tetap. Seed seleksi 42.

- RF: 300 pohon, min_samples_leaf=5, max_depth 8/12/None; sqrt feature sampling, bootstrap=True.
- Extra Trees: 300 pohon, min_samples_leaf=5, max_depth 8/12/None; sqrt feature sampling, bootstrap=False.
- Gradient Boosting: 200 pohon, learning_rate=0.05, min_samples_leaf=5, max_depth 2/3/4, subsample=1.
- XGBoost: 300 pohon, learning_rate=0.05, max_depth 2/3/4; subsample=0.8, colsample_bytree=0.8, reg_lambda=1; objective=binary:logistic, tree_method=hist, CPU n_jobs=2.

Pilih AP validation tertinggi per keluarga; tie persis memilih kandidat pertama (kapasitas lebih rendah). Threshold setiap model dari F1 validation maksimum; tie threshold lebih tinggi. Ranking keluarga dari AP validation, bukan test. Model tidak refit gabungan train+validation. Test dilaporkan setelah seleksi untuk evaluasi deskriptif lanjutan.

## TreeSHAP dan variasi

Gunakan 1.000 test dan background train yang persis sama dengan sampel lama. TreeExplainer approximate=False, raw, kelas 1 jika output multikelas. Raw forest diverifikasi terhadap predict_proba; raw boosting terhadap decision_function/output_margin. Additivity rtol=0 atol=1e-6. Simpan seluruh SHAP serta membership.

Seed training 42, 17, 73. Seed 42: tiga background 20261021/20261023/20261024, masing-masing 100 train, dan satu hasil path tetap. Seed tambahan: parameter terpilih dibekukan tanpa tuning ulang, background 20261021, observasi tetap. Jalankan pilot 20 observasi sebelum penjelasan utama tiap model. Ukuran background tetap; bukan eksperimen pengaruh ukuran.

## Ukuran analisis

Per kelompok enam fitur: mean abs SHAP, selisih signed dan abs berpasangan, Spearman/Kendall ranking, fitur teratas berdasarkan abs. Tie abs<=1e-12 di salah satu mode dikeluarkan dari denominator top agreement. Laporkan n valid.

Margin pemenang lokal = (a1-a2)/(a1+a2) untuk dua atribusi absolut terbesar. Jika penyebut <=1e-12, margin nol. Laporkan ketidaksepakatan tanpa syarat dan pada kedua margin >0.01, >0.05, >0.10; denominator masing-masing dilaporkan. Tidak memilih ambang terbaik setelah melihat hasil.

Magnitudo raw dilaporkan dalam unit model masing-masing. Indeks L1 relatif = mean sum abs(delta) / mean abs(raw_output - baseline_path), penyebut tetap per fitted model. Jika penyebut <=1e-12, indeks tidak terdefinisi. Indeks bukan jaminan invariansi terhadap transformasi link; lintas model tetap interpretasi deskriptif. Grup signed bukan Shapley pemain gabungan. Global source importance: jumlah signed indikator per source variable sebelum mean abs.

## Batas klaim

Tiga seed adalah sensitivitas deskriptif terbatas, bukan generalisasi populasi model. Tidak memakai p-value. Tidak menyatakan salah satu mode lebih benar, dataset baru, algoritme baru, atau hasil melampaui paper pembanding. Output lama/MD konsultasi/PDF lama tidak diubah. Protokol, manifest, tabel dan draf hasil revisi lokal menjadi sumber integrasi berikutnya; Google Docs belum diubah.

Catatan eksekusi: dua background tambahan RF seed 42 memakai kembali NPZ historis yang sudah direproduksi pada tahap pertama, setelah parameter dan probabilitas seluruh validation/test dipastikan identik dengan fitted model revisi. Provenance disimpan di reuse_provenance.json. Pilihan eksperimen tidak berubah.


Amendemen teknis sebelum analisis hasil XGBoost: pilot 300 pohon menghasilkan error raw margin sekitar 1,2-1,9e-6 pada 20 observasi. Toleransi XGBoost menjadi absolut 1e-5 (prediksi native float32); keluarga lain tetap 1e-6. Error aktual setiap pilot dicatat. Pilot ini dipakai untuk memeriksa implementasi, bukan memilih model/hasil atribusi.
