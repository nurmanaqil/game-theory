"""Small technical pilot, not the main attribution experiment."""
from pathlib import Path
import hashlib
import json
import platform
import time

import joblib
import numpy as np
import pandas as pd
import shap
import sklearn

BASE = Path(__file__).resolve().parent
SEED = 20261021
N_EXPLAIN = 20
N_BACKGROUND = 100


def main():
    out = BASE / "treeshap" / "pilot"
    out.mkdir(parents=True, exist_ok=True)
    check = json.loads((BASE / "treeshap" / "environment_model_check.json").read_text(encoding="utf-8"))
    model_path = BASE / "modeling" / "selected_rf.joblib"
    model_hash = hashlib.sha256(model_path.read_bytes()).hexdigest()
    assert check["status"] == "PASS" and model_hash == check["model_sha256"]
    model = joblib.load(model_path)
    encoded = BASE / "processed" / "encoded"
    X_train = pd.read_csv(encoded / "X_train.csv")
    X_test = pd.read_csv(encoded / "X_test.csv")
    assert list(X_train.columns) == list(X_test.columns) == list(model.feature_names_in_)
    # Selection is independent of labels, scores, or observed attribution differences.
    bg_idx = np.sort(np.random.default_rng(SEED).choice(len(X_train), N_BACKGROUND, replace=False))
    eval_idx = np.sort(np.random.default_rng(SEED + 1).choice(len(X_test), N_EXPLAIN, replace=False))
    background = X_train.iloc[bg_idx]
    X = X_test.iloc[eval_idx]
    background.to_csv(out / "background_train.csv", index=False)
    X.to_csv(out / "X_pilot.csv", index=False)
    for split, indices, name in [("train", bg_idx, "background_membership.csv"), ("test", eval_idx, "evaluation_membership.csv")]:
        metadata = pd.read_csv(BASE / "processed" / "metadata" / f"metadata_{split}.csv")
        subset = metadata.iloc[indices].copy()
        subset.insert(0, "split_row_index", indices)
        subset.to_csv(out / name, index=False)
    prediction = model.predict_proba(X)
    positive_index = list(model.classes_).index(1)
    results = []
    arrays = {}
    for mode in ["interventional", "tree_path_dependent"]:
        print(f"Menghitung {mode} untuk {len(X)} nasabah...", flush=True)
        start = time.perf_counter()
        # For sklearn RandomForestClassifier, raw tree output is class probability.
        # probability-mode transformation is not supported for tree_path_dependent.
        explainer = shap.TreeExplainer(
            model,
            data=background if mode == "interventional" else None,
            feature_perturbation=mode,
            model_output="raw",
        )
        values = np.asarray(explainer.shap_values(X, approximate=False, check_additivity=True))
        baseline = np.asarray(explainer.expected_value)
        assert values.shape == (len(X), X.shape[1], len(model.classes_)), values.shape
        assert baseline.shape == (len(model.classes_),)
        reconstructed = values.sum(axis=1) + baseline
        error = np.abs(reconstructed - prediction)
        passed = bool(np.allclose(reconstructed, prediction, rtol=0, atol=1e-6))
        assert np.isfinite(values).all() and passed, f"Additivity check failed for {mode}: {error.max()}"
        arrays[mode] = values[:, :, positive_index]
        np.savez_compressed(out / f"shap_{mode}.npz", values=values[:, :, positive_index], baseline=baseline[positive_index], test_row_indices=eval_idx, feature_names=np.asarray(X.columns, dtype=str))
        pd.DataFrame({
            "test_row_index": eval_idx,
            "probability_default": prediction[:, positive_index],
            "baseline_default": baseline[positive_index],
            "sum_shap_default": values[:, :, positive_index].sum(axis=1),
            "reconstructed_probability_default": reconstructed[:, positive_index],
            "absolute_error": error[:, positive_index],
        }).to_csv(out / f"additivity_{mode}.csv", index=False)
        results.append({"mode": mode, "n_explained": len(X), "baseline_default": float(baseline[positive_index]), "maximum_additivity_error_all_classes": float(error.max()), "additivity_passed": passed, "seconds": time.perf_counter() - start})
        print(f"LULUS {mode}: maksimum selisih additivity = {error.max():.3g}", flush=True)
    pd.DataFrame(results).to_csv(out / "pilot_summary.csv", index=False)
    bills = [f"BILL_AMT{i}" for i in range(1, 7)]
    bill_positions = [X.columns.get_loc(name) for name in bills]
    pd.DataFrame({
        "feature": bills,
        "interventional_mean_abs_shap": np.abs(arrays["interventional"][:, bill_positions]).mean(axis=0),
        "tree_path_dependent_mean_abs_shap": np.abs(arrays["tree_path_dependent"][:, bill_positions]).mean(axis=0),
        "mean_abs_paired_difference": np.abs(arrays["interventional"][:, bill_positions] - arrays["tree_path_dependent"][:, bill_positions]).mean(axis=0),
    }).to_csv(out / "billing_pilot_descriptive.csv", index=False)
    manifest = {
        "purpose": "technical pilot only; not a final research result",
        "seed_background": SEED, "seed_evaluation": SEED + 1,
        "background_source": "train", "evaluation_source": "test",
        "background_rows": bg_idx.tolist(), "evaluation_rows": eval_idx.tolist(),
        "model_sha256": model_hash, "model_output_argument": "raw",
        "verified_output_units": "class probabilities for sklearn RandomForestClassifier",
        "class_explained": 1, "class_index": positive_index,
        "approximate": False, "additivity_absolute_tolerance": 1e-6,
        "versions": {"python": platform.python_version(), "shap": shap.__version__, "sklearn": sklearn.__version__, "numpy": np.__version__, "pandas": pd.__version__},
        "results": results,
    }
    assert hashlib.sha256(model_path.read_bytes()).hexdigest() == model_hash
    (out / "pilot_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print("\n" + pd.DataFrame(results).round(6).to_string(index=False))
    print("\nHasil:", out)
    print("Pilot selesai. Jangan gunakan 20 nasabah ini untuk kesimpulan akhir penelitian.")


if __name__ == "__main__":
    main()
