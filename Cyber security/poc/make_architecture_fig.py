"""
make_architecture_fig.py
=========================

Renders the proposed defence architecture (Figure 3 in the report) using
matplotlib primitives only, so it stays reproducible and theme-consistent
with the other figures. Produces ../figures/fig3_architecture.png.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

FIG_DIR = os.path.join(os.path.dirname(__file__), "..", "figures")
os.makedirs(FIG_DIR, exist_ok=True)

# Report colour rule (CA-2 notice): black and blue only (grey allowed as neutral).
BLUE = "#0072B2"
GREEN = "#1F3864"   # navy (re-used where a second blue is needed)
ORANGE = "#000000"  # black (re-used where a distinct emphasis colour is needed)
GREY = "#555555"
LIGHT = "#EAF3FA"


def box(ax, x, y, w, h, text, fc=LIGHT, ec=BLUE, fs=9, bold=False):
    p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.06",
                       linewidth=1.4, edgecolor=ec, facecolor=fc)
    ax.add_patch(p)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fs, fontweight="bold" if bold else "normal", color="#111")


def arrow(ax, x1, y1, x2, y2, text="", color=GREY, style="-|>",
          conn="arc3,rad=0", lx=None, ly=None):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style,
                        connectionstyle=conn, mutation_scale=14,
                        linewidth=1.3, color=color)
    ax.add_patch(a)
    if text:
        tx = lx if lx is not None else (x1 + x2) / 2
        ty = ly if ly is not None else (y1 + y2) / 2 + 0.07
        ax.text(tx, ty, text, ha="center", va="bottom", fontsize=7.5,
                color=color)


fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6.9)
ax.axis("off")

# Human principal
box(ax, 0.2, 4.8, 1.9, 0.9, "Human\nprincipal", fc="#EEF2F8", ec=ORANGE, bold=True)
# Delegation authority
box(ax, 0.2, 2.9, 1.9, 1.0,
    "Delegation /\nAuthz Authority\n(OAuth2.1 AS,\nSPIRE, A2A IdP)",
    fc="#E6ECF5", ec=GREEN, fs=8, bold=True)

# Orchestrator agent (own NHI)
box(ax, 3.0, 4.6, 2.3, 1.1,
    "Orchestrator agent\nNHI: spiffe://.../orchestrator\nper-task scoped token",
    fs=8, bold=True)
# Sub-agent
box(ax, 3.0, 2.7, 2.3, 1.1,
    "Recon sub-agent\nNHI: spiffe://.../recon\nattenuated token (A2A hop)",
    fs=8, bold=True)

# PDP
box(ax, 6.3, 3.5, 1.6, 1.3,
    "Policy\nDecision\nPoint (PDP)\n+ HITL gate", fc="#EEF2F8", ec=ORANGE,
    fs=8.5, bold=True)

# Tools / MCP servers
box(ax, 8.2, 5.1, 1.6, 0.7, "MCP tool:\nscanner", fs=8)
box(ax, 8.2, 4.2, 1.6, 0.7, "MCP tool:\nDB / API", fs=8)
box(ax, 8.2, 3.3, 1.6, 0.7, "MCP tool:\nsecrets", fs=8)
box(ax, 8.2, 2.4, 1.6, 0.7, "MCP tool:\ncloud", fs=8)

# Audit log
box(ax, 6.3, 1.4, 1.6, 0.8, "Tamper-evident\naudit log", fc="#F2F2F2",
    ec=GREY, fs=8, bold=True)

# Arrows
arrow(ax, 1.15, 4.8, 1.15, 3.9, "delegates\n(signed)", color=ORANGE)
arrow(ax, 2.1, 3.4, 3.0, 4.8, "mint per-task\nscoped token", color=GREEN)
arrow(ax, 4.15, 4.6, 4.15, 3.8, "attenuate\n(narrow only)", color=BLUE)
arrow(ax, 5.3, 3.25, 6.3, 3.9, "tool call\n+ token", color=GREY)
arrow(ax, 7.9, 4.4, 8.2, 4.55, "ALLOW", color=BLUE)
arrow(ax, 7.9, 3.9, 8.2, 3.65, "DENY /\nESCALATE", color=ORANGE)
arrow(ax, 7.1, 3.5, 7.1, 2.2, "every\ndecision", color=GREY)
# HITL back to human - arc high above the agent boxes so it never crosses them
arrow(ax, 6.9, 4.8, 1.15, 5.7, "escalate high-impact actions to human (HITL)",
      color=ORANGE, conn="arc3,rad=-0.3", lx=4.0, ly=6.15)

ax.text(5.0, 6.7, "Proposed defence: Non-Human Identity + Scoped, Attenuable, "
        "Auditable Delegation",
        ha="center", va="center", fontsize=11, fontweight="bold", color="#111")

fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, "fig3_architecture.png"),
            bbox_inches="tight", dpi=150)
plt.close(fig)
print("wrote", os.path.normpath(os.path.join(FIG_DIR, "fig3_architecture.png")))
