from pathlib import Path
import hashlib
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import precision_recall_curve, precision_score, recall_score, f1_score, accuracy_score, confusion_matrix

folder = Path(__file__).resolve().parent
data = folder / 'processed' / 'encoded'
output = folder / 'modeling'
model_path = output / 'selected_rf.joblib'
model = joblib.load(model_path)
X_val = pd.read_csv(data / 'X_validation.csv')
y_val = pd.read_csv(data / 'y_validation.csv').squeeze('columns')
assert list(X_val.columns) == list(model.feature_names_in_)
assert len(X_val) == len(y_val)
positive_index = list(model.classes_).index(1)
probability = model.predict_proba(X_val)[:, positive_index]
precision, recall, thresholds = precision_recall_curve(y_val, probability)
precision, recall = precision[:-1], recall[:-1]
f1 = np.divide(2 * precision * recall, precision + recall, out=np.zeros_like(precision), where=(precision + recall) != 0)
best_index = np.flatnonzero(f1 == f1.max())[-1]
best_threshold = float(thresholds[best_index])
rows = []
for name, threshold in [('Threshold awal', 0.5), ('Threshold pilihan validation', best_threshold)]:
    prediction = (probability >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_val, prediction, labels=[0, 1]).ravel()
    rows.append({'Setting': name, 'Threshold': threshold, 'Accuracy': accuracy_score(y_val, prediction), 'Precision': precision_score(y_val, prediction, zero_division=0), 'Recall': recall_score(y_val, prediction, zero_division=0), 'F1': f1_score(y_val, prediction, zero_division=0), 'TN': int(tn), 'FP': int(fp), 'FN': int(fn), 'TP': int(tp)})
comparison = pd.DataFrame(rows)
comparison.to_csv(output / 'threshold_comparison_validation.csv', index=False)
pd.DataFrame({'Threshold': thresholds, 'Precision': precision, 'Recall': recall, 'F1': f1}).to_csv(output / 'threshold_search_validation.csv', index=False)
with (output / 'selected_threshold.json').open('w', encoding='utf-8') as f:
    json.dump({'threshold': best_threshold, 'selection_rule': 'maximize validation F1 for class 1', 'tie_break': 'higher threshold', 'validation_f1': float(f1[best_index]), 'model_file': model_path.name, 'model_sha256': hashlib.sha256(model_path.read_bytes()).hexdigest(), 'n_validation': len(y_val)}, f, indent=2)
pd.DataFrame({'y_true': y_val.to_numpy(), 'probability_default': probability}).to_csv(output / 'predictions_validation.csv', index=False)
assert sum(comparison.loc[1, ['TN', 'FP', 'FN', 'TP']]) == len(y_val)
assert np.isclose(comparison.loc[1, 'F1'], f1[best_index])
print('\nPerbandingan threshold validation:')
print(comparison.round(4).to_string(index=False))
print('\nSaved results to:', output)
