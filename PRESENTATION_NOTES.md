# Presentation Notes

## 1. Project Topic

AI Visual Trend Dashboard is a Data Hub Dashboard about AI-generated visual culture. It explores how prompt language, visual styles, AI tools, and representative images reveal changes in creative technology.

## 2. Target Users

- Designers who want visual trend references
- Art directors who compare tools and styles
- Students studying AI-generated visual culture
- Creators looking for prompt and moodboard ideas

## 3. Data Story

The dashboard derives its core statistics from the official DiffusionDB 2M metadata table. It begins with 2,000,000 rows and keeps 981,354 prompt records after requiring a valid timestamp, `image_nsfw < 0.1`, and `prompt_nsfw < 0.1`. Transparent keyword rules classify 263,472 prompts into 10 tracked visual styles. The website reports daily UTC trends for the real 2022-08-06 to 2022-08-20 source window.

The project also acknowledges that DiffusionDB is not enough by itself. The final website adds a multi-source evidence model with Krea Open Prompts, Hugging Face dataset discovery, Civitai API planning, official tool documentation, AIS-4SD, and a controlled benchmark protocol. These layers add current context without mixing unnormalized sources into the historical DiffusionDB trend counts.

## 4. Key Insight

Use the live hero metrics during the presentation. They dynamically identify the leading tracked style, runner-up style, and largest observed first-to-last-day change from real DiffusionDB prompt matches.

## 5. Main Features To Demo

1. Show top metrics and the 981,354 safety-filtered DiffusionDB prompt count.
2. Explain the AI Toolchain Snapshot: ideation, customization, commercial design, and motion/video.
3. Explain the Evidence Model Snapshot: historical baseline, current ecosystem layer, and source coverage model.
4. Use sidebar filters to select style, UTC date, tool, capability focus, and evidence lens.
5. Click a chart point for drill-down keywords and representative images.
6. Show the Trend Confidence Score and explain that it is an evidence-confidence score, not a statistical truth score.
7. Open Representative Works and explain visual evidence.
8. Open Tool Benchmarks to show the factual capability matrix and official source link.
9. Open Evidence Coverage and switch between Historical Baseline, Current Ecosystem, Multi-Source Evidence, and Controlled Benchmark Protocol.
10. Open Creative Strategy and show Use Case Recommendation.
11. Show Motion Preview and explain why motion is used only for cinematic/editorial/brand use cases.
12. Open Real References and explain how official tool references support the dashboard categories.
13. Show the 7-, 14-, and 21-day exploratory projections, momentum map, and comparison table. Explain why the uncertainty range expands at longer horizons.

## 6. Technical Stack

- Streamlit for the dashboard
- Pandas for CSV data processing
- Plotly for interactive charts
- NumPy / scikit-learn-compatible logic for weighted multi-horizon forecasting
- Local AI-generated image assets for representative visual evidence
- Lightweight GIF previews for selected motion-relevant styles
- Official reference links for real-world context
- Multi-source evidence coverage files for source reliability and future benchmark planning

## 7. Honest Limitation

DiffusionDB is real, but its 2M metadata table covers a short August 2022 collection window. The tracked-style taxonomy is a transparent keyword-rule lens rather than a universal classification of every prompt. Local gallery images are illustrative concept assets, not records copied from DiffusionDB. The Evidence Coverage page turns this limitation into a research design by separating historical data, current context, capability evidence, and future benchmark protocol.

## 8. Final One-Sentence Pitch

This project turns AI prompt data into a visual trend research dashboard that helps users understand not only which styles are visible in the data, but how strong the evidence is, why the styles matter, and how they can be used in real creative work.
