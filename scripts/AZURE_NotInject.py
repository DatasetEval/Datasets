import re
 
import pandas as pd
 
SOURCE_DIR = "source_datasets"
LEVELS = {1: "one", 2: "two", 3: "three"}
 
 
def language(prompt):
    # NotInject has no language column: 3/4 English, the "Multilingual" category is mostly Chinese
    if re.search(r"[一-鿿]", prompt):
        return "zh"
    if re.search(r"[Ѐ-ӿ]", prompt):
        return "ru"
    if re.search(r"[ñ¿¡]|\b(?:por|una|que|los|las|el)\b", prompt, re.I):
        return "es"
    return "en"
 
 
out = []
for n, name in LEVELS.items():
    df = pd.read_parquet(f"{SOURCE_DIR}/NotInject_{name}-00000-of-00001.parquet")
    df["prompt"] = df["prompt"].str.strip()
    df = df[df["prompt"] != ""].drop_duplicates(subset="prompt").reset_index(drop=True)
    out.append(pd.DataFrame({
        "ID": [f"NotInjectX{n}_{i:04d}" for i in range(1, len(df) + 1)],
        "prompt": df["prompt"],
        "attack_type": f"false_alert_keyword_x{n}",
        "language": df["prompt"].map(language),
    }))
 
df_f = pd.concat(out, ignore_index=True)
df_f.to_csv("formated_datasets/AZURE_NotInject.csv", index=False)
print(df_f.shape)
print(df_f["attack_type"].value_counts().sort_index().to_dict())
print(df_f["language"].value_counts().to_dict())