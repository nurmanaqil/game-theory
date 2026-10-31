from pathlib import Path
import pandas as pd
import json
import joblib

from typing import Any, TypedDict

class RFConfig(TypedDict):
    name: str
    params: dict[str, Any]

from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, average_precision_score,
    confusion_matrix
)

# 1. Baca train dan validation
folder_kredit = Path(__file__).resolve().parent

base = folder_kredit / "processed" / "encoded"

X_train = pd.read_csv(base / "X_train.csv")
y_train = pd.read_csv(base / "y_train.csv").squeeze("columns")

X_val = pd.read_csv(base / "X_validation.csv")
y_val = pd.read_csv(base / "y_validation.csv").squeeze("columns")

assert X_train.columns.equals(X_val.columns)
assert len(X_train) == len(y_train)
assert len(X_val) == len(y_val)

# 2. Siapkan dua model pembanding
models = {
    "Majority baseline": DummyClassifier(strategy="most_frequent"),
    "Random Forest awal": RandomForestClassifier(
        n_estimators=300,
        random_state=42,
        n_jobs=2
    )
}

# 3. Latih pada train, evaluasi pada validation
results = []

for name, model in models.items():
    model.fit(X_train, y_train)

    positive_index = list(model.classes_).index(1)
    probability = model.predict_proba(X_val)[:, positive_index]
    prediction = (probability >= 0.5).astype(int)

    results.append({
        "Model": name,
        "Accuracy": accuracy_score(y_val, prediction),
        "Precision": precision_score(y_val, prediction, zero_division=0),
        "Recall": recall_score(y_val, prediction, zero_division=0),
        "F1": f1_score(y_val, prediction, zero_division=0),
        "ROC_AUC": roc_auc_score(y_val, probability),
        "Average_precision": average_precision_score(y_val, probability)
    })

    print(f"\n{name} — confusion matrix")
    print(confusion_matrix(y_val, prediction, labels=[0, 1]))

results_df = pd.DataFrame(results)
print("\nHasil validation:")
print(results_df.round(4).to_string(index=False))

# 4. Simpan tabel hasil awal
output = folder_kredit / "modeling"
output.mkdir(parents=True, exist_ok=True)
results_df.to_csv(output / "baseline_validation.csv", index=False)

# Empat konfigurasi tambahan untuk dibandingkan dengan baseline
configs: list[RFConfig] = [
    {
        "name": "RF_leaf5",
        "params": {"min_samples_leaf": 5}
    },
    {
        "name": "RF_depth12_leaf5",
        "params": {"max_depth": 12, "min_samples_leaf": 5}
    },
    {
        "name": "RF_balanced_leaf5",
        "params": {
            "class_weight": "balanced",
            "min_samples_leaf": 5
        }
    },
    {
        "name": "RF_balanced_depth12_leaf5",
        "params": {
            "class_weight": "balanced",
            "max_depth": 12,
            "min_samples_leaf": 5
        }
    }
]

# Baseline yang sudah dilatih juga menjadi kandidat
best_model = models["Random Forest awal"]
best_name = "Random Forest awal"
best_score = average_precision_score(
    y_val,
    best_model.predict_proba(X_val)[:, list(best_model.classes_).index(1)]
)

for config in configs:
    print(f"\nMelatih {config['name']}...")

    model = RandomForestClassifier(
        n_estimators=300,
        random_state=42,
        n_jobs=2,
        **config["params"]
    )
    model.fit(X_train, y_train)

    positive_index = list(model.classes_).index(1)
    probability = model.predict_proba(X_val)[:, positive_index]
    prediction = (probability >= 0.5).astype(int)

    score = average_precision_score(y_val, probability)

    results.append({
        "Model": config["name"],
        "Accuracy": accuracy_score(y_val, prediction),
        "Precision": precision_score(y_val, prediction, zero_division=0),
        "Recall": recall_score(y_val, prediction, zero_division=0),
        "F1": f1_score(y_val, prediction, zero_division=0),
        "ROC_AUC": roc_auc_score(y_val, probability),
        "Average_precision": score
    })

    if score > best_score:
        best_model = model
        best_name = config["name"]
        best_score = score

comparison = pd.DataFrame(results).sort_values(
    "Average_precision", ascending=False
)

comparison.to_csv(output / "comparison_validation.csv", index=False)
joblib.dump(best_model, output / "selected_rf.joblib")

with open(output / "selected_rf_config.json", "w", encoding="utf-8") as f:
    json.dump({
        "model_name": best_name,
        "selection_metric": "validation_average_precision",
        "validation_average_precision": best_score,
        "parameters": best_model.get_params(),
        "feature_order": X_train.columns.tolist()
    }, f, indent=2)

print("\nPerbandingan validation:")
print(comparison.round(4).to_string(index=False))
print(f"\nModel terpilih: {best_name}")