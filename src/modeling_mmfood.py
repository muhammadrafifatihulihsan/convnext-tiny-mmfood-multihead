"""
Model multi-task MM-Food: satu backbone gambar, empat "head".

  - food_type      : klasifikasi (5 kelas)
  - dish_name      : klasifikasi (Top-K nama hidangan; sisanya diabaikan saat loss)
  - cooking_method : klasifikasi (metode masak sudah dinormalisasi)
  - nutrition      : regresi 4 nilai (kalori, protein, lemak, karbohidrat)

Kelas ini dibuat sebagai PreTrainedModel + PretrainedConfig supaya bisa
`save_pretrained()` / `push_to_hub()` / `from_pretrained()` seperti model
Hugging Face standar. Karena ini arsitektur kustom, file ini ikut tersimpan
di repo HF dan model dimuat dengan `trust_remote_code=True`.
"""
from typing import List, Optional

import torch
import torch.nn as nn
from transformers import AutoConfig, AutoModel, PretrainedConfig, PreTrainedModel

NUTRITION_KEYS = ["calories_kcal", "protein_g", "fat_g", "carbohydrate_g"]


class MMFoodConfig(PretrainedConfig):
    model_type = "mmfood-multitask"

    def __init__(
        self,
        backbone_name: str = "facebook/convnext-tiny-224",
        hidden_size: int = 768,
        backbone_config: Optional[dict] = None,
        head_dropout: float = 0.2,
        food_type_labels: Optional[List[str]] = None,
        dish_labels: Optional[List[str]] = None,
        cooking_labels: Optional[List[str]] = None,
        nutrition_keys: Optional[List[str]] = None,
        nutrition_mean: Optional[List[float]] = None,
        nutrition_std: Optional[List[float]] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.backbone_name = backbone_name
        self.hidden_size = hidden_size
        # config backbone disimpan di sini supaya model bisa dimuat TANPA internet / akses ke repo backbone
        self.backbone_config = backbone_config
        self.head_dropout = head_dropout
        self.food_type_labels = food_type_labels or []
        self.dish_labels = dish_labels or []
        self.cooking_labels = cooking_labels or []
        self.nutrition_keys = nutrition_keys or list(NUTRITION_KEYS)
        # statistik standardisasi pada ruang log1p (dipakai untuk inverse-transform)
        self.nutrition_mean = nutrition_mean or [0.0] * 4
        self.nutrition_std = nutrition_std or [1.0] * 4


class MMFoodMultiTask(PreTrainedModel):
    config_class = MMFoodConfig
    base_model_prefix = "backbone"

    def __init__(self, config: MMFoodConfig, load_backbone_weights: bool = False):
        super().__init__(config)
        if load_backbone_weights:
            # dipakai saat training pertama kali: ambil bobot pretrained
            self.backbone = AutoModel.from_pretrained(config.backbone_name)
        else:
            # dipakai saat from_pretrained(): bobot akan diisi dari checkpoint
            if config.backbone_config:
                bc = dict(config.backbone_config)
                model_type = bc.pop("model_type")
                bb_cfg = AutoConfig.for_model(model_type, **bc)
            else:
                bb_cfg = AutoConfig.from_pretrained(config.backbone_name)
            self.backbone = AutoModel.from_config(bb_cfg)

        h = config.hidden_size
        self.dropout = nn.Dropout(config.head_dropout)
        self.food_type_head = nn.Linear(h, max(len(config.food_type_labels), 1))
        self.dish_head = nn.Linear(h, max(len(config.dish_labels), 1))
        self.cooking_head = nn.Linear(h, max(len(config.cooking_labels), 1))
        self.nutrition_head = nn.Sequential(
            nn.Linear(h, 256), nn.GELU(), nn.Dropout(config.head_dropout), nn.Linear(256, 4)
        )
        self.post_init()

    def encode(self, pixel_values: torch.Tensor) -> torch.Tensor:
        out = self.backbone(pixel_values=pixel_values)
        feats = out.pooler_output
        if feats.dim() > 2:
            feats = feats.flatten(1)
        return self.dropout(feats)

    def forward(
        self,
        pixel_values: torch.Tensor,
        food_type: Optional[torch.Tensor] = None,
        dish: Optional[torch.Tensor] = None,
        cooking: Optional[torch.Tensor] = None,
        nutrition: Optional[torch.Tensor] = None,
        loss_weights=(1.0, 1.0, 0.5, 1.0),
    ):
        z = self.encode(pixel_values)
        logits_food = self.food_type_head(z)
        logits_dish = self.dish_head(z)
        logits_cook = self.cooking_head(z)
        pred_nut = self.nutrition_head(z)

        result = {
            "food_type_logits": logits_food,
            "dish_logits": logits_dish,
            "cooking_logits": logits_cook,
            "nutrition_pred": pred_nut,  # ruang log1p yang sudah distandarisasi
        }

        if food_type is not None:
            ce = nn.CrossEntropyLoss(ignore_index=-100)
            parts = {}
            parts["food_type"] = ce(logits_food, food_type)
            parts["dish"] = ce(logits_dish, dish) if (dish is not None and (dish != -100).any()) else logits_dish.sum() * 0
            parts["cooking"] = ce(logits_cook, cooking) if (cooking is not None and (cooking != -100).any()) else logits_cook.sum() * 0
            parts["nutrition"] = nn.functional.smooth_l1_loss(pred_nut, nutrition)
            w = loss_weights
            result["loss"] = w[0] * parts["food_type"] + w[1] * parts["dish"] + w[2] * parts["cooking"] + w[3] * parts["nutrition"]
            result["loss_parts"] = {k: v.detach() for k, v in parts.items()}
        return result

    @torch.no_grad()
    def predict(self, pixel_values: torch.Tensor, topk: int = 3):
        """Prediksi siap pakai: label top-k + nilai nutrisi dalam satuan asli."""
        self.eval()
        out = self.forward(pixel_values)
        cfg = self.config
        mean = torch.tensor(cfg.nutrition_mean, device=pixel_values.device)
        std = torch.tensor(cfg.nutrition_std, device=pixel_values.device)
        nut = torch.expm1((out["nutrition_pred"] * std + mean).clamp(max=9.0)).clamp(min=0)

        def top(logits, labels):
            k = min(topk, logits.shape[-1])
            p = logits.softmax(-1)
            v, i = p.topk(k, dim=-1)
            return [[(labels[j], float(s)) for j, s in zip(ri.tolist(), rv.tolist())] for ri, rv in zip(i, v)]

        results = []
        food, dish, cook = (
            top(out["food_type_logits"], cfg.food_type_labels),
            top(out["dish_logits"], cfg.dish_labels),
            top(out["cooking_logits"], cfg.cooking_labels),
        )
        for b in range(pixel_values.shape[0]):
            results.append(
                {
                    "food_type": food[b],
                    "dish_name": dish[b],
                    "cooking_method": cook[b],
                    "nutrition": {k: round(float(v), 1) for k, v in zip(cfg.nutrition_keys, nut[b].tolist())},
                }
            )
        return results
