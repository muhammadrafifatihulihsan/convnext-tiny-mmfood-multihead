> Historical workflow reference. Current usage restrictions are in ../LICENSE.md; current model findings are in ../ANALYSIS.md. Example repository names below are not publication targets.

# Panduan Penamaan dan Push Model ke Hugging Face Hub

Panduan ini dari pengetahuan saya tentang konvensi Hugging Face; fitur Hub bisa berubah, jadi cek https://huggingface.co/docs/hub jika ada yang berbeda.

## 1. Penamaan repo

Format repo model: **`username/nama-model`** (atau `nama-organisasi/nama-model`).

### Aturan teknis
- Karakter yang boleh: huruf, angka, `-`, `_`, `.`
- Tidak boleh diawali atau diakhiri `-` atau `.`
- Hindari `--` dan `..`
- Maksimal 96 karakter
- Hindari spasi dan karakter khusus

### Konvensi yang umum dipakai (bukan paksaan)
- **Huruf kecil semua**, kata dipisah `-`
- Pola: `{arsitektur/backbone}-{dataset}-{tugas}` atau `{backbone}-finetuned-{dataset}`
- Sertakan versi/ukuran jika ada varian: `-tiny`, `-base`, `-v2`
- Nama deskriptif tapi singkat; jangan memakai kata "model" atau "final"

### Contoh untuk proyek ini

| Status | Nama | Alasan |
|---|---|---|
| Disarankan | `username/convnext-tiny-mmfood-multitask` | backbone, dataset, tugas jelas |
| Baik | `username/mmfood-multitask-convnext-tiny` | alternatif urutan |
| Hindari | `username/Model Makanan Final!!` | spasi, simbol, huruf besar, tidak informatif |
| Hindari | `username/model1` | tidak menjelaskan apa-apa |

### Nama untuk dataset atau Space (jika nanti dibuat)
- Dataset: `username/mmfood-subset-30k`
- Space demo: `username/mmfood-demo`

## 2. Struktur file repo model yang standar

```
username/convnext-tiny-mmfood-multitask
|- README.md                  # model card (wajib dibaca orang), diawali YAML metadata
|- config.json                # konfigurasi model
|- model.safetensors          # bobot (format aman, disarankan dibanding .bin/.pt)
|- preprocessor_config.json   # konfigurasi pra-proses gambar
|- modeling_mmfood.py         # kode arsitektur kustom (karena bukan arsitektur bawaan transformers)
|- labels.json                # pemetaan label
|- raw/                       # (opsional) arsip versi non-standar
|- reports/                   # (opsional) metrik dan grafik
```

Catatan khusus model kustom: `config.json` memuat `auto_map` yang menunjuk ke `modeling_mmfood.py`. Pengguna harus memuat dengan `trust_remote_code=True`. Notebook 06 menangani ini lewat `register_for_auto_class()`.

## 3. Metadata YAML di README.md (model card)

Bagian paling atas `README.md` model diawali blok YAML. Hub memakainya untuk pencarian, filter, dan tampilan:

```yaml
---
license: openrail          # sesuaikan; lihat catatan lisensi di bawah
library_name: transformers
pipeline_tag: image-classification
tags:
  - food
  - multi-task
  - image-classification
  - nutrition-estimation
datasets:
  - Codatta/MM-Food-100K
base_model: facebook/convnext-tiny-224
metrics:
  - accuracy
  - mae
language:
  - en
---
```

Template lengkap ada di `MODEL_CARD_TEMPLATE.md`. Isi minimal model card yang baik:
1. Deskripsi singkat dan tugas model
2. Cara pakai (kode contoh)
3. Data latih dan proses (ukuran, split, hiperparameter)
4. Hasil evaluasi (dengan baseline pembanding)
5. **Keterbatasan dan bias**
6. Penggunaan yang tidak disarankan
7. Lisensi dan sitasi

### Catatan lisensi
Dataset MM-Food-100K berlisensi **OpenRAIL-M untuk penggunaan non-komersial**. Model yang dilatih darinya sebaiknya mencantumkan pembatasan yang sama. Backbone ConvNeXt punya lisensinya sendiri; cek halaman `facebook/convnext-tiny-224`. Jika ragu, tulis di model card bahwa pemakaian mengikuti ketentuan dataset dan backbone. Untuk kepastian hukum, hubungi pemilik dataset (hello@codatta.io, sesuai README dataset).

## 4. Cara push

### Persiapan
1. Buat akun di https://huggingface.co
2. Buat token di https://huggingface.co/settings/tokens, tipe **write** (atau fine-grained dengan izin write untuk repo ini)
3. Simpan token di tempat aman; jangan tulis di notebook atau commit ke Git

### Cara A - lewat notebook (yang dipakai proyek ini)
Notebook `07_push_to_huggingface.ipynb` sudah mengerjakan: validasi nama, `notebook_login()`, `create_repo`, lalu `upload_folder` untuk bagian standar, `raw/`, dan `reports/`, ditutup dengan tes muat dari Hub.

### Cara B - `push_to_hub` langsung dari objek model
```python
model.push_to_hub("username/convnext-tiny-mmfood-multitask", private=True)
processor.push_to_hub("username/convnext-tiny-mmfood-multitask", private=True)
```
Cara ini hanya mengunggah model dan processor. Model card, `labels.json`, dan kode kustom perlu dipastikan ikut (itulah alasan proyek ini memakai `upload_folder`).

### Cara C - lewat terminal
```bash
pip install -U huggingface_hub
huggingface-cli login
huggingface-cli upload username/convnext-tiny-mmfood-multitask ./hf_export . --repo-type model
huggingface-cli upload username/convnext-tiny-mmfood-multitask ./raw_model raw --repo-type model
```
Nama perintah CLI bisa berbeda antar versi `huggingface_hub`; cek `huggingface-cli --help`.

### Cara D - lewat Git (untuk file besar gunakan Git LFS)
```bash
git lfs install
git clone https://huggingface.co/username/convnext-tiny-mmfood-multitask
# salin file, lalu:
git add . && git commit -m "Add model" && git push
```

## 5. Checklist sebelum publikasi

- [ ] Nama repo huruf kecil, deskriptif, lolos validasi
- [ ] `private=True` saat pertama kali; ubah ke publik setelah dicek
- [ ] Model card dibaca ulang; angka cocok dengan `test_metrics.json`
- [ ] Ada baseline pembanding dan keterbatasan ditulis jujur
- [ ] Lisensi dan sitasi dataset dicantumkan
- [ ] Tes muat ulang dari Hub: `AutoModel.from_pretrained(repo, trust_remote_code=True)`
- [ ] Tidak ada token/rahasia di file yang diunggah
- [ ] Versi (tag/commit) dicatat di laporan agar bisa direproduksi

## 6. Versi dan pembaruan

- Setiap `upload_folder` membuat commit baru; riwayat tersimpan di tab *Files and versions*.
- Untuk versi besar buat tag: `api.create_tag(repo_id, tag="v1.0", repo_type="model")`.
- Pengguna bisa mengunci versi: `from_pretrained(repo, revision="v1.0")` atau hash commit.

## 7. Memperbaiki nama/lokasi

- Ganti nama atau pindah repo: `HfApi().move_repo(from_id, to_id)` (atau lewat Settings di web). Link lama otomatis mengalihkan, tapi sebaiknya tetap diperbarui di dokumentasi.
- Ubah publik/privat: `HfApi().update_repo_settings(repo_id, private=False)`.
