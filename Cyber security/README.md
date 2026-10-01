# Cyber Security CA-2 — Case Study Report

**Topic:** Non-Human Identity and Scoped Delegation in Agent-to-Agent Systems —
A Case Study of the GTG-1002 AI-Orchestrated Espionage Campaign (2025)

**Course:** Cyber Security (B.Tech, Sem VII, CSE) · Continuous Assessment 2, Part 2
**Faculty:** Dr. Pooja Bagane, Dr. Jitendra Rajpurohit
**Deadline:** Saturday, 10 October 2026, 4:30 pm (submit via the Google Form in the notice)

---

## What this is

A complete, submission-ready case-study package for CA-2 Part 2: a researched
report, a runnable proof-of-concept that *measures* the proposed defence, and all
the supporting material the rubric asks for (topic justification, video script,
slides, plagiarism plan, 44 references).

**One-line thesis:** GTG-1002 wasn't primarily a model-jailbreak story — it was an
**identity-and-delegation failure**. The AI agent acted with the operator's
inherited, persistent credentials, so its malicious actions were indistinguishable
from legitimate work. Give each agent its own non-human identity and delegate
authority *narrowly, ephemerally and verifiably*, and the blast radius collapses.

## Folder map

| Path | What's inside |
|---|---|
| `report/Case_Study_Report.md` | The report (source of truth) — all required sections. |
| `report/Case_Study_Report.docx` | Formatted Word: Times New Roman 12, black & blue, single column, title page. |
| `report/Case_Study_Report.pdf` | Rendered PDF — **rename to `G<NN>.pdf` before upload**. |
| `poc/` | Python proof-of-concept + 16 passing tests (`poc/README.md` to run it). |
| `figures/` | `fig1_outcomes.png`, `fig2_blast_radius.png`, `fig3_architecture.png`, `metrics.json`. |
| `docs/topic-selection.md` | Top-5 trending topics + why we chose this one. |
| `docs/video-script.md` | 7–10 min script, every member speaking. |
| `docs/slide-outline.md` | 11-slide deck outline. |
| `docs/rubric-mapping.md` | Maps every deliverable to the 20-mark rubric + submission checklist. |
| `docs/plagiarism-guidance.md` | How to hit < 10% similarity and ≤ 20% AI-plag (worth 6 marks). |
| `docs/references.md` | 44 IEEE-style references (notice requires ≥ 30). |

## Before you submit — do these

1. **Fill in the title page**: group number, **all** member names + roll numbers,
   on page 1 of the report (and in the `.docx`).
2. **Rewrite the report in your own words.** The draft is a researched scaffold;
   submitting it verbatim risks the AI-plag marks. See `docs/plagiarism-guidance.md`.
3. **Run the plagiarism + AI checks** on the college tool; attach both reports.
4. **Export to PDF and rename to `G<NN>.pdf`** (e.g., `G10.pdf`). Any other name
   is rejected.
5. **Record the video** (camera on, 7–10 min, every member) and **ZIP** it.
6. **One member uploads** everything via the Google Form. No resubmission after
   10 Oct.

## Run the proof-of-concept (for the demo & Methodology marks)

```bash
cd "Cyber security/poc"
python3 -m unittest -v test_nhi_delegation.py   # 16 tests, standard library only
python3 run_demo.py                              # transcripts, metrics, figures
```

See `poc/README.md` for details and the results table.

## Scope & integrity note

This package analyses a real, publicly reported incident and proposes a defensive
architecture. The proof-of-concept uses **synthetic assets only** and contains
**no real offensive code**; it is a teaching artifact (see report §5.4 for its
limitations). Use the written report as research structure and verified evidence
to learn from and rewrite in your own words.
