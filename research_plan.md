# Rencana riset mini paper Teori Game: TreeSHAP

Tanggal penyusunan: 20 Oktober 2026. Dokumen kerja untuk kelompok empat orang; bukan paper hasil eksperimen. Semua angka rancangan di bawah adalah usulan, bukan hasil atau ketentuan dosen.

## 1. Anggota dan keputusan awal

| NIM | Nama | Usulan tanggung jawab utama |
|---|---|---|
| L0124127 | Muhammad Daffa Ade Nugraha | Literatur dan penghubung teori permainan kooperatif |
| L0124025 | Muhammad Yahya Saputra | Integrasi naskah, protokol eksperimen, dan pemeriksaan reproduksibilitas |
| L0124139 | Nurman Aqil Wicaksono | Audit dataset, pemodelan, dan pencatatan eksperimen |
| L0124063 | Muhammad Irfan | Implementasi TreeSHAP, evaluasi atribusi, dan gambar |

Pembagian ini usulan, bukan penetapan keahlian anggota. Semua anggota membaca empat contoh paper, memahami metode, dan meninjau pekerjaan satu anggota lain.

Rekomendasi sementara: pilih B sebagai pertanyaan utama, gunakan A sebagai eksperimen terkontrol, dan jadikan C validasi tambahan berskala kecil. Hindari menjalankan ketiganya sebagai tiga proyek terpisah.

Judul kerja: **Sensitivity of TreeSHAP Feature Attributions to Feature Dependence Assumptions: Controlled Experiments and a Bike-Sharing Case Study**.

Pertanyaan utama: Pada prediktor pohon yang sama, bagaimana pilihan interventional dan tree-path-dependent mengubah pembagian atribusi antara fitur yang berkorelasi, serta seberapa stabil kesimpulan fitur terpenting terhadap pengulangan pelatihan dan pemilihan background?

## 2. Briefing dan sumber ketentuan

Ringkasan briefing bertanda waktu tersedia di [lecturer_briefing.md](lecturer_briefing.md), berdasarkan transkripsi otomatis lokal. Pisahkan tiga sumber: ucapan dosen dalam rekaman; keterangan pengguna tentang UTS/UAS; dan rekomendasi penelitian dalam dokumen ini. Paper acuan adalah bahan analisis, bukan instruksi yang otomatis berlaku untuk tugas.

Hal yang sudah disampaikan pengguna: kelompok empat orang; metode XAI TreeSHAP; dataset belum dipilih; mini paper untuk UTS dan paper yang lebih proper untuk UAS; ada tugas terkait soal per paper. Rekaman mendukung format UTS bebas dalam struktur paper, naskah Inggris, Paperpal di Word, similarity <20%, versi pertama belum harus sempurna, dan penilaian lebih baik untuk progres analisis yang lebih matang. Tenggat terdengar tanggal 25 tanpa bulan/jam. Jumlah soal, panjang naskah, dan rubrik rinci belum terkonfirmasi.

## 3. Pelajaran dari empat paper acuan

### 3.1 Tesla: XGBoost, Random Forest, CatBoost, dan TreeSHAP

Paper membandingkan tiga model regresi pada 761 pengamatan harian dengan tujuh prediktor komoditas dan indeks pasar. CatBoost dilaporkan terbaik, lalu dijelaskan menggunakan TreeSHAP. Pelajaran: masalah jelas, tabel data, protokol tuning, metrik prediksi, dan interpretasi model membentuk alur naskah yang mudah diikuti. Sumber datanya Yahoo Finance dan Investing.com; contoh ini tidak mewajibkan Kaggle.

Pemeriksaan kritis: R² 0,9999 harus ditelaah bersama konstruksi target, jeda waktu prediktor, dan pemisahan train/test. Ini bukan bukti otomatis kebocoran data. Rumusan model yang dilatih ulang per subset pada pembahasan Shapley juga tidak boleh langsung dipakai sebagai deskripsi TreeSHAP untuk satu model tetap. Makalah kelompok perlu mendefinisikan fungsi nilai koalisi yang benar-benar dihitung.

