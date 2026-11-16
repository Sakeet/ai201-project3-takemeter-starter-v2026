"""
Capstone trial runner: tests all 5 criteria once.
Run: python run_trials.py 1   (then 2, then 3)
"""
import sys, os, json, statistics, subprocess
from inference import load_model, classify, log_entry, LOG_PATH

TRIAL = sys.argv[1] if len(sys.argv) > 1 else "1"
PY = sys.executable
REQUIRED = ["timestamp", "input_text", "predicted_label", "confidence", "latency_ms"]

# Criteria 1 + 2: 10 ordinary comments, one process
GENERAL_INPUTS = [
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

# Criterion 3: bad inputs
EMPTY_INPUT = ""
LONG_INPUT = "Kohli is the greatest chaser in ODI history and " * 30  # ~1440 chars

# Criterion 4: fixed input from criteria.md
DETERMINISM_INPUT = "Bumrah's yorkers at the death are just unplayable"

# Criterion 5: the 5 fixed fact inputs from criteria.md
FACT_INPUTS = [
    "Kohli became the first batter to score 50 ODI centuries, in the 2023 World Cup semi-final.",
    "Sachin Tendulkar finished his career with 100 international centuries.",
    "Rohit Sharma's 264 against Sri Lanka in 2014 is the highest individual score in ODI history.",
    "Muttiah Muralitharan took 800 Test wickets, more than any other bowler.",
    "Australia beat India by 6 wickets in the 2023 World Cup final in Ahmedabad.",
]


def read_log():
    if not os.path.exists(LOG_PATH):
        return []
    with open(LOG_PATH, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def run_cli(text):
    """Run inference.py as a separate command and return any new log entries."""
    before = len(read_log())
    proc = subprocess.run([PY, "inference.py", text], capture_output=True,
                          text=True, encoding="utf-8", errors="replace")
    return proc, read_log()[before:]


def safe_fail(text):
    proc, new = run_cli(text)
    crashed = "Traceback" in proc.stderr
    logged_error = len(new) == 1 and bool(new[0].get("error"))
    return {"pass": logged_error and not crashed, "crashed": crashed,
            "entry": new[0] if new else None}


print(f"=== TRIAL {TRIAL} ===")
tokenizer, model, device = load_model()

# ---- Criteria 1 + 2 ----
c1_entries = []
for t in GENERAL_INPUTS:
    before = len(read_log())
    label, conf, lat = classify(t, tokenizer, model, device)
    log_entry(t, label, conf, lat)
    new = read_log()[before:]
    c1_entries.append(new[0] if new else None)
c1_pass = sum(1 for e in c1_entries if e and all(e.get(k) is not None for k in REQUIRED))
latencies = [e["latency_ms"] for e in c1_entries if e]
c2_median = statistics.median(latencies)

# ---- Criterion 3 ----
c3_empty = [safe_fail(EMPTY_INPUT) for _ in range(5)]
c3_long = [safe_fail(LONG_INPUT) for _ in range(5)]
c3_empty_pass = sum(r["pass"] for r in c3_empty)
c3_long_pass = sum(r["pass"] for r in c3_long)

# ---- Criterion 4 ----
c4_runs = []
for _ in range(3):
    proc, new = run_cli(DETERMINISM_INPUT)
    e = new[0] if new else {}
    conf = e.get("confidence")
    c4_runs.append((e.get("predicted_label"), round(conf, 2) if conf is not None else None))
c4_pass = len(set(c4_runs)) == 1 and c4_runs[0][0] is not None

# ---- Criterion 5 ----
c5_labels = []
for t in FACT_INPUTS:
    label, conf, lat = classify(t, tokenizer, model, device)
    log_entry(t, label, conf, lat)
    c5_labels.append({"text": t, "label": label, "confidence": round(conf, 3)})
c5_count = sum(1 for r in c5_labels if r["label"] == "fact")

# ---- Summary ----
print("\n=== RESULTS (copy into run log) ===")
print(f"C1 complete log entries:    {c1_pass}/10")
print(f"C2 median latency_ms:       {c2_median:.2f}  (all: {[round(x, 1) for x in latencies]})")
print(f"C3 empty -> logged error:   {c3_empty_pass}/5")
print(f"C3 long  -> logged error:   {c3_long_pass}/5")
print(f"C4 identical outputs:       {'3/3' if c4_pass else 'NOT identical'}  {c4_runs}")
print(f"C5 fact labels:             {c5_count}/5  {[r['label'] for r in c5_labels]}")

out = {
    "trial": TRIAL,
    "c1_pass": c1_pass, "c1_sample_entry": c1_entries[0],
    "c2_median_ms": c2_median, "c2_latencies": latencies,
    "c3_empty_pass": c3_empty_pass, "c3_long_pass": c3_long_pass,
    "c3_empty_sample": c3_empty[0], "c3_long_sample": c3_long[0],
    "c4_runs": c4_runs, "c4_pass": c4_pass,
    "c5_count": c5_count, "c5_labels": c5_labels,
}
with open(f"capstone_trial{TRIAL}.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2)
print(f"\nSaved capstone_trial{TRIAL}.json")