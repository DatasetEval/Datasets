import pandas as pd

df = pd.read_json("source_datasets/instruct-v2.json")

df["prompt"] = df["test_case_prompt"]
df["category"] = "Dangerous Code"
df["subcategory"] = "Instruct"
df["rule"] = df["rule"]

df_f = df[["prompt", "category", "subcategory", "rule"]]
df_f.to_csv("formated_datasets/CODE_instruct-v2.csv", index=False)
print(df_f.shape)   