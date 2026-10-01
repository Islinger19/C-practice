"""
nhi_delegation.py
=================

A dependency-free (standard-library only) reference implementation of the
defence proposed in the case study:

    Non-Human Identity (NHI) + Scoped, Attenuable, Auditable Delegation
    for Agent-to-Agent (A2A) systems.

The module is deliberately small and readable so that it can be used as a
teaching / demonstration artifact for the Cyber Security CA-2 case study on the
GTG-1002 AI-orchestrated espionage campaign (Anthropic, November 2025).

It demonstrates, in code, the four pillars of the proposed solution framework:

  1. Cryptographic agent identity  -> every agent has its own keyed identity,
     not the developer's inherited credential.
  2. Per-task ephemeral scoped tokens -> short-lived capability tokens minted
     per task instead of long-lived inherited secrets (OWASP NHI7:2025).
  3. Signed, attenuating delegation chains across A2A hops -> each hop can only
     *narrow* authority, never widen it (the "macaroon" caveat model of
     Birgisson et al., NDSS 2014; the "act" delegation-chain idea of
     RFC 8693 OAuth 2.0 Token Exchange).
  4. Human-in-the-loop (HITL) gates at privilege boundaries -> high-impact
     actions require an explicit out-of-band approval, mapping to the 4-6
     human decision points Anthropic reported in GTG-1002.

The cryptography here uses HMAC-SHA256 chaining (the macaroon construction).
It is NOT production cryptography (a real deployment would use Ed25519/JWS as
in A2A v1.0, SPIFFE X.509-SVIDs, or RFC 8693 token exchange) but it faithfully
reproduces the security property that matters for the demonstration: a token
holder can append restricting caveats but cannot remove or weaken existing
ones without knowing the issuer's root key.

Author: Cyber Security CA-2 Case Study Group
"""

from __future__ import annotations

import hashlib
import hmac
import secrets
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Dict, List, Optional, Tuple


# --------------------------------------------------------------------------- #
# 1. Cryptographic agent identity
# --------------------------------------------------------------------------- #
class Identity:
    """A non-human identity (NHI) for a single agent or workload.

    Each agent gets its OWN identity with its OWN secret, instead of inheriting
    the human developer's persistent credential. This is the central lesson of
    GTG-1002: the AI agents did not "hack in", they acted with keys they already
    held, so their malicious queries were indistinguishable from legitimate work
    (OWASP Agentic ASI03 - Identity & Privilege Abuse; OWASP NHI10:2025 -
    Human Use of NHI).
    """

    def __init__(self, name: str, kind: str = "agent"):
        self.name = name
        self.kind = kind                      # human | agent | tool | authority
        self.secret = secrets.token_bytes(32)  # the identity's private key
        # A stable, verifiable identifier (think SPIFFE ID / A2A Agent Card id).
        self.spiffe_id = f"spiffe://acme.internal/{kind}/{name}"

    def __repr__(self) -> str:
        return f"<Identity {self.spiffe_id}>"


# --------------------------------------------------------------------------- #
# 2 & 3. Capability tokens with attenuating caveats (the macaroon model)
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class Caveat:
    """A first-party caveat: a predicate that MUST hold for the token to be
    accepted. Caveats only ever *restrict* authority."""
    key: str          # e.g. "resource", "action", "audience", "expires", "task"
    op: str           # "==", "in", "<=", "prefix"
    value: object

    def holds(self, ctx: "RequestContext") -> bool:
        actual = ctx.attributes.get(self.key)
        if actual is None:
            return False
        if self.op == "==":
            return actual == self.value
        if self.op == "in":
            return actual in self.value
        if self.op == "<=":
            return float(actual) <= float(self.value)
        if self.op == "prefix":
            return isinstance(actual, str) and actual.startswith(self.value)
        return False

    def __str__(self) -> str:
        return f"{self.key} {self.op} {self.value}"


@dataclass
class DelegationToken:
    """A capability token ("macaroon") carrying an append-only chain of caveats
    and an HMAC signature chained over them.

    Security property (verified by `verify`): a holder may call `attenuate` to
    append a new caveat (narrowing authority), which re-chains the HMAC using
    the *current signature* as the key. Because the holder does not know the
    issuer root key, it cannot recompute a signature for a token with a caveat
    removed. Thus authority can only shrink as the token travels across A2A
    hops. This is what prevents the "multi-hop identity loss / privilege
    widening" that A2ABreak (ACSAC'26) found in naive delegation chains.
    """
    token_id: str
    issuer: str                       # spiffe id of the minting authority
    subject: str                      # spiffe id the token was minted FOR
    caveats: List[Caveat]
    signature: str                    # hex HMAC chained over the caveats
    delegation_path: List[str]        # ordered spiffe ids the token passed through

    @staticmethod
    def _sign(key: bytes, msg: str) -> str:
        return hmac.new(key, msg.encode(), hashlib.sha256).hexdigest()

    def attenuate(self, caveat: Caveat, new_holder: str) -> "DelegationToken":
        """Append a restricting caveat and record the A2A hop. Called by a
        delegating agent before handing the token to a sub-agent."""
        new_sig = self._sign(bytes.fromhex(self.signature), str(caveat))
        return DelegationToken(
            token_id=self.token_id,
            issuer=self.issuer,
            subject=self.subject,
            caveats=self.caveats + [caveat],
            signature=new_sig,
            delegation_path=self.delegation_path + [new_holder],
        )


