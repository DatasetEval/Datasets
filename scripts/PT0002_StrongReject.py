import pandas as pd

df = pd.read_csv("source_datasets/strongreject_dataset.csv").rename(columns={"category": "old_category"})

df["prompt"] = df["forbidden_prompt"]
df["category"] = "PT0002 Cognitive Control Bypass"
df["subcategory"] = df["old_category"]

df_f = df[["prompt", "category", "subcategory"]]
df_f.to_csv("formated_datasets/PT0002_StrongReject.csv", index=False)
print(df_f.shape)