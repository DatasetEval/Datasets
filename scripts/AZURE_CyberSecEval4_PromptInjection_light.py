from pathlib import Path
import pandas as pd

DATA = Path("formated_datasets")
FILES = {
    "English": "PT0199_CyberSecEval4_prompt_injection_EN.csv",
    **{lang: f"PT0104_CyberSecEval4_prompt_injection_{lang}.csv"
       for lang in ["French", "Spanish", "Hindi", "Arabic", "Russian"]},
}
KEEP = ["ignore_previous_instructions", "system_mode", "persuasion"]

df = pd.concat(pd.read_csv(DATA / f).assign(language=lang) for lang, f in FILES.items())
df = df[df.subcategory.isin(KEEP)].rename(columns={"subcategory": "attack_type"})
df.insert(0, "ID", [f"PI{i:03d}" for i in range(1, len(df) + 1)])
df[["ID", "prompt", "attack_type", "language"]].to_csv("formated_datasets/AZURE_CyberSecEval4_prompt_injection.csv", index=False)
print(df.shape)   