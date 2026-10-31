"""Persiapan data Aqil: recoding tetap, grouped split, encoding train-only, EDA train.

Jalankan dari root proyek atau folder kredit: python kredit/preprocess_dataset.py
Membaca snapshot raw dan kebijakan audit; tidak melatih model.
"""
from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import json
import platform
import sys
import zipfile
from pathlib import Path

BASE = Path(__file__).resolve().parent
DEPS = BASE / ".analysis_deps"
if DEPS.exists():
    sys.path.insert(0, str(DEPS))

import numpy as np
import pandas as pd
import joblib
import sklearn
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.preprocessing import OneHotEncoder
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

spec = importlib.util.spec_from_file_location("credit_audit", BASE / "audit_dataset.py")
audit_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit_module)
TARGET, BILLS, CATEGORIES = audit_module.TARGET, audit_module.BILLS, audit_module.CATEGORIES
SEED = 20261020
OUT = BASE / "processed"
ARTIFACTS = BASE / "artifacts"
PAPER = BASE / "paper"


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save_json(path, value):
    audit_module.write_json(Path(path), value)


def load_and_recode():
    for folder in [OUT / "semantic", OUT / "encoded", OUT / "metadata", ARTIFACTS, PAPER / "tables", PAPER / "figures"]:
        folder.mkdir(parents=True, exist_ok=True)
    raw = BASE / "raw" / "UCI_Credit_Card.csv"
    original = BASE / "UCI_Credit_Card.csv"
    manifest = json.loads((BASE / "raw" / "manifest.json").read_text(encoding="utf-8"))
    if sha256(raw) != manifest["sha256"] or sha256(original) != manifest["sha256"]:
        raise RuntimeError("Raw/original berbeda dari manifest audit. Proses dihentikan tanpa menimpanya.")
    policy = json.loads((BASE / "audit" / "kebijakan_preprocessing.json").read_text(encoding="utf-8"))
    if policy["target"] != TARGET or policy["drop_predictors"] != ["ID"]:
        raise ValueError("Kebijakan audit berubah; tinjau ulang script sebelum meneruskan.")
    df = pd.read_csv(raw)
    if df.columns.tolist() != audit_module.EXPECTED:
        raise ValueError("Skema raw berbeda dari audit.")
    X = df.drop(columns=["ID", TARGET]).copy()
    y = df[TARGET].copy()
    remap_mask = X.EDUCATION.isin([0, 5, 6])
    recode_changed = X.EDUCATION.isin([5, 6])
    X.loc[remap_mask, "EDUCATION"] = 0
    # 0 di sini adalah unknown menurut kebijakan, bukan tingkatan pendidikan.
    # MARRIAGE=0 tidak berubah angka, tetapi diinterpretasikan sebagai unknown.
    assert df.equals(pd.read_csv(raw))
    assert X.columns.tolist() == [c for c in df if c not in ["ID", TARGET]]
    assert y.notna().all() and set(y.unique()) == {0, 1}
    assert not X.isna().any().any()
    assert np.isfinite(X.to_numpy()).all()
    unchanged = [c for c in X if c != "EDUCATION"]
    assert X[unchanged].equals(df[unchanged])
    group_num = X.groupby(X.columns.tolist(), sort=True, dropna=False).ngroup()
    group_name = group_num.map(lambda v: f"PROFILE_{int(v):05d}")
    group_size = group_num.map(group_num.value_counts())
    unique_targets = pd.DataFrame({"group": group_num, "target": y}).groupby("group").target.nunique()
    meta = pd.DataFrame({"ID": df.ID, "raw_row_index_0based": df.index, "profile_group": group_name})
    before = df.EDUCATION.value_counts().sort_index()
    after = X.EDUCATION.value_counts().sort_index()
    recode_table = pd.DataFrame({"code": sorted(set(before.index) | set(after.index))})
    recode_table["before"] = recode_table.code.map(before).fillna(0).astype(int)
    recode_table["after"] = recode_table.code.map(after).fillna(0).astype(int)
    recode_table["meaning_after"] = recode_table.code.map({0: "unknown", 1: "graduate school", 2: "university", 3: "high school", 4: "others", 5: "merged into 0", 6: "merged into 0"})
    recode_table.to_csv(PAPER / "tables" / "education_recode.csv", index=False, encoding="utf-8-sig")
    ctx = {"X": X, "y": y, "df": df, "meta": meta, "groups": group_num, "hash": manifest["sha256"], "original": original, "raw": raw,
           "remap_rows": int(remap_mask.sum()), "numeric_values_changed": int(recode_changed.sum()),
           "repeated_profile_rows": int(group_size.gt(1).sum()), "n_groups": int(group_num.nunique()),
           "repeated_profile_groups": int(group_num[group_size.gt(1)].nunique()),
           "conflicting_profile_groups": int(unique_targets.gt(1).sum()), "recode_table": recode_table}
    print(f"Retained {len(df):,} rows and {X.shape[1]} semantic predictors. ID excluded; target separated.")
    print(f"EDUCATION: {ctx['remap_rows']} rows in unknown; {ctx['numeric_values_changed']} numeric codes changed.")
    print(f"Profiles after recoding: {ctx['n_groups']:,} groups; {ctx['repeated_profile_rows']} rows in {ctx['repeated_profile_groups']} repeated groups.")
    return ctx


