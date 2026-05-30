from pathlib import Path
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


def friendly_error(message):
    st.error(message)
    st.stop()


@st.cache_data(show_spinner=False)
def load_data():
    try:
        prompt_path = DATA_DIR / "prompt_trend_signals.csv"
        tool_path = DATA_DIR / "tool_benchmarks.csv"
        works_path = DATA_DIR / "representative_works.csv"
        references_path = DATA_DIR / "real_world_references.csv"

        prompts = pd.read_csv(prompt_path)
        tools = pd.read_csv(tool_path)
        works = pd.read_csv(works_path)
        references = pd.read_csv(references_path)
    except FileNotFoundError as exc:
        friendly_error(
            f"Data file missing: {exc.filename}. Please check the data folder or replace it with your Kaggle export."
        )
    except Exception as exc:
        friendly_error(f"Data loading failed: {exc}")

    required_prompt_cols = {"year", "style", "tool", "keyword", "intent", "prompt_count", "source"}
    if not required_prompt_cols.issubset(prompts.columns):
        missing = ", ".join(sorted(required_prompt_cols - set(prompts.columns)))
        friendly_error(f"Prompt CSV is missing required columns: {missing}")

    prompts["year"] = prompts["year"].astype(int)
    prompts["prompt_count"] = prompts["prompt_count"].astype(int)

    if "visual_evidence" not in works.columns:
        works["visual_evidence"] = (
            "Composition, lighting, color palette, and use-case signals connect this image to the selected trend."
        )

    style_year = prompts.groupby(["year", "style"], as_index=False)["prompt_count"].sum()
    max_count = style_year["prompt_count"].max()
    style_year["popularity"] = (style_year["prompt_count"] / max_count * 100).round(1)

    keywords = (
        prompts.groupby(["keyword", "intent", "tool", "style"], as_index=False)["prompt_count"]
        .sum()
        .rename(columns={"prompt_count": "frequency"})
        .sort_values("frequency", ascending=False)
    )

    growth = prompts.pivot_table(
        index=["keyword", "intent", "tool", "style"],
        columns="year",
        values="prompt_count",
        aggfunc="sum",
        fill_value=0,
    )
    first_year = prompts["year"].min()
    last_year = prompts["year"].max()
    growth["growth"] = ((growth[last_year] - growth[first_year]) / growth[first_year].replace(0, 1) * 100).round(0)
    keywords = keywords.merge(
        growth["growth"].reset_index(),
        on=["keyword", "intent", "tool", "style"],
        how="left",
    )

    segments = pd.DataFrame(
        {
            "creator_segment": [
                "Brand Designers",
                "Indie Filmmakers",
                "Game Concept Artists",
                "Social Creators",
                "Fashion Teams",
            ],
            "primary_need": [
                "commercially safe campaign imagery",
                "cinematic storyboards and visual tone tests",
                "worldbuilding and character exploration",
                "fast distinctive visual hooks",
                "editorial moodboards and look development",
            ],
            "adoption": [72, 81, 88, 93, 67],
            "budget_sensitivity": [58, 74, 69, 82, 51],
        }
    )

    return prompts, style_year, tools, keywords, segments, works, references


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


def render_sidebar(styles, tools, min_year, max_year):
    with st.sidebar:
        st.header("Dashboard Controls")

        if "selected_styles" not in st.session_state:
            st.session_state.selected_styles = styles[:5]
        if "selected_year" not in st.session_state:
            st.session_state.selected_year = max_year
        if "selected_tool" not in st.session_state:
            st.session_state.selected_tool = tools[0]

        if st.button("Random Explore", width="stretch"):
            st.session_state.selected_styles = [random.choice(styles)]
            st.session_state.selected_year = random.randint(min_year, max_year)
            st.session_state.selected_tool = random.choice(tools)
            st.session_state.random_notice = True

        selected_styles = st.multiselect(
            "Visual styles",
            styles,
            default=st.session_state.selected_styles,
            key="selected_styles",
        )
        selected_year = st.slider(
            "Analysis year",
            min_year,
            max_year,
            st.session_state.selected_year,
            key="selected_year",
        )
        selected_tool = st.selectbox(
            "AI tool deep dive",
            tools,
            index=tools.index(st.session_state.selected_tool),
            key="selected_tool",
        )
        benchmark_focus = st.radio(
            "Recommendation priority",
            ["Balanced", "Best image quality", "Commercial safety", "Speed"],
        )

        st.markdown("### Data Source")
        st.markdown(
            "[Stable-Diffusion-Prompts on Kaggle](https://www.kaggle.com/datasets/thedevastator/gustavosta-nlp-research-prompts/data)"
        )
        st.markdown(
            "[900k Diffusion Prompts Dataset](https://www.kaggle.com/datasets/tanreinama/900k-diffusion-prompts-dataset)"
        )
        st.caption(
            "Current CSV is a semi-real aggregate shaped like a prompt analytics export. "
            "Replace it with a Kaggle export for final deployment."
        )
        st.caption(
            "Cleaning: duplicate keyword groups removed, unsafe tags excluded, style labels normalized, yearly prompt counts aggregated."
        )

        if st.session_state.get("random_notice"):
            st.success("Random exploration generated.")

    if not selected_styles:
        selected_styles = styles

    return selected_styles, selected_year, selected_tool, benchmark_focus


