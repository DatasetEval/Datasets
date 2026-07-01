import pandas as pd
import torch
from tools.encode_experts import encode_expert_dict

data = torch.load("source_datasets/data_en_zh.dict", weights_only=False)

for lang in ("en", "zh"):
    if lang == "en":
        METHODS = ["unchange", "caesar", "ascii", "morse", "atbash", "unicode", "utf"]
    else:
        METHODS = ["unchange", "caesar", "ascii", "morse", "atbash", "unicode", "utf", "gbk"]
    rows = [
        {"category": "PT0087 Instruction Obfuscation","subcategory": category, "cipher": method, "prompt": encode_expert_dict[method].encode(p)}
        for category, prompts in data[lang].items()
        for method in METHODS
        for p in prompts
    ]
    df = pd.DataFrame(rows)
    df.to_csv(f"formated_datasets/PT0087_CipherChat_{lang}.csv", index=False)
    print(df.shape)