def split_data(ctx):
    X, y, groups, meta = ctx["X"], ctx["y"], ctx["groups"], ctx["meta"].copy()
    splitter = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=SEED)
    fold = np.full(len(X), -1, dtype=int)
    for k, (_, held_out) in enumerate(splitter.split(X, y, groups)):
        assert (fold[held_out] == -1).all()
        fold[held_out] = k
    assert (fold >= 0).all()
    split = pd.Series(np.where(fold == 0, "test", np.where(fold == 1, "validation", "train")), index=X.index)
    meta["fold"] = fold
    meta["split"] = split
    # Folds fixed before any performance analysis: 0=test, 1=validation, 2/3/4=train.
    assert meta.groupby("profile_group").split.nunique().eq(1).all()
    indices = {name: np.flatnonzero(split.eq(name).to_numpy()) for name in ["train", "validation", "test"]}
    rows = []
    overall_rate = y.mean()
    for name, idx in indices.items():
        part, label = X.iloc[idx], y.iloc[idx]
        part.to_csv(OUT / "semantic" / f"X_{name}.csv", index=False)
        label.to_frame().to_csv(OUT / "semantic" / f"y_{name}.csv", index=False)
        meta.iloc[idx].to_csv(OUT / "metadata" / f"metadata_{name}.csv", index=False)
        rows.append({"split": name, "n_rows": len(idx), "share_percent": len(idx) / len(X) * 100,
                     "nondefault": int(label.eq(0).sum()), "default": int(label.eq(1).sum()),
                     "default_percent": float(label.mean() * 100), "default_rate_difference_pp": float((label.mean() - overall_rate) * 100),
                     "n_groups": int(meta.iloc[idx].profile_group.nunique())})
    summary = pd.DataFrame(rows)
    if summary.default_rate_difference_pp.abs().max() > 2.0:
        raise RuntimeError("Deviasi proporsi kelas lebih dari batas audit 2 poin persentase. Tinjau split, jangan memilih dari performa model.")
    meta.to_csv(OUT / "metadata" / "split_manifest.csv", index=False)
    summary.to_csv(PAPER / "tables" / "split_summary.csv", index=False, encoding="utf-8-sig")
    ctx.update(indices=indices, meta=meta, split_summary=summary)
    print(summary.round(3).to_string(index=False))
    print("Profile-group overlap between splits: 0.")
    return summary


def encode_data(ctx):
    X, indices = ctx["X"], ctx["indices"]
    numeric = [c for c in X if c not in CATEGORIES]
    train = X.iloc[indices["train"]]
    ohe = OneHotEncoder(handle_unknown="ignore", drop=None, sparse_output=False, dtype=np.float64)
    transformer = ColumnTransformer([("numeric", "passthrough", numeric), ("category", ohe, CATEGORIES)], remainder="drop", verbose_feature_names_out=False)
    transformer.fit(train)  # Only training rows are allowed here.
    feature_names = transformer.get_feature_names_out().tolist()
    fitted_ohe = transformer.named_transformers_["category"]
    mapping = [{"encoded_feature": c, "source_feature": c, "type": "numeric", "category": ""} for c in numeric]
    cat_names = fitted_ohe.get_feature_names_out(CATEGORIES).tolist()
    pos = 0
    for source, categories in zip(CATEGORIES, fitted_ohe.categories_):
        for category in categories:
            mapping.append({"encoded_feature": cat_names[pos], "source_feature": source, "type": "one_hot", "category": int(category)})
            pos += 1
    map_table = pd.DataFrame(mapping)
    assert map_table.encoded_feature.tolist() == feature_names
    assert set(map_table.source_feature) == set(X.columns)
    unknown_rows = []
    widths = {}
    for name, idx in indices.items():
        semantic = X.iloc[idx]
        encoded = pd.DataFrame(transformer.transform(semantic), columns=feature_names)
        assert np.isfinite(encoded.to_numpy()).all()
        assert encoded.shape[0] == len(idx)
        assert not {"ID", TARGET}.intersection(encoded.columns)
        encoded.to_csv(OUT / "encoded" / f"X_{name}.csv", index=False)
        ctx["y"].iloc[idx].to_frame().to_csv(OUT / "encoded" / f"y_{name}.csv", index=False)
        widths[name] = encoded.shape[1]
        for source, known in zip(CATEGORIES, fitted_ohe.categories_):
            unseen = semantic.loc[~semantic[source].isin(known), source]
            unknown_rows.append({"split": name, "feature": source, "unseen_rows": len(unseen), "unseen_values": ",".join(str(v) for v in sorted(unseen.unique()))})
    unseen_table = pd.DataFrame(unknown_rows)
    unseen_table.to_csv(PAPER / "tables" / "unseen_categories.csv", index=False, encoding="utf-8-sig")
    map_table.to_csv(ARTIFACTS / "feature_map.csv", index=False)
    joblib.dump(transformer, ARTIFACTS / "preprocessor.joblib")
    schema = {"target": TARGET, "id_column_excluded": "ID", "raw_predictors": X.columns.tolist(),
              "numeric_columns": numeric, "categorical_columns": CATEGORIES, "encoded_features": feature_names,
              "bill_features": BILLS, "education_map": {"0": 0, "5": 0, "6": 0},
              "unknown_category_policy": "OneHotEncoder(handle_unknown='ignore'): unseen categories map to all-zero indicators within their source feature; report separately.",
              "ohe_drop": None, "fit_split": "train", "scaling": None, "resampling": None,
              "row_order_contract": "X/y/metadata within each split share row order. All CSVs are saved without pandas index. Do not sort files independently.",
              "shap_contract": "Compute SHAP on model inputs in encoded feature order. Aggregate one-hot signed attributions to source features using feature_map before source-level interpretation. Billing features remain numeric single columns."}
    save_json(ARTIFACTS / "feature_schema.json", schema)
    ctx.update(preprocessor=transformer, encoded_features=feature_names, feature_map=map_table, numeric=numeric, unseen=unseen_table, widths=widths)
    print(f"Encoder fit on train only: {len(numeric)} numeric + {len(cat_names)} indicator columns = {len(feature_names)} model inputs.")
    print("Unseen categories per split:")
    print(unseen_table.groupby("split").unseen_rows.sum().to_string())
    return schema


