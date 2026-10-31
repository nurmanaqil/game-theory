"""Paired descriptive analysis of the fixed TreeSHAP sample. No model fitting."""
from pathlib import Path
import json

import numpy as np
import pandas as pd
from scipy.stats import spearmanr, kendalltau
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent
BILLS = [f"BILL_AMT{i}" for i in range(1, 7)]


def main():
    source = BASE / "treeshap" / "main"
    out = source / "analysis"
    figures = out / "figures"
    figures.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((source / "main_manifest.json").read_text(encoding="utf-8"))
    assert all(r["additivity_passed"] for r in manifest["results"])
    with np.load(source / "shap_interventional.npz", allow_pickle=False) as a:
        phi_a, names, indices = a["values"], a["feature_names"], a["test_row_indices"]
    with np.load(source / "shap_tree_path_dependent.npz", allow_pickle=False) as b:
        phi_b = b["values"]
        assert np.array_equal(names, b["feature_names"])
        assert np.array_equal(indices, b["test_row_indices"])
    assert phi_a.shape == phi_b.shape == (1000, 89)
    positions = [list(names).index(name) for name in BILLS]
    a, b = phi_a[:, positions], phi_b[:, positions]
    absolute_a, absolute_b = np.abs(a), np.abs(b)
    delta = a - b
    summary = pd.DataFrame({
        "feature": BILLS,
        "mean_abs_shap_interventional": absolute_a.mean(axis=0),
        "mean_abs_shap_tree_path_dependent": absolute_b.mean(axis=0),
        "mean_signed_difference_interventional_minus_path": delta.mean(axis=0),
        "mean_abs_paired_difference": np.abs(delta).mean(axis=0),
        "median_abs_paired_difference": np.median(np.abs(delta), axis=0),
        "p95_abs_paired_difference": np.quantile(np.abs(delta), .95, axis=0),
    })
    for column, label in [("mean_abs_shap_interventional", "rank_interventional"), ("mean_abs_shap_tree_path_dependent", "rank_tree_path_dependent")]:
        summary[label] = summary[column].rank(ascending=False, method="average")
    summary.to_csv(out / "billing_comparison.csv", index=False)
    rho = float(spearmanr(summary["mean_abs_shap_interventional"], summary["mean_abs_shap_tree_path_dependent"]).statistic)
    tau = float(kendalltau(summary["mean_abs_shap_interventional"], summary["mean_abs_shap_tree_path_dependent"]).statistic)

    # A unique maximum is required for top-feature agreement. Near ties are excluded.
    tops_a = np.isclose(absolute_a, absolute_a.max(axis=1, keepdims=True), rtol=0, atol=1e-12)
    tops_b = np.isclose(absolute_b, absolute_b.max(axis=1, keepdims=True), rtol=0, atol=1e-12)
    unique = (tops_a.sum(axis=1) == 1) & (tops_b.sum(axis=1) == 1)
    winner_a, winner_b = absolute_a.argmax(axis=1), absolute_b.argmax(axis=1)
    agreement = unique & (winner_a == winner_b)
    n_unique = int(unique.sum())
    group_a, group_b = a.sum(axis=1), b.sum(axis=1)
    sample = pd.read_csv(source / "evaluation_membership.csv")
    assert np.array_equal(sample["split_row_index"].to_numpy(), indices)
    local = sample.copy()
    local["unique_top_both_modes"] = unique
    local["top_billing_interventional"] = [BILLS[i] if ok else "TIE" for i, ok in zip(winner_a, tops_a.sum(axis=1) == 1)]
    local["top_billing_tree_path_dependent"] = [BILLS[i] if ok else "TIE" for i, ok in zip(winner_b, tops_b.sum(axis=1) == 1)]
    local["top_agreement"] = pd.array([bool(x) if valid else pd.NA for x, valid in zip(agreement, unique)], dtype="boolean")
    local["billing_signed_sum_interventional"] = group_a
    local["billing_signed_sum_tree_path_dependent"] = group_b
    local["signed_group_difference"] = group_a - group_b
    local["sum_abs_individual_differences"] = np.abs(delta).sum(axis=1)
    for i, name in enumerate(BILLS):
        local[f"{name}_interventional"] = a[:, i]
        local[f"{name}_tree_path_dependent"] = b[:, i]
    local.to_csv(out / "per_customer_billing_comparison.csv", index=False)
    transition = pd.crosstab(local.loc[unique, "top_billing_interventional"], local.loc[unique, "top_billing_tree_path_dependent"]).reindex(index=BILLS, columns=BILLS, fill_value=0)
    transition.to_csv(out / "top_billing_transition_counts.csv")
    pd.DataFrame({
        "feature": BILLS,
        "interventional_unique_top_count": [int(((winner_a == i) & (tops_a.sum(axis=1) == 1)).sum()) for i in range(6)],
        "tree_path_dependent_unique_top_count": [int(((winner_b == i) & (tops_b.sum(axis=1) == 1)).sum()) for i in range(6)],
    }).to_csv(out / "top_billing_counts.csv", index=False)
    report = {
        "scope": "1000 fixed test observations, 6 billing features, one fitted model and one background sample",
        "n_observations": len(a), "n_unique_top_both_modes": n_unique,
        "n_tied_in_either_mode": int((~unique).sum()),
        "n_top_agreement": int(agreement.sum()),
        "n_top_disagreement": int((unique & ~agreement).sum()),
        "top_agreement_rate_among_unique": float(agreement.sum() / n_unique) if n_unique else None,
        "top_tie_rule": "exclude observations with more than one maximum abs(SHAP) within absolute tolerance 1e-12 in either mode",
        "global_ranking_scope": "six billing features ranked by mean absolute SHAP; average ranks for ties",
        "spearman_global_billing": rho, "kendall_tau_b_global_billing": tau,
        "mean_abs_signed_group_difference": float(np.abs(group_a - group_b).mean()),
        "mean_sum_abs_individual_differences": float(np.abs(delta).sum(axis=1).mean()),
        "group_note": "sum of signed individual attributions, not a new grouped-player Shapley game",
        "causal_claim": False,
        "limitations": ["single model seed", "single 100-row interventional background", "sample of test observations", "mode-specific baselines differ", "no statistical significance or causal effect established"],
    }
    (out / "analysis_summary.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    def save(fig, filename):
        fig.tight_layout()
        for ext in ["png", "pdf"]:
            fig.savefig(figures / f"{filename}.{ext}", dpi=220)
        plt.close(fig)

    x = np.arange(6)
    fig, ax = plt.subplots(figsize=(9, 4.8))
    ax.bar(x - .19, absolute_a.mean(axis=0) * 100, .38, label="Interventional")
    ax.bar(x + .19, absolute_b.mean(axis=0) * 100, .38, label="Tree path dependent")
    ax.set(xticks=x, xticklabels=BILLS, ylabel="Mean |SHAP| (probability percentage points)", title="Billing attribution magnitudes: 1,000 test observations")
    ax.legend(); ax.grid(axis="y", alpha=.2)
    save(fig, "billing_mean_absolute_shap")

    fig, ax = plt.subplots(figsize=(7, 6))
    im = ax.imshow(transition.to_numpy(), cmap="Blues")
    for i in range(6):
        for j in range(6):
            count = int(transition.iloc[i, j])
            ax.text(j, i, str(count), ha="center", va="center", color="white" if count > transition.to_numpy().max() / 2 else "black")
    ax.set(xticks=x, yticks=x, xticklabels=BILLS, yticklabels=BILLS, xlabel="Top billing feature: tree path dependent", ylabel="Top billing feature: interventional", title=f"Top billing feature comparison\n{n_unique} observations without ties")
    plt.setp(ax.get_xticklabels(), rotation=35, ha="right")
    fig.colorbar(im, ax=ax, label="Number of observations")
    save(fig, "top_billing_transition")

    fig, ax = plt.subplots(figsize=(6.6, 5.6))
    ax.scatter(group_a * 100, group_b * 100, s=12, alpha=.4)
    limits = [float(min(group_a.min(), group_b.min()) * 100), float(max(group_a.max(), group_b.max()) * 100)]
    ax.plot(limits, limits, "--", color="gray", label="Equal signed sums")
    ax.set(xlabel="Interventional: signed sum (percentage points)", ylabel="Tree path dependent: signed sum (percentage points)", title="Combined attribution of the six billing features")
    ax.legend(); ax.grid(alpha=.2)
    save(fig, "billing_signed_group_sum")
    print("\nPerbandingan enam fitur tagihan:")
    print(summary.round(6).to_string(index=False))
    print(f"\nRanking global: Spearman={rho:.4f}; Kendall tau-b={tau:.4f}")
    print(f"Fitur tagihan teratas sama: {agreement.sum()} dari {n_unique} nasabah tanpa tie.")
    print(f"Fitur tagihan teratas berbeda: {(unique & ~agreement).sum()}; dikecualikan karena tie: {(~unique).sum()}.")
    print("\nHasil:", out)
    print("Interpretasi: deskriptif untuk enam fitur tagihan; bukan bukti kausal atau keunggulan salah satu mode.")


if __name__ == "__main__":
    main()
