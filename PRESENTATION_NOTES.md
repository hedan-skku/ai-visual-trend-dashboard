# Presentation Notes

## 1. Project Topic

AI Visual Trend Dashboard is a Data Hub Dashboard about AI-generated visual culture. It explores how prompt language, visual styles, AI tools, and representative images reveal changes in creative technology.

## 2. Target Users

- Designers who want visual trend references
- Art directors who compare tools and styles
- Students studying AI-generated visual culture
- Creators looking for prompt and moodboard ideas

## 3. Data Story

The dashboard derives its statistics from the official DiffusionDB 2M metadata table. It begins with 2,000,000 rows and keeps 981,354 prompt records after requiring a valid timestamp, `image_nsfw < 0.1`, and `prompt_nsfw < 0.1`. Transparent keyword rules classify 263,472 prompts into 10 tracked visual styles. The website reports daily UTC trends for the real 2022-08-06 to 2022-08-20 source window.

## 4. Key Insight

Use the live hero metrics during the presentation. They dynamically identify the leading tracked style, runner-up style, and largest observed first-to-last-day change from real DiffusionDB prompt matches.

## 5. Main Features To Demo

1. Show top metrics and the 981,354 safety-filtered DiffusionDB prompt count.
2. Explain the AI Toolchain Snapshot: ideation, customization, commercial design, and motion/video.
3. Use sidebar filters to select style, UTC date, and tool.
4. Click a chart point for drill-down keywords and representative images.
5. Open Representative Works and explain visual evidence.
6. Open Tool Benchmarks to show the factual capability matrix and official source link.
7. Open Creative Strategy and show Use Case Recommendation.
8. Show Motion Preview and explain why motion is used only for cinematic/editorial/brand use cases.
9. Open Real References and explain how official tool references support the dashboard categories.
10. Show the next-7-days exploratory forecast and explain its short-window limitation.

## 6. Technical Stack

- Streamlit for the dashboard
- Pandas for CSV data processing
- Plotly for interactive charts
- NumPy / scikit-learn-compatible logic for linear forecasting
- Local AI-generated image assets for representative visual evidence
- Lightweight GIF previews for selected motion-relevant styles
- Official reference links for real-world context

## 7. Honest Limitation

DiffusionDB is real, but its 2M metadata table covers a short August 2022 collection window. The tracked-style taxonomy is a transparent keyword-rule lens rather than a universal classification of every prompt. Local gallery images are illustrative concept assets, not records copied from DiffusionDB.

## 8. Final One-Sentence Pitch

This project turns AI prompt data into a visual trend research dashboard that helps users understand not only which styles are popular, but why they matter and how they can be used in real creative work.
