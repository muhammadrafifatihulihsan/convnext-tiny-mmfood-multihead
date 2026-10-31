# Panduan mencoba model

[Dokumentasi](README.md) | [English](usage.md) | [Analisis](results.md)

## Membaca proses atau mencoba prediksi

Notebook 00?08 di GitHub memuat proses beserta seluruh output aslinya. Untuk mencoba model, unduh snapshot Hugging Face; dataset, checkpoint training, dan GPU tidak diperlukan. Izin penggunaan hanya untuk evaluasi pribadi nonkomersial sesuai [ketentuan](../LICENSE.md).

## Instalasi

Gunakan Python 3.10 dan environment terpisah: `python -m venv .venv`. Di PowerShell aktifkan dengan `.venv\Scripts\Activate.ps1`; Linux/macOS memakai `source .venv/bin/activate`. Jalankan perintah instalasi versi yang sudah diuji pada [panduan Inggris](usage.md#environment).

```python
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id="muhammadrafifatihulihsan/convnext-tiny-mmfood-multihead",
    local_dir="models/convnext-tiny-mmfood-multihead",
)
```

Bobot utama sekitar 112,3 MB. Snapshot lengkap menyertakan konfigurasi, label dan kode model. Untuk unduhan yang dapat ditelusuri, gunakan revision berisi SHA commit model. Repo publik dapat diunduh tanpa token.

## Menjalankan

Salin contoh lengkap predict_food.py dari [panduan inferensi](usage.md#predict-an-image), sediakan food.jpg, lalu jalankan `python predict_food.py`. Contoh memakai resize 255 bilinear, crop tengah 224 dan normalisasi ImageNet, sesuai evaluasi notebook. Processor bawaan ekspor berbeda sehingga tidak boleh dianggap identik.

Output berisi jenis makanan, nama hidangan, metode memasak dan empat nilai nutrisi. Skor klasifikasi bukan tingkat kepastian terkalibrasi. Hidangan di luar 50 kelas tetap dipetakan ke salah satu kelas yang dikenal. Nilai nutrisi bukan pengukuran porsi atau dasar keputusan kesehatan.

## Membaca angka dengan benar

Akurasi dish 79,21% hanya dihitung atas 856 gambar berlabel dari 3.600 gambar test. Audit byte gambar menemukan 281 gambar test identik dengan train (7,81%). Metrik historis dapat terlalu optimistis; proyek tidak diklaim sebagai benchmark bebas kebocoran. Detail baseline dan batas evaluasi ada di results.md.

Dokumentasi training menjelaskan eksperimen milik penulis, bukan pemberian izin fine-tuning, modifikasi atau redistribusi. Untuk mencoba model cukup ikuti jalur inferensi.
