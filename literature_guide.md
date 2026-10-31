# Pegangan Daffa: literatur, rumusan masalah, dan Shapley

Topik kelompok: pembagian atribusi fitur tagihan berkorelasi pada prediksi gagal bayar kartu kredit menggunakan dua mode TreeSHAP.

Disusun 20 Oktober 2026. Ini bahan belajar dan draf kerja, bukan hasil eksperimen atau klaim kebaruan yang sudah final. Semua contoh angka pada bagian Shapley bersifat ilustratif. Daftar pustaka mesin tersedia di `references.bib`.

## 1. Mulai dari pekerjaan apa?

Target Daffa adalah mampu menjawab tiga pertanyaan: apa masalahnya, apa yang sudah dilakukan peneliti lain, dan mengapa rancangan kelompok layak dijalankan. Jangan mulai dengan menulis seluruh Introduction dari judul-judul paper.

Urutan awal yang disarankan:

1. Baca penjelasan Shapley pada bagian 5 dokumen ini.
2. Baca R2 untuk fondasi SHAP, lalu R7 untuk melihat penelitian kredit yang paling dekat.
3. Baca R6 dan R4 untuk memahami korelasi serta perbedaan definisi permainan.
4. Baca R3 tentang TreeSHAP, lalu R9 sebagai contoh aplikasi kredit dari IEEE.
5. Lengkapi R8, R5, dan R1 sesuai kebutuhan kedalaman teori.
6. Isi catatan baca setiap paper. Setelah itu perbaiki rumusan masalah dan draf Introduction.

Target kerja awal: satu halaman ringkasan masalah, matriks 5-8 paper yang sudah dibaca, dan catatan teori yang bisa dijelaskan kepada anggota lain. Semua angka target ini merupakan saran internal.

## 2. Daftar bacaan yang dipilih

Prioritas IEEE diterapkan untuk bacaan aplikasi. Namun sumber asli Shapley, SHAP, TreeSHAP, dan penelitian yang paling dekat secara metodologis berada di penerbit lain. Jangan mengabaikannya karena label penerbit.

### R1. Landasan permainan kooperatif

L. S. Shapley, **A Value for n-Person Games**, 1953, dalam Contributions to the Theory of Games, Volume II.

