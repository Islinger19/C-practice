"""
test_nhi_delegation.py
======================

Unit tests for the scoped-delegation reference implementation and the
GTG-1002 counterfactual simulation. Run with:

    python3 -m unittest -v test_nhi_delegation.py

No third-party dependencies are required.
"""

import time
import unittest

from nhi_delegation import (
    AuditLog,
    Caveat,
    Decision,
    DelegationAuthority,
    Identity,
    PolicyDecisionPoint,
    RequestContext,
    scope,
)
import attack_simulation as sim


def _ctx(agent, resource, action, task="pentest-webapp-01",
         audience=None, sensitivity="low", now=None):
    return RequestContext(
        agent=agent,
        attributes={
            "resource": resource,
            "action": action,
            "audience": audience or agent,
            "task": task,
            "now": now if now is not None else time.time(),
        },
        sensitivity=sensitivity,
    )


class IdentityTests(unittest.TestCase):
    def test_each_agent_has_distinct_identity_and_secret(self):
        a = Identity("agent-a")
        b = Identity("agent-b")
        self.assertNotEqual(a.secret, b.secret)
        self.assertNotEqual(a.spiffe_id, b.spiffe_id)
        self.assertTrue(a.spiffe_id.startswith("spiffe://"))


class TokenCryptoTests(unittest.TestCase):
    def setUp(self):
        self.authority = DelegationAuthority(Identity("authz", "authority"))
        self.subject = Identity("agent", "agent")
        self.caveats = scope("asset://webapp-01/", ["scan", "read"],
                             self.subject.spiffe_id, "pentest-webapp-01", 3600)
        self.token = self.authority.mint(self.subject, self.caveats)

    def test_freshly_minted_token_verifies(self):
        self.assertTrue(self.authority.verify(self.token))

    def test_attenuated_token_still_verifies(self):
        narrowed = self.token.attenuate(
            Caveat("action", "in", ("scan",)), self.subject.spiffe_id)
        self.assertTrue(self.authority.verify(narrowed))
        self.assertEqual(len(narrowed.caveats), len(self.token.caveats) + 1)

    def test_caveat_removal_is_detected(self):
        # An attacker tries to strip the resource restriction to widen scope.
        tampered = self.token
        tampered.caveats = [c for c in tampered.caveats
                            if c.key != "resource"]
        self.assertFalse(self.authority.verify(tampered),
                         "stripping a caveat must break the HMAC chain")

    def test_signature_forgery_without_root_key_fails(self):
        other_authority = DelegationAuthority(Identity("evil", "authority"))
        # A different authority cannot validate a token it did not mint.
        self.assertFalse(other_authority.verify(self.token))


