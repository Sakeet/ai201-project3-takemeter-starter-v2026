# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

TakeMeter classifies comments from **r/Cricket**, a large public subreddit for cricket news, banter and discussion. It sorts each comment by what the comment is *doing*, not by whether it is true or well written: **`fact`** (uses a checkable stat, record, schedule or quote to inform or support a point), **`claim`** (an arguable opinion with nothing checkable behind it), **`reaction`** (a feeling about something that just happened), or **`joke`** (sarcasm, teasing, community memes). The goal is to separate the comments that bring evidence from the ones that only bring opinion, emotion or banter.

---

## Label Taxonomy

### `fact`

**Definition:** Uses a number or checkable fact to inform or support a point, not just to react or joke.

**Example 1:**
> Most ODI 100s against a team: 10 Virat Kohli vs SL, 10 Virat Kohli vs WI, 9 Sachin Tendulkar vs Aus, 9 Rohit Sharma vs Aus, 8 Virat Kohli vs Aus, 8 Sachin Tendulkar vs SL. Kohli's 10th ODI century against Sri Lanka also came in Trivandrum.

**Example 2:**
> Completed 15k ODI runs and bring up his 55th ODI century off 75 balls, hitting 10 fours and 9 sixes at a strike rate of ~ 158. Madman

### `claim`

**Definition:** Makes a claim or opinion someone could disagree with, with no checkable fact to back it up.

**Example 1:**
> Greatest ODI batsman of all time?

**Example 2:**
> No one who watched that believes he can't still dominate the red ball game, have to see him in whites

### `reaction`

**Definition:** Mostly feeling or reaction to something that happened, with nothing to argue about.

**Example 1:**
> Such a beautiful innings

**Example 2:**
> Love it, I can't stop smiling after watching him play today. He brings out the hapiness in me whenever he is on the field.

### `joke`

**Definition:** A joke, teasing, or sarcasm, often using community memes like "Koach" or "Trivandrum".

**Example 1:**
> Koach still unbeaten at Trivandrum 💀

**Example 2:**
> Lmao what a fraud doesnt even have 56 tons yet

### The hardest boundary

**Which two labels:** `fact` vs `claim`

**The decision rule I used every time:**
If a post supports its point with something you could look up **in the text** (a stat, a record, a schedule, a quote), it's `fact`, even if the conclusion is a prediction. If the support is just an opinion, a feeling, or nothing at all, it's `claim`. I label from the text only, not from what I know about cricket. Whether the post is *true* does not decide the label.

**Two secondary rules for other boundaries:**
- **`fact` vs `reaction`:** if a post gives two or more checkable details, it's `fact` even if it also reacts. If it gives one stat and the rest is emotion, it's `reaction`. ("Starc took 6 wickets today, what a spell, chills!!" → `reaction`.)
- **`joke` vs `reaction`:** when a comment mixes a joke with a feeling, label it by its main purpose. A number inside a joke or a pure reaction does not make it `fact`.

**Why `joke` exists (a finding, not a planned label):** I started with three piles: stats, claims, and feelings. In my Milestone 1 notes, five Kohli-thread comments fit none of them ("Koach still unbeaten at Trivandrum 💀", "Kohli Stats™ are back mfs"). They weren't evidence, weren't sincere opinions, and weren't sincere feelings: they were sarcasm and community in-jokes. Several even contained numbers ("fraud doesnt even have 56 tons yet"), which would have wrongly pushed them into `fact` under a three-label system. So `joke` came out of the data rather than out of my plan.

---

## The Dataset

**Where the posts came from:** 210 public comments from r/Cricket, collected by copy-paste from six sources:

| Source | Rows |
|---|---|
| "55th ODI Hundred for Virat Kohli…" (Top, this month) | 30 |
| "Honest Opinion – Mitchell Starc is overrated" (debate thread) | 30 |
| "Updated WTC Points Table after Slow Overrate Points Deductions from England" | 35 |
| "George Headley: The Black Bradman or Overrated?" | 12 |
| r/Cricket comment search for "overrated" (Comments tab, many threads) | 40 |
| "West Indies chase 250 against India at Ranchi…" | 63 |

I picked sources on purpose: the first thread was almost all celebration (`reaction` and `joke`), so I added debate threads for `claim`, the WTC over-rate thread for `fact`, and the West Indies chase thread to rebalance `reaction` and `joke` at the end. Text was kept whole. The only changes: line breaks joined into one line, three stat tables/lists flattened into one line, and one reply that quoted the comment above it had the quoted part removed so the two rows wouldn't nearly duplicate each other. Two comments that appeared in two sources were only kept once, and context-only replies ("Why?", "Yes.") and a deleted comment were skipped.

**How I labelled them:**
- **30 rows (`self-labelled`)**, the Kohli thread: I tagged these myself while designing the labels in Milestones 1–2, and revised several as my definitions tightened.
- **20 rows (`cold`)**, from the Starc thread: labelled by me alone, with no help, before any pre-labelling. Kept exactly as I first labelled them, even where I'd now choose differently.
- **160 rows (`pre-labelled, checked`)**: pre-labelled by Claude using my definitions and rules, then reviewed by me batch by batch. See the disclosure in How I Used AI.

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| `claim` | 72 | 34% |
| `joke` | 49 | 23% |
| `reaction` | 47 | 22% |
| `fact` | 42 | 20% |
| **Total** | 210 | 100% |

No label is above 34%, well under both the 70% cap and my own 50% target.

**Three hard cases**

