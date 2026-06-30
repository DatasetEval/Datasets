import pandas as pd

df = pd.read_csv("source_datasets/advbench_arabic_with_numbers.csv")
print(df.shape)
for col in df.columns:
    df_col = pd.DataFrame()
    df_col["prompt"] = df[col]
    df_col["category"] = "PT0014 Morpho-Syntactic Manipulation"
    df_col["subcategory"] = "Arabic"
    df_col.to_csv(f"formated_datasets/PT0014_ArabicAdvBench_{col}.csv", index=False)
    print(df_col.shape)