# Handoff penelitian TreeSHAP dan paper

Disusun 31 Oktober 2026. Dokumen ini memberi konteks kepada GPT atau agen berikutnya. Baca permintaan terbaru pengguna sebelum bertindak; daftar pekerjaan di bawah bukan izin untuk mengubah semua hal sekaligus.

## 1. Tujuan dan keputusan pengguna

Proyek merupakan paper kelompok mata kuliah Teori Game, mengenai atribusi Shapley pada model machine learning. Fokus yang sudah disepakati adalah **sensitivitas dua mode TreeSHAP terhadap enam fitur tagihan BILL_AMT1-BILL_AMT6** pada dataset kredit Taiwan. Pengguna ingin memahami metode, memiliki paper yang layak dievaluasi dosen, dan dapat mengembangkan eksperimen sampai UAS.

Pertanyaan utama: pada model prediksi yang sama dan nasabah yang sama, apakah interventional dan tree-path-dependent TreeSHAP membagi kontribusi secara berbeda pada enam fitur tagihan?

Keputusan yang harus dipertahankan:

- Dataset tetap UCI Default of Credit Card Clients. Jangan mengganti dataset tanpa instruksi.
- Model tetap menggunakan seluruh 23 prediktor asli, menjadi 89 kolom setelah encoding. Fokus enam fitur adalah fokus analisis atribusi, bukan instruksi melatih model hanya dengan enam prediktor.
- Empat model dibandingkan untuk memilih model utama. XGBoost terpilih berdasarkan AP validasi tertinggi. Perbandingan model **bukan pusat kontribusi paper**.
- Hasil TreeSHAP XGBoost menjadi analisis utama. Model lain menjadi konteks pendukung dalam lampiran.
- PAY_AMT tidak menjadi fokus utama paper terbaru. Hasilnya tetap tersimpan.
- Bahasa paper Inggris; komunikasi kepada pengguna Bahasa Indonesia yang mudah dipahami.
- Sitasi dan referensi IEEE, berurutan berdasarkan kemunculan pertama.
- Format awal satu kolom TNR 12 pt dan spasi 1,5 kemudian digantikan **untuk versi Google Docs IEEE** oleh template konferensi A4 pengguna: isi TNR 10 pt, dua kolom. Jangan mencampur dua versi format tersebut.
- Afiliasi dan email akan diisi pengguna sendiri. Jangan mengarang atau meminta ulang informasi tersebut.

Judul paper terbaru: **Sensitivity of TreeSHAP Attributions for Six Correlated Billing Features in Credit Default Prediction**.

## 2. Lokasi workspace dan dokumen utama

Workspace Windows PowerShell:

`D:\Kuliah\Semester 5\Game Theory\Project Paper`

| Artefak | Lokasi relatif workspace | Status |
| --- | --- | --- |
| Draf MD lokal terbaru | `kredit/paper/paper_draft_en.md` | Fokus enam fitur, sekitar 4.899 kata, 8 tabel, 5 grafik, 6 rumus, 11 referensi |
| PDF lokal satu kolom | `output/pdf/paper_draft_en.pdf` | 16 halaman saat terakhir dirender; TNR 12 pt |
| DOCX lokal satu kolom | `output/docx/paper_draft_en.docx` | Dibuat dari MD; bukan versi template dua kolom |
| Catatan revisi fokus | `kredit/paper/six_billing_revision_notes.md` | Keputusan dan batas klaim |
| Validasi fokus | `kredit/paper/paper_focus_validation.json` | Struktur, referensi, angka utama |
| Hasil lengkap eksperimen | `kredit/experiments/revision_v1/RESULTS.md` | Sumber hasil komputasi |
| Protokol | `kredit/experiments/revision_v1/protocol.md` | Rancangan dan amendment |
| Posisi literatur | `kredit/experiments/revision_v1/literature_positioning.md` | Membedakan dua paper 2025 |
| Pemeriksaan eksperimen | `kredit/experiments/revision_v1/final_quality_report.json` | PASS, 266 pemeriksaan konsistensi |
| Reproduksi hasil awal | `kredit/reproduction/20261023/SUMMARY.md` | Hasil RF awal berhasil direproduksi |
| Draf sebelum fokus dipersempit | `kredit/paper/archive/paper_draft_en_before_six_billing_focus.md` | Arsip, jangan dipakai sebagai draf terbaru |
| Draf gabungan lama | `kredit/paper/manuscript_revision_en.md` | Versi lama; belum sebaik draf terbaru |