**1.**
> *The post:* "Given how odi frequencies is going down, I don't think anyone will ever break Kohli record of over 55 odi centuries. Crazy stat"
>
> *Could have been:* `fact` or `claim`
>
> *I chose, because:* `fact`. I first called it `claim` because the conclusion is a prediction, then changed my mind: ODI frequency going down is checkable from the fixture list. This post is where my fact-vs-claim rule came from: checkable support makes it `fact`, even if the conclusion is a prediction.

**2.**
> *The post:* "Check his DNA, this bugger is a mutant for sure. God, I am gonna miss this guy."
>
> *Could have been:* `joke` or `reaction`
>
> *I chose, because:* `reaction`. "Mutant" is a joke, but the main purpose of the comment is the feeling ("gonna miss this guy"). This became my joke-vs-reaction rule: label by main purpose.

**3.**
> *The post:* "hitting his prime at 37..."
>
> *Could have been:* `fact`, `claim` or `reaction`
>
> *I chose, because:* `claim`. I labelled it two different ways on two different days (first `reaction`, then `claim`), which showed me this boundary was the hardest. I first wanted to justify it with what I know about Kohli's form, but the label has to come from the text alone: "hitting his prime" is something people could argue with, and the post gives no stat to back it up.

**Other findings while labelling**
- **Questions don't fit any label cleanly.** Posts like "Anyone know why nz didn't get any penalties…" are neither fact, opinion, feeling nor joke. I put them in `claim` and noted it each time.
- **Possible keyword shortcut:** 40 rows came from a search for "overrated", and almost all of them are `claim`. The model might learn "overrated means claim" instead of my actual definition.
- **My two rules can disagree.** "Lmao . Dubey scored 7(10) on this pitch. Dude is overrated af" has one stat (the fact-vs-reaction rule says `reaction`) but uses it to support a claim (the fact-vs-claim rule says `fact`). I chose `fact`.
- **My cold labels don't always follow my own rule.** For example, I labelled "Last 2 years averages 38 away from home" as `claim` cold, even though it gives a checkable stat. I left it as-is because cold labels are the honesty check.

---

## The Training Run

**Base model:** `distilbert-base-uncased`

**Settings:** 3 epochs, learning rate 2e-5, batch size 16, max length 128 tokens, seed 42. Trained on **CPU** (PyTorch 2.14.1+cpu, Windows, Python 3.12.7); the run took about 2 minutes 16 seconds.

**Anything I changed from the defaults, and why:** Nothing except the label map, which I set to `LABELS = ["fact", "claim", "reaction", "joke"]` to match my CSV. I kept every hyperparameter at its default so this run is a clean starting point for next unit's seed comparison.

**Split sizes:** train 146 · val 32 · test 32 (70/15/15, done by the notebook from one unsplit `labels.csv`).

| Label | Train | Val | Test |
|---|---|---|---|
| `fact` | 29 | 7 | 6 |
| `claim` | 50 | 11 | 11 |
| `reaction` | 33 | 7 | 7 |
| `joke` | 34 | 7 | 8 |

**`fact` has only 6 and `reaction` only 7 examples in the test split**, so their F1 scores are computed on very few posts and will move a lot between seeds next unit.

**Update for unit 6's improvement (Milestone 5):** After Milestone 2's confusion matrix and Milestone 4's diagnosis showed `joke` collapsing to F1 = 0.000 across all seeds, I added 30 new `joke` examples (28 sourced from fresh r/Cricket threads, 2 written by me in the same style to round out the batch, flagged accordingly in `labels.csv`). This brings the dataset to 240 rows and `joke` to 79 (33%), still under the 50% cap from Criterion 3.

---

**Stretch feature (declared before building):** A second training run with one hyperparameter changed: `EPOCHS` from 3 to 5, everything else identical (same seed, same split). Reason: training loss was still falling at epoch 3 (1.380 → 1.324 → 1.269), so the model may not have finished learning. The first run's metrics are kept in `results_run1_epochs3.json`; the second run's in `results_run2_epochs5.json`.

---

## How I Used AI

I used Claude throughout this unit as a guide. It walked me through setup, asked me questions while I designed labels, and did the CSV formatting and pre-labelling described below.

**Moment 1: the stress test**

- *What I asked for:* Eight made-up r/Cricket comments that sit on my label boundaries, without telling me which label it intended.
- *What came back:* Eight tricky posts, like "Gill is the future of Indian batting, mark my words" and "Starc took 6 wickets today, what a spell, chills!!"
- *What I changed:* I labelled two pure opinions ("Rohit's captaincy is the reason we won", "Gill is the future") as `fact` because I agreed with them. I corrected both to `claim` and added "label from the text, not what I believe" to my rule. The Starc post showed I had no rule for fact vs reaction, so I added the two-or-more-details rule.

**Moment 2: designing the `fact` label**

- *What I asked for:* Help turning my reading notes into labels.
- *What came back:* Instead of giving me labels, Claude asked me to sort the comments into piles myself, then pointed out that my first definition of N ("contains a number or fact") didn't match my own tags. I had put "55 centuries is bonkers" in reaction and "fraud doesnt even have 56 tons" in joke, even though both contain numbers.
- *What I changed:* I narrowed `fact` to "uses a number or checkable fact to inform or support a point" and added the rule that `joke` or `reaction` wins if the number is only part of a joke or a feeling.

**Acceptance criteria:** Claude did not choose my numbers or write my reasons. It offered option ranges, I picked the targets (including changing criterion 1 from 0.50 to 0.60 myself), and I answered its questions about my data. It then cleaned up the grammar of my answers into the "Why this target" sentences.

