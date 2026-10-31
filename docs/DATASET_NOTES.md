> Historical workflow reference. Current usage restrictions are in ../LICENSE.md; current model findings are in ../ANALYSIS.md. Example repository names below are not publication targets.

# Catatan Dataset MM-Food-100K

Hasil eksplorasi file `data/MM-Food-100K.csv` (100.000 baris, 10 kolom).

## Struktur kolom

| Kolom | Tipe | Catatan |
|---|---|---|
| `image_url` | string | URL gambar (host `file.b18a.io`); gambar tidak ada di CSV |
| `camera_or_phone_prob` | float | 0.6 - 0.9; mayoritas 0.7 dan 0.8 |
| `food_prob` | float | kemungkinan gambar berisi makanan |
| `dish_name` | string | 19.288 nilai unik, 2 kosong |
| `food_type` | string | 5 kelas |
| `ingredients` | string (list JSON) | belum dipakai |
| `portion_size` | string (list JSON) | belum dipakai |
| `nutritional_profile` | string (JSON) | `calories_kcal`, `protein_g`, `fat_g`, `carbohydrate_g` |
| `cooking_method` | string | 1.358 kosong, 2.264 nilai unik tidak konsisten |
| `sub_dt` | int | tanggal pengiriman (YYYYMMDD) |

## Distribusi `food_type`

| Kelas | Jumlah |
|---|---|
| Homemade food | 46.555 |
| Restaurant food | 35.461 |
| Raw vegetables and fruits | 9.357 |
| Packaged food | 8.354 |
| Others | 273 |

## Nutrisi (satuan asli)

| Nutrisi | Rata-rata | Std | Maks |
|---|---|---|---|
| Kalori (kkal) | 411 | 256 | 3.500 |
| Protein (g) | 21.4 | 18.1 | 250 |
| Lemak (g) | 17.6 | 15.0 | 250 |
| Karbohidrat (g) | 40.5 | 29.1 | 650 |

Distribusi condong ke kanan (ada nilai ekstrem), sehingga dipakai transformasi `log1p`.

## Keputusan pembersihan

| Masalah | Keputusan | Alasan |
|---|---|---|
| `dish_name` long-tail | Top-50 jadi kelas, sisanya `-100` (diabaikan loss dish) | Kelas dengan sedikit contoh tidak bisa dipelajari |
| `cooking_method` tidak konsisten | Normalisasi regex ke ~10 kelompok (`stir-fry`, `boil`, `bake`, ...) | `stir-frying`, `stir-fried`, `Stir-frying` artinya sama |
| Kalori <= 0 | Dibuang | Tidak masuk akal |
| `food_prob` < 0.5 | Dibuang | Kemungkinan bukan gambar makanan |
| Nutrisi skala lebar | `log1p` + standardisasi (statistik train) | Stabilitas training, mencegah kebocoran |

## Catatan kualitas

- Label berasal dari kombinasi anotasi manusia, GPT-4o, dan Qwen-max, lalu dikoreksi manusia (menurut README dataset). Anggap sebagai label "silver", bukan ground truth lab.
- Nilai nutrisi sering bulat (400, 350, 600), tanda estimasi kasar.
- `sub_dt` bisa dipakai untuk split berbasis waktu bila ingin menguji generalisasi; proyek ini memakai split acak stratified.

## Lisensi

OpenRAIL-M, non-komersial. Kontak: hello@codatta.io.
