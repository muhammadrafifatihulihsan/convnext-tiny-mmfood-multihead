# Troubleshooting

[Documentation](README.md) | [Usage](usage.md)

| Symptom | Cause to check | Action |
| --- | --- | --- |
| HF 401/404 | Wrong repo, invalid token or private access | Verify exact ID and account with hf auth whoami |
| CLI says already logged in, but 401 persists | Stale stored credential | Run hf auth login --force locally; never paste tokens into code |
| hf not recognized on Windows | Scripts directory absent from PATH | Use the installed hf.exe absolute path or reopen terminal after PATH update |
| Unknown mmfood-multitask type | Custom class not loaded | Use AutoModel with trust_remote_code after reviewing code |
| Missing modeling_mmfood.py | Partial download | Download the complete snapshot |
| Different output than notebook | Image/preprocessing mismatch | Match cached image bytes and Resize(255)/CenterCrop(224) |
| Negative or standardized nutrition | Reading nutrition_pred directly | Use predict() for inverse transform |
| Torchvision import or nms error | Incompatible torch/torchvision builds | Use a clean environment and matched package versions |
| Device mismatch | Model and input use different devices | Move both to CPU or the same CUDA device |
| Colab ZIP missing | Incorrect Drive path/internal directory | Follow recorded bootstrap in training.md |
| google.colab unavailable | Notebook run outside Colab | Read saved output locally; bootstrap requires Colab |
| Generic pipeline fails | Custom multi-head output | Use AutoModel and predict() |

For issue reports, provide OS, Python/package versions, device, model revision, transform used and a redacted traceback. Do not attach tokens, environment dumps or private photographs. Unexpected dish labels may reflect vocabulary limits rather than installation failure.
