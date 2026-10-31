"""Dataset PyTorch + transformasi gambar untuk MM-Food."""
import pandas as pd
import torch
from PIL import Image
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms as T

from data_utils import NUTRITION_KEYS


def get_transforms(mean, std, size: int):
    """Augmentasi untuk train; resize + center-crop untuk val/test."""
    train_tf = T.Compose([
        T.RandomResizedCrop(size, scale=(0.6, 1.0)),  # potong acak -> model tahan variasi framing
        T.RandomHorizontalFlip(),                      # cermin kiri-kanan
        T.ColorJitter(0.2, 0.2, 0.2),                  # variasi cahaya/kontras/saturasi
        T.ToTensor(),
        T.Normalize(mean, std),                        # normalisasi sesuai backbone
    ])
    eval_tf = T.Compose([
        T.Resize(int(size * 1.14)),
        T.CenterCrop(size),
        T.ToTensor(),
        T.Normalize(mean, std),
    ])
    return train_tf, eval_tf


class FoodDS(Dataset):
    """Satu item = gambar + 3 label kelas + 4 target nutrisi (sudah distandarisasi, kolom z_*)."""

    def __init__(self, df: pd.DataFrame, img_dir: str, tf):
        self.df, self.img_dir, self.tf = df.reset_index(drop=True), img_dir, tf

    def __len__(self):
        return len(self.df)

    def __getitem__(self, i):
        r = self.df.iloc[i]
        img = self.tf(Image.open(f"{self.img_dir}/{r.fname}").convert("RGB"))
        nut = torch.tensor([r[f"z_{k}"] for k in NUTRITION_KEYS], dtype=torch.float32)
        return dict(pixel_values=img, food_type=int(r.y_food), dish=int(r.y_dish),
                    cooking=int(r.y_cook), nutrition=nut)


def make_loader(df, img_dir, tf, batch_size, shuffle, num_workers):
    return DataLoader(FoodDS(df, img_dir, tf), batch_size=batch_size, shuffle=shuffle,
                      num_workers=num_workers, pin_memory=True, drop_last=shuffle)
