# Mode Sensitivity of TreeSHAP Attributions across Tree-Based Credit Default Models: Global Rankings and Individual Agreement

Research draft for author review — 23 October 2026

## Abstract

Feature-attribution conclusions depend on how an explanation method represents unavailable features. This study examines differences between interventional and tree-path-dependent TreeSHAP in credit default classification. Random Forest, Extra Trees, Gradient Boosting, and XGBoost are trained on the UCI Default of Credit Card Clients dataset using the same group-aware training, validation, and test partition. Three configurations per family are compared using validation average precision. Explanation analysis uses 1,000 fixed test observations and focuses on six correlated billing variables. Agreement is assessed through global importance rankings, the identity of the largest individual billing attribution, winner margins, and paired attribution magnitudes. Background sampling and training randomness are examined separately using three backgrounds and three training seeds. For the primary seed and background, individual leading-feature disagreement ranges from 14.9% to 42.6%. Gradient Boosting and XGBoost retain identical global billing rankings across modes despite individual disagreement rates of 21.0% and 14.9%. Requiring both leading-feature margins to exceed 0.05 reduces disagreement, but does not eliminate it; rates range from 7.85% to 34.34% on the resulting subsets. These findings show that global ranking agreement can conceal individual allocation differences and that disagreement counts require accompanying magnitude and margin analysis. The study is exploratory, uses a previously examined test partition, and does not identify a causal effect of feature correlation or establish one explanation mode as universally preferable.

**Keywords:** TreeSHAP; feature attribution; credit default; correlated features; explanation sensitivity; tree ensembles.

## 1. Introduction

Credit default models estimate the risk that a borrower will fail to meet a future payment obligation. Predictive performance is necessary for such models, but examining which variables contribute to a prediction is also useful for model analysis. SHAP expresses an individual model output as a reference value and feature contributions [1]. TreeSHAP makes this calculation practical for tree-based models [2]. However, choosing an efficient algorithm does not remove the need to define the reference game underlying the explanation.

This distinction matters when predictors contain overlapping information. Monthly credit-card bills describe related financial histories rather than independent measurements. A model can use several billing variables to represent similar signals. Interventional and tree-path-dependent TreeSHAP operationalize missing-feature expectations differently, so their allocations can differ even when both reconstruct the same fitted prediction. More generally, alternative Shapley formulations need not answer the same question [3].

Previous work has already investigated interventional and path-dependent SHAP in credit-risk settings [4]. Recent research has also examined the stability of explanations across repeated XGBoost training runs on the Taiwan credit-card dataset [5]. Therefore, comparing two TreeSHAP modes or using this dataset alone is not treated as a new methodological contribution. The present study provides a focused empirical analysis across four tree-model families, with particular attention to the distinction between global rankings and individual leading features. Winner-margin filtering and attribution-magnitude analysis help determine whether a change in the leading feature corresponds to a substantial allocation difference.

The study addresses three research questions:

1. **RQ1:** How do the two modes differ in global importance rankings and individual leading billing features within each fitted model?
2. **RQ2:** To what extent do disagreements remain after separating observations with near-tied leading features, and how large are the paired attribution differences?
3. **RQ3:** How sensitive are these patterns to background sampling and limited changes in training seed?

The contribution is an empirical comparison under a shared data and evaluation protocol. Comparisons across model families are descriptive because each family learns a different function. The analysis does not establish that correlation causes the observed differences, and it does not rank explanation modes against a known ground truth.

## 2. Background

### 2.1. Shapley attribution and TreeSHAP

For an input with feature set N of size M, the Shapley attribution of feature j is

$$
\phi_j = \sum_{S\subseteq N\setminus\{j\}}
\frac{|S|!(M-|S|-1)!}{M!}
\left[v(S\cup\{j\})-v(S)\right].
$$

Here, v(S) defines the model output assigned to a coalition of observed features. Shapley's allocation rule averages a feature's marginal contribution across coalitions [7]. SHAP applies this framework to model explanations [1]. For an additive explanation on the selected output scale,

