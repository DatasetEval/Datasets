import pandas as pd

df = pd.read_json('source_datasets/prompt_injection.json')

df["prompt"] = df["user_input"]
df["system_prompt"] = df["test_case_prompt"]
df["category"] = "PT0199 Textual Boundary Mimicry"
df["subcategory"] = df["injection_variant"]
df["type"] = df["injection_type"]
df["judge_question"] = df["judge_question"]

df_f = df[["prompt", "system_prompt", "category", "subcategory", "type", "judge_question"]]
df_f.to_csv("formated_datasets/PT0199_CyberSecEval4_prompt_injection_EN.csv")
print(df_f.shape)