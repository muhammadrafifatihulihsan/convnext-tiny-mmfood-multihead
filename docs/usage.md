# Download and run the model

[Documentation](README.md) | [Bahasa Indonesia](usage.id.md) | [Troubleshooting](troubleshooting.md)

## Choose your starting point

Read the GitHub notebooks to inspect the saved process. Download Hugging Face artifacts to try predictions. Inference does not need training data, a GPU or optimizer checkpoints. The permitted use is personal non-commercial evaluation; see [terms](../LICENSE.md).

## Environment

The CPU smoke test used Python 3.10 on Windows. Create a separate environment:

```bash
python -m venv .venv
```

Activate in PowerShell with `.venv\Scripts\Activate.ps1`, Linux/macOS with `source .venv/bin/activate`, or Windows Git Bash with `source .venv/Scripts/activate`.

```bash
python -m pip install torch==2.14.1 torchvision==0.29.2 transformers==5.20.2 safetensors==0.8.0 pillow==12.3.0 huggingface_hub==2.4.0
```

These versions record one working environment, not a cross-platform compatibility guarantee. Root requirements preserve the original broader training dependencies. See [validation](../VALIDATION.md).

## Download the full model folder

```python
from huggingface_hub import snapshot_download
folder = snapshot_download(
    repo_id="muhammadrafifatihulihsan/convnext-tiny-mmfood-multihead",
    local_dir="models/convnext-tiny-mmfood-multihead",
)
print(folder)
```

Weights are approximately 112.3 MB (107.1 MiB); the full snapshot also includes reports and code. A GitHub ZIP does not contain weights. Add `revision` with a commit SHA from the model's Files and versions page to pin an artifact version. Public download does not require a token; private access requires permission and local login.

## Predict an image

Save this as `predict_food.py`, place `food.jpg` beside it, and run `python predict_food.py`:

```python
import json
import torch
from PIL import Image
from torchvision import transforms as T
from transformers import AutoModel

folder = "models/convnext-tiny-mmfood-multihead"
model = AutoModel.from_pretrained(
    folder, trust_remote_code=True, local_files_only=True
).eval()
transform = T.Compose([
    T.Resize(255), T.CenterCrop(224), T.ToTensor(),
    T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])
with Image.open("food.jpg") as image:
    pixels = transform(image.convert("RGB")).unsqueeze(0)
with torch.no_grad():
    prediction = model.predict(pixels, topk=3)[0]
print(json.dumps(prediction, indent=2))
```

This uses the original evaluation transform. The exported processor differs; see [results](results.md). Review the custom modeling code before enabling `trust_remote_code`. A complete downloaded snapshot supports local loading; weights alone are insufficient.

## Output contract

| Key | Meaning |
| --- | --- |
| `food_type` | Ranked (label, softmax score) pairs for 5 food contexts |
| `dish_name` | Ranked pairs within the 50-name vocabulary |
| `cooking_method` | Ranked pairs within 11 normalized cooking methods |
| `nutrition` | calories_kcal, protein_g, fat_g, carbohydrate_g |

`predict()` returns one dictionary per image. Use a positive topk, normally 1?3; each head caps it at its class count. Low-level forward outputs are food_type_logits, dish_logits, cooking_logits and nutrition_pred. The last is standardized log-space output, not grams or kcal. Use predict() for inverse transformation.

Scores are not calibrated certainty and unknown dishes are not rejected. Nutrition is an estimate from image annotations, not measured dietary intake. CUDA users must move both model and pixels to the same device. No latency or memory benchmark is claimed.

## Existing Hub archive

The Hub also retains a historical raw/ checkpoint from the original upload (about 112.4 MB). It is not required for the documented safetensors inference path. A full repository snapshot includes this legacy archive; use `ignore_patterns=["raw/**"]` with snapshot_download to omit it. The curated local publication folder does not duplicate this older archive.