def correlations_and_figures(ctx):
    train = ctx["X"].iloc[ctx["indices"]["train"]]
    pearson = train[BILLS].corr(method="pearson")
    spearman = train[BILLS].corr(method="spearman")
    pearson.to_csv(PAPER / "tables" / "correlation_pearson_train.csv", index_label="feature")
    spearman.to_csv(PAPER / "tables" / "correlation_spearman_train.csv", index_label="feature")
    pairs = []
    for i, a in enumerate(BILLS):
        for b in BILLS[i+1:]:
            pairs.append({"feature_a": a, "feature_b": b, "pearson_train": float(pearson.loc[a,b]), "spearman_train": float(spearman.loc[a,b])})
    pair_table = pd.DataFrame(pairs)
    pair_table.to_csv(PAPER / "tables" / "billing_correlation_pairs_train.csv", index=False)
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.titlesize": 12, "axes.labelsize": 10, "figure.facecolor": "white", "savefig.facecolor": "white"})
    fig, axes = plt.subplots(1, 2, figsize=(12.8, 5.9), layout="constrained")
    for ax, matrix, title in zip(axes, [pearson, spearman], ["Pearson correlation", "Spearman rank correlation"]):
        im = ax.imshow(matrix, vmin=0, vmax=1, cmap="Blues")
        ax.set_xticks(range(6), BILLS, rotation=45, ha="right", fontsize=9)
        ax.set_yticks(range(6), BILLS, fontsize=9)
        ax.set_title(title)
        for row in range(6):
            for col in range(6):
                value = matrix.iloc[row,col]
                ax.text(col, row, f"{value:.3f}", ha="center", va="center", fontsize=9, color="white" if value > 0.68 else "#17212e")
        ax.tick_params(length=0)
        for spine in ax.spines.values():
            spine.set_visible(False)
    fig.colorbar(im, ax=axes, shrink=.75, label="Correlation coefficient", pad=.02)
    fig.suptitle(f"Monthly billing features: training data only (n = {len(train):,})", fontsize=14)
    fig.savefig(PAPER / "figures" / "billing_correlation_train.png", dpi=220)
    fig.savefig(PAPER / "figures" / "billing_correlation_train.pdf")
    plt.close(fig)
    counts = ctx["split_summary"]
    fig, ax = plt.subplots(figsize=(7.6, 4.5), layout="constrained")
    x = np.arange(3)
    pct = counts.default_percent.to_numpy()
    ax.bar(x, 100-pct, color="#c6d5e6", label="Non-default")
    ax.bar(x, pct, bottom=100-pct, color="#245b8a", label="Default")
    for i, row in enumerate(counts.itertuples()):
        ax.text(i, 100-row.default_percent/2, f"{row.default_percent:.2f}%", ha="center", va="center", color="white", fontsize=11)
        ax.text(i, (100-row.default_percent)/2, f"{100-row.default_percent:.2f}%", ha="center", va="center", color="#17212e", fontsize=11)
    ax.set_xticks(x, [f"{r.split.title()}\nn = {r.n_rows:,}" for r in counts.itertuples()])
    ax.set_ylim(0, 105)
    ax.set_ylabel("Share of observations (%)")
    ax.set_title("Class distribution after grouped data partitioning")
    ax.legend(loc="upper center", bbox_to_anchor=(.5, -.15), ncol=2, frameon=False)
    ax.spines[["top","right"]].set_visible(False)
    fig.savefig(PAPER / "figures" / "class_distribution_splits.png", dpi=220)
    fig.savefig(PAPER / "figures" / "class_distribution_splits.pdf")
    plt.close(fig)
    ctx.update(pearson=pearson, spearman=spearman, pair_table=pair_table)
    print("Training correlation matrices saved; no validation/test correlations used for feature choice.")
    print(pair_table.round(4).to_string(index=False))
    return pair_table