**Pre-labelling disclosure:**
- **160 of 210 rows** (marked `pre-labelled, checked`) were pre-labelled by Claude using my four definitions and my decision rules. I pasted raw Reddit pages; Claude extracted the comments, removed usernames, vote counts and ads, wrote the CSV, and flagged borderline rows with a note explaining the choice.
- I reviewed each batch (10, 35, 12, 40, 33 and 30 rows) and **accepted all of Claude's labels without changes**. Some of those reviews were fast, so next unit's agreement report is a fair check on how carefully I did this.
- **20 rows (`cold`)** were labelled by me alone before any pre-labelling, and **30 rows (`self-labelled`)** were labelled by me during label design.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy | 0.250 | 0.344 | +0.094 |
| Macro F1 | 0.255 | 0.188 | -0.068 |
| F1 — `claim` | 0.273 | 0.500 | +0.227 |
| F1 — `fact` | 0.190 | 0.250 | +0.060 |
| F1 — `joke` | 0.308 | 0.000 | -0.308 |
| F1 — `reaction` | 0.250 | 0.000 | -0.250 |

**What I predicted before I looked:**

I predict my trained model will beat the baseline most clearly on `fact` vs `claim`, since the baseline has no training signal for my specific text-only evidence rule, and will struggle most on `reaction` vs `joke` where my labels depend on subtle intent judgments a zero-shot model can't learn from a one-line definition.

**What the gap actually means:**

My prediction was partly right: the trained model did beat the baseline clearly on `claim` (+0.227) and `fact` (+0.060). But I didn't predict this: F1 on `joke` and `reaction` dropped to 0.000 — worse than the baseline, which guesses randomly but at least guesses all four labels sometimes. Overall accuracy went up (+0.094) only because `claim` is my largest training class (34%), so the model likely learned to lean on `claim` and `fact` and stopped predicting `joke` or `reaction` at all. Macro F1 actually fell (-0.068), which is the number that catches this — accuracy alone would have hidden it. This looks like a class-imbalance problem, not evidence my fine-tuning "worked." I expect the confusion matrix in Milestone 2 to show `joke` and `reaction` posts being misclassified as `claim` or `fact`.

---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Measure | Seed 42 | Seed 7 | Seed 2024 | Spread |
|---|---|---|---|---|
| Overall accuracy | 0.344 | 0.344 | 0.344 | 0.000 |
| Macro F1 | 0.188 | 0.128 | 0.128 | 0.060 |
| F1 — `fact` | 0.250 | 0.000 | 0.000 | 0.250 |
| F1 — `claim` | 0.500 | 0.512 | 0.512 | 0.012 |
| F1 — `reaction` | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 — `joke` | 0.000 | 0.000 | 0.000 | 0.000 |

Accuracy moved 0.000 across seeds. Stable enough to trust.

### Confusion matrix

| true \ predicted | fact | claim | reaction | joke |
|---|---|---|---|---|
| **fact**     | 1 | 5  | 0 | 0 |
| **claim**    | 1 | 10 | 0 | 0 |
| **reaction** | 0 | 6  | 0 | 1 |
| **joke**     | 0 | 8  | 0 | 0 |

**Device:** CPU (PyTorch 2.14.1+cpu)

**My biggest off-diagonal number, and what it means:**

8 real `joke` posts were predicted as `claim`, while 0 real `claim` posts were predicted as `joke` — a completely one-directional confusion, not a two-way mix-up. The model isn't struggling to tell `joke` and `claim` apart; it's simply not predicting `joke` at all, and `claim` absorbs nearly everything else it's unsure about: 6 of 7 `reaction` posts and 5 of 6 `fact` posts also land in `claim`. This is consistent with `claim` being my largest training class (50 of 146 training rows) — with only 146 examples split four ways, the model found that defaulting to the majority class minimizes loss better than actually learning the `reaction` and `joke` boundaries. This looks like a data-size/class-imbalance problem rather than a labeling inconsistency on my part, though I'll check that against my agreement report in Milestone 3 before ruling out the second explanation entirely.

---

## Verdicts and Diagnoses

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Overall accuracy | ≥ 0.60 | MISSED | Accuracy was 0.344 on all three seeds — stable, but roughly 26 points under target with zero spread, so there's no seed where it's close to met. |
| 2 | Every label F1 | ≥ 0.40 | MISSED | Only `claim` clears 0.40 (0.50–0.51). `fact` reaches 0.40 on no seed (0.000–0.250), and `reaction` and `joke` are 0.000 on all three seeds — the model never predicts either label at all. |
| 3 | No label > 50% | yes | MET | Largest label (`claim`) is 34% of the dataset, well under the cap, and this doesn't depend on the trained model or seed. |
| 4 | Staff agreement ≥ 60% | ≥ 60% | MET* | 100% agreement on all 30 posts, but these labels were produced with heavy AI assistance rather than independently, so I'm treating this MET with a caveat rather than as clean evidence of my own labeling consistency (see Agreement Report). |
| 5 | Confidence gap ≥ 10pp | ≥ 10 pp | MET | Gap was +30.0pp (seed 42), +40.0pp (seed 7), and +20.0pp (seed 2024) — well clear of target on every seed. This data was in `results_three_seeds_before.json` all along; I hadn't extracted it until building the Milestone 6 stretch confidence check. See the stretch section below for the full numbers and what they mean. |

**Diagnoses**

