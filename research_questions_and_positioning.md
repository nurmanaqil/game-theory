# Bagian Daffa: rumusan masalah, landasan teori, referensi, dan posisi penelitian

Versi untuk tinjauan kelompok, 20 Oktober 2026. Angka hasil model belum tersedia. Nomor [1]-[9] mengikuti sembilan bacaan utama dalam pegangan sebelumnya; nomor pada naskah final disesuaikan urutan sitasi. Dokumen ini disusun dari sumber primer yang dapat diakses, dengan batas telaah dijelaskan pada bagian akhir.

## A. Judul sementara

**Sensitivitas Pembagian Atribusi Fitur Tagihan Berkorelasi terhadap Pilihan Mode TreeSHAP pada Prediksi Gagal Bayar Kartu Kredit**

Judul bahasa Inggris: **Sensitivity of Attribution Allocation among Correlated Billing Features to TreeSHAP Mode Selection in Credit Card Default Prediction**.

## B. Latar belakang

Prediksi gagal bayar kartu kredit memanfaatkan informasi nasabah dan riwayat keuangannya untuk memperkirakan kemungkinan gagal membayar pada periode berikutnya. Penelitian sebelumnya telah menerapkan SHAP untuk menjelaskan model penilaian kredit [9] dan memeriksa kestabilan penjelasan pada dataset kredit [7], [8]. Karena itu, penerapan SHAP pada prediksi gagal bayar bukan hal baru. Pertanyaan yang perlu dipersempit adalah bagaimana pengaturan penjelasan memengaruhi kesimpulan mengenai kontribusi fitur.

SHAP menghubungkan penjelasan prediksi dengan nilai Shapley dalam permainan kooperatif [1], [2]. Fitur diperlakukan sebagai pemain, sedangkan kontribusi ditentukan dari tambahan nilai ketika suatu fitur bergabung dengan koalisi. Namun, pembagian tersebut bergantung pada fungsi nilai koalisi. Perbedaan cara memperlakukan fitur yang informasinya tidak tersedia dapat menghasilkan atribusi berbeda, khususnya ketika fitur saling berkaitan [4], [5].

Dalam konteks kartu kredit, jumlah tagihan beberapa bulan dari nasabah yang sama berpotensi membawa informasi yang tumpang tindih. TreeSHAP menyediakan pendekatan interventional dan tree-path-dependent untuk menjelaskan model pohon [3]. Pilihan tersebut perlu dinyatakan secara eksplisit karena penjelasan dengan asumsi yang berbeda tidak otomatis menjawab pertanyaan yang sama. Tree-path-dependent juga tidak dapat diperlakukan sebagai perhitungan conditional SHAP yang eksak.

Penelitian korelasi lintasmetode SHAP, termasuk dua mode TreeSHAP, sudah dilakukan dalam konteks energi [6]. Pada konteks kredit, pengulangan pelatihan dan analisis ranking SHAP juga telah diteliti menggunakan dataset yang sama dengan kelompok [7]. Oleh sebab itu, penelitian ini diposisikan sebagai replikasi dan pengembangan empiris yang terfokus pada sensitivitas pembagian atribusi antarfitur tagihan, bukan pengusulan algoritme SHAP baru. Analisis dirancang untuk menghubungkan perubahan nilai lokal, perubahan ranking global, dan konsistensi temuan antarhasil pelatihan.

## C. Identifikasi masalah

1. Fitur jumlah tagihan antarbulan dapat membawa informasi yang saling tumpang tindih, sehingga interpretasi kontribusi setiap bulan memerlukan perhatian terhadap aturan atribusi.
2. Pilihan mode TreeSHAP dapat mengubah pembagian kontribusi meskipun model dan observasi yang dijelaskan tetap sama.
3. Kesepakatan ranking global belum cukup untuk menyimpulkan bahwa penjelasan pada setiap nasabah juga sepakat.
4. Perubahan akibat mode explainer perlu dibedakan dari variasi akibat pelatihan model dan pemilihan background.

Poin 2-4 merupakan persoalan yang hendak diuji, bukan hasil yang sudah terbukti terjadi pada model kelompok. Besar perbedaan dapat kecil dan hasil seperti itu tetap perlu dilaporkan.

## D. Rumusan masalah

### Pertanyaan utama

**Bagaimana pilihan mode interventional dan tree-path-dependent pada TreeSHAP memengaruhi pembagian atribusi antarfitur tagihan yang berkorelasi dalam prediksi gagal bayar kartu kredit?**

### Pertanyaan penelitian operasional

