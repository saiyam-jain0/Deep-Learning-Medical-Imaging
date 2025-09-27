
import os
import argparse
import csv
import math
import numpy as np
from PIL import Image
import torch
from torchvision import transforms, models

def load_model_checkpoint(ckpt_path, device):
    model = models.efficientnet_b0(pretrained=False)
    num_ftrs = model.classifier[1].in_features
    model.classifier[1] = torch.nn.Linear(num_ftrs, 1)
    state = torch.load(ckpt_path, map_location=device)
    model.load_state_dict(state["model_state"] if "model_state" in state else state)
    model.to(device).eval()
    return model

def predict_tiles(model, tiles_list, tiles_dir, device, batch_size=32, tile_size=256):
    transform = transforms.Compose([
        transforms.Resize((tile_size, tile_size)),
        transforms.ToTensor(),
        transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])
    ])
    probs = {}
    loader = []
    names = []
    for info in tiles_list:
        names.append(info['tile_name'])
        img = Image.open(os.path.join(tiles_dir, info['tile_name'])).convert('RGB')
        loader.append(transform(img))
    with torch.no_grad():
        for i in range(0, len(loader), batch_size):
            batch = torch.stack(loader[i:i+batch_size]).to(device)
            out = model(batch)
            p = torch.sigmoid(out).squeeze().cpu().numpy()
            for j, val in enumerate(p):
                probs[names[i+j]] = float(val)
    return probs

def stitch_heatmap(tiles_list, probs, out_path, tile_size=256):
    max_x = max([int(t['x']) + int(t['w']) for t in tiles_list])
    max_y = max([int(t['y']) + int(t['h']) for t in tiles_list])
    canvas = np.zeros((max_y, max_x), dtype=np.float32)
    weight = np.zeros_like(canvas)
    for t in tiles_list:
        x, y, w, h = int(t['x']), int(t['y']), int(t['w']), int(t['h'])
        val = probs[t['tile_name']]
        canvas[y:y+h, x:x+w] += val
        weight[y:y+h, x:x+w] += 1.0
    weight[weight==0] = 1.0
    canvas = canvas / weight
    norm = (canvas - canvas.min()) / (canvas.max() - canvas.min() + 1e-9)
    heat = (norm * 255).astype(np.uint8)
    Image.fromarray(heat).save(out_path)
    print(f"Saved heatmap to {out_path}")

def read_tiles_csv(csv_path):
    tiles=[]
    with open(csv_path,'r') as f:
        reader = csv.DictReader(f)
        for r in reader:
            tiles.append(r)
    return tiles

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--tiles_dir", required=True)
    p.add_argument("--csv", required=True)
    p.add_argument("--ckpt", required=True)
    p.add_argument("--out", default="heatmap.png")
    p.add_argument("--batch", type=int, default=32)
    p.add_argument("--tile_size", type=int, default=256)
    args = p.parse_args()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tiles = read_tiles_csv(args.csv)
    model = load_model_checkpoint(args.ckpt, device)
    probs = predict_tiles(model, tiles, args.tiles_dir, device, batch_size=args.batch, tile_size=args.tile_size)
    stitch_heatmap(tiles, probs, args.out, tile_size=args.tile_size)
