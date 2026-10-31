"""Audit tahap 1-3. Tidak membuat split, encoding, model, atau data bersih.

Jalankan: python audit_dataset.py
Dependensi analisis: pandas, numpy. Notebook memakai fungsi-fungsi dalam file ini.
"""
from __future__ import annotations

import contextlib
import hashlib
import io
import json
import platform
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parent
TARGET = "default.payment.next.month"
BILLS = [f"BILL_AMT{i}" for i in range(1, 7)]
PAYMENTS = [f"PAY_AMT{i}" for i in range(1, 7)]
STATUS = ["PAY_0", "PAY_2", "PAY_3", "PAY_4", "PAY_5", "PAY_6"]
CATEGORIES = ["SEX", "EDUCATION", "MARRIAGE"] + STATUS
EXPECTED = ["ID", "LIMIT_BAL", "SEX", "EDUCATION", "MARRIAGE", "AGE"] + STATUS + BILLS + PAYMENTS + [TARGET]
SOURCES = {
    "S1": {"title": "UCI Default of Credit Card Clients", "url": "https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients", "doi": "10.24432/C55S3H"},
    "S2": {"title": "Kaggle mirror: uciml/default-of-credit-card-clients-dataset", "url": "https://www.kaggle.com/datasets/uciml/default-of-credit-card-clients-dataset"},
    "S3": {"title": "Lin dan Wang (2025), preprint, Tabel 1 dan bagian Data Source and Cleaning", "url": "https://arxiv.org/pdf/2508.01851", "journal_doi": "10.3390/risks13120238"},
}


def digest(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def write_json(path: Path, value) -> None:
    def normalize(x):
        if isinstance(x, np.generic):
            return x.item()
        raise TypeError(type(x).__name__)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, default=normalize, allow_nan=False) + "\n", encoding="utf-8")


def md_table(frame: pd.DataFrame) -> str:
    """Markdown tanpa dependensi tabulate."""
    def escape(x):
        return str(x).replace("|", " / ").replace("\n", " ")
    lines = ["| " + " | ".join(map(escape, frame.columns)) + " |", "| " + " | ".join(["---"] * len(frame.columns)) + " |"]
    lines += ["| " + " | ".join(escape(x) for x in row) + " |" for row in frame.itertuples(index=False, name=None)]
    return "\n".join(lines)


def prepare_source():
    original = BASE / "UCI_Credit_Card.csv"
    raw_dir, audit_dir = BASE / "raw", BASE / "audit"
    raw_dir.mkdir(exist_ok=True)
    audit_dir.mkdir(exist_ok=True)
    snapshot = raw_dir / original.name
    original_hash = digest(original)
    if snapshot.exists():
        if digest(snapshot) != original_hash:
            raise RuntimeError("Snapshot raw berbeda dari sumber lokal. Audit dihentikan; raw tidak ditimpa.")
    else:
        shutil.copyfile(original, snapshot)
    if digest(snapshot) != original_hash:
        raise RuntimeError("Verifikasi salinan raw gagal.")
    manifest = {
        "source_local": original.name,
        "raw_snapshot": "raw/" + snapshot.name,
        "size_bytes": original.stat().st_size,
        "sha256": original_hash,
        "first_recorded_by_this_audit_utc": datetime.now(timezone.utc).isoformat(),
        "download_date": None,
        "uploader_dataset_version": None,
        "provenance_status": "Struktur dibandingkan dengan dokumentasi UCI; kesamaan byte terhadap unduhan resmi belum diverifikasi.",
        "source_license": "S1 mencantumkan CC BY 4.0. Lisensi/versi mirror saat pengunduhan belum terekam.",
        "sources": SOURCES,
    }
    manifest_path = raw_dir / "manifest.json"
    if manifest_path.exists():
        previous = json.loads(manifest_path.read_text(encoding="utf-8"))
        if previous.get("sha256") != original_hash:
            raise RuntimeError("Manifest sebelumnya tidak sesuai. Tidak menimpa manifest raw.")
    else:
        write_json(manifest_path, manifest)
    df = pd.read_csv(snapshot)
    if df.columns.tolist() != EXPECTED:
        raise ValueError(f"Skema tidak sesuai. Kolom teramati: {df.columns.tolist()}")
    return {"df": df, "original": original, "snapshot": snapshot, "hash": original_hash, "audit_dir": audit_dir}


