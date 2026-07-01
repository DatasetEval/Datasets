import pandas as pd
import re

MITRE_CATEGORY = {
    "Recon":                "Reconnaissance",
    "Execution":            "Execution",
    "Persistence":          "Persistence",
    "Privilege Escalation": "Privilege Escalation",
    "Evasion":              "Defense Evasion",
    "Discovery":            "Discovery",
    "Lateral Movement":     "Lateral Movement",
    "Collection":           "Collection",
    "C2":                   "Command and Control",
    "Exfil":                "Exfiltration",
}

df = pd.read_json("source_datasets/mitre_prompts_multilingual_machine_translated.json", orient="records")
df["prompt"] = df["mutated_prompt"]
df["category"] = "PT0104 Natural Language Manipulation"
df["subcategory"] = df["mitre_category"].map(MITRE_CATEGORY)

cols = ["prompt", "category", "subcategory"]

for lang, group in df.groupby("speaking_language"):
    safe = re.sub(r"[^A-Za-z0-9]+", "_", lang).strip("_")
    out = f"formated_datasets/PT0104_CyberAttackAssistance_{safe}.csv"
    group[cols].to_csv(out, index=False)
    print(lang, group[cols].shape, "->", out)