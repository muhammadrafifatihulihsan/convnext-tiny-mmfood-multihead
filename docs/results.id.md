# Mengapa hasil model masih terbatas?

[README](../README.id.md) | [Analisis dan tabel lengkap](results.md) | [Dataset](data.md)

## Apakah hasilnya buruk?

Untuk percobaan pembelajaran, model sudah menunjukkan sinyal yang berguna. Untuk dipakai sebagai pengenal makanan umum atau penghitung nutrisi yang andal, bukti yang tersedia belum cukup. Jadi kesimpulan yang tepat adalah **model eksperimen dengan keterbatasan nyata**, bukan gagal total dan bukan siap produksi. Proyek ini belum menetapkan ambang kelayakan atau pembanding eksternal yang independen.

Sebagai pembanding baru, pilih kelas yang paling sering muncul di train, lalu tebak kelas tersebut untuk seluruh gambar test yang memenuhi syarat:

| Tugas | Tebakan kelas mayoritas train | Model tercatat |
| --- | ---: | ---: |
| Jenis/konteks makanan | 46,58% | 77,92% |
| Hidangan, subset top-50 | 10,05% | 79,21% |
| Metode memasak | 18,28% | 65,50% |

Model jelas lebih baik daripada tebakan konstan itu. Namun pembanding ini bukan model terlatih lain dan masih memakai split yang memiliki duplikasi. Angka tersebut tidak membuktikan generalisasi pada gambar baru yang independen.

MAE kalori 95,68 kkal berarti rata-rata selisih absolut sekitar 96 kkal terhadap label dataset. Bukan akurasi 95,68%, bukan batas kesalahan maksimum, dan bukan jaminan bahwa setiap prediksi hanya meleset sebesar itu. Sebagian kesalahan dapat jauh lebih besar. Distribusi error ekstrem dan error per kelompok belum dilaporkan.

## 1. Jenis makanan tidak selalu terlihat dari foto

Label seperti Homemade food dan Restaurant food menjelaskan konteks asal makanan. Hidangan yang tampak sama dapat dibuat di rumah atau disajikan restoran. Model hanya menerima foto/crop makanan, bukan informasi tempat dan pembuatnya. Karena itu, ambiguitas konteks merupakan penjelasan yang masuk akal, tetapi besarnya pengaruh belum diukur melalui analisis kesalahan individual.

Ketimpangan kelas juga nyata: Others hanya memiliki 77 contoh train dan 10 contoh test, sedangkan Homemade food memiliki 13.413 contoh train. Data sedikit dapat menyulitkan pembelajaran kelas kecil; sepuluh contoh test pun belum cukup untuk estimasi performa yang stabil. Akurasi total dapat terlihat cukup tinggi sambil menyembunyikan kelemahan pada kelas kecil.

## 2. Akurasi hidangan tinggi, tetapi cakupannya sempit

Model hanya mengenal 50 nama hidangan. Dari 28.798 gambar train, hanya 6.464 yang memberikan label dish valid. Akurasi 79,21% dihitung pada 856 gambar test berlabel dari total 3.600 (23,78%). Sisanya tidak digunakan dalam perhitungan akurasi dish tersebut.

Karena tidak mempunyai detektor kelas tidak dikenal, model tetap memilih nama dari 50 kelas saat menerima hidangan lain. Jadi skor pada subset yang dikenal tidak bisa dipakai sebagai akurasi pengenalan semua makanan. Keterbatasan cakupan ini lebih mendasar daripada sekadar menaikkan skor beberapa persen.

## 3. Metode memasak dapat ambigu dan labelnya disederhanakan

Sebanyak 2.264 nilai mentah metode memasak dinormalisasi melalui aturan kata kunci, lalu kelas jarang digabung. Hasilnya 11 kelas. Metode campuran dapat kehilangan informasi ketika dipaksa menjadi satu label. Makanan rebus, kukus atau stew juga dapat memiliki tampilan yang mirip.

Itu mekanisme yang mungkin menyulitkan klasifikasi, bukan hasil pengukuran sebab-akibat. Untuk memastikan penyebab error 34,50% pada head ini, perlu melihat pasangan gambar, label dan prediksi yang salah; dokumentasi tidak mengarang contoh kegagalan yang belum diperiksa.

