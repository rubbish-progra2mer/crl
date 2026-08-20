"""
Reconstructs Figure 1 (ToolBench difficulty buckets, N=50) and
Figure 2 (scorer ablation on MetaTool) from the numbers reported in the paper.
These are stand-ins that match the reported values; replace with the originals
if you still have the source plots.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({
    "font.size": 11,
    "axes.titlesize": 12,
    "axes.spreadsize" if False else "axes.labelsize": 11,
    "figure.dpi": 150,
})

BOR   = "#1f77b4"   # blue
F1    = "#ff7f0e"   # orange
FK5   = "#2ca02c"   # green

# ----------------------------------------------------------------------
# Figure 1: ToolBench difficulty buckets at N=50
# ----------------------------------------------------------------------
buckets = ["Easy\n(rank 1)\nn=272", "Medium\n(rank 2-5)\nn=116",
           "Hard\n(rank 6-20)\nn=76", "Very Hard\n(rank 21+)\nn=136"]
x = np.arange(len(buckets))
w = 0.27

# Left panel: chosen K
bor_K   = [2.5, 4.8, 5.7, 6.9]
bor_Ke  = [0.2, 0.5, 0.5, 0.7]
f1_K    = [1.5, 1.5, 1.5, 1.5]
fk5_K   = [5.0, 5.0, 5.0, 5.0]

# Right panel: found %
bor_F   = [100.0, 74.4, 16.7, 0.2]
bor_Fe  = [0.0, 0.4, 4.3, 0.0]
f1_F    = [100.0, 11.0, 0.0, 0.0]
fk5_F   = [100.0, 100.0, 0.0, 0.0]

fig, (axL, axR) = plt.subplots(1, 2, figsize=(11, 4.2))

axL.bar(x - w, bor_K, w, yerr=bor_Ke, capsize=3, label="BoR", color=BOR)
axL.bar(x,     f1_K,  w, label="$F_1$ ablation", color=F1)
axL.bar(x + w, fk5_K, w, label="FK=5", color=FK5)
axL.set_ylabel("Chosen $K$")
axL.set_title("Depth per difficulty bucket")
axL.set_xticks(x); axL.set_xticklabels(buckets)
axL.set_ylim(0, 10)
axL.legend(frameon=False, fontsize=9)

axR.bar(x - w, bor_F, w, yerr=bor_Fe, capsize=3, label="BoR", color=BOR)
axR.bar(x,     f1_F,  w, label="$F_1$ ablation", color=F1)
axR.bar(x + w, fk5_F, w, label="FK=5", color=FK5)
axR.set_ylabel("Found rate (%)")
axR.set_title("Coverage per difficulty bucket")
axR.set_xticks(x); axR.set_xticklabels(buckets)
axR.set_ylim(0, 110)
axR.legend(frameon=False, fontsize=9)

fig.tight_layout()
fig.savefig("figure1.pdf", bbox_inches="tight")
plt.close(fig)

# ----------------------------------------------------------------------
# Figure 2: Scorer ablation on MetaTool
# ----------------------------------------------------------------------
scorers = ["BM25\n(found@1=33%)", "MiniLM-L6-v2\n(found@1=60%)",
           "BGE-base-en-v1.5\n(found@1=57%)"]
xs = np.arange(len(scorers))
learned_K = [80.7, 2.3, 2.4]
bits      = [1.04, 4.44, 4.24]
cols      = ["#d62728", BOR, "#9467bd"]

fig2, (a, b) = plt.subplots(1, 2, figsize=(11, 4.2))

bars = a.bar(xs, learned_K, color=cols, width=0.6)
a.set_ylabel("Learned $K$")
a.set_title("Depth learned per scorer")
a.set_xticks(xs); a.set_xticklabels(scorers)
a.set_ylim(0, 90)
for r, v in zip(bars, learned_K):
    a.text(r.get_x() + r.get_width()/2, v + 1.5, f"{v}", ha="center", fontweight="bold")

bars2 = b.bar(xs, bits, color=cols, width=0.6)
b.set_ylabel("BoR (bits)")
b.set_title("Selectivity per scorer")
b.set_xticks(xs); b.set_xticklabels(scorers)
b.set_ylim(0, 5.2)
for r, v in zip(bars2, bits):
    b.text(r.get_x() + r.get_width()/2, v + 0.08, f"{v}", ha="center", fontweight="bold")

fig2.tight_layout()
fig2.savefig("figure2.pdf", bbox_inches="tight")
plt.close(fig2)

print("wrote figure1.pdf and figure2.pdf")
