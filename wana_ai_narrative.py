"""
WANA AI Narrative Layer
-----------------------
Extends the WANA Solar Investment Analysis project with an LLM-generated
narrative: for each investor archetype, it turns the top-3 ranking + Monte
Carlo robustness data into a short, decision-ready written recommendation,
the way a real analyst would hand it to an investment committee.

Usage:
export ANTHROPIC_API_KEY=sk-ant-...
python wana_ai_narrative.py

Requires: pip install anthropic pandas
"""

import os
import pandas as pd
from anthropic import Anthropic

DATAPATH = "data/processed" # adjust to your local WANA repo path

ARCHETYPE_LABELS = {
"developmentbank": "Development Bank",
"ippdeveloper": "IPP Developer",
"hyperscalerppa": "Hyperscaler PPA",
"esgfund": "ESG Fund",
}

client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

def top3_for_archetype(archetypes_df: pd.DataFrame, archetype: str) -> pd.DataFrame:
    subset = archetypes_df[archetypes_df["archetype"] == archetype]
    return subset.sort_values("rank").head(3)

def build_prompt(archetype_label: str, top3: pd.DataFrame) -> str:
    rows = "\n".join(
        f"- {r.country}: score {r.score:.1f}, rank #{int(r.rank)}"
        for r in top3.itertuples()
    )

    return f"""You are a solar investment analyst writing a short note for an
investment committee. Investor type: {archetype_label}.

Top 3 ranked countries (0-100 normalized score, six-lens framework covering
resource, market scale, untapped potential, execution readiness, trajectory,
demand pressure):

{rows}

Write a 3-4 sentence recommendation: which country you'd lead with, why,
and one honest caveat a rigorous analyst would flag (e.g. data limitations,
concentration risk, or a runner-up worth watching). Plain, concrete
language, no marketing fluff."""

def generate_narrative(archetype_label: str, top3: pd.DataFrame) -> str:
    prompt = build_prompt(archetype_label, top3)
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text.strip()

def main():
    archetypes_df = pd.read_csv(f"{DATAPATH}/wana_archetypes_long.csv")

    print("WANA — AI-generated investor briefings\n" + "=" * 40)
    for key, label in ARCHETYPE_LABELS.items():
        top3 = top3_for_archetype(archetypes_df, key)
        if top3.empty:
            continue
        narrative = generate_narrative(label, top3)
        print(f"\n### {label}\n{narrative}")

if __name__ == "__main__":
    main()
