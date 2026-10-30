import json

import pandas as pd

# Source: https://github.com/particlemedia/RAGTruth (MIT) — dataset/response.jsonl + dataset/source_info.jsonl
# Renamed with a ragtruth_ prefix to avoid generic names in source_datasets/.
responses = pd.read_json("source_datasets/response.jsonl", lines=True, dtype={"source_id": str})
sources = pd.read_json("source_datasets/source_info.jsonl", lines=True, dtype={"source_id": str})


def build_context(row):
    info = row["source_info"]
    if row["task_type"] == "QA":          # MS MARCO: {"question", "passages"}
        return info["passages"]
    if row["task_type"] == "Data2txt":    # Yelp business record: dict -> JSON string
        return json.dumps(info, ensure_ascii=False)
    return info                           # Summary: the news article (plain string)


sources["context"] = sources.apply(build_context, axis=1)
sources["question"] = sources.apply(
    lambda r: r["source_info"]["question"] if r["task_type"] == "QA" else None, axis=1
)

df = responses.merge(sources[["source_id", "task_type", "context", "question"]], on="source_id", how="left")

# Drop truncated answers and incorrect refusals (~1%): they are not faithfulness cases.
df = df[df["quality"] == "good"].copy()

df["response"] = df["response"]  # the text the guardrail must judge = the RAG answer
df["label"] = df["labels"].apply(lambda s: "hallucinated" if len(s) > 0 else "faithful")
df["category"] = "Hallucination"
df["subcategory"] = df["task_type"]  # QA / Summary / Data2txt
# Evident/Subtle x Conflict/Baseless Info, comma-separated like Aegis
df["hallucination_type"] = df["labels"].apply(
    lambda s: ", ".join(sorted({x["label_type"] for x in s})) if s else None
)
# Span-level answer key (character offsets into prompt), for guardrails that highlight instead of block
df["hallucinated_spans"] = df["labels"].apply(
    lambda s: json.dumps(
        [{"start": x["start"], "end": x["end"], "text": x["text"], "type": x["label_type"]} for x in s],
        ensure_ascii=False,
    ) if s else None
)

# Keep only the official test split: many hallucination detectors are fine-tuned on RAGTruth train.
df_f = df[df["split"] == "test"][[
    "response", "context", "question", "label", "category", "subcategory",
    "hallucination_type", "hallucinated_spans", "model",
]]
df_f.to_csv("formated_datasets/HALLU_RAGTruth.csv", index=False)
print(df_f.shape)