"""
Konfigurasi dan alokasi folder proyek (satu sumber kebenaran untuk SEMUA notebook).

Ada dua lokasi:
  1. REPO_DIR    : kode + dataset mentah (hasil unzip ke disk lokal Colab, /content)
  2. PROJECT_DIR : semua HASIL (di Google Drive supaya tidak hilang saat sesi Colab putus)

Struktur PROJECT_DIR (dibuat otomatis oleh get_paths()):

  mmfood-project/
  |- data/
  |   |- processed/       clean.csv, manifest.csv, train.csv, val.csv, test.csv
  |   |- image_cache/     images.tar  (arsip gambar yang sudah diunduh dan diperkecil)
  |- artifacts/           config.json, labels.json   (dipakai lintas notebook)
  |- checkpoints/         best.pt, last.pt           (training, bisa resume)
  |- reports/
  |   |- metrics/         history.json, test_metrics.json, eda_stats.json
  |   |- figures/         grafik EDA, kurva training, confusion matrix
  |- models/
  |   |- raw/             model versi belum standar HF (.pt)
  |   |- hf_export/       model versi standar HF (siap push)
  |- releases/            zip hasil akhir
"""
import json
import os
from types import SimpleNamespace

REPO_DIR = os.environ.get("MMFOOD_REPO", "/content/mmfood-multitask")
PROJECT_DIR = os.environ.get("MMFOOD_PROJECT", "/content/drive/MyDrive/mmfood-project")
LOCAL_IMAGE_DIR = "/content/images"  # gambar di disk lokal (cepat); arsipnya disimpan di Drive

# Nilai bawaan. Ubah lewat notebook 00 (disimpan ke artifacts/config.json).
DEFAULT_CFG = dict(
    # --- data ---
    backbone_name="facebook/convnext-tiny-224",  # backbone pretrained (ringan, cocok untuk T4)
    min_food_prob=0.5,       # buang baris yang kemungkinan bukan makanan
    top_k_dish=50,           # jumlah kelas nama hidangan
    min_per_cooking=150,     # metode masak yang jarang digabung ke 'other'
    n_attempt=36000,         # jumlah URL yang dicoba diunduh (sebagian link bisa mati)
    cache_size=256,          # sisi terpanjang gambar yang disimpan di disk (px)
    download_workers=32,     # jumlah thread unduh
    # --- training ---
    img_size=224,
    batch_size=64,
    epochs=6,
    lr_backbone=5e-5,
    lr_heads=1e-3,
    weight_decay=0.05,
    loss_weights=[1.0, 1.0, 0.5, 1.0],  # food_type, dish, cooking, nutrition
    num_workers=2,
    seed=42,
    # --- Hugging Face ---
    hf_username="GANTI_USERNAME_HF",
    model_name="convnext-tiny-mmfood-multitask",
    hf_private=True,
)


def get_paths(make_dirs: bool = True) -> SimpleNamespace:
    """Kembalikan semua path proyek; buat folder bila belum ada."""
    pr = PROJECT_DIR
    p = SimpleNamespace(
        repo=REPO_DIR,
        raw_csv=f"{REPO_DIR}/data/raw/MM-Food-100K.csv",
        project=pr,
        processed=f"{pr}/data/processed",
        image_cache=f"{pr}/data/image_cache",
        artifacts=f"{pr}/artifacts",
        checkpoints=f"{pr}/checkpoints",
        metrics=f"{pr}/reports/metrics",
        figures=f"{pr}/reports/figures",
        raw_model=f"{pr}/models/raw",
        hf_export=f"{pr}/models/hf_export",
        releases=f"{pr}/releases",
        local_images=LOCAL_IMAGE_DIR,
    )
    if make_dirs:
        for k, v in vars(p).items():
            if k not in ("repo", "raw_csv"):
                os.makedirs(v, exist_ok=True)
    return p


def load_cfg(p: SimpleNamespace) -> dict:
    """Muat konfigurasi: nilai bawaan ditimpa artifacts/config.json bila ada."""
    cfg = dict(DEFAULT_CFG)
    path = f"{p.artifacts}/config.json"
    if os.path.exists(path):
        cfg.update(json.load(open(path)))
    return cfg


def save_cfg(p: SimpleNamespace, cfg: dict) -> None:
    json.dump(cfg, open(f"{p.artifacts}/config.json", "w"), indent=2)
