"""Check the saved model before TreeSHAP. Does not fit or tune anything."""
from pathlib import Path
import hashlib
import json
import platform
import sys

import joblib
import numpy as np
import pandas as pd
import shap
import sklearn


def main():
    base = Path(__file__).resolve().parent
    modeling = base / "modeling"
    output = base / "treeshap"
    model_path = modeling / "selected_rf.joblib"
    config = json.loads((modeling / "selected_rf_config.json").read_text(encoding="utf-8"))
    threshold = json.loads((modeling / "selected_threshold.json").read_text(encoding="utf-8"))
    digest = hashlib.sha256(model_path.read_bytes()).hexdigest()
    assert digest == threshold["model_sha256"], (
        "Model berbeda dari model saat threshold dipilih. Jangan lanjut TreeSHAP sebelum diperiksa."
    )
    model = joblib.load(model_path)
    X = pd.read_csv(base / "processed" / "encoded" / "X_test.csv")
    reference = pd.read_csv(modeling / "predictions_test.csv")
    assert list(X.columns) == config["feature_order"] == list(model.feature_names_in_)
    assert X.shape == (5998, 89)
    assert len(reference) == len(X)
    assert np.array_equal(reference["test_row_index"].to_numpy(), np.arange(len(X)))
    positive_index = list(model.classes_).index(1)
    prediction = model.predict_proba(X)[:, positive_index]
    difference = np.abs(prediction - reference["probability_default"].to_numpy())
    assert np.isfinite(prediction).all()
    assert np.allclose(prediction, reference["probability_default"], rtol=1e-7, atol=1e-9), (
        "Prediksi tidak cocok dengan hasil Irfan. Periksa model, data, dan versi lingkungan."
    )
    report = {
        "status": "PASS",
        "python_executable": sys.executable,
        "versions": {
            "python": platform.python_version(), "numpy": np.__version__,
            "pandas": pd.__version__, "scikit_learn": sklearn.__version__,
            "shap": shap.__version__, "joblib": joblib.__version__,
        },
        "model_name": config["model_name"], "model_sha256": digest,
        "n_test": len(X), "n_features": X.shape[1],
        "positive_class_index": positive_index,
        "maximum_prediction_difference": float(difference.max()),
        "prediction_comparison_rtol": 1e-7, "prediction_comparison_atol": 1e-9,
        "model_fitted_or_tuned": False,
        "treeshap_computed": False,
    }
    output.mkdir(exist_ok=True)
    (output / "environment_model_check.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("LULUS: model bisa dibuka.")
    print("LULUS: data test memiliki 5.998 baris dan 89 kolom dalam urutan yang benar.")
    print("LULUS: prediksi sesuai dengan hasil Irfan dalam toleransi numerik.")
    print(f"Selisih maksimum probabilitas: {difference.max():.12g}")
    print("Model:", config["model_name"])
    print("SHAP:", shap.__version__)
    print("Laporan:", output / "environment_model_check.json")
    print("Belum melatih ulang model atau menghitung TreeSHAP.")


if __name__ == "__main__":
    main()