**Google Docs yang aktif dan penting:**

https://docs.google.com/document/d/1vgS3AwiC8151cwBpT-pf6nZ0TCvo4Jg5c6CBIN9lMp4/edit

- ID dokumen: `1vgS3AwiC8151cwBpT-pf6nZ0TCvo4Jg5c6CBIN9lMp4`.
- Tab **Draft**, ID `t.0`: berisi draf yang sudah diedit pengguna. Jangan ditimpa.
- Tab **Paper**, ID `t.d2y4968sa2kh`: sudah diisi dengan isi dari Draft dan diformat menyerupai template IEEE A4.
- Pengguna mengedit Draft ketika agen bekerja. Baca ulang keadaan terbaru sebelum mengubahnya. MD lokal tidak otomatis memuat perubahan redaksional Google Docs.
- Versi Paper disalin dari isi Draft yang dibaca pada 28 Oktober, termasuk perubahan abstrak dan paragraf pendahuluan pengguna saat itu. Perubahan Draft berikutnya belum otomatis disinkronkan.
- Dokumen Google lama `1QVm0qhm2uIk7VPTxM_E_8DgEhcnkI8iogQtUPeiQDQE`, judul TG, merupakan konteks historis, bukan target Paper terbaru.

Template pengguna: `D:\Downloads\conference-template-a4.docx`. File sumber tidak diubah. SHA-256 saat diperiksa: `57e2125b0a04860e103fd634c2b5fd19a7ea571fa59ac577bd97afc73ad99482`.

## 3. Anggota kelompok

Nama dan NIM telah diverifikasi langsung dari spreadsheet Kelompok Teori Game A 2026, Sheet1 baris 21-24, kelompok 6 topik TreeSHAP:

https://docs.google.com/spreadsheets/d/1hY-kgJZOOkfVS-7CGM3a3iAcCY25khSClBLlOi33s3E/edit

| Nama | NIM |
| --- | --- |
| Muhammad Daffa Ade Nugraha | L0124127 |
| Muhammad Yahya Saputra | L0124025 |
| Nurman Aqil Wicaksono | L0124139 |
| Muhammad Irfan | L0124063 |

Urutan ini dipakai pada draf. Afiliasi dan email sengaja tidak ditambahkan.

## 4. Data dan pembagian eksperimen

- 30.000 nasabah; target biner gagal bayar bulan berikutnya.
- Positif 6.636 (22,12%); negatif 23.364.
- ID nasabah dikeluarkan dari prediktor.
- EDUCATION 0/5/6 dipetakan menjadi unknown 0; EDUCATION 4 tetap kategori others. MARRIAGE 0 unknown.
- Status pembayaran -2/-1/0 tetap dibedakan; tagihan negatif dan pembayaran nol dipertahankan.
- Tidak ada penghapusan baris, imputation, scaling, clipping, class weighting, atau resampling.
- Setelah pemetaan kategori terdapat 29.944 profil prediktor unik; 52 grup profil berulang memuat 108 baris. Label berbeda pada profil identik dipertahankan.
- StratifiedGroupKFold 5 fold, shuffle, seed 20261020: fold 0 test, fold 1 validation, tiga fold lainnya training. Ini **satu fixed split**, bukan rata-rata 5-fold cross-validation.

| Split | Total | Negatif | Positif |
| --- | ---: | ---: | ---: |
| Train | 18.005 | 14.054 | 3.951 |
| Validation | 5.997 | 4.631 | 1.366 |
| Test | 5.998 | 4.679 | 1.319 |

Encoder dilatih hanya pada train: 9 kategorikal menjadi 75 indikator, ditambah 14 numerik = 89 input. Keenam BILL_AMT tetap numerik. Tidak ada kategori unseen pada held-out split.

Enam tagihan berurutan: BILL_AMT1 September, 2 Agustus, 3 Juli, 4 Juni, 5 Mei, 6 April 2005; satuan New Taiwan dollars.

Korelasi train BILL_AMT: Pearson 0,7963-0,9501, rata-rata 0,8816; Spearman 0,7324-0,9091. Korelasi diukur, bukan dimanipulasi. PAY_AMT memiliki Pearson 0,1149-0,3277 dan Spearman 0,4566-0,5498; jangan menyebutnya independen.

