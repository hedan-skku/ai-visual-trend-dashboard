# AI Visual Trend Dashboard Speaker Notes

## Slide 1: Title
Introduce the project as a Streamlit web dashboard that turns AI-generated visual culture into a creative exploration experience supported by real prompt trends, tool benchmarks, representative works, and evidence notes.

## Slide 2: 5W1H Framework
Explain the PRD foundation: why the project exists, who it serves, what it includes, when users would use it, where it runs, and how it was built.

## Slide 3: Target Users and Jobs
Describe the main users: students, creators, designers, marketers, art directors, and evaluators. Emphasize that the dashboard supports both research and creative inspiration.

## Slide 4: Requirement Coverage Matrix
Show how the website answers the PRD requirements: data credibility, interaction depth, visual evidence, technical quality, and presentation readiness.

## Slide 5: Main PRD Features
Map each core PRD feature to the actual website module: trend analysis, tool comparison, keyword dashboard, interactive filters, and dashboard metrics.

## Slide 6: Website Architecture
Walk through the website structure: Home creative exploration, Trend Analytics, Representative Works, Tool Benchmarks, Keyword Insights, Creative Strategy, Evidence Coverage, and Real References.

## Slide 7: UI Design Direction
Explain the dark UI, neon accents, sidebar navigation, responsive layout, and AI-themed visual language. Emphasize that the homepage now feels more like an exploration tool: users can generate a creative direction starter, view representative images, and compare two style languages before reading research details.

## Slide 8: Data Foundation
Clarify the real dataset pipeline. The dashboard starts with the official DiffusionDB 2M metadata table, keeps 981,354 prompt records after documented safety filters, and assigns 263,472 tracked-style prompt matches with transparent rules. Then explain the limitation: DiffusionDB is a short 2022 historical window, so the final dashboard adds separate evidence layers for current ecosystem signals, source coverage, future controlled benchmark testing, and a 2024-2026 Current Trend Horizon.

## Slide 9: Trend Analytics
Present the live-data insight: on 2022-08-20 UTC, 3D Render is the leading tracked style with 2,306 matched prompts, followed by Anime and Cyberpunk. Then show the 2024-2026 Current Trend Horizon to explain how the project avoids feeling outdated while keeping the 2022 data honest. Finally show the Trend Confidence Score and explain that it combines real prompt volume with newer evidence signals, without treating it as absolute truth.

## Slide 10: Representative Works
Explain why representative AI-generated images strengthen the dashboard: they make abstract style categories visible and understandable.

## Slide 11: AI Toolchain Benchmark
Explain that the dashboard avoids invented quality scores. It compares factual, source-linked capabilities and production roles: text-to-image, editing, video, customization, and discovery workflows.

## Slide 12: Interaction Design
Describe the live interaction design: linked filters, click drill-down, random exploration, cached loading, and performance feedback.

## Slide 13: Creative Strategy Layer
Show how the dashboard turns analysis into creative output through recommendations, prompt direction, moodboard preview, motion preview, and 7-, 14-, and 21-day exploratory projections. Use the momentum map to explain how current share and recent movement reveal different style trajectories.

## Slide 14: Evidence Coverage
Explain how the project breaks beyond DiffusionDB's limitation. Use the Evidence Coverage page to show the source reliability matrix, current ecosystem signals, 2024-2026 horizon layer, and controlled benchmark protocol. Emphasize that the project separates different evidence types instead of mixing incompatible datasets into one fake ranking.

## Slide 15: Technical Implementation
Highlight maintainability: modular functions, cached CSV loading, error handling, local assets, requirements file, README, and GitHub repository.

## Slide 16: Roadmap and Deliverables
Connect the final project to the PRD development plan: Step 1 prototype, Step 2 interactivity, Step 3 polish and final presentation assets. Mention current delivery status.

## Slide 17: Conclusion
Close with the main argument: the project presents AI visual trends as a complete research product, connecting PRD goals, data evidence, interface design, visual examples, and technical implementation.
