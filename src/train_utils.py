"""Fungsi bantu training/evaluasi yang dipakai notebook 04, 05, 06."""
import json

import torch
from transformers import AutoConfig

from data_utils import NUTRITION_KEYS
from modeling_mmfood import MMFoodConfig, MMFoodMultiTask


def build_model(cfg: dict, labels: dict, device: str, pretrained_backbone: bool = True):
    """Bangun model multi-task dari konfigurasi + label map. Mengembalikan (model, model_cfg)."""
    bb_cfg = AutoConfig.from_pretrained(cfg["backbone_name"])
    hidden = getattr(bb_cfg, "hidden_size", None) or bb_cfg.hidden_sizes[-1]  # dimensi fitur backbone
    model_cfg = MMFoodConfig(
        backbone_name=cfg["backbone_name"], hidden_size=hidden, backbone_config=bb_cfg.to_dict(),
        food_type_labels=labels["food_type"], dish_labels=labels["dish_name"],
        cooking_labels=labels["cooking_method"], nutrition_keys=labels["nutrition_keys"],
        nutrition_mean=labels["nutrition_mean"], nutrition_std=labels["nutrition_std"],
    )
    model = MMFoodMultiTask(model_cfg, load_backbone_weights=pretrained_backbone).to(device)
    return model, model_cfg


def to_dev(batch: dict, device: str) -> dict:
    return {k: v.to(device, non_blocking=True) for k, v in batch.items()}


@torch.no_grad()
def evaluate(model, loader, labels: dict, cfg: dict, device: str) -> dict:
    """Hitung loss, akurasi 3 head klasifikasi, dan MAE nutrisi (satuan asli kkal/gram)."""
    model.eval()
    use_amp = device == "cuda"
    mean_t = torch.tensor(labels["nutrition_mean"], device=device, dtype=torch.float32)
    std_t = torch.tensor(labels["nutrition_std"], device=device, dtype=torch.float32)

    tot_loss, n = 0.0, 0
    c_food = c_cook = c_dish = n_dish = 0
    abs_err = torch.zeros(4, device=device)

    for b in loader:
        b = to_dev(b, device)
        with torch.autocast(device_type="cuda", dtype=torch.float16, enabled=use_amp):
            out = model(b["pixel_values"], b["food_type"], b["dish"], b["cooking"],
                        b["nutrition"], cfg["loss_weights"])
        bs = b["pixel_values"].size(0)
        tot_loss += out["loss"].item() * bs
        n += bs
        c_food += (out["food_type_logits"].argmax(1) == b["food_type"]).sum().item()
        c_cook += (out["cooking_logits"].argmax(1) == b["cooking"]).sum().item()
        m = b["dish"] != -100  # dish hanya dihitung pada baris yang punya label Top-K
        c_dish += (out["dish_logits"].argmax(1)[m] == b["dish"][m]).sum().item()
        n_dish += m.sum().item()
        # kembalikan nutrisi ke satuan asli: un-standardize -> expm1
        pred = torch.expm1((out["nutrition_pred"].float() * std_t + mean_t).clamp(max=9)).clamp(min=0)
        true = torch.expm1(b["nutrition"] * std_t + mean_t)
        abs_err += (pred - true).abs().sum(0)

    mae = (abs_err / n).tolist()
    return dict(loss=tot_loss / n, acc_food_type=c_food / n, acc_cooking=c_cook / n,
                acc_dish=c_dish / max(n_dish, 1),
                **{f"mae_{k}": v for k, v in zip(NUTRITION_KEYS, mae)})


def load_json(path: str):
    return json.load(open(path, encoding="utf-8"))
