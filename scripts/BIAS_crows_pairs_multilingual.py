import pandas as pd

df_en = pd.read_csv("source_datasets/crows_pairs_EN_revised+210.csv", sep="\t", index_col=0)
df_fr = pd.read_csv("source_datasets/crows_pairs_FR_languagearc_contribution+210.csv", sep="\t", index_col=0)

df_en_stereo = df_en[df_en["stereo_antistereo"] == "stereo"]
df_en_stereo["language"] = "en"
df_en_antistereo = df_en[df_en["stereo_antistereo"] == "antistereo"]
df_en_antistereo["language"] = "en"
df_fr_stereo = df_fr[df_fr["stereo_antistereo"] == "stereo"]
df_fr_stereo["language"] = "fr"
df_fr_antistereo = df_fr[df_fr["stereo_antistereo"] == "antistereo"]
df_fr_antistereo["language"] = "fr"

df_en_stereo.rename(columns={"sent_less": "prompt", "sent_more": "prompt_biased"}, inplace=True)
df_en_antistereo.rename(columns={"sent_more": "prompt", "sent_less": "prompt_biased"}, inplace=True)
df_fr_stereo.rename(columns={"sent_less": "prompt", "sent_more": "prompt_biased"}, inplace=True)
df_fr_antistereo.rename(columns={"sent_more": "prompt", "sent_less": "prompt_biased"}, inplace=True)

df_f = pd.concat([df_en_stereo, df_en_antistereo, df_fr_stereo, df_fr_antistereo], axis=0, ignore_index=True)
df_f.rename(columns={"bias_type": "subcategory"}, inplace=True)
df_f["category"] = "Stereotype"

df_f = df_f[["prompt", "prompt_biased", "category", "subcategory", "language"]]

df_f.to_csv("formated_datasets/BIAS_crows_pairs_multilingual.csv", index=False)
