"""Build auditable dashboard CSV files from the DiffusionDB 2M metadata table.

Download the official CC0 metadata table first:

    curl -L -o /private/tmp/diffusiondb_metadata.parquet \
      https://huggingface.co/datasets/poloclub/diffusiondb/resolve/main/metadata.parquet

Then run:

    python3 scripts/build_real_data.py \
      --metadata /private/tmp/diffusiondb_metadata.parquet \
      --output-dir data
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


SOURCE_NAME = "DiffusionDB 2M metadata.parquet"
SOURCE_URL = "https://huggingface.co/datasets/poloclub/diffusiondb"
SOURCE_PAPER = "https://arxiv.org/abs/2210.14896"
LICENSE = "CC0 1.0"
PROMPT_NSFW_THRESHOLD = 0.1
IMAGE_NSFW_THRESHOLD = 0.1

# The first matched rule wins. Broad rendering terms stay near the end so
# specific visual languages are not swallowed by generic terms such as
# "unreal engine" or "octane render".
STYLE_RULES = [
    (
        "AI Cinematic Storyboard",
        "Cinematic",
        ["storyboard", "cinematic still", "film still", "movie still", "concept frame"],
    ),
    (
        "Luxury Fashion",
        "Commercial",
        ["fashion editorial", "haute couture", "vogue", "luxury", "runway fashion"],
    ),
    (
        "Documentary Realism",
        "Photography",
        ["documentary", "photojournalism", "street photography", "candid photo", "film grain"],
    ),
    (
        "Surreal Editorial",
        "Concept",
        ["surrealism", "surreal", "dreamlike", "impossible architecture", "editorial"],
    ),
    (
        "Retro Futurism",
        "Aesthetic",
        ["retro futurism", "retrofuturism", "vaporwave", "synthwave", "cassette futurism"],
    ),
    (
        "Cyberpunk",
        "Aesthetic",
        ["cyberpunk", "cyborg", "neon city", "neon street"],
    ),
    (
        "Anime",
        "Illustration",
        ["anime", "manga", "studio ghibli"],
    ),
    (
        "Dark Fantasy",
        "Worldbuilding",
        ["dark fantasy", "gothic", "occult", "necromancer", "dark forest"],
    ),
    (
        "Minimalism",
        "Design",
        ["minimalism", "minimalist", "minimal", "negative space"],
    ),
    (
        "3D Render",
        "Rendering",
        ["3d render", "3 d render", "octane render", "unreal engine", "blender", "zbrush", "isometric"],
    ),
]

SAMPLER_NAMES = {
    1: "ddim",
    2: "plms",
    3: "k_euler",
    4: "k_euler_ancestral",
    5: "k_heun",
    6: "k_dpm_2",
    7: "k_dpm_2_ancestral",
    8: "k_lms",
    9: "others",
}


def classify_prompts(prompts: pd.Series) -> pd.DataFrame:
    """Assign one transparent, keyword-rule style label to each matched prompt."""
    lower = prompts.fillna("").str.lower()
    style = pd.Series(pd.NA, index=prompts.index, dtype="string")
    keyword = pd.Series(pd.NA, index=prompts.index, dtype="string")
    intent = pd.Series(pd.NA, index=prompts.index, dtype="string")

    for style_name, intent_name, terms in STYLE_RULES:
        available = style.isna()
        for term in terms:
            matched = available & lower.str.contains(term, regex=False)
            style.loc[matched] = style_name
            keyword.loc[matched] = term
            intent.loc[matched] = intent_name
            available = style.isna()

    return pd.DataFrame({"style": style, "keyword": keyword, "intent": intent})


def create_summary(raw: pd.DataFrame, safe: pd.DataFrame, classified: pd.DataFrame) -> pd.DataFrame:
    timestamp = pd.to_datetime(safe["timestamp"], utc=True)
    recognized = int(classified["style"].notna().sum())
    safe_records = int(len(safe))
    rows = [
        ("source_name", SOURCE_NAME, "Official DiffusionDB 2M text-only metadata table"),
        ("source_url", SOURCE_URL, "Dataset distribution page"),
        ("paper_url", SOURCE_PAPER, "ACL 2023 DiffusionDB paper"),
        ("license", LICENSE, "DiffusionDB dataset license"),
        ("raw_records", int(len(raw)), "Rows in the official metadata parquet table"),
        ("safe_records", safe_records, "Rows after timestamp and NSFW threshold filters"),
        ("classified_records", recognized, "Safe prompts matched by the documented style rules"),
        (
            "classification_coverage",
            round(recognized / safe_records * 100, 2),
            "Percent of safe prompts matched by one tracked style rule",
        ),
        ("first_timestamp_utc", timestamp.min().isoformat(), "First safe record timestamp"),
        ("last_timestamp_utc", timestamp.max().isoformat(), "Last safe record timestamp"),
        (
            "safety_filter",
            f"image_nsfw < {IMAGE_NSFW_THRESHOLD}; prompt_nsfw < {PROMPT_NSFW_THRESHOLD}; timestamp present",
            "Applied before aggregation",
        ),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "note"])


def build(metadata: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    columns = ["timestamp", "prompt", "image_nsfw", "prompt_nsfw", "sampler", "width", "height"]
    raw = pd.read_parquet(metadata, columns=columns)

    safe = raw[
        raw["timestamp"].notna()
        & raw["prompt"].notna()
        & (raw["image_nsfw"] < IMAGE_NSFW_THRESHOLD)
        & (raw["prompt_nsfw"] < PROMPT_NSFW_THRESHOLD)
    ].copy()
    safe["period"] = pd.to_datetime(safe["timestamp"], utc=True).dt.strftime("%Y-%m-%d")

    labels = classify_prompts(safe["prompt"])
    classified = pd.concat([safe[["period", "prompt"]], labels], axis=1)
    classified = classified[classified["style"].notna()].copy()

    signals = (
        classified.groupby(["period", "style", "keyword", "intent"], as_index=False)
        .size()
        .rename(columns={"size": "prompt_count"})
    )
    signals["tool"] = "Stable Diffusion"
    signals["source"] = SOURCE_NAME
    signals = signals[["period", "style", "tool", "keyword", "intent", "prompt_count", "source"]]
    signals.to_csv(output_dir / "prompt_trend_signals.csv", index=False)

    summary = create_summary(raw, safe, pd.concat([safe, labels], axis=1))
    summary.to_csv(output_dir / "dataset_summary.csv", index=False)

    sampler = (
        safe["sampler"]
        .map(SAMPLER_NAMES)
        .fillna("unknown")
        .value_counts()
        .rename_axis("sampler")
        .reset_index(name="prompt_count")
    )
    sampler["share_percent"] = (sampler["prompt_count"] / sampler["prompt_count"].sum() * 100).round(2)
    sampler.to_csv(output_dir / "sampler_distribution.csv", index=False)

    ratio = np.select(
        [safe["width"] > safe["height"], safe["width"] < safe["height"]],
        ["Landscape", "Portrait"],
        default="Square",
    )
    aspect = pd.Series(ratio, name="aspect_ratio").value_counts().rename_axis("aspect_ratio").reset_index(name="prompt_count")
    aspect["share_percent"] = (aspect["prompt_count"] / aspect["prompt_count"].sum() * 100).round(2)
    aspect.to_csv(output_dir / "aspect_ratio_distribution.csv", index=False)

    examples = (
        classified.sort_values(["style", "period", "prompt"])
        .groupby("style", as_index=False)
        .head(2)[["period", "style", "keyword", "prompt"]]
    )
    examples["prompt"] = examples["prompt"].str.slice(0, 320)
    examples.to_csv(output_dir / "prompt_examples.csv", index=False)

    print(summary.to_string(index=False))
    print(f"\nWrote {len(signals):,} aggregated trend rows to {output_dir / 'prompt_trend_signals.csv'}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metadata", type=Path, required=True, help="Path to official DiffusionDB metadata.parquet")
    parser.add_argument("--output-dir", type=Path, default=Path("data"))
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    build(args.metadata, args.output_dir)
