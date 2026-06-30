import pandas as pd

# Jailbreak prompts dataset
df = pd.read_csv("source_datasets/jailbreak_prompts_2023_12_25.csv")

df["prompt"] = df["prompt"]
df["category"] = "PT0023 Pragmatic Manipulation"
df["subcategory"] = "Do Anything Now"

df_f = df[["prompt", "category", "subcategory"]]
df_f.to_csv("formated_datasets/PT0023_DoAnythingNow.csv", index=False)
print(df_f.shape)

# Regular prompts dataset
df2 = pd.read_csv("source_datasets/regular_prompts_2023_12_25.csv")

df2["prompt"] = df2["prompt"]
df2["category"] = "Harmless"
df2["subcategory"] = "Real prompts"
df2_f = df2[["prompt", "category", "subcategory"]]
df2_f.to_csv("formated_datasets/PT0023_DoAnythingNow_harmless.csv", index=False)
print(df2_f.shape)

