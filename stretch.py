"""
Capstone stretch: latency breakdown + load observation.
Run: python stretch.py
"""
import json, os, statistics, time
from concurrent.futures import ThreadPoolExecutor
from time import perf_counter
import torch
from inference import load_model, log_entry, LABELS, LOG_PATH

INPUTS = [
    "Kohli's cover drive is the best shot in world cricket",
    "What a catch by Jadeja, absolute scenes",
    "Koach still unbeaten at Trivandrum",
    "England's bazball won't work in Australia",
    "Starc took 6 wickets today, what a spell",
    "Bumrah is the best fast bowler of this generation",
    "Can't believe we lost that from there",
    "Rohit retiring from T20Is was the right call",
    "Imagine paying for tickets and watching rain all day",
    "Root has more Test runs than any active player",
]

def med(xs): return round(statistics.median(xs), 2)
def p95(xs): return round(sorted(xs)[int(0.95 * (len(xs) - 1))], 2)

def log_lines():
    if not os.path.exists(LOG_PATH): return 0
    with open(LOG_PATH, encoding="utf-8") as f: return sum(1 for _ in f)

# ---------- 1. Latency breakdown ----------
t0 = perf_counter()
tokenizer, model, device = load_model()
load_ms = (perf_counter() - t0) * 1000

def timed_predict(text):
    a = perf_counter()
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=128).to(device)
    b = perf_counter()
    with torch.no_grad():
        logits = model(**inputs).logits
    c = perf_counter()
    probs = torch.softmax(logits, dim=-1)[0]
    idx = int(torch.argmax(probs)); conf = float(probs[idx]); label = LABELS[idx]
    d = perf_counter()
    log_entry(text, label, conf, (d - a) * 1000)
    e = perf_counter()
    return {"tokenize": (b-a)*1000, "forward": (c-b)*1000,
            "postprocess": (d-c)*1000, "log_write": (e-d)*1000, "total": (e-a)*1000}

stages = {k: [] for k in ["tokenize", "forward", "postprocess", "log_write", "total"]}
for _ in range(3):                      # 3 passes over 10 inputs = 30 predictions
    for t in INPUTS:
        r = timed_predict(t)
        for k in stages: stages[k].append(r[k])

print("=== LATENCY BREAKDOWN (30 predictions, ms) ===")
print(f"one-time model load: {load_ms:.0f} ms")
total_med = med(stages["total"])
for k in ["tokenize", "forward", "postprocess", "log_write", "total"]:
    share = f"{100 * med(stages[k]) / total_med:.0f}%" if k != "total" else ""
    print(f"{k:12s} median {med(stages[k]):8.2f}   p95 {p95(stages[k]):8.2f}   {share}")

# ---------- 2. Load observation ----------
def run_phase(rate_per_sec, n=30):
    gap = 1.0 / rate_per_sec
    before = log_lines()
    errors = []
    with ThreadPoolExecutor(max_workers=10) as pool:
        futures = []
        start = perf_counter()
        for i in range(n):
            futures.append(pool.submit(timed_predict, INPUTS[i % len(INPUTS)]))
            time.sleep(max(0, start + (i + 1) * gap - perf_counter()))
        results = []
        for f in futures:
            try: results.append(f.result()["total"])
            except Exception as ex: errors.append(str(ex))
    wall = perf_counter() - start
    return {"rate": rate_per_sec, "requests": n, "median_ms": med(results), "p95_ms": p95(results),
            "max_ms": round(max(results), 2), "errors": len(errors),
            "log_entries_written": log_lines() - before, "wall_s": round(wall, 1)}

print("\n=== LOAD OBSERVATION (30 requests each) ===")
normal = run_phase(1)
fast = run_phase(10)
for p in (normal, fast):
    print(f"{p['rate']:>2}/s  median {p['median_ms']}ms  p95 {p['p95_ms']}ms  max {p['max_ms']}ms  "
          f"errors {p['errors']}  log entries {p['log_entries_written']}/{p['requests']}  wall {p['wall_s']}s")

with open("capstone_stretch.json", "w", encoding="utf-8") as f:
    json.dump({"load_ms": load_ms, "breakdown": {k: {"median": med(v), "p95": p95(v)} for k, v in stages.items()},
               "load_normal": normal, "load_10x": fast}, f, indent=2)
print("\nSaved capstone_stretch.json")