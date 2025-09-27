
import os
import argparse
import csv
from PIL import Image
import numpy as np

try:
    import openslide
    HAS_OPENS = True
except Exception:
    HAS_OPENS = False

def tile_openslide(slide_path, outdir, tile_size=256, overlap=0):
    slide = openslide.OpenSlide(slide_path)
    level = 0
    w, h = slide.level_dimensions[level]
    stride = tile_size - overlap
    os.makedirs(outdir, exist_ok=True)
    csv_path = os.path.join(outdir, "tiles_coords.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["tile_name", "x", "y", "w", "h"])
        cnt = 0
        for y in range(0, h - tile_size + 1, stride):
            for x in range(0, w - tile_size + 1, stride):
                tile = slide.read_region((x, y), level, (tile_size, tile_size)).convert("RGB")
                tile_name = f"tile_{cnt:06d}.png"
                tile.save(os.path.join(outdir, tile_name))
                writer.writerow([tile_name, x, y, tile_size, tile_size])
                cnt += 1
    print(f"Saved {cnt} tiles to {outdir}")

def tile_image(slide_path, outdir, tile_size=256, overlap=0):
    im = Image.open(slide_path).convert("RGB")
    w,h = im.size
    stride = tile_size - overlap
    os.makedirs(outdir, exist_ok=True)
    csv_path = os.path.join(outdir, "tiles_coords.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["tile_name", "x", "y", "w", "h"])
        cnt = 0
        for y in range(0, h - tile_size + 1, stride):
            for x in range(0, w - tile_size + 1, stride):
                box = (x, y, x+tile_size, y+tile_size)
                tile = im.crop(box)
                tile_name = f"tile_{cnt:06d}.png"
                tile.save(os.path.join(outdir, tile_name))
                writer.writerow([tile_name, x, y, tile_size, tile_size])
                cnt += 1
    print(f"Saved {cnt} tiles to {outdir}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True, help="Path to slide (svs or large image)")
    p.add_argument("--outdir", required=True)
    p.add_argument("--tile_size", type=int, default=256)
    p.add_argument("--overlap", type=int, default=0)
    args = p.parse_args()
    if args.input.lower().endswith(('.svs','.tif','.ndpi')) and HAS_OPENS:
        tile_openslide(args.input, args.outdir, args.tile_size, args.overlap)
    else:
        tile_image(args.input, args.outdir, args.tile_size, args.overlap)
