# Publication and maintenance

[Documentation](README.md) | [Validation](../VALIDATION.md)

## Destinations

- GitHub: https://github.com/muhammadrafifatihulihsan/convnext-tiny-mmfood-multihead
- Hugging Face: https://huggingface.co/muhammadrafifatihulihsan/convnext-tiny-mmfood-multihead

Local packages are publish/github/convnext-tiny-mmfood-multihead and publish/huggingface/convnext-tiny-mmfood-multihead. GitHub carries source, executed notebooks and evidence. HF carries safetensors, model/config/processor/labels and reports. Dataset CSVs, image caches, checkpoints and old archives are excluded from this release.

## Owner release checks

1. Compare original source, weights and notebook bytes with the staged copies.
2. Update docs from actual reports; retain metric denominators, preprocessing choices and duplicate-audit limitations.
3. Check local links, model-card metadata, JSON and secret patterns. Review staged filenames.
4. Test a complete local model folder on CPU. Record dependencies and output shapes; do not call that a full benchmark.
5. Verify authenticated identities and remote inventories. Push GitHub and upload only the curated HF package, retaining unrelated remote files and history.
6. Confirm public visibility and test anonymous download and model loading from the published revision.

Use local hf auth login. If a stale token is retained, use hf auth login --force, then hf auth whoami. Do not paste tokens into notebook cells, documentation, command arguments or remote URLs. Do not use another cached account to update the author's repo.

The original notebook's generated model card is a draft requiring review, not a replacement for curated analysis. SHA256SUMS.txt lists package files excluding itself and Git internals. Checksums establish byte integrity, not scientific validity. Line-ending rules preserve code/notebook bytes to keep comparisons meaningful.

## Hugging Face discovery metadata

The primary task remains image-classification, with custom multi-head inference documented explicitly. Manual tags are convnext, food-recognition, multi-task, nutrition-estimation and custom_code. Language tags are omitted: bilingual documentation is not evidence of a text-language modeling capability. Dataset, backbone, library and custom license metadata are kept in their dedicated fields.

Hub-generated tags (for example safetensors, model type, feature-extraction inferred from AutoModel, base-model relations, cited papers or region) may remain visible. They are not duplicate manual tags and are not removed by changing model-card keywords. The primary task and usage guide describe the actual intended interface; code/config are not altered just to change an inferred badge. See the [official model-card metadata guide](https://huggingface.co/docs/hub/model-cards).

## Bilingual and cross-platform consistency

README.md/README.id.md, docs/usage.md/docs/usage.id.md, and docs/results.md/docs/results.id.md are complete paired guides, not summaries of each other. Stable section IDs, figures, tables, code examples and quantitative values must stay aligned. Both languages use the same numeric notation so values can be checked without locale ambiguity. Other technical guides are currently English.

Shared Markdown bodies are identical in the GitHub and HF packages. Only the HF English README adds Hub YAML metadata; GitHub-only source/template/checking files need not exist in HF. Notebook links point to GitHub from both hosts. Download examples skip the historical raw archive by default and explain how to include it.

From the GitHub checkout run `python scripts/check_publication_docs.py`. To compare both staging packages, add `--peer ../../huggingface/convnext-tiny-mmfood-multihead`. The [checker source](https://github.com/muhammadrafifatihulihsan/convnext-tiny-mmfood-multihead/blob/main/scripts/check_publication_docs.py) validates section alignment, numeric parity, example and figure parity, table structure, local links and anchors, recorded metrics and checksum manifests. Meaning and translation quality still require a paragraph-level review. Refresh manifests before running checks after intentional edits.
