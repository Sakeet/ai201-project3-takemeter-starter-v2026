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
When a staff member labels the same posts, we agree on at least 60% of them.

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
