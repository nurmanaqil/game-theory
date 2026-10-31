"""Evaluate the frozen model and threshold on test; no fitting or selection."""
from pathlib import Path
import hashlib
import json
import platform

import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, average_precision_score, confusion_matrix,
    roc_curve, precision_recall_curve, ConfusionMatrixDisplay,
)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent
OUT = BASE / "modeling"
DATA = BASE / "processed" / "encoded"
FIGURES = OUT / "figures"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    FIGURES.mkdir(exist_ok=True)
    model_path = OUT / "selected_rf.joblib"
    threshold_path = OUT / "selected_threshold.json"
    config_path = OUT / "selected_rf_config.json"
    threshold_config = json.loads(threshold_path.read_text(encoding="utf-8"))
    config = json.loads(config_path.read_text(encoding="utf-8"))
    before = {p.name: digest(p) for p in [model_path, threshold_path, config_path]}
    assert digest(model_path) == threshold_config["model_sha256"], "Model differs from threshold-selection model."
    model = joblib.load(model_path)
    X = pd.read_csv(DATA / "X_test.csv")
    y = pd.read_csv(DATA / "y_test.csv").squeeze("columns")
    assert len(X) == len(y) == 5998
    assert list(X.columns) == config["feature_order"] == list(model.feature_names_in_)
    assert np.isfinite(X.to_numpy()).all()
    assert set(y.unique()) == {0, 1}
    positive_index = list(model.classes_).index(1)
    probability = model.predict_proba(X)[:, positive_index]
    assert np.isfinite(probability).all() and ((probability >= 0) & (probability <= 1)).all()
    threshold = float(threshold_config["threshold"])
    ap = average_precision_score(y, probability)
    auc = roc_auc_score(y, probability)
    rows = []
    matrices = {}
    # Both thresholds were fixed before test evaluation; neither is selected here.
    for name, value in [("Default threshold", 0.5), ("Validation-selected threshold", threshold)]:
        prediction = (probability >= value).astype(int)
        cm = confusion_matrix(y, prediction, labels=[0, 1])
        tn, fp, fn, tp = cm.ravel()
        matrices[name] = cm
        rows.append({
            "Setting": name, "Threshold": value,
            "Accuracy": accuracy_score(y, prediction),
            "Precision": precision_score(y, prediction, zero_division=0),
            "Recall": recall_score(y, prediction, zero_division=0),
            "F1": f1_score(y, prediction, zero_division=0),
            "ROC_AUC": auc, "Average_precision": ap,
            "TN": int(tn), "FP": int(fp), "FN": int(fn), "TP": int(tp),
        })
    result = pd.DataFrame(rows)
    result.to_csv(OUT / "test_metrics.csv", index=False)
    predictions = pd.DataFrame({
        "test_row_index": np.arange(len(y)), "y_true": y.to_numpy(),
        "probability_default": probability,
        "prediction_threshold_0_5": (probability >= 0.5).astype(int),
        "prediction_selected_threshold": (probability >= threshold).astype(int),
    })
    metadata_path = BASE / "processed" / "metadata" / "metadata_test.csv"
    # Preserve positional alignment with the original test matrix.
    metadata = pd.read_csv(metadata_path)
    assert len(metadata) == len(predictions)
    pd.concat([metadata.reset_index(drop=True), predictions], axis=1).to_csv(
        OUT / "predictions_test.csv", index=False
    )

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.4))
    for ax, (name, cm) in zip(axes, matrices.items()):
        ConfusionMatrixDisplay(cm, display_labels=["Non-default", "Default"]).plot(
            ax=ax, colorbar=False, cmap="Blues", values_format="d"
        )
        value = 0.5 if name == "Default threshold" else threshold
        ax.set_title(f"{name}\nThreshold = {value:.4f}")
    fig.suptitle("Random Forest: test-set confusion matrices (n = 5,998)")
    fig.tight_layout()
    for extension in ["png", "pdf"]:
        fig.savefig(FIGURES / f"test_confusion_matrices.{extension}", dpi=220)
    plt.close(fig)
    fpr, tpr, _ = roc_curve(y, probability)
    precision, recall, _ = precision_recall_curve(y, probability)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.4))
    axes[0].plot(fpr, tpr, label=f"ROC-AUC = {auc:.4f}")
    axes[0].plot([0, 1], [0, 1], "--", color="gray", label="Random ranking")
    axes[0].set(xlabel="False positive rate", ylabel="True positive rate", title="ROC curve")
    axes[1].step(recall, precision, where="post", label=f"Average precision = {ap:.4f}")
    axes[1].axhline(y.mean(), linestyle="--", color="gray", label=f"Default prevalence = {y.mean():.4f}")
    axes[1].set(xlabel="Recall", ylabel="Precision", title="Precision-recall curve")
    for ax in axes:
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1.02)
        ax.legend(fontsize=8)
        ax.grid(alpha=0.2)
    fig.suptitle("Random Forest: test-set ranking performance")
    fig.tight_layout()
    for extension in ["png", "pdf"]:
        fig.savefig(FIGURES / f"test_roc_pr.{extension}", dpi=220)
    plt.close(fig)

    checks = {
        "model_and_selection_files_unchanged": all(digest(OUT / name) == value for name, value in before.items()),
        "test_rows_covered": len(predictions) == len(y),
        "confusion_counts_reconcile": all(row["TN"] + row["FP"] + row["FN"] + row["TP"] == len(y) for row in rows),
        "positive_counts_reconcile": all(row["TP"] + row["FN"] == int(y.sum()) for row in rows),
        "saved_predictions_match": np.allclose(pd.read_csv(OUT / "predictions_test.csv")["probability_default"], probability),
    }
    assert all(checks.values()), checks
    report = {
        "model_name": config["model_name"], "model_sha256": digest(model_path),
        "selected_threshold": threshold, "threshold_selection": threshold_config["selection_rule"],
        "n_test": len(y), "n_default": int(y.sum()), "test_prevalence": float(y.mean()),
        "test_data_sha256": {name: digest(DATA / name) for name in ["X_test.csv", "y_test.csv"]},
        "training_or_tuning_performed": False,
        "versions": {"python": platform.python_version(), "sklearn": sklearn.__version__, "pandas": pd.__version__, "numpy": np.__version__},
        "checks": checks,
    }
    (OUT / "test_evaluation_manifest.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(result.round(4).to_string(index=False))
    print("\nChecks:", checks)


if __name__ == "__main__":
    main()