def render_hero(prompts, latest_df):
    top_style = latest_df.sort_values("popularity", ascending=False).iloc[0]
    min_year = prompts["year"].min()
    max_year = prompts["year"].max()
    growth_df = (
        prompts[prompts["year"].isin([min_year, max_year])]
        .groupby(["style", "year"], as_index=False)["prompt_count"]
        .sum()
        .pivot(index="style", columns="year", values="prompt_count")
        .fillna(0)
    )
    growth_df["growth"] = growth_df[max_year] - growth_df[min_year]
    fastest_style = growth_df.sort_values("growth", ascending=False).iloc[0]
    total_prompts = int(prompts["prompt_count"].sum())
    anime_2024 = prompts[(prompts["style"] == "Anime") & (prompts["year"] == max_year)]["prompt_count"].sum()
    cyberpunk_2024 = prompts[(prompts["style"] == "Cyberpunk") & (prompts["year"] == max_year)]["prompt_count"].sum()
    documentary_growth = (
        prompts[(prompts["style"] == "Documentary Realism") & (prompts["year"] == max_year)]["prompt_count"].sum()
        - prompts[(prompts["style"] == "Documentary Realism") & (prompts["year"] == min_year)]["prompt_count"].sum()
    )
    storyboard_growth = (
        prompts[(prompts["style"] == "AI Cinematic Storyboard") & (prompts["year"] == max_year)]["prompt_count"].sum()
        - prompts[(prompts["style"] == "AI Cinematic Storyboard") & (prompts["year"] == min_year)]["prompt_count"].sum()
    )

    st.caption("AI Visual Culture Research Dashboard")
    st.title("AI Visual Trend Dashboard")
    st.write(
        "Explore visual styles, prompt language, creator needs, tool positioning, "
        "representative AI-generated works, and forecasted creative directions."
    )

    metric_1, metric_2, metric_3, metric_4 = st.columns(4)
    metric_1.metric("Top Style", str(top_style["style"]), f'{float(top_style["popularity"]):.1f} score')
    metric_2.metric("Fastest Growth", str(fastest_style.name), f'+{int(fastest_style["growth"]):,}')
    metric_3.metric("Prompts Analyzed", f"{total_prompts:,}", "semi-real records")
    metric_4.metric("Data Years", f"{min_year}-{max_year}", f"{prompts['style'].nunique()} styles")

    st.success(
        f"Key insight: Anime-style prompt signals lead the {max_year} sample "
        f"({anime_2024:,} records), while Cyberpunk remains close behind ({cyberpunk_2024:,} records) "
        f"through lighting and atmosphere language. AI Cinematic Storyboard (+{storyboard_growth:,}) "
        f"and Documentary Realism (+{documentary_growth:,}) are emerging signals, suggesting a shift "
        "from pure aesthetics toward narrative, video-oriented, and believable visual storytelling."
    )
    st.info(
        "Data credibility note: this version uses a structured semi-real prompt dataset for demonstration. "
        "The pipeline is designed so the CSV can be replaced with a Kaggle Stable Diffusion prompt export."
    )


