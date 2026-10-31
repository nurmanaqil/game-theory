# Lingkungan dan verifikasi reproduksi

Lingkungan eksekusi lokal: `kredit/.venv_local/Scripts/python.exe` (Python 3.14.7).
Dependency proyek lama berformat cp314 masih dapat digunakan. Lingkungan baru memakai file `.pth` relatif untuk membaca paket dari `kredit/.venv/Lib/site-packages`; executable virtual environment lama tidak dipakai. Jangan menghapus folder `.venv` lama selama lingkungan baru masih memakai paket tersebut. Ini pemulihan lokal dengan dependency salinan, bukan instalasi bersih dari internet.

## Menjalankan pemeriksaan

Dari root proyek di PowerShell:

```powershell
& .\kredit\.venv_local\Scripts\python.exe -u .\kredit\verify_reproduction.py
```

Script menetapkan cache matplotlib ke folder workspace yang dapat ditulis. Semua hasil baru disimpan ke `kredit/reproduction/20261023/`, sedangkan artefak historis dipantau dengan SHA-256. Eksekusi ulang mengganti hasil verifikasi dalam folder itu, bukan hasil historis.

`requirements_reproduction.txt` mencatat 22 paket yang ditemukan pada dependency lama, termasuk SHAP. Catatan versi ini membantu instalasi bersih kelak, tetapi keberhasilan unduhan/instalasi bersih daftar tersebut belum diuji. Tidak memakai environment bawaan Codex untuk komputasi riset.

## Cakupan

- Verifikasi checksum raw dan checksum file preprocessing yang tercatat.
- Bentuk ulang grouped split dan cocokkan membership serta label.
- Terapkan encoder tersimpan dan cocokkan matriks encoded.
- Fit ulang encoder pada train, lalu cocokkan urutan kolom dan transformasi ketiga split. Eksekusi awal dicatat terpisah di `encoder_refit_report.json`; verifier berikutnya menyertakan langkah ini.
- Muat model tersimpan, cocokkan prediksi validation dan test, threshold, metrik, serta confusion counts.
- Latih ulang konfigurasi Random Forest terpilih dari seed dan parameter yang dicatat; cocokkan prediksinya. Tidak menuntut joblib identik byte karena metadata lingkungan bisa berbeda.
- Hitung ulang seluruh 1.000 atribusi dua mode pada background awal serta dua background interventional tambahan. Cocokkan array SHAP, baseline, dan additivity.
- Hitung ulang ketidaksepakatan fitur tagihan teratas dan Spearman pada ketiga background.

Belum mencakup pencarian ulang seluruh kandidat Random Forest, model baru, seed model tambahan, atau evaluasi ulang kebaruan literatur. Laporan PASS di `verification_report.json` hanya berlaku untuk cakupan pemeriksaan yang tercatat. Bandingkan versi historis pada manifest tiap tahap: sebagian preprocessing/evaluasi sebelumnya menggunakan Python 3.12.14, sementara TreeSHAP menggunakan Python 3.14.4.
