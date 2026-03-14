import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq

# ── Fixed parameters ─────────────────────────────────────────────────────────
St = 58.6        # Material bending strength [MPa]
YN = 1.0         # Stress cycle factor
mt = 5.0         # Module [mm]
YJ = 0.33        # Geometry (Lewis) factor for pinion
kT = 1.0         # Temperature factor
kR = 1.0         # Reliability factor
Wt = 3201.0      # Transmitted load [N]
Ko = 1.0         # Overload factor
Kv = 1.125       # Dynamic factor
Ks = 1.0         # Size factor
KB = 1.0         # Rim thickness factor
dp_mm = 100.0    # Pinion pitch diameter [mm]
dp_in = dp_mm / 25.4


def Km(b_mm):
    """Load distribution factor as a function of face width [mm]."""
    F = b_mm / 25.4  # convert to inches
    ratio = F / dp_in

    if np.isscalar(F):
        if ratio <= 0.05:
            Cpf = 0.05
        elif ratio <= 0.5:
            Cpf = F / (10 * dp_in) - 0.025
        else:
            Cpf = F / (10 * dp_in) - 0.0375 + 0.0125 * F
    else:
        Cpf = np.where(
            ratio <= 0.05,
            0.05,
            np.where(
                ratio <= 0.5,
                F / (10 * dp_in) - 0.025,
                F / (10 * dp_in) - 0.0375 + 0.0125 * F,
            ),
        )

    # Cma is only valid over a limited F range — clamp to >= 0
    Cma = 0.127 + 0.0158 * F - 9.720e-4 * F**2
    Cma = np.maximum(Cma, 0.0)

    return 1 + Cpf + Cma


def nb(b_mm):
    """Bending safety factor as a function of face width [mm]."""
    b = np.asarray(b_mm, dtype=float)
    return (St * YN * b * mt * YJ) / (kT * kR * Wt * Ko * Kv * Ks * Km(b) * KB)


def face_width_for_fos(target_fos, b_min_mm=1.0, b_max_mm=1000.0):
    """
    Given a target bending safety factor, return the required
    face width in inches and mm using a root-finding solver.

    Parameters
    ----------
    target_fos : float — desired safety factor
    b_min_mm   : float — lower search bound [mm]
    b_max_mm   : float — upper search bound [mm]

    Returns
    -------
    b_in : float — required face width [inches]
    b_mm : float — required face width [mm]
    """
    func = lambda b: nb(b) - target_fos

    fa = func(b_min_mm)
    fb = func(b_max_mm)

    # Check that a root exists in the interval
    if fa * fb > 0:
        nb_max = nb(b_max_mm)
        raise ValueError(
            f"No solution found in [{b_min_mm}, {b_max_mm}] mm. "
            f"Max achievable FOS in range = {nb_max:.3f}. "
            f"Try increasing b_max_mm."
        )

    b_sol_mm = brentq(func, b_min_mm, b_max_mm)
    b_sol_in = b_sol_mm / 25.4
    print(
        f"For FOS = {target_fos:.4g}: "
        f"face width = {b_sol_mm:.4f} mm  ({b_sol_in:.4f} in)"
    )
    return b_sol_in, b_sol_mm


# ── Solve for target FOS = 5 ──────────────────────────────────────────────────
target_fos = 3.0
b_fos5_in, b_fos5_mm = face_width_for_fos(target_fos)

# ── Compute curve ─────────────────────────────────────────────────────────────
b_range = np.linspace(1, 2 * 250, 2 * 1000)  # mm
nb_vals = nb(b_range)

max_nb = 7.0
mask = nb_vals <= max_nb

# ── Cases from the table ──────────────────────────────────────────────────────
cases = [
    {"b": 6,     "label": "Case 1\n(b=6 mm, FAIL)",      "color": "red"},
    {"b": 50,    "label": "Case 2\n(b=50 mm, PASS)",     "color": "green"},
    {"b": 49.16, "label": "Case 3\n(b=49.16 mm, LIMIT)", "color": "orange"},
]

# ── Plot ──────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(9, 5))

ax.plot(b_range[mask], nb_vals[mask], color="steelblue", linewidth=2.5,
        label=r"$n_b(b)$")

# nb = 1 threshold
ax.axhline(1.0, color="black", linestyle="--", linewidth=1.2,
           label=r"$n_b = 1$ (minimum)")

# Existing cases
for c in cases:
    nb_pt = float(nb(c["b"]))
    if nb_pt <= max_nb:
        ax.scatter(c["b"], nb_pt, color=c["color"], zorder=5, s=60)
        ax.annotate(
            c["label"],
            xy=(c["b"], nb_pt),
            xytext=(c["b"] + 6, nb_pt + 0.15),
            fontsize=8,
            color=c["color"],
            arrowprops=dict(arrowstyle="->", color=c["color"], lw=1),
        )

# ── FOS = 5 annotation ────────────────────────────────────────────────────────
ax.scatter(b_fos5_mm, target_fos, color="purple", zorder=6, s=80)
ax.axhline(target_fos, color="purple", linestyle=":", linewidth=1.2,
           label=rf"$n_b = {target_fos:.0f}$")
ax.axvline(b_fos5_mm, color="purple", linestyle=":", linewidth=1.2)
ax.annotate(
    f"FOS = {target_fos:.0f}\n"
    f"b = {b_fos5_mm:.1f} mm\n"
    f"b = {b_fos5_in:.3f} in",
    xy=(b_fos5_mm, target_fos),
    xytext=(b_fos5_mm + 15, target_fos - 0.7),
    fontsize=9,
    color="purple",
    arrowprops=dict(arrowstyle="->", color="purple", lw=1),
)

ax.set_xlabel("Face Width $b$ (mm)", fontsize=12)
ax.set_ylabel("Bending Safety Factor $n_b$", fontsize=12)
ax.set_title(
    "Bending Safety Factor vs. Face Width\n(Last Gear Pair, Pinion)",
    fontsize=13,
)
ax.set_xlim(0, 500)
ax.set_ylim(0, max_nb)
ax.legend(fontsize=10)
ax.grid(True, linestyle=":", alpha=0.6)

plt.tight_layout()
plt.savefig("safety_factor_vs_face_width.png", dpi=150)
plt.show()