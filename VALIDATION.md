# Publication validation

[Documentation](docs/README.md) | [Results and limitations](docs/results.md)

## Checks completed

| Check | Outcome | Scope |
| --- | --- | --- |
| Source integrity | Pass | Original src files byte-identical in the staged GitHub package |
| Notebook integrity | Pass | All 9 notebook files byte-identical, including original outputs |
| Model integrity | Pass | Weights, config, labels, processor and model code identical to original export |
| Local documentation links | Pass | Every relative Markdown target resolves in both packages |
| Model-card metadata | Pass | Parsed with huggingface_hub.ModelCard; custom license and library metadata present |
| JSON validity | Pass | Published JSON artifacts parse |
| Python examples | Pass | Complete inference/download examples compile |
| Local CPU inference | Pass | Complete HF package loads without backbone download; four outputs have expected shapes and finite values |
| Prediction decoding | Pass | One result per image; four nutrition keys and ranked classification outputs |
| Secret pattern scan | No matches | HF/GitHub token patterns and private-key headers in published text and notebooks |
| Exact-image audit | Leakage detected | 281 test images match train; see publication_audit.json |

## Tested environment

Python 3.10 on Windows, CPU inference. Package versions:

| Package | Version |
| --- | --- |
| torch | 2.14.1 |
| torchvision | 0.29.2 |
| transformers | 5.20.2 |
| safetensors | 0.8.0 |
| Pillow | 12.3.0 |
| huggingface_hub | 2.4.0 |

Inference used one cached RGB food image with the documented bilinear Resize(255), CenterCrop(224), ToTensor and ImageNet normalization. Forward shapes were [1,5], [1,50], [1,11], [1,4]. This is a loading/execution check, not a new accuracy benchmark.

## Limits of this validation

The six-epoch experiment and full test set were not rerun. No claim is made about GPU speed, all operating systems, calibrated probabilities, near-duplicate removal, clinical performance or absence of every possible privacy issue. Token-pattern scanning is not a complete malware/privacy audit. Existing public dataset contact information and historical notebook outputs remain.

Exact-image audit results are new publication evidence; saved test_metrics.json and history.json are untouched. The earlier order-dependent count of 477 crossing occurrences is replaced by clearly defined hash-group and image-level counts in the results guide. The source archive is retained outside the publication folders.
