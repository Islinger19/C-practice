"""
run_demo.py
===========

End-to-end driver for the GTG-1002 counterfactual case study. It:

  1. runs the kill-chain simulation against the baseline (inherited
     credentials) and the proposed (NHI + scoped delegation) models,
  2. prints a side-by-side transcript and metric table,
  3. writes machine-readable metrics to ../figures/metrics.json, and
  4. renders publication-quality figures (matplotlib) into ../figures/.

Usage:
    python3 run_demo.py            # full run + figures
    python3 run_demo.py --no-plot  # metrics only (no matplotlib needed)
"""

from __future__ import annotations

import json
import os
import sys

import attack_simulation as sim

FIG_DIR = os.path.join(os.path.dirname(__file__), "..", "figures")
os.makedirs(FIG_DIR, exist_ok=True)

# Report colour rule (CA-2 notice): black and blue only.
C_BASELINE = "#000000"   # black  (baseline / inherited credentials)
C_PROPOSED = "#0072B2"   # blue   (proposed / scoped delegation)
C_GRID = "#CCCCCC"       # neutral grey gridlines


def collect():
    baseline = sim.run_baseline()
    proposed = sim.run_proposed(human_approves=False)
    return baseline, proposed


def print_report(baseline, proposed):
    print("=" * 78)
    print(" GTG-1002 COUNTERFACTUAL KILL-CHAIN SIMULATION ".center(78, "="))
    print("=" * 78)
    for res in (baseline, proposed):
        print(f"\n### {res.model}\n")
        for line in res.transcript:
            print("   " + line)
    print("\n" + "-" * 78)
    print(" METRIC COMPARISON ".center(78, "-"))
    print("-" * 78)
    sb, sp = sim.summarize(baseline), sim.summarize(proposed)
    rows = [
        ("Tool actions attempted", sb["attempted"], sp["attempted"]),
        ("Actions authorized", sb["authorized"], sp["authorized"]),
        ("Actions blocked by policy", sb["blocked"], sp["blocked"]),
        ("Actions escalated to a human", sb["escalated_to_human"],
         sp["escalated_to_human"]),
        ("Blast radius (distinct resources)", sb["blast_radius_resources"],
         sp["blast_radius_resources"]),
        ("Lateral movement succeeded", sb["lateral_movement_succeeded"],
         sp["lateral_movement_succeeded"]),
        ("Bulk exfiltration succeeded", sb["exfiltration_succeeded"],
         sp["exfiltration_succeeded"]),
        ("Contained at phase", sb["contained_at_phase"],
         sp["contained_at_phase"]),
    ]
    print(f"\n{'Metric':38s} {'Baseline':>18s} {'Proposed':>18s}")
    print("-" * 78)
    for name, b, p in rows:
        print(f"{name:38s} {str(b):>18s} {str(p):>18s}")
    print("-" * 78)
    return sb, sp


def write_metrics(baseline, proposed):
    data = {
        "kill_chain_steps": [
            {"phase": s.phase, "action": s.action, "resource": s.resource,
             "sensitivity": s.sensitivity, "in_task_scope": s.in_task_scope}
            for s in sim.KILL_CHAIN
        ],
        "baseline": sim.summarize(baseline),
        "proposed": sim.summarize(proposed),
        "proposed_transcript": proposed.transcript,
        "human_prompts_in_proposed": getattr(proposed, "_human_prompts", None),
    }
    path = os.path.join(FIG_DIR, "metrics.json")
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"\n[+] metrics written to {os.path.normpath(path)}")
    return data


def make_figures(baseline, proposed):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 11,
        "axes.edgecolor": "#444444",
        "axes.grid": True,
        "grid.color": C_GRID,
        "grid.linewidth": 0.6,
        "figure.dpi": 150,
    })

    sb, sp = sim.summarize(baseline), sim.summarize(proposed)

    # --- Figure 1: outcome comparison bar chart --------------------------- #
    labels = ["Actions\nauthorized", "Actions\nblocked",
              "Escalated\nto human", "Blast radius\n(resources)"]
    base_vals = [sb["authorized"], sb["blocked"],
                 sb["escalated_to_human"], sb["blast_radius_resources"]]
    prop_vals = [sp["authorized"], sp["blocked"],
                 sp["escalated_to_human"], sp["blast_radius_resources"]]

    import numpy as np
    x = np.arange(len(labels))
    w = 0.38
    fig, ax = plt.subplots(figsize=(8, 4.5))
    b1 = ax.bar(x - w / 2, base_vals, w, label="Baseline (inherited creds)",
                color=C_BASELINE)
    b2 = ax.bar(x + w / 2, prop_vals, w,
                label="Proposed (NHI + scoped delegation)", color=C_PROPOSED)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("Count")
    ax.set_title("GTG-1002 kill chain: authorization outcomes by model")
    ax.legend(frameon=False, loc="upper right")
    for bars in (b1, b2):
        ax.bar_label(bars, padding=2, fontsize=9)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "fig1_outcomes.png"),
                bbox_inches="tight")
    plt.close(fig)

    # --- Figure 2: blast-radius containment per phase --------------------- #
    # Cumulative distinct resources reached as the kill chain progresses.
    phases, base_cum, prop_cum = [], [], []
    seen_b, seen_p = set(), set()
    # Recompute per-step reachability.
    prop_res = sim.run_proposed(human_approves=False)
    allowed_prop = set()
    for line in prop_res.transcript:
        if line.strip().startswith("[") and "ALLOW" in line:
            allowed_prop.add(line.split()[-1])
    for i, step in enumerate(sim.KILL_CHAIN, 1):
        seen_b.add(step.resource)                 # baseline reaches everything
        if step.resource in allowed_prop:
            seen_p.add(step.resource)
        phases.append(i)
        base_cum.append(len(seen_b))
        prop_cum.append(len(seen_p))

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(phases, base_cum, "-o", color=C_BASELINE,
            label="Baseline (inherited creds)")
    ax.plot(phases, prop_cum, "-s", color=C_PROPOSED,
            label="Proposed (NHI + scoped delegation)")
    ax.set_xlabel("Kill-chain step (recon → exfiltration)")
    ax.set_ylabel("Cumulative distinct resources reached")
    ax.set_title("Blast-radius containment across the kill chain")
    ax.legend(frameon=False, loc="upper left")
    ax.set_xticks(phases)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "fig2_blast_radius.png"),
                bbox_inches="tight")
    plt.close(fig)

    print(f"[+] figures written to {os.path.normpath(FIG_DIR)}/"
          " (fig1_outcomes.png, fig2_blast_radius.png)")


def main():
    baseline, proposed = collect()
    print_report(baseline, proposed)
    write_metrics(baseline, proposed)
    if "--no-plot" not in sys.argv:
        try:
            make_figures(baseline, proposed)
        except ImportError:
            print("[!] matplotlib/numpy not installed - skipping figures "
                  "(run with --no-plot to silence).")


if __name__ == "__main__":
    main()
