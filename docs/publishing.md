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