$$
f(x)=\phi_0+\sum_{j=1}^{M}\phi_j(x).
$$

TreeSHAP exploits tree structure to compute the relevant attributions efficiently [2]. It does not train a separate predictive model for every feature coalition. The interpretation of its output still depends on the value function and reference assumptions.

### 2.2. Two missing-feature treatments

Interventional TreeSHAP uses a supplied background dataset. Missing feature coordinates are replaced using background observations while the observed coordinates are fixed. This operation can break dependencies between observed and replaced features. It does not imply that all features inside a background row are independently sampled. The background also determines the reference output [2,11].

Tree-path-dependent TreeSHAP uses the tree paths and stored training-sample coverage to weight branches when a feature is unavailable. It does not require a separately supplied background sample [11]. This construction should not be described as an exact estimator of the full observational conditional distribution for arbitrary dependent predictors. Consequently, the two modes can define different explanation games and different baselines while both satisfying additive reconstruction.

### 2.3. Related research and positioning

García-Céspedes et al. examine interventional and path-dependent SHAP in credit-risk applications [4]. Their work establishes that this distinction is already relevant to the domain; the present study does not claim to introduce it. Lin and Wang examine explanation stability under repeated XGBoost training on the Taiwan dataset [5]. Their larger training-seed design addresses a stability dimension for which the three seeds here provide only a limited descriptive check. Work on dependent inputs in energy-system explanations further illustrates that attribution assumptions require attention beyond a single application domain [6].

The present analysis combines four model families, paired mode comparisons, explicit output-scale checks, and an examination of leading-feature margins and attribution magnitudes. Its scientific value rests on the observed relationships among these measurements, rather than the number of algorithms alone. A claim of priority over all previous studies would require a broader full-text literature audit.

## 3. Materials and methods

### 3.1. Dataset and partition

The UCI Default of Credit Card Clients dataset contains 30,000 customers, 23 predictors, and a binary next-month default target [8]. The records describe Taiwan credit-card customers, including demographic information and repayment, billing, and payment histories from April to September 2005. Default is the positive class and occurs in 6,636 records (22.12%). Customer identifiers are excluded from the predictors.

The preprocessing retains all observations. EDUCATION values 0, 5, and 6 are mapped to an unknown category, while value 4 retains its existing meaning. MARRIAGE value 0 is retained as unknown. Repayment-status values −2, −1, and 0 remain distinct. Negative bills and zero payments are preserved. There are no missing or nonfinite input values requiring imputation. No scaling, clipping, class resampling, or class weighting is applied.

After deterministic category mapping, records are grouped by their complete predictor profiles. The 29,944 distinct profiles include 52 repeated-profile groups containing 108 records. Conflicting target labels within identical profiles are retained. Grouping prevents identical mapped predictor profiles from appearing in different partitions.

A shuffled, stratified five-fold group splitter with seed 20261020 assigns fold 0 to testing, fold 1 to validation, and the other folds to training. This produces one fixed partition; the study does not report five-fold cross-validation averages.

**Table 1. Fixed group-aware data partition.**

| Partition | Records | Non-default | Default | Default prevalence |
| --- | ---: | ---: | ---: | ---: |
| Training | 18,005 | 14,054 | 3,951 | 21.94% |
| Validation | 5,997 | 4,631 | 1,366 | 22.78% |
| Test | 5,998 | 4,679 | 1,319 | 21.99% |

Nine categorical predictors are one-hot encoded using an encoder fitted exclusively on training data. Together with 14 numerical predictors, they yield 89 model input columns. The encoder ignores unknown categories at inference; no unseen categories occur in the held-out partitions. All four models use this same representation.

The six BILL_AMT variables are the primary analysis group because they represent successive billing periods with substantial dependence. Their training-set pairwise Pearson correlations range from 0.7963 to 0.9501, with mean 0.8816. Their Spearman correlations range from 0.7324 to 0.9091. The six PAY_AMT variables form a secondary comparison group: Pearson correlations range from 0.1149 to 0.3277, while Spearman correlations range from 0.4566 to 0.5498. This comparison describes groups with different dependence patterns; it does not isolate correlation experimentally.

