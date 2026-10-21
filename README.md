# Peta Banjir Jakarta per Kelurahan

Peta interaktif yang menunjukkan seberapa sering tiap kelurahan di DKI Jakarta kebanjiran selama 2013 sampai 2020, berdasarkan catatan BPBD DKI Jakarta.

**Lihat peta:** buka `index.html` di browser, atau lewat GitHub Pages kalau sudah diaktifkan.

## Isi peta

- 262 kelurahan di daratan Jakarta (Kepulauan Seribu tidak ditampilkan)
- Warna = jumlah catatan banjir 2013 sampai 2020, dibagi 5 kelas tetap: 0, 1-5, 6-15, 16-35, 36+
- Arahkan kursor atau ketuk kelurahan untuk lihat detail, dan cari kelurahan lewat kolom pencarian
- Daftar 12 kelurahan yang paling sering banjir

Tiga teratas: Kampung Melayu (121), Cawang (85), dan Bidara Cina (71). Ketiganya memang sering disebut di laporan banjir BPBD.

## Data

| Data | Sumber |
|---|---|
| Catatan kejadian banjir per RW, 2013 sampai 2020 | BPBD DKI Jakarta lewat [Open Data Jakarta](https://data.jakarta.go.id/dataset/data-kejadian-bencana-banjir-di-provinsi-dki-jakarta-tahun-2020) |
| Rekap jumlah banjir per kelurahan dan batas kelurahan (OpenStreetMap) | [zulhanandika/dashboard-banjir-jakarta](https://github.com/zulhanandika/dashboard-banjir-jakarta) |

File di folder `data/` adalah hasil olahan:

- `banjir_kelurahan_jakarta.csv`: tabel jumlah catatan banjir dan kelasnya, urut dari yang terbanyak
- `banjir_kelurahan_jakarta.geojson`: batas kelurahan (disederhanakan) plus atribut yang sama

## Cara bikin ulang

```bash
git clone https://github.com/zulhanandika/dashboard-banjir-jakarta sumber
pip install geopandas pyogrio openpyxl
python scripts/prep.py sumber
```

Script ini mencocokkan nama kelurahan di tabel dengan peta, menjumlahkan baris ganda, menentukan kelas, lalu menyisipkan data ke `scripts/template.html` jadi `index.html`.

## Pilihan desain

- **Kelas tetap, bukan natural breaks.** Supaya peta bisa dibandingkan dengan periode lain tanpa batas kelas berubah.
- **Warna biru berurutan** yang aman untuk buta warna, dan tetap terbaca di mode gelap.
- **Tanpa peta dasar jalan**, cukup batas kelurahan, supaya halaman ringan dan bisa dibuka tanpa server.

## Keterbatasan

- Ini data **kejadian masa lalu**, bukan model risiko atau prediksi.
- Satu kejadian banjir bisa tercatat beberapa kali kalau beberapa RW terdampak, jadi kelurahan yang lebih besar (RW lebih banyak) cenderung punya angka lebih tinggi.
- Jakarta punya [Indeks Bahaya Banjir](https://data.go.id/dataset/dataset/indeks-bahaya-banjir) resmi per kelurahan (data 2021), tapi aksesnya terbatas, jadi tidak dipakai di sini.
- Rekap per kelurahan berasal dari olahan pihak ketiga atas data resmi, belum dicocokkan ulang satu per satu dengan data mentah BPBD.

## Tentang proyek ini

Self-project untuk mencoba alur kerja analisis dan pemetaan dengan bantuan AI ([Claude](https://claude.ai)). Pencarian data, pengolahan, dan pembuatan peta dikerjakan bersama Claude.

Tools: Python (geopandas, shapely, pandas), D3.js.

Batas kelurahan © kontributor OpenStreetMap, lisensi ODbL.
