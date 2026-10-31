# Unduh dan jalankan model

[English](usage.md) | [Bahasa Indonesia](usage.id.md) | [Documentation](README.md)

<a id="download"></a>

## Unduh model

Unduh paket inferensi lengkap yang menyertakan bobot, konfigurasi, label, dan kode model kustom. Tidak perlu menjalankan training, menyediakan dataset, atau memakai GPU untuk mencoba inferensi CPU.

```python
from huggingface_hub import snapshot_download
folder = snapshot_download(
    repo_id="muhammadrafifatihulihsan/convnext-tiny-mmfood-multihead",
    local_dir="models/convnext-tiny-mmfood-multihead",
    ignore_patterns=["raw/**"],
)
print(folder)
```

Arsip raw/ yang sudah ada di Hub berisi checkpoint historis tambahan sekitar 112.4 MB. Contoh mengecualikannya karena inferensi safetensors tidak memerlukannya. Hapus ignore_patterns hanya jika Anda juga menginginkan arsip tersebut. Laporan dan kode menambah ukuran di luar bobot utama. ZIP GitHub tidak menyertakan bobot model.

Tentukan revision dengan SHA commit dari halaman Files and versions di Hub agar unduhan dapat direproduksi. Unduhan publik tidak memerlukan token. Lihat [panduan penggunaan](usage.id.md) untuk persiapan environment dan pemuatan offline.

<a id="inference"></a>

## Jalankan satu gambar

Environment yang diuji adalah Python 3.10 di Windows dengan inferensi CPU. Buat virtual environment, aktifkan, lalu instal versi yang tercatat berhasil:

```bash
python -m venv .venv
```

Aktifkan dengan `.venv\Scripts\Activate.ps1` di PowerShell, `source .venv/bin/activate` di Linux/macOS, atau `source .venv/Scripts/activate` di Windows Git Bash.

```bash
python -m pip install torch==2.14.1 torchvision==0.29.2 transformers==5.20.2 safetensors==0.8.0 pillow==12.3.0 huggingface_hub==2.4.0
```

Setelah mengunduh, simpan contoh berikut sebagai predict_food.py di samping food.jpg dan jalankan `python predict_food.py`:

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

Tinjau modeling_mmfood.py sebelum mengaktifkan trust_remote_code. Model kustom ini tidak menjanjikan kompatibilitas dengan pipeline image-classification generik. Versi yang ditentukan mencatat satu environment teruji, bukan semua kombinasi OS/GPU.

Contoh mengikuti evaluasi historis: Resize(255) bilinear, CenterCrop(224), dan normalisasi ImageNet. Processor ekspor yang dipertahankan memakai bicubic dan crop_pct=0.875, sehingga tidak diganti secara diam-diam dalam contoh. Metrik historis tidak boleh dianggap identik pada kedua jalur tersebut.

<a id="outputs"></a>

## Memahami output

| Key | Arti |
| --- | --- |
| food_type | Pasangan label/skor softmax top-k untuk konteks makanan |
| dish_name | Pasangan top-k dari kosakata hidangan tetap |
| cooking_method | Pasangan top-k untuk label metode memasak ternormalisasi |
| nutrition | calories_kcal, protein_g, fat_g, carbohydrate_g |

predict() menghasilkan satu dictionary per gambar. Gunakan topk positif, biasanya 1-3; tiap head membatasinya sesuai jumlah kelas. Nutrisi dikembalikan dari ruang log1p terstandardisasi, dibatasi agar tidak negatif, dan dibulatkan satu desimal. Nilainya tidak dinyatakan secara eksplisit per 100 g. Output tingkat rendah nutrition_pred masih berada di ruang log terstandardisasi.

Skor softmax bukan kepastian terkalibrasi. Hidangan tidak dikenal tidak ditolak: prediksi tetap memilih label yang dikenal. Untuk CUDA, pindahkan model dan input ke perangkat yang sama. Tidak ada klaim benchmark latensi atau memori.

<a id="permission"></a>

## Izin penggunaan

Hanya evaluasi pribadi nonkomersial; lihat [ketentuan](../LICENSE.md). Panduan ini menunjukkan inferensi, bukan izin memodifikasi atau melakukan fine-tuning model. [Validasi](../VALIDATION.md) mencatat cakupan yang diuji.
