# Results and interpretation

[Documentation](README.md) | [Data](data.md) | [Validation](../VALIDATION.md) | [Penjelasan Indonesia](results.id.md)

<a id="saved-results"></a>

## Saved test results

These are recorded results from test_metrics.json, not a newly repeated evaluation. Checkpoint selection minimizes validation loss over six recorded epochs.

| Task | Accuracy | Evaluated examples |
| --- | ---: | ---: |
| Food type | 77.92% | 3,600 |
| Dish, top-50 vocabulary | 79.21% | 856 |
| Cooking method | 65.50% | 3,600 |

Dish accuracy applies only to the labeled subset (23.78% of test), not arbitrary food photographs. The model always ranks known dishes even when the actual dish is outside its vocabulary.

| Nutrition | Model MAE | Baseline MAE | Relative MAE reduction |
| --- | ---: | ---: | ---: |
| Calories (kcal) | 95.68 | 190.06 | 49.66% |
| Protein (g) | 6.28 | 14.08 | 55.42% |
| Fat (g) | 5.23 | 10.56 | 50.50% |
| Carbohydrate (g) | 13.26 | 23.47 | 43.51% |

Baseline: `expm1(mean(log1p(train_targets)))`, predicted for every test image. It is neither the arithmetic mean in original units nor the median baseline that minimizes absolute error. Relative error reduction is not nutrition accuracy.

<a id="assessment"></a>

## Are these results poor?

The model learns useful signals on the recorded split, but the evidence is not strong enough to call it reliable on new real-world photographs. It is more accurate to describe it as a limited experimental baseline than to label the whole project either a failure or a success. There is no task-specific acceptance threshold or independent external benchmark here.

For context, new publication-time calculations choose the most frequent label in training and predict that one label for every eligible test image:

| Task | Train-majority baseline on test | Recorded model | Interpretation |
| --- | ---: | ---: | --- |
| Food type | 46.58% (1,677/3,600) | 77.92% | Better than always predicting the dominant context |
| Dish, labeled subset | 10.05% (86/856) | 79.21% | Stronger than a constant prediction within the restricted vocabulary |
| Cooking | 18.28% (658/3,600) | 65.50% | Learned signal, but roughly one third of eligible predictions are wrong |

These are constant-class baselines, not competing trained models, and they share the same compromised split. They do not establish leakage-free generalization. Their counts are stored in publication_audit.json; historical model metrics remain unchanged.

For nutrition, MAE 95.68 kcal means an average absolute deviation of about 96 kcal from dataset labels. It does not mean every prediction is within 96 kcal, a 95.68% accuracy, or a clinical error tolerance. Some errors can be much larger; tail errors and subgroup errors were not reported. Lower MAE than a constant baseline demonstrates a useful comparison on this split, not trustworthy portion measurement.

<a id="causes"></a>

## Why performance remains limited

| Task or mechanism | What is established in this project | Plausible effect, not a measured causal attribution |
| --- | --- | --- |
| Food context | Labels include homemade and restaurant food; input is only a food image | The same-looking dish can be prepared at home or served in a restaurant. Context labels may require information outside the crop |
| Minority classes | Others has 77 train and 10 test examples; majority classes dominate | Few examples can limit learning and make minority-class estimates unstable; overall accuracy can conceal this |
| Dish coverage | Only 6,464 train images have a top-50 dish target; other dish targets are ignored | The dish head sees less direct supervision than the other tasks; the system cannot name dishes outside its vocabulary |
| Cooking supervision | Ordered keyword rules collapse raw descriptions into 11 labels | Mixed cooking processes may not fit a single class; boiled, steamed and stewed food may have overlapping visual appearance |
| Nutrition supervision | Targets are source annotations, including model-assisted estimates; portion and ingredient columns are unused | An image alone does not reliably reveal oil, hidden ingredients, mass or recipe. Similar images can correspond to different nutrition targets |
| Image information | Cache longest side is at most 256 pixels; input is a 224 crop | Small textures and parts of a meal may be lost. Random training crops retain the full-image nutrition target, which may create a crop/target mismatch |
| Multi-task optimization | One encoder serves four heads, with fixed loss weights | Tasks may compete for shared features, or help each other. No single-task or loss-weight ablation establishes the direction or size of this effect |

