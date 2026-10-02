from pathlib import Path
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "formated_datasets"

# Only encodings that actually transform the text (the others leave it readable in this repo's files)
REAL_CIPHERS = {"en": ["caesar", "morse", "atbash", "ascii"], "zh": ["ascii", "unicode", "utf", "gbk"]}
# Topics whose underlying prompts are benign questions, not attacks
DROP_TOPICS = ["wang", "mental_health", "ethics_and_morality", "prompt_leaking"]

def cipher(lang, n):
    d = pd.read_csv(DATA / f"PT0087_CipherChat_{lang}.csv")
    d = d[d.cipher.isin(REAL_CIPHERS[lang]) & ~d.subcategory.isin(DROP_TOPICS)].drop_duplicates("prompt")
    d = d.sample(n, random_state=0)
    return pd.DataFrame({"prompt": d.prompt.str.strip(), "attack_type": "cipher_" + d.cipher,
                         "language": {"en": "English", "zh": "Chinese"}[lang]})

latent = pd.read_csv(DATA / "PT0139_LatentJailbreak.csv")
latent = pd.DataFrame({"prompt": latent.prompt, "language": "English",
                       "attack_type": "latent_" + latent.subcategory.str.lower().str.replace(" ", "_")})

wg = pd.read_csv(DATA / "FRR_WildGuardTest.csv")
wg = wg[(wg.category == "adversarial") & (wg.subcategory == "harmful")]
wg = pd.DataFrame({"prompt": wg.prompt, "attack_type": "wildguard_adversarial", "language": "English"})

out = pd.concat([cipher("en", 450), cipher("zh", 293), latent, wg]).reset_index(drop=True)
out.insert(0, "ID", [f"CX{i:04d}" for i in range(1, len(out) + 1)])
out[["ID", "prompt", "attack_type", "language"]].to_csv(DATA / "AZURE_Complex.csv", index=False)
print(out.shape)