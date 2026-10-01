# Proof-of-Concept: NHI + Scoped Delegation vs. the GTG-1002 Kill Chain

A dependency-free (Python 3.8+ standard library only) reference implementation of
the defence proposed in the case study, with a counterfactual simulation of the
GTG-1002 AI-orchestrated espionage kill chain.

## Files

| File | Purpose |
|---|---|
| `nhi_delegation.py` | The framework: cryptographic agent identity, macaroon-style attenuable capability tokens, a Policy Decision Point with a human-in-the-loop gate, and an audit log. |
| `attack_simulation.py` | Encodes the 12-step GTG-1002 kill chain and replays it under the **baseline** (inherited credentials) and **proposed** (NHI + scoped delegation) models. |
| `test_nhi_delegation.py` | 16 unit tests (crypto, policy, simulation invariants). |
| `run_demo.py` | End-to-end driver: prints transcripts + metric table, writes `../figures/metrics.json`, renders Figures 1 & 2. |
| `make_architecture_fig.py` | Renders Figure 3 (the architecture diagram). |

## Run it

```bash
cd "Cyber security/poc"

# 1) Run the tests (no third-party deps needed)
python3 -m unittest -v test_nhi_delegation.py

# 2) Run the simulation + metrics (figures need matplotlib + numpy)
python3 run_demo.py                 # full run + figures
python3 run_demo.py --no-plot       # metrics only, zero dependencies

# 3) (Re)generate the architecture figure
python3 make_architecture_fig.py
```

`run_demo.py` and `make_architecture_fig.py` need `matplotlib` and `numpy` for the
PNGs only; everything else is standard library. Install if needed:

```bash
pip install matplotlib numpy
```

## What it shows

Replaying the identical GTG-1002 kill chain under both models:

| Metric | Baseline (inherited creds) | Proposed (NHI + scoped delegation) |
|---|---:|---:|
| Actions authorised | 12 / 12 | 3 / 12 |
| Actions blocked | 0 | 9 |
| Blast radius (distinct resources) | 9 | 2 |
| Lateral movement succeeded | yes | no |
| Bulk exfiltration succeeded | yes | no |
| Contained at phase | not contained | phase 2 (vuln. discovery) |

**Key security property (tested):** a delegation token's caveats are HMAC-chained,
so a holder can *append* a restriction (narrow scope) but cannot *remove* one
without the issuer's root key — delegation across A2A hops can only ever shrink
authority. See `test_caveat_removal_is_detected` and
`test_signature_forgery_without_root_key_fails`.

## Important

This is a **teaching / demonstration artifact**, not production security software.
It uses HMAC-SHA256 macaroons rather than production Ed25519/JWS signatures or
SPIFFE X.509-SVIDs, and a fixed deterministic kill chain rather than an adaptive
adversary. It models **synthetic assets only** and contains **no real offensive
code**. See the report's §5.4 (Limitations) for the full list of caveats.
