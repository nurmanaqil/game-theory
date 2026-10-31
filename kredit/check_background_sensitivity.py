"""Sensitivity to two additional 100-row train backgrounds. Fixed model/test sample."""
from pathlib import Path
import hashlib
import json
import time

import joblib
import numpy as np
import pandas as pd
import shap
from scipy.stats import spearmanr

BASE = Path(__file__).resolve().parent
ADDITIONAL_SEEDS = [20261023, 20261024]
BILLS = [f"BILL_AMT{i}" for i in range(1, 7)]


def main():
    main_dir = BASE / "treeshap" / "main"
    out = BASE / "treeshap" / "background_check"
    out.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((main_dir / "main_manifest.json").read_text(encoding="utf-8"))
    model_path = BASE / "modeling" / "selected_rf.joblib"
    model_hash = hashlib.sha256(model_path.read_bytes()).hexdigest()
    assert model_hash == manifest["model_sha256"]
    model = joblib.load(model_path)
    train = pd.read_csv(BASE / "processed" / "encoded" / "X_train.csv")
    X = pd.read_csv(main_dir / "X_explanation_sample.csv")
    assert list(train.columns) == list(X.columns) == list(model.feature_names_in_)
    with np.load(main_dir / "shap_tree_path_dependent.npz", allow_pickle=False) as z:
        path_phi = z["values"]
        indices = z["test_row_indices"]
    with np.load(main_dir / "shap_interventional.npz", allow_pickle=False) as z:
        original_phi, original_base = z["values"], float(z["baseline"])
        assert np.array_equal(indices, z["test_row_indices"])
    positions = [list(X.columns).index(name) for name in BILLS]
    positive_index = list(model.classes_).index(1)
    probability = model.predict_proba(X)[:, positive_index]
    rows, ranking_rows = [], []

    def summarize(seed, phi, baseline, seconds, error):
        a, b = np.abs(phi[:, positions]), np.abs(path_phi[:, positions])
        tied_a = np.isclose(a, a.max(axis=1, keepdims=True), rtol=0, atol=1e-12).sum(axis=1) > 1
        tied_b = np.isclose(b, b.max(axis=1, keepdims=True), rtol=0, atol=1e-12).sum(axis=1) > 1
        valid = ~(tied_a | tied_b)
        n_valid = int(valid.sum())
        n_different = int(((a.argmax(axis=1) != b.argmax(axis=1)) & valid).sum())
        order = np.argsort(-a.mean(axis=0), kind="stable")
        rho = float(spearmanr(a.mean(axis=0), b.mean(axis=0)).statistic)
        rows.append({"background_seed": seed, "n_background": 100, "n_evaluation": len(X), "baseline_interventional": baseline, "global_billing_order": " > ".join(BILLS[i] for i in order), "spearman_vs_path": rho, "n_unique_both": n_valid, "n_disagreement_vs_path": n_different, "disagreement_rate_vs_path": n_different / n_valid if n_valid else None, "mean_abs_difference_from_original_interventional": float(np.abs(phi[:, positions] - original_phi[:, positions]).mean()), "max_additivity_error_class1": error, "seconds": seconds})
        ranks = pd.Series(a.mean(axis=0)).rank(ascending=False, method="average")
        for i, name in enumerate(BILLS):
            ranking_rows.append({"background_seed": seed, "feature": name, "mean_abs_shap_interventional": float(a[:, i].mean()), "rank_interventional": float(ranks.iloc[i])})

    original_error = float(np.abs(original_phi.sum(axis=1) + original_base - probability).max())
    assert original_error <= 1e-6
    summarize(manifest["seed_background"], original_phi, original_base, None, original_error)
    metadata = pd.read_csv(BASE / "processed" / "metadata" / "metadata_train.csv")
    for seed in ADDITIONAL_SEEDS:
        print(f"Menghitung background seed {seed} untuk {len(X)} nasabah...", flush=True)
        start = time.perf_counter()
        bg_indices = np.sort(np.random.default_rng(seed).choice(len(train), 100, replace=False))
        background = train.iloc[bg_indices]
        member = metadata.iloc[bg_indices].copy()
        member.insert(0, "train_row_index", bg_indices)
        member.to_csv(out / f"background_membership_{seed}.csv", index=False)
        background.to_csv(out / f"background_{seed}.csv", index=False)
        explainer = shap.TreeExplainer(model, data=background, feature_perturbation="interventional", model_output="raw")
        values = np.asarray(explainer.shap_values(X, approximate=False, check_additivity=True))
        assert values.shape == (len(X), X.shape[1], len(model.classes_))
        phi = values[:, :, positive_index]
        baseline = float(np.asarray(explainer.expected_value)[positive_index])
        error = float(np.abs(phi.sum(axis=1) + baseline - probability).max())
        assert np.isfinite(values).all() and error <= 1e-6
        np.savez_compressed(out / f"shap_interventional_{seed}.npz", values=phi, baseline=baseline, test_row_indices=indices, feature_names=np.asarray(X.columns, dtype=str))
        summarize(seed, phi, baseline, time.perf_counter() - start, error)
        print(f"LULUS seed {seed}: additivity error {error:.3g}", flush=True)
    table = pd.DataFrame(rows)
    table.to_csv(out / "background_comparison.csv", index=False)
    pd.DataFrame(ranking_rows).to_csv(out / "billing_ranks_by_background.csv", index=False)
    report = {"purpose": "descriptive sensitivity to three train background samples; original plus two additional", "model_sha256": model_hash, "fixed_test_rows": indices.tolist(), "background_seeds": [manifest["seed_background"], *ADDITIONAL_SEEDS], "n_background_each": 100, "shap_version": shap.__version__, "selection_of_background_by_results": False, "scope": "background composition only; not model seeds or background-size sensitivity"}
    (out / "background_check_manifest.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    assert hashlib.sha256(model_path.read_bytes()).hexdigest() == model_hash
    print("\n" + table.round(6).to_string(index=False))
    print("\nHasil:", out)
    print("Semua background dilaporkan; jangan hanya memilih background dengan hasil paling menarik.")


if __name__ == "__main__":
    main()