def audit(ctx):
    df, output = ctx["df"], ctx["audit_dir"]
    features = [c for c in df if c not in ["ID", TARGET]]
    profile = pd.DataFrame({
        "kolom": df.columns, "dtype": [str(df[c].dtype) for c in df],
        "jumlah_kosong": df.isna().sum().values,
        "nilai_unik": df.nunique(dropna=False).values,
        "minimum": [df[c].min() for c in df],
        "median": [df[c].median() for c in df],
        "maksimum": [df[c].max() for c in df],
        "jumlah_nol": [int(df[c].eq(0).sum()) for c in df],
        "jumlah_negatif": [int(df[c].lt(0).sum()) for c in df],
    })
    distribution = df[TARGET].value_counts().sort_index().rename_axis("kode").reset_index(name="jumlah")
    distribution["persen"] = distribution["jumlah"] / len(df) * 100
    distribution["arti"] = distribution["kode"].map({0: "Tidak gagal bayar", 1: "Gagal bayar"})
    category_rows = []
    for column in CATEGORIES:
        for code, count in df[column].value_counts(dropna=False).sort_index().items():
            category_rows.append({"kolom": column, "kode": code, "jumlah": int(count), "persen": 100 * count / len(df)})
    category_table = pd.DataFrame(category_rows)

    grouped = df.groupby(features, dropna=False, sort=True)
    profile_numbers = grouped.ngroup()
    summaries = []
    for number, indices in df.groupby(profile_numbers, sort=True).groups.items():
        if len(indices) < 2:
            continue
        part = df.loc[indices]
        summaries.append({
            "kelompok_profil_raw": f"RAW_{int(number):05d}",
            "jumlah_baris": len(part),
            "jumlah_target_unik": int(part[TARGET].nunique()),
            "target_0": int(part[TARGET].eq(0).sum()),
            "target_1": int(part[TARGET].eq(1).sum()),
            "daftar_ID": ",".join(str(int(x)) for x in part.ID),
        })
    duplicate_table = pd.DataFrame(summaries, columns=["kelompok_profil_raw", "jumlah_baris", "jumlah_target_unik", "target_0", "target_1", "daftar_ID"])
    flags = pd.DataFrame({"ID": df.ID})
    flags["education_tidak_terdefinisi_lengkap_S1"] = df.EDUCATION.isin([0, 5, 6])
    flags["marriage_tidak_terdefinisi_lengkap_S1"] = df.MARRIAGE.eq(0)
    flags["ada_tagihan_negatif"] = df[BILLS].lt(0).any(axis=1)
    flags["profil_fitur_berulang_raw"] = df.duplicated(subset=features, keep=False)
    target_count_by_profile = grouped[TARGET].transform("nunique")
    flags["profil_fitur_target_berbeda"] = target_count_by_profile.gt(1)
    flags["kelompok_profil_raw"] = profile_numbers.map(lambda x: f"RAW_{int(x):05d}")

    allowed = {"SEX": {1, 2}, "EDUCATION": set(range(7)), "MARRIAGE": {0, 1, 2, 3}}
    allowed.update({c: set(range(-2, 10)) for c in STATUS})
    outside_code = {c: sorted(set(df[c].dropna().unique()) - values) for c, values in allowed.items()}
    summary = {
        "n_baris": len(df), "n_kolom": len(df.columns), "n_fitur_prediksi": len(features),
        "missing_cells": int(df.isna().sum().sum()),
        "nonfinite_values": int((~np.isfinite(df.to_numpy(dtype=float))).sum()),
        "n_ID_unik": int(df.ID.nunique()),
        "duplicate_full_excess": int(df.duplicated().sum()),
        "duplicate_excluding_ID_excess": int(df.drop(columns="ID").duplicated().sum()),
        "duplicate_features_only_excess": int(df[features].duplicated().sum()),
        "rows_in_repeated_feature_profiles": int(flags.profil_fitur_berulang_raw.sum()),
        "repeated_feature_groups": len(duplicate_table),
        "conflicting_label_groups": int(duplicate_table.jumlah_target_unik.gt(1).sum()),
        "rows_in_conflicting_label_groups": int(flags.profil_fitur_target_berbeda.sum()),
        "education_0_5_6_rows": int(flags.education_tidak_terdefinisi_lengkap_S1.sum()),
        "marriage_0_rows": int(flags.marriage_tidak_terdefinisi_lengkap_S1.sum()),
        "rows_with_negative_bill": int(flags.ada_tagihan_negatif.sum()),
        "negative_bill_cells": int(df[BILLS].lt(0).sum().sum()),
        "negative_payment_cells": int(df[PAYMENTS].lt(0).sum().sum()),
        "constant_columns": [c for c in df if df[c].nunique(dropna=False) <= 1],
        "unexpected_codes_relative_to_audit_schema": outside_code,
        "target_counts": {str(int(k)): int(v) for k, v in df[TARGET].value_counts().sort_index().items()},
        "target_default_percent": float(df[TARGET].eq(1).mean() * 100),
        "raw_data_changes_applied": 0,
        "scope": "Audit seluruh data untuk kualitas dan dokumentasi; bukan seleksi fitur atau estimasi transformasi untuk model.",
    }
    profile.to_csv(output / "profil_kolom.csv", index=False, encoding="utf-8-sig")
    distribution.to_csv(output / "distribusi_target.csv", index=False, encoding="utf-8-sig")
    category_table.to_csv(output / "frekuensi_kategori.csv", index=False, encoding="utf-8-sig")
    duplicate_table.to_csv(output / "kelompok_profil_identik.csv", index=False, encoding="utf-8-sig")
    flags.to_csv(output / "penanda_baris_audit.csv", index=False, encoding="utf-8-sig")
    write_json(output / "ringkasan_audit.json", summary)
    ctx.update(summary=summary, profile=profile, distribution=distribution, categories=category_table, duplicate_table=duplicate_table)
    return summary