### 3.2 Coffee Bean: EfficientNet-B0 dan Grad-CAM

Paper memakai citra empat kategori dari Kaggle, CNN EfficientNet-B0, dan heatmap Grad-CAM. Pelajaran: interpretasi perlu dijelaskan dalam konteks objek, bukan hanya menampilkan gambar. Namun heatmap yang tampak masuk akal belum membuktikan kesetiaan atau kebenaran penjelasan. Ada kesalahan pada persamaan recall yang tercetak: penyebut seharusnya TP+FN, bukan TP+FP. Pemisahan validasi 10% juga jangan disebut k-fold cross-validation. Gunakan contoh struktur dan alur, tetapi periksa ulang rumus dan klaim.

### 3.3 APCOMS-IMEC: DCGAN dan klasifikasi cacat piston

Paper menggunakan 291 citra asli dan augmentasi DCGAN; melaporkan F1 0,7750 untuk data klasik, 0,9386 untuk sintetis, dan 0,8959 untuk gabungan. Hubungan Teori Game berada pada kompetisi generator-discriminator. Pelajaran untuk TreeSHAP: hubungan Teori Game harus dijelaskan secara konkret, tetapi jenis permainannya berbeda. GAN menggunakan formulasi adversarial/minimax; SHAP menggunakan pembagian nilai dalam permainan kooperatif.

Pertanyaan validitas penting: apakah pengujian menggunakan objek asli yang terpisah sejak sebelum augmentasi, dan apakah foto dari piston yang sama masuk ke lebih dari satu split? Ini pertanyaan audit, bukan tuduhan bahwa kebocoran benar-benar terjadi.

### 3.4 AIP Sectio: LSTM dan LIME

Paper menjelaskan keluaran LSTM saham Tesla menggunakan LIME dan beberapa faktor komoditas serta Dollar Index. Pelajaran: penjelasan lokal dapat berubah antarobservasi; kasus lokal perlu ditautkan ke prediksi spesifik. Ini bukan acuan algoritme TreeSHAP. Paper juga membahas rekonstruksi pola historis; jangan menyamakan rekonstruksi masa lalu dengan kemampuan meramalkan masa depan. Persentase arah naik/turun dan bobot penjelasan harus didefinisikan menurut keluaran model; bobot XAI tidak otomatis berarti persentase sebab-akibat.

## 4. Penilaian pilihan A, B, dan C

| Pilihan | Nilai untuk mata kuliah | Tantangan | Keputusan |
|---|---|---|---|
| A: sensitivitas terhadap korelasi | Mudah diperlihatkan dan divisualisasikan | Perubahan atribusi bisa berasal dari perubahan model saat dilatih ulang | Eksperimen inti pendukung B |
| B: asumsi fungsi nilai koalisi | Paling langsung ke konsep Shapley | Path-dependent bukan conditional SHAP eksak | Pertanyaan utama |
| C: kesesuaian dengan kontribusi diketahui | Kuat bila acuan matematis konsisten | Fungsi target, model terlatih, dan permainan dapat berbeda | Validasi tambahan UAS |

Kontribusi yang realistis adalah studi empiris terkontrol dengan protokol jelas dan kasus nyata yang dapat diulang. Jangan mengklaim algoritme baru atau penelitian pertama tentang korelasi dan SHAP. Literatur sudah banyak membahasnya; pencarian ini belum merupakan systematic literature review.

