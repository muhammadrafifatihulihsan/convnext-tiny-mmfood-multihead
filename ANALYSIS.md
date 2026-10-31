# Experiment analysis

The complete analysis is organized by question:

- [Dataset and preparation](docs/data.md): filtering, label vocabularies, image sampling and imbalance.
- [Architecture](docs/project.md): shared encoder, task losses and nutrition decoding.
- [Results](docs/results.md): saved metrics, baseline, learning curves and leakage assessment.
- [Validation](VALIDATION.md): publication-time checks and their limits.

The central evaluation caveat is exact-image overlap: 281 test images match training bytes. Dish accuracy covers 856 eligible images, and exported preprocessing differs from the historical transform. Read results.md before interpreting the metrics as evidence of generalization.
