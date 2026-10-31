# Download and run the model

[English](usage.md) | [Bahasa Indonesia](usage.id.md) | [Documentation](README.md)

<a id="download"></a>

## Download the model

Download the full inference package, including weights, configuration, labels and custom model code. No training run, dataset or GPU is required to try CPU inference.

```python
from huggingface_hub import snapshot_download
folder = snapshot_download(
    repo_id="muhammadrafifatihulihsan/convnext-tiny-mmfood-multihead",
    local_dir="models/convnext-tiny-mmfood-multihead",
    ignore_patterns=["raw/**"],
)
print(folder)
```

The existing Hub raw/ archive contains another historical checkpoint of about 112.4 MB. The example excludes it because safetensors inference does not need it. Omit ignore_patterns only if you want that archive too. Reports and code add to the main weight size. A GitHub ZIP does not include model weights.

Pin revision to a commit SHA from the Hub's Files and versions page for reproducible downloads. Public downloads do not require a token. See [the usage guide](usage.md) for environment setup and offline loading.

<a id="inference"></a>

## Run one image

The tested environment is Python 3.10 on Windows, using CPU inference. Create a virtual environment, activate it, then install the recorded working versions:

```bash
python -m venv .venv
```

Activate with `.venv\Scripts\Activate.ps1` in PowerShell, `source .venv/bin/activate` on Linux/macOS, or `source .venv/Scripts/activate` in Windows Git Bash.

```bash
python -m pip install torch==2.14.1 torchvision==0.29.2 transformers==5.20.2 safetensors==0.8.0 pillow==12.3.0 huggingface_hub==2.4.0
```

After downloading, save this as predict_food.py beside food.jpg and run `python predict_food.py`:

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

Review modeling_mmfood.py before enabling trust_remote_code. This custom model does not promise compatibility with the generic image-classification pipeline. The pinned versions record one tested environment, not every OS/GPU combination.

The example follows historical bilinear Resize(255), CenterCrop(224) and ImageNet normalization. The retained exported processor uses bicubic sampling and crop_pct=0.875, so it is not substituted silently. Historical metrics cannot be assumed equal across those paths.

<a id="outputs"></a>

## Understand the outputs

| Key | Meaning |
| --- | --- |
| food_type | Top-k label/softmax-score pairs for food context |
| dish_name | Top-k pairs from the fixed dish vocabulary |
| cooking_method | Top-k pairs for normalized cooking labels |
| nutrition | calories_kcal, protein_g, fat_g, carbohydrate_g |

predict() returns one dictionary per image. Use positive topk, normally 1-3; each head caps it at its class count. Nutrition is decoded from standardized log1p space, clipped nonnegative and rounded to one decimal. It is not explicitly per 100 g. Low-level nutrition_pred is still standardized log space.

Softmax scores are not calibrated certainty. Unknown dishes are not rejected: predictions always choose known labels. For CUDA, move model and input to the same device. No latency or memory benchmark is claimed.

<a id="permission"></a>

## Permission

Personal non-commercial evaluation only; see [terms](../LICENSE.md). This guide demonstrates inference, not permission to modify or fine-tune the model. [Validation](../VALIDATION.md) records the tested scope.
