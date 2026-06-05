from pathlib import Path
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
                radial-gradient(circle at top left, rgba(102, 217, 232, .10), transparent 28rem),
                linear-gradient(180deg, {THEME["bg"]} 0%, #0a1018 100%);
            color: {THEME["text"]};
        }}

        section[data-testid="stSidebar"] {{
            background: #0b1017;
            border-right: 1px solid rgba(255,255,255,.08);
            min-width: 18rem;
        }}

        div[data-testid="stMetric"] {{
            background: rgba(16, 22, 32, .78);
            border: 1px solid rgba(255,255,255,.08);
            border-radius: 8px;
            padding: 1rem;
        }}

        .hero {{
            min-height: 330px;
            padding: 2.2rem;
            border-radius: 10px;
            border: 1px solid rgba(255,255,255,.08);
            background:
                radial-gradient(circle at top left, rgba(102, 217, 232, .18), transparent 24rem),
                linear-gradient(135deg, rgba(16, 22, 32, .98), rgba(8, 12, 16, .98));
            background-size: cover;
            background-position: center;
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
            margin-bottom: 1.4rem;
        }}

        .eyebrow {{
            color: {THEME["cyan"]};
            font-size: .82rem;
            font-weight: 700;
            text-transform: uppercase;
            margin-bottom: .55rem;
        }}

        .hero h1 {{
            color: {THEME["text"]};
            font-size: clamp(2rem, 5vw, 4.2rem);
            line-height: 1.03;
            margin: 0;
            max-width: 900px;
        }}

        .hero p {{
            max-width: 780px;
            color: #cbd5df;
            margin-top: .9rem;
            font-size: 1.05rem;
        }}

        .section-title {{
            margin: 2rem 0 .9rem;
            color: {THEME["gold"]};
            font-size: 1.24rem;
            font-weight: 750;
        }}

        .story-card, .source-card, .prompt-card {{
            background: rgba(16, 22, 32, .76);
            border: 1px solid rgba(255,255,255,.08);
            border-radius: 8px;
            padding: 1rem;
            min-height: 100%;
        }}

        .work-card {{
            background: rgba(16, 22, 32, .78);
            border: 1px solid rgba(255,255,255,.08);
            border-radius: 8px;
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
            .hero {{
                min-height: 280px;
                padding: 1.2rem;
            }}

            .hero h1 {{
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
    st.markdown(f"### {title}")


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

        prompts = pd.read_csv(prompt_path)
        tools = pd.read_csv(tool_path)
        works = pd.read_csv(works_path)
        references = pd.read_csv(references_path)
        summary = pd.read_csv(summary_path)
        samplers = pd.read_csv(sampler_path)
        aspect_ratios = pd.read_csv(aspect_path)
        examples = pd.read_csv(examples_path)
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
    return prompts, style_period, tools, keywords, samplers, aspect_ratios, works, references, summary_values, examples


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
            "Analysis date",
            options=periods,
            key="selected_period",
        )
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

        st.markdown("### Data Source")
        st.markdown(
            "[DiffusionDB dataset](https://huggingface.co/datasets/poloclub/diffusiondb)"
        )
        st.markdown(
            "[DiffusionDB research paper](https://arxiv.org/abs/2210.14896)"
        )
        st.caption(
            "Current CSVs are derived from the official DiffusionDB 2M metadata table. "
            "The source contains real user-specified Stable Diffusion prompts and hyperparameters."
        )
        st.caption(
            "Cleaning: valid timestamps only; image_nsfw < 0.1; prompt_nsfw < 0.1; "
            "tracked styles assigned with documented keyword rules; counts aggregated by UTC date."
        )

        if st.session_state.get("random_notice"):
            st.success("Random exploration generated.")

    if not selected_styles:
        selected_styles = styles

    return selected_styles, selected_period, selected_tool, benchmark_focus


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

    st.caption("AI Visual Culture Research Dashboard")
    st.title("AI Visual Trend Dashboard")
    st.write(
        "Explore real Stable Diffusion prompt signals, visual styles, tool capabilities, "
        "representative concept images, and short-horizon creative directions."
    )

    metric_1, metric_2, metric_3, metric_4 = st.columns(4)
    metric_1.metric("Top Tracked Style", str(top_style["style"]), f'{float(top_style["popularity"]):.1f} index')
    metric_2.metric("Fastest Daily Growth", str(fastest_style.name), f'{int(fastest_style["growth"]):+,}')
    metric_3.metric("Safe Prompts Analyzed", f"{safe_records:,}", "real DiffusionDB records")
    metric_4.metric("Tracked Style Matches", f"{classified_records:,}", f"{prompts['style'].nunique()} documented rules")

    st.success(
        f"Key insight from {max_period:%Y-%m-%d}: {ranking_sentence} {fastest_style.name} has the largest first-to-last-day "
        f"change ({int(fastest_style['growth']):+,} matched prompts)."
    )
    st.info(
        f"Data credibility note: statistics are derived from the official DiffusionDB 2M metadata table "
        f"({min_period:%Y-%m-%d} to {max_period:%Y-%m-%d} UTC). Safety filtering and tracked-style "
        "classification rules are documented in scripts/build_real_data.py."
    )


def render_snapshot():
    show_section("Research Snapshot")
    c1, c2, c3 = st.columns(3)
    with c1:
        with st.container(border=True):
            st.write("**What is measured?**")
            st.caption("Real DiffusionDB prompts are safety-filtered, classified with documented keyword rules, and aggregated by UTC date.")
    with c2:
        with st.container(border=True):
            st.write("**What is not claimed?**")
            st.caption("The tracked styles are a transparent analytical lens, not a universal ranking of every AI-generated image.")
    with c3:
        with st.container(border=True):
            st.write("**What makes this unique?**")
            st.caption("The dashboard connects real prompt signals to concept images, factual tool capabilities, parameters, and forecasts.")


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
    show_section("Visual Trend Analysis")
    st.caption("Click any line point or ranking bar to inspect the real DiffusionDB keyword matches behind that trend.")
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

    show_section("Real Metadata Profile")
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

    show_section("Exploratory Forecast: Multi-Horizon Style Signals")
    st.caption(
        "Forecasts use each style's daily share of tracked DiffusionDB matches, rather than raw volume. "
        "Recent days receive more weight, uncertainty expands with the horizon, and projections remain exploratory "
        "because the source window is short."
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
                "The dashboard reports a transparent analytical lens, not a complete ontology."
            )


def main():
    inject_css()
    with st.spinner("Loading trends..."):
        prompts, style_period, tools, keywords, samplers, aspect_ratios, works, references, summary, examples = load_data()

    styles = sorted(prompts["style"].unique().tolist())
    tool_names = tools["tool"].tolist()
    periods = sorted(prompts["period"].dt.strftime("%Y-%m-%d").unique().tolist())

    selected_styles, selected_period, selected_tool, benchmark_focus = render_sidebar(
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
    render_toolchain_snapshot()

    if len(selected_styles) == 1:
        st.success(
            f"Random exploration insight: {selected_styles[0]} on {selected_period} can be inspected alongside "
            f"{selected_tool}. Open the gallery and keyword pages to inspect the evidence."
        )

    render_snapshot()

    pages = [
        "Trend Analytics",
        "Representative Works",
        "Tool Benchmarks",
        "Prompt Language",
        "Creative Strategy",
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
    elif active_page == "Representative Works":
        tab_gallery(works, styles)
    elif active_page == "Tool Benchmarks":
        tab_tools(tools, selected_tool, benchmark_focus)
    elif active_page == "Prompt Language":
        tab_keywords(keywords, selected_styles)
    elif active_page == "Creative Strategy":
        tab_strategy(style_period, works, styles)
    elif active_page == "Real References":
        tab_references(references)

    render_data_notes(prompts, summary)

    st.caption(
        "Built by HEDAN | Real prompt statistics derived from DiffusionDB CC0 metadata | "
        "Streamlit, Plotly, Pandas, and illustrative local AI-generated concept visuals"
    )


if __name__ == "__main__":
    main()
