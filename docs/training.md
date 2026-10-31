# Recorded training workflow

[Documentation](README.md) | [Architecture](project.md) | [Data](data.md)

This describes the author's experiment for inspection and provenance. It does not grant permission to create modified models. Original notebook code and outputs are retained, including historical paths.

## Notebook sequence

| Notebook | Stage | Main artifact |
| --- | --- | --- |
| [00](https://github.com/muhammadrafifatihulihsan/convnext-tiny-mmfood-multihead/blob/main/notebooks/00_setup_config.ipynb) | Mount Drive, inspect runtime, save config | artifacts/config.json |
| [01](https://github.com/muhammadrafifatihulihsan/convnext-tiny-mmfood-multihead/blob/main/notebooks/01_eda_cleaning.ipynb) | EDA, clean labels and plot distributions | clean.csv and EDA reports |
| [02](https://github.com/muhammadrafifatihulihsan/convnext-tiny-mmfood-multihead/blob/main/notebooks/02_download_images.ipynb) | Stratified URL sample and image download | manifest.csv, images.tar |
| [03](https://github.com/muhammadrafifatihulihsan/convnext-tiny-mmfood-multihead/blob/main/notebooks/03_split_labels.ipynb) | Split, map labels, standardize nutrition | train/val/test.csv, labels.json |
| [04](https://github.com/muhammadrafifatihulihsan/convnext-tiny-mmfood-multihead/blob/main/notebooks/04_train_model.ipynb) | Optimize and validate | best.pt, last.pt, history.json |
| [05](https://github.com/muhammadrafifatihulihsan/convnext-tiny-mmfood-multihead/blob/main/notebooks/05_evaluate.ipynb) | Test metrics and baseline | test_metrics.json and figures |
| [06](https://github.com/muhammadrafifatihulihsan/convnext-tiny-mmfood-multihead/blob/main/notebooks/06_save_export_model.ipynb) | Raw and Transformers export | hf_export and raw model |
| [07](https://github.com/muhammadrafifatihulihsan/convnext-tiny-mmfood-multihead/blob/main/notebooks/07_push_to_huggingface.ipynb) | Historical Hub upload | Model repo and tag |
| [08](https://github.com/muhammadrafifatihulihsan/convnext-tiny-mmfood-multihead/blob/main/notebooks/08_package_results.ipynb) | Historical result packaging | Results ZIP |

## Recorded settings

| Parameter | Value |
| --- | --- |
| Backbone | facebook/convnext-tiny-224 |
| Image size / cache longest side | 224 / 256 |
| Batch / epochs / seed | 64 / 6 / 42 |
| Backbone / head learning rate | 5e-5 / 1e-3 |
| Optimizer / weight decay | AdamW / 0.05 |
| LR schedule | 5% linear warmup then cosine |
| Task weights | 1.0 food, 1.0 dish, 0.5 cooking, 1.0 nutrition |
| Gradient clipping | Maximum norm 1.0 |
| Precision | CUDA float16 autocast and GradScaler |
| Loader / download workers | 2 / 32 |
| Best checkpoint | Lowest validation loss |

Training drops the incomplete final batch. Random crops (scale 0.6-1.0), horizontal flips and color jitter augment training images. Evaluation uses deterministic resizing/cropping. Dropout is 0.2.

## Original Colab bootstrap

The ZIP path is `MyDrive/models-train/mmfood-multitask/mmfood-multitask.zip`. Its top-level internal directory must be `mmfood-multitask/`, extracted to `/content/mmfood-multitask`. That historical internal name remains necessary because notebook code is unchanged, although the public repo name is convnext-tiny-mmfood-multihead.

For an owner-authorized rerun, stage source, docs and upstream `data/raw/MM-Food-100K.csv` inside that internal directory before zipping. Put the ZIP at the expected Drive path, select a Colab GPU runtime and run the notebooks in sequence. Other readers can inspect all outputs without executing training.

The bootstrap sets MMFOOD_PROJECT to the Drive output directory before importing config. An artifacts/config.json inside the extracted source ZIP is not automatically the configuration loaded from that output directory. On a fresh owner run, set/save the intended configuration in notebook 00. Historical source defaults contain a placeholder HF username; notebook 07 overrides the destination explicitly. Check that cell before any upload.

## Resume limitations

last.pt includes model, optimizer, scheduler, epoch, best validation score and history. GradScaler and RNG states are absent, so resumed training is not bit-for-bit equivalent. Live image availability and dependency updates can change the result. This publication did not rerun all six epochs.

Notebook 06 reads MODEL_CARD_TEMPLATE.md; its filename is retained for compatibility but its text has been rewritten. Notebook 07 uploads raw weights and creates a v1.0 tag; the curated publication instead keeps only inference artifacts and reports. Use [publishing](publishing.md) for current owner procedures, not an unattended replay of historical upload cells.
