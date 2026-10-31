# TreeSHAP pada prediksi gagal bayar kartu kredit

Proyek paper Teori Game ini membandingkan mode interventional dan tree-path-dependent pada TreeSHAP untuk melihat pembagian atribusi enam fitur tagihan yang berkorelasi, BILL_AMT1–BILL_AMT6. Kedua mode menjelaskan model Random Forest dan observasi yang sama. Hasil membahas perilaku model, bukan penyebab gagal bayar.

## Status proyek

Audit, preprocessing, pemodelan, evaluasi test, eksperimen TreeSHAP utama, dan pemeriksaan sensitivitas background sudah memiliki hasil tersimpan. Dataset berisi 30.000 observasi dan 23 prediktor asal. Split berisi 18.005 train, 5.997 validation, dan 5.998 test; encoding menghasilkan 89 kolom.

Model terpilih menggunakan 300 pohon, max_depth=12, min_samples_leaf=5, dan seed 42. Threshold dipilih dari validation. Analisis TreeSHAP menggunakan 1.000 observasi test dan tiga background train berukuran 100. Pengulangan pelatihan antarseed belum dilakukan.

## Revisi eksperimen 23 Oktober 2026

Eksperimen terbaru membandingkan Random Forest, Extra Trees, Gradient Boosting, dan XGBoost: tiga konfigurasi per keluarga dan tiga seed training. Dua mode TreeSHAP dibandingkan pada sampel 1.000 test tetap. Semua keluarga diuji pada tiga background untuk seed utama, dan satu background untuk dua seed tambahan.

- [Ringkasan hasil revisi dan lima grafik](kredit/experiments/revision_v1/RESULTS.md)
- [Draf naskah lengkap revisi](kredit/paper/manuscript_revision_en.md)
- [Protokol dan amendemen teknis](kredit/experiments/revision_v1/protocol.md)
- [Posisi literatur dan batas akses full text](kredit/experiments/revision_v1/literature_positioning.md)
- [Cara menjalankan eksperimen revisi](kredit/experiments/revision_v1/README.md)

Draf naskah masih memerlukan review penulis dan penyatuan gaya sitasi; Google Docs belum diubah. Hasil serta panduan konsultasi sebelumnya dipertahankan sebagai catatan tahap awal. Dependency baru dicatat di `kredit/requirements_revision.txt`; unit SHAP probabilitas forest tidak dicampur dengan raw margin boosting.

## Struktur folder

| Lokasi | Isi |
|---|---|
| Dokumen Markdown di root | Briefing, rencana penelitian, rumusan masalah, dan panduan literatur |
| [references.bib](references.bib) | Referensi BibTeX |
| `kredit/` | Script dan notebook pipeline |
| `kredit/raw/` dan `kredit/audit/` | Snapshot raw, manifest, dan hasil audit |
| `kredit/processed/` dan `kredit/artifacts/` | Split semantic/encoded, metadata, preprocessor, dan feature map |
| `kredit/modeling/` | Model terpilih, threshold, prediksi, metrik, dan gambar |
| `kredit/treeshap/` | Pilot, eksperimen utama, analisis, dan sensitivitas background |
| `kredit/paper/` | Draf bagian paper terbaru, tabel, dan gambar |
| `kredit/archive/` dan `kredit/paper/archive/` | Script dan draf versi lama |
| `output/pdf/` | PDF bagian paper yang sudah dihasilkan |
| `research_notes/` | Transkripsi dan catatan referensi |
| `tmp/` | Berkas sementara dan helper rendering |
| `.tools/`, `.models/`, `kredit/.analysis_deps/`, `kredit/.venv/` | Dependency dan runtime yang ikut dipindahkan dari laptop lama |

## Bahan paper terbaru

- [Dataset dan preprocessing](kredit/paper/dataset_preprocessing.md)
- [Pemodelan dan evaluasi](kredit/paper/modeling_evaluation.md)
- [Hasil TreeSHAP](kredit/paper/treeshap_results.md)
- [Protokol eksperimen utama](kredit/treeshap/experiment_protocol.md)
- [Handoff pemodelan](kredit/modeling/modeling_handoff.md)

