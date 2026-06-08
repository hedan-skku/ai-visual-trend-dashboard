from pathlib import Path
from html import escape
import os
import random

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

try:
    from sklearn.linear_model import LinearRegression
except Exception:
    LinearRegression = None


BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
ASSET_DIR = BASE_DIR / "assets"
BG_COLOR = "#080c10"

THEME = {
    "bg": BG_COLOR,
    "panel": "#101620",
    "text": "#ecf2f8",
    "muted": "#9ca9b8",
    "gold": "#e3bf73",
    "cyan": "#66d9e8",
    "rose": "#ff7aa8",
    "green": "#8be28b",
}


st.set_page_config(page_title="AI Visual Trend Dashboard", page_icon="AI", layout="wide")


def inject_css():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background:
                linear-gradient(180deg, #070b10 0%, {THEME["bg"]} 38%, #0b1119 100%);
            color: {THEME["text"]};
        }}

        .main .block-container {{
            max-width: 1240px;
            padding-top: 1.2rem;
        }}

        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, #0a1016 0%, #0d141d 100%);
            border-right: 1px solid rgba(255,255,255,.08);
            min-width: 18rem;
        }}

        div[data-testid="stMetric"] {{
            background: linear-gradient(180deg, rgba(18, 27, 39, .94), rgba(11, 17, 25, .94));
            border: 1px solid rgba(255,255,255,.10);
            border-top: 1px solid rgba(102, 217, 232, .24);
            border-radius: 10px;
            padding: 1rem 1.05rem;
            box-shadow: 0 18px 40px rgba(0,0,0,.24);
        }}

        div[data-testid="stMetric"] p {{
            color: {THEME["muted"]};
        }}

        div[data-testid="stMetricValue"] {{
            color: #f4f8fb;
        }}

        .hero-panel {{
            min-height: 300px;
            padding: 2.4rem;
            border-radius: 14px;
            border: 1px solid rgba(255,255,255,.11);
            background:
                linear-gradient(120deg, rgba(16, 22, 32, .98) 0%, rgba(12, 20, 29, .94) 52%, rgba(6, 10, 14, .98) 100%);
            background-size: cover;
            background-position: center;
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
            margin: .4rem 0 1.2rem;
            box-shadow: 0 28px 75px rgba(0,0,0,.35);
        }}

        .hero-kicker {{
            color: {THEME["cyan"]};
            font-size: .82rem;
            font-weight: 700;
            letter-spacing: .08em;
            text-transform: uppercase;
            margin-bottom: .55rem;
        }}

        .hero-title {{
            color: {THEME["text"]};
            font-size: clamp(2rem, 5vw, 4.2rem);
            line-height: 1.03;
            margin: 0;
            max-width: 900px;
            font-weight: 820;
        }}

        .hero-copy {{
            max-width: 780px;
            color: #cbd5df;
            margin-top: .9rem;
            font-size: 1.05rem;
        }}

        .hero-pill-row {{
            margin-top: 1.05rem;
        }}

        .hero-pill {{
            display: inline-flex;
            align-items: center;
            padding: .42rem .68rem;
            border-radius: 999px;
            margin: .18rem .28rem .18rem 0;
            background: rgba(102, 217, 232, .11);
            border: 1px solid rgba(102, 217, 232, .24);
            color: #dffbff;
            font-size: .86rem;
            font-weight: 650;
        }}

        .insight-strip {{
            background: linear-gradient(90deg, rgba(102,217,232,.12), rgba(227,191,115,.10));
            border: 1px solid rgba(255,255,255,.10);
            border-left: 3px solid {THEME["cyan"]};
            border-radius: 10px;
            padding: .95rem 1.05rem;
            margin: .95rem 0 .4rem;
            color: #e7f6f9;
        }}

        .insight-strip strong {{
            color: #ffffff;
        }}

        .section-header-line {{
            display: flex;
            align-items: center;
            gap: .7rem;
            margin: 2.25rem 0 1rem;
        }}

        .section-header-line:before {{
            content: "";
            width: .35rem;
            height: 1.25rem;
            border-radius: 99px;
            background: linear-gradient(180deg, {THEME["cyan"]}, {THEME["gold"]});
        }}

        .section-header-line h3 {{
            margin: 0;
            color: {THEME["gold"]};
            font-size: 1.28rem;
            font-weight: 800;
        }}

        .stButton > button {{
            border-radius: 9px;
            border: 1px solid rgba(102,217,232,.30);
            background: linear-gradient(90deg, rgba(102,217,232,.18), rgba(227,191,115,.16));
            color: #f2fbff;
            font-weight: 720;
        }}

        .stButton > button:hover {{
            border-color: rgba(102,217,232,.55);
            color: #ffffff;
        }}

        .section-title {{
            margin: 2rem 0 .9rem;
            color: {THEME["gold"]};
            font-size: 1.24rem;
            font-weight: 750;
        }}

        .story-card, .source-card, .prompt-card {{
            background: linear-gradient(180deg, rgba(18, 27, 39, .86), rgba(11, 17, 25, .88));
            border: 1px solid rgba(255,255,255,.10);
            border-radius: 10px;
            padding: 1rem;
            min-height: 100%;
        }}

        .work-card {{
            background: linear-gradient(180deg, rgba(18, 27, 39, .86), rgba(11, 17, 25, .88));
            border: 1px solid rgba(255,255,255,.10);
            border-radius: 10px;
            overflow: hidden;
            min-height: 100%;
            margin-bottom: 1rem;
        }}

        .work-card img {{
            width: 100%;
            aspect-ratio: 4 / 3;
            object-fit: cover;
            display: block;
        }}

        div[data-testid="stImage"] {{
            width: 100%;
        }}

        div[data-testid="stImage"] img {{
            width: 100% !important;
            height: auto !important;
            border-radius: 6px;
            display: block;
            object-fit: cover;
        }}

        .work-card-body {{
            padding: .9rem;
        }}

        .work-meta {{
            color: {THEME["cyan"]};
            font-size: .78rem;
            font-weight: 700;
            margin-bottom: .35rem;
            text-transform: uppercase;
        }}

        .work-title {{
            color: {THEME["text"]};
            font-size: 1.03rem;
            font-weight: 760;
            margin-bottom: .35rem;
        }}

        .muted {{
            color: {THEME["muted"]};
            font-size: .94rem;
        }}

        .tag {{
            display: inline-block;
            padding: .34rem .58rem;
            border-radius: 999px;
            margin: .16rem .18rem .16rem 0;
            background: rgba(102, 217, 232, .12);
            border: 1px solid rgba(102, 217, 232, .22);
            color: #d9fbff;
            font-size: .86rem;
        }}

        .recommendation {{
            border-left: 3px solid {THEME["gold"]};
            background: rgba(227, 191, 115, .10);
            padding: .9rem 1rem;
            border-radius: 6px;
            color: #f8e6bd;
        }}

        .copy-box {{
            width: 100%;
            min-height: 110px;
            color: #ecf2f8;
            background: #0b1017;
            border: 1px solid rgba(255,255,255,.14);
            border-radius: 8px;
            padding: .8rem;
            font: 14px ui-monospace, SFMono-Regular, Menlo, monospace;
        }}

        .small-note {{
            color: {THEME["muted"]};
            font-size: .85rem;
        }}

        @media (max-width: 760px) {{
            .hero-panel {{
                min-height: 280px;
                padding: 1.2rem;
            }}

            .hero-title {{
                font-size: 2.1rem;
            }}

            section[data-testid="stSidebar"] {{
                min-width: auto;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def show_section(title):
    st.markdown(
        f"""
        <div class="section-header-line">
            <h3>{escape(title)}</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )


def safe_image(relative_path, **kwargs):
    image_path = BASE_DIR / str(relative_path)
    if image_path.exists():
        st.image(str(image_path), **kwargs)
        return True

    st.warning(f"Image asset missing: {relative_path}")
    return False


def data_path(filename):
    candidate_dirs = [DATA_DIR]
    source_dir = os.environ.get("AI_VISUAL_DASHBOARD_SOURCE_DIR")
    if source_dir:
        candidate_dirs.append(Path(source_dir) / "data")

    for directory in candidate_dirs:
        path = directory / filename
        if path.exists():
            return path
    return DATA_DIR / filename


def friendly_error(message):
    st.error(message)
    st.stop()


@st.cache_data(show_spinner=False)
def load_data():
    try:
        prompt_path = data_path("prompt_trend_signals.csv")
        tool_path = data_path("tool_benchmarks.csv")
        works_path = data_path("representative_works.csv")
        references_path = data_path("real_world_references.csv")
        summary_path = data_path("dataset_summary.csv")
        sampler_path = data_path("sampler_distribution.csv")
        aspect_path = data_path("aspect_ratio_distribution.csv")
        examples_path = data_path("prompt_examples.csv")
        source_coverage_path = data_path("source_coverage.csv")
        ecosystem_path = data_path("current_ecosystem_signals.csv")
        benchmark_prompts_path = data_path("controlled_benchmark_prompts.csv")
        benchmark_rubric_path = data_path("benchmark_rubric.csv")
        horizon_path = data_path("trend_horizon_2024_2026.csv")
        explore_previews_path = data_path("explore_previews.csv")

        prompts = pd.read_csv(prompt_path)
        tools = pd.read_csv(tool_path)
        works = pd.read_csv(works_path)
        references = pd.read_csv(references_path)
        summary = pd.read_csv(summary_path)
        samplers = pd.read_csv(sampler_path)
        aspect_ratios = pd.read_csv(aspect_path)
        examples = pd.read_csv(examples_path)
        source_coverage = pd.read_csv(source_coverage_path)
        ecosystem = pd.read_csv(ecosystem_path)
        benchmark_prompts = pd.read_csv(benchmark_prompts_path)
        benchmark_rubric = pd.read_csv(benchmark_rubric_path)
        horizon = pd.read_csv(horizon_path)
        explore_previews = pd.read_csv(explore_previews_path)
    except FileNotFoundError as exc:
        friendly_error(
            f"Data file missing: {exc.filename}. Restore the committed data/ CSV files or run "
            "scripts/build_real_data.py with the official DiffusionDB metadata table."
        )
    except Exception as exc:
        friendly_error(f"Data loading failed: {exc}")

    required_prompt_cols = {"period", "style", "tool", "keyword", "intent", "prompt_count", "source"}
    if not required_prompt_cols.issubset(prompts.columns):
        missing = ", ".join(sorted(required_prompt_cols - set(prompts.columns)))
        friendly_error(f"Prompt CSV is missing required columns: {missing}")

    prompts["period"] = pd.to_datetime(prompts["period"])
    prompts["prompt_count"] = prompts["prompt_count"].astype(int)

    if "visual_evidence" not in works.columns:
        works["visual_evidence"] = (
            "Composition, lighting, color palette, and use-case signals connect this image to the selected trend."
        )

    style_period = prompts.groupby(["period", "style"], as_index=False)["prompt_count"].sum()
    max_count = style_period["prompt_count"].max()
    style_period["popularity"] = (style_period["prompt_count"] / max_count * 100).round(1)

    keywords = (
        prompts.groupby(["keyword", "intent", "tool", "style"], as_index=False)["prompt_count"]
        .sum()
        .rename(columns={"prompt_count": "frequency"})
        .sort_values("frequency", ascending=False)
    )

    growth = prompts.pivot_table(
        index=["keyword", "intent", "tool", "style"],
        columns="period",
        values="prompt_count",
        aggfunc="sum",
        fill_value=0,
    )
    periods = sorted(prompts["period"].unique())
    midpoint = max(len(periods) // 2, 1)
    early_periods = periods[:midpoint]
    late_periods = periods[midpoint:]
    growth["early_count"] = growth[early_periods].sum(axis=1)
    growth["late_count"] = growth[late_periods].sum(axis=1)
    growth["growth"] = (
        (growth["late_count"] - growth["early_count"])
        / growth["early_count"].replace(0, 1)
        * 100
    ).round(0)
    keywords = keywords.merge(
        growth["growth"].reset_index(),
        on=["keyword", "intent", "tool", "style"],
        how="left",
    )

    summary_values = dict(zip(summary["metric"], summary["value"]))
    return (
        prompts,
        style_period,
        tools,
        keywords,
        samplers,
        aspect_ratios,
        works,
        references,
        summary_values,
        examples,
        source_coverage,
        ecosystem,
        benchmark_prompts,
        benchmark_rubric,
        horizon,
        explore_previews,
    )


def plot_layout(fig, height=430):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=BG_COLOR,
        plot_bgcolor=BG_COLOR,
        font={"color": THEME["text"]},
        height=height,
        margin={"l": 10, "r": 10, "t": 50, "b": 20},
        legend_title_text="",
    )
    return fig


def render_sidebar(styles, tools, periods):
    with st.sidebar:
        st.header("Dashboard Controls")

        if "selected_styles" not in st.session_state:
            st.session_state.selected_styles = styles[:5]
        if "selected_period" not in st.session_state:
            st.session_state.selected_period = periods[-1]
        if "selected_tool" not in st.session_state:
            st.session_state.selected_tool = tools[0]

        if st.button("Random Explore", width="stretch"):
            st.session_state.selected_styles = [random.choice(styles)]
            st.session_state.selected_period = random.choice(periods)
            st.session_state.selected_tool = random.choice(tools)
            st.session_state.random_notice = True

        selected_styles = st.multiselect(
            "Visual styles",
            styles,
            key="selected_styles",
        )
        selected_period = st.select_slider(
            "Historical baseline date",
            options=periods,
            key="selected_period",
        )
        st.caption("DiffusionDB is a real 2022 baseline. Current 2024-2026 signals are shown as a separate horizon layer.")
        selected_tool = st.selectbox(
            "AI tool deep dive",
            tools,
            key="selected_tool",
        )
        benchmark_focus = st.selectbox(
            "Capability focus",
            ["text_to_image", "image_editing", "image_to_video", "public_trend_gallery", "open_local_customization"],
            format_func=lambda item: item.replace("_", " ").title(),
        )
        evidence_lens = st.selectbox(
            "Evidence lens",
            [
                "Historical baseline",
                "Current ecosystem",
                "Multi-source evidence",
                "Controlled benchmark protocol",
            ],
        )

        st.markdown("### Data Source")
        st.markdown(
            "[DiffusionDB dataset](https://huggingface.co/datasets/poloclub/diffusiondb)"
        )
        st.markdown(
            "[DiffusionDB research paper](https://arxiv.org/abs/2210.14896)"
        )
        st.caption(
            "The quantitative baseline is derived from the official DiffusionDB 2M metadata table. "
            "New evidence layers document source coverage, current ecosystem signals, and a controlled benchmark protocol."
        )
        st.caption(
            "Cleaning: valid timestamps only; image_nsfw < 0.1; prompt_nsfw < 0.1; "
            "tracked styles assigned with documented keyword rules; counts aggregated by UTC date."
        )

        if st.session_state.get("random_notice"):
            st.success("Random exploration generated.")

    if not selected_styles:
        selected_styles = styles

    return selected_styles, selected_period, selected_tool, benchmark_focus, evidence_lens


def render_hero(prompts, latest_df, summary):
    top_style = latest_df.sort_values("popularity", ascending=False).iloc[0]
    min_period = prompts["period"].min()
    max_period = prompts["period"].max()
    growth_df = (
        prompts[prompts["period"].isin([min_period, max_period])]
        .groupby(["style", "period"], as_index=False)["prompt_count"]
        .sum()
        .pivot(index="style", columns="period", values="prompt_count")
        .fillna(0)
    )
    growth_df["growth"] = growth_df[max_period] - growth_df[min_period]
    fastest_style = growth_df.sort_values("growth", ascending=False).iloc[0]
    safe_records = int(float(summary["safe_records"]))
    classified_records = int(float(summary["classified_records"]))
    top_two = latest_df.sort_values("prompt_count", ascending=False).head(2)
    top_one = top_two.iloc[0]
    if len(top_two) > 1:
        ranking_sentence = (
            f"{top_one['style']} is the leading tracked style "
            f"({int(top_one['prompt_count']):,} matched prompts), followed by {top_two.iloc[1]['style']} "
            f"({int(top_two.iloc[1]['prompt_count']):,})."
        )
    else:
        ranking_sentence = (
            f"{top_one['style']} is the only selected tracked style in the current filter "
            f"({int(top_one['prompt_count']):,} matched prompts)."
        )

    st.markdown(
        """
        <div class="hero-panel">
            <div class="hero-kicker">AI Visual Culture Research Dashboard</div>
            <h1 class="hero-title">AI Visual Trend Dashboard</h1>
            <p class="hero-copy">
                Explore the visual language of generative AI: from real prompt signals to cinematic style previews,
                tool workflows, creative direction starters, and 2024-2026 trend outlooks.
            </p>
            <div class="hero-pill-row">
                <span class="hero-pill">Real prompt baseline</span>
                <span class="hero-pill">2024-2026 outlook</span>
                <span class="hero-pill">Creative direction generator</span>
                <span class="hero-pill">Visual evidence gallery</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    metric_1, metric_2, metric_3, metric_4 = st.columns(4)
    metric_1.metric("Top Tracked Style", str(top_style["style"]), f'{float(top_style["popularity"]):.1f} index')
    metric_2.metric("Fastest Daily Growth", str(fastest_style.name), f'{int(fastest_style["growth"]):+,}')
    metric_3.metric("Safe Prompts Analyzed", f"{safe_records:,}", "real DiffusionDB records")
    metric_4.metric("Tracked Style Matches", f"{classified_records:,}", f"{prompts['style'].nunique()} documented rules")

    st.markdown(
        f"""
        <div class="insight-strip">
            <strong>Key insight from {max_period:%Y-%m-%d}:</strong>
            {escape(ranking_sentence)} {escape(str(fastest_style.name))} has the largest first-to-last-day change
            ({int(fastest_style['growth']):+,} matched prompts).
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.expander("Data credibility note", expanded=False):
        st.write(
            f"Statistics are derived from the official DiffusionDB 2M metadata table "
            f"({min_period:%Y-%m-%d} to {max_period:%Y-%m-%d} UTC). Safety filtering and tracked-style "
            "classification rules are documented in scripts/build_real_data.py."
        )


def render_snapshot():
    show_section("What You Can Do Here")
    c1, c2, c3 = st.columns(3)
    with c1:
        with st.container(border=True):
            st.write("**Discover the look**")
            st.caption("Use style cards, images, keywords, and motion previews to quickly understand what each AI visual trend feels like.")
    with c2:
        with st.container(border=True):
            st.write("**Build creative direction**")
            st.caption("Turn a trend into a practical prompt starter for campaigns, film moodboards, product renders, or social visuals.")
    with c3:
        with st.container(border=True):
            st.write("**Check the evidence**")
            st.caption("When you need rigor, open the trend charts, confidence score, source coverage page, and official references.")


def render_toolchain_snapshot():
    show_section("AI Toolchain Snapshot")
    st.caption("A qualitative workflow map based on the official capability references linked in the Tool Benchmarks page.")

    toolchain = [
        {
            "stage": "Ideation",
            "tools": "Midjourney / OpenAI Images",
            "why": "Fast concept exploration, strong mood, and visual style discovery.",
        },
        {
            "stage": "Customization",
            "tools": "Stable Diffusion",
            "why": "Best for controlled workflows, custom models, and iterative experimentation.",
        },
        {
            "stage": "Commercial Design",
            "tools": "Adobe Firefly",
            "why": "Useful for brand-safe production, campaign assets, and design workflows.",
        },
        {
            "stage": "Motion / Video",
            "tools": "Runway",
            "why": "Strong fit for image-to-video, cinematic sequences, and storyboard previews.",
        },
    ]

    cols = st.columns(len(toolchain))
    for col, item in zip(cols, toolchain):
        with col:
            with st.container(border=True):
                st.write(f"**{item['stage']}**")
                st.caption(item["tools"])
                st.caption(item["why"])


def render_evidence_model_snapshot(source_coverage, ecosystem):
    show_section("Behind the Trend Signals")
    st.caption(
        "A quick reliability snapshot. The full research explanation lives in the Evidence Coverage page."
    )
    c1, c2, c3 = st.columns(3)
    with c1:
        with st.container(border=True):
            st.write("**Real prompt baseline**")
            st.caption("DiffusionDB anchors the charts with real prompt metadata.")
    with c2:
        with st.container(border=True):
            st.write("**Current signals**")
            st.caption(
                f"{len(ecosystem)} newer signals add context from tools, datasets, and AI communities."
            )
    with c3:
        with st.container(border=True):
            st.write("**Fair comparison plan**")
            st.caption(
                f"{len(source_coverage)} source layers are separated so evidence stays honest."
            )


def style_profile(style):
    profiles = {
        "Cyberpunk": {
            "mood": "Electric, urban, nocturnal",
            "best_for": "music visuals, tech campaigns, sci-fi posters",
            "creative_hook": "Use reflections, rain, signage, and layered city depth.",
        },
        "Anime": {
            "mood": "Emotional, expressive, character-led",
            "best_for": "key visuals, youth campaigns, character storytelling",
            "creative_hook": "Use expressive silhouettes, color contrast, and dramatic backlight.",
        },
        "3D Render": {
            "mood": "Polished, material-focused, commercial",
            "best_for": "product launches, spatial branding, object studies",
            "creative_hook": "Use clean geometry, studio light, glass, metal, and precise framing.",
        },
        "Retro Futurism": {
            "mood": "Nostalgic, optimistic, speculative",
            "best_for": "worldbuilding, editorial sets, concept interiors",
            "creative_hook": "Mix chrome, analog interfaces, warm light, and future nostalgia.",
        },
        "Minimalism": {
            "mood": "Quiet, refined, spacious",
            "best_for": "brand identity, design systems, premium layouts",
            "creative_hook": "Use negative space, restrained color, clean typography, and calm rhythm.",
        },
        "Dark Fantasy": {
            "mood": "Mystic, cinematic, dramatic",
            "best_for": "game worlds, book covers, atmospheric storytelling",
            "creative_hook": "Use fog, ritual silhouettes, shadow, and a clear magical focal point.",
        },
        "Documentary Realism": {
            "mood": "Believable, grounded, observational",
            "best_for": "editorial storytelling, social issue visuals, realistic concept scenes",
            "creative_hook": "Use natural light, human scale, small details, and subtle grain.",
        },
        "Surreal Editorial": {
            "mood": "Dreamlike, high-fashion, impossible",
            "best_for": "fashion editorials, magazine covers, luxury campaigns",
            "creative_hook": "Use impossible architecture, floating fabric, and polished photographic light.",
        },
        "Luxury Fashion": {
            "mood": "Premium, elegant, controlled",
            "best_for": "brand campaigns, lookbooks, beauty and fashion direction",
            "creative_hook": "Use refined styling, soft highlights, glossy surfaces, and restraint.",
        },
        "AI Cinematic Storyboard": {
            "mood": "Narrative, atmospheric, motion-ready",
            "best_for": "film previsualization, music videos, storyboards",
            "creative_hook": "Use dramatic framing, volumetric light, camera movement, and sequence logic.",
        },
    }
    return profiles.get(
        style,
        {
            "mood": "Experimental and flexible",
            "best_for": "visual exploration and creative ideation",
            "creative_hook": "Use a clear subject, strong lighting, and a specific emotional goal.",
        },
    )


def preview_for_style(explore_previews, works, style):
    preview = explore_previews[explore_previews["style"] == style]
    if not preview.empty:
        return preview.iloc[0]

    work = works[works["style"] == style].iloc[0]
    return pd.Series(
        {
            "style": work["style"],
            "image": work["image"],
            "preview_title": work["representative_work"],
            "preview_caption": work["visual_evidence"],
        }
    )


def render_current_trend_horizon(horizon):
    show_section("2024-2026 Current Trend Horizon")
    st.caption(
        "This is a forward-looking signal layer, not DiffusionDB prompt volume. It uses current ecosystem evidence, "
        "official tool capability references, dataset discovery, and benchmark planning to show where AI visual culture is moving."
    )

    latest_year = int(horizon["horizon_year"].max())
    latest = horizon[horizon["horizon_year"] == latest_year].sort_values("signal_score", ascending=False)
    top_theme = latest.iloc[0]
    gain = (
        horizon.pivot_table(index="trend_theme", columns="horizon_year", values="signal_score", aggfunc="mean")
        .dropna()
        .assign(gain=lambda df: df[latest_year] - df[int(horizon["horizon_year"].min())])
        .sort_values("gain", ascending=False)
    )
    fastest_theme = gain.iloc[0]

    c1, c2, c3 = st.columns(3)
    c1.metric("Leading 2026 Signal", top_theme["trend_theme"], f'{int(top_theme["signal_score"])} signal')
    c2.metric("Fastest Horizon Gain", gain.index[0], f'+{int(fastest_theme["gain"])}')
    c3.metric("Horizon Window", "2024-2026", "current + outlook")

    fig = px.line(
        horizon,
        x="horizon_year",
        y="signal_score",
        color="trend_theme",
        markers=True,
        title="Evidence-weighted AI visual trend horizon",
        hover_data=["related_style", "confidence_label", "source_layer", "user_takeaway"],
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig.update_xaxes(dtick=1)
    st.plotly_chart(plot_layout(fig, height=460), use_container_width=True)

    with st.expander("How to read the 2024-2026 horizon", expanded=False):
        st.write(
            "The horizon score is a qualitative signal score. It should be read as a research outlook, not as a measured "
            "usage count. DiffusionDB remains the historical prompt baseline; this layer explains newer directions such as "
            "AI video, commercial AI production, open model communities, and synthetic realism."
        )
        st.dataframe(
            latest[["trend_theme", "related_style", "signal_score", "confidence_label", "evidence_basis", "user_takeaway"]]
            .rename(
                columns={
                    "trend_theme": "Trend theme",
                    "related_style": "Related style",
                    "signal_score": "2026 signal",
                    "confidence_label": "Confidence",
                    "evidence_basis": "Evidence basis",
                    "user_takeaway": "User takeaway",
                }
            ),
            width="stretch",
            hide_index=True,
            height=260,
        )


def render_visual_trend_playground(
    prompts,
    style_period,
    works,
    explore_previews,
    selected_styles,
    selected_period,
    selected_tool,
):
    show_section("Explore a Visual Trend")
    st.caption(
        "Start with a style, a creative goal, and a representative image. The data is still there, but the first move is creative exploration."
    )

    styles = sorted(works["style"].unique().tolist())
    goals = [
        "Brand campaign",
        "Short film moodboard",
        "Product launch",
        "Game world concept",
        "Social media visual",
    ]

    if st.session_state.get("home_explore_style") not in styles:
        filtered_choices = [style for style in selected_styles if style in styles]
        st.session_state.home_explore_style = filtered_choices[0] if filtered_choices else styles[0]
    if st.session_state.get("home_goal") not in goals:
        st.session_state.home_goal = goals[0]

    if st.button("Surprise me with a visual direction", width="stretch"):
        st.session_state.home_explore_style = random.choice(styles)
        st.session_state.home_goal = random.choice(goals)
        st.session_state.home_surprise_notice = True
        st.rerun()

    if st.session_state.get("home_surprise_notice"):
        st.success("New visual direction generated. Use the prompt starter below as a launch point.")
        st.session_state.home_surprise_notice = False

    col_controls, col_preview = st.columns([1, 1.15])
    with col_controls:
        explore_style = st.selectbox("Style to explore", styles, key="home_explore_style")
        creative_goal = st.selectbox("Creative goal", goals, key="home_goal")

        profile = style_profile(explore_style)
        style_rows = prompts[prompts["style"] == explore_style]
        selected_date = pd.to_datetime(selected_period)
        latest_rows = style_period[
            (style_period["style"] == explore_style) & (style_period["period"] <= selected_date)
        ].sort_values("period")
        latest_score = float(latest_rows["popularity"].iloc[-1]) if not latest_rows.empty else 0.0
        total_matches = int(style_rows["prompt_count"].sum()) if not style_rows.empty else 0
        top_keywords = (
            style_rows.groupby("keyword")["prompt_count"].sum().sort_values(ascending=False).head(4).index.tolist()
            if not style_rows.empty
            else []
        )
        tag_html = " ".join(f'<span class="tag">{escape(keyword)}</span>' for keyword in top_keywords)

        with st.container(border=True):
            st.write(f"**{explore_style} personality card**")
            st.caption(f"Mood: {profile['mood']}")
            st.caption(f"Best for: {profile['best_for']}")
            st.caption(f"Trend evidence: {total_matches:,} matched DiffusionDB prompts")
            st.progress(min(latest_score / 100, 1.0), text=f"Trend energy on {selected_period}: {latest_score:.1f}/100")
            if tag_html:
                st.markdown(tag_html, unsafe_allow_html=True)

    with col_preview:
        work = works[works["style"] == explore_style].iloc[0]
        preview = preview_for_style(explore_previews, works, explore_style)
        safe_image(preview["image"], caption=f'{preview["style"]} | Explore preview')
        st.caption(f"{preview['preview_title']}: {preview['preview_caption']}")

    prompt = (
        f"{creative_goal.lower()} using {explore_style.lower()}: {work['prompt_starter']}. "
        f"Build the direction around {profile['creative_hook']} Use {selected_tool} as the first tool to test, "
        "then refine composition, format, lighting, audience, and production context."
    )
    st.text_area("Creative direction starter", prompt, height=110)


def render_visual_highlights(works):
    show_section("Visual Highlights")
    st.caption("Representative concept images make the trend categories easier to understand before reading the charts.")
    preferred_styles = ["AI Cinematic Storyboard", "Surreal Editorial", "Luxury Fashion"]
    highlight_df = works[works["style"].isin(preferred_styles)]
    if highlight_df.empty:
        highlight_df = works.head(3)

    cols = st.columns(3)
    for index, row in highlight_df.head(3).reset_index(drop=True).iterrows():
        with cols[index]:
            with st.container(border=True):
                safe_image(row["image"], width="stretch")
                st.write(f"**{row['style']}**")
                st.caption(row["representative_work"])
                st.caption(row["why_it_represents_the_trend"])


def selected_points(event):
    if event and hasattr(event, "selection") and event.selection:
        return event.selection.get("points", [])
    if isinstance(event, dict):
        return event.get("selection", {}).get("points", [])
    return []


def render_drilldown(points, prompts, works):
    if not points:
        st.info("Click a point or bar in the chart above to inspect its keywords and representative image.")
        return

    point = points[0]
    style = point.get("legendgroup") or point.get("y") or point.get("customdata", [None])[0]
    period = point.get("x")

    if isinstance(style, (int, float)):
        style = point.get("label")

    detail = prompts.copy()
    if style in set(prompts["style"]):
        detail = detail[detail["style"] == style]
    if period is not None:
        selected_date = pd.to_datetime(period, errors="coerce")
        if not pd.isna(selected_date):
            detail = detail[detail["period"] == selected_date]

    if detail.empty:
        st.warning("No detailed records found for the selected chart point.")
        return

    work = works[works["style"].isin(detail["style"].unique())].head(1)
    c1, c2 = st.columns([1, 1.1])
    with c1:
        if not work.empty:
            safe_image(
                work.iloc[0]["image"],
                caption=f'{work.iloc[0]["style"]} | {work.iloc[0]["model"]}',
            )
    with c2:
        st.markdown("#### Drill-down details")
        st.dataframe(
            detail[["period", "style", "tool", "keyword", "intent", "prompt_count"]]
            .sort_values("prompt_count", ascending=False),
            width="stretch",
            hide_index=True,
        )


def tab_trends(prompts, style_period, samplers, aspect_ratios, works, selected_styles, selected_period):
    show_section("Historical Prompt Baseline")
    st.caption(
        "This chart uses real 2022 DiffusionDB prompt metadata as a baseline. Click any line point or ranking bar "
        "to inspect the keyword matches behind that historical signal."
    )
    selected_date = pd.to_datetime(selected_period)
    filtered = style_period[(style_period["style"].isin(selected_styles)) & (style_period["period"] <= selected_date)]
    latest = filtered[filtered["period"] == selected_date]

    col_line, col_bar = st.columns([1.25, 1])
    with col_line:
        fig_trend = px.line(
            filtered,
            x="period",
            y="popularity",
            color="style",
            markers=True,
            title="Tracked style index by UTC date",
            color_discrete_sequence=px.colors.qualitative.Set2,
            custom_data=["style"],
        )
        trend_event = st.plotly_chart(
            plot_layout(fig_trend),
            use_container_width=True,
            on_select="rerun",
            selection_mode="points",
            key="trend_chart",
        )

    with col_bar:
        fig_bar = px.bar(
            latest.sort_values("popularity", ascending=True),
            x="popularity",
            y="style",
            orientation="h",
            color="style",
            title=f"Tracked style ranking on {selected_date:%Y-%m-%d}",
            color_discrete_sequence=px.colors.qualitative.Set2,
            custom_data=["style"],
        )
        bar_event = st.plotly_chart(
            plot_layout(fig_bar),
            use_container_width=True,
            on_select="rerun",
            selection_mode="points",
            key="ranking_chart",
        )

    show_section("Clicked Insight")
    render_drilldown(selected_points(trend_event) or selected_points(bar_event), prompts, works)

    show_section("Baseline Metadata Profile")
    st.caption("These charts come directly from DiffusionDB metadata after the same safety filter.")
    col_sampler, col_ratio = st.columns([1.35, 1])
    fig_sampler = px.bar(
        samplers.sort_values("prompt_count"),
        x="prompt_count",
        y="sampler",
        orientation="h",
        title="Sampler distribution in safe records",
        color="share_percent",
        color_continuous_scale="Teal",
    )
    col_sampler.plotly_chart(plot_layout(fig_sampler, height=430), use_container_width=True)
    fig_ratio = px.pie(
        aspect_ratios,
        names="aspect_ratio",
        values="prompt_count",
        title="Image aspect-ratio distribution",
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    col_ratio.plotly_chart(plot_layout(fig_ratio, height=430), use_container_width=True)


def build_confidence_table(prompts, ecosystem):
    totals = prompts.groupby("style", as_index=False)["prompt_count"].sum()
    signal_weights = (
        ecosystem.groupby("related_style", as_index=False)
        .agg(current_signal_weight=("weight", "max"), source_count=("source", "nunique"))
        .rename(columns={"related_style": "style"})
    )
    confidence = totals.merge(signal_weights, on="style", how="left").fillna(
        {"current_signal_weight": 0, "source_count": 0}
    )
    confidence["source_count"] = confidence["source_count"].astype(int) + 1
    confidence["evidence_score"] = (
        42
        + np.log10(confidence["prompt_count"].clip(lower=1)) * 8
        + confidence["current_signal_weight"] * 7
        + confidence["source_count"].clip(upper=4) * 3
    ).clip(0, 100).round(0)
    confidence["confidence_label"] = np.select(
        [
            confidence["evidence_score"] >= 82,
            confidence["evidence_score"] >= 68,
        ],
        ["High", "Medium"],
        default="Exploratory",
    )
    confidence["interpretation"] = np.where(
        confidence["current_signal_weight"] > 0,
        "DiffusionDB baseline plus current ecosystem evidence",
        "DiffusionDB baseline only; needs newer source validation",
    )
    return confidence.sort_values("evidence_score", ascending=False)


def render_trend_confidence(prompts, ecosystem, selected_styles):
    show_section("Trend Confidence Score")
    st.caption(
        "This is an evidence-confidence score, not a statistical truth score. It combines DiffusionDB prompt volume "
        "with whether a style has additional current ecosystem evidence from official docs, open prompt corpora, "
        "dataset catalogs, or community APIs."
    )
    confidence = build_confidence_table(prompts, ecosystem)
    confidence = confidence[confidence["style"].isin(selected_styles)]
    col_chart, col_table = st.columns([1.05, 1.35])
    with col_chart:
        fig = px.bar(
            confidence.sort_values("evidence_score"),
            x="evidence_score",
            y="style",
            color="confidence_label",
            orientation="h",
            title="Evidence confidence by selected style",
            color_discrete_map={"High": THEME["green"], "Medium": THEME["gold"], "Exploratory": THEME["rose"]},
        )
        st.plotly_chart(plot_layout(fig, height=430), use_container_width=True)
    with col_table:
        st.dataframe(
            confidence[
                [
                    "style",
                    "prompt_count",
                    "source_count",
                    "current_signal_weight",
                    "evidence_score",
                    "confidence_label",
                    "interpretation",
                ]
            ].rename(
                columns={
                    "style": "Style",
                    "prompt_count": "DiffusionDB matches",
                    "source_count": "Evidence layers",
                    "current_signal_weight": "Current-signal weight",
                    "evidence_score": "Score",
                    "confidence_label": "Label",
                    "interpretation": "Interpretation",
                }
            ),
            width="stretch",
            hide_index=True,
            height=390,
        )


def tab_evidence_coverage(source_coverage, ecosystem, benchmark_prompts, benchmark_rubric, horizon, evidence_lens):
    show_section("Data Coverage & Source Reliability")
    st.caption(
        "This page turns DiffusionDB's limitation into a research design: DiffusionDB remains the quantitative "
        "historical baseline, while newer sources are treated as evidence layers until they are normalized and validated."
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Evidence Layers", f"{len(source_coverage)}")
    c2.metric("Current Signals", f"{len(ecosystem)}")
    c3.metric("Horizon Signals", f"{horizon['trend_theme'].nunique()} themes")
    c4.metric("Rubric Dimensions", f"{len(benchmark_rubric)}")

    lens_guidance = {
        "Historical baseline": (
            "This lens keeps the strongest claim narrow: DiffusionDB provides real prompt-volume evidence for the "
            "historical 2022 source window."
        ),
        "Current ecosystem": (
            "This lens adds present-day context from official product documentation, open prompt corpora, public dataset "
            "indexes, and community APIs."
        ),
        "Multi-source evidence": (
            "This lens compares all evidence layers side by side so the audience can see which claims are quantitative, "
            "which are contextual, and which are planned for future validation."
        ),
        "Controlled benchmark protocol": (
            "This lens prepares a fair future comparison: each tool receives the same prompts, and results are scored "
            "with the same rubric before any winner is claimed."
        ),
    }
    st.info(f"Current lens: {evidence_lens}. {lens_guidance[evidence_lens]}")

    show_section("Selected Evidence Lens")
    if evidence_lens == "Historical baseline":
        lens_view = source_coverage[source_coverage["evidence_layer"].eq("Historical baseline")]
        st.dataframe(
            lens_view[["source", "data_type", "time_window", "scale", "strength", "limitation"]].rename(
                columns={
                    "source": "Source",
                    "data_type": "Data type",
                    "time_window": "Time window",
                    "scale": "Scale",
                    "strength": "Strength",
                    "limitation": "Limitation",
                }
            ),
            width="stretch",
            hide_index=True,
        )
    elif evidence_lens == "Current ecosystem":
        st.dataframe(
            ecosystem[["signal", "related_style", "source", "evidence_type", "confidence_label", "what_it_adds"]].rename(
                columns={
                    "signal": "Signal",
                    "related_style": "Related style",
                    "source": "Source",
                    "evidence_type": "Evidence type",
                    "confidence_label": "Confidence",
                    "what_it_adds": "What it adds",
                }
            ),
            width="stretch",
            hide_index=True,
            height=300,
        )
    elif evidence_lens == "Controlled benchmark protocol":
        st.dataframe(
            benchmark_prompts[["task_id", "creative_task", "primary_style", "evaluation_focus", "target_tools"]].rename(
                columns={
                    "task_id": "ID",
                    "creative_task": "Creative task",
                    "primary_style": "Style",
                    "evaluation_focus": "Evaluation focus",
                    "target_tools": "Target tools",
                }
            ),
            width="stretch",
            hide_index=True,
            height=300,
        )
    else:
        st.dataframe(
            source_coverage[["source", "evidence_layer", "data_type", "confidence_weight", "limitation"]].rename(
                columns={
                    "source": "Source",
                    "evidence_layer": "Evidence layer",
                    "data_type": "Data type",
                    "confidence_weight": "Weight",
                    "limitation": "Limitation",
                }
            ),
            width="stretch",
            hide_index=True,
            height=300,
        )

    fig = px.bar(
        source_coverage.sort_values("confidence_weight"),
        x="confidence_weight",
        y="source",
        color="evidence_layer",
        orientation="h",
        title="Source reliability and role in the evidence model",
        hover_data=["strength", "limitation"],
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    st.plotly_chart(plot_layout(fig, height=470), use_container_width=True)

    show_section("Source Coverage Matrix")
    st.dataframe(
        source_coverage[
            [
                "source",
                "evidence_layer",
                "data_type",
                "time_window",
                "scale",
                "platform_scope",
                "strength",
                "limitation",
                "confidence_weight",
            ]
        ].rename(
            columns={
                "source": "Source",
                "evidence_layer": "Evidence layer",
                "data_type": "Data type",
                "time_window": "Time window",
                "scale": "Scale",
                "platform_scope": "Platform scope",
                "strength": "Strength",
                "limitation": "Limitation",
                "confidence_weight": "Weight",
            }
        ),
        width="stretch",
        hide_index=True,
        height=430,
    )

    show_section("Current Ecosystem Signals")
    col_signal, col_signal_table = st.columns([1, 1.35])
    with col_signal:
        fig_signal = px.scatter(
            ecosystem,
            x="weight",
            y="related_style",
            color="confidence_label",
            size="weight",
            hover_name="signal",
            title="Signals that extend beyond DiffusionDB",
            color_discrete_map={"High": THEME["green"], "Medium-High": THEME["cyan"], "Medium": THEME["gold"]},
            size_max=34,
        )
        st.plotly_chart(plot_layout(fig_signal, height=460), use_container_width=True)
    with col_signal_table:
        st.dataframe(
            ecosystem[["signal", "related_style", "source", "evidence_type", "confidence_label", "what_it_adds", "limitation"]]
            .rename(
                columns={
                    "signal": "Signal",
                    "related_style": "Related style",
                    "source": "Source",
                    "evidence_type": "Evidence type",
                    "confidence_label": "Confidence",
                    "what_it_adds": "What it adds",
                    "limitation": "Limitation",
                }
            ),
            width="stretch",
            hide_index=True,
            height=430,
        )

    show_section("2024-2026 Horizon Layer")
    st.caption(
        "These rows are separated from DiffusionDB counts. They are evidence-weighted outlook signals for current and future-facing trends."
    )
    st.dataframe(
        horizon[["horizon_year", "trend_theme", "related_style", "signal_score", "confidence_label", "source_layer", "user_takeaway"]]
        .rename(
            columns={
                "horizon_year": "Year",
                "trend_theme": "Trend theme",
                "related_style": "Related style",
                "signal_score": "Signal score",
                "confidence_label": "Confidence",
                "source_layer": "Source layer",
                "user_takeaway": "User takeaway",
            }
        ),
        width="stretch",
        hide_index=True,
        height=360,
    )

    show_section("Controlled AI Tool Benchmark Protocol")
    st.caption(
        "This protocol is ready for a future empirical test. It is not displayed as completed model scoring yet, "
        "because the project should not claim tool winners before every tool is tested on the same prompts."
    )
    benchmark_filter = st.selectbox(
        "Benchmark task filter",
        ["All tasks"] + sorted(benchmark_prompts["creative_task"].unique().tolist()),
        key="benchmark_task_filter",
    )
    benchmark_view = (
        benchmark_prompts
        if benchmark_filter == "All tasks"
        else benchmark_prompts[benchmark_prompts["creative_task"] == benchmark_filter]
    )
    st.dataframe(
        benchmark_view[["task_id", "creative_task", "primary_style", "evaluation_focus", "prompt", "target_tools", "status"]]
        .rename(
            columns={
                "task_id": "ID",
                "creative_task": "Creative task",
                "primary_style": "Style",
                "evaluation_focus": "Evaluation focus",
                "prompt": "Prompt",
                "target_tools": "Target tools",
                "status": "Status",
            }
        ),
        width="stretch",
        hide_index=True,
        height=390,
    )

    show_section("Benchmark Scoring Rubric")
    st.dataframe(
        benchmark_rubric.rename(
            columns={
                "dimension": "Dimension",
                "score_anchor_1": "Score 1",
                "score_anchor_3": "Score 3",
                "score_anchor_5": "Score 5",
                "why_it_matters": "Why it matters",
            }
        ),
        width="stretch",
        hide_index=True,
    )


def render_work_card(row):
    with st.container(border=True):
        safe_image(row["image"], width="stretch")
        st.caption(f'{row["style"]} | {row["recommended_tool"]} | {row["model"]}')
        st.write(f'**{row["representative_work"]}**')
        st.caption(f'Visual evidence: {row["visual_evidence"]}')
        st.caption(row["why_it_represents_the_trend"])
        st.caption(f'Prompt starter: {row["prompt_starter"]}')


def tab_gallery(works, styles):
    show_section("Representative Works Gallery")
    st.caption(
        "These locally stored AI-generated concept images are illustrative examples, not records from DiffusionDB "
        "and not third-party artworks. Each card explains how visible composition, lighting, color, and use-case "
        "signals relate to a tracked prompt category."
    )

    gallery_filter = st.selectbox("Gallery filter", ["All styles"] + styles, key="gallery_style_filter")
    gallery_df = works if gallery_filter == "All styles" else works[works["style"] == gallery_filter]

    cols = st.columns(3)
    for index, row in gallery_df.reset_index(drop=True).iterrows():
        with cols[index % 3]:
            render_work_card(row)


def tab_tools(tools, selected_tool, benchmark_focus):
    show_section("AI Tool Capability Comparison")
    st.caption(
        "This page intentionally avoids invented 0-100 quality scores. Values summarize documented product "
        "capabilities from the linked official pages; they are not a universal ranking."
    )

    capability_columns = [
        "text_to_image",
        "image_editing",
        "image_to_video",
        "public_trend_gallery",
        "open_local_customization",
    ]
    capability_labels = {item: item.replace("_", " ").title() for item in capability_columns}
    display = tools.copy()
    display["documented_yes_count"] = display[capability_columns].eq("Yes").sum(axis=1)
    display["selected"] = np.where(display["tool"] == selected_tool, "Selected tool", "Other tools")

    fig = px.bar(
        display,
        x="tool",
        y="documented_yes_count",
        color="selected",
        title="Explicitly documented capabilities by tool",
        color_discrete_map={"Selected tool": THEME["gold"], "Other tools": THEME["cyan"]},
        hover_data=capability_columns,
    )
    st.plotly_chart(plot_layout(fig, height=430), use_container_width=True)

    focused = tools[tools[benchmark_focus] == "Yes"]["tool"].tolist()
    if focused:
        st.success(f"Tools explicitly documenting {capability_labels[benchmark_focus]}: {', '.join(focused)}.")
    else:
        st.info(
            f"No row is labeled an unqualified Yes for {capability_labels[benchmark_focus]}. "
            "Check the capability matrix and official links for workflow-specific details."
        )

    matrix = tools[["tool"] + capability_columns].rename(columns=capability_labels)
    st.dataframe(matrix, width="stretch", hide_index=True)

    show_section(f"{selected_tool} Deep Dive")
    tool_info = tools[tools["tool"] == selected_tool].iloc[0]
    st.write(f'**Best fit:** {tool_info["best_for"]}')
    st.caption(tool_info["evidence_note"])
    st.link_button("Open official capability reference", tool_info["official_url"])


def tab_keywords(keywords, selected_styles):
    show_section("Prompt Language Intelligence")
    filtered_keywords = keywords[keywords["style"].isin(selected_styles)]
    st.caption(
        "Keyword frequency and growth are derived from real DiffusionDB prompt matches. "
        "Growth compares the first half of the collection window with the second half."
    )

    col_scatter, col_table = st.columns([1.35, 1])
    with col_scatter:
        fig_keywords = px.scatter(
            filtered_keywords,
            x="frequency",
            y="growth",
            size="frequency",
            color="intent",
            hover_name="keyword",
            title="Keyword frequency vs. growth for selected styles",
            color_discrete_sequence=px.colors.qualitative.Set3,
        )
        keyword_event = st.plotly_chart(
            plot_layout(fig_keywords),
            use_container_width=True,
            on_select="rerun",
            selection_mode="points",
            key="keyword_chart",
        )

    with col_table:
        st.dataframe(
            filtered_keywords[["keyword", "style", "intent", "frequency", "growth"]]
            .sort_values(["growth", "frequency"], ascending=False),
            width="stretch",
            hide_index=True,
        )

    top_keywords = filtered_keywords.sort_values("frequency", ascending=False).head(8)
    st.write("Top keyword signals:")
    st.caption(" · ".join(top_keywords["keyword"].tolist()))

    points = selected_points(keyword_event)
    if points:
        st.info(f"Selected keyword: {points[0].get('hovertext', points[0].get('text', 'keyword'))}")


def forecast_direction(change):
    if change >= 3:
        return "Accelerating"
    if change >= 1:
        return "Rising"
    if change <= -3:
        return "Cooling quickly"
    if change <= -1:
        return "Cooling"
    return "Stable"


def predict_styles(style_period, max_horizon=21):
    observed = style_period.copy()
    observed["daily_total"] = observed.groupby("period")["prompt_count"].transform("sum")
    observed["trend_share"] = observed["prompt_count"] / observed["daily_total"] * 100

    future_periods = pd.date_range(
        observed["period"].max() + pd.Timedelta(days=1),
        periods=max_horizon,
        freq="D",
    )
    forecast_rows = []
    outlook_rows = []

    for style, group in observed.groupby("style"):
        group = group.sort_values("period").tail(14)
        x = np.arange(len(group), dtype=float).reshape(-1, 1)
        y = group["trend_share"].to_numpy()
        weights = np.linspace(1.0, 2.2, len(group))

        if LinearRegression is not None:
            model = LinearRegression().fit(x, y, sample_weight=weights)
            slope = float(model.coef_[0])
            fitted = model.predict(x)
        else:
            slope, intercept = np.polyfit(x.flatten(), y, 1, w=weights)
            fitted = x.flatten() * slope + intercept

        current_share = float(y[-1])
        residual = float(np.std(y - fitted)) if len(y) > 1 else 0.35
        volatility = float(np.std(np.diff(y))) if len(y) > 1 else 0.35
        interval_base = max(residual, volatility * 0.7, 0.35)
        recent_mean = float(y[-3:].mean())
        previous_mean = float(y[-6:-3].mean()) if len(y) >= 6 else float(y[:3].mean())
        recent_momentum = recent_mean - previous_mean

        for step, period in enumerate(future_periods, start=1):
            prediction = float(np.clip(current_share + slope * step, 0, 100))
            interval = interval_base * np.sqrt(1 + step / 4)
            forecast_rows.append(
                {
                    "period": period,
                    "style": style,
                    "step": step,
                    "prediction": round(prediction, 2),
                    "lower": round(max(0, prediction - interval), 2),
                    "upper": round(min(100, prediction + interval), 2),
                }
            )

        change_14d = slope * 14
        outlook_rows.append(
            {
                "style": style,
                "current_share": round(current_share, 2),
                "recent_momentum": round(recent_momentum, 2),
                "daily_slope": round(slope, 2),
                "projected_7d": round(float(np.clip(current_share + slope * 7, 0, 100)), 2),
                "projected_14d": round(float(np.clip(current_share + slope * 14, 0, 100)), 2),
                "projected_21d": round(float(np.clip(current_share + slope * 21, 0, 100)), 2),
                "volatility": round(volatility, 2),
                "observed_14d_matches": int(group["prompt_count"].sum()),
                "signal": forecast_direction(change_14d),
            }
        )

    return observed, pd.DataFrame(forecast_rows), pd.DataFrame(outlook_rows)


def clipboard_component(text):
    st.text_area("Prompt ready to copy", value=text, height=120)
    st.caption("Select the text above and copy it with Cmd+C. This avoids unstable browser iframe clipboard code.")


def use_case_recommendation(works):
    recommendations = {
        "Brand campaign": {
            "style": "Luxury Fashion",
            "tool": "Adobe Firefly",
            "why": "Best for polished commercial visuals, brand-safe production, and campaign-like art direction.",
        },
        "Game concept": {
            "style": "Dark Fantasy",
            "tool": "Stable Diffusion",
            "why": "Best for worldbuilding, character mood, controlled style exploration, and iterative concept art.",
        },
        "Social media visual": {
            "style": "Surreal Editorial",
            "tool": "Midjourney",
            "why": "Best for distinctive scroll-stopping images with strong visual surprise and editorial polish.",
        },
        "Short film moodboard": {
            "style": "AI Cinematic Storyboard",
            "tool": "Runway",
            "why": "Best for cinematic framing, previsualization, video-like atmosphere, and sequence planning.",
        },
        "Product render": {
            "style": "3D Render",
            "tool": "OpenAI Images / DALL-E",
            "why": "Best for clean object studies, material exploration, and fast product visualization.",
        },
    }

    show_section("Use Case Recommendation")
    use_case = st.selectbox("I want to create", list(recommendations.keys()))
    rec = recommendations[use_case]
    work = works[works["style"] == rec["style"]].iloc[0]
    prompt = (
        f"For a {use_case.lower()}, use {rec['style']} with {rec['tool']}. "
        f"Prompt starter: {work['prompt_starter']}. "
        "Add audience, format, lighting, composition, and usage context."
    )

    c1, c2 = st.columns([1, 1.2])
    with c1:
        safe_image(work["image"], caption=f"{rec['style']} | {rec['tool']}")
    with c2:
        with st.container(border=True):
            st.write(f"**Recommended style:** {rec['style']}")
            st.write(f"**Recommended tool:** {rec['tool']}")
            st.caption(rec["why"])
            st.caption(prompt)


def motion_preview():
    show_section("Motion Preview")
    st.caption(
        "These lightweight GIFs add motion only where it supports the topic: cinematic/video, editorial mood, and brand campaign direction."
    )
    motion_assets = [
        ("AI Cinematic Storyboard", "assets/motion-cinematic-storyboard.gif", "Camera-like motion preview for video-oriented storytelling."),
        ("Surreal Editorial", "assets/motion-surreal-editorial.gif", "Slow editorial motion for dreamlike image direction."),
        ("Luxury Fashion", "assets/motion-luxury-fashion.gif", "Subtle campaign-style motion for premium brand visuals."),
    ]
    cols = st.columns(3)
    for index, (title, image, caption) in enumerate(motion_assets):
        with cols[index]:
            safe_image(image, width="stretch")
            st.caption(f"{title}: {caption}")


def tab_strategy(style_period, works, styles):
    show_section("Creative Direction Generator")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        mood = st.selectbox("Mood", ["Cinematic", "Dreamlike", "Elegant", "Unsettling", "Energetic"])
    with col_b:
        medium = st.selectbox("Medium", ["Editorial campaign", "Short film", "Product launch", "Game world", "Social series"])
    with col_c:
        audience = st.selectbox("Audience", ["Design directors", "Young creators", "Luxury consumers", "Indie studios", "Tech brands"])

    selected_style = st.selectbox("Visual style", styles)
    prompt_seed = works[works["style"] == selected_style].iloc[0]["prompt_starter"]
    prompt = (
        f"{mood.lower()} {selected_style.lower()} for a {medium.lower()}, designed for {audience.lower()}. "
        f"Use {prompt_seed}, clear subject, cinematic composition, intentional lighting, material texture, "
        "camera perspective, and a specific emotional outcome."
    )

    with st.container(border=True):
        st.write("**Generated creative direction**")
        st.caption(prompt)
    clipboard_component(prompt)

    use_case_recommendation(works)
    motion_preview()

    show_section("Moodboard Preview")
    mood_styles = st.multiselect(
        "Moodboard styles",
        styles,
        default=[selected_style] + [style for style in styles if style != selected_style][:2],
    )
    preview = works[works["style"].isin(mood_styles)].head(3)
    cols = st.columns(3)
    for index, row in preview.reset_index(drop=True).iterrows():
        with cols[index]:
            safe_image(row["image"], caption=f'{row["style"]} | {row["model"]}')

    show_section("2026 Creative Outlook: Multi-Horizon Style Signals")
    st.caption(
        "This section starts from each style's daily share of tracked DiffusionDB matches, then projects scenario checkpoints. "
        "It should be read together with the 2024-2026 Current Trend Horizon on the homepage because the historical source window is short."
    )

    forecast_horizon = st.select_slider(
        "Projection horizon",
        options=[7, 14, 21],
        value=14,
        format_func=lambda value: f"{value} days",
    )
    observed, forecast, outlook = predict_styles(style_period, max_horizon=21)
    default_forecast_styles = outlook.sort_values("current_share", ascending=False)["style"].head(5).tolist()
    forecast_styles = st.multiselect(
        "Compare forecast styles",
        styles,
        default=default_forecast_styles,
    )
    if not forecast_styles:
        forecast_styles = default_forecast_styles
    focus_style = st.selectbox("Uncertainty focus", forecast_styles)

    fig_forecast = go.Figure()
    style_colors = dict(zip(styles, px.colors.qualitative.Set3))
    for style in forecast_styles:
        actual_group = observed[observed["style"] == style].sort_values("period")
        forecast_group = forecast[
            (forecast["style"] == style) & (forecast["step"] <= forecast_horizon)
        ].sort_values("period")
        line_color = style_colors[style]

        if style == focus_style:
            band_periods = [actual_group["period"].iloc[-1]] + forecast_group["period"].tolist()
            band_upper = [actual_group["trend_share"].iloc[-1]] + forecast_group["upper"].tolist()
            band_lower = [actual_group["trend_share"].iloc[-1]] + forecast_group["lower"].tolist()
            fig_forecast.add_trace(
                go.Scatter(
                    x=band_periods + band_periods[::-1],
                    y=band_upper + band_lower[::-1],
                    fill="toself",
                    fillcolor="rgba(102,217,232,0.12)",
                    line={"color": "rgba(255,255,255,0)"},
                    name=f"{style} uncertainty",
                    showlegend=False,
                    hoverinfo="skip",
                )
            )

        fig_forecast.add_trace(
            go.Scatter(
                x=actual_group["period"],
                y=actual_group["trend_share"],
                mode="lines+markers",
                name=f"{style} actual",
                line={"color": line_color},
            )
        )
        fig_forecast.add_trace(
            go.Scatter(
                x=[actual_group["period"].iloc[-1]] + forecast_group["period"].tolist(),
                y=[actual_group["trend_share"].iloc[-1]] + forecast_group["prediction"].tolist(),
                mode="lines+markers",
                name=f"{style} projected",
                line={"color": line_color, "dash": "dash"},
            )
        )
    fig_forecast.add_vline(
        x=observed["period"].max().timestamp() * 1000,
        line_dash="dot",
        line_color="rgba(236,242,248,.45)",
    )
    fig_forecast.update_layout(
        title=f"Actual trend share and {forecast_horizon}-day weighted projection",
        yaxis_title="Share of tracked-style matches (%)",
        hovermode="x unified",
    )
    st.plotly_chart(plot_layout(fig_forecast, height=500), use_container_width=True)

    horizon_column = f"projected_{forecast_horizon}d"
    outlook["projected_change"] = (outlook[horizon_column] - outlook["current_share"]).round(2)
    rising = outlook.sort_values("projected_change", ascending=False).iloc[0]
    cooling = outlook.sort_values("projected_change").iloc[0]
    st.info(
        f"At the {forecast_horizon}-day horizon, {rising['style']} has the strongest projected gain "
        f"({rising['projected_change']:+.2f} percentage points), while {cooling['style']} shows the strongest "
        f"cooling signal ({cooling['projected_change']:+.2f} points)."
    )

    col_momentum, col_outlook = st.columns([1, 1.25])
    with col_momentum:
        fig_momentum = px.scatter(
            outlook,
            x="current_share",
            y="recent_momentum",
            size="observed_14d_matches",
            color="signal",
            hover_name="style",
            hover_data=["daily_slope", "volatility", "projected_7d", "projected_14d", "projected_21d"],
            title="Momentum map: current share vs. recent movement",
            color_discrete_map={
                "Accelerating": THEME["green"],
                "Rising": THEME["cyan"],
                "Stable": THEME["gold"],
                "Cooling": THEME["rose"],
                "Cooling quickly": "#ef6b6b",
            },
            size_max=48,
        )
        fig_momentum.add_hline(y=0, line_dash="dot", line_color="rgba(236,242,248,.45)")
        fig_momentum.update_layout(
            xaxis_title="Current share of tracked matches (%)",
            yaxis_title="Recent 3-day momentum (percentage points)",
        )
        st.plotly_chart(plot_layout(fig_momentum, height=470), use_container_width=True)

    with col_outlook:
        outlook_table = (
            outlook[
                [
                    "style",
                    "current_share",
                    "recent_momentum",
                    "daily_slope",
                    "projected_7d",
                    "projected_14d",
                    "projected_21d",
                    "volatility",
                    "signal",
                ]
            ]
            .sort_values(horizon_column, ascending=False)
            .rename(
                columns={
                    "style": "Style",
                    "current_share": "Current share %",
                    "recent_momentum": "Recent momentum pp",
                    "daily_slope": "Daily slope pp",
                    "projected_7d": "Projected 7d %",
                    "projected_14d": "Projected 14d %",
                    "projected_21d": "Projected 21d %",
                    "volatility": "Volatility pp",
                    "signal": "14d signal",
                }
            )
        )
        st.dataframe(outlook_table, width="stretch", hide_index=True, height=430)

    st.caption(
        "How to read this section: solid lines are observed shares; dashed lines are projections. "
        "The shaded range is shown for the selected focus style only. The 7-, 14-, and 21-day values are scenario "
        "checkpoints, not long-term market forecasts."
    )

    st.warning(
        "Ethical note: disclose synthetic production when needed, avoid misleading realism, respect artist identity, "
        "and document which assets, datasets, or tools influenced the final output."
    )


def tab_references(references):
    show_section("Real-World References")
    st.caption(
        "This section uses official tool pages and documentation as research references. "
        "It does not copy third-party artwork; it links to sources and explains what trend evidence each source supports."
    )
    for _, row in references.iterrows():
        with st.container(border=True):
            c1, c2 = st.columns([1, 2])
            with c1:
                st.write(f"**{row['platform']}**")
                st.caption(row["official_reference"])
                st.link_button("Open official reference", row["url"], width="stretch")
            with c2:
                st.write(f"**Related style:** {row['related_style']}")
                st.caption(f"Why it matters: {row['why_it_matters']}")
                st.caption(f"Visual evidence: {row['visual_evidence']}")


def render_data_notes(prompts, summary):
    show_section("Data Notes")
    source = prompts["source"].iloc[0]
    c1, c2, c3 = st.columns(3)
    with c1:
        with st.container(border=True):
            st.write("**Real Source Data**")
            st.caption(
                f"{source}. {int(float(summary['raw_records'])):,} official metadata rows; "
                f"{int(float(summary['safe_records'])):,} rows after documented safety filters."
            )
    with c2:
        with st.container(border=True):
            st.write("**Processing**")
            st.caption(
                "Tracked styles use transparent keyword rules in scripts/build_real_data.py. "
                "Matches are grouped by UTC date, style, keyword, and intent."
            )
    with c3:
        with st.container(border=True):
            st.write("**Interpretation Boundary**")
            st.caption(
                f"{float(summary['classification_coverage']):.2f}% of safety-filtered prompts match a tracked style. "
                "The dashboard reports a transparent analytical lens, not a complete ontology. The Evidence Coverage page "
                "adds newer source context without mixing it into the historical DiffusionDB counts."
            )


def main():
    inject_css()
    with st.spinner("Loading trends..."):
        (
            prompts,
            style_period,
            tools,
            keywords,
            samplers,
            aspect_ratios,
            works,
            references,
            summary,
            examples,
            source_coverage,
            ecosystem,
            benchmark_prompts,
            benchmark_rubric,
            horizon,
            explore_previews,
        ) = load_data()

    styles = sorted(prompts["style"].unique().tolist())
    tool_names = tools["tool"].tolist()
    periods = sorted(prompts["period"].dt.strftime("%Y-%m-%d").unique().tolist())

    selected_styles, selected_period, selected_tool, benchmark_focus, evidence_lens = render_sidebar(
        styles,
        tool_names,
        periods,
    )

    selected_date = pd.to_datetime(selected_period)
    filtered_latest = style_period[
        (style_period["style"].isin(selected_styles)) & (style_period["period"] == selected_date)
    ]
    if filtered_latest.empty:
        filtered_latest = style_period[style_period["period"] == selected_date]

    render_hero(prompts, filtered_latest, summary)
    render_current_trend_horizon(horizon)
    render_visual_trend_playground(
        prompts,
        style_period,
        works,
        explore_previews,
        selected_styles,
        selected_period,
        selected_tool,
    )
    render_visual_highlights(works)
    render_snapshot()
    render_toolchain_snapshot()
    render_evidence_model_snapshot(source_coverage, ecosystem)

    if len(selected_styles) == 1:
        st.success(
            f"Random exploration insight: {selected_styles[0]} on the {selected_period} historical baseline can be inspected alongside "
            f"{selected_tool}. Use the 2024-2026 horizon for current outlook and the gallery for visual evidence."
        )

    pages = [
        "Trend Analytics",
        "Representative Works",
        "Tool Benchmarks",
        "Prompt Language",
        "Creative Strategy",
        "Evidence Coverage",
        "Real References",
    ]
    if "active_page" not in st.session_state:
        st.session_state.active_page = pages[0]

    active_page = st.radio(
        "Dashboard page",
        pages,
        key="active_page",
        horizontal=True,
        label_visibility="collapsed",
    )

    if active_page == "Trend Analytics":
        with st.spinner("Rendering trend analytics..."):
            tab_trends(prompts, style_period, samplers, aspect_ratios, works, selected_styles, selected_period)
            render_trend_confidence(prompts, ecosystem, selected_styles)
    elif active_page == "Representative Works":
        tab_gallery(works, styles)
    elif active_page == "Tool Benchmarks":
        tab_tools(tools, selected_tool, benchmark_focus)
    elif active_page == "Prompt Language":
        tab_keywords(keywords, selected_styles)
    elif active_page == "Creative Strategy":
        tab_strategy(style_period, works, styles)
    elif active_page == "Evidence Coverage":
        tab_evidence_coverage(source_coverage, ecosystem, benchmark_prompts, benchmark_rubric, horizon, evidence_lens)
    elif active_page == "Real References":
        tab_references(references)

    render_data_notes(prompts, summary)

    st.caption(
        "Built by HEDAN | Real prompt statistics derived from DiffusionDB CC0 metadata | "
        "Multi-source evidence layers, Streamlit, Plotly, Pandas, and illustrative local AI-generated concept visuals"
    )


if __name__ == "__main__":
    main()