## 5. Pemilihan model

Tiga kandidat per keluarga, seleksi menggunakan AP validation seed 42. Equal candidate count bukan equal compute atau tuning ekstensif. Konfigurasi terpilih dibekukan untuk seed 17 dan 73. Threshold tiap fit dari F1 validation maksimum; tie memilih threshold lebih tinggi. Tidak refit train+validation.

| Model | AP validation | AP test | ROC-AUC test | F1 test |
| --- | ---: | ---: | ---: | ---: |
| Random Forest | 0,5731 | 0,5481 | 0,7741 | 0,5179 |
| Extra Trees | 0,5640 | 0,5387 | 0,7650 | 0,5139 |
| Gradient Boosting | 0,5757 | 0,5441 | 0,7716 | 0,5193 |
| XGBoost | **0,5805** | 0,5472 | 0,7749 | 0,5303 |

XGBoost adalah model utama karena validation AP tertinggi. RF AP test sedikit lebih besar tidak mengubah seleksi. AP bukan otomatis trapezoidal PR-AUC. Jangan memakai MAPE atau R² untuk memilih classifier ini. Brier adalah squared probability error, bukan ukuran kalibrasi murni.

Konfigurasi terpilih:

- RF: 300 pohon, depth 12, min_samples_leaf 5, max_features sqrt, bootstrap true; depth kandidat 8/12/None.
- Extra Trees: 300 pohon, depth None, min_samples_leaf 5, sqrt, bootstrap false; kandidat 8/12/None.
- Gradient Boosting: 200 stages, learning_rate 0,05, depth 3, min_samples_leaf 5, subsample 1; kandidat depth 2/3/4.
- XGBoost: 300 estimators, learning_rate 0,05, depth 3, subsample 0,8, colsample_bytree 0,8, reg_lambda 1, binary:logistic, tree_method hist, n_jobs 2; kandidat depth 2/3/4. Minimum-child native default bukan min_samples_leaf sklearn.

**Test sudah pernah diperiksa pada penelitian awal.** Revisi ini eksploratif; jangan menyebut test sebagai evaluasi konfirmatori yang belum pernah disentuh.

## 6. Protokol TreeSHAP dan hasil utama

- 1.000 observasi test tetap, dipilih tanpa pengembalian, seed 20261022.
- Background interventional: masing-masing 100 baris train, seed 20261021/20261023/20261024.
- Training seed 42 memakai tiga background. Seed 17/73 hanya background 20261021. Bukan full factorial.
- Kedua mode menjelaskan fungsi terlatih, input, class default, dan skala raw yang sama; approximate false.
- Raw XGBoost dan Gradient Boosting = margin log-odds. Raw RF dan Extra Trees = probabilitas kelas 1.
- Jangan menggabungkan magnitudo raw forest dan boosting seolah satuan sama. Jangan melakukan sigmoid pada setiap SHAP log-odds secara terpisah.
- Additivity diperiksa untuk seluruh 89 input ditambah baseline, bukan hanya enam tagihan.
- Toleransi sklearn 1e-6; XGBoost 1e-5 setelah amendment pilot float32 terdokumentasi. Error XGBoost maksimum 4,05e-6; seluruh 32 array lolos. Delapan array merupakan bukti XGBoost utama.

Hasil utama XGBoost seed 42, background 20261021:

- Ranking global kedua mode sama: BILL_AMT1, BILL_AMT4, BILL_AMT3, BILL_AMT2, BILL_AMT5, BILL_AMT6.
- Spearman dan Kendall tau-b ranking enam fitur = 1,0000.
- Leading feature absolut di antara enam tagihan berbeda untuk **149/1.000 = 14,9%** nasabah.
- Margin kedua mode >0,01: 125/952 = 13,13%.
- Margin kedua mode >0,05: **60/764 = 7,85%**.
- Margin kedua mode >0,10: 24/609 = 3,94%.
- Mean billing L1 difference = 0,105069 log-odds; mean absolute signed-group-total difference = 0,055804.
- Baseline interventional -1,373689; path-dependent -1,274798 (log-odds).
- BILL_AMT1 terbesar dalam mean absolute attribution. **BILL_AMT4** terbesar dalam mean paired absolute difference (~0,030967). Kepentingan dan sensitivitas bukan ukuran yang sama.
- Disagreement background 20261021/23/24: 14,9% / 13,7% / 12,1%.
- Disagreement training seed 42/17/73 dengan bg 20261021: 14,9% / 14,9% / 17,1%.

