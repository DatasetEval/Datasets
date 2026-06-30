import pandas as pd

# v1 zh

df = pd.read_csv("source_datasets/jade_benchmark_zh.csv")

VIOLATION_TYPE = {
    "违法犯罪": "Illegal/Criminal",
    "侵犯权益": "Infringement of Rights",
    "歧视偏见": "Discrimination/Bias",
}

df["prompt"] = df["问题"]
df["category"] = "PT0014 Morpho-Syntactic Manipulation"
df["subcategory"] = df["违规类型"].map(VIOLATION_TYPE)
df_f = df[["prompt", "category", "subcategory"]]
df_f.to_csv("formated_datasets/PT0014_Jade_v1_zh.csv", index=False)

print(df_f.shape)

# v1 en

df2 = pd.read_csv("source_datasets/jade_benchmark_en.csv")

VIOLATION_TYPE = {
    "违法犯罪": "Illegal/Criminal",
    "侵犯权益": "Infringement of Rights",
    "歧视偏见": "Discrimination/Bias",
}

df2["prompt"] = df2["问题"]
df2["category"] = "PT0014 Morpho-Syntactic Manipulation"
df2["subcategory"] = df2["违规类型"].map(VIOLATION_TYPE)
df2_f = df2[["prompt", "category", "subcategory"]]
df2_f.to_csv("formated_datasets/PT0014_Jade_v1_en.csv", index=False)

print(df2_f.shape)

# v2 zh easy

df3 = pd.read_csv("source_datasets/jade_benchmark_easy_zh.csv")

VIOLATION_TYPE = {
    "违法犯罪": "Illegal/Criminal",
    "侵害权益": "Infringement of Rights",
    "歧视偏见": "Discrimination/Bias",
}

df3["prompt"] = df3["问题"]
df3["category"] = "PT0014 Morpho-Syntactic Manipulation"
df3["subcategory"] = df3["违规类型"].str.strip().map(VIOLATION_TYPE)
df3_f = df3[["prompt", "category", "subcategory"]]
df3_f.to_csv("formated_datasets/PT0014_Jade_v2_zh_easy.csv", index=False)

print(df3_f.shape)

# v2 zh medium

df4 = pd.read_csv("source_datasets/jade_benchmark_medium_zh.csv")

VIOLATION_TYPE = {
    "违法犯罪": "Illegal/Criminal",
    "侵害权益": "Infringement of Rights",   # v2 spelling
    "侵犯权益": "Infringement of Rights",   # v1 spelling — also appears in v2 files
    "歧视偏见": "Discrimination/Bias",
}


df4["prompt"] = df4["问题"]
df4["category"] = "PT0014 Morpho-Syntactic Manipulation"
df4["subcategory"] = df4["违规类型"].str.strip().map(VIOLATION_TYPE)
df4_f = df4[["prompt", "category", "subcategory"]]
df4_f.to_csv("formated_datasets/PT0014_Jade_v2_zh_medium.csv", index=False)
print(df3_f.shape)