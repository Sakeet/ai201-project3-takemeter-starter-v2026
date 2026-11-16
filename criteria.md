# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

## 1.
Overall accuracy on the held-out test set is at least 0.60 across all three seeds.

**Why this target:** I picked 0.60 because the model would be right 3 out of 5 times, which I'd call useful. With my four labels (fact, claim, reaction, joke), random guessing only gets about 25%, so 0.60 is well above chance.

## 2.
Every label (fact, claim, reaction, joke) has an F1 of at least 0.40 on the held-out set.

**Why this target:** I expect the model to struggle to tell claim, reaction, and joke apart, because in r/Cricket jokes often sound like reactions and sarcasm can sound like a claim. So I set a lower bar per label than for overall accuracy.

## 3.
No label makes up more than 50% of labels.csv.

**Why this target:** In my first thread (the Kohli century), about two-thirds of the comments were reaction or joke. Match and celebration threads lean heavily that way, so if I don't collect from debate threads, reaction could dominate and the model would learn to guess it. Capping at 50% forces me to collect enough fact and claim posts.

## 4.
When a staff member labels the same 30 posts next unit, we agree on at least 60% of them.

**Why this target:** In my stress test I mixed up fact and claim, labeling posts like "Gill is the future of Indian batting" as fact when they had no checkable support. If that boundary is hard for me, someone else may draw it differently, so I set agreement at 60% rather than higher.

## 5.
The model's most-confident third of test predictions is at least 10 percentage points more accurate than its least-confident third.

**Why this target:** Posts the model is unsure about are probably the hard, borderline ones, like "hitting his prime at 37" (claim or reaction?) or posts mixing a stat with a reaction. Those were hard for me too. If the model's confidence means anything, its confident predictions should be right noticeably more often than its unsure ones.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->


---

# Capstone — Deployment Extension Criteria (Shape A)

The five criteria above were for the trained classifier itself, written
before training in unit 5. These five are new, written before any capstone
results exist, and they're about the deployment and instrumentation layer
added this unit — not the model's accuracy, which was already tested in
unit 6.

**System extended:** TakeMeter (the r/Cricket comment classifier)
**Shape:** A — Deploy and instrument

## 1. Every inference call produces a complete log entry

**Target:** 10 of 10 calls to `inference.py` write a log entry to
`logs/predictions.jsonl` containing all five fields: timestamp, input_text,
predicted_label, confidence, latency_ms.

**Why this target:** Instrumentation is the whole point of Shape A. If even
one call fails to log, I can't later reconstruct what the deployed system
did, which defeats the purpose of building this layer at all. 10 of 10 (not
9 of 10) because a logging gap isn't a tolerable failure rate — it's a
silent hole in observability.

## 2. Median latency per prediction stays under 40ms on CPU

**Target:** Across 10 calls to inference.py in one Python process, the median of the latency_ms field is under 40ms. (Model loading time is not counted.)

**Why this target:** My first measurement showed a median of 18.15ms with
one cold-start outlier at 154ms. 40ms gives headroom above my observed
median while still being a real, checkable bar — not so loose that any
result would pass.

## 3. Malformed input fails safely, not silently or with a crash

**Target:** Empty string input and input over 1000 characters both produce
a logged error entry (not a silent success, not an unhandled exception) —
in 5 of 5 tries each.

An entry counts as an error entry if it has an error field that is not empty.

**Why this target:** A deployed service meets bad input eventually. The
risk isn't that it fails — it's that it fails invisibly (a crash with no
log, or a confident-looking wrong answer). 5 of 5 because this is a basic
safety property, not a probabilistic one — it should hold every time.

## 4. Identical input produces identical output

**Target:** Running the input "Bumrah's yorkers at the death are just unplayable" through inference.py as 3 separate commands gives the same predicted_label and the same confidence (to 2 decimal places) all 3 times.

**Why this target:** The model runs in eval mode with no randomness, so
this should hold deterministically. If it doesn't, something in the
deployment layer — not the model — is introducing nondeterminism, and
that's a real bug worth finding.

## 5. The deployed model labels clear stat-based comments as fact

**Target**: Of the 5 fixed comments listed below, each clearly citing a checkable statistic (by my own Milestone 2 definition of fact), at least 3 are labeled fact by the deployed model.

**Why this target:** My cost-measurement run tonight showed 9 of 10 test
posts labeled `claim` or `joke`, including several with clear stats that
should read as `fact`. My Part 2 F1 for `fact` was already weak (only 6
test examples). This criterion checks whether that weakness survives into
the deployed service, using fresh examples I haven't already looked at
the model's answer for.

Test inputs:

“Kohli became the first batter to score 50 ODI centuries, in the 2023 World Cup semi-final.”
“Sachin Tendulkar finished his career with 100 international centuries.”
“Rohit Sharma’s 264 against Sri Lanka in 2014 is the highest individual score in ODI history.”
“Muttiah Muralitharan took 800 Test wickets, more than any other bowler.”
“Australia beat India by 6 wickets in the 2023 World Cup final in Ahmedabad.”