class DelegationAuthority:
    """Issues and verifies capability tokens. Think of this as the per-tenant
    authorization server (OAuth 2.1 AS / SPIRE server / A2A identity provider)."""

    def __init__(self, identity: Identity):
        self.identity = identity
        self._issued: Dict[str, float] = {}   # token_id -> issued_at (for audit)

    def mint(self, subject: Identity, caveats: List[Caveat]) -> DelegationToken:
        """Mint a fresh, per-task, scoped token for `subject`.

        The root signature is HMAC(root_key, token_id) then chained through
        every caveat, so the issuer can later re-derive and verify it."""
        token_id = secrets.token_hex(8)
        sig = DelegationToken._sign(self.identity.secret, token_id)
        for cav in caveats:
            sig = DelegationToken._sign(bytes.fromhex(sig), str(cav))
        self._issued[token_id] = time.time()
        return DelegationToken(
            token_id=token_id,
            issuer=self.identity.spiffe_id,
            subject=subject.spiffe_id,
            caveats=list(caveats),
            signature=sig,
            delegation_path=[subject.spiffe_id],
        )

    def verify(self, token: DelegationToken) -> bool:
        """Recompute the chained HMAC from the root key and confirm it matches.
        A tampered or caveat-stripped token fails here."""
        sig = DelegationToken._sign(self.identity.secret, token.token_id)
        for cav in token.caveats:
            sig = DelegationToken._sign(bytes.fromhex(sig), str(cav))
        return hmac.compare_digest(sig, token.signature)


# --------------------------------------------------------------------------- #
# Request context + policy decision point
# --------------------------------------------------------------------------- #
class Decision(Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"
    ESCALATE = "ESCALATE_TO_HUMAN"


@dataclass
class RequestContext:
    """Everything the Policy Decision Point needs to evaluate one tool call."""
    agent: str                         # spiffe id of the calling agent
    attributes: Dict[str, object]      # resource, action, audience, task, ...
    sensitivity: str = "low"           # low | medium | high | critical
    timestamp: float = field(default_factory=time.time)


# --------------------------------------------------------------------------- #
# Audit log
# --------------------------------------------------------------------------- #
@dataclass
class AuditEvent:
    ts: float
    agent: str
    action: str
    resource: str
    decision: str
    reason: str


class AuditLog:
    def __init__(self):
        self.events: List[AuditEvent] = []

    def record(self, ctx: RequestContext, decision: Decision, reason: str):
        self.events.append(AuditEvent(
            ts=ctx.timestamp,
            agent=ctx.agent,
            action=str(ctx.attributes.get("action", "?")),
            resource=str(ctx.attributes.get("resource", "?")),
            decision=decision.value,
            reason=reason,
        ))

    def denials(self) -> List[AuditEvent]:
        return [e for e in self.events if e.decision != Decision.ALLOW.value]

    def distinct_resources_touched(self) -> int:
        return len({e.resource for e in self.events
                    if e.decision == Decision.ALLOW.value})


# --------------------------------------------------------------------------- #
# 4. Policy Decision Point with HITL gate
# --------------------------------------------------------------------------- #
# A human approval callback returns True to approve an escalated action.
HumanApprover = Callable[[RequestContext], bool]


class PolicyDecisionPoint:
    """Zero-trust guard sitting in front of every tool (every MCP server).

    It (a) verifies the capability token cryptographically, (b) checks that
    EVERY caveat holds for this specific request, and (c) routes high /
    critical sensitivity actions through a human-in-the-loop gate. This is the
    enforcement point the GTG-1002 defenders lacked: in the real campaign the
    agent's requests carried the operator's inherited, unscoped credential, so
    nothing re-checked whether *this* action, on *this* resource, was in scope.
    """

    HITL_LEVELS = {"high", "critical"}

    def __init__(self, authority: DelegationAuthority,
                 audit: AuditLog,
                 approver: Optional[HumanApprover] = None):
        self.authority = authority
        self.audit = audit
        self.approver = approver

    def authorize(self, token: DelegationToken,
                  ctx: RequestContext) -> Tuple[Decision, str]:
        # (a) cryptographic verification of the delegation chain
        if not self.authority.verify(token):
            d, r = Decision.DENY, "token signature invalid (tampered chain)"
            self.audit.record(ctx, d, r)
            return d, r

        # the caller must be the final holder of the token
        if ctx.agent != token.delegation_path[-1]:
            d, r = Decision.DENY, "caller is not the current token holder"
            self.audit.record(ctx, d, r)
            return d, r

        # (b) every caveat must hold for THIS request
        for cav in token.caveats:
            if not cav.holds(ctx):
                d, r = Decision.DENY, f"caveat not satisfied: [{cav}]"
                self.audit.record(ctx, d, r)
                return d, r

        # (c) human-in-the-loop gate at the privilege boundary
        if ctx.sensitivity in self.HITL_LEVELS:
            if self.approver is None or not self.approver(ctx):
                d, r = Decision.ESCALATE, "human approval required and not granted"
                self.audit.record(ctx, d, r)
                return d, r
            self.audit.record(ctx, Decision.ALLOW,
                              "allowed after human approval")
            return Decision.ALLOW, "allowed after human approval"

        self.audit.record(ctx, Decision.ALLOW, "within scope")
        return Decision.ALLOW, "within scope"


# --------------------------------------------------------------------------- #
# Convenience builders for common scoped caveats
# --------------------------------------------------------------------------- #
def scope(resource_prefix: str, actions: List[str], audience: str,
          task_id: str, ttl_seconds: int) -> List[Caveat]:
    """Build the caveat set for a least-privilege, per-task token."""
    return [
        Caveat("resource", "prefix", resource_prefix),
        Caveat("action", "in", tuple(actions)),
        Caveat("audience", "==", audience),
        Caveat("task", "==", task_id),
        # "now" is supplied by the request context at call time; the token is
        # only valid while the current clock is at or before the expiry.
        Caveat("now", "<=", time.time() + ttl_seconds),
    ]
