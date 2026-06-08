# Presentation Notes

## 1. Project Topic

AI Visual Trend Dashboard is a creative data dashboard about AI-generated visual culture. It begins with visual exploration and then connects that experience to real prompt data, tool evidence, and research notes.

## 2. Target Users

- Designers who want visual trend references
- Art directors who compare tools and styles
- Students studying AI-generated visual culture
- Creators looking for prompt and moodboard ideas
- Users who want an engaging way to turn visual trends into creative directions

## 3. Data Story

The dashboard derives its core statistics from the official DiffusionDB 2M metadata table. It begins with 2,000,000 rows and keeps 981,354 prompt records after requiring a valid timestamp, `image_nsfw < 0.1`, and `prompt_nsfw < 0.1`. Transparent keyword rules classify 263,472 prompts into 10 tracked visual styles. The website reports daily UTC trends for the real 2022-08-06 to 2022-08-20 source window.

The project also acknowledges that DiffusionDB is not enough by itself. The final website adds a multi-source evidence model with Krea Open Prompts, Hugging Face dataset discovery, Civitai API planning, official tool documentation, AIS-4SD, and a controlled benchmark protocol. These layers add current context without mixing unnormalized sources into the historical DiffusionDB trend counts.

To make the project feel less outdated, the time design is split into two layers. DiffusionDB is presented as a real 2022 historical baseline, while a separate 2024-2026 Current Trend Horizon shows evidence-weighted outlook signals for AI video storyboarding, commercial AI production, open model ecosystems, synthetic realism, prompt corpus expansion, product visualization, and personalized style systems.

## 4. Key Insight

Use the live hero metrics during the presentation. They dynamically identify the leading tracked style, runner-up style, and largest observed first-to-last-day change from real DiffusionDB prompt matches.

## 5. Main Features To Demo

1. Show top metrics and the 981,354 safety-filtered DiffusionDB prompt count.
2. Show the 2024-2026 Current Trend Horizon and explain why it is separated from DiffusionDB prompt counts.
3. Use Explore a Visual Trend to show how a user can choose a style, creative goal, fresh preview image, and prompt starter.
4. Show Visual Highlights to explain the visual language of different AI styles.
5. Explain the AI Toolchain Snapshot: ideation, customization, commercial design, and motion/video.
6. Explain the Evidence Model Snapshot: historical baseline, current ecosystem layer, and source coverage model.
7. Use sidebar filters to select style, historical baseline date, tool, capability focus, and evidence lens.
8. Click a chart point for drill-down keywords and representative images.
9. Show the Trend Confidence Score and explain that it is an evidence-confidence score, not a statistical truth score.
10. Open Representative Works and explain visual evidence.
11. Open Tool Benchmarks to show the factual capability matrix and official source link.
12. Open Evidence Coverage and switch between Historical Baseline, Current Ecosystem, Multi-Source Evidence, and Controlled Benchmark Protocol.
13. Open Creative Strategy and show Use Case Recommendation.
14. Show Motion Preview and explain why motion is used only for cinematic/editorial/brand use cases.
15. Open Real References and explain how official tool references support the dashboard categories.
16. Show the 7-, 14-, and 21-day exploratory projections, momentum map, and comparison table. Explain why longer horizons have wider uncertainty.

## 6. Technical Stack

- Streamlit for the dashboard
- Pandas for CSV data processing
- Plotly for interactive charts
- NumPy / scikit-learn-compatible logic for weighted multi-horizon forecasting
- Local AI-generated image assets for representative visual evidence
- Lightweight GIF previews for selected motion-relevant styles
- Official reference links for real-world context
- Multi-source evidence coverage files for source reliability and future benchmark planning
- Homepage creative interaction modules: Visual Trend Playground and Visual Highlights
- 2024-2026 Current Trend Horizon data layer
- Separate explore-preview image set for homepage freshness

## 7. Honest Limitation

DiffusionDB is real, but its 2M metadata table covers a short August 2022 collection window. The tracked-style taxonomy is a transparent keyword-rule lens rather than a universal classification of every prompt. Local gallery images are illustrative concept assets, not records copied from DiffusionDB. The Evidence Coverage page turns this limitation into a research design by separating historical data, current context, capability evidence, and future benchmark protocol.

## 8. Final One-Sentence Pitch

This project turns AI prompt data into a creative visual trend experience: users can first explore style ideas, then check the data and evidence behind those trends.
