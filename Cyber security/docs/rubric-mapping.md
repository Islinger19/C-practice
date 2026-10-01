# Rubric Mapping & Submission Checklist (CA-2 Part 2)

This maps every deliverable in this folder to the official CA-2 rubric from the
notice, so nothing scored is left to chance. **Total: 20 marks.**

## Mark distribution (from the notice)

| Sr. | Performance criteria | Marks |
|---|---|---:|
| 1 | Selection of Topic and its Relevance in Today's World | 2 |
| 2 | Plagiarism Report & AI Plag | 6 |
| 3 | Methodology | 6 |
| 4 | Video Presentation (7–8 min) | 6 |
| | **Total** | **20** |

> Note: the QUIZ (Part 1, Unit 2, 10 marks) on Sat 10 Oct is separate from this
> case-study report (Part 2, Unit 4, 20 marks). This folder covers Part 2 only.

---

## 1 · Selection of Topic & Relevance — target **2/2**

Top band = *"highly relevant, innovative, and aligned with current trends."*

- ✅ Anchored to a named, recent incident (GTG-1002, Sept–Nov 2025) that reached
  **US congressional testimony**.
- ✅ In the hottest current trend space — **agentic AI / agent-to-agent (A2A)**.
- ✅ **Distinct** from every other group's topic on the shared list (non-human
  identity + delegation is untouched by the others).
- ✅ Justification documented in `topic-selection.md` with a comparison table.

## 2 · Plagiarism Report & AI Plag — target **6/6**

Rubric: *Similarity < 10% (mandatory)*; AI-plag **0–20% → 3M**, 21–30% → 2M,
31–40% → 1M, >40% → 0M; **Similarity report → 3M**. Resubmission not allowed
after Sat 10 Oct 2026.

- ➡️ See `plagiarism-guidance.md` for a step-by-step plan to hit **<10%
  similarity and <20% (ideally ~0%) AI-plag**.
- ⚠️ **This is the biggest risk area.** The report here is a *draft you must
  rewrite in your own words* — do **not** submit AI-generated text verbatim.
  Treat the draft as structure + evidence, then paraphrase throughout and add
  your own analysis.
- ✅ Report already includes **44 cited references** (notice requires ≥ 30),
  reducing uncited-similarity risk.
- [ ] Run Turnitin (or college tool) → export similarity + AI reports → include
  in submission.

## 3 · Methodology — target **6/6**

Top band = *"Excellent, well-structured, justified, and technically sound
methodology."*

- ✅ Explicit 4-stage research method (evidence → root cause → design →
  experiment) in report §3.
- ✅ Stated **threat model & assumptions** (§3.4).
- ✅ A **working proof-of-concept** (`poc/`) that *measures* the defence —
  counterfactual simulation, 16 passing tests, reproducible figures. This is
  what pushes Methodology from "good" to "excellent."
- ✅ Every design choice mapped to an established **standard** (RFC 8693/8707,
  macaroons, SPIFFE, OWASP) — i.e., justified, not invented.

## 4 · Video Presentation (7–8 / 7–10 min) — target **6/6**

Top band = *"professional delivery, timing, clarity, and visuals."*

- ✅ Time-boxed script in `video-script.md` (every member speaks; camera on).
- ✅ 11-slide visual outline in `slide-outline.md` using the three figures.
- [ ] Record MP4 (camera on), keep 7–10 min, **ZIP** it for upload.

---

## Formatting & submission rules (from the notice) — verify before upload

- [ ] **First page** has: group number, **all** member names, topic selected.
- [ ] Font **Times New Roman**; **contents font size 12**; **single column**.
- [ ] Allowed colours only: **black and blue**.
- [ ] Sections present: **Title, Student's name, Abstract, Keywords, Introduction,
  Literature Review (with citations), Methodology, Implementation Details,
  Results & Discussions, Conclusion, References (≥ 30).** ✅ all present in the
  report.
- [ ] Export the report to **PDF**, named **`G<NN>.pdf`** (e.g., `G10.pdf`).
      *Any other name is rejected.*
- [ ] **Only one** group member uploads, via the Google Form in the notice.
- [ ] Plagiarism report (similarity **< 10%**) **and** AI-plag report attached.
- [ ] Video Presentation uploaded as a **ZIP**.
- [ ] Deadline: **Saturday, 10 October 2026, till 4:30 pm.** No resubmission after.

---

## What's in this folder

```
Cyber security/
├── README.md                       ← start here
├── report/
│   ├── Case_Study_Report.md        ← the report (source of truth)
│   ├── Case_Study_Report.docx      ← formatted Word (TNR 12, black/blue, 1-col)
│   └── Case_Study_Report.pdf       ← rendered PDF (rename to G<NN>.pdf)
├── poc/                            ← Python proof-of-concept + tests
│   ├── nhi_delegation.py
│   ├── attack_simulation.py
│   ├── run_demo.py
│   ├── make_architecture_fig.py
│   ├── test_nhi_delegation.py
│   └── README.md
├── figures/                        ← fig1/fig2/fig3 PNG + metrics.json
└── docs/
    ├── topic-selection.md          ← top-5 + why we chose #1
    ├── video-script.md             ← 7–10 min, per-member
    ├── slide-outline.md            ← 11 slides
    ├── rubric-mapping.md           ← this file
    ├── plagiarism-guidance.md      ← hit <10% similarity / <20% AI-plag
    └── references.md               ← 44 IEEE references
```
