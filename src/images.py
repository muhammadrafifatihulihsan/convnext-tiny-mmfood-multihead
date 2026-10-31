"""Unduh gambar dari URL, cache ke Drive, dan pulihkan cache di sesi baru."""
import io
import os
import tarfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd
import requests
from PIL import Image
from tqdm.auto import tqdm


def download_one(url: str, path: str, max_side: int) -> bool:
    """Unduh satu gambar, perkecil (sisi terpanjang = max_side), simpan JPEG. True bila sukses."""
    if os.path.exists(path):  # sudah ada -> lewati (membuat unduhan bisa dilanjutkan)
        return True
    for _ in range(2):  # coba maksimal 2 kali
        try:
            r = requests.get(url, timeout=15)
            if r.status_code != 200:
                continue
            im = Image.open(io.BytesIO(r.content)).convert("RGB")
            im.thumbnail((max_side, max_side))
            im.save(path, "JPEG", quality=90)
            return True
        except Exception:
            time.sleep(0.5)
    return False


def download_all(df: pd.DataFrame, out_dir: str, max_side: int, workers: int) -> pd.Series:
    """Unduh paralel semua baris df (kolom: image_url, fname). Mengembalikan Series bool per fname."""
    os.makedirs(out_dir, exist_ok=True)
    status = {}
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(download_one, r.image_url, f"{out_dir}/{r.fname}", max_side): r.fname
                for r in df.itertuples()}
        for f in tqdm(as_completed(futs), total=len(futs), desc="Unduh gambar"):
            status[futs[f]] = f.result()
    return df["fname"].map(status)


def archive_images(local_dir: str, tar_path: str) -> None:
    """Arsipkan folder gambar lokal ke satu file .tar (disimpan di Drive)."""
    with tarfile.open(tar_path, "w") as t:
        t.add(local_dir, arcname=os.path.basename(local_dir))


def restore_images(local_dir: str, tar_path: str) -> int:
    """Pastikan gambar ada di disk lokal; bila belum, ekstrak dari arsip Drive. Return jumlah file."""
    have = len(os.listdir(local_dir)) if os.path.isdir(local_dir) else 0
    if have == 0:
        if not os.path.exists(tar_path):
            raise FileNotFoundError("Arsip gambar belum ada. Jalankan notebook 02 dulu.")
        with tarfile.open(tar_path) as t:
            t.extractall(os.path.dirname(local_dir))
        have = len(os.listdir(local_dir))
    return have
