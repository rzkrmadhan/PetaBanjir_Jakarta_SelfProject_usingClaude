"""Bikin versi gambar (PNG) dari peta banjir, buat README dan Notion.

Pakai:
    python scripts/make_figure.py
Hasil: images/peta_banjir_jakarta.png
"""
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

ROOT = Path(__file__).resolve().parent.parent
COLORS = ["#f1f4f2", "#c6dbef", "#6baed6", "#2b7bba", "#08306b"]   # sama dengan peta interaktif
LABELS = ["0", "1 - 5", "6 - 15", "16 - 35", "36+"]


def main():
    gdf = gpd.read_file(ROOT / "data" / "banjir_kelurahan_jakarta.geojson")
    gdf = gdf.set_crs(4326, allow_override=True).to_crs(32748)          # UTM 48S, biar scale bar benar
    gdf["color"] = gdf["cls"].map(lambda c: COLORS[int(c)])

    fig, ax = plt.subplots(figsize=(9, 9.2), dpi=200)
    gdf.plot(ax=ax, color=gdf["color"], edgecolor="white", linewidth=0.35)
    ax.set_axis_off()

    # Label 3 kelurahan teratas
    for _, r in gdf.nlargest(3, "n").iterrows():
        p = r.geometry.representative_point()
        ax.annotate(f"{r['kel']} ({r['n']})", xy=(p.x, p.y), xytext=(14, -14), textcoords="offset points",
                    fontsize=8.5, color="#14232e",
                    arrowprops=dict(arrowstyle="-", color="#14232e", lw=0.6),
                    bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#c9d3da", lw=0.5))

    counts = gdf["cls"].value_counts()
    handles = [Patch(facecolor=COLORS[i], edgecolor="#9aa9b4", lw=0.5,
                     label=f"{LABELS[i]}  ({counts.get(i, 0)} kelurahan)") for i in range(4, -1, -1)]
    ax.legend(handles=handles, title="Jumlah kejadian banjir\n2013 - 2020", loc="lower left",
              frameon=True, fontsize=8.5, title_fontsize=9, framealpha=1, edgecolor="#d6e0e6")

    # Scale bar 5 km
    x0, y0, x1, y1 = gdf.total_bounds
    sx, sy = x1 - 6000, y0 + 600
    ax.plot([sx, sx + 5000], [sy, sy], color="#14232e", lw=2.5, solid_capstyle="butt")
    ax.text(sx + 2500, sy + 700, "5 km", ha="center", fontsize=8.5, color="#14232e")

    ax.set_title("Kelurahan yang paling sering banjir di Jakarta", fontsize=14, fontweight="bold",
                 loc="left", color="#14232e", pad=22)
    ax.text(0, 1.012, "Jumlah kejadian banjir per kelurahan, 2013 - 2020. Makin gelap, makin sering banjir.",
            transform=ax.transAxes, fontsize=9.5, color="#5a6b78")
    fig.text(0.02, 0.03, "Sumber: BPBD DKI Jakarta via Open Data Jakarta, rekap per kelurahan dari "
             "github.com/zulhanandika/dashboard-banjir-jakarta. Batas kelurahan © OpenStreetMap.\n"
             "Proyeksi UTM zona 48S (EPSG:32748). Kepulauan Seribu tidak ditampilkan.",
             fontsize=7, color="#5a6b78")

    out = ROOT / "images"
    out.mkdir(exist_ok=True)
    fig.savefig(out / "peta_banjir_jakarta.png", bbox_inches="tight", facecolor="white")
    print("Tersimpan:", out / "peta_banjir_jakarta.png")


if __name__ == "__main__":
    main()
