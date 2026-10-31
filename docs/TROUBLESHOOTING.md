> Historical workflow reference. Current usage restrictions are in ../LICENSE.md; current model findings are in ../ANALYSIS.md. Example repository names below are not publication targets.

# Troubleshooting di Colab

| Gejala | Penyebab umum | Solusi |
|---|---|---|
| `FileNotFoundError` saat unzip | Lokasi zip di Drive berbeda | Ubah `ZIP_ON_DRIVE` di sel *Bootstrap* (sel kode pertama) notebook tersebut |
| `CUDA tersedia: False` | GPU belum diaktifkan | `Runtime > Change runtime type > T4 GPU`, lalu jalankan ulang notebook dari atas |
| Unduhan gambar banyak gagal | Link mati, atau host membatasi permintaan | Normal bila sebagian gagal. Jika >50% gagal, ubah `download_workers` di notebook 00 menjadi 8-16, lalu jalankan ulang notebook 02 |
| Sesi putus saat mengunduh | Batas waktu Colab | Jalankan ulang notebook 02; gambar yang sudah ada dilewati. Arsip Drive baru dibuat setelah unduhan selesai |
| `CUDA out of memory` | Batch terlalu besar | Ubah `batch_size` jadi 32 atau 16 di notebook 00, lalu jalankan ulang notebook 04 |
| Training sangat lambat | `num_workers` kecil atau CPU lambat | Coba `num_workers=4`; pastikan GPU aktif |
| Sesi putus saat training | Batas Colab | Jalankan ulang notebook 04 dari atas; resume otomatis dari `last.pt` |
| `ModuleNotFoundError: modeling_mmfood` | `sys.path` belum diatur | Jalankan sel *Bootstrap* (sel kode pertama) lebih dulu |
| Akurasi `dish_name` rendah | Banyak nama mirip (mis. "noodle soup" vs "beef noodle soup") | Wajar; pertimbangkan menggabung kelas mirip atau melaporkan top-3 accuracy |
| MAE nutrisi hampir sama dengan baseline | Label nutrisi kasar/dibulatkan | Wajar; tulis di laporan sebagai keterbatasan data |
| `trust_remote_code` error saat muat | `modeling_mmfood.py` tidak ikut ke folder export | Pastikan notebook 06 (Langkah 6.3) dijalankan penuh (ada `register_for_auto_class`) |
| 401/403 saat push | Token salah atau hanya read | Buat token **write** baru lalu `notebook_login()` ulang |
| 404 saat push | `hf_username` salah | Samakan dengan username di profil HF |
| Nama repo ditolak | Karakter tidak valid | Lihat Langkah 7.1 notebook 07 dan panduan penamaan |
| `FileNotFoundError: Arsip gambar belum ada` | Notebook 02 belum selesai | Jalankan notebook 02 sampai tuntas sebelum 04-06 |
| `FileNotFoundError ... labels.json` / `train.csv` | Notebook sebelumnya belum dijalankan | Jalankan berurutan 00 -> 08 |
| `The least populated classes ... Others` saat split | Terlalu sedikit gambar *Others* yang berhasil diunduh | Naikkan `n_attempt` di notebook 00 lalu ulangi 02 dan 03 |

## Mengurangi beban

Untuk uji cepat (10-15 menit): `n_attempt=8000`, `epochs=2` (ubah di notebook 00). Setelah alur lancar, naikkan lagi.
