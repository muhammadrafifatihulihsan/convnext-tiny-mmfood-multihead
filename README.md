# convnext-tiny-mmfood-multihead

Image-based multi-task food classification and nutrition estimation using ConvNeXt-Tiny.

[Model and downloadable files](https://huggingface.co/muhammadrafifatihulihsan/convnext-tiny-mmfood-multihead) ? [Source and notebooks](https://github.com/muhammadrafifatihulihsan/convnext-tiny-mmfood-multihead) ? [Bahasa Indonesia](README.id.md)

The source code, model weights, notebook outputs and historical metrics are preserved. See [experiment analysis](ANALYSIS.md), [usage terms](LICENSE.md), and [third-party notices](THIRD_PARTY_NOTICES.md). Personal non-commercial evaluation only; this is not an open-source license.

> Evaluation caveat: exact cached-image duplicates cross dataset splits (477 repeated-content occurrences detected). Historical test metrics may be optimistic; see ANALYSIS.md. No retraining or deduplication was performed.

## Download and inference

```python
from huggingface_hub import snapshot_download
folder = snapshot_download("muhammadrafifatihulihsan/convnext-tiny-mmfood-multihead")
```

Install `requirements.txt` in an isolated Python environment. The listed lower bounds are original, not a verified compatibility matrix.

```python
import torch
from PIL import Image
from torchvision import transforms as T
from transformers import AutoModel
model = AutoModel.from_pretrained(folder, trust_remote_code=True).eval()
transform = T.Compose([T.Resize(255), T.CenterCrop(224), T.ToTensor(),
    T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])
x = transform(Image.open("food.jpg").convert("RGB")).unsqueeze(0)
with torch.no_grad():
    print(model.predict(x, topk=3)[0])
```

Review the custom model code before loading it; pin `revision` to the published commit for reproducibility. Outputs contain top-k food type, dish name, cooking method, and estimated nutrition (kcal and grams). This is an experimental model, not a medical or dietary decision tool.

## Repository contents

GitHub contains code, notebooks, experiment configuration and reports. Hugging Face contains inference weights and model files plus reports. Dataset CSVs, image caches, training checkpoints and old ZIP archives are excluded.

## Training notebook setup

Read docs/REPRODUCTION.md before executing notebooks 00?08 in Colab. Outputs are retained to show the original process; they do not establish reproducibility in a fresh environment. Existing docs under docs/ describe the historical workflow; this README and ANALYSIS.md clarify current publication limitations.
