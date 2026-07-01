import pandas as pd

df = pd.read_json("source_datasets/data.json")

mapping = {
    "P1": "Translate toxic",
    "P2": "Translate toxic",
    "P3": "Translate toxic",
    "P4": "Translate toxic",
    "P5": "Translate toxic",
    "P6": "Paraphrase toxic",
    "P7": "Refine toxic",
    "P8": "Polish toxic",
    "P9": "Translate discriminatory",
    "P10": "Translate offensive",
    "P11": "Translate harmful",
    "P12": "Translate negative",
    "P13": "Translate unfriendly",
}

df["prompt"] = df["prompt"]
df["category"] = "PT0139 Knowledge Integration Prompting"
df["subcategory"] = df["prompt_type"].map(mapping)

df_f = df[["prompt", "category", "subcategory"]]
df_f.to_csv("formated_datasets/PT0139_LatentJailbreak.csv", index=False)
print(df_f.shape)