def dictionary(ctx):
    df = ctx["df"]
    definitions = {
        "ID": ("Identitas nasabah", "ID", "Tidak berlaku", "Identifier; bukan urutan waktu", "Tidak menjadi prediktor; simpan untuk pelacakan", "S1"),
        "LIMIT_BAL": ("Batas kredit yang diberikan", "Numerik", "NT dollar", "Mencakup kredit individu dan tambahan keluarga menurut S1", "Pertahankan; tidak diskalakan untuk pilot Random Forest", "S1"),
        "SEX": ("Kategori jenis kelamin yang direkam", "Kategoris", "Kode", "1=laki-laki; 2=perempuan", "Pertahankan kode raw; encoding kategoris setelah split", "S1"),
        "EDUCATION": ("Kategori pendidikan", "Kategoris", "Kode", "1=pascasarjana; 2=universitas; 3=SMA; 4=lainnya. 0/5/6 tidak dijelaskan lengkap di S1", "Rencana: 0/5/6 menjadi satu kategori unknown; 4 tetap others; belum diterapkan", "S1; kebijakan kelompok"),
        "MARRIAGE": ("Kategori status perkawinan", "Kategoris", "Kode", "1=menikah; 2=belum menikah; 3=lainnya; 0 tidak dijelaskan di S1", "Pertahankan 0 sebagai kategori unknown; jangan diberi arti status tertentu", "S1; kebijakan kelompok"),
        "AGE": ("Usia nasabah", "Numerik", "Tahun", "Nilai usia, bukan kode kategori", "Pertahankan", "S1"),
        TARGET: ("Gagal bayar pada bulan berikutnya", "Target biner", "Kode", "1=gagal bayar; 0=tidak gagal bayar; target Oktober 2005 menurut S3", "Pisahkan sebagai y; tidak boleh masuk fitur X", "S1; S3"),
    }
    months = ["September 2005", "Agustus 2005", "Juli 2005", "Juni 2005", "Mei 2005", "April 2005"]
    for column, month in zip(STATUS, months):
        definitions[column] = (f"Status pembayaran {month}", "Kategoris", "Kode", "-1=bayar sesuai ketentuan; 1-9=bulan keterlambatan (S1). -2=tidak ada konsumsi; 0=revolving credit menurut S3, bukan dokumentasi lengkap S1", "Pertahankan -2/-1/0 terpisah, bukan missing; encoding kategoris setelah split", "S1; S3 (interpretasi tambahan -2/0)")
    for i, month in enumerate(months, 1):
        definitions[f"BILL_AMT{i}"] = (f"Jumlah tagihan {month}", "Numerik", "NT dollar", "Tagihan, bukan jumlah pembayaran; nilai negatif mungkin sah", "Pertahankan termasuk negatif; jangan hapus karena korelasi", "S1; S3 (penjelasan negatif)")
        definitions[f"PAY_AMT{i}"] = (f"Jumlah pembayaran {month}", "Numerik", "NT dollar", "Jumlah pembayaran, bukan status keterlambatan", "Pertahankan termasuk nol; tidak imputasi nol", "S1")
    rows = []
    for column in df:
        description, kind, unit, codes, rule, source = definitions[column]
        rows.append({"kolom": column, "arti": description, "jenis_semantik": kind, "dtype_csv": str(df[column].dtype), "satuan": unit, "definisi_kode_dan_catatan": codes, "perlakuan": rule, "sumber": source})
    table = pd.DataFrame(rows)
    table.to_csv(ctx["audit_dir"] / "kamus_variabel.csv", index=False, encoding="utf-8-sig")
    sources = "\n".join(f"- {key}: [{value['title']}]({value['url']})." for key, value in SOURCES.items())
    text = "# Kamus variabel dataset kredit\n\nSatu baris adalah satu nasabah. Riwayat bulan merupakan kolom, bukan baris waktu. ID bukan waktu.\n\n"
    text += md_table(table) + "\n\n## Catatan definisi\n\n"
    text += "- PAY_0 adalah September dan PAY_2 adalah Agustus; tidak membuat PAY_1 atau menggeser urutan bulan.\n"
    text += "- EDUCATION 0/5/6 disebut unknown sebagai kebijakan konservatif, bukan pengakuan bahwa arti aslinya telah dipastikan.\n"
    text += "- MARRIAGE 3 mengikuti S1 sebagai others, tidak otomatis disebut bercerai.\n"
    text += "- Arti PAY -2 dan 0 memakai S3 sebagai literatur tambahan. Nilai tersebut tetap kategori tersendiri walau definisinya belum lengkap pada S1.\n"
    text += "- Nilai tagihan negatif tidak memiliki alasan transaksi per baris dalam dataset. Jangan menyimpulkan semua kasus adalah refund atau overpayment.\n\n## Sumber\n\n" + sources + "\n"
    (BASE / "data_dictionary.md").write_text(text, encoding="utf-8")
    ctx["dictionary"] = table
    return table