Hasil pendukung seed 42, bg pertama:

| Model | Disagreement | Global Spearman | Mean billing L1 |
| --- | ---: | ---: | --- |
| Random Forest | 42,2% | 0,7714 | 1,1591 percentage points |
| Extra Trees | 42,6% | 0,7714 | 0,3041 percentage points |
| Gradient Boosting | 21,0% | 1,0000 | 0,0643 log-odds |

Angka **42,2%** adalah RF awal, bukan hasil utama XGBoost. Jangan tertukar.

## 7. Makna ukuran dan batas klaim

- Pearson mengukur hubungan linear; Spearman hubungan berdasarkan ranking. Spearman digunakan dua kali: korelasi nilai fitur dan kesamaan ranking importance antarmode. Jelaskan objek yang sedang dibandingkan.
- Global importance = rata-rata |SHAP| pada 1.000 nasabah.
- Leading billing feature = argmax |SHAP| dalam enam tagihan; bukan selalu driver positif risiko terbesar atau fitur teratas dari semua 89 input.
- Unique maxima memakai toleransi absolut 1e-12. Semua primary full-group denominator saat ini 1.000.
- Winner margin = (a1-a2)/(a1+a2), a1/a2 dua atribusi absolut terbesar; nol jika denominator <=1e-12.
- Filter margin mengubah subset dan denominator. Jangan menyebut penurunan disagreement sebagai perbaikan error prediksi atau hasil pada seluruh 1.000 nasabah.
- L1 menjumlahkan selisih absolut enam atribusi; signed group total memungkinkan pembatalan antarfitur. Penjumlahan ini bukan grouped-player Shapley game baru.
- Additivity bukan bukti penjelasan kausal atau satu mode paling benar.
- Path-dependent tidak otomatis merepresentasikan distribusi kondisional observasional yang sempurna.
- Correlated billing features bukan bukti correlation causes disagreement. Judul tidak boleh mengklaim efek kausal korelasi.
- Tiga seed/background tidak menghasilkan bukti stabilitas populasi atau confidence interval yang kuat.
- One-hot masking dapat menghasilkan kombinasi indikator yang tidak alami; source-level aggregation tidak mengubah game input encoded.

## 8. Literatur dan novelty

Dua paper 2025 yang berbeda:

1. García-Céspedes, Alias-Carrascosa, Moreno, *On Machine Learning models explainability in the banking sector: the case of SHAP*, DOI https://doi.org/10.1080/01605682.2025.2485263. Sudah membahas interventional/path-dependent dan reference/portfolio distribution. Full text belum diaudit lengkap; jangan memakai klaim dataset Home Credit sebagai pembeda terverifikasi.
2. Lin dan Wang, *SHAP Stability in Credit Risk Management: A Case Study in Credit Card Default Model*, DOI https://doi.org/10.3390/risks13120238. Dataset Taiwan sama; 100 XGBoost training seeds; global ranking stability. Eksperimen tiga seed kita tidak lebih luas dalam dimensi ini. Jangan menggabungkan rincian kedua paper.

Sumber terkait lain: Nikoltchovska dkk. (2026), *Correlations Matter in Explanations for Energy Systems*, https://doi.org/10.1007/s13218-026-00904-4.

Jangan mengklaim SHAP sepenuhnya berbeda dari TreeSHAP, pertama membandingkan dua mode, dataset sama/berbeda otomatis novelty, atau secara keseluruhan mengungguli paper jurnal. Kontribusi saat ini adalah studi empiris terfokus yang menghubungkan ranking global, agreement individual, margin, dan magnitudo pada enam fitur.

## 9. Status terakhir Google Docs dan masalah terbuka

Pada 28 Oktober, tab Paper diformat native melalui Google Docs API. Isi TNR 10 pt, title 24 pt, abstract 9 pt, caption/references 8 pt, body single spacing, margin A4 sekitar kiri/kanan 45,35 pt, atas 54 pt, bawah 72 pt, gutter dua kolom 18 pt. Ada 8 tabel native, 11 gambar inline (5 grafik + 6 rumus bernomor). Nilai semua sel tabel cocok dengan sumber saat verifikasi.

