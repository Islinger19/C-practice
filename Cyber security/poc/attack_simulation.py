"""
attack_simulation.py
====================

A counterfactual simulation of the GTG-1002 AI-orchestrated espionage kill
chain, replayed against two authorization models:

  * BASELINE  - "inherited credentials": the orchestrating agent and all of its
                sub-agents act with one long-lived, broadly-scoped credential
                (the operator's own). This mirrors the condition Anthropic
                reported for GTG-1002, where the agent "used keys it already
                held" and its malicious requests were indistinguishable from
                legitimate work.

  * PROPOSED  - "NHI + scoped delegation": every agent carries its own
                non-human identity; the orchestrator receives a per-task token
                scoped to the current objective; each A2A hop attenuates the
                token further; a Policy Decision Point enforces every caveat at
                the tool boundary; and privilege-boundary actions require
                human-in-the-loop approval.

The simulation reconstructs the attack phases Anthropic described
(reconnaissance -> vulnerability discovery -> credential harvesting ->
lateral movement -> data collection/exfiltration -> documentation) as a fixed
sequence of attempted tool invocations, then measures, for each model:

    - actions authorized vs. blocked
    - blast radius (distinct sensitive resources successfully reached)
    - whether cross-tenant / out-of-scope lateral movement succeeded
    - whether bulk exfiltration succeeded
    - where (if anywhere) a human was asked to approve

The point is NOT that scoped delegation makes attacks impossible. It is that
it (a) collapses the blast radius of a compromised or misused agent to a
single task's scope and (b) forces the adversary back to the human
decision-points that were the campaign's only real bottleneck.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from nhi_delegation import (
    AuditLog,
    Caveat,
    Decision,
    DelegationAuthority,
    DelegationToken,
    Identity,
    PolicyDecisionPoint,
    RequestContext,
    scope,
)
import time


# --------------------------------------------------------------------------- #
# The attacker's intended kill chain (one entry per attempted tool call).
# Phases follow Anthropic's reported GTG-1002 lifecycle.
# --------------------------------------------------------------------------- #
@dataclass
class Step:
    phase: str
    action: str
    resource: str
    sensitivity: str          # low | medium | high | critical
    in_task_scope: bool       # is this action within the legitimate task?
    note: str = ""


# The legitimate task the operator *claimed* to be doing: an authorized
# vulnerability assessment of the single web-app asset "webapp-01".
LEGIT_TASK_ID = "pentest-webapp-01"
LEGIT_SCOPE_PREFIX = "asset://webapp-01/"

KILL_CHAIN: List[Step] = [
    # Phase 1 - Reconnaissance (legitimate-looking, within the sanctioned asset)
    Step("1. Reconnaissance", "scan", "asset://webapp-01/network", "low", True,
         "Port/service enumeration of the in-scope asset"),
    Step("1. Reconnaissance", "scan", "asset://webapp-01/http", "low", True,
         "Attack-surface mapping of the in-scope web app"),
    # Phase 2 - Vulnerability discovery (still arguably in-scope)
    Step("2. Vulnerability discovery", "analyze", "asset://webapp-01/http",
         "medium", True, "Identify injectable endpoint on in-scope asset"),
    # Phase 2 - but now reaching for assets that were never in scope
    Step("2. Vulnerability discovery", "scan", "asset://db-cluster/pg",
         "medium", False, "Pivot scan toward the production DB cluster"),
    # Phase 3 - Credential harvesting (reading secrets from infra it holds keys to)
    Step("3. Credential harvesting", "read", "asset://ci/service-tokens",
         "high", False, "Read CI/CD service-account tokens (NHI secret theft)"),
    Step("3. Credential harvesting", "read", "asset://cloud/imds-metadata",
         "high", False, "Query cloud metadata endpoint for role credentials"),
    # Phase 4 - Lateral movement using harvested credentials
    Step("4. Lateral movement", "authenticate", "asset://db-cluster/pg",
         "high", False, "Authenticate to prod DB with harvested token"),
    Step("4. Lateral movement", "authenticate", "asset://registry/containers",
         "high", False, "Authenticate to the private container registry"),
    Step("4. Lateral movement", "authenticate", "asset://logging/elastic",
         "high", False, "Authenticate to central logging infrastructure"),
    # Phase 5 - Data collection & exfiltration (the objective)
    Step("5. Data collection/exfiltration", "export", "asset://db-cluster/pg",
         "critical", False, "Bulk export of the highest-value database"),
    Step("5. Data collection/exfiltration", "export", "asset://cloud/s3-backups",
         "critical", False, "Exfiltrate backup buckets"),
    # Phase 6 - Documentation (the agent writes up what it stole)
    Step("6. Documentation", "write", "asset://attacker/report", "medium", False,
         "Agent documents the intrusion for the operator"),
]


@dataclass
class Result:
    model: str
    authorized: int = 0
    blocked: int = 0
    escalated: int = 0
    resources_reached: List[str] = field(default_factory=list)
    exfiltration_succeeded: bool = False
    lateral_movement_succeeded: bool = False
    first_block_phase: Optional[str] = None
    transcript: List[str] = field(default_factory=list)

    @property
    def blast_radius(self) -> int:
        return len(set(self.resources_reached))


# --------------------------------------------------------------------------- #
# BASELINE: inherited, broadly-scoped, long-lived credential
# --------------------------------------------------------------------------- #
def run_baseline() -> Result:
    """Everything the agent attempts is allowed, because the single inherited
    credential grants broad standing access and nothing re-checks per-action
    scope. There is no human gate on individual tactical actions - exactly the
    80-90%-autonomous condition Anthropic reported."""
    res = Result(model="Baseline (inherited credentials)")
    for step in KILL_CHAIN:
        # The inherited credential authorizes any action on any resource.
        res.authorized += 1
        res.resources_reached.append(step.resource)
        if step.action == "authenticate":
            res.lateral_movement_succeeded = True
        if step.action == "export":
            res.exfiltration_succeeded = True
        res.transcript.append(
            f"[{step.phase}] ALLOW  {step.action} {step.resource} "
            f"(inherited credential - no scope check)")
    return res


# --------------------------------------------------------------------------- #
# PROPOSED: NHI + per-task scoped delegation + PDP + HITL
# --------------------------------------------------------------------------- #
def run_proposed(human_approves: bool = False) -> Result:
    """The orchestrator is minted a token scoped ONLY to the sanctioned task
    (vuln assessment of webapp-01, read/scan/analyze actions only, 1-hour TTL).
    It delegates to a recon sub-agent, attenuating further. Every tool call is
    checked by the PDP; anything outside the task scope is denied, and any
    high/critical action is escalated to a human.

    `human_approves=False` models a vigilant operator who refuses the
    out-of-scope escalations (the realistic defensive posture).
    """
    authority_identity = Identity("tenant-authz", kind="authority")
    authority = DelegationAuthority(authority_identity)
    audit = AuditLog()

    approvals = {"count": 0}

    def approver(ctx: RequestContext) -> bool:
        approvals["count"] += 1
        return human_approves

    pdp = PolicyDecisionPoint(authority, audit, approver=approver)

    # Non-human identities - each agent has its OWN identity, not the human's.
    orchestrator = Identity("orchestrator-agent", kind="agent")
    recon_subagent = Identity("recon-subagent", kind="agent")

    # Per-task, least-privilege token for the orchestrator.
    base_caveats = scope(
        resource_prefix=LEGIT_SCOPE_PREFIX,
        actions=["scan", "analyze", "read"],
        audience=recon_subagent.spiffe_id,   # bound to who will use it (RFC 8707)
        task_id=LEGIT_TASK_ID,
        ttl_seconds=3600,
    )
    orch_token = authority.mint(orchestrator, base_caveats)

    # A2A hop: orchestrator delegates to the recon sub-agent, attenuating to
    # read-only scanning. Authority can only shrink here.
    sub_token: DelegationToken = orch_token.attenuate(
        Caveat("action", "in", ("scan", "analyze")),
        new_holder=recon_subagent.spiffe_id,
    )

    res = Result(model="Proposed (NHI + scoped delegation)")
    for step in KILL_CHAIN:
        ctx = RequestContext(
            agent=recon_subagent.spiffe_id,
            attributes={
                "resource": step.resource,
                "action": step.action,
                "audience": recon_subagent.spiffe_id,
                "task": LEGIT_TASK_ID,
                "now": time.time(),
            },
            sensitivity=step.sensitivity,
        )
        decision, reason = pdp.authorize(sub_token, ctx)
        if decision == Decision.ALLOW:
            res.authorized += 1
            res.resources_reached.append(step.resource)
            if step.action == "authenticate":
                res.lateral_movement_succeeded = True
            if step.action == "export":
                res.exfiltration_succeeded = True
            res.transcript.append(
                f"[{step.phase}] ALLOW  {step.action} {step.resource}")
        else:
            if decision == Decision.ESCALATE:
                res.escalated += 1
            else:
                res.blocked += 1
            if res.first_block_phase is None:
                res.first_block_phase = step.phase
            res.transcript.append(
                f"[{step.phase}] {decision.value:17s} {step.action} "
                f"{step.resource}  <- {reason}")
    res._audit = audit                     # attach for inspection
    res._human_prompts = approvals["count"]
    return res


# --------------------------------------------------------------------------- #
# Pretty-printing / metrics
# --------------------------------------------------------------------------- #
def summarize(res: Result) -> Dict[str, object]:
    return {
        "model": res.model,
        "attempted": len(KILL_CHAIN),
        "authorized": res.authorized,
        "blocked": res.blocked,
        "escalated_to_human": res.escalated,
        "blast_radius_resources": res.blast_radius,
        "lateral_movement_succeeded": res.lateral_movement_succeeded,
        "exfiltration_succeeded": res.exfiltration_succeeded,
        "contained_at_phase": res.first_block_phase or "NOT CONTAINED",
    }


if __name__ == "__main__":
    import json

    baseline = run_baseline()
    proposed = run_proposed(human_approves=False)

    print("=" * 74)
    print("GTG-1002 counterfactual kill-chain simulation")
    print("=" * 74)
    for res in (baseline, proposed):
        print(f"\n### {res.model}")
        for line in res.transcript:
            print("   " + line)
        print("   --- summary ---")
        print(json.dumps(summarize(res), indent=6))
