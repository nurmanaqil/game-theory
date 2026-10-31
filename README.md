# TreeSHAP pada prediksi gagal bayar kartu kredit

Proyek minipaper Teori Game ini membandingkan interventional dan tree-path-dependent TreeSHAP pada enam fitur tagihan BILL_AMT1–BILL_AMT6. Empat classifier digunakan untuk seleksi berdasarkan AP validasi; **XGBoost menjadi model utama**. Random Forest, Extra Trees, dan Gradient Boosting memberikan konteks pendukung.

## Status proyek

Dataset berisi 30.000 observasi dan 23 prediktor asli, direpresentasikan sebagai 89 input setelah encoding. Split tetap: 18.005 training, 5.997 validation, 5.998 test. Fokus enam tagihan adalah fokus atribusi, bukan model enam prediktor.

Analisis memakai 1.000 observasi test, tiga background training berukuran 100 pada seed utama, dan seed training 42/17/73. Peringkat global XGBoost sama pada dua mode, tetapi fitur tagihan teratas berbeda pada 149/1.000 observasi. Test sudah pernah diperiksa; hasil bersifat eksploratif.

Draf aktif: [paper_draft_en.md](kredit/paper/paper_draft_en.md). PDF dan Google Docs dapat memiliki redaksi pengguna yang lebih baru dan tidak otomatis tersinkronisasi.

**Kelengkapan salinan:** CSV, protokol, manifest, dan laporan historis tersedia; model `.joblib`, encoder, serta array `.npz` belum ikut tersedia. Laporan historis 266 checks bukan bukti bahwa verifikasi penuh dapat dijalankan dari salinan ini. Lihat [petunjuk verifikasi](kredit/REPRODUCTION.md).

## Revisi eksperimen 23 Oktober 2026

Eksperimen terbaru membandingkan Random Forest, Extra Trees, Gradient Boosting, dan XGBoost: tiga konfigurasi per keluarga dan tiga seed training. Dua mode TreeSHAP dibandingkan pada sampel 1.000 test tetap. Semua keluarga diuji pada tiga background untuk seed utama, dan satu background untuk dua seed tambahan.

- [Ringkasan hasil revisi dan lima grafik](kredit/experiments/revision_v1/RESULTS.md)
- [Draf aktif fokus enam tagihan](kredit/paper/paper_draft_en.md)
- [Protokol dan amendemen teknis](kredit/experiments/revision_v1/protocol.md)
- [Posisi literatur dan batas akses full text](kredit/experiments/revision_v1/literature_positioning.md)
- [Cara menjalankan eksperimen revisi](kredit/experiments/revision_v1/README.md)

Draf aktif memakai sitasi numerik IEEE dan tetap memerlukan review penulis. Usulan revisi audit tersedia di [paper_draft_revised_en.md](kredit/paper/paper_draft_revised_en.md); Google Docs tidak otomatis diperbarui. Hasil serta panduan konsultasi sebelumnya dipertahankan sebagai catatan tahap awal. Dependency baru dicatat di `kredit/requirements_revision.txt`; unit SHAP probabilitas forest tidak dicampur dengan raw margin boosting.

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

## Audit dan revisi 31 Oktober 2026

- [Usulan revisi paper](kredit/paper/paper_draft_revised_en.md) dan [catatan perubahan](kredit/paper/REVISION-NOTES.md).
- [Audit proyek](kredit/paper/review/PROJECT-AUDIT.md) dan [verifikasi perbaikan](kredit/paper/review/IMPLEMENTATION-VERIFICATION.md).
- Review numerik CSV tidak menggantikan reproduksi model/SHAP atau pemeriksaan plagiarisme dan AI.
