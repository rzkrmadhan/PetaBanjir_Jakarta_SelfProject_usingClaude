# Peta Banjir Jakarta per Kelurahan

Interactive map yang nunjukin seberapa sering tiap kelurahan di Jakarta kena banjir selama 2013 sampai 2020, berdasarkan data BPBD DKI Jakarta.

**Lihat peta:** buka `index.html` di browser, atau lewat GitHub Pages kalau sudah aktif.

## Ada apa aja di petanya

- 262 kelurahan di daratan Jakarta (Kepulauan Seribu nggak ditampilin)
- Warna = jumlah kejadian banjir 2013 sampai 2020, dibagi jadi 5 class: 0, 1-5, 6-15, 16-35, 36+
- Hover atau tap kelurahan buat lihat detailnya, plus ada search bar buat cari kelurahan
- List 12 kelurahan yang paling sering banjir

Top 3-nya: Kampung Melayu (121), Cawang (85), dan Bidara Cina (71). Ketiganya memang langganan muncul di laporan banjir BPBD.

## Data

| Data | Sumber |
|---|---|
| Data kejadian banjir per RW, 2013 sampai 2020 | BPBD DKI Jakarta via [Open Data Jakarta](https://data.jakarta.go.id/dataset/data-kejadian-bencana-banjir-di-provinsi-dki-jakarta-tahun-2020) |
| Rekap jumlah banjir per kelurahan + boundary kelurahan (OpenStreetMap) | [zulhanandika/dashboard-banjir-jakarta](https://github.com/zulhanandika/dashboard-banjir-jakarta) |

Output di folder `data/`:

- `banjir_kelurahan_jakarta.csv`: tabel jumlah kejadian banjir dan class-nya, urut dari yang paling banyak
- `banjir_kelurahan_jakarta.geojson`: boundary kelurahan (sudah di-simplify) plus atribut yang sama

## Cara run ulang

```bash
git clone https://github.com/zulhanandika/dashboard-banjir-jakarta sumber
pip install geopandas pyogrio openpyxl
python scripts/prep.py sumber
```

Script-nya nge-join nama kelurahan di tabel dengan polygon di peta, gabungin baris yang dobel, nentuin class, terus masukin datanya ke `scripts/template.html` jadi `index.html`.

## Kenapa didesain begini

- **Pakai fixed class, bukan natural breaks (Jenks).** Natural breaks bikin batas class berubah tiap datanya ganti, jadi susah dibandingin. Dengan fixed class, kalau nanti ada peta periode lain, tinggal dijejerin aja.
- **Color ramp biru yang colorblind-friendly**, dan tetap kebaca di dark mode.
- **Tanpa basemap jalan**, cukup boundary kelurahan. Biar ringan dan bisa dibuka langsung tanpa server.

## Limitasi

- Ini data **kejadian yang sudah lewat**, bukan model risiko atau prediksi.
- Satu kejadian banjir bisa kecatat beberapa kali kalau beberapa RW kena. Jadi kelurahan yang lebih besar (RW-nya lebih banyak) cenderung angkanya lebih tinggi.
- Jakarta sebenarnya punya [Indeks Bahaya Banjir](https://data.go.id/dataset/dataset/indeks-bahaya-banjir) resmi per kelurahan (data 2021), tapi aksesnya terbatas, jadi nggak dipakai di sini.
- Rekap per kelurahan diambil dari olahan pihak ketiga atas data resmi, belum dicek ulang satu per satu ke raw data BPBD.

## Tentang project ini

Self-project buat nyobain workflow analisis dan mapping pakai bantuan AI ([Claude](https://claude.ai)). Mulai dari cari data, olah data, sampai bikin petanya dikerjain bareng Claude.

Tools: Python (geopandas, shapely, pandas), D3.js.

Boundary kelurahan © kontributor OpenStreetMap, lisensi ODbL.
