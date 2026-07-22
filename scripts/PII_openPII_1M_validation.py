import pandas as pd

df = pd.read_csv("source_datasets/openpii.csv")
df = df[df["privacy_mask"].str.count(r"\|") < 3]

df["category"] = "PII"
df = df.rename(columns={"privacy_mask": "subcategory", "source_text": "prompt"})

df.to_csv("formated_datasets/PII_openPII_1M_validation.csv", index=False, encoding="utf-8")