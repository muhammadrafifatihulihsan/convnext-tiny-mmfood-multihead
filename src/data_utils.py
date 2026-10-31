"""Utilitas data: pembersihan label, normalisasi cooking_method, parsing nutrisi."""
import json
import re

import numpy as np
import pandas as pd

NUTRITION_KEYS = ["calories_kcal", "protein_g", "fat_g", "carbohydrate_g"]

# Aturan normalisasi metode masak (urutan penting: cocok pertama yang dipakai).
COOKING_RULES = [
    ("stir-fry", r"stir"),
    ("deep-fry", r"deep|crispy"),
    ("pan-fry", r"pan[- ]?fr"),
    ("fry", r"fr(y|ied|ying)"),
    ("steam", r"steam"),
    ("boil", r"boil|blanch|poach"),
    ("simmer-stew", r"stew|braise|braising|simmer|sauce|curry|soup|hot ?pot"),
    ("bake", r"bak(e|ed|ing)|roast|oven"),
    ("grill", r"grill|bbq|barbecue|char|skewer|broil"),
    ("raw", r"raw|fresh|none|no cook|uncooked|salad|cold|mix"),
]


def normalize_cooking(x) -> str:
    if not isinstance(x, str) or not x.strip():
        return "unknown"
    s = x.lower().strip()
    for name, pat in COOKING_RULES:
        if re.search(pat, s):
            return name
    return "other"


def normalize_dish(x):
    if not isinstance(x, str):
        return None
    s = re.sub(r"\s+", " ", x.strip().lower())
    return s or None


def parse_nutrition(s: str):
    try:
        d = json.loads(s)
        return [float(d[k]) for k in NUTRITION_KEYS]
    except Exception:
        return [np.nan] * 4


def prepare_dataframe(csv_path: str, top_k_dish: int = 50, min_food_prob: float = 0.5) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df = df[df["food_prob"] >= min_food_prob].copy()
    df["dish_norm"] = df["dish_name"].map(normalize_dish)
    df["cooking_norm"] = df["cooking_method"].map(normalize_cooking)

    nut = np.array([parse_nutrition(s) for s in df["nutritional_profile"]])
    for i, k in enumerate(NUTRITION_KEYS):
        df[k] = nut[:, i]
    df = df.dropna(subset=NUTRITION_KEYS)
    df = df[df["calories_kcal"] > 0]  # buang nilai kalori tidak masuk akal

    top = df["dish_norm"].value_counts().head(top_k_dish).index.tolist()
    df["dish_label"] = df["dish_norm"].where(df["dish_norm"].isin(top), other=None)
    return df.reset_index(drop=True)