def verify_outputs(ctx):
    X, y, meta = ctx["X"], ctx["y"], ctx["meta"]
    checks = {
        "raw_original_unchanged": sha256(ctx["original"]) == ctx["hash"],
        "raw_snapshot_unchanged": sha256(ctx["raw"]) == ctx["hash"],
        "no_rows_dropped": sum(len(v) for v in ctx["indices"].values()) == len(ctx["df"]),
        "ID_not_in_predictors": "ID" not in X,
        "target_not_in_predictors": TARGET not in X,
        "all_six_billing_features_retained": set(BILLS).issubset(X.columns),
        "raw_billing_values_unchanged": X[BILLS].equals(ctx["df"][BILLS]),
        "negative_bill_count_unchanged": int(X[BILLS].lt(0).sum().sum()) == int(ctx["df"][BILLS].lt(0).sum().sum()),
        "profile_groups_disjoint": meta.groupby("profile_group").split.nunique().eq(1).all(),
        "ID_unique_and_covered_once": meta.ID.is_unique and set(meta.ID) == set(ctx["df"].ID),
        "both_classes_in_all_splits": all(set(y.iloc[idx].unique()) == {0,1} for idx in ctx["indices"].values()),
        "stratification_deviation_within_2pp": ctx["split_summary"].default_rate_difference_pp.abs().max() <= 2,
        "consistent_encoded_feature_order": len(set(ctx["widths"].values())) == 1,
    }
    train = X.iloc[ctx["indices"]["train"]]
    ohe = ctx["preprocessor"].named_transformers_["category"]
    checks["encoder_categories_from_train_only"] = all(np.array_equal(known, np.sort(train[c].unique())) for c, known in zip(CATEGORIES, ohe.categories_))
    loaded_transformer = joblib.load(ARTIFACTS / "preprocessor.joblib")
    checks["saved_transformer_matches"] = np.array_equal(loaded_transformer.transform(train.iloc[:7]), ctx["preprocessor"].transform(train.iloc[:7]))
    for name, idx in ctx["indices"].items():
        saved_X = pd.read_csv(OUT / "encoded" / f"X_{name}.csv")
        saved_y = pd.read_csv(OUT / "encoded" / f"y_{name}.csv")[TARGET]
        saved_meta = pd.read_csv(OUT / "metadata" / f"metadata_{name}.csv")
        semantic = pd.read_csv(OUT / "semantic" / f"X_{name}.csv")
        checks[f"{name}_feature_names"] = saved_X.columns.tolist() == ctx["encoded_features"]
        checks[f"{name}_encoded_matches_semantic"] = np.allclose(saved_X.to_numpy(), loaded_transformer.transform(semantic), rtol=1e-13, atol=1e-12)
        checks[f"{name}_labels_match_raw_ID"] = np.array_equal(saved_y.to_numpy(), ctx["df"].set_index("ID").loc[saved_meta.ID, TARGET].to_numpy())
        checks[f"{name}_row_alignment"] = len(saved_X) == len(saved_y) == len(saved_meta) == len(idx)
        checks[f"{name}_finite"] = np.isfinite(saved_X.to_numpy()).all()
    checks = {k: bool(v) for k,v in checks.items()}
    save_json(ARTIFACTS / "preprocessing_checks.json", checks)
    if not all(checks.values()):
        raise AssertionError({k:v for k,v in checks.items() if not v})
    config = {"seed": SEED, "partition": "StratifiedGroupKFold(n_splits=5, shuffle=True): fold0=test; fold1=validation; folds2,3,4=train", "groups": "Exact equality of 23 semantic predictors after prespecified EDUCATION mapping; excludes ID and target.",
              "target_ratios": {"train": .6, "validation": .2, "test": .2}, "raw_sha256": ctx["hash"],
              "n_rows": len(X), "n_semantic_features": X.shape[1], "n_encoded_features": len(ctx["encoded_features"]),
              "rows_dropped": 0, "education_unknown_rows": ctx["remap_rows"], "education_numeric_codes_changed": ctx["numeric_values_changed"],
              "n_profile_groups_after_recode": ctx["n_groups"], "repeated_profile_rows_after_recode": ctx["repeated_profile_rows"], "repeated_profile_groups_after_recode": ctx["repeated_profile_groups"],
              "conflicting_target_groups_after_recode": ctx["conflicting_profile_groups"],
              "versions": {"python": platform.python_version(), "numpy": np.__version__, "pandas": pd.__version__, "scikit_learn": sklearn.__version__, "matplotlib": matplotlib.__version__, "joblib": joblib.__version__},
              "training_started": False, "model_results_available": False}
    save_json(ARTIFACTS / "preprocessing_config.json", config)
    save_json(ARTIFACTS / "artifact_checksums.json", {str(p.relative_to(BASE)).replace('\\','/'): sha256(p) for p in sorted(OUT.rglob("*.csv"))})
    ctx["checks"] = checks
    ctx["config"] = config
    print(f"Verification passed: {sum(checks.values())}/{len(checks)} checks.")
    return checks