![Training-set billing correlations](figures/billing_correlation_train.png)

**Figure 1.** Training-set correlation structure of the six billing variables. Correlations are computed before interpreting held-out attribution differences.

### 3.2. Predictive models and selection

Random Forest combines trees trained with bootstrap sampling and feature subsampling. Extra Trees introduces additional randomization in split thresholds. Gradient Boosting builds trees sequentially to improve the current model. XGBoost uses regularized gradient boosting with its own tree-construction and sampling controls [9,10]. These differences motivate including all four families in the attribution analysis.

Three candidate configurations per family are evaluated at training seed 42. Random Forest and Extra Trees vary maximum depth over 8, 12, and unrestricted. Both use 300 trees, minimum leaf size 5, and square-root feature sampling; bootstrap sampling is enabled only for Random Forest. Gradient Boosting varies depth over 2, 3, and 4, using 200 stages, learning rate 0.05, minimum leaf size 5, and subsample 1. XGBoost varies depth over 2, 3, and 4, using 300 estimators, learning rate 0.05, row and column sampling fractions 0.8, L2 regularization 1, histogram tree construction, and a binary-logistic objective. Its native minimum-child settings remain at their defaults. Equal candidate counts do not imply equal computational budgets or exhaustive tuning.

The configuration with highest validation average precision (AP) is selected within each family; an exact tie retains the first candidate. Selected configurations are frozen before retraining at seeds 17 and 73. For each fitted model, the decision threshold maximizes validation F1, with the higher threshold selected if maxima tie. Models are not refitted on combined training and validation data.

**Table 2. Selected model configurations.**

| Model | Trees or stages | Learning rate | Selected maximum depth | Sampling |
| --- | ---: | ---: | --- | --- |
| Random Forest | 300 | — | 12 | Bootstrap; square-root feature sampling |
| Extra Trees | 300 | — | Unrestricted | No bootstrap; square-root feature sampling |
| Gradient Boosting | 200 | 0.05 | 3 | All training rows per stage |
| XGBoost | 300 | 0.05 | 3 | Row fraction 0.8; column fraction 0.8 |

AP is the selection metric because the positive class is less frequent and ranking default risk is central to the task. AP is computed as a precision-recall summary and is not relabeled as trapezoidal PR-AUC. ROC-AUC, precision, recall, F1, and Brier score provide complementary descriptions. Brier score measures squared probability error and is not treated as a pure calibration statistic. No cost-optimal lending threshold is claimed.

The test partition had already been examined during the original project. Although this revision selects configurations and thresholds using validation data, its test results are exploratory rather than a new, untouched confirmatory evaluation.

### 3.3. Paired TreeSHAP calculations

The explanation sample contains 1,000 fixed test observations selected without replacement using seed 20261022. Each interventional background contains 100 training observations. Background seeds are 20261021, 20261023, and 20261024. Training seed 42 is analyzed with all three backgrounds; seeds 17 and 73 use only background 20261021. This design varies background sampling and training randomness separately and is not a complete factorial experiment.

Each paired comparison uses the same fitted model, observations, feature order, default-class output, and raw output scale. The approximation option is disabled. For Random Forest and Extra Trees, the raw output is default probability. For Gradient Boosting and XGBoost, it is the log-odds margin. Reconstructions are checked against native probability outputs or native margins as appropriate. Individual log-odds attributions are not passed separately through a sigmoid to obtain probability contributions.

A 20-observation implementation pilot precedes each fitted model's main calculation. Absolute additive-reconstruction tolerances are 10⁻⁶ for the scikit-learn models and 10⁻⁵ for XGBoost. The latter tolerance is a documented amendment after a 300-tree pilot showed approximately 1–2 × 10⁻⁶ discrepancies against native float32 margins. Two historical Random Forest background arrays are reused only after reproducing model parameters and held-out predictions and verifying array provenance. The final collection contains 32 explanation arrays.

