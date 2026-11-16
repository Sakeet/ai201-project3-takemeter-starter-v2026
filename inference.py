"""
TakeMeter inference — loads the trained model ONCE, classifies text.
Run: python inference.py "some comment text here"
"""
import sys
import os
import time
import json
from datetime import datetime, timezone

CANDIDATE_PATHS = [
    "./model", "./saved_model", "./takemeter_model",
    "./distilbert-finetuned", "./results/model", "./model_output",
]

LABELS = ["fact", "claim", "reaction", "joke"]  # from your taxonomy
LOG_PATH = "logs/predictions.jsonl"


def find_model_path():
    for p in CANDIDATE_PATHS:
        if os.path.isdir(p) and os.path.exists(os.path.join(p, "config.json")):
            return p
    return None


def load_model():
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    import torch

    path = find_model_path()
    if path is None:
        print(
            "No saved model found in any of:\n  " + "\n  ".join(CANDIDATE_PATHS) +
            "\n\nFIX: your notebook likely never called model.save_pretrained(...).\n"
        )
        sys.exit(1)

    print(f"Loading model from {path} ...")
    tokenizer = AutoTokenizer.from_pretrained(path)
    model = AutoModelForSequenceClassification.from_pretrained(path)
    model.eval()
    torch.set_num_threads(4)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    with torch.no_grad():  # warm-up so the first real request isn't a cold start
        model(**tokenizer("warm up", return_tensors="pt").to(device))
    return tokenizer, model, device


def classify(text, tokenizer, model, device):
    import torch
    start = time.perf_counter()
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=128).to(device)
    with torch.no_grad():
        logits = model(**inputs).logits
    probs = torch.softmax(logits, dim=-1)[0]
    pred_idx = int(torch.argmax(probs))
    confidence = float(probs[pred_idx])
    latency_ms = (time.perf_counter() - start) * 1000
    label = LABELS[pred_idx] if pred_idx < len(LABELS) else f"label_{pred_idx}"
    return label, confidence, latency_ms


def log_entry(text, label, confidence, latency_ms, error=None):
    os.makedirs("logs", exist_ok=True)
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "input_text": text,
        "predicted_label": label,
        "confidence": confidence,
        "latency_ms": round(latency_ms, 2) if latency_ms is not None else None,
        "error": error,
    }
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")
    return entry


def main():
    if len(sys.argv) < 2:
        print('Usage: python inference.py "some comment text"')
        sys.exit(1)

    text = sys.argv[1]

    try:
        if not text.strip():
            raise ValueError("empty input text")
        if len(text) > 1000:
            raise ValueError(f"input too long ({len(text)} chars, max 1000)")

        tokenizer, model, device = load_model()
        label, confidence, latency_ms = classify(text, tokenizer, model, device)
        entry = log_entry(text, label, confidence, latency_ms)
        print(json.dumps(entry, indent=2))

    except Exception as e:
        log_entry(text, None, None, None, error=str(e))
        print(f"ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()