def write_deliverables(ctx):
    table = audit_module.md_table
    split = ctx["split_summary"][["split", "n_rows", "nondefault", "default", "default_percent"]].copy()
    split["default_percent"] = split.default_percent.map(lambda x: f"{x:.2f}%")
    split["split"] = split["split"].str.title()
    split.columns = ["Partition", "Observations", "Non-default", "Default", "Default share"]
    train_n = int(ctx["split_summary"].loc[ctx["split_summary"].split.eq("train"), "n_rows"].iloc[0])
    pair = ctx["pair_table"]
    rmin, rmax = pair.pearson_train.min(), pair.pearson_train.max()
    smin, smax = pair.spearman_train.min(), pair.spearman_train.max()
    main_pair = pair[(pair.feature_a == "BILL_AMT1") & (pair.feature_b == "BILL_AMT2")].iloc[0]
    unknown_nontrain = int(ctx["unseen"].loc[ctx["unseen"].split.ne("train"), "unseen_rows"].sum())
    clean_table = pd.DataFrame([
        ["ID", "Excluded from model inputs; retained in metadata", "Identifier is not a substantive predictor"],
        [TARGET, "Separated as target", "Prevent target leakage"],
        ["EDUCATION", "Codes 0/5/6 merged as unknown (code 0); 4 retained as others", "Conservative treatment of insufficiently documented categories"],
        ["MARRIAGE", "Code 0 retained as unknown", "Do not invent a specific status"],
        ["PAY status features", "Retained as categorical, including -2/-1/0", "Distinct recorded states are not missing values"],
        ["Billing/payment amounts", "Retained, including negative bills and zero payments", "No verified basis for automatic deletion"],
        ["Repeated profiles", "Retained; same feature profile assigned to one partition", "Limit identical-profile overlap without replacing observed outcomes"],
        ["All rows", "Retained; no imputation, scaling, clipping, or resampling", "Preserve observations and limit extra experimental factors"],
    ], columns=["Item", "Treatment", "Rationale"])
    clean_table.to_csv(PAPER / "tables" / "preprocessing_summary.csv", index=False, encoding="utf-8-sig")
    manuscript = "# Dataset and Preprocessing\n\n"
    manuscript += "## Data source and outcome\n\nThe study uses the Default of Credit Card Clients dataset, originally distributed by the UCI Machine Learning Repository and obtained through its Kaggle mirror [D1,D2]. The local dataset contains 30,000 customer records, 23 candidate predictors, one identifier, and one binary outcome. The six-month histories cover April-September 2005. Financial amounts are denominated in New Taiwan dollars. The target indicates default payment in the following month. There are 6,636 default observations (22.12%) and 23,364 non-default observations (77.88%). This is a customer-level historical classification dataset; ID order is not a temporal observation sequence.\n\n"
    manuscript += "## Quality audit and prespecified transformations\n\nThe original CSV was preserved and verified against a raw snapshot using SHA-256. The audit found no missing or nonfinite values. ID was excluded from the predictor matrix, and the outcome was stored separately. EDUCATION codes 0, 5, and 6 were mapped to a single unknown category, while code 4 remained others. This policy affected 345 observations, of which 331 changed numeric code because 14 were already coded 0. MARRIAGE code 0 was retained as a separate unknown category. Negative billing amounts, zero payments, and observed repayment-status categories were retained. The interpretation of additional repayment-status codes was documented using supplementary literature rather than inferred from their numeric sign [D3]. No observations were removed, no outlier clipping was performed, and no class resampling was applied.\n\n"
    manuscript += table(clean_table) + "\n\nTable 1. Prespecified data preparation decisions.\n\n"
    manuscript += f"## Group-aware partitioning\n\nCustomer profiles were grouped by exact equality of the 23 predictors after deterministic category mapping, excluding ID and outcome. There were {ctx['n_groups']:,} distinct profiles; {ctx['repeated_profile_rows']} records belonged to {ctx['repeated_profile_groups']} repeated-profile groups. Groups with different observed outcomes were retained without relabeling. A five-fold StratifiedGroupKFold partition was generated using shuffle=True and random_state={SEED}. Fold 0 was assigned to test, fold 1 to validation, and folds 2-4 to training, targeting a 60:20:20 partition [D4]. Fold allocation was fixed without model-performance-based selection. Identical mapped profiles did not cross partitions. This grouping reduces identical-profile overlap but does not establish independence with respect to unobserved customer relationships.\n\n"
    manuscript += table(split) + "\n\nTable 2. Actual partition sizes and class composition.\n\n"
    unseen_sentence = ("No unseen categorical values were found in validation or test." if unknown_nontrain == 0 else f"The held-out audit found {unknown_nontrain} categorical field occurrence(s) not seen in training; these were represented as all-zero indicators within the affected source variable.")
    manuscript += f"## Encoding\n\nThe nine categorical predictors were one-hot encoded with no reference category dropped. The encoder was fitted only on the {train_n:,} training observations and then applied unchanged to validation and test, using handle_unknown='ignore' [D5]. The 14 numerical predictors were passed through without scaling. The resulting matrices contain {len(ctx['encoded_features'])} inputs in the same order across partitions. The six BILL_AMT features remain individual numerical columns. A mapping from encoded columns to original variables was saved for subsequent source-feature-level explanation. {unseen_sentence} Held-out data were not used to refit the encoder.\n\n"
    manuscript += f"## Exploratory correlation analysis\n\nCorrelation analysis used training observations only. Pairwise Pearson correlations among BILL_AMT1-BILL_AMT6 ranged from {rmin:.3f} to {rmax:.3f}, while Spearman correlations ranged from {smin:.3f} to {smax:.3f}. For BILL_AMT1 and BILL_AMT2, the corresponding coefficients were {main_pair.pearson_train:.3f} and {main_pair.spearman_train:.3f}. These descriptive results support examining attribution allocation among strongly associated billing features. They do not establish causal relationships or show that billing features dominate the fitted predictor. No correlated billing feature was removed because these features are the object of the planned TreeSHAP comparison.\n\n"
    manuscript += "![Training-only billing correlations](../figures/billing_correlation_train.png)\n\nFigure 1. Pearson and Spearman correlations among six monthly billing features in the training partition.\n\n"
    manuscript += "![Class composition of partitions](../figures/class_distribution_splits.png)\n\nFigure 2. Class composition after group-aware partitioning. Labels report within-partition percentages.\n\n"
    manuscript += "## Reproducibility and scope\n\nRaw checksum, split membership, software versions, feature ordering, category mapping, fitted preprocessor, and validation checks were recorded. Preparation of the dataset does not establish model performance or TreeSHAP findings; these require subsequent modeling and explanation experiments. All checks reported here concern data preparation.\n\n## References for this section\n\n"
    manuscript += "[D1] I. Yeh, Default of Credit Card Clients, UCI Machine Learning Repository, 2009. https://doi.org/10.24432/C55S3H\n\n[D2] Kaggle mirror: https://www.kaggle.com/datasets/uciml/default-of-credit-card-clients-dataset\n\n[D3] L. Lin and Y. Wang, SHAP Stability in Credit Risk Management: A Case Study in Credit Card Default Model, 2025. https://doi.org/10.3390/risks13120238 (supplementary code interpretations checked against the preprint: https://arxiv.org/pdf/2508.01851).\n\n[D4] scikit-learn 1.7, StratifiedGroupKFold documentation. https://scikit-learn.org/1.7/modules/generated/sklearn.model_selection.StratifiedGroupKFold.html\n\n[D5] scikit-learn 1.7, OneHotEncoder documentation. https://scikit-learn.org/1.7/modules/generated/sklearn.preprocessing.OneHotEncoder.html\n"
    (PAPER / "archive").mkdir(parents=True, exist_ok=True)
    (PAPER / "archive/dataset_preprocessing_legacy.md").write_text(manuscript, encoding="utf-8")
    guide = "# Hasil Aqil: apa yang dikeluarkan dan apa yang masuk paper\n\n"
    guide += "## Status\n\nPreprocessing, split tetap, encoding train-only, analisis korelasi train, dan bahan metode selesai. Belum melatih model atau menghitung TreeSHAP.\n\n"
    guide += "## Apa yang di-drop?\n\n- ID dikeluarkan dari X, tetap ada pada metadata.\n- Target dipisahkan sebagai y, bukan dihapus dari penelitian.\n- Tidak ada baris dihapus. Tagihan negatif, pembayaran nol, label berbeda pada profil sama, serta enam tagihan berkorelasi tetap disimpan.\n"
    guide += f"- EDUCATION: 345 observasi menjadi unknown; 331 kode 5/6 berubah ke 0, sementara 14 kode 0 sudah unknown. MARRIAGE 0 tetap unknown.\n\n## Pembagian aktual\n\n" + table(split)
    guide += f"\n\nProfil identik dihitung ulang setelah recoding: {ctx['repeated_profile_rows']} baris dalam {ctx['repeated_profile_groups']} kelompok. Tidak ada kelompok yang tersebar ke lebih dari satu split. Matriks model memiliki {len(ctx['encoded_features'])} kolom hasil encoding dari 23 fitur asal.\n\n"
    guide += "## Output untuk paper\n\nBuka `paper/dataset_preprocessing.md` sebagai bahan paper aktif. Sesuaikan penomoran tabel, gambar, dan sitasi dengan naskah bersama. Draf awal dengan sitasi D1-D5 tersimpan di `paper/archive/dataset_preprocessing_legacy.md`. Gambar PNG/PDF di `paper/figures/` siap dimasukkan. Tabel CSV di `paper/tables/` adalah sumber angka untuk tabel naskah, bukan semua wajib ditampilkan.\n\n"
    guide += "Bagian ini dapat ditulis sebagai pekerjaan yang sudah dilakukan. Klaim performa Random Forest, fitur terpenting, atau perbedaan TreeSHAP belum boleh ditambahkan sebelum eksperimen model.\n\n"
    guide += "## Output untuk Irfan\n\nGunakan `processed/encoded/X_train.csv` dan `y_train.csv` untuk pelatihan. Validation dipakai memilih pengaturan/threshold. Test disisihkan untuk evaluasi akhir. Jangan melakukan split baru atau fit ulang encoder pada gabungan data. Urutan baris X, y, dan metadata konsisten; jangan mengurutkan salah satunya secara terpisah.\n\n"
    guide += "Contoh pembacaan:\n\n```python\nfrom pathlib import Path\nimport pandas as pd\nbase = Path('kredit/processed/encoded')\nX_train = pd.read_csv(base / 'X_train.csv')\ny_train = pd.read_csv(base / 'y_train.csv')['default.payment.next.month']\nX_val = pd.read_csv(base / 'X_validation.csv')\ny_val = pd.read_csv(base / 'y_validation.csv')['default.payment.next.month']\n```\n\n"
    guide += "## Output untuk Yahya\n\nGunakan input model dalam urutan `artifacts/feature_schema.json`. Background TreeSHAP interventional harus berasal dari train. Gunakan `feature_map.csv` untuk menjumlahkan atribusi signed indikator kategori kembali ke fitur asal sebelum ringkasan feature-level. Penjumlahan indikator untuk pelaporan tidak otomatis sama dengan Shapley dari permainan fitur yang digabung. Semua BILL_AMT tetap satu kolom numerik.\n\n"
    guide += "## Struktur hasil\n\n- `processed/semantic/`: fitur dengan nama asal sesudah pemetaan; untuk audit/EDA.\n- `processed/encoded/`: X dan y siap model, tanpa ID atau index tambahan.\n- `processed/metadata/`: ID, grup profil, fold, dan membership split.\n- `artifacts/`: preprocessor, skema, feature map, konfigurasi, checksum, dan hasil verifikasi.\n- `paper/`: teks metode, tabel, gambar.\n- `Paket_Aqil_untuk_Irfan.zip`: paket lokal untuk handoff dan reproduksi.\n\n"
    guide += "## Batas dan perhatian\n\nKode kategori yang tidak jelas diperlakukan konservatif. Data historis Taiwan bukan pembuktian untuk nasabah Indonesia saat ini. Pengelompokan profil hanya mengatasi kesamaan fitur yang teramati. Kategori validation/test yang tidak dijumpai di train dicatat di `paper/tables/unseen_categories.csv`; kebijakan ignore dipertahankan dan encoder tidak diperbarui dari held-out data.\n\n"
    guide += f"## Verifikasi\n\n{sum(ctx['checks'].values())}/{len(ctx['checks'])} pemeriksaan lulus: checksum raw tetap, tidak ada grup lintas-split, encoder hanya mengikuti kategori train, alignment ID/label benar, nilai finite, urutan fitur sama, dan artefak hasil simpan dapat dibaca ulang.\n"
    (BASE / "preprocessing_guide.md").write_text(guide, encoding="utf-8")
    # Requirements for a normal isolated environment; installed versions are recorded too.
    import scipy
    requirements = {"numpy": np.__version__, "pandas": pd.__version__, "scikit-learn": sklearn.__version__, "scipy": scipy.__version__, "joblib": joblib.__version__, "matplotlib": matplotlib.__version__}
    (BASE / "requirements_preprocessing.txt").write_text("\n".join(f"{k}=={v}" for k,v in requirements.items()) + "\n", encoding="utf-8")
    print("Paper text, tables, figures, and handoff guide saved.")