### 3.4. Attribution comparisons

For explanation mode m, global importance of feature j is

$$
I_j^{(m)}=\frac{1}{n}\sum_{i=1}^{n}|\phi_{ij}^{(m)}|.
$$

Spearman correlation and Kendall tau-b compare rankings of the six billing importances. They summarize these six-feature vectors descriptively and are not used as population significance tests.

The individual leading billing feature maximizes absolute attribution within the six-feature group. If either mode has a tied maximum within absolute tolerance 10⁻¹², that observation is excluded from the corresponding agreement denominator. The disagreement rate is the fraction of remaining observations whose leading-feature identities differ.

For the largest and second-largest absolute attributions a₁ and a₂, define the winner margin

$$
m=\frac{a_1-a_2}{a_1+a_2},
$$

with zero assigned when the denominator is at most 10⁻¹². Additional comparisons require both modes to have margins exceeding 0.01, 0.05, or 0.10. These thresholds are specified in the analysis protocol. They change the evaluated population, so subset sizes accompany their disagreement rates.

For feature group G, paired allocation differences are measured as

$$
D_{L1,G}=\frac{1}{n}\sum_i\sum_{j\in G}
|\phi_{ij}^{(int)}-\phi_{ij}^{(path)}|,
$$

and the absolute difference in the signed group total as

$$
D_{sum,G}=\frac{1}{n}\sum_i
\left|\sum_{j\in G}\phi_{ij}^{(int)}-
\sum_{j\in G}\phi_{ij}^{(path)}\right|.
$$

The first measure includes reallocations among group members; the second can cancel such reallocations. Neither is a prediction-error measure. Summing existing feature attributions does not create a new Shapley game in which the group is a single player. Likewise, source-level summaries of categorical predictors sum signed indicator contributions before taking absolute values; they do not redefine the original encoded-feature game.

## 4. Results

### 4.1. Predictive performance

Table 3 reports the primary training seed. XGBoost has the highest validation AP (0.5805) and is therefore the designated primary predictive model. Random Forest has slightly higher test AP (0.5481 versus 0.5472), which does not trigger model reselection. All four models remain in the explanation comparison. These small score differences are descriptive and are not evidence of statistically established superiority.

**Table 3. Predictive performance at training seed 42. Threshold-based test metrics use validation-selected thresholds.**

| Model | Validation AP | Test AP | Test ROC-AUC | Precision | Recall | F1 | Brier |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Random Forest | 0.5731 | 0.5481 | 0.7741 | 0.4698 | 0.5770 | 0.5179 | 0.1361 |
| Extra Trees | 0.5640 | 0.5387 | 0.7650 | 0.4802 | 0.5527 | 0.5139 | 0.1372 |
| Gradient Boosting | 0.5757 | 0.5441 | 0.7716 | 0.5050 | 0.5345 | 0.5193 | 0.1356 |
| XGBoost | 0.5805 | 0.5472 | 0.7749 | 0.5169 | 0.5444 | 0.5303 | 0.1351 |

![Validation and test average precision](../experiments/revision_v1/figures/predictive_ap.png)

**Figure 2.** Validation and test AP for the four selected models. Validation AP determines selection; test AP is reported for evaluation.

### 4.2. Reconstruction and reference values

All 32 stored explanation arrays pass the specified additive-reconstruction tolerances. The largest observed XGBoost reconstruction error is 4.05 × 10⁻⁶. These checks establish numerical consistency with the selected output, not that either mode is a uniquely correct explanation.

For primary Random Forest, the interventional baseline is 0.2485 and the path-dependent baseline is 0.2190, a difference of approximately 2.95 percentage points. Both reconstruct the same model predictions. Consequently, the total attribution difference also reflects a changed reference level, rather than only a redistribution among billing variables.

### 4.3. Global rankings and individual leading features

Table 4 uses seed 42 and background 20261021. All models have 1,000 eligible observations. Random Forest and Extra Trees have similar leading-feature disagreement rates, at 42.2% and 42.6%. Gradient Boosting and XGBoost have lower rates, at 21.0% and 14.9%, despite perfectly matching global billing rankings between modes. Global agreement therefore does not guarantee individual agreement.

