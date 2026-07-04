import pandas as pd

df = pd.read_json("source_datasets/frr_multilingual_machine_translated.json")
df = df[df["is_malicious"] == False]
df["prompt"] = df["mutated_prompt"]
df["category"] = "PT0001 Overt Instruction"
df["subcategory"] = df["attack_type"]

for language, df_lang in df.groupby("speaking_language"):
    df_f = df_lang[["prompt", "category", "subcategory"]]
    out_path = f"formated_datasets/PT0001_mitre_FRR_{language.lower()}.csv"
    df_f.to_csv(out_path, index=False)
    print(language, df_f.shape)