Google Docs memiliki banyak continuous section breaks untuk mengubah body dua kolom menjadi area full-width untuk tabel/grafik. Tabel III sempat terpotong antarhalaman, lalu caption diberi pageBreakBefore sehingga tabel tetap utuh. Referensi juga dimulai pada halaman baru. Ekspor keseluruhan dokumen terakhir memuat 28 halaman: 17 halaman Draft + 11 halaman Paper; ini bukan 28 halaman satu paper.

**Masalah yang diangkat pengguna terakhir:** screenshot menunjukkan TABLE VII dan TABLE VIII full-width menyela teks dua kolom di tengah halaman. Respons terakhir menjelaskan bahwa tabel spanning two columns boleh, tetapi penempatan belum ideal terhadap template; sebaiknya dirapikan ke bagian atas/bawah halaman, dengan padding, caption bersama tabel, dan aliran baca jelas. Agen mengakui terlalu cepat menyebut formatting selesai.

**Belum ada perbaikan tata letak setelah screenshot itu.** Jangan mengklaim masalah tersebut sudah selesai. Tugas handoff ini hanya membuat MD, bukan menjalankan perbaikan Google Docs.

Jika pengguna meminta melanjutkan perapian:

1. Baca ulang dokumen dan ID tab terbaru; jangan mengandalkan indeks karakter dari handoff.
2. Pertahankan seluruh redaksi dan angka terbaru pengguna. Scope utama tab Paper; Draft tidak diubah kecuali diminta.
3. Atur posisi tabel lebar dan perpindahan section/page agar tidak memotong alur dua kolom. Hindari memaksa setiap tabel menjadi full-width bila dapat dibuat satu kolom dengan tetap terbaca.
4. Periksa tabel/grafik seluruh paper, bukan hanya screenshot atau halaman pertama.
5. Ekspor PDF aktual Google Docs dan periksa hasil render; metadata kolom saja tidak membuktikan layout rapi.
6. Nyatakan keterbatasan layout Google Docs jika ada, bukan menjanjikan fidelity mutlak terhadap Word template.

Bukti QA dan snapshot:

- `tmp/ieee_google_qa/verification.json`.
- `tmp/ieee_google_qa/export.pdf` dan `page-*.png`, `contact-*.png` adalah intermediate ekspor seluruh dokumen, bukan deliverable publik.
- `tmp/ieee_google_source.json` snapshot awal pembacaan 28 Oktober, **bukan jaminan sumber paling baru**.

## 10. Implementasi, runtime, dan alat

Script eksperimen selesai, jangan retrain tanpa kebutuhan:

- `kredit/run_revision_experiments.py`
- `kredit/merge_revision_experiments.py`
- `kredit/analyze_revision_experiments.py`
- `kredit/write_revision_sections.py`
- `kredit/verify_revision_results.py`
- `kredit/finish_revision.py`

Sumber angka di `kredit/experiments/revision_v1/`: `predictive_metrics.csv`, `selection_validation.csv`, `attribution_summary.csv`, `feature_comparison.csv`, `source_importance.csv`, `seed_sensitivity.csv`, `pilot_checks.csv`, `correlation_summary.csv`. Local per-customer billing: `xgboost/seed_42/local_BILL_AMT_20261021.csv`.

Grafik fokus enam fitur: `kredit/paper/figures/six_billing_focus/`. Korelasi: `kredit/paper/figures/billing_correlation_train.png`.

Script penulisan artefak:

- `tmp/pdfs/plot_six_billing_focus.py`: grafik dari hasil tersimpan, tidak retrain.
- `tmp/pdfs/build_paper_pdf.py`: PDF satu kolom dari MD.
- `tmp/pdfs/render_paper_equations.py`: gambar rumus.
- `tmp/build_paper_docx.py`: DOCX satu kolom.
- `tmp/verify_focused_paper.py`: verifikasi fokus dan tautan gambar.
- `tmp/refocus_paper_six_billing.py`, `tmp/update_paper_ieee.py`, `tmp/finalize_paper_draft.py`: script transformasi historis, **jangan dijalankan sembarangan**; beberapa mengasumsikan struktur draf lama dan tidak idempotent.
- `write_revision_sections.py` dapat menimpa draf gabungan lama, bukan pengganti draf polished terbaru.