**Table 4. Primary billing-group comparison. Probability differences are expressed in percentage points (pp); boosting differences remain in log-odds units.**

| Model | Disagreement | Global Spearman | Mean L1 difference | Mean group-total difference | Difference units |
| --- | --- | --- | --- | --- | --- |
| Random Forest | 42.2% | 0.7714 | 1.1591 | 1.0415 | pp |
| Extra Trees | 42.6% | 0.7714 | 0.3041 | 0.2614 | pp |
| Gradient Boosting | 21.0% | 1.0000 | 0.0643 | 0.0361 | log-odds |
| XGBoost | 14.9% | 1.0000 | 0.1051 | 0.0558 | log-odds |

![Billing feature importance by explanation mode](../experiments/revision_v1/figures/billing_importance.png)

**Figure 3.** Mean absolute billing attributions for the two modes. B1–B6 denote BILL_AMT1–BILL_AMT6. Forest and boosting panels use their respective output units; their raw magnitudes should not be directly pooled.

Magnitude analysis changes the interpretation of the disagreement counts. Random Forest and Extra Trees have nearly equal disagreement rates, but their mean billing L1 differences are approximately 1.1591 pp and 0.3041 pp. Thus, a similar frequency of changed winners can accompany substantially different allocation changes on a shared probability scale.

### 4.4. Winner margins and attribution magnitudes

Requiring both margins to exceed 0.05 reduces the disagreement rate for every model, but disagreement remains. The retained samples differ across models, so Table 5 compares conditional rates rather than a common-population robustness score.

**Table 5. Leading-feature disagreement before and after requiring both winner margins to exceed 0.05.**

| Model | Full n | Full disagreement | Filtered n | Filtered disagreements | Filtered rate |
| --- | --- | --- | --- | --- | --- |
| Random Forest | 1000 | 42.2% | 664 | 228 | 34.34% |
| Extra Trees | 1000 | 42.6% | 548 | 150 | 27.37% |
| Gradient Boosting | 1000 | 21.0% | 808 | 109 | 13.49% |
| XGBoost | 1000 | 14.9% | 764 | 60 | 7.85% |

![Disagreement conditional on winner margins](../experiments/revision_v1/figures/winner_margin_disagreement.png)

**Figure 4.** Disagreement rates at the specified margin cutoffs. Each cutoff requires both modes to exceed that margin; eligible sample sizes decrease as the cutoff increases.

![Attribution differences grouped by leading-feature agreement](../experiments/revision_v1/figures/difference_magnitude_by_winner.png)

**Figure 5.** Distributions of individual billing L1 differences, separated by whether leading-feature identities agree. Boxes show the interquartile range and median, with whiskers extending to observations within 1.5 interquartile ranges. Outlier markers are hidden for readability; those observations remain in the numerical analysis. Panels retain model-specific output units.

These comparisons show why a changed leading feature alone is insufficient to characterize an explanation difference. A small perturbation can exchange nearly tied ranks, while an unchanged winner can coexist with changes in other contributions. Margin filtering and paired magnitudes describe complementary properties.

### 4.5. Background and training-seed sensitivity

The three backgrounds produce different disagreement rates at the same primary training seed (Table 6). Random Forest ranges from 36.5% to 42.2%, Extra Trees from 38.3% to 42.6%, Gradient Boosting from 19.1% to 21.3%, and XGBoost from 12.1% to 14.9%. The tree-path-dependent explanation remains fixed within each fitted model; background variation changes the interventional comparison.

**Table 6. Billing leading-feature disagreement across background samples at training seed 42; n = 1,000 in each cell.**

| Model | Background 20261021 | Background 20261023 | Background 20261024 |
| --- | --- | --- | --- |
| Random Forest | 42.2% | 40.0% | 36.5% |
| Extra Trees | 42.6% | 40.2% | 38.3% |
| Gradient Boosting | 21.0% | 19.0% | 21.3% |
| XGBoost | 14.9% | 13.7% | 12.1% |

