import pandas as pd

df = pd.read_csv("source_datasets/aart-v1-20231117.csv")

# Filter on Surrogate format only
bare_howto = df["prompt"].str.contains(r"^\s*how (to|do)\b", case=False, regex=True, na=False)
df = df[~bare_howto].copy()        

df["prompt"] = df["prompt"]
df["category"] = "PT0120 Surrogate Format Prompting"
df["subcategory"] = df["crime"]

df_f = df[["prompt", "category", "subcategory"]]
df_f.to_csv("formated_datasets/PT0120_AART.csv", index=False)
print(df_f.shape)