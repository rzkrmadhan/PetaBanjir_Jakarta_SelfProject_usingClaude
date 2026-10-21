"""Bangun ulang data dan peta banjir per kelurahan DKI Jakarta.

Pakai:
    git clone https://github.com/zulhanandika/dashboard-banjir-jakarta sumber
    pip install geopandas pyogrio openpyxl
    python scripts/prep.py sumber

Hasil: data/banjir_kelurahan_jakarta.geojson, data/banjir_kelurahan_jakarta.csv, index.html
"""
import csv
import json
import re
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.geometry import MultiPolygon
from shapely.geometry.polygon import orient

ROOT = Path(__file__).resolve().parent.parent
BINS = [-1, 0, 5, 15, 35, 10**6]          # batas kelas tetap, supaya bisa dibandingkan antar tahun
LABELS = ["0", "1-5", "6-15", "16-35", "36+"]


def key(s):
    """Samakan penulisan nama kelurahan (huruf kecil, tanpa spasi/tanda baca)."""
    return re.sub(r"[^a-z]", "", str(s).lower())


def rewind(geom):
    """D3 butuh ring luar searah jarum jam (kebalikan GeoJSON RFC 7946)."""
    if geom.geom_type == "Polygon":
        return orient(geom, -1)
    return MultiPolygon([orient(p, -1) for p in geom.geoms])


def round_coords(c):
    return [round_coords(x) for x in c] if isinstance(c[0], list) else [round(c[0], 5), round(c[1], 5)]


def main(src):
    src = Path(src)
    kel = gpd.read_file(src / "Kelurahan-DKI-Jakarta.gpkg")          # batas OSM, EPSG:4326
    tab = pd.read_excel(src / "Rekapitulasi Banjir Jakarta per Kelurahan.xlsx")

    kel["key"] = kel["name"].map(key)
    tab["key"] = tab["Kelurahan"].map(key)
    # Beberapa kelurahan muncul 2 baris (penulisan beda di data asli), jadi dijumlahkan
    tab = tab.groupby("key", as_index=False).agg(
        kota=("Kota", "first"), kec=("Kecamatan", "first"), kel=("Kelurahan", "first"), n=("Jumlah Banjir", "sum"))

    m = kel.merge(tab, on="key", how="left", validate="one_to_one")
    missing = m[m["n"].isna()]
    if len(missing):
        sys.exit(f"Ada {len(missing)} poligon tanpa data: {missing['name'].tolist()}")

    m = m[m["kota"] != "Kepulauan Seribu"].copy()                   # pulau jauh, tidak ditampilkan
    m["n"] = m["n"].astype(int)
    m["cls"] = pd.cut(m["n"], bins=BINS, labels=range(5)).astype(int)
    m["geometry"] = m.geometry.simplify(0.00008, preserve_topology=True).map(rewind)

    fc = json.loads(m[["kel", "kec", "kota", "n", "cls", "geometry"]].to_json(drop_id=True))
    for f in fc["features"]:
        f["geometry"]["coordinates"] = round_coords(f["geometry"]["coordinates"])

    out = ROOT / "data"
    out.mkdir(exist_ok=True)
    (out / "banjir_kelurahan_jakarta.geojson").write_text(json.dumps(fc, separators=(",", ":")))

    with open(out / "banjir_kelurahan_jakarta.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["kota", "kecamatan", "kelurahan", "jumlah_catatan_banjir_2013_2020", "kelas"])
        for p in sorted((f["properties"] for f in fc["features"]), key=lambda p: -p["n"]):
            w.writerow([p["kota"], p["kec"], p["kel"], p["n"], LABELS[p["cls"]]])

    html = (ROOT / "scripts" / "template.html").read_text()
    data_js = "const FLOOD=" + json.dumps(fc, separators=(",", ":")) + ";"
    (ROOT / "index.html").write_text(html.replace("/*DATA*/", data_js))
    print(f"Selesai: {len(fc['features'])} kelurahan")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
