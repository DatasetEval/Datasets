import pandas as pd

N_TOTAL = 515
SEED = 42
# Languages to include (ISO code -> name used in the multilingual file; "en" = mitre_frr.json)
LANGUAGES = {
    "en": "English",
    "fr": "French",
    "de": "German",
    "es": "Spanish",
    "it": "Italian",
    "pt": "Portuguese",
    "hi": "Hindi",
    "th": "Thai",
}
# Drop the ~20 prompts whose benign label is debatable (config changes "not immediately obvious as
# malicious", executing arbitrary code, disabling security alerts, introducing side channels...).
EXCLUDE_AMBIGUOUS = True
AMBIGUOUS = (
    r"arbitrary code|not immediately obvious as malicious|temporarily disable|inadvertent|"
    r"disable (?:a |the )?security|without being detected|evade detection|backdoor|exfiltrat|"
    r"keylog|potentially malicious|could potentially be (?:used|exploited)"
)

en = pd.read_json("source_datasets/mitre_frr.json")
en["original_english_prompt"] = en["mutated_prompt"]
en["speaking_language"] = "English"
ml = pd.read_json("source_datasets/frr_multilingual_machine_translated.json")

df = pd.concat([en, ml], ignore_index=True)
df = df[df["is_malicious"] == False]
df["mutated_prompt"] = df["mutated_prompt"].str.strip()
df = df[df["mutated_prompt"] != ""].drop_duplicates(subset="mutated_prompt")
if EXCLUDE_AMBIGUOUS:
    df = df[~df["original_english_prompt"].str.contains(AMBIGUOUS, case=False)]

# Even split: e.g. 515 over 8 languages -> 3 x 65 + 5 x 64
codes = list(LANGUAGES)
base, extra = divmod(N_TOTAL, len(codes))
quota = {c: base + (1 if i < extra else 0) for i, c in enumerate(codes)}

pools = {
    c: df[df["speaking_language"] == LANGUAGES[c]]
    .sample(frac=1, random_state=SEED)
    .drop_duplicates(subset="original_english_prompt")
    for c in codes
}
used = {}  # original English prompt -> number of languages it was already picked in
out = []
# The 700 translations only come from ~340 distinct English prompts, so some reuse across
# languages is unavoidable. Smallest pools first; within a pool, least-used prompts first.
for code in sorted(codes, key=lambda c: len(pools[c])):
    pool = pools[code].copy()
    if len(pool) < quota[code]:
        raise ValueError(f"{code}: only {len(pool)} prompts, {quota[code]} needed")
    pool["times_used"] = pool["original_english_prompt"].map(used).fillna(0)
    pick = pool.sort_values("times_used", kind="stable").head(quota[code])
    for p in pick["original_english_prompt"]:
        used[p] = used.get(p, 0) + 1
    out.append(pd.DataFrame({
        "ID": [f"MitreFRR{code.upper()}{i:04d}" for i in range(1, len(pick) + 1)],
        "prompt": pick["mutated_prompt"].values,
        "attack_type": "harmless",
        "language": code,
    }))

df_f = pd.concat(out, ignore_index=True)
df_f["order"] = df_f["language"].map({c: i for i, c in enumerate(codes)})
df_f = df_f.sort_values(["order", "ID"]).drop(columns="order")
df_f.to_csv("formated_datasets/AZURE_mitre_multilingual_mix.csv", index=False)
print(df_f.shape)
print(df_f["language"].value_counts().reindex(codes).to_dict())
print("distinct underlying prompts:", len(used), "| picked in 2+ languages:", sum(v > 1 for v in used.values()))