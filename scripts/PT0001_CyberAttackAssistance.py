import pandas as pd

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

df = pd.read_json("source_datasets/mitre_benchmark_100_per_category_with_augmentation.json", orient="records")
df["prompt"] = df["mutated_prompt"]
df["category"] = "PT0001 Overt Instruction"
df["subcategory"] = df["mitre_category"].map(MITRE_CATEGORY)
df_f = df[["prompt", "category", "subcategory"]]

df_f.to_csv("formated_datasets/PT0001_CyberAttackAssistance.csv", index=False)

print(df_f.shape)