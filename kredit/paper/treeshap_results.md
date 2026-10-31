# TreeSHAP Evaluation and Attribution Results

## A. Paired Explanation Design

The selected Random Forest was explained using the interventional and tree-path-dependent modes of TreeSHAP. Both modes used the same fitted forest, the same encoded feature order, and the same evaluation observations. No model fitting or predictive tuning was performed during attribution analysis. A simple random sample of 1,000 test observations was selected without replacement using NumPy default_rng with seed 20261022. Sampling did not use outcomes, prediction scores, or observed explanation differences. The initial interventional background contained 100 randomly selected training observations, sampled without replacement with seed 20261021.

The explanations targeted the model's probability for default, coded as class 1. The implementation used SHAP 0.54.1, scikit-learn 1.7.2, and model_output='raw' for both modes. For this scikit-learn RandomForestClassifier, the raw tree outputs are class probabilities; this was verified by comparing the reconstructed outputs against predict_proba. The tree-path-dependent mode used training-path information stored in the fitted model, without an externally supplied background. It was not treated as an exact general-purpose conditional SHAP estimator. Calculations used approximate=False. Implementation settings followed the TreeExplainer documentation [14].

A 20-observation technical pilot preceded the main experiment. The pilot was used to check implementation, not as independent confirmatory evidence. For the main sample, the reconstruction equation was checked for both output classes: the mode-specific baseline plus the sum of all 89 encoded-feature attributions had to equal the predicted class probability within an absolute tolerance of 1e-6. Maximum reconstruction errors were 2.69e-8 for the initial interventional explanation and 3.94e-15 for the tree-path-dependent explanation.

## B. Comparison Measures

The primary analysis focused on BILL_AMT1-BILL_AMT6. Global importance within this set was defined as the mean absolute SHAP value across the 1,000 observations. Global rankings were compared using Spearman correlation and Kendall tau-b. These rankings concern only the six billing features, not all predictors.

For each observation, the top billing feature was the feature with the largest absolute attribution. Observations with tied maxima within an absolute tolerance of 1e-12 in either mode were excluded from the top-feature agreement denominator. No such ties occurred. Paired attribution differences were computed as interventional minus tree-path-dependent values and summarized by their signed and absolute magnitudes.

The signed attributions of the six billing features were also summed for each observation. This sum is an aggregate of individual-feature attributions; it is not asserted to be the Shapley value of a new game with the six features merged into one player. Magnitudes reported in probability percentage points equal SHAP values multiplied by 100.

## C. Main Attribution Results

**Table C. Attribution magnitudes and rankings within the six billing features, using the initial background. Magnitudes and paired differences are in probability percentage points.**

| Feature | Mean absolute SHAP: interventional | Mean absolute SHAP: path-dependent | Mean absolute paired difference | Rank: interventional | Rank: path-dependent |
|---|---:|---:|---:|---:|---:|
| BILL_AMT1 | 0.4571 | 0.4164 | 0.2287 | 3 | 1 |
| BILL_AMT2 | 0.4640 | 0.3184 | 0.2532 | 2 | 3 |
| BILL_AMT3 | 0.4711 | 0.3413 | 0.2345 | 1 | 2 |
| BILL_AMT4 | 0.4056 | 0.3147 | 0.1692 | 4 | 4 |
| BILL_AMT5 | 0.3388 | 0.2720 | 0.1445 | 5 | 6 |
| BILL_AMT6 | 0.3370 | 0.2795 | 0.1290 | 6 | 5 |

With the initial background, BILL_AMT3 ranked first under interventional TreeSHAP, while BILL_AMT1 ranked first under tree-path-dependent TreeSHAP. The six-feature rankings had Spearman correlation 0.7714 and Kendall tau-b 0.6000. Ranking changes should be interpreted alongside their magnitudes: the mean absolute interventional attributions of the three highest-ranked billing features were close, ranging from 0.4571 to 0.4711 percentage points.

![Figure C: Mean absolute SHAP values for the six billing features under the initial background. Magnitudes are expressed in probability percentage points.](<../treeshap/main/analysis/figures/billing_mean_absolute_shap.png>)

**Figure C.** Mean absolute SHAP values for the six billing features under the initial background. Magnitudes are expressed in probability percentage points.

At the individual level, the top billing feature agreed for 578 observations (57.8%) and differed for 422 (42.2%). Thus, partial agreement in global rankings did not imply agreement in the leading billing feature for each individual. This disagreement concerns the largest absolute billing attribution; it does not establish that the leading feature among all predictors changed, or that the model's prediction changed.

