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
| Overall accuracy |  |  |  |
| Macro F1 |  |  |  |
| F1 — `label_one` |  |  |  |
| F1 — `label_two` |  |  |  |

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted |  |  |  |
|---|---|---|---|
| **** |  |  |  |
| **** |  |  |  |
| **** |  |  |  |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** ___ / 30 = ___%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



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