def cleaning_rules(ctx):
    s = ctx["summary"]
    rules = [
        ("P01", "Data mentah", f"{s['n_baris']:,} baris, {s['n_kolom']} kolom", "Bekukan snapshot dan verifikasi SHA-256; sumber asli tidak ditimpa", "Mencegah perubahan data tanpa jejak", "Selesai: snapshot dan manifest dibuat", 0),
        ("P02", "Kolom ID", f"{s['n_ID_unik']:,} ID unik", "Keluarkan dari X, tetap simpan sebagai metadata", "ID bukan prediktor substantif atau urutan waktu", "Ditetapkan; diterapkan pada tahap persiapan X/y", s['n_baris']),
        ("P03", "Target", f"Kode 0/1; gagal bayar {s['target_default_percent']:.2f}% pada file ini", "Pisahkan target dari X; jaga proporsi kelas pada pembagian", "Menghindari kebocoran target dan evaluasi menyesatkan", "Ditetapkan; belum membuat split", s['n_baris']),
        ("P04", "Missing/nonfinite", f"{s['missing_cells']} sel kosong; {s['nonfinite_values']} nonfinite", "Tidak melakukan imputasi pada data saat ini", "Tidak ada missing numerik yang memerlukan pengisian", "Ditetapkan; tidak ada pengisian", 0),
        ("P05", "EDUCATION 0/5/6", f"{s['education_0_5_6_rows']} baris", "Pemetaan deterministik 0/5/6 -> kategori unknown; 4 tetap others", "S1 tidak menjelaskan kode tersebut lengkap; jangan mengarang tingkat pendidikan", "Ditetapkan untuk tahap berikutnya; raw belum diubah", s['education_0_5_6_rows']),
        ("P06", "MARRIAGE 0", f"{s['marriage_0_rows']} baris", "Pertahankan sebagai kategori unknown terpisah", "Arti status spesifik tidak dijelaskan di S1", "Ditetapkan untuk encoding; raw belum diubah", s['marriage_0_rows']),
        ("P07", "PAY -2/-1/0", "Terdapat kode nonpositif pada seluruh bulan", "Pertahankan kategori terpisah; jangan jadikan NaN atau jumlah bulan negatif", "S3 menambahkan arti -2/0; tidak setara dengan kode keterlambatan positif", "Ditetapkan; encoding setelah split", int(ctx['df'][STATUS].le(0).any(axis=1).sum())),
        ("P08", "Tagihan negatif", f"{s['rows_with_negative_bill']} nasabah; {s['negative_bill_cells']} sel", "Pertahankan; hanya beri flag audit", "Tidak ada bukti setiap nilai negatif adalah kesalahan", "Ditetapkan; flag tersedia; tidak ada clipping", s['rows_with_negative_bill']),
        ("P09", "Pembayaran nol", "Nol ada pada PAY_AMT", "Pertahankan nol sebagai nilai teramati", "Nol tidak otomatis missing", "Ditetapkan; tidak ada imputasi", int(ctx['df'][PAYMENTS].eq(0).any(axis=1).sum())),
        ("P10", "Profil raw identik", f"{s['rows_in_repeated_feature_profiles']} baris dalam {s['repeated_feature_groups']} kelompok; {s['duplicate_features_only_excess']} pengulangan berlebih", "Jangan drop otomatis; hitung ulang kelompok profil setelah pemetaan kategori tetap, sebelum split", "Nasabah berbeda dapat memiliki fitur sama; kelompok tidak memakai target", "Audit selesai; pengelompokan untuk split menunggu tahap 4", s['rows_in_repeated_feature_profiles']),
        ("P11", "Profil raw sama, target berbeda", f"{s['conflicting_label_groups']} kelompok; {s['rows_in_conflicting_label_groups']} baris", "Pertahankan label masing-masing; tidak melakukan voting atau mengganti target", "Fitur yang diamati tidak menentukan outcome secara sempurna", "Ditetapkan; flag tersedia", s['rows_in_conflicting_label_groups']),
        ("P12", "Nilai ekstrem", "Lihat min/median/p99/max pada statistik numerik", "Tidak hapus/clipping otomatis; jika kelak perlu ambang, pelajari hanya pada train", "Nilai besar tidak otomatis salah dan penghapusan bisa mengubah populasi", "Ditetapkan: tanpa filter outlier pada audit", 0),
        ("P13", "Fitur tagihan berkorelasi", "BILL_AMT1-BILL_AMT6 adalah fokus penelitian", "Pertahankan enam fitur; analisis korelasi untuk keputusan riset dilakukan pada train nanti", "Menghapusnya akan menghilangkan objek penelitian", "Ditetapkan; tidak melakukan seleksi fitur", 0),
        ("P14", "Encoding dan scaling", "9 kategori semantik; 14 numerik; ID/target terpisah", "Rencana one-hot kategori; fit encoder pada train. Tidak wajib scaling untuk Random Forest", "Mencegah urutan kategori semu dan kebocoran transformasi", "Ditetapkan; belum fit encoder atau scaler", 0),
        ("P15", "Ketidakseimbangan kelas", "Gagal bayar lebih sedikit dari tidak gagal bayar", "Pilot memakai distribusi asli tanpa SMOTE/undersampling", "Hindari faktor sampling tercampur dengan mode TreeSHAP", "Ditetapkan; tidak melakukan resampling", 0),
    ]
    table = pd.DataFrame(rules, columns=["kode", "isu", "temuan", "keputusan", "alasan", "status", "baris_terkait_bukan_jumlah_dihapus"])
    table.to_csv(ctx["audit_dir"] / "keputusan_pembersihan.csv", index=False, encoding="utf-8-sig")
    policy = {
        "scope": "Aturan tahap 1-3; belum diterapkan menjadi dataset model",
        "drop_predictors": ["ID"], "target": TARGET,
        "education_recode_future": {"0": "unknown", "5": "unknown", "6": "unknown", "4": "others", "1": "graduate_school", "2": "university", "3": "high_school"},
        "marriage_code_0_future": "unknown",
        "retain_negative_bills": True, "retain_zero_payments": True,
        "retain_raw_duplicates_and_conflicting_targets": True,
        "group_split_future": "Kelompok identik dari X setelah pemetaan kategori deterministik; tanpa ID dan tanpa target. Belum dibuat.",
        "categorical_columns": CATEGORIES, "bill_focus": BILLS,
        "fit_encoder_on": "train_only_future", "resampling_pilot": None,
        "automatic_row_deletions": 0,
    }
    write_json(ctx["audit_dir"] / "kebijakan_preprocessing.json", policy)
    md = "# Keputusan pembersihan: tahap 1-3\n\n"
    md += "Semua keputusan di bawah terdokumentasi. Tidak ada baris dihapus, nilai diubah, encoding diterapkan, atau split dibuat pada tahap ini. Kolom baris terkait bukan jumlah baris yang akan dibuang.\n\n"
    md += md_table(table.drop(columns="baris_terkait_bukan_jumlah_dihapus"))
    md += "\n\n## Pembedaan pengulangan\n\n"
    md += f"- Duplikat seluruh 25 kolom: {s['duplicate_full_excess']}.\n- Pengulangan berlebih setelah ID dikeluarkan, termasuk target: {s['duplicate_excluding_ID_excess']}.\n"
    md += f"- Pengulangan berlebih berdasarkan 23 fitur saja: {s['duplicate_features_only_excess']}.\n- Semua baris yang tergabung profil fitur berulang: {s['rows_in_repeated_feature_profiles']}.\n"
    md += "- Grup untuk split kelak dibentuk tanpa target dan setelah pemetaan kategori yang sudah ditetapkan. Jangan memakai grup raw audit ini tanpa memeriksa ulang profil yang bisa menjadi identik setelah pemetaan.\n"
    md += "- Kesamaan profil teramati bukan bukti identitas orang sama. Label berbeda tetap dipertahankan.\n\n## Sumber keputusan\n\n"
    md += "Definisi pokok: [UCI](https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients). Interpretasi tambahan PAY -2/0 dan kemungkinan tagihan negatif: [Lin dan Wang, preprint 2025, Tabel 1 dan bagian Data Source and Cleaning](https://arxiv.org/pdf/2508.01851). Pengelompokan unknown serta protokol split/encoding merupakan kebijakan penelitian kelompok, bukan aturan bawaan UCI.\n"
    (BASE / "data_cleaning_decisions.md").write_text(md, encoding="utf-8")
    ctx["rules"] = table
    return table


