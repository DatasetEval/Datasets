import pandas as pd

## base
df = pd.read_parquet("source_datasets/base-00000-of-00001.parquet", engine="pyarrow")

df.rename(columns={"categories": "subcategory"}, inplace=True)
df["category"] = "PT0003 Semantic Manipulation"

df_f = df[["prompt", "category", "subcategory"]]

df_f.to_csv("formated_datasets/PT0003_SaladBench_base.csv", index=False)
print(df_f.shape)

## enhanced

df2 = pd.read_parquet("source_datasets/attackEnhanced-00000-of-00001.parquet", engine="pyarrow")

df2.rename(columns={"categories": "subcategory"}, inplace=True)
df2["category"] = "PT0003 Semantic Manipulation"

df2_f = df2[["prompt", "category", "subcategory"]]

df2_f.to_csv("formated_datasets/PT0003_SaladBench_enhanced.csv", index=False)
print(df2_f.shape)