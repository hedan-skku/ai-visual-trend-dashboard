# Presentation Notes

## 1. Project Topic

AI Visual Trend Dashboard is a Data Hub Dashboard about AI-generated visual culture. It explores how prompt language, visual styles, AI tools, and representative images reveal changes in creative technology.

## 2. Target Users

- Designers who want visual trend references
- Art directors who compare tools and styles
- Students studying AI-generated visual culture
- Creators looking for prompt and moodboard ideas

## 3. Data Story

The dashboard uses a structured semi-real prompt dataset with 22,050 prompt signals. The data is grouped by year, style, tool, keyword, and intent. The pipeline is designed so the CSV can be replaced by a Kaggle Stable Diffusion prompt export.

## 4. Key Insight

Anime leads the 2024 sample volume, while Cyberpunk remains strong through cinematic lighting and atmosphere keywords. AI Cinematic Storyboard and Documentary Realism are emerging, suggesting a shift from static aesthetics toward narrative, video-oriented, and believable image-making.

## 5. Main Features To Demo

1. Show top metrics and the 22,050 prompt count.
2. Explain the AI Toolchain Snapshot: ideation, customization, commercial design, and motion/video.
3. Use sidebar filters to select style, year, and tool.
4. Click a chart point for drill-down keywords and representative images.
5. Open Representative Works and explain visual evidence.
6. Open Tool Benchmarks to show selected tool highlighting.
7. Open Creative Strategy and show Use Case Recommendation.
8. Show Motion Preview and explain why motion is used only for cinematic/editorial/brand use cases.
9. Open Real References and explain how official tool references support the dashboard categories.
10. Show 2025-2027 exploratory forecast.

## 6. Technical Stack

- Streamlit for the dashboard
- Pandas for CSV data processing
- Plotly for interactive charts
- NumPy / scikit-learn-compatible logic for linear forecasting
- Local AI-generated image assets for representative visual evidence
- Lightweight GIF previews for selected motion-relevant styles
- Official reference links for real-world context

## 7. Honest Limitation

The current dataset is semi-real and structured for demonstration. The strongest final improvement would be replacing `data/prompt_trend_signals.csv` with a real Kaggle prompt export while keeping the same schema.

## 8. Final One-Sentence Pitch

This project turns AI prompt data into a visual trend research dashboard that helps users understand not only which styles are popular, but why they matter and how they can be used in real creative work.