`kredit/paper/archive/dataset_preprocessing_legacy.md` adalah draf awal dengan sitasi D1–D5. Versi aktif menggunakan sitasi [7] dan [10]–[13]. Generator preprocessing tetap menghasilkan draf awal ke folder arsip agar tidak menimpa versi aktif.

Dokumen audit dan panduan preprocessing menjelaskan status pada tahap pembuatannya. Pernyataan “belum melatih model” dalam dokumen tersebut bukan status keseluruhan proyek saat ini. Rencana sintetis dan pengulangan model dalam dokumen riset merupakan rencana pengembangan, bukan hasil yang telah tersedia.

## Urutan pipeline

Jalankan perintah berikut dari root proyek hanya jika memang ingin menghasilkan ulang output tahap terkait. Beberapa script menulis ulang hasil pada lokasi yang sama; training juga mengganti model terpilih.

| Urutan | Perintah | Fungsi |
|---|---|---|
| 1 | `python kredit/audit_dataset.py` | Audit dan dokumentasi dataset |
| 2 | `python kredit/preprocess_dataset.py` | Recoding, grouped split, encoding, dan hasil preprocessing |
| 3 | `python kredit/train_model.py` | Melatih dan memilih model berdasarkan validation |
| 4 | `python kredit/select_threshold.py` | Memilih threshold berdasarkan F1 validation |
| 5 | `python kredit/evaluate_model.py` | Mengevaluasi model pada test |
| 6 | `python kredit/check_model.py` | Memeriksa checksum, urutan fitur, dan kesesuaian prediksi |
| 7 | `python kredit/run_treeshap_pilot.py` | Pilot teknis pada 20 observasi |
| 8 | `python kredit/run_treeshap_main.py` | Perbandingan utama pada 1.000 observasi |
| 9 | `python kredit/analyze_treeshap.py` | Analisis atribusi berpasangan dan gambar |
| 10 | `python kredit/check_background_sensitivity.py` | Pemeriksaan dua background tambahan |

Notebook pendamping: [audit](kredit/01_dataset_audit.ipynb) dan [preprocessing](kredit/02_preprocessing.ipynb). Script di `kredit/archive/` adalah versi historis dan tidak termasuk pipeline aktif.

## Lingkungan setelah pemindahan

Executable virtual environment lama masih menunjuk ke `C:\Python314\python.exe`. Lingkungan pengganti `kredit/.venv_local/` sudah dibuat dengan Python lokal 3.14.7 dan membaca dependency cp314 yang ikut tersalin melalui `.pth` relatif. Ini belum merupakan instalasi bersih. Petunjuk dan cakupan verifikasi tersedia di [REPRODUCTION.md](kredit/REPRODUCTION.md); laporan eksekusi berada di `kredit/reproduction/20261023/`.

Requirements yang tersedia adalah `kredit/requirements_preprocessing.txt` dan `kredit/requirements_sebelum_shap.txt`. Keduanya belum mencakup SHAP secara lengkap. Manifest TreeSHAP mencatat Python 3.14.4, SHAP 0.54.1, dan scikit-learn 1.7.2; manifest preprocessing mencatat Python 3.12.14. Gunakan manifest tiap tahap sebagai catatan lingkungan historis.

## Konvensi dan arsip

Nama kode dan dokumen menggunakan huruf kecil dengan snake_case. Nama dataset dan artefak hasil dipertahankan agar cocok dengan konfigurasi, checksum, dan pemanggilan kode. PDF hanya diganti nama; isinya tidak dirender ulang. `kredit/Paket_Aqil_untuk_Irfan.zip` dipertahankan sebagai snapshot handoff lama dan masih memuat struktur sebelum rename; generator akan memakai nama baru saat paket dibuat ulang.

Google Docs merupakan naskah bersama. Rename lokal tidak mengubah Google Docs; hasil TreeSHAP lokal belum dimasukkan ke dokumen bersama pada pemeriksaan terakhir.