def render_snapshot():
    show_section("Research Snapshot")
    c1, c2, c3 = st.columns(3)
    with c1:
        with st.container(border=True):
            st.write("**What changed?**")
            st.caption("Creators are moving from simple style imitation toward mood, camera language, and art direction systems.")
    with c2:
        with st.container(border=True):
            st.write("**What matters now?**")
            st.caption("The strongest prompt signals combine subject, lighting, material, camera, emotion, and usage context.")
    with c3:
        with st.container(border=True):
            st.write("**What makes this unique?**")
            st.caption("The dashboard connects trends to representative images, tool choice, creator segments, and forecasts.")


def render_toolchain_snapshot():
    show_section("AI Toolchain Snapshot")
    st.caption("A quick view of where each tool fits in an AI visual production workflow.")

    toolchain = [
        {
            "stage": "Ideation",
            "tools": "Midjourney / DALL-E",
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
    year = point.get("x")

    if isinstance(style, (int, float)):
        style = point.get("label")

    detail = prompts.copy()
    if style in set(prompts["style"]):
        detail = detail[detail["style"] == style]
    if year in set(prompts["year"]):
        detail = detail[detail["year"] == int(year)]

    if detail.empty:
        st.warning("No detailed records found for the selected chart point.")
        return

    work = works[works["style"].isin(detail["style"].unique())].head(1)
    c1, c2 = st.columns([1, 1.1])
    with c1:
        if not work.empty:
            st.image(str(BASE_DIR / work.iloc[0]["image"]), caption=f'{work.iloc[0]["style"]} | {work.iloc[0]["model"]}')
    with c2:
        st.markdown("#### Drill-down details")
        st.dataframe(
            detail[["year", "style", "tool", "keyword", "intent", "prompt_count"]]
            .sort_values("prompt_count", ascending=False),
            width="stretch",
            hide_index=True,
        )


def tab_trends(prompts, style_year, segments, works, selected_styles, selected_year):
    show_section("Visual Trend Analysis")
    st.caption("Click any line point or ranking bar to inspect the keywords and representative image behind that trend.")
    filtered = style_year[(style_year["style"].isin(selected_styles)) & (style_year["year"] <= selected_year)]
    latest = filtered[filtered["year"] == selected_year]

    col_line, col_bar = st.columns([1.25, 1])
    with col_line:
        fig_trend = px.line(
            filtered,
            x="year",
            y="popularity",
            color="style",
            markers=True,
            title="Style popularity over time",
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
            title=f"Style ranking in {selected_year}",
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

    show_section("Creator Segment Map")
    fig_segment = px.scatter(
        segments,
        x="budget_sensitivity",
        y="adoption",
        size="adoption",
        color="creator_segment",
        hover_data=["primary_need"],
        title="Who is adopting AI visuals, and why?",
        color_discrete_sequence=px.colors.qualitative.Bold,
    )
    st.plotly_chart(plot_layout(fig_segment, height=470), use_container_width=True)


def render_work_card(row):
    with st.container(border=True):
        st.image(str(BASE_DIR / row["image"]), width="stretch")
        st.caption(f'{row["style"]} | {row["recommended_tool"]} | {row["model"]}')
        st.write(f'**{row["representative_work"]}**')
        st.caption(f'Visual evidence: {row["visual_evidence"]}')
        st.caption(row["why_it_represents_the_trend"])
        st.caption(f'Prompt starter: {row["prompt_starter"]}')


def tab_gallery(works, styles):
    show_section("Representative Works Gallery")
    st.caption(
        "Representative images are generated AI concept assets stored locally in assets/. "
        "Each card turns the image into visual evidence by naming composition, lighting, color, and use-case signals."
    )

    gallery_filter = st.selectbox("Gallery filter", ["All styles"] + styles, key="gallery_style_filter")
    gallery_df = works if gallery_filter == "All styles" else works[works["style"] == gallery_filter]

    cols = st.columns(3)
    for index, row in gallery_df.reset_index(drop=True).iterrows():
        with cols[index % 3]:
            render_work_card(row)


def tab_tools(tools, selected_tool, benchmark_focus):
    show_section("AI Tool Comparison")

    radar_metrics = ["popularity", "speed", "quality", "creativity", "ease_of_use", "commercial_safety"]
    fig_radar = go.Figure()
    for _, row in tools.iterrows():
        opacity = 0.86 if row["tool"] == selected_tool else 0.18
        width = 4 if row["tool"] == selected_tool else 1.5
        fig_radar.add_trace(
            go.Scatterpolar(
                r=[row[metric] for metric in radar_metrics],
                theta=["Popularity", "Speed", "Quality", "Creativity", "Ease of Use", "Commercial Safety"],
                fill="toself",
                name=row["tool"],
                opacity=opacity,
                line={"width": width},
            )
        )
    fig_radar.update_layout(polar={"radialaxis": {"visible": True, "range": [0, 100]}})
    radar_event = st.plotly_chart(
        plot_layout(fig_radar, height=540),
        use_container_width=True,
        on_select="rerun",
        selection_mode="points",
        key="tool_radar",
    )

    weights = {
        "Balanced": {"popularity": .15, "speed": .12, "quality": .22, "creativity": .22, "ease_of_use": .14, "commercial_safety": .15},
        "Best image quality": {"popularity": .10, "speed": .08, "quality": .40, "creativity": .25, "ease_of_use": .07, "commercial_safety": .10},
        "Commercial safety": {"popularity": .10, "speed": .12, "quality": .16, "creativity": .12, "ease_of_use": .15, "commercial_safety": .35},
        "Speed": {"popularity": .10, "speed": .40, "quality": .16, "creativity": .14, "ease_of_use": .14, "commercial_safety": .06},
    }
    score_df = tools.copy()
    score_df["score"] = sum(score_df[column] * weight for column, weight in weights[benchmark_focus].items())
    winner = score_df.sort_values("score", ascending=False).iloc[0]

    st.success(
        f'Recommended for {benchmark_focus}: {winner["tool"]}. Best used for {winner["best_for"]}.'
    )

    show_section(f"{selected_tool} Deep Dive")
    tool_info = tools[tools["tool"] == selected_tool].iloc[0]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Quality", int(tool_info["quality"]))
    c2.metric("Creativity", int(tool_info["creativity"]))
    c3.metric("Ease of Use", int(tool_info["ease_of_use"]))
    c4.metric("Commercial Safety", int(tool_info["commercial_safety"]))

    radar_points = selected_points(radar_event)
    if radar_points:
        st.caption(f"Selected radar dimension: {radar_points[0].get('theta', 'metric')}.")


def tab_keywords(keywords, selected_tool):
    show_section("Prompt Language Intelligence")
    filtered_keywords = keywords[keywords["tool"] == selected_tool]

    col_scatter, col_table = st.columns([1.35, 1])
    with col_scatter:
        fig_keywords = px.scatter(
            filtered_keywords,
            x="frequency",
            y="growth",
            size="frequency",
            color="intent",
            hover_name="keyword",
            title=f"Keyword frequency vs. growth for {selected_tool}",
            color_discrete_sequence=px.colors.qualitative.Set3,
        )
        keyword_event = st.plotly_chart(
            plot_layout(fig_keywords),
            width="stretch",
            on_select="rerun",
            selection_mode="points",
            key="keyword_chart",
        )

    with col_table:
        st.dataframe(
            filtered_keywords[["keyword", "style", "intent", "frequency", "growth"]]
            .sort_values(["growth", "frequency"], ascending=False),
            use_container_width=True,
            hide_index=True,
        )

    top_keywords = filtered_keywords.sort_values("frequency", ascending=False).head(8)
    st.write("Top keyword signals:")
    st.caption(" · ".join(top_keywords["keyword"].tolist()))

    points = selected_points(keyword_event)
    if points:
        st.info(f"Selected keyword: {points[0].get('hovertext', points[0].get('text', 'keyword'))}")


def predict_styles(style_year):
    future_years = np.array([2025, 2026, 2027])
    rows = []
    for style, group in style_year.groupby("style"):
        group = group.sort_values("year")
        x = group["year"].to_numpy().reshape(-1, 1)
        y = group["popularity"].to_numpy()

        if LinearRegression is not None:
            model = LinearRegression().fit(x, y)
            preds = model.predict(future_years.reshape(-1, 1))
        else:
            slope, intercept = np.polyfit(group["year"].to_numpy(), y, 1)
            preds = future_years * slope + intercept

        fitted = np.interp(group["year"], group["year"], y)
        residual = float(np.std(y - fitted)) if len(y) > 1 else 3.0
        interval = max(residual, 3.0)
        for year, pred in zip(future_years, preds):
            pred = float(np.clip(pred, 0, 100))
            rows.append(
                {
                    "year": int(year),
                    "style": style,
                    "prediction": round(pred, 1),
                    "lower": round(max(0, pred - interval), 1),
                    "upper": round(min(100, pred + interval), 1),
                }
            )
    return pd.DataFrame(rows)


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
            "tool": "DALL-E",
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
        st.image(str(BASE_DIR / work["image"]), caption=f"{rec['style']} | {rec['tool']}")
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
            st.image(str(BASE_DIR / image), width="stretch")
            st.caption(f"{title}: {caption}")


def tab_strategy(style_year, works, styles):
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
            st.image(str(BASE_DIR / row["image"]), caption=f'{row["style"]} | {row["model"]}')

    show_section("Forecast: 2025-2027")
    st.caption(
        "Forecasts are exploratory and based on linear extrapolation of historical prompt counts. "
        "They are useful for storytelling and comparison, not production forecasting."
    )
    forecast = predict_styles(style_year)
    fig_forecast = go.Figure()
    for style, group in forecast.groupby("style"):
        fig_forecast.add_trace(
            go.Scatter(
                x=group["year"],
                y=group["prediction"],
                mode="lines+markers",
                name=style,
            )
        )
        fig_forecast.add_trace(
            go.Scatter(
                x=list(group["year"]) + list(group["year"])[::-1],
                y=list(group["upper"]) + list(group["lower"])[::-1],
                fill="toself",
                fillcolor="rgba(102,217,232,0.08)",
                line={"color": "rgba(255,255,255,0)"},
                name=f"{style} interval",
                showlegend=False,
            )
        )
    fig_forecast.update_layout(title="Linear prediction with simple uncertainty interval")
    st.plotly_chart(plot_layout(fig_forecast, height=500), use_container_width=True)

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


def render_data_notes(prompts):
    show_section("Data Notes")
    source = prompts["source"].iloc[0]
    c1, c2, c3 = st.columns(3)
    with c1:
        with st.container(border=True):
            st.write("**Current Data**")
            st.caption(f"{source}. The included CSV is a structured demo dataset, not a claim of full production-scale collection.")
    with c2:
        with st.container(border=True):
            st.write("**Processing**")
            st.caption("CSV records are grouped by year, style, tool, keyword, and intent; counts are normalized into popularity scores.")
    with c3:
        with st.container(border=True):
            st.write("**Final Upgrade Path**")
            st.caption("For final grading, replace the prompt CSV with a Kaggle Stable Diffusion export or your own prompt log while keeping the same schema.")


def main():
    inject_css()
    with st.spinner("Loading trends..."):
        prompts, style_year, tools, keywords, segments, works, references = load_data()

    styles = sorted(prompts["style"].unique().tolist())
    tool_names = tools["tool"].tolist()
    min_year = int(prompts["year"].min())
    max_year = int(prompts["year"].max())

    selected_styles, selected_year, selected_tool, benchmark_focus = render_sidebar(
        styles,
        tool_names,
        min_year,
        max_year,
    )

    filtered_latest = style_year[
        (style_year["style"].isin(selected_styles)) & (style_year["year"] == selected_year)
    ]
    if filtered_latest.empty:
        filtered_latest = style_year[style_year["year"] == selected_year]

    render_hero(prompts, filtered_latest)
    render_toolchain_snapshot()

    if len(selected_styles) == 1:
        st.success(
            f"Random exploration insight: {selected_styles[0]} in {selected_year} is linked to "
            f"{selected_tool}. Open the gallery and keyword tabs to inspect the evidence."
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
            tab_trends(prompts, style_year, segments, works, selected_styles, selected_year)
    elif active_page == "Representative Works":
        tab_gallery(works, styles)
    elif active_page == "Tool Benchmarks":
        tab_tools(tools, selected_tool, benchmark_focus)
    elif active_page == "Prompt Language":
        tab_keywords(keywords, selected_tool)
    elif active_page == "Creative Strategy":
        tab_strategy(style_year, works, styles)
    elif active_page == "Real References":
        tab_references(references)

    render_data_notes(prompts)

    st.caption("Built by HEDAN | Streamlit, Plotly, Pandas, and AI-generated representative visuals")


if __name__ == "__main__":
    main()
