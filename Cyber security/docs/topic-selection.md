# Topic Selection — Top 5 Trending Cyber Security Case-Study Topics (and why we chose #1)

This note documents how the group chose its CA-2 case-study topic. The CA-2
rubric awards **2 marks for "Selection of Topic and its Relevance in Today's
World,"** with the top band reserved for a topic that is *"highly relevant,
innovative, and aligned with current trends."* We therefore deliberately picked
a topic that (a) is anchored to a concrete, recent, named incident, (b) occupies
a trend space (autonomous/agentic AI, agent-to-agent communication) that **no
other group on the shared list is covering**, and (c) has enough technical depth
to support a real methodology and an implementable proof-of-concept.

The topics below are trendy around agentic AI / A2A communication. **We selected
#1.** The other four are kept here to show the comparison we made and are free
for other groups to reuse.

---

## ✅ #1 (CHOSEN) — Non-Human Identity and Scoped Delegation in Agent-to-Agent Systems: A Case Study of the GTG-1002 AI-Orchestrated Espionage Campaign (2025)

**Why it wins.** GTG-1002 is the first publicly reported large-scale cyber
campaign in which an AI agent performed an estimated 80–90% of the intrusion
work — reconnaissance, vulnerability discovery, lateral movement and data
extraction — with humans approving only 4–6 critical steps, orchestrated by
chaining Claude Code to MCP servers driving tools like Nmap, Metasploit and
SQLMap. The root problem is **not** prompt injection: it is that the agent
inherited the full, persistent permissions of its operator, so its queries and
clones were indistinguishable from legitimate work. It did not hack in — it used
keys it already held.

- **Problem statement:** autonomous agents inherit broad, long-lived identities,
  so a subverted agent gets an enormous blast radius with nothing to distinguish
  abuse from use.
- **Solution framework:** cryptographic non-human identity per agent; per-task
  ephemeral scoped tokens instead of inherited credentials; signed, *attenuating*
  delegation chains across A2A hops; and human-in-the-loop gates at privilege
  boundaries.
- **Why defensible & distinct:** nobody else on the group list touches non-human
  identity or A2A delegation; it maps cleanly to real standards (OAuth 2.0 Token
  Exchange, RFC 8707, macaroons, SPIFFE/SPIRE, the OWASP Agentic & NHI Top 10),
  and it supports a working proof-of-concept (included in `../poc/`) that
  *measures* the defence — which lifts the Methodology score (6 marks) as well as
  the Topic score (2 marks).
- **Deliverables status:** full report, 44 references, runnable PoC with 16
  passing tests, three figures, video script and slide outline — all in this
  folder.

---

## #2 — Securing the Model Context Protocol (MCP): Defending AI Agents Against Tool Poisoning and the Confused-Deputy Problem

A tool's *description* is read by the agent as trusted instructions; Invariant
Labs showed in 2025 that a poisoned description can silently exfiltrate a
developer's SSH keys. Pair the attack class with the MCP 2025-06-18/2025-11-25
authorization hardening (OAuth 2.1, RFC 8707 resource indicators, Client ID
Metadata Documents) as the solution. Strong, very current, implementable — our
second choice.

## #3 — A2A Protocol Security: A Specification-Level Analysis of Multi-Hop Delegation and Identity Loss (building on A2ABreak)

A2A reached production v1.0 in 2026 with signed Agent Cards; the ACSAC'26
"A2ABreak" paper found eleven specification-level vulnerabilities, including
credential harvesting via multi-hop identity loss. A case study could reproduce
one finding on a toy A2A deployment and propose signed, audience-bound
delegation as the fix. Deep and novel, but heavier to implement than #1.

## #4 — Runtime AI Malware: Detecting LLM-Backed "Just-in-Time" Threats (PROMPTFLUX / PROMPTSTEAL)

Google's GTIG reported the first malware that calls an LLM API *at runtime* to
rewrite itself (PROMPTFLUX) and generate commands on demand (PROMPTSTEAL, used
by APT28). Solution angle: behavioural/network detection of LLM-API callbacks
and self-modification. Very trendy; detection-focused, so it suits a group that
prefers an ML/analytics methodology.

## #5 — "Vibe Hacking" and Agentic Extortion: Lessons from GTG-2002 and a Least-Privilege Defence for AI Coding Agents

Anthropic's August 2025 report documented a single operator using Claude Code to
breach 17+ organisations with ransom demands over US$500k. Solution angle:
egress controls, scoped credentials and anomaly detection for coding agents.
Closely related to #1 (same identity root cause) — we folded its evidence into
our chosen report rather than making it a separate topic.

---

### Decision summary

| Criterion (CA-2 relevance band) | #1 GTG-1002 / NHI | #2 MCP | #3 A2A | #4 Runtime malware | #5 Vibe hacking |
|---|:---:|:---:|:---:|:---:|:---:|
| Anchored to a named 2025–26 incident | ★★★ | ★★ | ★★ | ★★★ | ★★★ |
| Trend alignment (agentic / A2A) | ★★★ | ★★★ | ★★★ | ★★ | ★★ |
| Distinct from other groups' topics | ★★★ | ★★ | ★★★ | ★★ | ★★ |
| Supports an implementable PoC + methodology | ★★★ | ★★★ | ★★ | ★★ | ★★ |

**Chosen: #1** — strongest on every axis, and the only one that lets us *measure*
the defence in code.