**RQ1.** Pada model dan observasi yang sama, seberapa besar perbedaan atribusi kedua mode untuk masing-masing fitur BILL_AMT1 sampai BILL_AMT6?

**RQ2.** Sejauh mana perbedaan tersebut mengubah ranking global dan identitas fitur tagihan dengan magnitudo kontribusi terbesar pada nasabah individual?

**RQ3.** Bagaimana kesepakatan agregat atribusi kelompok tagihan dibandingkan dengan pembagian atribusi di antara fitur-fitur di dalam kelompok tersebut?

**RQ4, pendukung.** Apakah pola kesepakatan atau ketidaksepakatan kedua mode bertahan pada beberapa pengulangan pelatihan dengan seed berbeda?

Untuk UTS, prioritaskan RQ1-RQ2. RQ3 memakai hasil atribusi yang sama dan dapat dimasukkan jika pilot sudah stabil. RQ4 menjadi pemeriksaan penguatan, bukan klaim kebaruan utama.

## E. Tujuan penelitian

1. Mengukur perbedaan atribusi fitur tagihan antara dua mode TreeSHAP pada model tetap.
2. Menilai dampaknya terhadap kesimpulan fitur tagihan terpenting pada tingkat lokal dan global.
3. Membandingkan atribusi agregat kelompok tagihan dengan pembagian atribusi internalnya.
4. Memeriksa konsistensi temuan pada pengulangan pelatihan yang dikendalikan.

## F. Ruang lingkup dan rancangan pengujian

- Dataset: Default of Credit Card Clients dari UCI, diperoleh melalui Kaggle; target adalah default.payment.next.month. Sumber data harus tetap disitasi di luar sembilan referensi teori/aplikasi ini.
- Model awal: Random Forest Classifier. Penggunaan model ini merupakan pilihan lingkup, bukan bukti bahwa ia lebih unggul dari XGBoost.
- Model dapat memakai fitur lain yang relevan. Fokus evaluasi atribusi adalah BILL_AMT1-BILL_AMT6; ID tidak menjadi prediktor.
- Pembagian train/validation/test serta preprocessing disimpan tetap. Pasangan/kelompok korelasi dikonfirmasi pada train.
- Dalam satu run, kedua mode memakai fitted model dan sampel penjelasan yang sama. Background interventional berasal dari train; jalur pohon pada path-dependent tidak dianggap mempunyai referensi identik secara otomatis.
- Kelas gagal bayar dan satuan keluaran ditetapkan eksplisit. Untuk Random Forest, periksa bahwa nilai yang dibandingkan benar-benar mengacu pada keluaran kelas gagal bayar yang sama. Baseline tiap mode dan additivity residual dilaporkan.
- Jika seed pelatihan diubah, split, background interventional, dan sampel evaluasi dijaga tetap. Dengan demikian perbandingan mode dalam run dan variasi model antarrun dapat dilaporkan terpisah.
- Threshold keputusan atau kategori profil nasabah tidak dipilih setelah melihat hasil test.
- Tidak ada klaim kausal, fairness sosial yang terjamin, atau penerapan langsung pada nasabah Indonesia.

### Ukuran yang menjawab rumusan masalah

| Pertanyaan | Ukuran utama | Makna |
|---|---|---|
| RQ1 | Rata-rata selisih absolut nilai SHAP berpasangan | Besar perubahan atribusi pada model serta nasabah yang sama |
| RQ2 global | Spearman ranking berdasarkan mean absolute SHAP | Kesepakatan urutan kepentingan pada populasi evaluasi |
| RQ2 lokal | Proporsi nasabah yang fitur tagihan teratasnya berbeda antara mode | Apakah rata-rata global menyembunyikan ketidaksepakatan individual |
| RQ3 | Atribusi signed agregat kelompok dan proporsi mean absolute SHAP per fitur dalam kelompok | Apakah perubahan terutama berupa pembagian ulang di dalam kelompok |
| RQ4 | Distribusi ukuran-ukuran tersebut antarseed | Apakah temuan bertahan pada hasil pelatihan lain |

“Teratas” pada analisis utama berarti magnitudo absolut terbesar di antara enam fitur tagihan. Ini berbeda dari fitur yang paling menaikkan prediksi gagal bayar; jika ukuran kedua dipakai, beri nama dan analisis terpisah. Tentukan penanganan ties dan atribusi kelompok mendekati nol sebelum evaluasi utama.

Untuk RQ3, jumlahkan nilai SHAP individual sebagai agregat. Jangan menyebutnya Shapley dari permainan dengan satu pemain gabungan tanpa menghitung ulang permainan tersebut. Karena baseline mode dapat berbeda, perubahan agregat perlu dibaca bersama kontribusi fitur di luar kelompok dan baseline.