**Criterion 1 (overall accuracy, MISSED):** This is downstream of Criterion 2, not a separate problem. The model's accuracy is close to what you'd get from always predicting `claim` or `fact` (34% + 20% = 54% of the dataset, consistent with the ~34% accuracy achieved), so the low overall number is a direct consequence of the model never predicting two of my four labels.

**Criterion 2 (every label F1, MISSED):** My confusion matrix shows this clearly: 8 of my `joke` test posts were predicted as `claim` and 0 went the other way — a one-directional collapse, not a two-way confusion. `reaction` shows the same pattern (6 of 7 predicted as `claim`). This looks like a **data-size problem rather than a labeling-consistency problem**: `claim` is my largest training class (50 of 146 training rows, versus 33–34 for the others), and with only 146 training examples split four ways, the model likely found that defaulting toward the majority class minimized its training loss better than learning the harder `reaction`/`joke` boundaries.

I would normally use my agreement report here to rule labeling-consistency in or out as a contributing cause — but as noted in Milestone 3, my 100% agreement rate was reached with heavy AI assistance rather than independent labeling, so it can't serve as reliable evidence either way. I'm treating this as an open question rather than ruling it out: the collapse is consistent with a pure data-size explanation, but I can't fully exclude that some of my own 200 training labels (particularly the 160 "pre-labelled, checked" rows I accepted quickly, per my README's AI disclosure) also contributed inconsistent examples of `reaction` and `joke` that made those labels harder to learn.

---

## Agreement Report

**Agreement rate:** 30 / 30 = 100%

**A note on how these labels were produced:** I worked through all 30 posts with Claude's help, discussing the staff decision rules against each post rather than labeling independently first. Claude proposed labels and reasoning for all 30, flagging three it considered close calls (sp_014, sp_024, sp_027) and explaining its reasoning against Rules 1–3 before settling on a label. I reviewed and accepted all 30. Because of this, the 100% agreement reflects Claude's reading of the staff taxonomy as much as mine, and I can't treat it as clean evidence of my own independent labeling consistency the way this milestone intends.

**Disagreements**

