"""
Measures real cost per run: latency in milliseconds, averaged over N predictions.
Since this model runs locally (no API), "cost" = compute time, not dollars.
Run: python measure_cost.py
"""
import statistics
from inference import load_model, classify, log_entry

TEST_INPUTS = [
    "Kohli has scored 55 ODI centuries, most ever",
    "Greatest batsman of all time?",
    "Such a beautiful innings",
    "Koach still unbeaten at Trivandrum",
    "Completed 15k ODI runs off 75 balls",
    "No one who watched that believes he can't dominate",
    "Love it, can't stop smiling after watching him play",
    "Lmao what a fraud",
    "Starc took 6 wickets today, what a spell",
    "Last 2 years averages 38 away from home",
]

N_RUNS = 10

def main():
    print("Loading model once...")
    tokenizer, model, device = load_model()
    print(f"Device: {device}\n")

    latencies = []
    print(f"Running {N_RUNS} predictions...\n")

    for i, text in enumerate(TEST_INPUTS[:N_RUNS], 1):
        label, confidence, latency_ms = classify(text, tokenizer, model, device)
        log_entry(text, label, confidence, latency_ms)
        latencies.append(latency_ms)
        print(f"{i:2d}. {latency_ms:7.2f} ms  ->  {label} ({confidence:.2f})  | {text[:50]}")

    avg = statistics.mean(latencies)
    median = statistics.median(latencies)
    stdev = statistics.stdev(latencies) if len(latencies) > 1 else 0

    print(f"\n--- Cost per run (compute time, {device}) ---")
    print(f"Average latency: {avg:.2f} ms")
    print(f"Median latency:  {median:.2f} ms")
    print(f"Std dev:         {stdev:.2f} ms")
    print(f"Min / Max:       {min(latencies):.2f} ms / {max(latencies):.2f} ms")
    print(f"\nFor your README 'What It Costs' section:")
    print(f"One prediction costs ~{avg:.1f} ms of {device} compute time, measured over {N_RUNS} runs.")
    print(f"At 100 requests/day: ~{avg * 100 / 1000:.2f} seconds of total compute time per day.")

if __name__ == "__main__":
    main()