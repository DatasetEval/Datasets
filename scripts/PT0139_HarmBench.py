import pandas as pd

df = pd.read_csv("source_datasets/harmbench_behaviors_text_all.csv")
df = df[df["FunctionalCategory"] == "contextual"]
df["prompt"] = df["ContextString"] + ' ' + df["Behavior"]
df["category"] = "PT0001 Overt Instruction"
df["subcategory"] = df["SemanticCategory"]

df_f = df[["prompt", "category", "subcategory"]]

df_f.to_csv("formated_datasets/PT0139_HarmBench.csv", index=False)

print(df_f.shape)