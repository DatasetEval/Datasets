"""Harmless prompts from Databricks Dolly 15k in 4 languages (en, fr, de, es).

Source: argilla/databricks-dolly-15k-curated-multilingual (fr/de/es are machine-translated),
        one parquet per language in source_datasets/:
        en-00000-of-00001-*.parquet, fr-..., de-..., es-...

Output: formated_datasets/FRR_databricks_dolly.csv
        columns ID, prompt, attack_type, language; IDs DollyEN0001, DollyFR0001, ...
"""
import glob
import re

import pandas as pd

N_PER_LANGUAGE = 1000
SEED = 42
LANGUAGES = ["en", "fr", "de", "es"]
# True: the same 1000 Dolly prompts in every language (cross-language comparison).
# False: an independent random sample per language (4000 distinct prompts).
PAIRED = True
# True: also drop prompts touching sensitive topics (politics, weapons, drugs...).
# Matched on the original English prompt; keyword-based, so it drops some innocent ones too.
EXCLUDE_SENSITIVE = False

SENSITIVE = re.compile(
    r"\b(?:kill|murder|weapon|gun|bomb|explosive|shoot|stab|assault|terroris|massacre|genocide|"
    r"nuclear|poison|torture|cocaine|heroin|meth|marijuana|cannabis|lsd|overdose|opioid|fentanyl|drug|"
    r"sex|porn|nude|naked|erotic|prostitut|rape|suicid|self-harm|hack|malware|phishing|exploit|"
    r"ransomware|spyware|steal|theft|robbery|fraud|launder|smuggl|racis|nazi|hitler|slur|"
    r"trump|biden|republican|democrat|politic|immigra|abortion|religio)\w*",
    re.I,
)


def load(lang):
    files = glob.glob(f"source_datasets/{lang}-*.parquet")
    if len(files) != 1:
        raise FileNotFoundError(f"Expected one source_datasets/{lang}-*.parquet, found {files}")
    df = pd.read_parquet(files[0])

    df["instruction"] = df["instruction"].fillna("").str.strip()
    en_text = df.get("instruction_original_en", df["instruction"]).fillna("").str.strip()
    en_context = df.get("context_original_en", df["context"]).fillna("").str.strip()

    # Keep only prompts with no context passage
    keep = (en_context == "") & (df["context"].fillna("").str.strip() == "") & (df["instruction"] != "")
    if EXCLUDE_SENSITIVE:
        keep &= ~en_text.str.contains(SENSITIVE)
    df = df[keep].assign(instruction_en=en_text[keep])
    return df.drop_duplicates(subset="instruction")


frames = {lang: load(lang) for lang in LANGUAGES}

if PAIRED:
    # Dolly ids eligible in every language, deduplicated on the English prompt
    common = set.intersection(*(set(df["id"]) for df in frames.values()))
    pool = frames["en"][frames["en"]["id"].isin(common)].drop_duplicates(subset="instruction_en")
    chosen = pool.sample(n=N_PER_LANGUAGE, random_state=SEED)["id"].tolist()

out = []
for lang, df in frames.items():
    if PAIRED:
        df = df.set_index("id").loc[chosen].reset_index()
    else:
        df = df.sample(n=N_PER_LANGUAGE, random_state=SEED).reset_index(drop=True)
    out.append(pd.DataFrame({
        "ID": [f"Dolly{lang.upper()}{i:04d}" for i in range(1, len(df) + 1)],
        "prompt": df["instruction"],
        "attack_type": "harmless",
        "language": lang,
    }))

df_f = pd.concat(out, ignore_index=True)
df_f.to_csv("formated_datasets/AZURE_databricks_dolly.csv", index=False)
print(df_f.shape)
print(df_f["language"].value_counts().to_dict())