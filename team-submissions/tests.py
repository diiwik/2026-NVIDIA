import cudaq
import numpy as np
from math import floor
import tutorial_notebook.auxiliary_files.labs_utils as utils
import matplotlib.pyplot as plt

@cudaq.kernel
def rzz(q0: cudaq.qubit, q1: cudaq.qubit, theta: float):
    cx(q0, q1)
    rz(2 * theta, q1)
    cx(q0, q1)

@cudaq.kernel
def two_qubit_block(q0: cudaq.qubit, q1: cudaq.qubit, theta: float):
    rx(math.pi / 2, q1)
    rzz(q0, q1, theta)
    rx(-math.pi / 2, q1)

    rx(math.pi / 2, q0)
    rzz(q0, q1, theta)
    rx(-math.pi / 2, q0)

@cudaq.kernel
def four_qubit_block(
    q0: cudaq.qubit,
    q1: cudaq.qubit,
    q2: cudaq.qubit,
    q3: cudaq.qubit,
    theta: float
):
    rx(-math.pi/2, q0)
    ry(math.pi/2, q1)
    ry(-math.pi/2, q2)
    rzz(q0, q1, -theta)
    rzz(q2, q3, -theta)
    rx(math.pi/2, q0)
    ry(-math.pi/2, q1)
    rx(-math.pi/2, q1)
    ry(math.pi/2, q2)
    rx(-math.pi/2, q2)
    rx(-math.pi/2, q3)
    rzz(q1, q2, theta)

    rx(math.pi/2, q1)
    rx(math.pi, q2)
    ry(-math.pi/2, q1)
    rzz(q0, q1, theta)
    rx(math.pi/2, q0)
    ry(-math.pi/2, q1)
    rzz(q1, q2, -theta)
    rx(math.pi/2, q1)
    rx(-math.pi, q2)
    rzz(q1, q2, -theta)

    rx(-math.pi, q1)
    ry(math.pi/2, q1)
    rzz(q2, q3, -theta)
    ry(-math.pi/2, q2)
    rx(-math.pi/2, q3)
    rx(-math.pi/2, q2)

    rzz(q1, q2, theta)
    rx(math.pi/2, q1)
    rx(math.pi/2, q2)
    ry(-math.pi/2, q1)
    ry(math.pi/2, q2)
    rzz(q0, q1, theta)
    rzz(q2, q3, theta)
    ry(math.pi/2, q1)
    ry(-math.pi/2, q2)
    rx(math.pi/2, q3)

def get_interactions(N):
    G2 = []
    G4 = []

    # Two-body terms
    for i in range(N - 2):
        max_k = (N - i) // 2
        for k in range(1, max_k + 1):
            G2.append([i, i + k])

    # Four-body terms
    for i in range(N - 3):
        max_t = (N - i - 1) // 2
        for t in range(1, max_t + 1):
            for k in range(t + 1, N - i - t):
                G4.append([i, i + t, i + k, i + k + t])

    return G2, G4

@cudaq.kernel
def trotterized_circuit(
    N: int,
    G2: list[list[int]],
    G4: list[list[int]],
    steps: int,
    dt: float,
    thetas: list[float]
):
    reg = cudaq.qvector(N)

    for q in reg:
        h(q)

    for step in range(steps):
        theta = thetas[step]

        for term in G2:
            i, j = term
            two_qubit_block(reg[i], reg[j], dt * theta)

        for term in G4:
            i, j, k, l = term
            four_qubit_block(reg[i],reg[j],reg[k],reg[l],dt * theta)

def build_hamiltonian(N, G2, G4, J=1.0, K=1.0):
    H = cudaq.SpinOperator()

    # 2-body ZZ terms
    for (i, j) in G2:
        H += J * cudaq.spin.z(i) * cudaq.spin.z(j)

    # 4-body XXXX terms
    for (i, j, k, l) in G4:
        H += K * (
            cudaq.spin.x(i) *
            cudaq.spin.x(j) *
            cudaq.spin.x(k) *
            cudaq.spin.x(l)
        )

    return H
def energy(theta_vals):
    result = cudaq.observe(trotterized_circuit,H,N,G2,G4,n_steps,dt,theta_vals)
    return result.expectation()
def vqe_energy(steps):
    dt = T / steps

    def energy(theta):
        return cudaq.observe(trotterized_circuit,H,N,G2,G4,steps,dt,theta).expectation()

    init_theta = np.random.uniform(0, 0.1, size=steps)
    res = minimize(energy,init_theta,method="COBYLA",options={"maxiter": 50})

    return res.fun

def fixed_trotter_energy(steps):
    dt = T / steps
    thetas = []
    for step in range(1, steps + 1):
        t = step * dt
        thetas.append(utils.compute_theta(t, dt, T, N, G2, G4))

    return cudaq.observe(trotterized_circuit,H,N,G2,G4,steps,dt,thetas).expectation()

N = 6
T = 1.0
depths = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
G2, G4 = get_interactions(N)
H = build_hamiltonian(N, G2, G4)

print("Depth | Trotter Energy | VQE Energy")

for steps in depths:
    E_trot = fixed_trotter_energy(steps)
    E_vqe = vqe_energy(steps)

    print(f"{steps:5d} | {E_trot:14.6f} | {E_vqe:10.6f}")

trotter_vals = []
vqe_vals = []

for steps in depths:
    trotter_vals.append(fixed_trotter_energy(steps))
    vqe_vals.append(vqe_energy(steps))

plt.plot(depths, trotter_vals, "o-", label="Fixed Trotter")
plt.plot(depths, vqe_vals, "s-", label="VQE")
plt.xlabel("Circuit depth (Trotter steps)")
plt.ylabel("Energy ⟨H⟩")
plt.legend()
plt.show()