![Background-sample sensitivity](../experiments/revision_v1/figures/background_disagreement.png)

**Figure 6.** Disagreement across three independently sampled training backgrounds of size 100. A common vertical scale supports comparison of rates, but three samples do not establish background convergence.

With the first background fixed, changing training seed gives the rates in Table 7. The broad family pattern persists in these runs. Nevertheless, three seeds are insufficient to estimate population uncertainty or establish general stability. Held-out predictions differ across the three fitted seeds within each family, including Gradient Boosting.

**Table 7. Billing leading-feature disagreement across training seeds with background 20261021; n = 1,000 in each cell.**

| Model | Seed 42 | Seed 17 | Seed 73 |
| --- | --- | --- | --- |
| Random Forest | 42.2% | 46.1% | 42.2% |
| Extra Trees | 42.6% | 41.6% | 41.9% |
| Gradient Boosting | 21.0% | 21.1% | 21.0% |
| XGBoost | 14.9% | 14.9% | 17.1% |

### 4.6. Secondary payment-feature comparison

For the six PAY_AMT features, primary disagreement rates are 13.9% for Random Forest, 19.8% for Extra Trees, 9.0% for Gradient Boosting, and 12.1% for XGBoost. These rates are lower than their corresponding billing rates. However, XGBoost has similar mean L1 differences for billing and payment features, approximately 0.1051 and 0.1067 log-odds units. Fewer winner changes therefore do not necessarily mean smaller allocation differences. Since the groups differ in distribution, predictive relevance, and tree usage as well as correlation, their comparison cannot identify a causal effect of correlation.

## 5. Discussion

The main finding is a separation between aggregate and individual agreement. Gradient Boosting and XGBoost preserve the global ordering of all six billing features while assigning different leading billing features to a substantial subset of customers. A global importance chart alone would miss these differences. For an explanation study, evaluation should therefore specify whether its intended conclusion concerns average importance, individual ranking, or the magnitude of assigned contributions.

Near ties explain part of the observed winner switching. Disagreement decreases when both modes must identify a more distinct winner, but remains between 7.85% and 34.34% in the 0.05-margin subsets. These percentages should not be interpreted as error rates. Neither mode is an externally validated ground truth, and the filtering procedure selects different subsets. The result supports reporting margins alongside winner identities rather than declaring every switched winner a major explanatory failure.

Attribution magnitudes provide a further qualification. The forest comparison shows that similar disagreement counts can coexist with different absolute allocation changes. Conversely, the XGBoost billing/payment comparison shows similar L1 changes despite different winner-switching rates. Ranking and magnitude measurements cannot substitute for one another.

The lower disagreement rates observed for boosting in this design do not establish that boosting explanations are intrinsically more reliable. Different model families learn different functions and use features differently; the raw output scale also differs between forests and boosting. Even an output normalization would not remove these functional differences. The defensible comparison is between modes within a fitted model, followed by a descriptive comparison of the resulting patterns across families.

Background-dependent reference values also matter. Changing a background can change both the interventional baseline and feature allocations. The observed differences therefore concern the complete explanation specification: fitted model, reference distribution, output scale, and missing-feature treatment. Reporting only the explainer name would omit choices needed to reproduce the analysis.

## 6. Limitations and reproducibility

The experiment uses one dataset, one fixed split, a limited configuration search, three training seeds, and three backgrounds of one size. It does not estimate confidence intervals from independent datasets or repeated partitions. The test set was previously examined, so the reported evaluation remains exploratory. The background design does not test larger sizes, convergence, or shifts in portfolio composition. Its partially crossed structure does not estimate interactions between every training seed and background.

Feature correlation is measured rather than manipulated. The study consequently cannot conclude that correlation alone causes mode disagreement. Such a claim would require a controlled dependence experiment or a narrower question with an appropriate identification design. Likewise, no small-tree coalition enumeration or externally defined attribution target is used to establish one mode as correct.

