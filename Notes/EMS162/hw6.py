import numpy as np
import matplotlib.pyplot as plt

N_data = [6, 20, 1000]
phi_axis = np.linspace(0, 4 * np.pi, 200000)
wave_length = 1.54184
a_vec = 4

intensity_phi = np.empty((len(N_data), len(phi_axis)))

for i, N in enumerate(N_data):
    numerator = np.sin(N * phi_axis / 2)**2
    denominator = np.sin(phi_axis / 2)**2

    # Avoid division by zero using where
    intensity = np.where(
        denominator > 1e-12,
        numerator / denominator,
        N**2   # correct limiting value
    )

    intensity_phi[i] = intensity
    #intensity_phi[i] = intensity / N**2  # normalize



# ---------------------------------------------------------
# Atomic scattering factor coefficients
# f(sin(theta)/lambda) = sum_{i=1}^4 a_i exp(-b_i (sinθ/λ)^2) + c
# ---------------------------------------------------------

atomic_scattering_coeffs = {
    "H":  {
        "a": np.array([0.489918, 0.262003, 0.196767, 0.049879]),
        "b": np.array([20.659300, 7.740390, 49.551900, 2.201590]),
        "c": 0.001305
    },
    "He": {
        "a": np.array([0.873400, 0.630900, 0.311200, 0.178000]),
        "b": np.array([9.103700, 3.356800, 22.927600, 0.982100]),
        "c": 0.006400
    },
    "Li": {
        "a": np.array([1.128200, 0.750800, 0.617500, 0.465300]),
        "b": np.array([3.954600, 1.052400, 85.390500, 168.261000]),
        "c": 0.037700
    },
    "Be": {
        "a": np.array([1.591900, 1.127800, 0.539100, 0.702900]),
        "b": np.array([43.642700, 1.862300, 103.483000, 542.000000]),
        "c": 0.038500
    },
    "B": {
        "a": np.array([2.054500, 1.332600, 1.097900, 0.706800]),
        "b": np.array([23.218500, 1.021000, 60.349800, 0.140300]),
        "c": -0.193200
    },
    "C": {
        "a": np.array([2.310000, 1.020000, 1.588600, 0.865000]),
        "b": np.array([20.843900, 10.207500, 0.568700, 51.651200]),
        "c": 0.215600
    },
    "N": {
        "a": np.array([12.212600, 3.132200, 2.012500, 1.166300]),
        "b": np.array([0.005700, 9.893300, 28.997500, 0.582600]),
        "c": -11.529000
    },
    "O": {
        "a": np.array([3.048500, 2.286800, 1.546300, 0.867000]),
        "b": np.array([13.277100, 5.701100, 0.323900, 32.908900]),
        "c": 0.250800
    },
    "F": {
        "a": np.array([3.539200, 2.641200, 1.517000, 1.024300]),
        "b": np.array([10.282500, 4.294400, 0.261500, 26.147600]),
        "c": 0.277600
    },
    "Ne": {
        "a": np.array([3.955300, 3.112500, 1.454600, 1.125100]),
        "b": np.array([8.404200, 3.426200, 0.230600, 21.718400]),
        "c": 0.351500
    },
    "Na": {
        "a": np.array([4.762600, 3.173600, 1.267400, 1.112800]),
        "b": np.array([3.285000, 8.842200, 0.313600, 129.424000]),
        "c": 0.676000
    },
    "Mg": {
        "a": np.array([5.420400, 2.173500, 1.226900, 2.307300]),
        "b": np.array([2.827500, 79.261100, 0.380800, 7.193700]),
        "c": 0.858400
    },
    "Al": {
        "a": np.array([6.420200, 1.900200, 1.593600, 1.964600]),
        "b": np.array([3.038700, 0.742600, 31.547200, 85.088600]),
        "c": 1.115100
    },
    "Si": {
        "a": np.array([5.662690, 3.071640, 2.624460, 1.393200]),
        "b": np.array([2.665200, 38.663400, 0.916946, 93.545800]),
        "c": 1.247070
    }
}

# ---------------------------------------------------------
# Atomic form factor
# ---------------------------------------------------------

def atomic_form_factor(element, theta, a_vec, phase_angle):
    coeff = atomic_scattering_coeffs[element]
    s = phase_angle / (4 * np.pi * a_vec * np.sin(theta))
    a = coeff["a"]
    b = coeff["b"]
    c = coeff["c"]
    return np.sum(a[:, None] * np.exp(-b[:, None] * s**2), axis=0) + c



 
numerator = np.sin(20 * phi_axis / 2)**2
denominator = np.sin(phi_axis / 2)**2

# Avoid division by zero using where
intensity = np.where(
    denominator > 1e-12,
    numerator / denominator,
    20**2   # correct limiting value
)

theta = np.arcsin((wave_length/(4*np.pi*a_vec) * phi_axis) ** (1/2))

krawitz_intensity = atomic_form_factor('Co', theta, a_vec, phi_axis) ** 2 * intensity









fig, ax = plt.subplots(1, len(N_data), figsize=(30, 8))

for i, N in enumerate(N_data):
    ax[i].plot(phi_axis, intensity_phi[i], "g-",
               label=f"N = {N} atoms")
    ax[i].legend()
    ax[i].set_xlabel("phase angle [radians]")
    ax[i].set_ylabel("Interference")

plt.tight_layout()
plt.show()