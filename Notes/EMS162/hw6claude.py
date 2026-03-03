import numpy as np
import matplotlib.pyplot as plt

# ✅ Make all fonts bigger globally
plt.rcParams.update({"font.size": 20})


N_data = [6, 20, 1000]
phi_axis = np.linspace(0, 4 * np.pi, 200000)
wave_length = 1.54184
a_vec = 4

# ---------------------------------------------------------
# Interference function for N = 6, 20, 1000
# ---------------------------------------------------------
intensity_phi = np.empty((len(N_data), len(phi_axis)))

for i, N in enumerate(N_data):
    numerator = np.sin(N * phi_axis / 2) ** 2
    denominator = np.sin(phi_axis / 2) ** 2
    intensity_phi[i] = np.where(
        denominator > 1e-12,
        numerator / denominator,
        float(N**2),
    )

# ---------------------------------------------------------
# Atomic scattering factor coefficients
# f(s) = sum a_i * exp(-b_i * s^2) + c,  s = sin(theta)/lambda
# ---------------------------------------------------------
atomic_scattering_coeffs = {
    "H": {
        "a": np.array([0.489918, 0.262003, 0.196767, 0.049879]),
        "b": np.array([20.659300, 7.740390, 49.551900, 2.201590]),
        "c": 0.001305,
    },
    "He": {
        "a": np.array([0.873400, 0.630900, 0.311200, 0.178000]),
        "b": np.array([9.103700, 3.356800, 22.927600, 0.982100]),
        "c": 0.006400,
    },
    "Li": {
        "a": np.array([1.128200, 0.750800, 0.617500, 0.465300]),
        "b": np.array([3.954600, 1.052400, 85.390500, 168.261000]),
        "c": 0.037700,
    },
    "Be": {
        "a": np.array([1.591900, 1.127800, 0.539100, 0.702900]),
        "b": np.array([43.642700, 1.862300, 103.483000, 542.000000]),
        "c": 0.038500,
    },
    "B": {
        "a": np.array([2.054500, 1.332600, 1.097900, 0.706800]),
        "b": np.array([23.218500, 1.021000, 60.349800, 0.140300]),
        "c": -0.193200,
    },
    "C": {
        "a": np.array([2.310000, 1.020000, 1.588600, 0.865000]),
        "b": np.array([20.843900, 10.207500, 0.568700, 51.651200]),
        "c": 0.215600,
    },
    "N": {
        "a": np.array([12.212600, 3.132200, 2.012500, 1.166300]),
        "b": np.array([0.005700, 9.893300, 28.997500, 0.582600]),
        "c": -11.529000,
    },
    "O": {
        "a": np.array([3.048500, 2.286800, 1.546300, 0.867000]),
        "b": np.array([13.277100, 5.701100, 0.323900, 32.908900]),
        "c": 0.250800,
    },
    "F": {
        "a": np.array([3.539200, 2.641200, 1.517000, 1.024300]),
        "b": np.array([10.282500, 4.294400, 0.261500, 26.147600]),
        "c": 0.277600,
    },
    "Ne": {
        "a": np.array([3.955300, 3.112500, 1.454600, 1.125100]),
        "b": np.array([8.404200, 3.426200, 0.230600, 21.718400]),
        "c": 0.351500,
    },
    "Na": {
        "a": np.array([4.762600, 3.173600, 1.267400, 1.112800]),
        "b": np.array([3.285000, 8.842200, 0.313600, 129.424000]),
        "c": 0.676000,
    },
    "Mg": {
        "a": np.array([5.420400, 2.173500, 1.226900, 2.307300]),
        "b": np.array([2.827500, 79.261100, 0.380800, 7.193700]),
        "c": 0.858400,
    },
    "Al": {
        "a": np.array([6.420200, 1.900200, 1.593600, 1.964600]),
        "b": np.array([3.038700, 0.742600, 31.547200, 85.088600]),
        "c": 1.115100,
    },
    "Si": {
        "a": np.array([5.662690, 3.071640, 2.624460, 1.393200]),
        "b": np.array([2.665200, 38.663400, 0.916946, 93.545800]),
        "c": 1.247070,
    },
    "Co": {
        "a": np.array([12.2841, 7.34050, 4.00340, 2.34880]),
        "b": np.array([4.27910, 0.278400, 13.5359, 71.1692]),
        "c": 1.01180,
    },
}


def atomic_form_factor(element, phi, wavelength, a):
    """
    Compute f(s) where s = sin(theta)/lambda, derived from phase angle phi.
    phi = 4*pi*a*sin^2(theta)/lambda
    => sin^2(theta) = phi*lambda / (4*pi*a)
    => s^2 = sin^2(theta)/lambda^2 = phi / (4*pi*a*lambda)
    """
    coeff = atomic_scattering_coeffs[element]
    s2 = np.where(
        phi > 0,
        phi / (4 * np.pi * a * wavelength),
        0.0,
    )
    a_i = coeff["a"]
    b_i = coeff["b"]
    c = coeff["c"]
    f = (
        np.sum(a_i[:, None] * np.exp(-b_i[:, None] * s2[None, :]), axis=0) + c
    )
    return f


# ---------------------------------------------------------
# Co intensity for N = 20
# ---------------------------------------------------------
N_co = 20
numerator_co = np.sin(N_co * phi_axis / 2) ** 2
denominator_co = np.sin(phi_axis / 2) ** 2
interference_co = np.where(
    denominator_co > 1e-12,
    numerator_co / denominator_co,
    float(N_co**2),
)

f_co = atomic_form_factor("Co", phi_axis, wave_length, a_vec)
intensity_co = f_co**2 * interference_co

# ---------------------------------------------------------
# Plotting — 1 row, 4 columns
# ---------------------------------------------------------
fig, axes = plt.subplots(2, 2, figsize=(20, 16))
axes = axes.flatten()

labels = [f"N = {N}" for N in N_data] + ["Co, N = 20"]
colors = ["g", "b", "r", "darkorange"]
y_data = list(intensity_phi) + [intensity_co]
y_labels = [
    "Interference",
    "Interference",
    "Interference",
    r"$f^2 \cdot$ Interference",
]

for ax, y, label, color, ylabel in zip(
    axes, y_data, labels, colors, y_labels
):
    ax.plot(phi_axis, y, color=color, lw=0.8, label=label)
    ax.set_xlabel("Phase angle [radians]")
    ax.set_ylabel(ylabel)
    ax.set_xticks([0, np.pi, 2 * np.pi, 3 * np.pi, 4 * np.pi])
    ax.set_xticklabels(["0", "π", "2π", "3π", "4π"])
    ax.legend()

plt.tight_layout()
plt.show()