The left-hand evidence comes from saved configuration, labels, split counts and code. The mechanisms in the last column are hypotheses explaining why this setup is challenging; no experiment here isolates their individual effect. It would be incorrect to assign a percentage of the error to any one cause.

<a id="diagnosis"></a>

## What the curves can and cannot diagnose

Six epochs were recorded, with validation loss still improving slightly at the end. This does not prove the model needs more epochs, that six epochs are the main problem, or that a larger backbone will solve it. Training and validation losses use different data and augmentation/dropout behavior, so their numerical gap is not a controlled overfitting test. The later plateau is consistent with diminishing returns, but neither pure underfitting nor overfitting is established by these curves alone.

Likewise, image leakage is a credibility problem that may inflate results; it is not an explanation for low accuracy. The processor mismatch can explain differences between notebook and exported-processor predictions, but cannot explain historical test errors computed with the notebook transform. These two issues must not be used as generic excuses for every failure.

<a id="priorities"></a>

## What should be investigated first

For a future owner-authorized experiment, prioritize reliable measurement before a larger model: group identical/near-duplicate images before splitting; fit label choices on train only; use a consistent evaluation/inference transform; and evaluate on a separate source. Then inspect actual mistakes by class and report macro-F1, per-class recall, top-k dish coverage, nutrition tail errors and a train-median nutrition baseline.

Only after that should controlled comparisons test class balancing, label cleanup, crops that retain the whole meal, loss weights, single-task models, longer training or a larger backbone. Improved portion/ingredient information would require a different input/data design. None of these changes has been implemented or claimed to improve the current weights.

<a id="training"></a>

## Training behavior

![Training curves](../reports/figures/training_curves.png)

Train loss fell from 3.709 to 1.245; validation loss from 2.343 to 1.850. Validation dish accuracy rose from 71.14% to 76.84%. Later validation improvements were smaller while train loss continued falling. Epoch 6 has the lowest recorded validation loss. These trends describe this split, not independent generalization.

![Food-type confusion matrix](../reports/figures/confusion_food_type.png)

The confusion image shows counts, not normalized recall. Raw per-class predictions are not part of the published artifacts; no new precision/recall/F1 values are inferred from image colors.

<a id="overlap"></a>

## Exact-content audit

| Measurement | Result |
| --- | ---: |
| Cached JPEG files hashed | 35,998 |
| Distinct SHA-256 values | 33,889 |
| Hash groups spanning splits | 431 |
| Images in cross-split groups | 1,715 |
| Test images with train matches | 281 / 3,600 (7.81%) |
| Validation images with train matches | 263 / 3,600 (7.31%) |

Full cached JPEG bytes were hashed and grouped by split. This confirms exact-image leakage despite disjoint URLs. Near duplicates, resized versions and recompressed copies are not detected. The earlier traversal-dependent count of 477 crossing occurrences is replaced by these order-independent counts.

Overlap can inflate validation and test results. Its effect cannot be quantified without a new grouped/deduplicated evaluation and potentially retraining. Do not subtract the duplicate fraction from accuracy to invent a corrected score. These are saved experimental results, not a leakage-free benchmark.

<a id="preprocessing"></a>

## Preprocessing discrepancy

Evaluation uses bilinear Resize(255), CenterCrop(224). The exported ConvNextImageProcessor specifies bicubic sampling and crop_pct=0.875 with shortest edge 224; its resize path differs. The [usage guide](usage.md) uses the historical transform. The processor artifact is retained unchanged for provenance. Full metrics have not been recomputed for either path during documentation work.

<a id="conclusions"></a>

## Conclusions supported by evidence

All four heads run, and saved nutrition MAE beats the recorded constant baseline. Accurate real-world portions, calibrated certainty, unseen-cuisine generalization, minority-class robustness and medical suitability are not established. A future authorized model version would require image-group splitting, train-only vocabulary selection, consistent processing and external evaluation. This publication does not silently change the original experiment.
