from pathlib import Path
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "formated_datasets"
N_EN_PER_TACTIC = 40   # 10 tactics x 40 = 400 English, + all 100 French

en = pd.read_csv(DATA / "PT0001_CyberAttackAssistance.csv").assign(language="English")
en = en.groupby("subcategory").sample(N_EN_PER_TACTIC, random_state=0)
fr = pd.read_csv(DATA / "PT0104_CyberAttackAssistance_French.csv").assign(language="French")

df = pd.concat([en, fr])
# strip the JSON-like wrapper ({"prompt": "...", or « prompt » : « ... in French) and its closing "}
df["prompt"] = (df.prompt.str.replace(r'^\s*\{\s*["«]\s*prompt\s*["»]\s*:\s*["«]\s*', "", regex=True)
                         .str.replace(r'\s*["»]\s*\}\s*(?=[^}]*$)', " ", regex=True).str.strip())

out = pd.DataFrame({
    "prompt": df.prompt,
    "attack_type": "cyber_" + df.subcategory.str.lower().str.replace(" ", "_"),
    "language": df.language,
}).reset_index(drop=True)
out.insert(0, "ID", [f"CY{i:03d}" for i in range(1, len(out) + 1)])
out.to_csv(DATA / "AZURE_CyberAttackAssistance.csv", index=False)
print(out.shape)