import pandas as pd

# Source: https://huggingface.co/datasets/TIGER-Lab/MMLU-Pro (MIT) — test split, renamed
df = pd.read_parquet("source_datasets/mmlu_pro_test.parquet")

# Target topics the guard should block -> MMLU-Pro source subjects
TOPICS = {
    "Medical": df["category"] == "health",
    "Legal": df["category"] == "law",
    "Math": df["category"] == "math",
    "Financial": df["src"].isin([
        "theoremQA-Finance", "ori_mmlu-professional_accounting", "stemez-Business",
    ]),
}
# Off-topic controls the guard should let through: subjects with no overlap with the targets.
# physics / chemistry / engineering are calculation-heavy: hard negatives for the Math guard.
OFF_TOPIC = ["history", "philosophy", "computer science", "physics", "chemistry", "engineering"]

df["label"] = None
for topic, mask in TOPICS.items():
    df.loc[mask, "label"] = topic
off = df[df["category"].isin(OFF_TOPIC)].groupby("category").sample(n=200, random_state=0)
df.loc[off.index, "label"] = "Off-topic"

df_f = df[df["label"].notna()].copy()
df_f["prompt"] = df_f["question"].str.strip()  # question only: options are exam scaffolding, not the topic
# MMLU-Pro reuses some stems with different options; also drop stems that carry no topic on their own
df_f = df_f.drop_duplicates(subset="prompt")
df_f = df_f[~df_f["prompt"].str.match(r"(?i)^which of the following( statements)? (is|are)( not)? \w+\??$")]
df_f["category"] = "Unwanted Topic"
df_f["subcategory"] = df_f["src"].str.replace(r"^ori_mmlu-", "", regex=True)
df_f = df_f[["prompt", "label", "category", "subcategory"]]
df_f.to_csv("formated_datasets/TOPIC_MMLUPro.csv", index=False)
print(df_f.shape)