The encoded representation introduces an additional interpretive limitation. Replacing subsets of one-hot indicators can create combinations not present in the original categorical data. Source-level aggregation is useful for reporting but does not retroactively turn the encoded-feature game into a grouped categorical game. No operational lending-policy, fairness, or probability-calibration claim is established by these experiments.

The project retains the raw-data fingerprint, fixed memberships, training-only encoder, candidate scores, selected configurations, model manifests, background indices, predictions, attribution arrays, reconstruction checks, and analysis tables. Final automated verification passes 266 checks covering stored results and their consistency. These checks support computational traceability; they do not remove the design limitations above. Detailed result tables and scripts accompany this draft in the local project.

## 7. Conclusion

Under a shared credit-default protocol, interventional and tree-path-dependent TreeSHAP yield individual leading-billing-feature disagreement rates of 14.9%–42.6% across four tree-model families. Identical global billing rankings in the two boosting models coexist with individual disagreement. Margin filtering reduces but does not eliminate winner switching, while paired magnitudes show that switching frequency alone does not quantify the size of allocation changes.

The findings support reporting global rankings, individual agreement, winner margins, output units, and attribution magnitudes together. They demonstrate sensitivity to explanation specifications within this experiment, without proving a causal role for correlation or a universally superior mode. Further work should examine broader seed and background designs, previously untouched evaluation data, and controlled dependence changes before making stronger general claims.

## References

[1] Lundberg, S. M., and Lee, S.-I. (2017). A Unified Approach to Interpreting Model Predictions. *Advances in Neural Information Processing Systems*, 30. [Publisher record](https://proceedings.neurips.cc/paper/2017/hash/8a20a8621978632d76c43dfd28b67767-Abstract.html).

[2] Lundberg, S. M., et al. (2020). From local explanations to global understanding with explainable AI for trees. *Nature Machine Intelligence*, 2, 56–67. [DOI](https://doi.org/10.1038/s42256-019-0138-9).

[3] Sundararajan, M., and Najmi, A. (2020). The Many Shapley Values for Model Explanation. *Proceedings of Machine Learning Research*, 119, 9269–9278. [Publisher record](https://proceedings.mlr.press/v119/sundararajan20b.html).

[4] García-Céspedes, R., Alias-Carrascosa, F. J., and Moreno, M. (2025). On Machine Learning models explainability in the banking sector: the case of SHAP. *Journal of the Operational Research Society*, 76(12), 2591–2603. [Publisher DOI record](https://doi.org/10.1080/01605682.2025.2485263).

[5] Lin, L., and Wang, Y. (2025). SHAP Stability in Credit Risk Management: A Case Study in Credit Card Default Model. *Risks*, 13(12), 238. [Publisher record](https://doi.org/10.3390/risks13120238).

[6] Nikoltchovska, A., Pütz, S., Götz, M., and Schäfer, B. (2026). Correlations Matter in Explanations for Energy Systems. *KI – Künstliche Intelligenz*, 40, 41–54. [Publisher record](https://doi.org/10.1007/s13218-026-00904-4).

[7] Shapley, L. S. (1953). A Value for n-Person Games. In *Contributions to the Theory of Games II*. Princeton University Press. [DOI](https://doi.org/10.1515/9781400881970-018).

[8] Yeh, I. (2009). Default of Credit Card Clients. *UCI Machine Learning Repository*. [Dataset and DOI](https://doi.org/10.24432/C55S3H).

[9] Scikit-learn developers. Ensemble methods. *Scikit-learn 1.7 documentation*. Accessed 23 October 2026. [Documentation](https://scikit-learn.org/1.7/modules/ensemble.html).

[10] XGBoost developers. XGBoost Parameters. *XGBoost documentation*. Accessed 23 October 2026. [Documentation](https://xgboost.readthedocs.io/en/stable/parameter.html).

[11] SHAP developers. shap.TreeExplainer. *SHAP documentation*. Accessed 23 October 2026. [Documentation](https://shap.readthedocs.io/en/latest/generated/shap.TreeExplainer.html).
