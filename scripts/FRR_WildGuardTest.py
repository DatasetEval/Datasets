import pandas as pd

df = pd.read_parquet("source_datasets/train-00000-of-00001.parquet").dropna()
df["prompt"] = df["prompt"]
df["category"] = df["adversarial"].map({True: "adversarial", False: "regular"})
df["subcategory"] = df["label"].map({"harmful": "harmful", "unharmful": "harmless"})

df_f = df[["prompt", "category", "subcategory"]]

df_f.to_csv("formated_datasets/FRR_WildGuardTest.csv", index=False)

print(df_f.shape)