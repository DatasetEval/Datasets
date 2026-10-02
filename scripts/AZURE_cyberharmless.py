"""Harmless cybersecurity-operations prompts from Trend Micro's Primus-Instruct.

Source: trendmicro-ailab/Primus-Instruct (gated, ODC-By), one parquet per task in SOURCE_DIR.
Keeps the user prompt only (the assistant answers are dropped). All security tasks are
single-turn, so the prompt is the first user message, which holds the full request
(the dataset's own `prompt` column is truncated for some tasks).

Output: formated_datasets/FRR_primus_instruct.csv (ID, prompt, attack_type, language)
"""
import pandas as pd

SOURCE_DIR = "source_datasets"
TASKS = [
    "alert_explanation",
    "cmd_analysis",
    "security_doc_qa",
    "security_event_query_generation",
    "terraform_misconfiguration_scan",
    # "general",  # non-security chit-chat, partly Chinese and multi-turn: left out
]

frames = []
for task in TASKS:
    df = pd.read_parquet(f"{SOURCE_DIR}/{task}.parquet")
    df["prompt"] = df["messages"].apply(
        lambda msgs: next(m["content"] for m in msgs if m["role"] == "user").strip()
    )
    frames.append(df[["prompt"]])

df = pd.concat(frames, ignore_index=True)
df = df[df["prompt"] != ""].drop_duplicates(subset="prompt").reset_index(drop=True)

df["ID"] = [f"Primus{i:04d}" for i in range(1, len(df) + 1)]
df["attack_type"] = "harmless"
df["language"] = "en"

df_f = df[["ID", "prompt", "attack_type", "language"]]
df_f.to_csv("formated_datasets/AZURE_primus_instruct.csv", index=False)
print(df_f.shape)