def build_notebook():
    def md(s):
        return {"cell_type": "markdown", "metadata": {}, "source": s.splitlines(keepends=True)}
    def code(s):
        return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": s.splitlines(keepends=True)}
    cells = [md("# Preprocessing, grouped split, encoding, dan EDA train\n\n**Aqil — L0124139.** Melanjutkan audit tahap 1-3. Raw tetap. Semua data disimpan; ID/target dipisahkan dari X. Script `preprocess_dataset.py` dan `audit_dataset.py` harus tetap di folder yang sama. Dependensi tercatat di requirements_preprocessing.txt. Notebook tersimpan dieksekusi menggunakan Python secara berurutan, bukan kernel Jupyter pada lingkungan pembuat."),
        code("import importlib.util\nfrom pathlib import Path\nbase = next((p for p in [Path.cwd(), *Path.cwd().parents] if (p / 'preprocess_dataset.py').is_file()), None)\nif base is None:\n    base = next((p / 'kredit' for p in [Path.cwd(), *Path.cwd().parents] if (p / 'kredit' / 'preprocess_dataset.py').is_file()), None)\nif base is None:\n    raise FileNotFoundError('Jalankan dari folder kredit atau root proyek.')\nspec = importlib.util.spec_from_file_location('credit_preprocessing', base / 'preprocess_dataset.py')\np = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(p)\nprint('Modul preprocessing siap.')\n"),
        md("## 1. Pemetaan deterministik dan grup profil\n\nKategori dipetakan berdasarkan kebijakan audit yang sudah ditetapkan. Kelompok dibentuk dari kesamaan X setelah mapping, tanpa ID/target. Belum ada fit statistik."),
        code("ctx = p.load_and_recode()\nprint(ctx['recode_table'].to_string(index=False))\n"),
        md("## 2. Split tetap\n\nLima fold StratifiedGroupKFold dengan seed 20261020. Fold 0=test, 1=validation, 2/3/4=train. Rasio mendekati 60/20/20 karena grup tidak dipecah. Tidak memilih split dari performa model."),
        code("split_summary = p.split_data(ctx)\n"),
        md("## 3. Encoding dari train saja\n\n14 numerik dipertahankan, 9 kategori di-one-hot tanpa drop kategori acuan. Kategori baru held-out diabaikan dan dicatat, tidak dipakai fit ulang. X/y/metadata memiliki urutan baris sama."),
        code("schema = p.encode_data(ctx)\n"),
        md("## 4. Korelasi train dan gambar paper\n\nPearson dan Spearman hanya memakai train. Fitur yang berkorelasi tidak dihapus karena merupakan objek penelitian. Korelasi bukan bukti sebab-akibat atau kontribusi model."),
        code("correlation_pairs = p.correlations_and_figures(ctx)\n"),
        md("## 5. Periksa artefak hasil simpan\n\nPeriksa checksum, coverage, grup, kategori train, urutan fitur, dan label berdasarkan ID. Tidak ada model dilatih pada notebook ini."),
        code("checks = p.verify_outputs(ctx)\nfor name, passed in checks.items():\n    print(name, ':', passed)\n"),
        md("## 6. Teks metode dan handoff\n\nMasukkan teks metode dan gambar ke naskah bersama. Data encoded diserahkan ke Irfan, feature map ke Yahya. Tidak semua file teknis perlu masuk badan paper."),
        code("p.write_deliverables(ctx)\n"),
    ]
    for i,c in enumerate(cells):
        c["id"] = f"credit-preprocess-{i:02d}"
    notebook = {"nbformat": 4, "nbformat_minor": 5, "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}, "language_info": {"name": "python", "version": platform.python_version()}, "execution_method": "Sequential Python code cells; no Jupyter kernel invoked"}, "cells": cells}
    namespace = {"__name__": "__main__"}
    counter = 0
    for c in cells:
        if c["cell_type"] != "code":
            continue
        counter += 1
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            exec(compile("".join(c["source"]), f"preprocess-cell-{counter}", "exec"), namespace)
        c["execution_count"] = counter
        c["outputs"] = [{"output_type": "stream", "name": "stdout", "text": stream.getvalue().splitlines(keepends=True)}]
        print(stream.getvalue(), end="", flush=True)
    save_json(BASE / "02_preprocessing.ipynb", notebook)
    return namespace["ctx"]


def package_handoff():
    selected = [BASE / name for name in ["audit_dataset.py", "preprocess_dataset.py", "UCI_Credit_Card.csv", "01_dataset_audit.ipynb", "data_dictionary.md", "data_cleaning_decisions.md", "preprocessing_guide.md", "02_preprocessing.ipynb", "dataset_audit.md", "requirements_preprocessing.txt"]]
    for folder in ["raw", "audit", "processed", "artifacts", "paper"]:
        selected.extend(p for p in (BASE / folder).rglob("*") if p.is_file())
    bundle = BASE / "Paket_Aqil_untuk_Irfan.zip"
    with zipfile.ZipFile(bundle, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for file in sorted(set(selected)):
            z.write(file, arcname="kredit/" + str(file.relative_to(BASE)).replace("\\", "/"))
    with zipfile.ZipFile(bundle) as z:
        if z.testzip() is not None:
            raise RuntimeError("Verifikasi paket zip gagal.")
    print(f"Handoff ZIP verified: {bundle.stat().st_size / 1024**2:.2f} MB.")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    build_notebook()
    package_handoff()
