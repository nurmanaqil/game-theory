# Aturan eksperimen utama TreeSHAP

Aturan ditetapkan setelah pilot teknis, sebelum menjalankan perhitungan utama.

- Model tetap: model Irfan yang checksum-nya disimpan pada pemeriksaan lingkungan. Tidak melakukan fit atau tuning.
- Sampel evaluasi: 1.000 dari 5.998 baris test, sampling acak tanpa pengembalian dengan NumPy default_rng seed 20261022. Pemilihan tidak memakai label, probabilitas, ranking, atau perbedaan SHAP.
- Background interventional: 100 baris train, sampling acak tanpa pengembalian dengan seed 20261021. Sampel ini sama dengan pilot.
- Kedua mode menggunakan model, observasi, kelas 1, dan satuan probabilitas yang sama. tree_path_dependent memakai informasi jalur pelatihan dalam model tanpa background tambahan.
- model_output='raw' untuk kedua mode. Untuk RandomForestClassifier ini output pohon berupa probabilitas, diverifikasi dengan rekonstruksi predict_proba seluruh kelas.
- Perhitungan exact sesuai permainan tiap mode: approximate=False. Additivity diperiksa dengan toleransi absolut 1e-6.
- Simpan seluruh 89 atribusi kelas 1, baseline, probabilitas, serta membership sampel dan background.
- Fokus perbandingan: enam BILL_AMT, perbedaan signed berpasangan, rata-rata selisih absolut, ranking mean(abs(SHAP)) enam fitur, kesepakatan fitur tagihan teratas per nasabah berdasarkan abs(SHAP), dan jumlah signed atribusi kelompok tagihan. Aturan tie harus dijelaskan dalam tahap analisis.
- Agregat signed kelompok tidak disebut Shapley dari permainan pemain gabungan.
- Baseline dua mode boleh berbeda. Perbedaan atribusi diamati dalam keseluruhan pengaturan penjelasan, bukan bukti efek kausal korelasi atau kesalahan suatu mode.
- Pilot 20 baris bukan sampel konfirmasi independen dari eksperimen utama; overlap sampel dapat terjadi.
- Batas awal: satu fitted model (seed 42), satu background 100 baris, dan satu sampel evaluasi. Belum ada kesimpulan ketahanan terhadap seed model atau variasi background. Analisis background tambahan dapat memperkuat interpretasi dan harus dilaporkan terpisah.

Output utama: kredit/treeshap/main/. Tidak menimpa hasil pilot atau hasil pemodelan Irfan.
