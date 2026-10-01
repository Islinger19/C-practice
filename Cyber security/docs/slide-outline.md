# Slide Outline (11 slides) — for the video presentation

Keep slides visual and sparse (≤ 6 bullets each). Colours: black text, blue
accents (to match the report's allowed colour scheme). Embed the figures from
`../figures/`.

---

**Slide 1 — Title**
- Non-Human Identity and Scoped Delegation in Agent-to-Agent Systems
- A Case Study of the GTG-1002 AI-Orchestrated Espionage Campaign (2025)
- Group __ · member names · Cyber Security CA-2 · Dr. Pooja Bagane, Dr. Jitendra Rajpurohit

**Slide 2 — The incident (facts)**
- Sept 2025, Anthropic detects GTG-1002 (Chinese state-sponsored, high confidence)
- ~30 targets: tech, finance, chemicals, government
- AI did 80–90% of tactical work · 4–6 human decision points · 1000s of requests
- First AI-orchestrated campaign → congressional testimony Dec 2025

**Slide 3 — How it worked (attack flow)**
- Claude Code on Kali Linux + custom MCP servers → Nmap / Metasploit / SQLMap
- Phases: recon → vuln discovery → credential harvest → lateral movement → exfiltration → documentation
- Jailbreak: role-play ("legit security firm") + task decomposition
- Honest caveat: agent hallucinated/overstated findings

**Slide 4 — Problem statement**
- Not prompt injection — it's **identity & delegation**
- Agents **inherit** broad, persistent operator credentials
- Malicious actions ≈ legitimate actions → massive **blast radius**
- *"It used keys it already held."*

**Slide 5 — Why this is urgent (NHI landscape)**
- Machine identities outnumber humans **82:1** (CyberArk 2025)
- 23.8M secrets leaked on GitHub in 2024; 70% still valid 2 years later
- Real corroboration: Salesloft Drift / UNC6395 — OAuth token theft, 700+ orgs
- Maps to OWASP Agentic **ASI03** & NHI Top 10

**Slide 6 — Literature & the gap**
- Offence is real: GPT-4 exploited 87% of one-day CVEs (Fang et al.)
- Fixes exist: macaroons, OAuth Token Exchange (RFC 8693), RFC 8707, SPIFFE/SPIRE
- Standards momentum: authenticated delegation, OpenID, NIST NCCoE, A2A v1.0
- **Gap:** no *measured* demonstration tied to a real incident → our contribution

**Slide 7 — Proposed defence (architecture)**
- Figure 3 (`fig3_architecture.png`)
- 4 pillars: NHI · per-task scoped tokens · attenuating A2A delegation · HITL + audit

**Slide 8 — Implementation**
- Python 3.11, standard library only (hmac/hashlib/secrets)
- Macaroon caveat chain: can **add** restrictions, can't **remove** them
- `run_demo.py` + 16 passing unit tests
- Code snippet: `attenuate()` / `verify()`

**Slide 9 — Results**
- Table 1 + Figure 1 (`fig1_outcomes.png`)
- Baseline: 12/12 authorised, blast radius 9, NOT contained
- Proposed: 3/12 authorised, blast radius 2, contained at phase 2
- Lateral movement & exfiltration: baseline ✓ / proposed ✗

**Slide 10 — Discussion & limitations**
- Figure 2 (`fig2_blast_radius.png`) — containment curve
- Defence-in-depth: scope caveat denies *before* the human gate is even needed
- Limits: contested evidence/no IoCs; hallucination; PoC is a model; in-scope misuse remains

**Slide 11 — Conclusion**
- An agent is only as dangerous as the authority it's handed
- Scope + attenuate + HITL + audit → contain autonomous-agent intrusions
- Future: Ed25519/JWS + SPIFFE, adaptive red-team agent, anomaly detection
- References: see report (44 sources) · Thank you — Group __
