# Plagiarism & AI-Plag Guidance (worth 6 of 20 marks)

This is the single most point-sensitive and most *avoidable* way to lose marks.
The notice is strict:

- **Similarity must be < 10%** (regular plagiarism) — *mandatory*.
- **AI-plag:** 0–20% → **3M**, 21–30% → 2M, 31–40% → 1M, **> 40% → 0M**.
- **Similarity report → 3M.**
- **No resubmission after Saturday, 10 October 2026.**

> ⚠️ **Read this first.** The report in `report/` was AI-drafted as a *scaffold*:
> correct structure, verified facts, real citations. If you submit it verbatim it
> will score **high on AI-plag** and you will lose up to 6 marks. You must
> **rewrite it in your own words** before submission. The steps below show how to
> keep the substance (and the marks for Methodology/Topic) while driving both
> scores down.

---

## Part A — Getting similarity below 10%

1. **Paraphrase, don't copy.** Go section by section and re-express each paragraph
   in your own phrasing and sentence structure. Change the order of ideas where
   you can. Never paste sentences from the cited web sources.
2. **Quote sparingly and mark it.** If you must use an exact phrase (e.g.
   "80–90% of the tactical work"), put it in quotation marks **and** cite it.
   Short, clearly-quoted, cited strings don't count against you the way unquoted
   copying does.
3. **Cite everything.** Every statistic, claim and definition should carry a
   bracketed reference [n]. The report already has 44 references — keep them.
4. **Write original connective analysis.** Tools flag *matching* text, not *your*
   reasoning. The more of the report that is genuinely your own interpretation
   (why the identity root cause matters, what your PoC numbers mean), the lower
   the similarity.
5. **Rebuild tables/figures as your own.** The figures here are generated from
   your own PoC run — that's original. Describe them in your own words.
6. **Avoid "reference recycling."** Don't copy reference strings from one source;
   the IEEE entries here were assembled independently, which is fine.

## Part B — Getting AI-plag low (aim ≤ 20%, ideally near 0%)

AI detectors flag text that reads as machine-generated: uniform sentence length,
over-smooth transitions, hedging, and generic phrasing. To lower it:

1. **Rewrite in your natural student voice.** Vary sentence length. Use the first
   person plural where appropriate ("we implemented", "we found").
2. **Inject specifics only you have.** Name your group, your asset names, your
   exact `run_demo.py` output on your machine, a sentence about a bug you hit —
   concrete, personal detail reads as human.
3. **Break up perfectly balanced structure.** Real writing is a bit uneven. Merge
   or split paragraphs; add a short aside; remove throat-clearing phrases.
4. **Read it aloud and edit.** Anything that doesn't sound like you — change it.
5. **Don't "AI-paraphrase."** Running the text back through an AI paraphraser
   often *raises* AI-plag. Rewrite by hand.
6. **Re-derive, don't regenerate.** Explain the macaroon attenuation idea from
   your own understanding after reading `poc/nhi_delegation.py`, rather than
   restating the draft.

## Part C — Produce the reports

1. Export your rewritten report to PDF.
2. Run it through the **college-approved tool** (commonly **Turnitin**, which
   gives both a *Similarity* score and an *AI writing* score). Use the tool your
   faculty specifies — don't rely on free web checkers for the official number.
3. If similarity ≥ 10% or AI-plag > 20%, iterate on the flagged sections (the
   tool highlights them) and re-check. **Leave time** — no resubmission after
   10 Oct.
4. Export/download both reports (similarity + AI) and include them in the
   submission package.

## Part D — Quick self-check before you submit

- [ ] I rewrote every section in my own words (no pasted source sentences).
- [ ] Every fact/number has a citation [n].
- [ ] Direct quotes are in quotation marks and cited.
- [ ] Similarity **< 10%** on the official tool.
- [ ] AI-plag **≤ 20%** (target ~0%).
- [ ] Both reports exported and attached.
- [ ] Figures/results are from my own PoC run.

---

### Academic-integrity note

Use this scaffold the way the rubric intends: as research structure and verified
evidence to **learn from and rewrite**, not as a finished submission. The
technical content (the GTG-1002 analysis, the delegation design, the PoC) is
genuinely yours to understand, run, extend, and explain — doing so is exactly
what earns the Methodology and Topic marks *and* keeps the plagiarism scores low.
