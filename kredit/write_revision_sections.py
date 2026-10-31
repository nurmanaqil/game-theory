# Local manuscript sections to replace the old modeling/results sections after review.
from pathlib import Path
import json
import pandas as pd
B=Path(__file__).resolve().parent;O=B/'experiments/revision_v1'
assert json.loads((O/'analysis_checks.json').read_text())['status']=='PASS'
A=pd.read_csv(O/'attribution_summary.csv');P=pd.read_csv(O/'predictive_metrics.csv');S=pd.read_csv(O/'seed_sensitivity.csv')
names={'random_forest':'Random Forest','extra_trees':'Extra Trees','gradient_boosting':'Gradient Boosting','xgboost':'XGBoost'}
def md(df):
 s='| '+' | '.join(df.columns)+' |\n| '+' | '.join(['---']*len(df.columns))+' |\n'
 return s+'\n'.join('| '+' | '.join('NA' if pd.isna(v) else f'{v:.4f}' if isinstance(v,float) else str(v) for v in r)+' |' for r in df.itertuples(index=False,name=None))+'\n'
perf=pd.read_csv(O/'paper_predictive_table.csv');val=P[(P.seed==42)&(P.split=='validation')&(P.threshold_rule=='validation_f1')];winner=names[val.loc[val.AP.idxmax(),'family']]
q=A[(A.seed==42)&(A.background_seed==20261021)&(A.group=='BILL_AMT')&(A.margin_cutoff==0)]
mi=q.disagreement_rate.min()*100;ma=q.disagreement_rate.max()*100
text=f'''# Mode Sensitivity of TreeSHAP Attributions across Tree-Based Credit Default Models

## Status of these sections

These are revised local methods and results sections. They supplement the existing dataset/preprocessing section and require citation/numbering integration before submission. The original consultation document and Google Doc have not been edited. The analysis is exploratory development following earlier examination of the same test partition.

## Abstract draft

Feature-attribution conclusions can depend on the reference assumptions used by explanation algorithms. This study compares interventional and tree-path-dependent TreeSHAP on the UCI credit-card-default dataset using four tree-model families: Random Forest, Extra Trees, Gradient Boosting, and XGBoost. Models share a fixed group-aware partition and encoded predictor schema. Three configurations per family are compared by validation average precision, and classification thresholds are selected by validation F1. Attribution analysis uses 1,000 fixed test observations, three training backgrounds for the primary seed, and two additional training seeds with a fixed background. The analysis focuses on correlated billing features and assesses global importance, individual top-feature agreement, winner margins, and paired attribution differences. For the primary seed and background, top-billing-feature disagreement spans {mi:.1f}% to {ma:.1f}% across model families. Model-specific output units, differing baselines, prior test exposure, and the limited seed/background design constrain interpretation. The study evaluates sensitivity of model explanations and does not identify causal effects or establish an attribution method as universally correct.

## 1. Research questions and scope

The study asks whether two TreeSHAP settings lead to different billing-feature allocations within the same fitted predictor, whether similar global rankings coexist with different individual leading features, and whether disagreements persist when near-tied winners are examined separately. Comparisons across model families are descriptive. The fitted function changes across families, so between-family differences cannot be assigned solely to explainer behavior.

Six BILL_AMT variables form the primary group. Six PAY_AMT variables form a secondary comparison with training-set correlations recorded before interpretation. Demographic and repayment-status indicators remain in the predictive models. No correlated billing feature is removed. A difference between the two feature groups is not interpreted as the causal effect of correlation because relevance, distributions, and model usage also differ.

## 2. Predictive model development

All models use the existing 18,005/5,997/5,998 training/validation/test partition. Exact mapped predictor profiles remain within one partition, and the fitted training-only encoder provides the same 89 input columns. Model families receive three candidate configurations each, which is an equal number of configurations rather than an equal computational budget or an exhaustive optimization.

Random Forest and Extra Trees use 300 trees, minimum leaf size 5, and square-root feature sampling. Depth candidates are 8, 12, and unrestricted. Random Forest uses bootstrap sampling; Extra Trees does not. Gradient Boosting uses 200 stages, learning rate 0.05, minimum leaf size 5, and depths 2/3/4, with subsample 1. XGBoost uses 300 estimators, learning rate 0.05, depths 2/3/4, row and column sampling fractions 0.8, L2 regularization 1, histogram tree construction, and the binary-logistic objective. No class resampling or class weighting is applied.

Candidate selection uses the highest validation average precision at training seed 42. Exact ties retain the first candidate. Within each family, selected hyperparameters are frozen for seeds 17 and 73. A separate classification threshold for each fitted model maximizes validation F1; tied maxima select the higher threshold. Models are not refitted on combined training and validation data. All four families are included in explanation analysis regardless of which has the highest predictive score.

Performance reporting includes AP, ROC-AUC, precision, recall, F1, accuracy, Brier score, and log loss. AP and ROC-AUC evaluate continuous scores; threshold-based metrics evaluate binary decisions. Brier score is not interpreted as a pure calibration measure. No business-cost-optimal threshold is claimed.

## 3. Paired TreeSHAP protocol

The evaluation sample contains the same 1,000 test observations used in the original experiment, selected without replacement using seed 20261022. Backgrounds contain 100 training observations each, sampled with seeds 20261021, 20261023, and 20261024. The primary training seed is evaluated with all three backgrounds. The additional model seeds use only the first background, keeping background and model randomness separate rather than running a complete factorial design.

Both explanation modes use the same fitted predictor, observations, encoded column order, and raw output within each comparison. Calculations use approximate=False. Random Forest and Extra Trees raw outputs are default probabilities. Gradient Boosting and XGBoost raw outputs are log-odds margins. Additive reconstruction is compared against the corresponding native prediction function; probability magnitudes and margin magnitudes are not directly pooled. Sigmoid transformations of individual margin attributions are not used to construct probability attributions.

A 20-observation implementation pilot precedes each model's main explanation. Absolute reconstruction tolerances are 1e-6 for the scikit-learn families and 1e-5 for XGBoost. The latter was documented after a 300-tree technical pilot showed approximately 1-2e-6 discrepancies against native float32 margins. Actual errors and settings are retained. Two additional primary-RF background results reuse verified historical arrays after full validation/test prediction identity and parameter equality were established.

## 4. Attribution measures

Global feature importance is the sample mean of absolute SHAP values. For each observation, the top billing feature maximizes absolute attribution among the six billing columns. Tied maxima within absolute tolerance 1e-12 in either mode are excluded from the agreement denominator. Spearman correlation and Kendall tau-b summarize agreement between the six-feature global rankings; they are descriptive summaries rather than population significance tests.

For the two largest absolute attributions a1 and a2, the winner margin is (a1-a2)/(a1+a2), set to zero for a denominator at most 1e-12. Disagreement is reported for all unique maxima and for subsets requiring both modes' margins to exceed 0.01, 0.05, and 0.10. All thresholds were specified in the protocol, and changing subset denominators are reported.

Paired magnitudes include the mean sum of absolute feature differences and the mean absolute difference between signed group sums. A relative L1 index divides the former by the mean absolute model raw output centered on the path baseline. This index is not invariant under nonlinear link transformations. Signed sums over the billing group are aggregates of individual-player attributions, not Shapley values of a new grouped-player game.

For whole-model reporting, signed one-hot attributions are summed to each original variable before taking mean absolute values. This reporting aggregation does not redefine the underlying encoded-input game. Interventional masking of encoded inputs may create combinations outside natural categorical patterns, which remains an interpretation limitation.

## 5. Predictive results

{md(perf)}

The primary family selected by validation AP is **{winner}**. Test performance is reported after selection and is not used to choose the family. These results are not directly comparable with published metrics obtained using other splits, encodings, sampling policies, or tuning budgets.

![Validation and test average precision](figures/predictive_ap.png)

## 6. Attribution results

Primary seed/background results for the billing group:

{md(q[['family','n_valid','n_disagreement','disagreement_rate','spearman','mean_L1_difference','units']])}

Raw magnitudes retain their model-specific units. Differences in baselines necessarily lead to compensating changes in total attribution when both modes reconstruct the same output. Billing-group differences therefore cannot be described solely as redistribution among months with an unchanged group total.

![Mean absolute billing attributions](figures/billing_importance.png)

Winner-margin subsets:

{md(A[(A.seed==42)&(A.background_seed==20261021)&(A.group=='BILL_AMT')&(A.margin_cutoff.isin([0,.05]))][['family','margin_cutoff','n_valid','n_disagreement','disagreement_rate']])}

![Individual disagreement and winner margins](figures/winner_margin_disagreement.png)

The subset analysis assesses whether disagreement coexists with more clearly separated local winners. It does not convert disagreement into an explanation error rate or show that excluded cases are unimportant. Magnitudes and changed denominators must be considered together.

The two forest families have similar top-feature disagreement rates but different L1 magnitudes in the same probability units. Ranking switches and attribution magnitudes should therefore be reported separately. The following plot compares the distributions for unchanged and changed winners in the primary setting; outliers are hidden only in the display, not removed from the data.

![Attribution magnitude by winner agreement](figures/difference_magnitude_by_winner.png)

## 7. Background and training-seed sensitivity

![Background composition sensitivity](figures/background_disagreement.png)

{md(S)}

The seed check is descriptive and limited to three runs. The seed table checks equality of test prediction vectors against seed 42. Identical vectors, if observed, are not treated as evidence of additional varied fits; equality on this sample alone would not establish equality of the functions over all possible inputs. Background sizes remain fixed at 100, and all are sampled from the same training partition; this is not an evaluation under a new population or externally shifted portfolio. The additional seeds do not have all three backgrounds, so no general model-seed-by-background interaction is estimated.

## 8. Relation to earlier work and limitations

Comparisons between interventional and path-dependent explanations and sensitivity to portfolio reference distributions already appear in García-Céspedes, Alias-Carrascosa, and Moreno (2025). Lin and Wang (2025) study training-seed stability using 100 XGBoost fits on the same UCI credit dataset. Neither use of TreeSHAP, reuse of this dataset, nor seed repetition is claimed as a new contribution. The present empirical focus combines model-family comparisons, global/local agreement, and winner-margin diagnostics; a claim of first use requires a broader literature audit than performed here.

One dataset, one previously examined test partition, limited hyperparameter search, three training seeds, and three fixed-size backgrounds limit generalization. The experiment does not manipulate correlation, establish causal effects, evaluate a population-level significance hypothesis, or validate Shapley values against exhaustive enumeration on a small tree. Numerical additivity verifies consistency with model outputs and does not prove substantive or causal correctness.

## References for these sections

- García-Céspedes, R., Alias-Carrascosa, F. J., and Moreno, M. (2025). On Machine Learning models explainability in the banking sector: the case of SHAP. https://doi.org/10.1080/01605682.2025.2485263. Publisher abstract/metadata and accessible notes checked; complete full text not audited.
- Lin, L., and Wang, Y. (2025). SHAP Stability in Credit Risk Management: A Case Study in Credit Card Default Model. https://doi.org/10.3390/risks13120238. Accessible publisher-method excerpts checked.
- SHAP developers. TreeExplainer documentation. https://shap.readthedocs.io/en/latest/generated/shap.TreeExplainer.html. Runtime versions are recorded in manifest.json.
- scikit-learn developers. GradientBoostingClassifier 1.7.2. https://scikit-learn.org/1.7/modules/generated/sklearn.ensemble.GradientBoostingClassifier.html.
- XGBoost developers. Parameter documentation. https://xgboost.readthedocs.io/en/stable/parameter.html.

Full numerical tables, per-observation results, software versions, membership, models, baselines, and protocol amendments are retained in this experiment directory.
'''
(O/'paper_methods_results_en.md').write_text(text,encoding='utf-8')
print('Local manuscript sections written')