def verify_and_report(ctx):
    df, s, out = ctx["df"], ctx["summary"], ctx["audit_dir"]
    checks = {
        "original_unchanged": digest(ctx["original"]) == ctx["hash"],
        "raw_snapshot_matches_original": digest(ctx["snapshot"]) == ctx["hash"],
        "raw_dataframe_not_modified": df.equals(pd.read_csv(ctx["snapshot"])),
        "dictionary_covers_each_column_once": ctx["dictionary"].kolom.tolist() == df.columns.tolist() and ctx["dictionary"].kolom.is_unique,
        "target_counts_reconcile": int(ctx["distribution"].jumlah.sum()) == len(df),
        "category_counts_reconcile": all(int(g.jumlah.sum()) == len(df) for _, g in ctx["categories"].groupby("kolom")),
        "duplicate_members_reconcile": int(ctx["duplicate_table"].jumlah_baris.sum()) == s["rows_in_repeated_feature_profiles"],
        "target_is_binary_and_complete": df[TARGET].notna().all() and set(df[TARGET].unique()) == {0, 1},
    }
    checks = {k: bool(v) for k, v in checks.items()}
    write_json(out / "verifikasi_audit.json", checks)
    if not all(checks.values()):
        raise AssertionError(checks)
    numerics = ["LIMIT_BAL", "AGE"] + BILLS + PAYMENTS
    desc = df[numerics].describe(percentiles=[.01, .25, .5, .75, .99]).transpose().reset_index(names="kolom")
    desc.to_csv(out / "statistik_numerik.csv", index=False, encoding="utf-8-sig")
    # Statistik seluruh data berikut untuk audit, tidak dipakai sebagai ambang transformasi/model.
    summary_rows = [("Baris", s['n_baris']), ("Kolom", s['n_kolom']), ("Fitur prediksi (tanpa ID/target)", s['n_fitur_prediksi']), ("Sel kosong", s['missing_cells']), ("ID unik", s['n_ID_unik']), ("Baris dihapus/diubah", 0)]
    report = "# Audit dataset kredit: langkah 1-3\n\n"
    report += "Penanggung jawab: Nurman Aqil Wicaksono (L0124139). Tanggal penyusunan awal: 20 Oktober 2026.\n\n"
    report += "## Status\n\nSnapshot raw, notebook audit, kamus 25 variabel, dan keputusan pembersihan selesai. Belum membuat split, dataset bersih, encoding, model, atau TreeSHAP. Semua pemeriksaan keutuhan sumber lulus.\n\n"
    report += md_table(pd.DataFrame(summary_rows, columns=["Ukuran", "Hasil"])) + "\n\n## Target\n\n" + md_table(ctx["distribution"].round(2))
    report += f"\n\nBaseline selalu memprediksi kelas mayoritas mencapai {max(s['target_counts'].values()) / s['n_baris'] * 100:.2f}% accuracy; ini perhitungan proporsi kelas, bukan model yang sudah dilatih.\n\n"
    report += "## Temuan yang perlu dibawa ke preprocessing\n\n"
    report += f"- EDUCATION 0/5/6: {s['education_0_5_6_rows']} baris. Kelak digabung sebagai unknown; kode 4 tetap others.\n"
    report += f"- MARRIAGE 0: {s['marriage_0_rows']} baris. Tetap kategori unknown.\n"
    report += f"- Tagihan negatif: {s['rows_with_negative_bill']} nasabah, {s['negative_bill_cells']} sel. Dipertahankan.\n"
    report += f"- Profil fitur raw identik: {s['rows_in_repeated_feature_profiles']} baris dalam {s['repeated_feature_groups']} kelompok, termasuk {s['conflicting_label_groups']} kelompok dengan target berbeda. Tidak dihapus otomatis.\n"
    if not s['constant_columns']:
        report += "- Tidak ada kolom konstan. Setiap prediktor memiliki variasi teramati; ini belum bukti daya prediksi.\n"
    else:
        report += "- Kolom konstan ditemukan: " + ", ".join(s['constant_columns']) + ".\n"
    report += "- Kolom nominal tetap kategori walau dibaca sebagai integer. Nilai ekstrem belum difilter, dan distribusi kelas belum diubah.\n\n"
    report += "## Keutuhan dan asal data\n\n"
    report += f"SHA-256 sumber asli dan snapshot: `{ctx['hash']}`. Snapshot: `raw/UCI_Credit_Card.csv`. Manifest memuat URL sumber, ukuran, dan waktu pencatatan; tanggal unduh/versi Kaggle belum diketahui dan tidak dikarang. Kesamaan byte terhadap unduhan resmi belum diverifikasi.\n\n"
    report += "## Cara menjalankan\n\nBuka `01_dataset_audit.ipynb` dan jalankan sel berurutan dengan Python, pandas, dan numpy. Alternatif dari folder proyek: `python kredit/audit_dataset.py`. Notebook memanggil fungsi transparan di `audit_dataset.py`, sehingga file script perlu tetap berada di folder yang sama.\n\n"
    report += "Notebook yang disertakan telah dieksekusi berurutan menggunakan Python (bukan kernel Jupyter pada lingkungan ini). Output sel berasal dari eksekusi tersebut. Jika salinan raw berbeda dari sumber, proses berhenti tanpa menimpanya.\n\n"
    report += "## Hasil untuk Aqil\n\n- `data_dictionary.md`: definisi setiap kolom dan sumbernya.\n- `data_cleaning_decisions.md`: temuan, perlakuan, dan alasan.\n- `audit/`: tabel frekuensi, profil kolom, penanda per baris, grup identik, statistik numerik, kebijakan JSON, dan verifikasi.\n\n"
    report += "## Pekerjaan berikutnya\n\nTerapkan pemetaan kategori deterministik ke salinan kerja, bentuk ulang grup profil tanpa ID/target, lalu buat train/validation/test dengan menjaga grup dan mendekati proporsi kelas. Fit encoder hanya pada train. Korelasi untuk pemilihan fokus riset dihitung pada train, bukan memakai hasil audit seluruh data untuk memilih fitur. Tahap berikutnya belum dijalankan.\n\n"
    report += f"## Bahan Dataset dan Preprocessing\n\nDataset lokal memiliki {s['n_baris']:,} observasi dengan {s['n_fitur_prediksi']} prediktor, satu identifier, dan satu target biner. Target positif berjumlah {s['target_counts'].get('1', 0):,} ({s['target_default_percent']:.2f}%). Audit menemukan {s['missing_cells']} sel kosong dan {s['nonfinite_values']} nilai nonfinite. Kode kategori yang dokumentasinya tidak lengkap, tagihan negatif, dan profil fitur identik ditandai untuk perlakuan eksplisit. Data mentah dipertahankan dan snapshot diverifikasi menggunakan SHA-256. Pada tahap audit ini tidak ada baris dibuang maupun nilai ditransformasikan. Prosedur split dan encoding harus dijelaskan dalam bentuk sudah dilakukan hanya setelah tahap tersebut benar-benar dijalankan.\n\n"
    report += "## Referensi\n\n" + "\n".join(f"- [{k}: {v['title']}]({v['url']})" for k, v in SOURCES.items()) + "\n"
    (BASE / "dataset_audit.md").write_text(report, encoding="utf-8")
    write_json(out / "runtime.json", {"python": platform.python_version(), "pandas": pd.__version__, "numpy": np.__version__, "execution": "Sequential Python cell execution; no Jupyter kernel invoked", "recorded_at_utc": datetime.now(timezone.utc).isoformat()})
    return checks


