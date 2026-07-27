import pandas as pd

df_eng = pd.read_json("source_datasets/eng.jsonl", lines=True)
df_ara = pd.read_json("source_datasets/ara.jsonl", lines=True)
df_cmn = pd.read_json("source_datasets/cmn.jsonl", lines=True)
df_fra = pd.read_json("source_datasets/fra.jsonl", lines=True)
df_ita = pd.read_json("source_datasets/ita.jsonl", lines=True)
df_nld = pd.read_json("source_datasets/nld.jsonl", lines=True)
df_pol = pd.read_json("source_datasets/pol.jsonl", lines=True)
df_por = pd.read_json("source_datasets/por.jsonl", lines=True)
df_spa = pd.read_json("source_datasets/spa.jsonl", lines=True)
df_hin = pd.read_json("source_datasets/hin.jsonl", lines=True)

df_eng.rename(columns={"functionality": "subcategory", "text": "prompt", "is_hateful": "label", "lang": "language"}, inplace=True)
df_ara.rename(columns={"functionality": "subcategory", "text": "prompt", "is_hateful": "label", "lang": "language"}, inplace=True)
df_cmn.rename(columns={"functionality": "subcategory", "text": "prompt", "is_hateful": "label", "lang": "language"}, inplace=True)
df_fra.rename(columns={"functionality": "subcategory", "text": "prompt", "is_hateful": "label", "lang": "language"}, inplace=True)
df_ita.rename(columns={"functionality": "subcategory", "text": "prompt", "is_hateful": "label", "lang": "language"}, inplace=True)
df_nld.rename(columns={"functionality": "subcategory", "text": "prompt", "is_hateful": "label", "lang": "language"}, inplace=True)
df_pol.rename(columns={"functionality": "subcategory", "text": "prompt", "is_hateful": "label", "lang": "language"}, inplace=True)
df_por.rename(columns={"functionality": "subcategory", "text": "prompt", "is_hateful": "label", "lang": "language"}, inplace=True)
df_spa.rename(columns={"functionality": "subcategory", "text": "prompt", "is_hateful": "label", "lang": "language"}, inplace=True)
df_hin.rename(columns={"functionality": "subcategory", "text": "prompt", "is_hateful": "label", "lang": "language"}, inplace=True)

df = pd.concat([df_eng, df_ara, df_cmn, df_fra, df_ita, df_nld, df_pol, df_por, df_spa, df_hin], ignore_index=True)   
df["category"] = "Hate Speech"
df_f = df[["prompt", "label", "category", "subcategory", "language"]]

df_f.to_csv("formated_datasets/TOXICITY_multi_hate_check.csv", index=False)
print(df_f.shape)