# Assemble a full local draft while retaining the historical section files.
import re
data=(B/'paper/dataset_preprocessing.md').read_text(encoding='utf-8')
data=data.replace('obtained through its Kaggle mirror','available through its Kaggle mirror')
data=data.replace('# Dataset and Preprocessing','## Dataset and preprocessing',1)
# Preserve original source references, replacing subsection levels to fit the manuscript.
data=re.sub(r'^## ([A-F]\. )?', '### ',data,flags=re.M)
data=data.replace('### Dataset and preprocessing','## Dataset and preprocessing',1)
abstract=text.split('## Abstract draft\n\n',1)[1].split('\n\n## 1.',1)[0]
body=text.split('## 1. Research questions and scope',1)[1]
body='## Research questions and scope'+body
body=re.sub(r'^## \d+\. ', '## ',body,flags=re.M)
body=body.replace('](figures/','](../experiments/revision_v1/figures/')
intro="""## Introduction

Credit-default classifiers use demographic characteristics, credit limits, and repayment histories to estimate a binary outcome. Predictive evaluation establishes how scores and decisions behave on held-out records, whereas attribution analysis examines how a fitted model's output is allocated among its inputs. These are separate objectives: changing an explanation setting need not change the underlying prediction.

Monthly billing features can carry overlapping information. A feature-attribution method must specify what a coalition of available features means and how the remaining features are represented. Interventional and tree-path-dependent TreeSHAP implement different reference mechanisms. Their numerical agreement therefore cannot be assumed, and disagreement alone does not identify an explanation error.

Existing credit-risk studies already compare explanation settings and examine stability under model initialization. This study is positioned as focused empirical development rather than a new attribution algorithm. Its evaluation links global billing-feature rankings, individual top-feature agreement, and the separation between the two largest local attributions. Four tree-model families provide a descriptive comparison under a common split and evaluation sample. A secondary payment-feature group is included with training-only correlation measurements; group differences do not isolate correlation as a cause.

## Related work and game-theoretic basis

Shapley values allocate the value of a cooperative game according to average marginal contributions over player orderings. For model explanations, the game is defined by a coalition-value function and a reference mechanism. Features are players; the allocated total is the model output relative to a baseline. Shapley uniqueness applies after specifying the game and does not require two different reference games to produce identical allocations (Shapley, 1953; Sundararajan and Najmi, 2020).

SHAP provides an additive attribution framework, and TreeSHAP exploits tree structure to calculate attributions under supported dependence assumptions (Lundberg and Lee, 2017; Lundberg et al., 2020). Tree-path-dependent explanations use path statistics in the fitted trees and are not treated here as general exact conditional-expectation SHAP estimates.

García-Céspedes et al. (2025) examine interventional/path-dependent explanations and sensitivity to portfolio reference distributions. Lin and Wang (2025) assess global-ranking stability over 100 XGBoost fits on the same UCI credit dataset. The present three-seed design does not match that seed coverage. Our focus adds model-family and winner-margin diagnostics to a paired empirical analysis, but first-use claims require a broader review. The accessible evidence and full-text access limitations are documented in the experiment's literature_positioning.md.

"""
conclusion="""
## Discussion and conclusion

The experiment separates predictive selection from attribution assessment. The model with the highest validation AP remains the predictive primary model even when another family's test AP is slightly higher. Explanation comparisons retain each model's native output space; probability and margin attributions are not combined as if they had identical units.

The results include settings in which identical global billing-feature orderings coexist with different leading features for individual observations. Winner-margin subsets distinguish near-tied rankings from more clearly separated local winners, while paired L1 and group-sum differences retain magnitude information. Neither diagnostic supplies a ground-truth attribution target. Background and seed variation are reported as limited descriptive sensitivity checks, not population inference.

The evidence supports documenting explanation settings, baselines, output units, and individual-level agreement alongside global importance. Conclusions apply to the fitted functions, fixed evaluation sample, and sampled references examined. Additional datasets, broader model-seed replication, background-size experiments, and controlled-correlation designs remain possible extensions rather than completed validations.

## Foundational references

- Shapley, L. S. (1953). A Value for n-Person Games. https://doi.org/10.1515/9781400881970-018.
- Lundberg, S. M., and Lee, S.-I. (2017). A Unified Approach to Interpreting Model Predictions. https://proceedings.neurips.cc/paper/2017/hash/8a20a8621978632d76c43dfd28b67767-Abstract.html.
- Lundberg et al. (2020). From local explanations to global understanding with explainable AI for trees. https://doi.org/10.1038/s42256-019-0138-9.
- Sundararajan, M., and Najmi, A. (2020). The Many Shapley Values for Model Explanation. https://proceedings.mlr.press/v119/sundararajan20b.html.

Editorial status: Local full draft assembled from the existing dataset section and the revised methods/results. Reference labels from the dataset section are preserved; consolidation into a journal citation style remains an author-review step. The full text of the García-Céspedes paper has not been audited in full. Google Docs is unchanged.
"""
full='# Mode Sensitivity of TreeSHAP Attributions across Tree-Based Credit Default Models\n\nDraft for author review - 23 October 2026.\n\n## Abstract\n\n'+abstract+'\n\n'+intro+data+'\n\n'+body+conclusion
(B/'paper/manuscript_revision_en.md').write_text(full,encoding='utf-8')
print('Full local manuscript draft written')
