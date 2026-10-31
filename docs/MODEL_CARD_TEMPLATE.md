> Historical workflow reference. Current usage restrictions are in ../LICENSE.md; current model findings are in ../ANALYSIS.md. Example repository names below are not publication targets.

---
license: openrail
library_name: transformers
pipeline_tag: image-classification
base_model: {{BACKBONE}}
datasets:
  - Codatta/MM-Food-100K
tags:
  - food
  - multi-task
  - image-classification
  - nutrition-estimation
metrics:
  - accuracy
  - mae
language:
  - en
---

# {{REPO_ID}}

Model multi-task yang menerima **satu foto makanan** dan memprediksi: jenis makanan (`food_type`), nama hidangan (Top-{{TOP_K}}), metode masak, serta estimasi nutrisi (kalori, protein, lemak, karbohidrat).

> Proyek pembelajaran/penelitian. **Bukan** alat medis atau gizi. Estimasi nutrisi dari satu foto kasar dan tidak boleh dipakai untuk keputusan kesehatan.

## Cara pakai

```python
import torch
from PIL import Image
from transformers import AutoModel, AutoImageProcessor

repo = "{{REPO_ID}}"
model = AutoModel.from_pretrained(repo, trust_remote_code=True).eval()
processor = AutoImageProcessor.from_pretrained(repo)

img = Image.open("makanan.jpg").convert("RGB")
x = processor(img, return_tensors="pt")["pixel_values"]
print(model.predict(x, topk=3)[0])
```

`trust_remote_code=True` diperlukan karena arsitektur kustom (`modeling_mmfood.py` ada di repo ini). Disarankan menyematkan `revision="<commit>"`.

Output contoh:
```json
{"food_type": [["Restaurant food", 0.71], ...],
 "dish_name": [["noodle soup", 0.32], ...],
 "cooking_method": [["boil", 0.45], ...],
 "nutrition": {"calories_kcal": 420.0, "protein_g": 22.0, "fat_g": 15.0, "carbohydrate_g": 50.0}}
```

## Arsitektur

Backbone `{{BACKBONE}}` (pretrained) + 4 head: tiga klasifikasi dan satu regresi (4 nilai nutrisi dalam ruang `log1p` yang distandarisasi, dikembalikan ke satuan asli saat `predict`).

## Data latih

- Sumber: MM-Food-100K (Codatta), subset yang berhasil diunduh dari URL gambar.
- Split stratified berdasarkan `food_type`: train {{N_TRAIN}} / val {{N_VAL}} / test {{N_TEST}}.
- `dish_name`: {{TOP_K}} nama teratas dipakai sebagai kelas; baris lain tidak dihitung pada loss dish.
- `cooking_method`: dinormalisasi dengan aturan kata kunci, kelas jarang digabung ke `other`.
- Nutrisi: `log1p` lalu standardisasi (statistik dari train).

## Pelatihan

| Hiperparameter | Nilai |
|---|---|
| Epoch | {{EPOCHS}} |
| Batch size | {{BATCH}} |
| LR backbone / head | {{LR_BB}} / {{LR_HEAD}} |
| Optimizer | AdamW, cosine schedule + warmup, mixed precision |

## Hasil (test set)

| Metrik | Nilai |
|---|---|
| Akurasi `food_type` | {{ACC_FOOD}} |
| Akurasi `dish_name` (baris Top-{{TOP_K}}) | {{ACC_DISH}} |
| Akurasi `cooking_method` | {{ACC_COOK}} |

MAE nutrisi dibandingkan baseline "tebak rata-rata train":

| Nutrisi | MAE model | MAE baseline |
|---|---|---|
| Kalori (kkal) | {{MAE_CAL}} | {{BASE_CAL}} |
| Protein (g) | {{MAE_PRO}} | {{BASE_PRO}} |
| Lemak (g) | {{MAE_FAT}} | {{BASE_FAT}} |
| Karbohidrat (g) | {{MAE_CARB}} | {{BASE_CARB}} |

Metrik lengkap, kurva training, dan confusion matrix ada di folder `reports/`.

## Keterbatasan dan bias

- Label nutrisi berasal dari anotasi model AI yang dikoreksi manusia, bukan pengukuran laboratorium; banyak nilai tampak dibulatkan.
- Estimasi porsi dari satu foto tidak akurat; hasil nutrisi hanya perkiraan kasar.
- Kelas `Others` sangat sedikit sehingga hasilnya tidak dapat diandalkan.
- Data didominasi makanan Asia dan foto dari kontributor kampanye tertentu; performa pada masakan lain belum teruji.
- Hanya sebagian URL yang berhasil diunduh; subset bisa bias terhadap gambar yang masih tersedia.
- Hanya {{TOP_K}} nama hidangan teratas yang dikenali; hidangan lain akan dipetakan ke kelas terdekat.

## Penggunaan yang tidak disarankan

Diagnosis atau manajemen penyakit (mis. diabetes), keputusan diet medis, serta penggunaan komersial (lihat lisensi).

## Lisensi

Dataset sumber berlisensi **OpenRAIL-M untuk penggunaan non-komersial**; penggunaan model ini mengikuti ketentuan tersebut serta lisensi backbone. Untuk penggunaan komersial, hubungi pemilik dataset (hello@codatta.io).

## Sitasi

- MM-Food-100K: A 100,000-Sample Multimodal Food Intelligence Dataset with Verifiable Provenance. https://huggingface.co/papers/2508.10429
- Backbone: {{BACKBONE}}