[Halaman penerbit/DOI](https://doi.org/10.1515/9781400881970-018)

Gunakan untuk asal konsep pembagian nilai permainan kooperatif. Fokus pada pemain, characteristic function, dan sifat pembagian. Bab ini lebih matematis dan akses penerbit dapat memerlukan institusi. Metadata dan pengantar penerbit diverifikasi; bukan telaah penuh bab.

Pertanyaan baca: nilai apa yang dibagi? Mengapa nilai koalisi harus didefinisikan sebelum menghitung Shapley?

### R2. Fondasi SHAP

S. M. Lundberg dan S.-I. Lee, **A Unified Approach to Interpreting Model Predictions**, NeurIPS 2017, pp. 4765-4774.

[Halaman resmi](https://proceedings.neurips.cc/paper/2017/hash/8a20a8621978632d76c43dfd28b67767-Abstract.html) | [PDF resmi](https://proceedings.neurips.cc/paper/2017/file/8a20a8621978632d76c43dfd28b67767-Paper.pdf)

Menjelaskan SHAP sebagai kerangka atribusi fitur lokal dengan bentuk penjelasan aditif. Baca Introduction dan bagian additive feature attribution methods, lalu hubungan dengan Shapley. PDF tersedia dan teks bagian konsep diperiksa; Daffa tetap membaca sendiri sebelum menjadikannya dasar uraian metode.

Pertanyaan baca: mengapa satu fitur dapat memiliki kontribusi berbeda pada dua nasabah? Apa beda nilai lokal dan ringkasan global?

### R3. Fondasi TreeSHAP

S. M. Lundberg dkk., **From local explanations to global understanding with explainable AI for trees**, Nature Machine Intelligence, vol. 2, pp. 56-67, 2020. DOI 10.1038/s42256-019-0138-9.

[Penerbit](https://doi.org/10.1038/s42256-019-0138-9) | [Naskah penulis](https://arxiv.org/abs/1905.04610)

Gunakan untuk alasan memilih TreeSHAP pada model pohon dan cara menghubungkan penjelasan lokal dengan pola global. Baca gambaran metode, algoritme serta supplementary methods tentang path-dependent dan interventional. Ringkasan penerbit dan bagian metode yang tersedia ditelusuri; belum seluruh suplemen direplikasi.

Pertanyaan baca: apa fungsi model pohon dalam mempercepat perhitungan? Apa yang dimaksud eksak relatif terhadap asumsi permainan?

### R4. Dua tujuan penjelasan dan konteks kredit

H. Chen, J. D. Janizek, S. Lundberg, dan S.-I. Lee, **True to the Model or True to the Data?**, 2020.

[Naskah penulis/preprint](https://arxiv.org/abs/2006.16234)

Membahas perbedaan interventional dan observational expectation serta mengapa pilihan bergantung tujuan penjelasan. Ada contoh credit risk modeling, sehingga bacaan ini langsung relevan. Analisis utamanya menggunakan model linear; jangan menyalin kesimpulannya seolah membuktikan bahwa tree-path-dependent adalah conditional SHAP eksak. Status sitasi pada pegangan ini menggunakan preprint; metadata publikasi final perlu disesuaikan jika ditemukan.

Pertanyaan baca: kita ingin menjelaskan fungsi yang dipelajari model atau informasi yang terkandung dalam hubungan antarfitur?

### R5. Mengapa Shapley bisa memiliki beberapa penerapan

M. Sundararajan dan A. Najmi, **The Many Shapley Values for Model Explanation**, ICML 2020, PMLR 119, pp. 9269-9278.

[Halaman resmi](https://proceedings.mlr.press/v119/sundararajan20b.html) | [PDF resmi](https://proceedings.mlr.press/v119/sundararajan20b/sundararajan20b.pdf)

Gunakan untuk menjelaskan bahwa keunikan Shapley berlaku setelah permainan ditetapkan. Operasionalisasi permainan yang berbeda dapat menghasilkan atribusi berbeda. Metadata dan abstrak resmi diverifikasi; baca teks penuh untuk argumen dan contoh formal.

Pertanyaan baca: apakah perbedaan atribusi selalu merupakan error? Mengapa fitur yang tidak dipakai fungsi model dapat menerima atribusi dalam permainan informasional tertentu?

### R6. Penelitian yang sangat dekat dengan masalah korelasi

A. Nikoltchovska, S. Pütz, M. Götz, dan B. Schäfer, **Correlations Matter in Explanations for Energy Systems**, KI - Künstliche Intelligenz, vol. 40, pp. 41-54, 2026. Terbit 30 Maret 2026. DOI 10.1007/s13218-026-00904-4.

[Teks terbuka penerbit](https://doi.org/10.1007/s13218-026-00904-4)

Bagian experimental design dan perbandingan metode dibaca. Studi ini memakai korelasi sintetis terkontrol dan data energi nyata, termasuk dua mode TreeSHAP. Ini alasan kita tidak mengklaim ide korelasi plus perbandingan mode sebagai penelitian pertama. Ambil pelajaran tentang membedakan tujuan penjelasan, bukan menerima seluruh interpretasi atau istilahnya tanpa pemeriksaan.

Pertanyaan baca: apa yang sudah dijawab oleh eksperimen mereka? Apa yang perlu direplikasi, dan apa tambahan spesifik yang akan diuji kelompok?

### R7. Penelitian terdekat pada dataset kredit yang sama

L. Lin dan Y. Wang, **SHAP Stability in Credit Risk Management: A Case Study in Credit Card Default Model**, Risks, vol. 13, no. 12, artikel 238, 2025. DOI 10.3390/risks13120238.

[Versi jurnal](https://doi.org/10.3390/risks13120238) | [Preprint penulis](https://arxiv.org/abs/2508.01851) | [PDF preprint](https://arxiv.org/pdf/2508.01851)

Metode preprint diperiksa. Paper memakai UCI Default of Credit Card Clients, melatih 100 XGBoost dengan seed berbeda, dan menilai stabilitas ranking SHAP menggunakan Kendall's W. Karena dataset serta analisis antarseed sudah ada, keduanya bukan kebaruan mandiri. Versi jurnal juga tersedia; saat mengutip detail metode, cocokkan dengan versi jurnal karena preprint dapat berbeda.

Pertanyaan baca: apakah mereka membandingkan kedua mode secara eksplisit dengan model/background/observasi terkontrol? Bagaimana preprocessing dan penggabungan fitur hasil encoding memengaruhi perbandingan? Jawab berdasarkan teks atau kode, bukan menganggap hal yang tidak disebut berarti pasti tidak dilakukan.

Catatan audit: jangan menyalin angka persentase atau tabel tanpa menghitung ulang. Contohnya, 6.636 dari 30.000 adalah 22,12%; salah satu bagian preprint menuliskan sekitar 22,22%. Kesalahan kecil sumber tidak perlu diwarisi.

### R8. Pengaruh ketidakseimbangan kelas pada interpretasi kredit

Y. Chen, R. Calabrese, dan B. Martin-Barragan, **Interpretable machine learning for imbalanced credit scoring datasets**, European Journal of Operational Research, vol. 312, no. 1, pp. 357-372, 2024. DOI 10.1016/j.ejor.2023.06.036.

[DOI](https://doi.org/10.1016/j.ejor.2023.06.036) | [Repositori universitas](https://www.research.ed.ac.uk/en/publications/interpretable-machine-learning-for-imbalanced-credit-scoring-data/) | [PDF repositori](https://www.research.ed.ac.uk/files/372197768/ChenEtal2023EJORInterpretableMachineLearning.pdf)

Abstrak dan metadata repositori penulis diverifikasi. Paper meneliti stabilitas SHAP/LIME ketika class imbalance berubah. Relevan untuk membatasi faktor eksperimen: perubahan sampling kelas tidak boleh tercampur tanpa sengaja dengan perubahan mode explainer. Bukan alasan otomatis menerapkan SMOTE; metode lengkap perlu dibaca dahulu.

Pertanyaan baca: bagaimana mereka mengukur stabilitas? Apa beda variasi data, model, dan explainer?

### R9. Contoh aplikasi dari IEEE

Q. Xu, Y. Liao, Q. Li, J. Zhang, Z. Song, L. Wang, dan X. Yuan, **SHAP-based Interpretable Models for Credit Default Assessment Using Machine Learning**, ICSTE 2024, IEEE, pp. 213-217. DOI 10.1109/ICSTE63875.2024.00044.

[IEEE Xplore](https://ieeexplore.ieee.org/document/10840375) | [DOI](https://doi.org/10.1109/ICSTE63875.2024.00044) | [Metadata dan abstrak institusi penulis](https://research.mpu.edu.mo/en/publications/shap-based-interpretable-models-for-credit-default-assessment-usi/)

Metadata/abstrak diverifikasi melalui IEEE dan institusi penulis; full text belum ditelaah. Studi memakai Lending Club, bukan otomatis dataset Taiwan kelompok. Gunakan untuk konteks aplikasi penjelasan kredit dan contoh susunan studi; jangan mengutipnya sebagai bukti perbandingan dua mode TreeSHAP.

Pertanyaan baca: apa target yang sebenarnya diprediksi? Model apa yang dijelaskan? Apakah klaim interpretasi didukung evaluasi kuantitatif?

### R10. IEEE tambahan jika ingin memperluas konteks

**Interpreting Credit Risk Prediction with XGBoost and SHAP**, ISRITI 2025, IEEE. DOI 10.1109/ISRITI68345.2025.11393290.

[IEEE Xplore](https://ieeexplore.ieee.org/abstract/document/11393290)

Metadata/abstrak terverifikasi; full text serta metadata penulis belum diverifikasi dari sumber primer yang dapat dibaca. Belum dimasukkan ke BibTeX final. Baca setelah sumber inti; jangan mengambil angka hasilnya sebagai pembanding langsung tanpa menyamakan dataset dan protokol.

## 3. Peta literatur dan batas kebaruan

| Yang sudah diteliti | Sumber utama | Implikasi |
|---|---|---|
| Atribusi prediksi melalui SHAP | R2 | Menggunakan SHAP bukan kebaruan |
| Penjelasan model pohon melalui TreeSHAP | R3 | Memakai Random Forest/TreeSHAP bukan kebaruan |
| Perbedaan permainan dan pengaruh korelasi | R4, R5, R6 | Perbandingan atribusi tidak otomatis menguji siapa yang benar |
| Stabilitas antarseed pada dataset kredit Taiwan | R7 | Dataset sama plus seed berbeda sudah pernah dilakukan |
| Dampak imbalance pada penjelasan kredit | R8 | Sampling dan rasio kelas harus dikontrol |
| Aplikasi SHAP pada penilaian kredit | R9 | Paper perlu lebih spesifik daripada menampilkan feature importance |

Posisi kerja yang aman: **studi empiris terfokus tentang sensitivitas pembagian atribusi pada kelompok tagihan berkorelasi terhadap pilihan mode TreeSHAP, dengan pemeriksaan lokal, global, dan pengulangan pelatihan**.

Posisi ini adalah deskripsi lingkup, belum bukti kebaruan. Kontribusi potensial perlu diperiksa terhadap metode lengkap dan kode R6/R7 serta penelitian turunannya. Jangan menulis “belum ada penelitian”, “pertama”, atau “menyelesaikan bias korelasi” berdasarkan pencarian awal.

## 4. Rumusan masalah dan tujuan

### Latar masalah dalam bahasa sederhana

Jumlah tagihan seorang nasabah pada bulan yang berdekatan sering bergerak bersama. Model dapat menggunakan beberapa bulan tersebut untuk membuat prediksi gagal bayar. Namun, pembagian atribusi terhadap masing-masing bulan bergantung pada cara mendefinisikan informasi fitur yang tidak tersedia. Kita ingin mengetahui seberapa besar pilihan mode TreeSHAP mengubah pembagian tersebut dan apakah kesimpulan fitur utama tetap bertahan.

### Rumusan utama

**Bagaimana pilihan mode interventional dan tree-path-dependent pada TreeSHAP memengaruhi pembagian atribusi antarfitur tagihan yang berkorelasi dalam prediksi gagal bayar kartu kredit?**

RQ1: Pada model dan observasi yang sama, seberapa besar nilai atribusi lokal serta ranking global fitur tagihan berbeda antara kedua mode?

RQ2: Apakah identitas fitur tagihan yang paling berkontribusi berubah, dan seberapa sering perubahan tersebut terjadi pada observasi yang dievaluasi?

RQ3 (pendukung): Apakah pola perbedaan mode bertahan pada beberapa pengulangan pelatihan dengan seed berbeda?

Untuk RQ2 tetapkan apakah “paling berkontribusi” diukur berdasarkan magnitudo absolut atau kontribusi positif terhadap kelas gagal bayar. Kedua ukuran menjawab pertanyaan berbeda. Hindari memilih definisi setelah melihat hasil.

### Tujuan

1. Mengukur kesepakatan dan perbedaan atribusi kedua mode pada satu prediktor yang sama.
2. Menilai dampak perbedaan terhadap kesimpulan tentang fitur tagihan utama.
3. Memeriksa kestabilan temuan antarpelatihan tanpa mencampurkan perubahan test/background.
4. Menjelaskan hasil melalui konsep nilai koalisi dan Shapley, dengan membatasi interpretasi pada perilaku model.

Judul kerja: **Sensitivity of TreeSHAP Attribution Allocation among Correlated Billing Features in Credit Card Default Prediction**.

### Batas yang perlu disepakati dengan tim

- Satu model Random Forest untuk pilot; seluruh fitur relevan dapat digunakan model, tetapi analisis utama fokus pada BILL_AMT1-BILL_AMT6.
- Jangan menghapus semua fitur berkorelasi karena justru itulah objek penelitian.
- Simpan encoding, train/validation/test, kelas target, dan observasi yang dijelaskan secara konsisten.
- Background interventional diambil dari train dan tetap untuk perbandingan utama. Path-dependent memakai informasi jalur pohon; tidak memiliki distribusi referensi yang identik secara otomatis.
- Pilih keluaran kelas gagal bayar dalam satuan yang konsisten. Baseline tiap mode dapat berbeda dan wajib dilaporkan.
- Perbandingan mode dalam setiap run harus menggunakan model yang persis sama. Variasi antarrun merupakan sumber variasi berbeda.
- Penjumlahan atribusi enam tagihan boleh disebut agregat atribusi kelompok, bukan otomatis Shapley permainan baru dengan enam fitur sebagai satu pemain.
- Dataset ini observasional dengan riwayat tetap enam bulan per nasabah; penelitian tidak mengklaim penyebab gagal bayar atau representasi nasabah Indonesia saat ini.

## 5. Penjelasan Shapley untuk pegangan

### 5.1 Intuisi dasarnya

Bayangkan beberapa pemain menghasilkan suatu nilai bersama. Tambahan nilai dari seorang pemain dapat bergantung pada siapa yang sudah bergabung. Shapley menghitung rata-rata tambahan kontribusi pemain tersebut pada semua urutan bergabung yang mungkin. Dengan demikian, kontribusi tidak ditentukan hanya dari satu urutan.

Dalam penjelasan model, pemain adalah fitur dan nilai yang dibagi adalah selisih keluaran model terhadap baseline. Satu nasabah merupakan satu kasus penjelasan. Mengubah definisi nilai koalisi dapat mengubah permainan dan pembagiannya. Landasan: R1 dan R5.

### 5.2 Contoh hitungan dua pemain

Contoh ini sengaja dibuat untuk belajar; bukan hasil model atau data kelompok. Misalkan hanya ada dua pemain A dan B dengan nilai koalisi dalam ruang probabilitas:

| Informasi tersedia menurut permainan | Nilai |
|---|---:|
| Tidak ada, v(kosong) | 0,20 |
| A saja, v(A) | 0,32 |
| B saja, v(B) | 0,26 |
| A dan B, v(A,B) | 0,40 |

Ada dua urutan: A lalu B dan B lalu A.

- A terlebih dahulu: kontribusi A = 0,32-0,20 = 0,12.
- A setelah B: kontribusi A = 0,40-0,26 = 0,14.
- Nilai Shapley A = (0,12+0,14)/2 = 0,13.
- B terlebih dahulu: kontribusi B = 0,26-0,20 = 0,06.
- B setelah A: kontribusi B = 0,40-0,32 = 0,08.
- Nilai Shapley B = (0,06+0,08)/2 = 0,07.

Pemeriksaan: 0,20+0,13+0,07 = 0,40. A menambah 13 poin persentase dan B menambah 7 poin persentase relatif terhadap baseline dalam contoh permainan ini. Ini bukan persentase sebab-akibat. Pada model yang dijelaskan dalam log-odds, satuannya berbeda dan hitungan tidak boleh diberi label poin persentase.

### 5.3 Rumus umum

Untuk himpunan fitur N berukuran M dan koalisi S:

\[
\phi_i(x)=\sum_{S\subseteq N\setminus\{i\}}
\frac{|S|!(M-|S|-1)!}{M!}
\left[v_x(S\cup\{i\})-v_x(S)\right].
\]

Bagian dalam kurung adalah tambahan nilai dari fitur i. Bobotnya mewakili proporsi urutan yang menempatkan S sebelum fitur i. Koalisi bukan berarti model harus selalu dilatih ulang hanya dengan fitur S. Dalam eksperimen TreeSHAP kelompok, prediktor tetap; yang berubah adalah cara memberi nilai pada informasi yang tidak tersedia. Sumber konseptual: R1-R5.

### 5.4 Sifat yang perlu dipahami

| Sifat | Makna dalam permainan yang telah ditetapkan |
|---|---|
| Efisiensi | Total atribusi sama dengan nilai seluruh fitur dikurangi nilai koalisi kosong |
| Simetri | Pemain dengan tambahan kontribusi identik untuk semua koalisi mendapat bagian sama |
| Dummy | Pemain yang tambahan kontribusinya selalu nol memperoleh nol |
| Aditivitas | Shapley dari penjumlahan dua permainan sama dengan penjumlahan Shapley keduanya |

Simetri tidak berarti dua fitur yang sekadar berkorelasi tinggi harus mendapat nilai sama. Fitur yang tidak dipakai model juga belum tentu dummy dalam permainan conditional karena ia bisa membawa informasi tentang fitur lain. Sifat matematis ini tidak otomatis membuktikan fairness sosial atau ketepatan kausal. R1, R4, R5.

### 5.5 SHAP, TreeSHAP, dan mode implementasi

**Shapley:** konsep pembagian nilai permainan kooperatif. **SHAP:** kerangka penjelasan aditif untuk kontribusi fitur terhadap prediksi. **TreeSHAP:** algoritme untuk menghitung atribusi model pohon menurut asumsi permainan tertentu. Jadi, SHAP/TreeSHAP menjelaskan model; prediksi tetap dibuat Random Forest atau model pohon lain. R2-R3.

Untuk interventional dengan background empiris B:

\[
v_x^{int}(S)=\frac{1}{|B|}\sum_{b\in B}f(x_S,b_{\bar S}).
\]

Fitur dalam S berasal dari nasabah x dan fitur lain dari baris background. Ketergantungan antara bagian yang dipertahankan dan diganti diputus; ketergantungan antarkolom yang diambil bersama dari satu baris background tetap dapat dipertahankan. Maka jangan menyatakan semua fitur selalu dianggap saling independen secara menyeluruh.

Sebagai pembanding konseptual, permainan conditional ideal adalah:

\[
v_x^{cond}(S)=E[f(X)\mid X_S=x_S].
\]

**Tree-path-dependent bukan conditional ideal tersebut.** Ia menggunakan struktur pohon dan frekuensi sampel pelatihan pada jalurnya. Nama perbandingan eksperimen harus tetap interventional versus tree-path-dependent. Pembahasan conditional membantu memahami persoalan informasi, bukan label pengganti mode implementasi. R3-R6 dan [dokumentasi TreeExplainer](https://shap.readthedocs.io/en/latest/generated/shap.TreeExplainer.html).

Untuk satu observasi, laporkan phi0+sum(phi)=f(x) dalam satuan keluaran yang sama. Untuk ranking global gunakan mean absolute SHAP, bukan rata-rata signed SHAP yang dapat saling meniadakan. Jika membahas bagian tagihan, bedakan ranking di antara enam tagihan dan ranking di antara seluruh fitur.

## 6. Draf latar belakang dalam bahasa Indonesia

Prediksi gagal bayar kartu kredit dapat memanfaatkan riwayat tagihan, status pembayaran, dan informasi nasabah. Selain kemampuan prediksi, penjelasan mengenai kontribusi fitur diperlukan untuk memahami perilaku model. Studi sebelumnya telah menerapkan SHAP pada penilaian kredit dan meneliti stabilitas penjelasannya [R7-R9].

Dalam kerangka SHAP, fitur diperlakukan sebagai pemain dalam permainan kooperatif. Namun, nilai atribusi bergantung pada definisi nilai koalisi dan perlakuan terhadap fitur yang tidak diketahui. Ketika fitur saling berkorelasi, pilihan definisi permainan dapat menghasilkan penjelasan yang berbeda tanpa otomatis menunjukkan kesalahan salah satu pendekatan [R2,R4,R5]. Penelitian korelasi lintas-explainer juga telah dilakukan, termasuk pada dua mode TreeSHAP [R6].

Penelitian ini dirancang sebagai studi empiris terfokus pada pembagian atribusi di antara fitur jumlah tagihan bulanan dalam prediksi gagal bayar kartu kredit. Dua mode TreeSHAP dibandingkan pada model serta observasi yang sama. Analisis mencakup perbedaan nilai lokal, perubahan ranking global, dan konsistensi temuan antarpengulangan pelatihan. Tujuannya adalah menilai dampak pilihan mode terhadap kesimpulan interpretasi, bukan menentukan penyebab gagal bayar atau mengusulkan algoritme Shapley baru.

## 7. Draf Introduction bahasa Inggris

Credit card default prediction can use customers' billing and repayment histories to estimate future default outcomes. Explaining the resulting predictions is useful for understanding model behavior, beyond reporting predictive performance alone. Previous studies have applied SHAP to credit assessment and examined the stability of explanations in credit risk models [R7-R9].

SHAP connects feature attribution to cooperative game theory by allocating a model output relative to a reference value among input features [R1,R2]. However, the resulting allocation depends on the coalition value function and the treatment of unavailable features [R4,R5]. This distinction matters when predictors contain overlapping information. Prior work has investigated correlation effects across explanation methods, including interventional and path-dependent TreeSHAP [R6]. Therefore, neither applying SHAP to credit default prediction nor repeating model training is, by itself, a new contribution [R7].

This study examines how the choice between interventional and tree-path-dependent TreeSHAP affects attribution allocation among correlated monthly billing features in credit card default prediction. The two modes are compared using the same fitted model and evaluation observations within each run. We assess local attribution differences, global ranking agreement, and the persistence of mode-related differences across repeated model fits. The study is positioned as a focused empirical replication and extension, with conclusions restricted to the fitted models, explanation settings, and dataset examined.

Draf ini tidak boleh diberi kalimat hasil atau klaim metode unggul sebelum eksperimen. Penanda R1-R9 harus diganti sitasi yang dikelola secara konsisten pada naskah final. Urutan nomor pustaka mengikuti urutan kemunculan pada naskah, bukan nomor panduan baca.

## 8. Template catatan baca per paper

Salin satu blok untuk setiap paper:

- Identitas: judul, penulis, tahun, venue, DOI/URL.
- Status bacaan: abstrak saja / metode / teks penuh / suplemen / kode.
- Masalah yang dijawab:
- Dataset dan target:
- Model prediksi:
- Explainer dan mode yang dinyatakan eksplisit:
- Background dan satuan keluaran:
- Unit evaluasi: lokal / global / kelompok fitur.
- Yang divariasikan dan yang dijaga tetap:
- Metrik dan temuan yang benar-benar dilaporkan:
- Batasan dan kemungkinan masalah validitas:
- Klaim yang didukung untuk paper kelompok:
- Persamaan/perbedaan terhadap rancangan kelompok:
- Lokasi bukti: halaman, bagian, tabel, atau kutipan pendek.
- Pertanyaan yang belum terjawab:

Jika mode/background tidak jelas, catat “tidak ditemukan pada bagian yang dibaca”, bukan menebak konfigurasi default. Setiap klaim kebaruan memerlukan bukti lebih kuat daripada tidak menemukan satu kata pada abstrak.

## 9. Checklist serah-terima Daffa

- [ ] Dapat menjelaskan pemain, koalisi, nilai koalisi, dan contoh hitungan dua pemain.
- [ ] Dapat membedakan prediktor, SHAP, dan TreeSHAP.
- [ ] Memahami bahwa path-dependent bukan conditional SHAP eksak.
- [ ] R2, R6, dan R7 sudah dibaca pada bagian yang relevan, bukan hanya ringkasan ini.
- [ ] Matriks bacaan membedakan metadata/abstrak dengan telaah teks penuh.
- [ ] Rumusan masalah utama dan analisis pendukung sudah disepakati tim.
- [ ] Posisi terhadap paper energi dan paper kredit antarseed dinyatakan jujur.
- [ ] Introduction memiliki alur konteks, persoalan atribusi, penelitian terdahulu, dan tujuan.
- [ ] Tidak ada angka hasil model yang dikarang, klaim kausal, atau klaim penelitian pertama.
- [ ] Daftar pustaka dicocokkan lagi dengan versi paper yang benar-benar dibaca.