def build_notebook():
    def markdown(text):
        return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(keepends=True)}
    def code(text):
        return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": text.splitlines(keepends=True)}
    cells = [
        markdown("# Audit dataset kredit: tahap 1-3\n\n**Aqil — L0124139.** Menjaga raw, memeriksa data, menyusun kamus variabel, dan menetapkan aturan. Tidak membuat split/model. Script `audit_dataset.py` harus tetap berada di samping notebook. Dependensi: pandas dan numpy.\n\nSel notebook yang tersimpan sudah dijalankan berurutan memakai Python; lingkungan pembuat tidak menyediakan kernel Jupyter."),
        markdown("## 1. Temukan modul audit\n\nDapat dijalankan dari folder `kredit` atau root proyek. Pembacaan dan penulisan hasil audit dilakukan oleh fungsi di script yang dapat diperiksa."),
        code("import importlib.util\nfrom pathlib import Path\n\nbase = next((p for p in [Path.cwd(), *Path.cwd().parents] if (p / 'audit_dataset.py').is_file()), None)\nif base is None:\n    base = next((p / 'kredit' for p in [Path.cwd(), *Path.cwd().parents] if (p / 'kredit' / 'audit_dataset.py').is_file()), None)\nif base is None:\n    raise FileNotFoundError('Jalankan dari root proyek atau folder kredit.')\nspec = importlib.util.spec_from_file_location('credit_audit', base / 'audit_dataset.py')\naudit_module = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(audit_module)\nprint('Modul audit ditemukan.')\n"),
        markdown("## 2. Simpan snapshot raw dan manifest\n\nSumber asli tidak ditimpa. Snapshot yang sudah ada harus memiliki checksum sama; jika berbeda, proses berhenti. Tanggal unduh dan versi Kaggle tidak diketahui, sehingga dicatat kosong."),
        code("ctx = audit_module.prepare_source()\nprint('Dimensi:', ctx['df'].shape)\nprint('SHA-256:', ctx['hash'])\nprint('Raw snapshot dan sumber asli identik:', audit_module.digest(ctx['snapshot']) == ctx['hash'])\n"),
        markdown("## 3. Audit kualitas dan variasi\n\nIni audit seluruh data. Belum ada threshold outlier, seleksi fitur, atau transformasi yang dipelajari. Pengulangan berdasarkan fitur tidak otomatis berarti orang yang sama."),
        code("summary = audit_module.audit(ctx)\nfor key in ['missing_cells','nonfinite_values','n_ID_unik','duplicate_excluding_ID_excess','rows_in_repeated_feature_profiles','conflicting_label_groups','education_0_5_6_rows','marriage_0_rows','rows_with_negative_bill']:\n    print(key, ':', summary[key])\nprint('\\nDistribusi target:')\nprint(ctx['distribution'].to_string(index=False))\nprint('\\nProfil 25 kolom:')\nprint(ctx['profile'].to_string(index=False))\n"),
        markdown("## 4. Kamus variabel\n\nS1=UCI; S2=mirror Kaggle; S3=Lin dan Wang (preprint 2025). Arti PAY -2/0 dibedakan sumbernya dari definisi utama UCI. Kategori unknown adalah kebijakan konservatif kelompok."),
        code("data_dictionary = audit_module.dictionary(ctx)\nprint(data_dictionary[['kolom','arti','jenis_semantik','satuan']].to_string(index=False))\nprint('\\nDokumen lengkap: data_dictionary.md')\n"),
        markdown("## 5. Keputusan pembersihan\n\nAturan didokumentasikan tanpa menerapkan pembersihan ke raw. Pemisahan target/ID, pemetaan kategori, dan encoder dijalankan pada tahap berikutnya. Nilai negatif, nol, label berbeda dan fitur berkorelasi tidak dihapus otomatis."),
        code("rules = audit_module.cleaning_rules(ctx)\nprint(rules[['kode','isu','temuan','status']].to_string(index=False))\nprint('\\nDokumen lengkap: data_cleaning_decisions.md')\n"),
        markdown("## 6. Verifikasi dan serah terima\n\nCek sumber dan raw tetap sama, data yang dibaca tidak dimutasi, kamus mencakup seluruh kolom, dan hitungan saling sesuai. Output utama Aqil: README, kamus, dan keputusan pembersihan. Hasil audit bukan data siap model."),
        code("checks = audit_module.verify_and_report(ctx)\nfor name, passed in checks.items():\n    print(name, ':', passed)\nprint('\\nSelesai tahap 1-3. Tidak membuat split, encoding, model atau TreeSHAP.')\n"),
    ]
    for i, cell in enumerate(cells):
        cell["id"] = f"credit-audit-{i:02d}"
    notebook = {"nbformat": 4, "nbformat_minor": 5, "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}, "language_info": {"name": "python", "version": platform.python_version()}, "execution_method": "Sequential code-cell execution in Python, not a Jupyter kernel"}, "cells": cells}
    # Execute the real code cells, capture real output; no invented execution results.
    namespace = {"__name__": "__main__"}
    number = 0
    for cell in notebook["cells"]:
        if cell["cell_type"] != "code":
            continue
        number += 1
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            exec(compile("".join(cell["source"]), f"audit-cell-{number}", "exec"), namespace)
        cell["execution_count"] = number
        cell["outputs"] = [{"output_type": "stream", "name": "stdout", "text": captured.getvalue().splitlines(keepends=True)}]
        print(captured.getvalue(), end="")
    path = BASE / "01_dataset_audit.ipynb"
    write_json(path, notebook)
    print("Notebook tersimpan:", path.name)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    build_notebook()
