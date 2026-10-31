# Experiment audit

## Existing evidence

ConvNeXt-Tiny with food-type (5), dish (50), cooking-method (11) classification heads and a four-output nutrition regression head. Six recorded epochs; split sizes: 28,798 train, 3,600 validation, 3,600 test.

Test accuracy: food type 77.9167%; cooking 65.5%; dish 79.2056%. Dish accuracy applies to only 856 labeled test images (23.78%), not all 3,600. Train/validation dish counts are 6,464/790.

Nutrition MAE: calories 95.6775 kcal, protein 6.2753 g, fat 5.2291 g, carbohydrate 13.2584 g. Baseline MAE: 190.0570 kcal, 14.0763 g, 10.5646 g, 23.4719 g respectively. The baseline is expm1(mean(log1p(train targets))), not the arithmetic mean in original units. Metrics are historical artifacts, not a newly reproduced evaluation.

## Methodological limits

No image URL overlap was found between splits. The subsequent content audit below confirms exact duplicates across splits; this weakens test independence and may inflate reported performance. Top-50 dish selection occurs before splitting, so class vocabulary uses full-data frequency information. Nutrition normalization is fitted on train only. Labels are partly AI-generated and are not laboratory nutrition measurements. Class imbalance, restricted dish vocabulary, portions, and sampling introduce limitations.

## Preprocessing discrepancy

Historical evaluation uses torchvision Resize(int(224*1.14)) = Resize(255), default bilinear interpolation, CenterCrop(224), ToTensor, ImageNet normalization. Exported ConvNextImageProcessor uses crop_pct=0.875 and bicubic resampling, so its preprocessing differs. Use the explicit evaluation transform in the README for comparisons to historical results. Export weights and processor are preserved unchanged; do not assume metric equivalence for the exported processor.

## Reproduction limitations

Notebooks require Google Colab and a Drive ZIP bootstrap. They are preserved with outputs and original source. Environment packages were not fully pinned; exact historical reproduction is not guaranteed. Resume checkpoints omit scaler/RNG state. The code and weights were not repaired or retrained in this publication.

## Cached-image content audit

SHA-256 checked 35998 cached image files; 33889 distinct byte hashes; 477 repeated-content occurrences crossing split boundaries. This detects exact bytes only, not visually similar images.