## G. Landasan Shapley, SHAP, dan TreeSHAP

Nilai Shapley adalah aturan pembagian nilai dalam permainan kooperatif. Seorang pemain diberi rata-rata kontribusi marginalnya pada seluruh kemungkinan urutan masuk ke koalisi [1]. Dalam penjelasan model, pemain adalah fitur, koalisi adalah subset fitur, dan fungsi nilai menentukan bagaimana keluaran model dinilai ketika hanya informasi subset tersebut tersedia [2], [5].

Untuk himpunan M fitur N, nilai Shapley fitur i pada observasi x dituliskan:

\[
\phi_i(x)=\sum_{S\subseteq N\setminus\{i\}}
\frac{|S|!(M-|S|-1)!}{M!}
\left[v_x(S\cup\{i\})-v_x(S)\right].
\]

Bagian dalam kurung merupakan tambahan nilai akibat fitur i. Bobotnya memperhitungkan seluruh urutan bergabung. Sifat efisiensi, simetri, dummy, dan aditivitas berlaku terhadap permainan yang sudah ditentukan. Fitur yang sekadar berkorelasi tinggi belum tentu simetris dalam permainan; sifat matematis ini juga bukan jaminan keadilan sosial.

SHAP merupakan kerangka penjelasan aditif, sedangkan TreeSHAP menyediakan algoritme bagi model pohon [2], [3]. Model prediksi tetap Random Forest. Untuk satu observasi, baseline ditambah jumlah atribusi harus sesuai keluaran yang dijelaskan. Atribusi global dapat diringkas menggunakan rata-rata nilai absolut pada populasi evaluasi.

Interventional mengganti fitur yang tidak dipertahankan menggunakan baris background. Hubungan antara fitur yang dipertahankan dan yang diganti terputus, tetapi kolom-kolom yang diambil bersama dari satu baris background tetap dapat memiliki ketergantungan. Tree-path-dependent memakai struktur pohon dan frekuensi sampel pada jalurnya. Ia tidak sama dengan oracle distribusi kondisional. Perbedaan keduanya dibahas sebagai konsekuensi pengaturan penjelasan, bukan otomatis kesalahan atau bukti keunggulan salah satu mode [3]-[6].

## H. Daftar referensi utama

