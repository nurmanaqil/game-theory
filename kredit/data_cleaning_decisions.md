# Keputusan pembersihan: tahap 1-3

Semua keputusan di bawah terdokumentasi. Tidak ada baris dihapus, nilai diubah, encoding diterapkan, atau split dibuat pada tahap ini. Kolom baris terkait bukan jumlah baris yang akan dibuang.

| kode | isu | temuan | keputusan | alasan | status |
| --- | --- | --- | --- | --- | --- |
| P01 | Data mentah | 30,000 baris, 25 kolom | Bekukan snapshot dan verifikasi SHA-256; sumber asli tidak ditimpa | Mencegah perubahan data tanpa jejak | Selesai: snapshot dan manifest dibuat |
| P02 | Kolom ID | 30,000 ID unik | Keluarkan dari X, tetap simpan sebagai metadata | ID bukan prediktor substantif atau urutan waktu | Ditetapkan; diterapkan pada tahap persiapan X/y |
| P03 | Target | Kode 0/1; gagal bayar 22.12% pada file ini | Pisahkan target dari X; jaga proporsi kelas pada pembagian | Menghindari kebocoran target dan evaluasi menyesatkan | Ditetapkan; belum membuat split |
| P04 | Missing/nonfinite | 0 sel kosong; 0 nonfinite | Tidak melakukan imputasi pada data saat ini | Tidak ada missing numerik yang memerlukan pengisian | Ditetapkan; tidak ada pengisian |
| P05 | EDUCATION 0/5/6 | 345 baris | Pemetaan deterministik 0/5/6 -> kategori unknown; 4 tetap others | S1 tidak menjelaskan kode tersebut lengkap; jangan mengarang tingkat pendidikan | Ditetapkan untuk tahap berikutnya; raw belum diubah |
| P06 | MARRIAGE 0 | 54 baris | Pertahankan sebagai kategori unknown terpisah | Arti status spesifik tidak dijelaskan di S1 | Ditetapkan untuk encoding; raw belum diubah |
| P07 | PAY -2/-1/0 | Terdapat kode nonpositif pada seluruh bulan | Pertahankan kategori terpisah; jangan jadikan NaN atau jumlah bulan negatif | S3 menambahkan arti -2/0; tidak setara dengan kode keterlambatan positif | Ditetapkan; encoding setelah split |
| P08 | Tagihan negatif | 1930 nasabah; 3932 sel | Pertahankan; hanya beri flag audit | Tidak ada bukti setiap nilai negatif adalah kesalahan | Ditetapkan; flag tersedia; tidak ada clipping |
| P09 | Pembayaran nol | Nol ada pada PAY_AMT | Pertahankan nol sebagai nilai teramati | Nol tidak otomatis missing | Ditetapkan; tidak ada imputasi |
| P10 | Profil raw identik | 108 baris dalam 52 kelompok; 56 pengulangan berlebih | Jangan drop otomatis; hitung ulang kelompok profil setelah pemetaan kategori tetap, sebelum split | Nasabah berbeda dapat memiliki fitur sama; kelompok tidak memakai target | Audit selesai; pengelompokan untuk split menunggu tahap 4 |
| P11 | Profil raw sama, target berbeda | 21 kelompok; 46 baris | Pertahankan label masing-masing; tidak melakukan voting atau mengganti target | Fitur yang diamati tidak menentukan outcome secara sempurna | Ditetapkan; flag tersedia |
| P12 | Nilai ekstrem | Lihat min/median/p99/max pada statistik numerik | Tidak hapus/clipping otomatis; jika kelak perlu ambang, pelajari hanya pada train | Nilai besar tidak otomatis salah dan penghapusan bisa mengubah populasi | Ditetapkan: tanpa filter outlier pada audit |
| P13 | Fitur tagihan berkorelasi | BILL_AMT1-BILL_AMT6 adalah fokus penelitian | Pertahankan enam fitur; analisis korelasi untuk keputusan riset dilakukan pada train nanti | Menghapusnya akan menghilangkan objek penelitian | Ditetapkan; tidak melakukan seleksi fitur |
| P14 | Encoding dan scaling | 9 kategori semantik; 14 numerik; ID/target terpisah | Rencana one-hot kategori; fit encoder pada train. Tidak wajib scaling untuk Random Forest | Mencegah urutan kategori semu dan kebocoran transformasi | Ditetapkan; belum fit encoder atau scaler |
| P15 | Ketidakseimbangan kelas | Gagal bayar lebih sedikit dari tidak gagal bayar | Pilot memakai distribusi asli tanpa SMOTE/undersampling | Hindari faktor sampling tercampur dengan mode TreeSHAP | Ditetapkan; tidak melakukan resampling |

## Pembedaan pengulangan

- Duplikat seluruh 25 kolom: 0.
- Pengulangan berlebih setelah ID dikeluarkan, termasuk target: 35.
- Pengulangan berlebih berdasarkan 23 fitur saja: 56.
- Semua baris yang tergabung profil fitur berulang: 108.
- Grup untuk split kelak dibentuk tanpa target dan setelah pemetaan kategori yang sudah ditetapkan. Jangan memakai grup raw audit ini tanpa memeriksa ulang profil yang bisa menjadi identik setelah pemetaan.
- Kesamaan profil teramati bukan bukti identitas orang sama. Label berbeda tetap dipertahankan.

## Sumber keputusan

Definisi pokok: [UCI](https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients). Interpretasi tambahan PAY -2/0 dan kemungkinan tagihan negatif: [Lin dan Wang, preprint 2025, Tabel 1 dan bagian Data Source and Cleaning](https://arxiv.org/pdf/2508.01851). Pengelompokan unknown serta protokol split/encoding merupakan kebijakan penelitian kelompok, bukan aturan bawaan UCI.
