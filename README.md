# AI Visual Trend Dashboard

An interactive Streamlit dashboard for exploring AI-generated visual culture through creative style discovery, representative visual examples, real DiffusionDB prompt statistics, multi-source evidence layers, factual tool capability references, keyword signals, and short-horizon exploratory forecasts.

## Key Insight

The dashboard reports style signals found in the official DiffusionDB 2M metadata table. Tracked styles are assigned with documented keyword rules, so the results are transparent and reproducible rather than presented as a universal ranking of AI art.

The homepage is designed as a creative exploration experience first: users can pick a visual style, generate a creative direction starter, compare two style languages, and inspect representative concept images before going deeper into charts and evidence.

Because DiffusionDB has a short August 2022 source window, the final version adds an Evidence Coverage model: current ecosystem signals, source reliability notes, and a controlled benchmark protocol are displayed separately from the historical prompt counts.

The website connects real prompt counts, keyword growth, sampler metadata, aspect-ratio distribution, illustrative concept images, official tool capability references, trend-confidence scoring, evidence coverage, and exploratory multi-horizon trend forecasts.

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
- `data/source_coverage.csv`
- `data/current_ecosystem_signals.csv`
- `data/controlled_benchmark_prompts.csv`
- `data/benchmark_rubric.csv`

The statistics are derived from the official [DiffusionDB dataset](https://huggingface.co/datasets/poloclub/diffusiondb), a CC0 dataset of real Stable Diffusion Discord generations. The dashboard uses the official 2M-row text-only `metadata.parquet` table.

Source references:

- [DiffusionDB dataset card](https://huggingface.co/datasets/poloclub/diffusiondb)
- [DiffusionDB paper](https://arxiv.org/abs/2210.14896)
- [DiffusionDB GitHub repository](https://github.com/poloclub/diffusiondb)
- [Krea Open Prompts](https://github.com/krea-ai/open-prompts)
- [Hugging Face text-to-image dataset catalog](https://huggingface.co/datasets?sort=likes&task_categories=task_categories%3Atext-to-image)
- [Civitai REST API reference](https://github.com/civitai/civitai/wiki/REST-API-Reference)
- [Midjourney Video documentation](https://docs.midjourney.com/docs/en/video)
- [Runway Image-to-Video guide](https://help.runwayml.com/hc/en-us/articles/48324313115155-Image-to-Video-Prompting-Guide)
- [Adobe Firefly product page](https://www.adobe.com/products/firefly.html)
- [AIS-4SD Zenodo dataset](https://zenodo.org/records/15131117)

Data cleaning and aggregation:

- Start with `2,000,000` official metadata rows
- Require a valid timestamp
- Keep `image_nsfw < 0.1`
- Keep `prompt_nsfw < 0.1`
- Retain `981,354` safety-filtered prompt records
- Assign tracked styles with transparent keyword rules in `scripts/build_real_data.py`
- Aggregate matches by UTC date, style, keyword, and intent
- Normalize daily tracked-style counts into an index for trend charts and into daily tracked-match shares for forecast comparison

Tracked-style classification:

```text
Safe DiffusionDB records analyzed: 981,354
Tracked-style prompt matches: 263,472
Classification coverage: 26.85%
Source time window: 2022-08-06 to 2022-08-20 UTC
```

The tracked-style coverage is intentionally partial. Prompts without an explicit rule match remain part of the analyzed source population but are not forced into a style category.

The newer evidence files do not overwrite DiffusionDB counts. They document what each extra source can and cannot prove:

- `source_coverage.csv` separates historical baseline, expanded prompt corpus, dataset discovery, current ecosystem signal, capability evidence, and controlled benchmark layers.
- `current_ecosystem_signals.csv` records newer signals such as image-to-video workflows, commercial generative production, open prompt corpus expansion, and community model/tag APIs.
- `controlled_benchmark_prompts.csv` defines 24 reusable prompts for a future fair cross-tool experiment.
- `benchmark_rubric.csv` defines how outputs should be scored before any empirical tool ranking is claimed.

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
- Homepage Visual Trend Playground for style discovery and creative direction starters
- Style Duel for side-by-side comparison of two visual languages
- Visual Highlights preview with representative concept images
- Homepage AI Toolchain Snapshot showing where each tool fits in the production workflow
- Homepage Evidence Model Snapshot explaining how DiffusionDB limitations are handled
- Plotly chart selection with click drill-down
- Trend Confidence Score combining historical prompt volume with current evidence layers
- Factual AI tool capability matrix with official source links and no invented 0-100 quality scores
- Real sampler and aspect-ratio metadata charts
- Representative AI-generated concept gallery using local illustrative assets and visual evidence captions
- Use Case Recommendation for brand campaigns, game concepts, social visuals, short film moodboards, and product renders
- Motion Preview GIFs for cinematic, editorial, and luxury use cases
- Evidence Coverage page with source reliability matrix, current ecosystem signals, and controlled benchmark protocol
- Real-World References page with official tool links and trend evidence notes
- Stable prompt text area for copying generated creative directions
- Moodboard preview based on selected visual styles
- Exploratory 7-, 14-, and 21-day weighted projections using daily tracked-match shares, momentum signals, and expanding uncertainty intervals
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
2. Use Explore a Visual Trend to generate a creative direction starter.
3. Compare two styles in Style Duel.
4. Use the sidebar filters.
5. Click a trend chart point to show drill-down details.
6. Open Representative Works and explain that the local images are illustrative concept assets.
7. Use Random Explore.
8. Show Use Case Recommendation and Motion Preview.
9. Open Evidence Coverage and switch the evidence lens to explain why the project is no longer limited to a single DiffusionDB reading.
10. Open Real References to show official research links.
11. Show the multi-horizon forecast chart, momentum map, and scenario table; explain why longer horizons have wider uncertainty.

## Suggested Presentation Insight

Use the latest dashboard result shown in the hero metrics during your presentation. The insight is computed from real daily DiffusionDB prompt matches:

- Prompt matches are grouped by UTC `period` and tracked `style`.
- Each daily style count is normalized into a comparison index.
- The latest date is compared with the first date to identify the largest observed change.
