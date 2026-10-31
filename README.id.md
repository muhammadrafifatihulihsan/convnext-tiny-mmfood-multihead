# ConvNeXt-Tiny - MMFood Multihead

[English](README.md) | [Bahasa Indonesia](README.id.md)

<a id="overview"></a>

## Ringkasan

Eksperimen pemahaman makanan dari gambar saja: satu backbone ConvNeXt-Tiny memprediksi jenis makanan, nama hidangan, metode memasak, dan empat nilai nutrisi. Alurnya mencakup eksplorasi dataset, training, evaluasi, dan ekspor model. Sembilan notebook asli tetap menyimpan output eksekusinya.

[GitHub: kode dan notebook](https://github.com/muhammadrafifatihulihsan/convnext-tiny-mmfood-multihead) | [Hugging Face: file model](https://huggingface.co/muhammadrafifatihulihsan/convnext-tiny-mmfood-multihead)

| Properti | Nilai |
| --- | --- |
| Backbone | facebook/convnext-tiny-224 |
| Input | Foto makanan RGB, 224 x 224 setelah preprocessing |
| Kelas jenis makanan / hidangan / metode memasak | 5 / 50 / 11 |
| Nutrisi | Kalori (kcal), protein, lemak, karbohidrat (g) |
| Subset pelatihan | 28,798 train / 3,600 validation / 3,600 test |
| Epoch tercatat | 6 |
| Bobot utama | model.safetensors, 112.3 MB (107.1 MiB) |
| Pemuatan model | AutoModel dengan kode kustom yang perlu ditinjau |
| Izin | Evaluasi pribadi nonkomersial atas kontribusi penulis |

Ini model eksperimen, bukan layanan nutrisi produksi, alat medis, atau sistem pengukuran porsi terkalibrasi. Akses publik tidak membuat kontribusi penulis menjadi open source.

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

Tentukan revision dengan SHA commit dari halaman Files and versions di Hub agar unduhan dapat direproduksi. Unduhan publik tidak memerlukan token. Lihat [panduan penggunaan](docs/usage.id.md) untuk persiapan environment dan pemuatan offline.

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

<a id="results"></a>

## Hasil tercatat

| Tugas | Hasil test | Cakupan / baseline |
| --- | ---: | --- |
| Jenis makanan | 77.92% akurasi | 3,600 gambar |
| Hidangan | 79.21% akurasi | 856 gambar berlabel top-50 |
| Metode memasak | 65.50% akurasi | 3,600 gambar |
| Kalori | 95.68 kcal MAE | Baseline 190.06 kcal |
| Protein | 6.28 g MAE | Baseline 14.08 g |
| Lemak | 5.23 g MAE | Baseline 10.56 g |
| Karbohidrat | 13.26 g MAE | Baseline 23.47 g |

![Kurva pelatihan](reports/figures/training_curves.png)

Ini metrik tersimpan, bukan evaluasi baru. Akurasi hidangan hanya mencakup 23.78% contoh test. Baseline nutrisi adalah expm1(mean(log1p(train targets))), bukan rata-rata aritmetika dalam satuan asli.

Audit byte identik menemukan 431 kelompok lintas split yang melibatkan 1,715 gambar. Sebanyak 281 gambar test cocok dengan train (7.81%); validasi memiliki 263 kecocokan dengan train (7.31%). Ini dapat menaikkan skor. Tidak ada klaim benchmark yang sudah dikoreksi dari kebocoran.

![Confusion matrix jenis makanan](reports/figures/confusion_food_type.png)

Lihat [hasil dan analisis lengkap](docs/results.id.md) serta [JSON audit](reports/metrics/publication_audit.json).

<a id="interpretation"></a>

## Mengapa performanya terbatas

Model melampaui prediksi konstan kelas mayoritas train: 46.58% jenis makanan, 10.05% hidangan pada gambar yang memenuhi syarat, dan 18.28% metode memasak. Ini menunjukkan sinyal yang dipelajari pada split tersebut, bukan generalisasi andal pada foto independen.

Asal makanan dan metode memasak dapat ambigu secara visual. Cakupan hidangan terbatas; kelas kecil memiliki sedikit supervisi. Nutrisi bergantung pada porsi dan bahan tersembunyi yang tidak diukur oleh gambar. Label sumber mencakup estimasi berbantuan model, bukan pengukuran laboratorium.

Crop dapat menghilangkan informasi makanan sambil tetap memakai target nutrisi gambar utuh. Fitur bersama dapat membantu atau bersaing antar-tugas. Ini mekanisme yang masuk akal, bukan penyebab terisolasi yang terbukti melalui ablation. Enam epoch atau backbone kecil tidak boleh disalahkan tanpa perbandingan.

MAE 95.68 kcal adalah rata-rata error absolut terhadap anotasi, bukan error maksimum atau persentase akurasi. Kebocoran dapat membuat skor terlalu optimistis, bukan menjelaskan skor rendah. Perbedaan processor memengaruhi perbandingan jalur inferensi, bukan evaluasi notebook yang sudah tercatat. Prioritaskan split independen, preprocessing konsisten, dan analisis per kelas/error sebelum mengklaim manfaat model lebih besar atau training lebih lama. Lihat [penjelasan lengkap](docs/results.id.md).

<a id="architecture"></a>

## Arsitektur

```text
RGB image -> preprocessing -> ConvNeXt-Tiny -> pooled features (768)
                                         -> food_type_head
                                         -> dish_head
                                         -> cooking_head
                                         -> nutrition_head -> inverse log transform
```

Tiga head klasifikasi linear berbagi encoder; MLP nutrisi memakai 768 -> 256 -> 4 dengan GELU dan dropout. Dropout head adalah 0.2. Klasifikasi memakai cross entropy, dengan label dish -100 diabaikan; nutrisi memakai Smooth L1. Loss gabungan adalah food + dish + 0.5 * cooking + nutrition.

Target nutrisi adalah z = (log1p(y) - mean_train) / std_train. Prediksi memakai expm1(clamp(z * std_train + mean_train, max=9)), lalu membatasi hasil agar tidak negatif. Ini pilihan implementasi, bukan jaminan fisiologis. [Arsitektur dan modul](docs/project.md).

<a id="data-training"></a>

## Data dan pelatihan tercatat

Sumber memiliki 100,000 baris metadata; pembersihan menyisakan 99,949. Dari 36,000 percobaan unduhan, 35,998 masuk eksperimen. Split distratifikasi menurut jenis makanan dengan seed 42. Kosakata hidangan memakai frekuensi top-50 dari seluruh data bersih sebelum split. Label metode memasak memakai aturan kata kunci berurutan dan penggabungan berdasarkan frekuensi train. Normalisasi nutrisi hanya memakai statistik train; kolom bahan dan porsi bukan input.

| Pengaturan | Nilai |
| --- | --- |
| Batch / epoch | 64 / 6 |
| Learning rate backbone / head | 5e-5 / 1e-3 |
| Optimizer / weight decay | AdamW / 0.05 |
| Jadwal | Warmup linear 5% lalu cosine |
| Gradient clipping | Norma maksimum 1.0 |
| Checkpoint terbaik | Loss validasi terendah |

Kelas Others hanya memiliki 77 gambar train dan 10 test. Sisi terpanjang cache gambar adalah 256; training memakai random crop, flip, dan color jitter. Training CUDA memakai autocast float16 dan GradScaler. Resume tidak menyimpan state scaler/RNG. Eksperimen penuh tidak dijalankan ulang selama pekerjaan dokumentasi. [Persiapan data](docs/data.md) dan [proses training](docs/training.md).

<a id="notebooks"></a>

## Telusuri notebook

```text
00 Setup -> 01 EDA -> 02 Image cache -> 03 Splits and labels
         -> 04 Training -> 05 Evaluation -> 06 Export
         -> 07 Hub publication -> 08 Results packaging
```

[Baca sembilan notebook beserta output di GitHub](https://github.com/muhammadrafifatihulihsan/convnext-tiny-mmfood-multihead/tree/main/notebooks). Byte kode asli, bobot, dan output notebook dipertahankan. Path internal Colab historis memakai mmfood-multitask, sedangkan repo publik memakai convnext-tiny-mmfood-multihead. [Panduan training](docs/training.md) menjelaskan kebutuhan bootstrap dan perilaku upload asli.

Membaca output tidak memerlukan training. Izin evaluasi saja tidak memberikan hak modifikasi atau fine-tuning.

<a id="files"></a>

## Lokasi file

| Lokasi | Isi |
| --- | --- |
| GitHub: src/, notebooks/, artifacts/ | Kode, alur yang sudah dieksekusi, dan pengaturan eksperimen tersimpan |
| Hugging Face: model.safetensors | Bobot inferensi |
| Hugging Face: config.json, modeling_mmfood.py | Konfigurasi backbone/head, pemetaan AutoClass, dan implementasi kustom |
| Hugging Face: labels.json, preprocessor_config.json | Pemetaan label/statistik dan processor ekspor asli |
| Hugging Face: raw/ | Arsip historis yang dipertahankan, opsional saat mengunduh |
| Keduanya: docs/, reports/, licenses/ | Panduan, metrik, audit, gambar, dan lisensi sumber |
| Keduanya: VALIDATION.md, SHA256SUMS.txt | Cakupan validasi dan checksum paket kurasi |

Kedua paket kurasi tidak memuat CSV dataset, cache gambar, atau checkpoint optimizer. HF mempertahankan arsip inferensi raw yang sudah ada; arsip ini tidak disalin ulang ke folder kurasi lokal. File arsip berada di luar manifest checksum folder tersebut. Gambar contoh pada laporan tetap mengikuti hak dataset.

<a id="documentation"></a>

## Dokumentasi dan validasi

| Panduan | Isi |
| --- | --- |
| [Penggunaan](docs/usage.id.md) / [English](docs/usage.md) | Setup, unduhan, prediksi, dan arti output |
| [Hasil](docs/results.id.md) / [English](docs/results.md) | Baseline, error, kebocoran, dan prioritas investigasi |
| [Proyek](docs/project.md) | Arsitektur dan modul |
| [Data](docs/data.md) | Pembersihan, sampling, kosakata, dan ketimpangan |
| [Training](docs/training.md) | Kebutuhan notebook dan hiperparameter |
| [Troubleshooting](docs/troubleshooting.md) | Environment, pemuatan, dan autentikasi |
| [Publikasi](docs/publishing.md) | Proses rilis penulis dan kebijakan tag |
| [Atribusi](docs/attribution.md) | Sumber dan sitasi |

[Validasi](VALIDATION.md) mencatat pemeriksaan yang benar-benar dilakukan. Unduhan model publik, verifikasi checksum, dan eksekusi CPU telah diuji; ini bukan evaluasi akurasi baru. Laporan asli dipertahankan. Baseline dan audit overlap saat publikasi ditandai secara terpisah. Pasangan README, panduan penggunaan, dan hasil mempunyai cakupan Inggris/Indonesia setara; panduan teknis lainnya saat ini memakai bahasa Inggris.

<a id="terms"></a>

## Ketentuan dan kredit

Kontribusi asli penulis hanya mengizinkan evaluasi pribadi nonkomersial. Tidak diberikan izin modifikasi, fine-tuning, redistribusi, atau integrasi produk. Hak pihak ketiga dan hak yang diwajibkan platform tetap berlaku. Lihat [ketentuan](LICENSE.md) dan [pemberitahuan pihak ketiga](THIRD_PARTY_NOTICES.md).

Penulis: [muhammadrafifatihulihsan](https://github.com/muhammadrafifatihulihsan). Sumber: [MM-Food-100K](https://huggingface.co/datasets/Humanbased-AI/MM-Food-100K), [laporan dataset](https://arxiv.org/abs/2508.10429), [riset ConvNeXt](https://arxiv.org/abs/2201.03545), dan [backbone](https://huggingface.co/facebook/convnext-tiny-224). Kartu dataset menyatakan ketentuan OpenRAIL-M nonkomersial; backbone memakai Apache-2.0. Cantumkan revisi kode/model yang tepat bersama karya sumber saat mengutip. Tidak ada klaim DOI proyek.