## 4. Nutrisi tidak ditentukan oleh tampilan saja

Foto tidak selalu menunjukkan berat porsi, minyak, gula, bahan tersembunyi atau resep. Kolom ingredients dan portion_size tersedia pada sumber, tetapi tidak digunakan oleh model. Label nutrisi juga merupakan anotasi/estimasi yang dibantu model AI, bukan pengukuran laboratorium.

Dengan input terbatas ini, dua foto mirip dapat memiliki nilai nutrisi berbeda. Mengungguli baseline konstan menunjukkan hubungan yang dipelajari pada data tersebut, bukan bahwa model mampu mengukur nutrisi sebenarnya. Tidak ada dasar untuk menentukan batas akurasi maksimum akibat kualitas label tanpa pengukuran tambahan.

## 5. Crop dan pembagian kapasitas model perlu diuji

Gambar cache diperkecil hingga sisi terpanjang 256 piksel, lalu model menerima crop 224. Detail kecil atau bagian porsi dapat hilang. Random crop saat training tetap memakai target nutrisi gambar utuh; ini berpotensi menimbulkan ketidakcocokan antara potongan gambar dan label total makanan.

Satu backbone juga melayani empat head dengan bobot loss tetap. Berbagi fitur dapat membantu atau menimbulkan konflik antar-tugas. Belum ada ablation untuk membandingkan model satu tugas, bobot loss, resolusi atau crop. Karena itu, jangan menyatakan ConvNeXt-Tiny pasti terlalu kecil atau multi-task pasti menurunkan performa.

## 6. Enam epoch bukan penyebab yang sudah terbukti

Loss train turun dari 3,709 ke 1,245; loss validasi dari 2,343 ke 1,850. Di akhir, perbaikan validasi mengecil tetapi belum berhenti sepenuhnya. Ini belum membuktikan bahwa sekadar menambah epoch akan memperbaiki hasil.

Loss train dan validasi berasal dari data serta perilaku augmentasi/dropout berbeda. Selisih keduanya bukan bukti tunggal overfitting. Diperlukan eksperimen terkontrol untuk membedakan keterbatasan data, optimisasi dan kapasitas model.

## 7. Duplikasi justru dapat membuat hasil terlalu bagus

Audit menemukan 281 gambar test identik dengan train (7,81%) serta 263 gambar validasi identik dengan train. Kebocoran ini merusak independensi evaluasi dan berpotensi menaikkan skor. **Duplikasi bukan alasan skor rendah.** Hasil pada test yang benar-benar independen dapat berbeda, tetapi tidak bisa dihitung dengan mengurangi 7,81% dari akurasi.

Processor ekspor juga berbeda dari transformasi evaluasi. Ini dapat menjelaskan perbedaan prediksi ketika memakai processor ekspor, tetapi bukan penjelasan error historis yang dihitung memakai transformasi notebook. Contoh inferensi yang didokumentasikan sudah mengikuti transformasi historis.

## Prioritas perbaikan yang masuk akal

Untuk versi baru yang diizinkan penulis, urutannya adalah:

1. Kelompokkan gambar identik/nyaris identik sebelum split, tentukan label hanya dari train, dan samakan preprocessing evaluasi/inferensi.
2. Ukur kembali pada sumber gambar independen; tampilkan macro-F1, recall per kelas, cakupan top-k hidangan dan distribusi error nutrisi, bukan akurasi total saja.
3. Periksa kesalahan aktual serta kualitas label; bandingkan nutrisi dengan baseline median train yang relevan untuk MAE.
4. Uji satu perubahan pada satu waktu: keseimbangan kelas, crop yang menjaga seluruh porsi, bobot loss, model satu tugas, durasi training atau backbone lebih besar.
5. Pertimbangkan informasi porsi/bahan jika tujuan berubah menjadi estimasi nutrisi yang lebih presisi; itu membutuhkan desain data/input baru.

Daftar ini adalah rencana investigasi, bukan janji peningkatan. Bobot, kode dan metrik historis tetap dipertahankan; tidak ada pelatihan ulang dalam pembaruan dokumentasi ini.