[1] L. S. Shapley, “A Value for n-Person Games,” dalam *Contributions to the Theory of Games, Volume II*, H. W. Kuhn dan A. W. Tucker, Eds. Princeton University Press, 1953. DOI: [10.1515/9781400881970-018](https://doi.org/10.1515/9781400881970-018).

[2] S. M. Lundberg dan S.-I. Lee, “A Unified Approach to Interpreting Model Predictions,” *Advances in Neural Information Processing Systems*, vol. 30, pp. 4765-4774, 2017. [Halaman resmi](https://proceedings.neurips.cc/paper/2017/hash/8a20a8621978632d76c43dfd28b67767-Abstract.html).

[3] S. M. Lundberg, G. Erion, H. Chen, A. DeGrave, J. M. Prutkin, B. Nair, R. Katz, J. Himmelfarb, N. Bansal, dan S.-I. Lee, “From local explanations to global understanding with explainable AI for trees,” *Nature Machine Intelligence*, vol. 2, pp. 56-67, 2020. DOI: [10.1038/s42256-019-0138-9](https://doi.org/10.1038/s42256-019-0138-9).

[4] H. Chen, J. D. Janizek, S. Lundberg, dan S.-I. Lee, “True to the Model or True to the Data?,” arXiv preprint arXiv:2006.16234, 2020. [Naskah penulis](https://arxiv.org/abs/2006.16234).

[5] M. Sundararajan dan A. Najmi, “The Many Shapley Values for Model Explanation,” dalam *Proceedings of the 37th International Conference on Machine Learning*, PMLR, vol. 119, pp. 9269-9278, 2020. [Halaman resmi](https://proceedings.mlr.press/v119/sundararajan20b.html).

[6] A. Nikoltchovska, S. Pütz, M. Götz, dan B. Schäfer, “Correlations Matter in Explanations for Energy Systems,” *KI - Künstliche Intelligenz*, vol. 40, pp. 41-54, 2026. DOI: [10.1007/s13218-026-00904-4](https://doi.org/10.1007/s13218-026-00904-4).

[7] L. Lin dan Y. Wang, “SHAP Stability in Credit Risk Management: A Case Study in Credit Card Default Model,” *Risks*, vol. 13, no. 12, artikel 238, 2025. DOI: [10.3390/risks13120238](https://doi.org/10.3390/risks13120238). [Preprint terbuka](https://arxiv.org/pdf/2508.01851).

[8] Y. Chen, R. Calabrese, dan B. Martin-Barragan, “Interpretable machine learning for imbalanced credit scoring datasets,” *European Journal of Operational Research*, vol. 312, no. 1, pp. 357-372, 2024. DOI: [10.1016/j.ejor.2023.06.036](https://doi.org/10.1016/j.ejor.2023.06.036). [Repositori penulis](https://www.research.ed.ac.uk/en/publications/interpretable-machine-learning-for-imbalanced-credit-scoring-data/).

[9] Q. Xu, Y. Liao, Q. Li, J. Zhang, Z. Song, L. Wang, dan X. Yuan, “SHAP-based Interpretable Models for Credit Default Assessment Using Machine Learning,” dalam *2024 14th International Conference on Software Technology and Engineering (ICSTE)*, IEEE, pp. 213-217, 2024. DOI: [10.1109/ICSTE63875.2024.00044](https://doi.org/10.1109/ICSTE63875.2024.00044). [Metadata institusi penulis](https://research.mpu.edu.mo/en/publications/shap-based-interpretable-models-for-credit-default-assessment-usi/).

Referensi data tambahan, di luar sembilan bacaan di atas: I. Yeh, *Default of Credit Card Clients*, UCI Machine Learning Repository, 2009, DOI [10.24432/C55S3H](https://doi.org/10.24432/C55S3H). [Mirror Kaggle](https://www.kaggle.com/datasets/uciml/default-of-credit-card-clients-dataset).

Referensi implementasi tambahan: [shap.TreeExplainer, dokumentasi resmi](https://shap.readthedocs.io/en/latest/generated/shap.TreeExplainer.html). Catat versi pustaka saat eksperimen, bukan sekadar dokumentasi latest.

## I. Perbandingan terhadap sembilan sumber

Lima bacaan pertama terutama landasan konsep atau metode, bukan sembilan pesaing yang semuanya perlu dikalahkan. Pembeda terhadap suatu paper tidak membuktikan kebaruan terhadap seluruh literatur.

| Sumber | Fokus sumber | Hubungan atau pembeda rancangan kelompok |
|---|---|---|
| [1] Shapley | Dasar pembagian nilai permainan kooperatif | Menjadi fondasi. Kelompok tidak memperbaiki teorema; mengoperasionalkan konsep pada penjelasan model kredit. |
| [2] Lundberg dan Lee | Kerangka SHAP | Kelompok menggunakan kerangka tersebut untuk evaluasi sensitivitas pengaturan, bukan mengusulkan SHAP baru. |
| [3] Lundberg dkk. | Algoritme dan alat penjelasan model pohon | Kelompok mengevaluasi implikasi pemakaian dua mode pada kasus tagihan; tidak mengklaim algoritme lebih cepat atau akurat. |
| [4] Chen dkk. | Tujuan interventional/observational, dengan analisis model linear | Kelompok menguji dua mode implementasi TreeSHAP pada model pohon. Path-dependent tidak dilabeli conditional ideal. |
| [5] Sundararajan dan Najmi | Perbedaan operasionalisasi nilai Shapley | Menjadi dasar interpretasi hasil; kelompok tidak mengklaim aksioma atau solusi teoritis baru. |
| [6] Nikoltchovska dkk. | Korelasi dan perbandingan banyak explainer pada sintetis serta energi | Kasus kredit dan pengukuran lokal/global merupakan perubahan fokus. Perbandingan mode maupun eksperimen korelasi sendiri sudah ada. |
| [7] Lin dan Wang | Stabilitas ranking SHAP pada dataset kredit sama dengan 100 seed XGBoost | Kelompok memprioritaskan perbandingan mode berpasangan pada fitted model yang sama, serta ketidaksepakatan individual. Dataset, seed, dan ranking subgroup tagihan tidak menjadi klaim baru. |
| [8] Chen dkk. | Dampak perubahan imbalance pada stabilitas SHAP/LIME di kredit | Kelompok menjaga rasio/sampling dan split tetap; variabel eksperimen utama adalah mode TreeSHAP, bukan tingkat imbalance. |
| [9] Xu dkk., IEEE | Aplikasi SHAP untuk penilaian kredit Lending Club | Kelompok menilai sensitivitas atribusi tagihan pada Taiwan, bukan hanya mengurutkan fitur. Berdasarkan abstrak, belum dapat dipastikan seluruh rincian metode [9]. |

Khusus [7]: preprint juga melaporkan Kendall's W untuk subgroup tagihan. Karena itu kalimat “penelitian sebelumnya hanya menilai semua fitur dan belum menilai kelompok tagihan” tidak didukung. Pada teks preprint yang diperiksa, perbandingan dua mode secara eksplisit tidak ditemukan; versi jurnal dan kode masih perlu dicocokkan sebelum menyatakan hal itu tidak dilakukan penulis.

## J. Hal yang dapat dibuat lebih baik dalam rancangan kita

Kata “lebih baik” di sini berarti ketelitian desain untuk menjawab pertanyaan kelompok. Belum berarti model lebih akurat, explainer lebih benar, atau paper lebih unggul daripada penelitian terdahulu.

1. **Pisahkan sumber variasi.** Bandingkan dua mode pada model tetap di setiap run; gunakan hasil antarseed sebagai lapisan terpisah. Ini membuat pertanyaan tentang pengaturan explainer lebih mudah dinilai.
2. **Hubungkan hasil global dengan kasus individual.** Laporkan kesepakatan ranking global bersama frekuensi perubahan fitur tagihan teratas per nasabah. Hasil global yang sepakat tidak menjamin semua penjelasan individual sepakat.
3. **Periksa atribusi kelompok dan pembagiannya sekaligus.** Tanyakan apakah perbedaan terdapat pada total agregat atau pembagian internal. Tetap bedakan agregasi dari permainan dengan pemain gabungan.
4. **Buat pengaturan penjelasan transparan.** Simpan versi pustaka, mode, background, kelas keluaran, baseline, dan indeks sampel. Periksa additivity pada satuan yang konsisten.
5. **Laporkan ketidakpastian dan hasil kecil/nol.** Jangan memilih seed atau kasus individual yang mendukung cerita. Jika kedua mode hampir sama, jelaskan batas temuan pada model serta data yang diuji.

Semua praktik tersebut merupakan rancangan kontribusi empiris dan reproducibility, bukan jaminan kebaruan. Jika ingin menyatakan keunggulan kuantitatif, tetapkan ukuran, pembanding yang sebanding, dan kriteria sebelum eksperimen. Saat ini belum ada hasil untuk mendukung klaim tersebut.

### Pernyataan kontribusi yang dapat dipakai

“Penelitian ini mengevaluasi sensitivitas pembagian atribusi antarfitur tagihan berkorelasi terhadap pilihan mode TreeSHAP dalam prediksi gagal bayar kartu kredit. Evaluasi dilakukan secara berpasangan pada model dan observasi yang sama, dengan analisis pada tingkat lokal, global, dan agregat kelompok tagihan. Pengulangan pelatihan digunakan untuk memeriksa konsistensi temuan. Kontribusi penelitian berupa bukti empiris dan protokol evaluasi yang terdokumentasi pada konfigurasi yang diuji.”

### Klaim yang belum boleh ditulis

- Penelitian pertama yang membahas korelasi pada SHAP atau stabilitas SHAP untuk kartu kredit.
- Mengatasi masalah korelasi atau membuktikan satu mode paling benar.
- Model lebih akurat dari penelitian sebelumnya tanpa perbandingan yang setara.
- Random Forest menggantikan XGBoost merupakan kebaruan metode.
- Penelitian terdahulu tidak memiliki suatu analisis hanya karena abstraknya tidak menyebutkannya.
- SHAP menunjukkan penyebab nasabah gagal bayar atau menjamin keputusan kredit adil.

## K. Batas telaah sumber untuk tinjauan Daffa

- [1]: metadata dan pengantar penerbit, bukan telaah lengkap bab.
- [2]-[3]: konsep dan bagian metode yang tersedia telah ditelusuri; seluruh suplemen/kode belum direplikasi.
- [4]-[5]: metadata dan abstrak resmi serta konsep terkait ditelaah; detail pembuktian perlu dibaca sebelum dikutip khusus.
- [6]: teks terbuka bagian desain, metode perbandingan, dan hasil relevan diperiksa.
- [7]: metode dan evaluasi preprint diperiksa. Versi jurnal tersedia, tetapi perbedaan revisinya belum diaudit lengkap.
- [8]: metadata dan abstrak repositori penulis diverifikasi; telaah penuh metode masih diperlukan.
- [9]: metadata/abstrak institusi penulis diverifikasi; full text belum diperiksa.

Urutan tinjauan paling penting: [7] untuk mencegah duplikasi klaim, [6] untuk konteks korelasi, lalu [4]-[5] untuk interpretasi permainan. Sesudah itu selaraskan rumusan penelitian dengan anggota data, model, dan TreeSHAP sebelum mengunci naskah.