class PolicyDecisionPointTests(unittest.TestCase):
    def setUp(self):
        self.authority = DelegationAuthority(Identity("authz", "authority"))
        self.audit = AuditLog()
        self.agent = Identity("recon", "agent")
        self.caveats = scope("asset://webapp-01/", ["scan", "read"],
                             self.agent.spiffe_id, "pentest-webapp-01", 3600)
        self.token = self.authority.mint(self.agent, self.caveats)

    def test_in_scope_low_sensitivity_allowed(self):
        pdp = PolicyDecisionPoint(self.authority, self.audit)
        d, _ = pdp.authorize(self.token, _ctx(
            self.agent.spiffe_id, "asset://webapp-01/http", "scan"))
        self.assertEqual(d, Decision.ALLOW)

    def test_out_of_scope_resource_denied(self):
        pdp = PolicyDecisionPoint(self.authority, self.audit)
        d, reason = pdp.authorize(self.token, _ctx(
            self.agent.spiffe_id, "asset://db-cluster/pg", "scan"))
        self.assertEqual(d, Decision.DENY)
        self.assertIn("resource", reason)

    def test_disallowed_action_denied(self):
        pdp = PolicyDecisionPoint(self.authority, self.audit)
        d, _ = pdp.authorize(self.token, _ctx(
            self.agent.spiffe_id, "asset://webapp-01/http", "export"))
        self.assertEqual(d, Decision.DENY)

    def test_expired_token_denied(self):
        expired = self.authority.mint(self.agent, scope(
            "asset://webapp-01/", ["scan"], self.agent.spiffe_id,
            "pentest-webapp-01", ttl_seconds=-1))
        pdp = PolicyDecisionPoint(self.authority, self.audit)
        d, _ = pdp.authorize(expired, _ctx(
            self.agent.spiffe_id, "asset://webapp-01/http", "scan"))
        self.assertEqual(d, Decision.DENY)

    def test_high_sensitivity_escalates_without_approver(self):
        # read is in-scope action & resource but high sensitivity -> HITL gate
        caveats = scope("asset://webapp-01/", ["read"], self.agent.spiffe_id,
                        "pentest-webapp-01", 3600)
        token = self.authority.mint(self.agent, caveats)
        pdp = PolicyDecisionPoint(self.authority, self.audit, approver=None)
        d, _ = pdp.authorize(token, _ctx(
            self.agent.spiffe_id, "asset://webapp-01/secrets", "read",
            sensitivity="high"))
        self.assertEqual(d, Decision.ESCALATE)

    def test_high_sensitivity_allowed_when_human_approves(self):
        caveats = scope("asset://webapp-01/", ["read"], self.agent.spiffe_id,
                        "pentest-webapp-01", 3600)
        token = self.authority.mint(self.agent, caveats)
        pdp = PolicyDecisionPoint(self.authority, self.audit,
                                  approver=lambda ctx: True)
        d, _ = pdp.authorize(token, _ctx(
            self.agent.spiffe_id, "asset://webapp-01/secrets", "read",
            sensitivity="high"))
        self.assertEqual(d, Decision.ALLOW)

    def test_wrong_holder_denied(self):
        # Caller is not the final holder in the delegation path.
        pdp = PolicyDecisionPoint(self.authority, self.audit)
        d, reason = pdp.authorize(self.token, _ctx(
            "spiffe://acme.internal/agent/someone-else",
            "asset://webapp-01/http", "scan"))
        self.assertEqual(d, Decision.DENY)
        self.assertIn("holder", reason)


class SimulationTests(unittest.TestCase):
    def test_baseline_is_fully_compromised(self):
        res = sim.run_baseline()
        s = sim.summarize(res)
        self.assertEqual(s["authorized"], len(sim.KILL_CHAIN))
        self.assertTrue(s["lateral_movement_succeeded"])
        self.assertTrue(s["exfiltration_succeeded"])
        self.assertEqual(s["contained_at_phase"], "NOT CONTAINED")

    def test_proposed_blocks_lateral_movement_and_exfiltration(self):
        res = sim.run_proposed(human_approves=False)
        s = sim.summarize(res)
        self.assertFalse(s["lateral_movement_succeeded"])
        self.assertFalse(s["exfiltration_succeeded"])
        # Only the in-scope recon of webapp-01 should get through.
        self.assertLess(s["authorized"], len(sim.KILL_CHAIN))
        self.assertNotEqual(s["contained_at_phase"], "NOT CONTAINED")

    def test_proposed_blast_radius_is_smaller(self):
        base = sim.summarize(sim.run_baseline())
        prop = sim.summarize(sim.run_proposed(human_approves=False))
        self.assertLess(prop["blast_radius_resources"],
                        base["blast_radius_resources"])

    def test_even_with_careless_human_scope_still_binds(self):
        # If the human rubber-stamps escalations, HIGH actions pass, but actions
        # that are out of RESOURCE/ACTION scope are still denied by caveats
        # regardless of the human (defence in depth).
        res = sim.run_proposed(human_approves=True)
        s = sim.summarize(res)
        # export is not an allowed action in any caveat -> still blocked
        self.assertFalse(s["exfiltration_succeeded"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
