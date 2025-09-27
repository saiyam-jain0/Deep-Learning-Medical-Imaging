# Deep Learning for Medical Imaging / WSI Tumor Heatmap & Viewer

> This repository implements a pipeline for working with whole-slide pathology images (WSIs) — tiling, tile-level model inference, heatmap stitching, and an interactive visualization viewer.

---

## 🧾 Table of Contents

- [Project Overview](#project-overview)  
- [Features](#features)  
- [Directory Structure](#directory-structure)  
- [Installation](#installation)  
- [Usage](#usage)  
  - [Preprocess / Tiling](#preprocess--tiling)  
  - [Inference & Stitching](#inference--stitching)  
  - [Launch Viewer](#launch-viewer)  
- [Results / Sample Outputs](#results--sample-outputs)  
- [Evaluation](#evaluation)  
- [Future Improvements](#future-improvements)  
- [Credits & References](#credits--references)  
- [License](#license)

---

## Project Overview

Clinical researchers and digital pathology tools often require working with gigapixel whole-slide images (WSIs), which are too large to process in one pass. This repository addresses that challenge by:

1. Splitting WSIs into manageable tiles,  
2. Running a trained deep model (e.g. EfficientNet, U-Net, or HoVer-Net) on the tiles,  
3. Stitching tile predictions into slide-level heatmaps, and  
4. Serving an interactive viewer (via Flask + OpenSeadragon) to overlay heatmaps on slides for visual inspection.

This setup closely aligns with use cases in **digital pathology**, cancer diagnosis, and research applications (e.g. tumor region mapping, cellular quantification).  

---

## Features

- Tiling of high-resolution WSIs or large pathology images (`preprocess_tiles.py`)  
- Tile-level inference with model checkpoint support (`inference_and_stitch.py`)  
- Reconstruction / stitching of heatmaps over original slide coordinates  
- Lightweight Flask + OpenSeadragon viewer (`/viewer`)  
- Quantitative metrics (Dice, IoU, area metrics) — **you should fill in / extend these**  
- Example screenshots and demo videos  

---

## Directory Structure

```text
Deep-Learning-Medical-Imaging/
├── README.md
├── preprocess_tiles.py
├── inference_and_stitch.py
├── app.py                  # Main Flask app (or similar)
├── templates/
│   └── viewer.html         # Viewer page template
├── static/
│   ├── slide_downscaled.jpg
│   └── heatmap.png
├── models/
│   └── your_model_checkpoint.pth
├── data/
│   └── sample_slide.svs    # (Optional: sample data or WSI)
└── requirements.txt
````

You may also have your original Brain Tumor classification files (model, scripts, etc.) in separate subfolders — feel free to document them here.

---

## Installation

1. Clone the repo:

   ```bash
   git clone https://github.com/<your-username>/Deep-Learning-Medical-Imaging.git
   cd Deep-Learning-Medical-Imaging
   ```

2. (Recommended) Create a virtual environment:

   ```bash
   conda create -n wsi_env python=3.9
   conda activate wsi_env
   ```

3. Install required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. If you need OpenSlide support:

   * On Ubuntu: `sudo apt-get install openslide-tools libopenslide-dev`
   * On Mac (via Homebrew): `brew install openslide`
   * Then `pip install openslide-python`

---

## Usage

### Preprocess / Tiling

Run the tiling script on a WSI or large pathology image:

```bash
python preprocess_tiles.py --input path/to/your_slide.svs \
                           --outdir tiles_out \
                           --tile_size 256 \
                           --overlap 32
```

This produces folder `tiles_out/` containing PNG tiles and `tiles_coords.csv` (with `x, y, w, h` info).

### Inference & Stitching

Run inference on the tiles and stitch into a single heatmap:

```bash
python inference_and_stitch.py --tiles_dir tiles_out \
                               --csv tiles_out/tiles_coords.csv \
                               --ckpt models/your_checkpoint.pth \
                               --out static/heatmap.png \
                               --batch 32 \
                               --tile_size 256
```

### Launch Viewer

Start the Flask app (e.g. `app.py`) and open `/viewer` in your browser:

```bash
export FLASK_APP=app.py
flask run
```

Then visit: `http://127.0.0.1:5000/viewer`
You should see the slide image with an overlay heatmap — pan and zoom to inspect.

---

## Results / Sample Outputs

*(Fill this section with screenshots and example outputs of your demo.)*

* Overlaid heatmap example: `static/heatmap.png` over slide
* Screenshot: `/viewer` page
* Dice / IoU numbers for held-out sample tiles (e.g. `Dice = 0.78`, `IoU = 0.68`)
* Optional: a 60-second screencast video link

---

## Evaluation

You can evaluate performance using tile-level metrics or aggregated slide-level metrics. Example metrics:

* **Dice coefficient**, **IoU (Jaccard)**
* **Precision / Recall / F1**
* **Tumor area fraction**, **cell counts** (if segmented)

You may script a small evaluation notebook or script to compute these over a validation set of slides.

---

## Future Improvements

* Use segmentation models (U-Net / HoVer-Net) for pixel-level mask instead of heatmap
* Generate DeepZoom or IIIF overlays for more scalable viewer performance
* Dockerize the application for easy deployment
* Deploy as web service (Heroku, Render, GCP)
* Add batch inference, GPU optimization and streaming I/O for large slides

---

## Credits & References

* **Slideflow** — framework for WSI deep learning & visualization
* **OpenSlide** — reading whole-slide images
* **TIAToolbox** — tools and utilities for computational pathology
* **HoVer-Net / U-Net** — models for nuclei / tissue segmentation
* Tutorials and papers on digital pathology and WSIs

---