![Figure D: Counts of individual top billing features under the initial background. Rows indicate interventional features and columns indicate path-dependent features. Diagonal entries indicate agreement; all 1,000 observations had unique maxima.](<../treeshap/main/analysis/figures/top_billing_transition.png>)

**Figure D.** Counts of individual top billing features under the initial background. Rows indicate interventional features and columns indicate path-dependent features. Diagonal entries indicate agreement; all 1,000 observations had unique maxima.

The mean absolute difference between the signed billing-group sums was 1.0415 probability percentage points. The mean sum of the six absolute paired attribution differences was 1.1591 percentage points. Consequently, the observed differences cannot be described solely as a redistribution among billing months with an unchanged group total. The group totals themselves also differed.

![Figure E: Paired signed sums of the six billing attributions under the initial background. Each point represents an observation; the dashed line indicates equal group sums. Units are probability percentage points.](<../treeshap/main/analysis/figures/billing_signed_group_sum.png>)

**Figure E.** Paired signed sums of the six billing attributions under the initial background. Each point represents an observation; the dashed line indicates equal group sums. Units are probability percentage points.

The initial interventional baseline was 0.248518, compared with 0.219025 for the path-dependent mode. These baselines refer to different reference mechanisms. Across all features, differences in total attribution necessarily compensate for the baseline difference because both modes reconstruct the same prediction. Interpretation therefore considers the complete explanation settings, rather than treating every attribution difference as an isolated effect of feature correlation.

## D. Sensitivity to Background Composition

Two additional interventional backgrounds were sampled from training data using seeds 20261023 and 20261024. Each contained 100 observations. The fitted model, 1,000 evaluation observations, calculation settings, and path-dependent explanations remained fixed. All three backgrounds were reported without selecting a preferred background based on the findings. Each additional run passed the additivity check, with maximum class-1 errors below 2.72e-8.

**Table D. Sensitivity to three 100-observation training backgrounds. Rankings and disagreement concern the six billing features only.**

| Background seed | Interventional baseline | Highest-ranked billing feature | Spearman vs. path-dependent | Individual top-feature disagreement |
|---|---:|---|---:|---:|
| 20261021 | 0.248518 | BILL_AMT3 | 0.7714 | 422/1,000 (42.2%) |
| 20261023 | 0.229877 | BILL_AMT1 | 1.0000 | 400/1,000 (40.0%) |
| 20261024 | 0.247681 | BILL_AMT3 | 0.8286 | 365/1,000 (36.5%) |

![Figure F: Sensitivity to three training backgrounds of 100 records each. Left: individual top-billing-feature disagreement with path-dependent TreeSHAP. Right: global six-feature ranking agreement. The model and evaluation sample remain fixed.](<../treeshap/main/analysis/figures/background_sensitivity.png>)

**Figure F.** Sensitivity to three training backgrounds of 100 records each. Left: individual top-billing-feature disagreement with path-dependent TreeSHAP. Right: global six-feature ranking agreement. The model and evaluation sample remain fixed.

Individual disagreement remained present for all three sampled backgrounds, ranging from 36.5% to 42.2%. However, the identity of the globally highest-ranked billing feature was sensitive to background composition. For seed 20261023, the complete global billing ranking matched the path-dependent ranking (Spearman correlation 1.0000), while individual top billing features still differed for 40.0% of observations. This provides a direct example of identical global orderings coexisting with different individual explanations.

## E. Interpretation and Limitations

For this fitted model and evaluation sample, explanatory conclusions depended on both the selected TreeSHAP mode and the interventional reference sample. The results support reporting individual-level agreement alongside global rankings and explicitly documenting background selection. They do not establish that one mode is more accurate, that correlation causally generated the observed differences, or that any billing feature causes default. The modes implement different reference assumptions for allocating contributions.

The study uses one dataset, one model-training seed, one fixed evaluation sample, and three backgrounds of equal size. It does not evaluate sensitivity to model retraining, background size, or alternative data partitions. The percentages are descriptive results for the sampled observations and settings, without a population-level significance claim. The six billing features are analyzed in their original numerical columns; a comprehensive ranking of all original predictors is outside the reported six-feature comparison.

## Implementation Reference

[14] SHAP developers, "shap.TreeExplainer," *SHAP documentation*. Available: [TreeExplainer API documentation](https://shap.readthedocs.io/en/stable/generated/shap.TreeExplainer.html). Accessed: October 21, 2026.
