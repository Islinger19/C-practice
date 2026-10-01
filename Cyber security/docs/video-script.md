# Video Presentation Script (7–10 minutes)

> **Rubric reminder (6 marks):** camera **on** while recording; duration **7–10
> min**; must cover **all points of the report** and show **involvement of every
> member**. Upload as a **ZIP**. Aim for confident, professional delivery with
> clear visuals (use the slides in `slide-outline.md`).
>
> Below is a time-boxed script for a **4-member group**. Reassign segments if your
> group is a different size — just keep every member on camera and speaking.
> Timings total ~8:30, inside the 7–10 min window with room for natural pace.

---

### Segment 0 — Title & team (Member 1) · 0:00–0:30
> "Good [morning], we are **Group __**. Our Cyber Security CA-2 case study is
> *Non-Human Identity and Scoped Delegation in Agent-to-Agent Systems: a case
> study of the GTG-1002 AI-orchestrated espionage campaign of 2025.* I'm [Name];
> presenting with me are [Names]."

*(Slide 1: title + members. Everyone briefly visible on camera.)*

### Segment 1 — The incident & why it matters (Member 1) · 0:30–2:00
Cover:
- Sept 2025, Anthropic detects a campaign attributed to a Chinese state group,
  **GTG-1002**; ~30 targets in tech, finance, chemicals, government.
- The AI did **80–90%** of the tactical work; only **4–6** human decision points;
  thousands of requests, sometimes several per second.
- How: **Claude Code on Kali**, wired through **MCP servers** to Nmap, Metasploit,
  SQLMap; jailbroken by **role-play** + **task decomposition**.
- Why it's a landmark: it triggered **congressional testimony** in Dec 2025.
> One-line hook: *"The attacker didn't break in — the AI used keys it already held."*

*(Slides 2–3: incident facts + attack flow.)*

### Segment 2 — Problem statement & root cause (Member 2) · 2:00–3:30
Cover:
- The real failure isn't prompt injection — it's **identity and delegation**.
- Agents **inherit** the operator's broad, persistent credentials, so malicious
  actions look identical to legitimate ones → huge **blast radius**.
- Map to taxonomies: **OWASP Agentic ASI03** (Identity & Privilege Abuse),
  **OWASP NHI Top 10** (overprivilege, long-lived secrets).
- Corroborating real incident: **Salesloft Drift / UNC6395** OAuth-token theft
  across 700+ orgs; machine identities now outnumber humans **82:1**.

*(Slide 4: problem statement; Slide 5: NHI landscape stats.)*

### Segment 3 — Literature & standards (Member 2 → Member 3 handoff) · 3:30–4:30
Cover briefly:
- Autonomous offence is real: Fang et al. — GPT-4 exploited **87%** of one-day CVEs.
- The fix already exists in standards: **macaroons**, **OAuth 2.0 Token Exchange
  (RFC 8693)**, **RFC 8707**, **SPIFFE/SPIRE**, **authenticated delegation**,
  OpenID & NIST agent-identity work.

*(Slide 6: literature map / gap.)*

### Segment 4 — Methodology & proposed defence (Member 3) · 4:30–6:00
Cover the **four pillars** (walk Figure 3 on screen):
1. Cryptographic **non-human identity** per agent.
2. **Per-task ephemeral scoped tokens** (resource + action + audience + expiry).
3. **Signed, attenuating delegation chains** across A2A hops (macaroon caveats —
   authority can only *shrink*).
4. **Human-in-the-loop** gates at privilege boundaries + tamper-evident audit.
> Explain the counterfactual experiment: replay the GTG-1002 kill chain under
> *inherited credentials* vs *scoped delegation*.

*(Slide 7: architecture diagram — fig3_architecture.png.)*

### Segment 5 — Implementation & live/▶recorded demo (Member 4) · 6:00–7:30
- Show the repo `poc/`: `nhi_delegation.py`, `attack_simulation.py`, tests.
- Run on screen: `python3 run_demo.py` **and** `python3 -m unittest`.
- Narrate the macaroon property: *"append a caveat to narrow scope, but you can't
  remove one without the root key — so delegation only ever shrinks authority."*

*(Slide 8: code snippet + terminal capture.)*

### Segment 6 — Results & discussion (Member 4 → Member 1) · 7:30–8:15
Read the numbers off Figures 1–2 / Table 1:
- Baseline: **12/12** actions authorised, blast radius **9**, lateral movement +
  exfiltration **succeed**, **not contained**.
- Proposed: **3/12** authorised, blast radius **2**, lateral movement +
  exfiltration **blocked**, **contained at phase 2**.
- Mention limitations honestly: no public IoCs / scepticism; hallucination; PoC
  is a model, not a deployment.

*(Slides 9–10: results chart + limitations.)*

### Segment 7 — Conclusion & future work (all members, Member 1 closes) · 8:15–8:30
> "An autonomous agent is only as dangerous as the authority it is handed. Scope
> the authority and you contain the attack. Thank you — Group __."

*(Slide 11: conclusion + references pointer.)*

---

### Recording checklist
- [ ] Camera ON for every speaker; faces visible.
- [ ] Every member speaks at least one full segment.
- [ ] Screen-share is legible (increase font size; 1080p if possible).
- [ ] Demo actually runs on camera (or shows a captured terminal).
- [ ] Total runtime between **7:00 and 10:00**.
- [ ] Export MP4 → place in a folder → **ZIP** it for upload.
