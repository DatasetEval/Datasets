import pandas as pd

df = pd.read_json("source_datasets/train_aegis.json")

df_input = df[df["prompt"] != "REDACTED"].copy()
df_input["category"] = "Unsafe"
df_input.rename(columns={"prompt_label": "label", 
                         "violated_categories": "subcategory"}, inplace=True)
df_input_f = df_input[["prompt", "label", "category", "subcategory"]]
df_input_f.to_csv("formated_datasets/UNSAFE_Aegis_Content_Safety_PROMPT.csv", index=False)
print(df_input_f.shape)

df_output = df[df["response_label"].isin(["unsafe", "safe"])].copy().drop(columns="prompt")
df_output["category"] = "Unsafe"
df_output.rename(columns={"response_label": "label",
                          "violated_categories": "subcategory",
                          "response": "prompt"}, inplace=True)
df_output_f = df_output[["prompt", "label", "category", "subcategory"]]
df_output_f.to_csv("formated_datasets/UNSAFE_Aegis_Content_Safety_RESPONSE.csv", index=False)
print(df_output_f.shape)