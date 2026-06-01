# AI Visual Trend Dashboard

An interactive Streamlit dashboard for exploring AI-generated visual culture through real DiffusionDB prompt statistics, factual tool capability references, illustrative representative works, keyword signals, and short-horizon exploratory forecasts.

## Key Insight

The dashboard reports style signals found in the official DiffusionDB 2M metadata table. Tracked styles are assigned with documented keyword rules, so the results are transparent and reproducible rather than presented as a universal ranking of AI art.

The website connects real prompt counts, keyword growth, sampler metadata, aspect-ratio distribution, illustrative concept images, official tool capability references, and exploratory linear forecasts.

## Live Demo

Local development URL:

```bash
http://localhost:8501
```

When deployed, add your Streamlit Cloud URL here:

```text
https://your-app-name.streamlit.app
```

## Screenshot

Main dashboard preview:

![Streamlit preview](streamlit-preview.png)

Representative works preview:

![Representative works preview](representative-works-preview.png)

## How To Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
streamlit run app.py
```

If port 8501 is busy:

```bash
streamlit run app.py --server.port 8510
```

## Data Source

Current project data lives in:

- `data/prompt_trend_signals.csv`
- `data/dataset_summary.csv`
- `data/sampler_distribution.csv`
- `data/aspect_ratio_distribution.csv`
- `data/prompt_examples.csv`
- `data/tool_benchmarks.csv`
- `data/representative_works.csv`
- `data/real_world_references.csv`

The statistics are derived from the official [DiffusionDB dataset](https://huggingface.co/datasets/poloclub/diffusiondb), a CC0 dataset of real Stable Diffusion Discord generations. The dashboard uses the official 2M-row text-only `metadata.parquet` table.

Source references:

- [DiffusionDB dataset card](https://huggingface.co/datasets/poloclub/diffusiondb)
- [DiffusionDB paper](https://arxiv.org/abs/2210.14896)
- [DiffusionDB GitHub repository](https://github.com/poloclub/diffusiondb)

Data cleaning and aggregation:

- Start with `2,000,000` official metadata rows
- Require a valid timestamp
- Keep `image_nsfw < 0.1`
- Keep `prompt_nsfw < 0.1`
- Retain `981,354` safety-filtered prompt records
- Assign tracked styles with transparent keyword rules in `scripts/build_real_data.py`
- Aggregate matches by UTC date, style, keyword, and intent
- Normalize daily tracked-style counts into an index for chart comparison

Tracked-style classification:

```text
Safe DiffusionDB records analyzed: 981,354
Tracked-style prompt matches: 263,472
Classification coverage: 26.85%
Source time window: 2022-08-06 to 2022-08-20 UTC
```

The tracked-style coverage is intentionally partial. Prompts without an explicit rule match remain part of the analyzed source population but are not forced into a style category.

## Rebuild The Real Data

Download the official DiffusionDB metadata table to a temporary folder:

```bash
curl -L -o /private/tmp/diffusiondb_metadata.parquet \
  https://huggingface.co/datasets/poloclub/diffusiondb/resolve/main/metadata.parquet
```

Rebuild the dashboard CSV files:

```bash
python3 scripts/build_real_data.py \
  --metadata /private/tmp/diffusiondb_metadata.parquet \
  --output-dir data
```

## Features

- Cached CSV data loading with `st.cache_data`
- Sidebar filters for style, UTC date, tool, and capability focus
- Random exploration button for live demos
- Homepage AI Toolchain Snapshot showing where each tool fits in the production workflow
- Plotly chart selection with click drill-down
- Factual AI tool capability matrix with official source links and no invented 0-100 quality scores
- Real sampler and aspect-ratio metadata charts
- Representative AI-generated concept gallery using local illustrative assets and visual evidence captions
- Use Case Recommendation for brand campaigns, game concepts, social visuals, short film moodboards, and product renders
- Motion Preview GIFs for cinematic, editorial, and luxury use cases
- Real-World References page with official tool links and trend evidence notes
- Stable prompt text area for copying generated creative directions
- Moodboard preview based on selected visual styles
- Exploratory next-7-days linear forecast with uncertainty interval
- Friendly error handling for missing or invalid CSV files

## Visual Style Coverage

The dashboard tracks 10 AI visual styles:

- Cyberpunk
- Anime
- 3D Render
- Retro Futurism
- Minimalism
- Dark Fantasy
- Documentary Realism
- Surreal Editorial
- Luxury Fashion
- AI Cinematic Storyboard

## Tech Stack

- Python
- Streamlit
- Pandas
- Plotly
- NumPy
- scikit-learn
- AI-generated local image assets

## Deployment Notes

For Streamlit Cloud:

1. Push this project to GitHub.
2. Make sure `requirements.txt`, `app.py`, `data/`, and `assets/` are committed.
3. Create a new Streamlit Cloud app from the GitHub repository.
4. Set the main file path to `app.py`.
5. Add the public app URL to the top of this README.

## Demo Video Plan

Record a 1-2 minute Loom or OBS video:

1. Show the dashboard hero metrics and data volume.
2. Use the sidebar filters.
3. Click a trend chart point to show drill-down details.
4. Open Representative Works and explain that the local images are illustrative concept assets.
5. Use Random Explore.
6. Show Use Case Recommendation and Motion Preview.
7. Open Real References to show official research links.
8. Copy a creative direction prompt.
9. Show the short-horizon forecast chart and explain its limitation.

## Suggested Presentation Insight

Use the latest dashboard result shown in the hero metrics during your presentation. The insight is computed from real daily DiffusionDB prompt matches:

- Prompt matches are grouped by UTC `period` and tracked `style`.
- Each daily style count is normalized into a comparison index.
- The latest date is compared with the first date to identify the largest observed change.
