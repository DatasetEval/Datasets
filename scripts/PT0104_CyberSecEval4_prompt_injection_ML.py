import pandas as pd
import re

df = pd.read_json('source_datasets/prompt_injection_multilingual_machine_translated.json')

df["prompt"] = df["user_input"]
df["system_prompt"] = df["test_case_prompt"]
df["category"] = "PT0199 Textual Boundary Mimicry"
df["subcategory"] = df["injection_variant"]
df["type"] = df["injection_type"]

cols = ["prompt", "system_prompt", "category", "subcategory", "type"]

for lang, group in df.groupby("speaking_language"):
    safe = re.sub(r"[^A-Za-z0-9]+", "_", lang).strip("_")   # Filipino/Tagalog -> Filipino_Tagalog
    out = f"formated_datasets/PT0199_CyberSecEval4_prompt_injection_{safe}.csv"
    group[cols].to_csv(out, index=False)
    print(lang, group[cols].shape, "->", out)