Python riset: `kredit\.venv_local\Scripts\python.exe`, Python 3.14.7; paket riset dari `.venv/Lib/site-packages` dan extension dependencies. XGBoost 3.4.1, SHAP 0.54.1, scikit-learn 1.7.2 saat eksperimen. Warning lokasi Python lama dapat muncul walaupun proses berhasil.

Untuk artefak, temukan bundled runtime menggunakan tool load_workspace_dependencies. Path sebelumnya:

`C:\Users\Asus\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe`

Bundled Python memiliki python-docx/reportlab/pdfplumber/pypdfium2, tetapi sebelumnya tidak memiliki matplotlib. Gunakan Python riset untuk plotting dan bundled Python untuk artefak. Jangan berasumsi versi bundle tetap.

Kendala yang sudah diketahui:

- Renderer DOCX `render_docx.py` gagal karena LibreOffice/soffice tidak tersedia. DOCX lokal hanya diverifikasi struktur, belum visual. Jangan mengklaim sudah lolos render visual.
- Template DOCX pengguna memakai **Strict OOXML** (`purl.oclc.org`), sehingga python-docx gagal membaca dengan error relationship officeDocument. Inspeksi ZIP/XML berhasil; jangan menganggap file rusak atau menimpa sumber.
- CUA pernah gagal inisialisasi dengan kernel assets path error; jangan mengandalkan browser automation sebelum memeriksa ulang.
- Untuk Google Docs, utamakan plugin Google Drive: get_document, batch_update_document, export_file. Tool dapat ditemukan melalui ALL_TOOLS.
- Index Docs memakai UTF-16, range harus memiliki tabId. Banyak request default ke tab pertama jika tabId hilang.
- requiredRevisionId dapat conflict saat pengguna mengedit Draft. Sebelumnya dipakai targetRevisionId untuk merge perubahan scoped Paper setelah memeriksa konflik; jangan retry mutasi tak pasti tanpa readback.
- API updateTableColumnProperties menggunakan `tableColumnProperties: {widthType, width}`; bukan `columnProperties` atau `columnWidth`.
- updateParagraphStyle pageBreakBefore tidak boleh diberlakukan pada range yang mengandung paragraf dalam tabel. Terapkan pada caption/heading yang tepat.
- updateTableRowStyle memakai tableStartLocation dan rowIndices. Kolom section memakai columnProperties dan paddingEnd; width section output-only.
- Ekspor plugin menghasilkan authenticated download URL berumur pendek. Jangan menaruh URL bearer di dokumen/final. Sebelumnya unduhan PowerShell membutuhkan sandbox escalation karena DNS dalam sandbox gagal; di luar sandbox berhasil. Unduh ulang dari export baru, jangan memakai URL kedaluwarsa.
- Jangan menggunakan command PowerShell terlalu panjang; pernah gagal Windows error 206. Gunakan apply_patch dan file script. Hindari interpolasi dollar/backtick di string shell; `$$` pernah diekspansi PowerShell saat inline Python.

## 11. Pengembangan yang belum dilakukan

Ukuran background yang beragam dan lebih banyak pengulangan; training seeds lebih banyak; evaluasi untouched yang baru; controlled dependence/correlation experiments; dataset tambahan jika disepakati; calibration/fairness/cost analysis. Semua ini **rencana**, bukan hasil yang boleh dimasukkan seolah selesai.

Status ilmiah: hasil komputasi dapat ditelusuri dan pemeriksaan konsistensi lulus, tetapi manuscript belum otomatis publication-ready. Masih perlu review klaim, full-text literature audit, dan penyelesaian format target.

## 12. Cara bekerja dengan pengguna

Pengguna menyukai eksekusi langsung untuk tugas yang sudah jelas dan penjelasan Indonesia sederhana untuk konsep statistik. Tetap pertahankan fokus enam tagihan; jangan membuat paper bergeser menjadi kompetisi model. Jangan meminta ulang persetujuan untuk keputusan yang sudah disepakati. Jangan mengirim pesan ke orang lain atau mengubah tab lain tanpa scope yang sesuai. Jangan membuka thread baru atau mendelegasikan agen kecuali diminta.

Jika ditanya ringkasan penelitian, jelaskan: **empat model untuk seleksi, XGBoost dipilih, kemudian dua mode TreeSHAP dibandingkan pada enam fitur dari model yang sama; global ranking sama tidak menjamin penjelasan individual sama**.