Pembaruan audit kebaruan, 20 Oktober 2026: ditemukan penelitian yang sangat dekat, [Correlations Matter in Explanations for Energy Systems](https://doi.org/10.1007/s13218-026-00904-4), Nikoltchovska dkk., terbit 30 Maret 2026. Penelitian ini sudah menggunakan korelasi sintetis terkontrol dan membandingkan beberapa explainer, termasuk TreeSHAP interventional dan path-dependent, disertai studi data energi nyata. Karena itu, gabungan ide A+B serta sintetis+kasus nyata tidak dapat diklaim sebagai kebaruan umum. Posisi yang aman adalah replikasi dan pengembangan empiris; calon pengembangan berupa perbandingan ketidaksepakatan lokal/global dan variasi antarpelatihan masih harus diaudit terhadap literatur. [On marginal feature attributions of tree-based models](https://arxiv.org/abs/2302.08434), Filom dkk., 2023, juga membahas perbedaan ranking path-dependent pada pohon yang merepresentasikan fungsi sama.

Pembaruan konteks kelompok: pengguna kemudian memilih kasus gagal bayar kartu kredit dengan file `kredit/UCI_Credit_Card.csv`. Pegangan khusus literatur dan rumusan kasus terbaru tersedia di `literature_guide.md`; bagian Bike Sharing di dokumen ini merupakan rancangan awal. Ditemukan pula [SHAP Stability in Credit Risk Management: A Case Study in Credit Card Default Model](https://doi.org/10.3390/risks13120238), Lin dan Wang, 2025, yang menggunakan dataset kredit Taiwan yang sama dan 100 seed XGBoost. Jadi dataset tersebut ditambah pengulangan seed bukan kebaruan mandiri; fokus kerja tetap perbandingan mode dan alokasi atribusi fitur berkorelasi, dengan audit kebaruan lanjutan.

## 5. Kaitan matematis dengan Teori Game

Fitur berperan sebagai pemain; S adalah koalisi fitur; v_x(S) menyatakan nilai ketika fitur dalam S diketahui menurut aturan permainan. Shapley membagi selisih prediksi terhadap nilai dasar:

\[
\phi_i(x)=\sum_{S\subseteq N\setminus\{i\}}
\frac{|S|!(M-|S|-1)!}{M!}\,[v_x(S\cup\{i\})-v_x(S)].
\]

Untuk permainan interventional yang memakai background empiris B:

\[
v_x^{int}(S)=\frac{1}{|B|}\sum_{b\in B}f(x_S,b_{\bar S}).
\]

Untuk permainan conditional ideal:

\[
v_x^{cond}(S)=E[f(X)\mid X_S=x_S].
\]

Dalam interventional, ketergantungan antara fitur yang dipertahankan dan fitur yang digantikan diputus; ketergantungan antarkolom yang diambil bersama dari baris background tidak harus hilang. Jangan menyederhanakan menjadi klaim bahwa semua fitur selalu diasumsikan independen.

Tree-path-dependent memakai struktur pohon serta frekuensi sampel pelatihan yang melewati jalur pohon. Ia bukan oracle distribusi kondisional sebenarnya. Oleh sebab itu perbandingan implementasi utama harus dinamai **interventional versus tree-path-dependent**, bukan interventional versus conditional exact. Terminologi interventional sendiri tidak cukup untuk menyimpulkan efek kausal di dunia nyata.

Bahas efisiensi, simetri, dummy player, dan aditivitas terhadap permainan yang telah didefinisikan. Fitur yang tidak digunakan model belum tentu dummy dalam permainan conditional apabila memberikan informasi tentang fitur lain. Periksa local additivity untuk setiap explainer menggunakan baseline masing-masing:

\[
f(x)\approx\phi_0+\sum_i\phi_i(x).
\]

Baseline dapat berbeda antarmode, sehingga selisih atribusi perlu dibaca bersama selisih baseline. Tidak ada kesimpulan otomatis bahwa satu mode lebih benar karena nilainya berbeda.

Contoh analitis opsional: X1 dan X2 Gaussian standar, korelasi rho, dan f(x)=x1. Dengan baseline populasi nol, interventional memberi phi1=x1 dan phi2=0; conditional memberi phi1=x1-rho*x2/2 dan phi2=rho*x2/2. Keduanya menjumlah ke x1. Contoh ini menunjukkan konsekuensi definisi permainan; bukan hasil TreeSHAP pada model yang dilatih. Untuk menilai implementasi pohon, gunakan acuan pada fungsi pohon yang sama.

## 6. Dataset dan alasan pemilihan

### Utama: UCI Bike Sharing, hour.csv

Sumber primer: [UCI Bike Sharing](https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset). DOI dataset: [10.24432/C5W894](https://doi.org/10.24432/C5W894). Lisensi yang tertera: CC BY 4.0. Data Capital Bikeshare tahun 2011-2012, dengan variabel waktu dan cuaca. Gunakan data per jam, jangan mencampurkannya dengan agregat harian sebagai observasi independen. Catat jumlah baris dari CSV sebenarnya: halaman metadata menampilkan 17.389, sementara angka yang sering digunakan untuk hour.csv adalah 17.379; audit jumlah aktual sebelum menulis naskah.

Target: cnt. Buang casual dan registered dari prediktor karena keduanya menjumlah menjadi cnt. Buang instant sebagai ID; gunakan dteday untuk pengurutan dan pembagian waktu. Pasangan kandidat utama temp dan atemp; ukur korelasinya pada train, jangan mengarang angkanya. Pasangan kalender seperti bulan-musim bisa menjadi analisis tambahan karena ketergantungannya bersifat kategoris dan bukan sekadar Pearson.

Posisikan kasus nyata sebagai penjelasan prediksi permintaan pada informasi waktu/cuaca yang tersedia. Jika mengklaim forecasting operasional, tetapkan horizon serta pastikan cuaca masa depan bukan observasi yang belum tersedia pada saat prediksi.

Kaggle: [Bike Sharing Demand](https://www.kaggle.com/competitions/bike-sharing-demand/data). Ini alternatif yang sesuai preferensi pengguna, tetapi format kompetisi, target test, jumlah baris, dan syarat pemakaian perlu diverifikasi. Jangan menganggap file Kaggle identik dengan hour.csv UCI. Untuk eksperimen yang perlu seluruh target evaluasi tersedia, UCI lebih praktis. Jika menggunakan mirror Kaggle, catat uploader/slug/versi dan sumber asal; sitasi Kaggle serta sumber primer.

Alternatif Kaggle nonkompetisi yang telah ditemukan: [Bike Sharing in Washington D.C. Dataset](https://www.kaggle.com/datasets/marklvl/bike-sharing-dataset), slug `marklvl/bike-sharing-dataset`; daftar file terindeks memuat `Readme.txt`, `day.csv`, dan `hour.csv`. Pilih `hour.csv` untuk pilot; audit isi CSV, lisensi mirror, jumlah baris, serta kecocokan dengan sumber primer saat pengunduhan. Alternatif dataset berbeda adalah [London bike sharing dataset](https://www.kaggle.com/datasets/hmavrodiev/london-bike-sharing-dataset), file `london_merged.csv`, dengan target `cnt`, suhu aktual `t1` dan suhu terasa `t2`; kartu data menyebut sumber TfL, freemeteo, dan kalender hari libur pemerintah Inggris. Ketersediaan halaman/file telah ditelusuri, tetapi CSV belum diunduh atau dianalisis sehingga nilai korelasi belum diverifikasi.

### Cadangan: Concrete Compressive Strength

[UCI Concrete](https://archive.ics.uci.edu/dataset/165/concrete+compressive+strength), [DOI 10.24432/C5PK67](https://doi.org/10.24432/C5PK67). Memiliki 1.030 pengamatan, delapan input bahan/umur, satu target kuat tekan, dan lisensi CC BY 4.0. Lebih ringan daripada data waktu, tetapi pasangan fitur dengan korelasi yang berguna harus diperiksa dahulu. Pemisahan berdasarkan kelompok komposisi campuran perlu dipertimbangkan apabila campuran sama diukur pada umur berbeda.

Jangan memilih dataset hanya karena ada di Kaggle. Kriteria penerimaan: asal pengukuran jelas, target dapat dijelaskan, kamus variabel tersedia, lisensi dapat diperiksa, tidak ada kebocoran target, dan ukuran cukup untuk evaluasi.

## 7. Protokol eksperimen yang diusulkan

### Tahap UTS: hasil minimum yang utuh

1. Satu dataset nyata, satu model utama RandomForestRegressor, dan DummyRegressor sebagai pembanding prediksi. XGBoost menjadi replikasi tambahan jika waktu cukup.
2. Data diurutkan waktu. Usulan split kronologis 60% train, 20% validation, 20% test; tuning hanya pada train/validation. Jangan memilih konfigurasi berdasarkan test. Laporkan periode dan jumlah baris aktual.
3. Seleksi pasangan fitur berdasarkan train. Preprocessing dipelajari dari train dan diterapkan konsisten. Untuk kategori, dokumentasikan encoding; bila one-hot, agregasi penjelasan kembali ke fitur asal harus dinyatakan.
4. Latih model sekali per seed. Untuk pasangan perbandingan, gunakan model dan sampel test yang persis sama; yang berubah hanya mode explainer. Tetapkan model_output='raw' untuk regresi dan feature_perturbation secara eksplisit; hindari ketergantungan pada auto.
5. Background interventional diambil dari train, misalnya 100 baris; jelaskan 200-500 baris test dengan indeks tersimpan. Ini angka usulan untuk pilot, bisa disesuaikan waktu komputasi.
6. Jalankan lima seed pilot. Pisahkan variasi seed pelatihan dari variasi sampling background. Tree-path-dependent pada model dan input tetap tidak perlu dianggap stokastik.
7. Ukur MAE, RMSE, R²; selisih SHAP lokal berpasangan; mean absolute SHAP; Spearman ranking; dan overlap top-3. Tampilkan baseline serta additivity residual.
8. Naskah sudah berisi hasil aktual, pembahasan, batasan, dan kesimpulan sesuai bukti. Jangan menyebut dugaan hasil sebagai hasil eksperimen.

### Tahap UAS: eksperimen sintetis dan penguatan

Usulan DGP: Z1,Z2,Z3,Z4 dan epsilon independen normal standar; X1=Z1, X2=rho*Z1+sqrt(1-rho²)*Z2, X3=Z3, X4=Z4; Y=2*X1+X3²+sigma*epsilon. X2 adalah proxy berkorelasi tanpa term langsung pada fungsi target; X4 kontrol tak relevan yang independen. Distribusi marginal target tetap ketika rho berubah.

Gunakan tingkat rho dalam notasi kode [0.0, 0.3, 0.6, 0.9, 0.99]. Tidak perlu rho=1 yang singular pada pilot. Tetapkan ukuran data dan sigma; gunakan latent draw, noise, serta split yang berpasangan antar-rho. Usulan 3.000 sampel/ulangan, 10 ulangan awal dan 20 jika anggaran komputasi memungkinkan.

Pada setiap rho, fit satu model lalu bandingkan dua mode pada model yang sama. Jika model dilatih ulang antar-rho, efek total mencakup perubahan representasi model; jangan menamai semuanya efek murni explainer. Simpan RMSE dan frekuensi split fitur untuk membantu menjelaskan pergeseran atribusi. Eksperimen model tetap dapat ditambahkan secara terpisah untuk mengisolasi sensitivitas penjelasan terhadap perubahan distribusi/input.

Variasi background 50/100/300 dilakukan sebagai studi tersendiri dengan model dan test tetap. Tambah XGBoost sebagai replikasi metode dan satu dataset cadangan hanya setelah pipeline inti stabil. Desain rho dan ukuran background tidak harus difaktorialkan seluruhnya agar biaya tetap masuk akal.

Untuk validasi numerik C, gunakan pohon kecil 3-5 fitur. Enumerasi 2^M koalisi dan hitung Shapley dengan background empiris yang persis sama dengan explainer interventional; bandingkan pada model pohon tersebut. Perbedaan terhadap fungsi pembentukan target merupakan error model yang terpisah. Conditional reference memerlukan distribusi yang diketahui atau estimator kondisional beserta ketidakpastiannya; jangan menjadikannya kewajiban UTS.

### Definisi metrik penjelasan

- Global importance: I_j=mean_x |phi_j(x)|. Jangan memakai mean signed SHAP untuk peringkat global karena saling meniadakan.
- Selisih mode: D=mean_x sum_j |phi_j_int(x)-phi_j_path(x)|; satuannya sama dengan target. Jika dinormalisasi, tetapkan denominator dan penanganan nilai mendekati nol sebelum melihat hasil.
- Kesepakatan ranking: Spearman antara dua vektor I; atur ties dan laporkan kondisi ranking tidak terdefinisi.
- Overlap top-k: Jaccard |A intersect B|/|A union B|, dengan k tetap. Ketidaksepakatan tidak otomatis berarti ketidakakuratan.
- Pembagian proxy: I2/(I1+I2), hanya ketika penyebut cukup besar.
- Agregat pasangan: mean |phi1+phi2| dan I1+I2 boleh dilaporkan tetapi keduanya berbeda. Penjumlahan SHAP individual bukan otomatis Shapley dari permainan baru dengan pemain gabungan.
- Additivity: maksimum dan rata-rata |f(x)-phi0-sum(phi)|. Ini pemeriksaan implementasi, bukan bukti bahwa penjelasan bersifat kausal atau benar secara substantif.

Laporkan variasi antarrun sebagai distribusi serta interval ketidakpastian; untuk inferensi antarrun gunakan unit seed/run berpasangan. Untuk bootstrap data per jam, gunakan blok waktu, bukan menganggap jam selalu independen. Hindari memilih hanya run terbaik.

## 8. Hasil yang perlu ditampilkan

Empat keluaran minimum UTS: tabel dataset/split dan konfigurasi; tabel metrik prediksi; diagram ranking kedua mode; serta dua penjelasan lokal berpasangan pada observasi yang sama. Sertakan additivity residual dan aturan memilih kasus lokal, misalnya satu hari permintaan tinggi dan satu rendah yang dipilih dengan kriteria tertulis.

Untuk UAS tambahkan kurva rho terhadap selisih atribusi dan pembagian proxy dengan error bar; analisis sensitivitas background; validasi enumerasi; serta satu tabel ringkasan kapan kesimpulan mode berbeda. Hasil nol tetap informatif apabila desain dan batasannya jelas.

## 9. Struktur naskah dan rencana kerja

Struktur: judul dan identitas; abstract ditulis setelah hasil; introduction dengan masalah/RQ/kontribusi; related work; game-theoretic formulation; methodology; results and discussion; limitations; conclusion; references. Target kerja internal 4-6 halaman dapat dipakai untuk mengendalikan lingkup, tetapi bukan ketentuan dosen sampai terverifikasi.

| Hari kerja relatif | Keluaran yang dapat diperiksa | Penanggung jawab utama |
|---|---|---|
| 1 | Ringkasan briefing, daftar syarat, dan keputusan RQ | Yahya + semua anggota |
| 2 | Matriks literatur dan audit dataset | Daffa + Aqil |
| 3 | Data split, baseline, dan model pertama | Aqil; Irfan memeriksa |
| 4 | Dua mode TreeSHAP dan metrik berpasangan | Irfan; Yahya memeriksa |
| 5 | Lima run pilot, tabel, dan gambar | Aqil + Irfan |
| 6 | Draf penuh dengan hasil aktual | Semua, integrasi Yahya |
| 7 | Audit klaim/sitasi, bahasa, dan latihan pembelaan | Semua, integrasi Daffa |

Jadwal tujuh hari di atas adalah pola ideal jika tersedia waktu. Dengan asumsi tenggat 25 Oktober 2026, pakai sprint lima hari pada lecturer_briefing.md: 20 Oktober keputusan/audit; 21 model; 22 TreeSHAP; 23 pengulangan/draf; 24 audit; 25 pengumpulan. Untuk UAS, lanjutkan eksperimen sintetis, pengulangan lebih banyak, dan replikasi model; jangan mengganti topik setelah pipeline UTS terbentuk kecuali pilot memperlihatkan hambatan substantif.

Praktik reproduksibilitas: simpan raw data asli beserta URL, tanggal unduh, versi dan checksum; konfigurasi seed/split/fitur/background/test; versi Python, shap dan model; CSV hasil setiap run; script pembuat gambar; serta README urutan menjalankan. Semua tabel dan angka naskah diturunkan dari hasil tersimpan. Paperpal dipakai untuk penyuntingan bahasa setelah klaim dan sitasi diverifikasi manusia.

## 10. Referensi riset terverifikasi dan urutan baca

Pencarian dilakukan 20 Oktober 2026 dengan prioritas IEEE. Beberapa halaman IEEE membatasi akses otomatis; untuk entri bertanda metadata/abstrak, telaah metode lengkap masih perlu dilakukan melalui akses kampus. Jangan mengutip detail yang belum dibaca. Fondasi asli SHAP/TreeSHAP tetap perlu walaupun tidak semuanya IEEE.

| Prioritas | Sumber | Kegunaan dan batas akses |
|---|---|---|
| 1 | [Forecasting Tesla Stock Price Using XGBoost, Random Forest, and CatBoost](https://doi.org/10.1109/ICAITech66481.2025.11387624), ICAITech 2025, IEEE | Full text lampiran dibaca visual; contoh terdekat untuk struktur TreeSHAP |
| 2 | [Stability and Consistency Analysis of SHAP and LIME Explanations Across Machine Learning Models](https://doi.org/10.1109/ICERECT65215.2025.11378102), ICERECT 2025, masuk Xplore 2026 | Metadata/abstrak; pembanding metrik stabilitas Spearman dan Jaccard |
| 3 | [Exploring Consistent Feature Selection for Software Fault Prediction: An XAI-Based Model-Agnostic Approach](https://doi.org/10.1109/ACCESS.2025.3558913), IEEE Access 2025 | Metadata/abstrak; variasi data/validasi dan konsistensi pemilihan fitur |
| 4 | [A Correlation-Aware Feature Selection and Explainable AI Framework for Avian Influenza Outbreak Prediction](https://doi.org/10.1109/ACCESS.2025.3625369), IEEE Access 2025 | Metadata/abstrak; korelasi dan redundansi, tetapi fokus seleksi fitur, bukan pembuktian dua mode TreeSHAP |
| 5 | [Peeking Inside the Black-Box: A Survey on Explainable Artificial Intelligence (XAI)](https://doi.org/10.1109/ACCESS.2018.2870052), IEEE Access 2018 | Pemetaan umum XAI; pengantar, bukan bukti khusus eksperimen korelasi |
| 6 | [A Unified Approach to Interpreting Model Predictions](https://proceedings.neurips.cc/paper/2017/hash/8a20a8621978632d76c43dfd28b67767-Abstract.html), Lundberg dan Lee, NeurIPS 2017 | Fondasi SHAP; non-IEEE |
| 7 | [From local explanations to global understanding with explainable AI for trees](https://doi.org/10.1038/s42256-019-0138-9), Lundberg dkk., Nature Machine Intelligence 2020 | Fondasi TreeSHAP; non-IEEE |
| 8 | [Explaining individual predictions when features are dependent](https://arxiv.org/abs/1903.10464), Aas, Jullum, Løland | Sumber penulis tentang fitur dependen; tautan ini versi preprint, cocokkan publikasi final saat sitasi |
| 9 | [True to the Model or True to the Data?](https://arxiv.org/abs/2006.16234), Chen dkk., 2020 | Dua tujuan atribusi dan perbedaan permainan; non-IEEE |
| 10 | [Problems with Shapley-value-based explanations as feature importance measures](https://proceedings.mlr.press/v119/kumar20e.html), Kumar dkk., ICML 2020 | Batas interpretasi dan alasan menghindari klaim kebenaran universal |
| 11 | [First-Mover Bias in Gradient Boosting Explanations](https://arxiv.org/abs/2603.22346), Caraker dkk., preprint 2026 | Pemeriksaan kebaruan terkini; belum diperlakukan sebagai bukti peer-reviewed |

Dokumentasi implementasi: [shap.TreeExplainer](https://shap.readthedocs.io/en/latest/generated/shap.TreeExplainer.html). Ia menjelaskan parameter mode, background, dan output. Dokumentasi bukan pengganti paper ilmiah.

Untuk menuntaskan literature review: baca penuh 6-10 sumber inti; catat dataset, model, jenis permainan, pertanyaan, metrik, temuan dan batasan; telusuri referensi serta paper yang mengutipnya. Kebaruan yang perlu diuji lebih lanjut adalah konfigurasi evaluasi dan studi kasus kelompok, bukan gagasan umum bahwa korelasi memengaruhi SHAP.

## 11. Latihan pertanyaan untuk empat paper acuan

Daftar ini bahan latihan dan draf awal. Jumlah serta format soal resmi mengikuti briefing.

| Paper | Pertanyaan | Arah jawaban |
|---|---|---|
| Tesla | Mengapa model terbaik ditentukan sebelum interpretasi? | Berdasarkan metrik validasi yang ditetapkan; test tidak dipakai tuning; penjelasan menerangkan model terpilih |
| Tesla | Apakah R² sangat tinggi membuktikan forecasting bagus? | Perlu definisi horizon, fitur yang tersedia saat prediksi, split waktu, dan baseline |
| Tesla | Mengapa fitur pasar berkorelasi bisa mengubah ranking SHAP? | Pembagian kredit dipengaruhi model, distribusi referensi, dan fungsi nilai koalisi |
| Coffee | Apa fungsi EfficientNet dan apa fungsi Grad-CAM? | EfficientNet menghasilkan prediksi; Grad-CAM menjelaskan fokus spasial secara post-hoc |
| Coffee | Apakah heatmap membuktikan model bebas shortcut? | Tidak; perlu kontrol/ablasi dan evaluasi tambahan |
| Coffee | Apa perbaikan persamaan recall? | TP/(TP+FN); precision adalah TP/(TP+FP) |
| Piston | Di mana konsep game theory digunakan? | Kompetisi generator dan discriminator pada objektif adversarial |
| Piston | Mengapa F1 sintetis tertinggi belum cukup? | Harus diperiksa sumber dan independensi test serta generalisasi ke citra asli |
| Piston | Kapan pemisahan data dilakukan terhadap augmentasi? | Pisahkan objek asli dahulu; augmentasi/GAN hanya memakai train |
| AIP LIME | Bagaimana LIME menjelaskan LSTM? | Membangun surrogate sederhana berbobot di sekitar instance |
| AIP LIME | Mengapa dua hari dapat memiliki penjelasan berbeda? | Penjelasan bersifat lokal terhadap instance dan keluaran model |
| AIP LIME | Apakah bobot penjelasan berarti persentase pengaruh kausal? | Tidak tanpa definisi, normalisasi, dan desain kausal yang mendukung |

## 12. Kriteria selesai

UTS internal selesai jika masalah/RQ jelas, data terverifikasi, pipeline berjalan ulang, kedua mode diperiksa additivitasnya, hasil pilot aktual tersedia, naskah penuh dapat dibaca, referensi dapat dilacak, dan semua anggota mampu menjelaskan hubungan dengan permainan kooperatif. Eksperimen tambahan adalah penguatan UAS, bukan alasan menunda naskah pertama.
