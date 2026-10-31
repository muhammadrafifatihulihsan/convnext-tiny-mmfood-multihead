---
license: other
license_name: mmfood-personal-evaluation-only
license_link: LICENSE.md
library_name: transformers
base_model: {{BACKBONE}}
tags: [food, multi-task, image-classification, nutrition-estimation, custom_code]
---
# {{REPO_ID}}

Image-only model with three classification heads and four nutrition outputs. Custom AutoModel architecture. Source and complete usage: https://github.com/muhammadrafifatihulihsan/convnext-tiny-mmfood-multihead

## Recorded experiment

Train {{N_TRAIN}} / validation {{N_VAL}} / test {{N_TEST}}. Epochs {{EPOCHS}}, batch {{BATCH}}, backbone/head learning rates {{LR_BB}} / {{LR_HEAD}}. Dish vocabulary {{TOP_K}}.

| Task | Accuracy |
| --- | ---: |
| Food type | {{ACC_FOOD}} |
| Dish, eligible subset only | {{ACC_DISH}} |
| Cooking | {{ACC_COOK}} |

| Nutrition | MAE | Log-space constant baseline MAE |
| --- | ---: | ---: |
| Calories | {{MAE_CAL}} | {{BASE_CAL}} |
| Protein | {{MAE_PRO}} | {{BASE_PRO}} |
| Fat | {{MAE_FAT}} | {{BASE_FAT}} |
| Carbohydrate | {{MAE_CARB}} | {{BASE_CARB}} |

## Review before publication

For the original run, dish accuracy covers 856 test images and 281 of 3,600 test images match train bytes. Re-audit counts for any new run. The baseline is expm1(mean(log1p(train targets))). Exported processing differs from the historical bilinear Resize(255)/CenterCrop(224) transform. Do not claim a leakage-free benchmark, calibrated confidence or measured nutrition.

See the canonical project's docs/usage.md for full inference instructions and docs/results.md for analysis. Include LICENSE.md and THIRD_PARTY_NOTICES.md when publishing: author contributions are for personal non-commercial evaluation only, with upstream rights preserved. This generated draft needs owner review before replacing a curated model card.