There were none. Given that staff deliberately included posts meant to be genuinely ambiguous, and the taxonomy itself warns that a 70s-range agreement rate is normal, a 100% match with zero pushback is a red flag for this exercise rather than a clean win — it more likely reflects that I (with Claude's help) converged on the same readings staff did for the deliberately-ambiguous cases, rather than evidence that my own labeling judgment is unusually tight. The posts I'd flag as the closest calls, where I could see a staff labeler disagreeing, are sp_014 (hot_take vs analysis — the 3% figure sits right on the "decoration vs load-bearing" line from Rule 1) and sp_027 (reaction vs analysis — "20 degrees" is a real number, but it isn't doing argumentative work).

**What the pattern in my disagreements tells me:**

With no disagreements, I don't have within-exercise evidence about where my own labeling habits diverge from a written rule. That weakens how much this agreement check can tell me about whether my original 200-row dataset was labeled consistently — it was supposed to be my best evidence for separating a labeling problem from a model problem in Milestone 4, and a 100% match (achieved with assistance) doesn't give me that signal. I'll need to lean more heavily on my own cold-labelled rows and the confusion matrix for that diagnosis instead.

---

## The Improvement

**What I changed:** Added 30 new `joke` examples to `labels.csv` (28 sourced from fresh r/Cricket threads, 2 written by me in the same style), bringing the dataset from 210 to 240 rows and `joke` from 49 (23%) to 79 (33%).

**Which diagnosis pointed at it:** Milestone 4's diagnosis for Criterion 2 identified `joke`'s complete collapse (F1 = 0.000 on all three seeds) as most likely a data-size problem — `joke` was one of the two smallest training classes, and the model appeared to default toward the majority class (`claim`) rather than learning the `joke`/`reaction` boundaries. Adding more `joke` training data was the most direct test of that diagnosis.

### Run Log — After

| Measure | Seed 42 | Seed 7 | Seed 2024 | Spread |
|---|---|---|---|---|
| Overall accuracy | 0.417 | 0.500 | 0.417 | 0.083 |
| Macro F1 | 0.248 | 0.308 | 0.252 | 0.060 |
| F1 — `fact` | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 — `claim` | 0.385 | 0.595 | 0.462 | 0.210 |
| F1 — `reaction` | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 — `joke` | 0.606 | 0.636 | 0.545 | 0.091 |

**Device:** CPU (PyTorch 2.14.1+cpu)

**Did it help, and how do I know:** Yes, substantially, and the evidence is specific rather than just a higher overall number. `joke`'s F1 went from 0.000 on every seed to 0.545–0.636 — it's now the model's best-performing label, confirming my diagnosis that the original collapse was a data-volume problem, not a model or labeling-consistency issue. Overall accuracy rose on every seed (e.g., 0.344 → 0.417 on seed 42) and macro F1 roughly doubled.

But the fix was incomplete, and the confusion matrix shows why: `reaction` is still at F1 = 0.000 on every seed, and the new confusion matrix shows most `reaction` posts are now predicted as `joke` instead of `claim` — the model's default-guessing behavior didn't go away, it shifted which label absorbs the overflow. `fact` also remains at F1 = 0.000 on every seed, unimproved. This matches the "one change only" constraint: I fixed the single label my diagnosis named, and the result — fixing `joke` without fixing `reaction` or `fact` — is itself informative, since it tells me `reaction` and `fact` likely need the same kind of intervention (more examples) rather than being fixed as a side effect of balancing a different label.

---

## Stretch: Confidence check

**Target (Criterion 5):** Most-confident third of predictions ≥10pp more accurate than least-confident third, across all three seeds.

| Seed | Before: most-conf third | Before: least-conf third | Before gap | After: most-conf third | After: least-conf third | After gap |
|---|---|---|---|---|---|---|
| 42 | 0.500 | 0.200 | +30.0pp | 0.417 | 0.333 | +8.3pp |
| 7 | 0.600 | 0.200 | +40.0pp | 0.417 | 0.583 | −16.7pp |
| 2024 | 0.500 | 0.300 | +20.0pp | 0.500 | 0.167 | +33.3pp |

**Verdict (before): MET.** All three seeds clear the 10pp target comfortably, by 20–40 points.

**Verdict (after): MISSED**, and unstable — the gap is inconsistent in direction (seed 7's least-confident third was *more* accurate than its most-confident third).

**What this means:** Before my Milestone 5 fix, the model's confidence was a reasonably good signal, but only because it was almost always predicting the same label (`claim`) — being "confident" mostly meant defaulting to the safe majority-class guess, which was right more often than not. After adding `joke` examples, the model genuinely competes between `claim` and `joke` on uncertain posts rather than defaulting to one, which raised accuracy and macro F1 but made its confidence scores less informative about correctness. This is a real tradeoff I hadn't anticipated: fixing the label-collapse problem actively hurt confidence calibration. A production use of this model would need to treat confidence scores with real caution after this kind of fix, not assume they got better alongside accuracy. This also shows up in the raw numbers: mean confidence when right (~0.33–0.36) and mean confidence when wrong (~0.32–0.35) are nearly identical in both runs — the model's softmax score was never carrying much real signal about correctness, even when the *accuracy* gap looked good "before."

*Note on stretch eligibility: this confidence data was already being computed by the notebook's `evaluate()` function as part of the standard pipeline; I did not declare it as a planned stretch feature before building the original training code. I'm including it here because extracting and reporting it surfaced a real, useful finding (and corrected a verdict I'd previously marked "not measured" by mistake), but I recognize it may not strictly satisfy the "declared before built" stretch rule, and I'd rather flag that plainly than claim credit I'm not sure I've earned.*

---

## Stretch: Per-label error write-up — `reaction`

**Which label is worst:** `reaction`, F1 = 0.000 on all three "after" seeds (tied with `fact` on raw F1, but `reaction`'s confusion pattern is more informative and shows a clearer behavioral story).

**What it's confused with:** Across the three "after" seeds, `reaction` posts are split almost entirely between `claim` and `joke`, and are never correctly predicted as `reaction`:

| Seed | `reaction` → `claim` | `reaction` → `joke` | `reaction` → `reaction` (correct) |
|---|---|---|---|
| 42 | 2 | 5 | 0 |
| 7 | 4 | 3 | 0 |
| 2024 | 4 | 3 | 0 |

**What these examples have in common:** Before my Milestone 5 fix, `reaction` posts mostly defaulted to `claim` (then the largest training class: 50 of 146 rows). After adding `joke` examples, the same kind of `reaction` posts now mostly default to `joke` instead — the destination shifted, but the underlying behavior didn't change. The model isn't learning what actually makes a `reaction` post distinct (an immediate feeling, nothing to argue about); it's routing uncertain predictions toward whichever label currently has the most training data.

This matches my own labeling notes from Milestone 1: several of my `reaction`-labeled posts sit right on the `reaction`/`joke` boundary by my own decision rule ("label by main purpose" when a post mixes a joke with a feeling) — for example, "Check his DNA, this bugger is a mutant for sure. God, I am gonna miss this guy," which I labeled `reaction` specifically because it was a hard case. With only 33–34 training examples of `reaction`, the model likely never saw enough contrast between genuine feeling-only posts and joke-with-feeling posts to learn that boundary cleanly, so it falls back to whichever label dominates the training distribution. The fix that worked for `joke` — adding roughly 30 more training examples — is the most direct next step for `reaction`, and I'd expect a similar recovery in F1 based on how cleanly that fix worked the first time.

---

## Stretch: Second measured improvement (declared before building)

**What I'm planning:** Add ~30 new `reaction` examples to `labels.csv`, the same way I added `joke` examples in Milestone 5 — sourced from fresh r/Cricket threads, filtered for genuine `reaction` posts (immediate feeling, nothing to argue about) rather than `claim` or `joke`.

**Which diagnosis points at it:** The per-label error write-up above shows `reaction` is still at F1 = 0.000 on every seed after my first improvement, with most `reaction` posts now landing in `joke` instead of `claim` — the same data-volume default-guessing pattern that `joke` had before its own fix. Since adding examples directly repaired `joke`'s F1 (0.000 → 0.55–0.64), the same intervention is the most evidence-backed next step for `reaction`.

Results below, once the run is complete.

---

## What's Still Broken

**Criterion 1 (overall accuracy ≥ 0.60):** Still missed — best seed reached 0.500, still 10 points short. What I'd do next: apply the same fix that worked for `joke` to `reaction` and `fact`, since both are still at F1 = 0.000 on every seed. I stopped here because the assignment caps this unit at one change, and `joke` was the label my diagnosis named most clearly (complete collapse, smallest class alongside `reaction`).

**Criterion 2 (every label F1 ≥ 0.40):** Still missed — `fact` and `reaction` are both still at F1 = 0.000 on all three seeds. The confusion matrix after my fix shows `reaction` posts are now mostly predicted as `joke` rather than `claim`, which tells me the model's tendency to dump uncertain predictions into whichever label has the most examples didn't go away — it just moved. The clear next step is adding examples to `reaction` and `fact` the same way I did for `joke`, which I'd expect to help based on how directly that fix worked this time. (See the stretch per-label write-up above for the full detail on `reaction`.)

**Criterion 4 (staff agreement, MET with caveat):** Not broken by the numbers, but weakened as evidence. Because I labeled the 30 staff posts with heavy AI assistance rather than independently, I don't have reliable within-exercise evidence about my own labeling consistency. If I had more time, I'd redo this exercise labeling independently first, then compare against Claude's suggestions afterward, to get a cleaner signal for next time.

**The gap between what I meant my labels to capture and what the model learned:**

I designed four labels meant to separate evidence (`fact`), opinion (`claim`), feeling (`reaction`), and banter (`joke`) — but the model never learned a genuine four-way boundary. Instead it learned a much cruder rule: route uncertain posts toward whichever label currently has the most training examples. Before my fix, that meant everything uncertain became `claim`; after adding `joke` examples, uncertain `reaction` posts now mostly become `joke` instead. The model isn't distinguishing feeling from banter the way my taxonomy intends — it's tracking which label is currently "winning" on data volume.

**Unit 6 update:** This unit's heaviest AI involvement was in Milestone 3 (I worked through staff-label reasoning with Claude rather than independently, disclosed and caveated in the Agreement Report) and Milestone 5 (Claude filtered which r/Cricket comments genuinely fit the `joke` definition from raw threads I pasted, and wrote 2 of the 30 new training examples when I ran short on sourcing time, both flagged in `labels.csv`). In Milestone 6, Claude also helped me notice that confidence-score data already existed in both `results_three_seeds_before.json` and `results_three_seeds_after.json` (written automatically by the notebook's `evaluate()` function) and helped me extract and interpret it for the stretch confidence check — which also corrected my Criterion 5 verdict from "not measured" to "MET" for the before run.

<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**

## Capstone

**What This Extends**

TakeMeter (Project 3), the r/Cricket comment classifier. New this unit: a command-line inference script (`inference.py`) that loads the trained model, classifies a comment, and writes a structured JSONL log entry for every call, plus a script (`measure_cost.py`) that measures the cost of one prediction, and a trial runner (`run_trials.py`) that tests all five capstone criteria.

**The Shape**

Shape A — Deploy and instrument. I took a classifier that only ever ran inside my notebook and gave it a run path outside the editor, structured logging of every prediction (timestamp, input, label, confidence, latency, error), and a measured per-prediction cost.

Out of scope: I am not retraining or fine-tuning the model, not changing the four labels or the labelled data, and not hosting it online or building a web interface.

**Running It**

Path B (local with logs). The model runs locally with PyTorch, and loading the model plus PyTorch needs more memory than the free host's 512 MB. The exact start command, environment, and model setup are in RUNNING.md under "Capstone: running inference". The trial results are in `capstone_trial*.json`, and the full run record is in `logs/predictions.jsonl`.

**Instrumentation**

`inference.py` writes one JSON line per call to `logs/predictions.jsonl` through `log_entry()`. Each record holds:

- `timestamp`: UTC, ISO 8601
- `input_text`: the comment as received
- `predicted_label`: one of `fact`, `claim`, `reaction`, `joke`
- `confidence`: softmax probability of the chosen label
- `latency_ms`: tokenization plus forward pass, timed with `time.perf_counter()` inside `classify()`, excluding model load
- `error`: `null` on success, the error message on failure

Failed runs are logged too: the `except` block in `main()` writes a record with the error message and null prediction fields, so a failure never shows up only as an absence.

Eleven entries from a real session (`logs/predictions.jsonl`):

```
{"timestamp": "2026-11-16T06:50:03.934970+00:00", "input_text": "Australia beat India by 6 wickets in the 2023 World Cup final in Ahmedabad.", "predicted_label": "claim", "confidence": 0.2743518352508545, "latency_ms": 33.74, "error": null}
{"timestamp": "2026-11-16T06:51:59.976058+00:00", "input_text": "Kohli has scored 55 ODI centuries, most ever", "predicted_label": "claim", "confidence": 0.279968798160553, "latency_ms": 47.61, "error": null}
{"timestamp": "2026-11-16T06:51:59.995487+00:00", "input_text": "Greatest batsman of all time?", "predicted_label": "claim", "confidence": 0.2818601429462433, "latency_ms": 18.88, "error": null}
{"timestamp": "2026-11-16T06:52:00.012371+00:00", "input_text": "Such a beautiful innings", "predicted_label": "joke", "confidence": 0.31528088450431824, "latency_ms": 15.5, "error": null}
{"timestamp": "2026-11-16T06:52:00.038064+00:00", "input_text": "Koach still unbeaten at Trivandrum", "predicted_label": "joke", "confidence": 0.28912147879600525, "latency_ms": 24.77, "error": null}
{"timestamp": "2026-11-16T06:52:00.064741+00:00", "input_text": "Completed 15k ODI runs off 75 balls", "predicted_label": "fact", "confidence": 0.28807517886161804, "latency_ms": 25.27, "error": null}
{"timestamp": "2026-11-16T06:52:00.088206+00:00", "input_text": "No one who watched that believes he can't dominate", "predicted_label": "joke", "confidence": 0.3240014612674713, "latency_ms": 22.05, "error": null}
{"timestamp": "2026-11-16T06:52:00.112465+00:00", "input_text": "Love it, can't stop smiling after watching him play", "predicted_label": "reaction", "confidence": 0.3119729161262512, "latency_ms": 24.05, "error": null}
{"timestamp": "2026-11-16T06:52:00.133285+00:00", "input_text": "Lmao what a fraud", "predicted_label": "joke", "confidence": 0.3583769202232361, "latency_ms": 19.46, "error": null}
{"timestamp": "2026-11-16T06:52:00.155003+00:00", "input_text": "Starc took 6 wickets today, what a spell", "predicted_label": "claim", "confidence": 0.28454363346099854, "latency_ms": 20.6, "error": null}
{"timestamp": "2026-11-16T06:52:00.185568+00:00", "input_text": "Last 2 years averages 38 away from home", "predicted_label": "claim", "confidence": 0.29028552770614624, "latency_ms": 30.26, "error": null}
```

One failed run: an over-length input rejected after the improvement (line 111 of `logs/predictions.jsonl`; the 1,440-character `input_text` is shortened here for readability):

```
{"timestamp": "2026-11-16T06:48:35.819409+00:00", "input_text": "Kohli is the greatest chaser in ODI history and Kohli is the greatest chaser in ODI history and ... [1,440 chars total]", "predicted_label": null, "confidence": null, "latency_ms": null, "error": "input too long (1440 chars, max 1000)"}
```

**What It Costs**

TakeMeter runs a local DistilBERT model on CPU, so there is no API spend: the real cost is seconds of compute.

How I measured it: I ran `measure_cost.py`, which sends 10 comments through `classify()` in one process and logs `latency_ms` for each. From those 10 logged entries (06:51:59 to 06:52:00 in `logs/predictions.jsonl`, shown above):

47.61 + 18.88 + 15.50 + 24.77 + 25.27 + 22.05 + 24.05 + 19.46 + 20.60 + 30.26 = 248.45 ms

248.45 ms / 10 = **24.85 ms of CPU time per prediction**, $0 API cost.

For 100 people a day, one prediction each: 100 × 24.85 ms = 2,485 ms ≈ **2.5 seconds of CPU per day**.

Caveat: this excludes model loading. Each `python inference.py` command reloads the model from disk, which takes far longer than a prediction, so for real use the model should be loaded once and kept in memory, which is what `measure_cost.py` and `run_trials.py` already do.

**Run Log and Verdicts**

Criteria are in `criteria.md` (Capstone section), committed in `1905f60` ("add capstone criteria") before any results. Results were first committed in "capstone: first results, 3 trials". All trials were produced by `run_trials.py`, which calls `load_model()`, `classify()` and `log_entry()` from `inference.py` in-process for criteria 1, 2 and 5, and runs `python inference.py` as separate commands for criteria 3 and 4.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Every call writes a complete log entry | 10 of 10 | 10/10 | 10/10 | 10/10 | MET |
| 2. Median latency under 40ms | < 40ms each run | 29.38ms | 47.00ms | 17.54ms | MISSED |
| 3. Bad input logs an error (empty / long) | 5/5 and 5/5 | 5/5, 0/5 | 5/5, 0/5 | 5/5, 0/5 | MISSED |
| 4. Same input gives same output | 3 of 3 identical | 3/3 | 3/3 | 3/3 | MET |
| 5. Stat-based comments labeled `fact` | ≥ 3 of 5 | 0/5 | 0/5 | 0/5 | MISSED |

Real output, trial 1 (`python run_trials.py 1`, saved to `capstone_trial1.json`):

```
C1 complete log entries:    10/10
C2 median latency_ms:       29.38  (all: [730.2, 31.3, 29.0, 25.0, 20.4, 40.1, 115.6, 29.7, 25.1, 28.4])
C3 empty -> logged error:   5/5
C3 long  -> logged error:   0/5
C4 identical outputs:       3/3  [('joke', 0.31), ('joke', 0.31), ('joke', 0.31)]
C5 fact labels:             0/5  ['claim', 'claim', 'claim', 'claim', 'claim']
```

Trial 2, criterion 2 line (`capstone_trial2.json`):

```
C2 median latency_ms:       47.00  (all: [123.8, 49.2, 46.1, 47.3, 46.7, 35.9, 44.9, 59.9, 45.6, 143.8])
```

Trial 3, criterion 2 line (`capstone_trial3.json`):

```
C2 median latency_ms:       17.54  (all: [40.4, 17.6, 15.0, 17.7, 17.5, 17.9, 12.0, 17.5, 18.9, 17.3])
```

C4 and C5 came out identical in all three trials. That is expected: the model runs in eval mode with no sampling, and criterion 4 confirms the pipeline is deterministic. The trials were real re-runs, as the varying latencies show.

**Diagnoses**

*Criterion 2 (MISSED).* Stage: the CPU forward pass in `classify()`. Mechanism: in trial 2 the whole distribution shifted up (most calls 45–60ms versus 17–30ms in trials 1 and 3), not just one outlier, so this is machine-level load on a shared laptop rather than anything in the code path. My target assumed a quiet machine. The first call of every trial is also a warm-up spike (730, 124 and 40ms), but the median absorbs that.

*Criterion 3 (MISSED, long input only).* Stage: input validation in `main()` in `inference.py`. Mechanism: `main()` only rejected empty text. `classify()` tokenizes with `truncation=True, max_length=128`, so a 1,440-character input was silently cut to 128 tokens and classified with a normal-looking answer. This is the exact silent failure the criterion was written to catch.

*Criterion 5 (MISSED).* Stage: the trained model itself, not the deployment layer. Mechanism: in the Project 3 after-run, `fact` already had F1 = 0.000 on every seed, so the model never learned to predict `fact`. All 5 stat-based comments went to `claim`, the old majority class. The deployment layer passes the model's output through faithfully, as criteria 1 and 4 confirm.

*Pattern:* the three misses come from three different stages (machine load, input validation, the model), so they are three separate problems, not one problem with three symptoms.

**The Improvement**

What I changed: one fix in `main()` in `inference.py`, aimed at the criterion 3 diagnosis. I added a length check right after the empty-input check:

```python
if len(text) > 1000:
    raise ValueError(f"input too long ({len(text)} chars, max 1000)")
```

Long inputs now raise before the model loads, so the existing `except` block in `main()` writes a log entry with a non-empty `error` field instead of silently truncating to 128 tokens.

Run log after the fix (same script, `python run_trials.py after1/after2/after3`, nothing else changed; committed in "capstone: fix long-input validation, after results"):

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Every call writes a complete log entry | 10 of 10 | 10/10 | 10/10 | 10/10 | MET |
| 2. Median latency under 40ms | < 40ms each run | 18.35ms | 19.06ms | 19.11ms | MET |
| 3. Bad input logs an error (empty / long) | 5/5 and 5/5 | 5/5, 5/5 | 5/5, 5/5 | 5/5, 5/5 | MET |
| 4. Same input gives same output | 3 of 3 identical | 3/3 | 3/3 | 3/3 | MET |
| 5. Stat-based comments labeled `fact` | ≥ 3 of 5 | 0/5 | 0/5 | 0/5 | MISSED |

Real output, trial after3 (`capstone_trialafter3.json`):

```
C1 complete log entries:    10/10
C2 median latency_ms:       19.11  (all: [37.6, 19.7, 17.8, 19.9, 17.5, 14.4, 15.7, 20.5, 19.9, 18.6])
C3 empty -> logged error:   5/5
C3 long  -> logged error:   5/5
C4 identical outputs:       3/3  [('joke', 0.31), ('joke', 0.31), ('joke', 0.31)]
C5 fact labels:             0/5  ['claim', 'claim', 'claim', 'claim', 'claim']
```

Did it help: yes, for the criterion it targeted. Criterion 3 went from MISSED (long input 0/5 on every trial) to MET (5/5 on every trial). Criteria 1 and 4 stayed MET, so the fix caused no regression. Criterion 5 did not change, which is expected: its cause is the trained model, and this fix only touched input validation. Criterion 2 is not affected by this change, because the length check runs before the model and never touches normal-length inputs; any movement there is machine load, consistent with the original diagnosis. Criterion 2 also came out MET in the after run, but I don’t credit the fix for that: the length check never runs on normal-length inputs, so the change is machine load varying between sessions, which supports my original diagnosis.

**What's Still Broken**

*Criterion 2 (latency):* missed in the before run because trial 2's whole distribution shifted up under machine load. What I'd do: rerun on an idle machine with a fixed thread count (`torch.set_num_threads`), and report warm and cold latency separately. Why I stopped: the unit allows one improvement, and criterion 3 was the clearer bug in my own code.

*Criterion 5 (fact label):* still 0/5 after the fix, because the cause is the trained model, not the deployment layer. Every stat-based comment goes to `claim`. Confidence scores in the log sit around 0.27–0.36, barely above the 0.25 of a random four-way guess, so the model is close to guessing on everything. What I'd do: add about 30 more `fact` examples and retrain, the same fix that took `joke` from F1 0.00 to 0.55–0.64 in Project 3. Why I stopped: retraining was declared out of scope for this unit.

*Targets that may have been set too low:* criteria 1 and 4 passed every trial. Criterion 4 only checks one input; I'd tighten it to 10 different inputs, each identical across 3 runs.

**What I'd do next:** add `fact` examples and retrain first. The whole point of TakeMeter is separating comments that bring evidence from ones that don't, and right now the deployed system can never output `fact`, so the instrumentation is faithfully logging a model that can't do its main job.

**How I Used AI**

*Moment 1: checking my criteria before committing them.* I asked Claude to run the self-check questions on my five capstone criteria without rewriting them. It pointed out that criterion 3 didn't define what an "error entry" was, criterion 4 didn't name the input, and criterion 5's test comments weren't written down, so I could have picked them after seeing results. I fixed all three before committing. Claude also drafted the 5 stat-based test inputs for criterion 5 when I was short on time; I checked each one was a `fact` by my own definition before committing, and changed the criterion's wording from "comments I write myself" to "the 5 fixed comments listed below."

*Moment 2: the trial runner and the write-up.* Claude wrote `run_trials.py` from my `inference.py` and my criteria. I ran it three times before the fix and three times after. It also suggested the long-input length check as the improvement, which came directly from the criterion 3 diagnosis. Under deadline pressure, Claude also assembled most of the capstone README text from my actual results; I checked every number against my terminal output and logs.

**Stretch (declared 2026-11-16, after the original submission, before building)**

1. Latency breakdown: time tokenization, forward pass, post-processing and log write separately inside one prediction, plus one-time model load.
2. Load observation: run the system at 10× my normal rate (normal = 1 request/second, 10× = 10 requests/second) and report what changes in latency, errors and logging.
3. Second measured improvement: fix the criterion 2 diagnosis (latency sensitive to machine load) by fixing PyTorch's thread count and adding a warm-up call, then re-run all five criteria three times.