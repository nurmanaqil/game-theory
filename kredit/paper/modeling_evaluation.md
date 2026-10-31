# Modeling and Predictive Evaluation

## Model Development and Selection

A majority-class dummy classifier was used as a predictive baseline. Five Random Forest configurations were evaluated using the fixed training and validation partitions. Each forest contained 300 trees and used random state 42. The candidate configurations comprised the initial forest with unrestricted depth and a minimum leaf size of one, a forest with a minimum leaf size of five, a forest with maximum depth 12 and minimum leaf size five, and class-weighted variants of the latter two configurations using `class_weight='balanced'`. All models were fitted exclusively on training observations. No class resampling was applied.

The model-selection criterion was validation average precision for the default class. Average precision is reported separately from ROC-AUC. The selected configuration used maximum depth 12, a minimum of five samples per leaf, and no class weighting. Its validation average precision was 0.5731, compared with 0.5455 for the initial Random Forest. Validation ROC-AUC was 0.7898. The runner-up configuration achieved average precision 0.5717; this small difference should not be interpreted as evidence of consistent superiority across training seeds or data partitions.

**Table A. Validation performance of the candidate models at threshold 0.5.**

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC | Average precision |
|---|---:|---:|---:|---:|---:|---:|
| Majority-class baseline | 0.7722 | 0.0000 | 0.0000 | 0.0000 | 0.5000 | 0.2278 |
| Initial Random Forest | 0.8077 | 0.6433 | 0.3499 | 0.4533 | 0.7684 | 0.5455 |
| RF, minimum leaf size 5 | 0.8149 | 0.6834 | 0.3492 | 0.4622 | 0.7880 | 0.5717 |
| RF, depth 12, minimum leaf size 5 | 0.8151 | 0.6870 | 0.3455 | 0.4598 | 0.7898 | 0.5731 |
| Balanced RF, minimum leaf size 5 | 0.7976 | 0.5578 | 0.5373 | 0.5474 | 0.7866 | 0.5704 |
| Balanced RF, depth 12, minimum leaf size 5 | 0.7902 | 0.5380 | 0.5593 | 0.5485 | 0.7881 | 0.5674 |

## Decision Threshold Selection

After selecting the model, its classification threshold was selected by maximizing F1 for the default class on validation observations. Candidate thresholds were the distinct validation prediction scores; ties were resolved in favor of the higher threshold. The selected threshold was 0.23619742272000907. A prediction was labeled default when its score was greater than or equal to this threshold. Validation F1 increased from 0.4598 at threshold 0.5 to 0.5597 at the selected threshold. This threshold selection changes binary decisions but does not change the fitted forest, prediction scores, or probability-based TreeSHAP explanations.

## Held-Out Test Evaluation

The selected forest and threshold were frozen before evaluation on the 5,998 test observations. The forest was not refitted on the combined training and validation partitions. No model configuration or threshold was selected using test outcomes. ROC-AUC and average precision were calculated from the predicted scores; classification metrics were calculated using the predetermined thresholds. Positive-class precision, recall, and F1 refer to default, coded as 1.

**Table B. Held-out test performance of the selected Random Forest.**

| Threshold | Accuracy | Precision | Recall | F1 | ROC-AUC | Average precision |
|---|---:|---:|---:|---:|---:|---:|
| 0.5000 | 0.8206 | 0.6878 | 0.3374 | 0.4527 | 0.7741 | 0.5481 |
| 0.2362, selected on validation | 0.7638 | 0.4698 | 0.5770 | 0.5179 | 0.7741 | 0.5481 |

At the validation-selected threshold, the model detected 761 of the 1,319 default cases and missed 558. Among 4,679 non-default cases, 859 were incorrectly labeled default and 3,820 were correctly classified. Relative to threshold 0.5, the selected threshold detected 316 additional default cases while producing 657 additional false positives. Thus, improved recall and F1 were accompanied by lower precision and accuracy.

Test F1 (0.5179) and average precision (0.5481) were lower than their corresponding validation values (0.5597 and 0.5731). These results provide a predictive context for the subsequent attribution analysis; they do not establish deployment suitability or superiority over previously published models. Findings currently refer to one fixed partition and one training seed. Repeated-seed attribution experiments, if conducted, should be reported separately.

**Figure A.** Test-set confusion matrices for the selected Random Forest at the default threshold of 0.5 and the validation-selected threshold of approximately 0.2362. Rows represent true labels and columns represent predicted labels.

Figure source: `kredit/modeling/figures/test_confusion_matrices.png` (PDF version also available).

**Figure B.** ROC and precision-recall curves of the selected Random Forest on the test partition. The dashed precision-recall reference corresponds to the test default prevalence of 0.2199. Average precision is 0.5481 and ROC-AUC is 0.7741.

Figure source: `kredit/modeling/figures/test_roc_pr.png` (PDF version also available).

Editorial note: adjust table and figure numbering when merging with the manuscript. Source figures and this editorial note are coordination information and should be removed from the submitted manuscript.
