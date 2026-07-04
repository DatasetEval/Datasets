import pandas as pd

df = pd.read_json("source_datasets/autocomplete.json")

df["prompt"] = df["test_case_prompt"]
df["category"] = "Dangerous Code"
df["subcategory"] = "Instruct"
df["rule"] = df["rule"]

df_f = df[["prompt", "category", "subcategory", "rule"]]
df_f.to_csv("formated_datasets/CODE_autocomplete.csv", index=False)
print(df_f.shape)   