# Hasil pemodelan Irfan

## Status

Baseline, perbandingan lima konfigurasi Random Forest, pemilihan threshold validation, dan evaluasi test selesai. Belum menghitung TreeSHAP atau mengulang pelatihan antarseed.

## Model dan aturan yang sudah ditetapkan

- Model: `selected_rf.joblib`, konfigurasi lengkap: `selected_rf_config.json`.
- 300 pohon, max_depth=12, min_samples_leaf=5, class_weight=None, seed=42.
- Pemilihan model berdasarkan average precision validation tertinggi dari lima kandidat.
- Threshold 0.23619742272000907, dipilih berdasarkan F1 validation maksimum. Simpan presisi penuh dari `selected_threshold.json`.
- Model hanya dilatih pada train. Tidak di-refit pada gabungan train dan validation.
- Test sudah dievaluasi. Pertahankan model dan threshold ini; jangan menggunakan hasil test untuk tuning lanjutan.

## Hasil test

ROC-AUC 0.7741, average precision 0.5481. Pada threshold terpilih: accuracy 0.7638, precision 0.4698, recall 0.5770, F1 0.5179; TN=3820, FP=859, FN=558, TP=761.

## Berkas

- `comparison_validation.csv`: tabel pemilihan model.
- `threshold_comparison_validation.csv`: perbandingan threshold validation.
- `threshold_search_validation.csv`: seluruh kandidat threshold validation.
- `predictions_validation.csv`: label dan probabilitas validation.
- `test_metrics.csv`: hasil test pada kedua threshold yang ditetapkan sebelumnya.
- `predictions_test.csv`: metadata, nomor baris test, label, probabilitas, dan keputusan pada kedua threshold.
- `test_evaluation_manifest.json`: checksum, versi lingkungan evaluasi, dan verifikasi.
- `figures/`: confusion matrices dan kurva ROC/precision-recall, PNG dan PDF.
- Naskah paper: `kredit/paper/modeling_evaluation.md`.

## Untuk Yahya

Gunakan model tersimpan yang sama dan observasi yang sama untuk dua mode TreeSHAP. Pertahankan urutan 89 kolom dalam konfigurasi model. Fokus pada kelas 1; dokumentasikan satuan output dan baseline serta periksa additivity. Background interventional hanya dari train. Gunakan feature map Aqil untuk pelaporan fitur asal; keenam BILL_AMT tetap kolom numerik individual. Threshold hanya mengubah keputusan klasifikasi dan bukan fungsi probabilitas yang dijelaskan. TreeSHAP belum dihitung oleh script evaluasi ini.

## Reproduksi

Jalankan `python kredit/evaluate_model.py` dari root proyek dengan lingkungan yang kompatibel. Script ini hanya memuat model dan memprediksi test, tanpa fit. Versi lingkungan evaluasi ada pada manifest; versi lingkungan training asli belum direkam otomatis oleh `train_model.py`. Tidak ada klaim bahwa lingkungan training dan evaluasi pasti identik.
