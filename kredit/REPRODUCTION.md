# Verifikasi salinan proyek saat ini

Jalankan dari folder mana pun (sesuaikan path script):

```powershell
py game-theory/kredit/verify_revision_results.py
py -m unittest discover -s game-theory/kredit -p test_checkpoint_integrity.py
```

Verifier memeriksa keberadaan model dan array sebelum memuat dependency riset. Exit code 2 dan status `INCOMPLETE` berarti artefak belum tersedia; bukan kegagalan numerik. Hasil baru disimpan ke `experiments/revision_v1/verification_report_current.json`, tidak menimpa laporan historis `final_quality_report.json`. Review visual harus dicatat manual, bukan disimpulkan dari pemeriksaan numerik.

Lengkapi model terlatih, encoder, dan 32 array SHAP dari sumber eksperimen asli. Jangan membuat file dummy atau memakai hasil training baru sebagai pengganti bukti historis. Manifest mencatat Python 3.14.7, NumPy 2.3.5, pandas 3.0.1, scikit-learn 1.7.2, SciPy 1.16.2, SHAP 0.54.1, XGBoost 3.4.1, dan joblib 1.5.2. `requirements_revision.txt` merupakan daftar versi, tetapi instalasi bersihnya belum diverifikasi.

Untuk eksperimen baru gunakan environment terpisah dengan versi tersebut dan **folder output baru**:

```powershell
$env:TREESHAP_OUTPUT_DIR = Join-Path $PWD 'game-theory/kredit/experiments/new_run'
py game-theory/kredit/run_revision_experiments.py
```

Jangan menjalankan perintah training hanya untuk menguji perbaikan kode. Pipeline menolak output historis/default dan folder yang sudah memiliki completed manifest. Checkpoint baru memiliki sidecar provenance yang mencatat input, parameter, seed, runtime, serta checksum file. Checkpoint tanpa sidecar atau dengan fingerprint berbeda ditolak. Helper historis `prefit_candidates.py`, `precompute_extra_trees.py`, dan generator/merge lama tidak mendukung output baru ini; jangan gunakan untuk resume pipeline yang diperbarui. Rekalkulasi gambar/naskah juga harus ditinjau sebelum memakai output baru.

Saat memverifikasi probabilitas CSV gunakan pandas `float_precision="round_trip"`; parsing default dapat mengubah klasifikasi observasi tepat pada threshold. Bedakan presisi serialisasi dari perubahan model.

## Catatan lingkungan historis

Petunjuk berikut berasal dari workspace lama. Environment dan executable tersebut **belum ikut tersedia di salinan ini**.

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
