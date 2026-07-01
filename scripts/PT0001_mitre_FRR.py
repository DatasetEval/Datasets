import pandas as pd

df = pd.read_json("source_datasets/mitre_frr.json")
df = df[df["is_malicious"] == False]
df["prompt"] = df["mutated_prompt"]
df["category"] = "PT0001 Overt Instruction"
df["subcategory"] = df["attack_type"]

df_f = df[["prompt", "category", "subcategory"]]
df_f.to_csv("formated_datasets/PT0001_mitre_FRR.csv", index=False)
print(df_f.shape)