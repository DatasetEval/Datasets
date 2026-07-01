import pandas as pd
import json, os

FILES = [
    "animal_abuse.json",
    "child_abuse.json",
    "controversial_topics,politics.json",
    "discrimination,stereotype,injustice.json",
    "drug_abuse,weapons,banned_substance.json",
    "financial_crime,property_crime,theft.json",
    "hate_speech,offensive_language.json",
    "misinformation_regarding_ethics,laws_and_safety.json",
    "non_violent_unethical_behavior.json",
    "privacy_violation.json",
    "self_harm.json",
    "sexually_explicit,adult_content.json",
    "terrorism,organized_crime.json",
    "violence,aiding_and_abetting,incitement.json",
]

rows = []
for name in FILES:
    path = os.path.join("source_datasets", name)
    subcategory = os.path.splitext(name)[0]                        # "animal_abuse", no extension
    with open(path, encoding="utf-8") as f:
        for line in f:                                             # JSONL: one conversation per line
            line = line.strip()
            if not line:
                continue
            conv = json.loads(line)                                # list of {"role", "content"}
            while conv and conv[-1]["role"] != "user":             # trim trailing assistant so it ends on user
                conv = conv[:-1]
            if not conv:
                continue
            rows.append({
                "prompt": conv[-1]["content"],                     # final coreference user turn
                "category": "PT0128 Multi-Turn Prompting",
                "subcategory": subcategory,
                "messages": json.dumps(conv, ensure_ascii=False),  # full history, ready to send
            })

df_f = pd.DataFrame(rows, columns=["prompt", "category", "subcategory", "messages"])
df_f.to_csv("formated_datasets/PT0128_CoSafe.csv", index=False)
print(df_f.shape)   # (1400, 4)