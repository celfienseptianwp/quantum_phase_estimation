import numpy as np
from math import log2
from qiskit.circuit.library import UnitaryGate

# ===========================
# Quantum Fourier Transform
# ===========================
def QFT(quantum_circuit, n_control):
    # Core iteration of QFT
    for outer_order, outer in enumerate(range(n_control - 1, 0, -1)):
        quantum_circuit.h(outer)
        for inner_order, inner in enumerate(reversed(range(outer_order + 1))):
            quantum_circuit.cp(np.pi / 2**(inner + 1), outer - 1, outer + inner_order)

    # Last Hadamard in 0 qubit    
    quantum_circuit.h(0)
    quantum_circuit.barrier()

    # Change the order of qubit
    for order in range(n_control // 2):
        quantum_circuit.swap(order, n_control - 1 - order)

#====================================
# Inverse Quantum Fourier Transform
#====================================
def IQFT(quantum_circuit, n_control):
    quantum_circuit.barrier()

    # Change the order of qubit
    for order in range(n_control // 2):
        quantum_circuit.swap(order, n_control - 1 - order)

    # First Hadamard in 0 qubit
    quantum_circuit.barrier()
    quantum_circuit.h(0)

    # Core iteration of IQFT
    for outer_order, outer in enumerate(reversed(range(n_control - 1))):
        for inner_order in range(outer + 1):
            quantum_circuit.cp(np.pi / 2**(inner_order + 1), outer_order, n_control - 1 - inner_order)
        quantum_circuit.h(outer_order + 1)

#=================================
# Quantum Phase Estimation (QPE)
#=================================
def QuantumPhaseEstimation(quantum_circuit, unitary_matrix, n_control):
    quantum_circuit.barrier()

    # Determine number of target qubit
    if isinstance(unitary_matrix, UnitaryGate):
        dim = unitary_matrix.num_qubits
        n_target = dim
        U_gate = unitary_matrix
    else:
        N = unitary_matrix.shape[0]
        n_target = int(log2(N))
        if 2**n_target != N:
            raise ValueError("Ukuran operator uniter harus 2^n × 2^n")
        U_gate = UnitaryGate(unitary_matrix)

    total_qubit = n_control + n_target

    # Hadamard for control qubit
    for q in range(n_control):
        quantum_circuit.h(q)

    # Controlled-U^(2^k)
    target_qubits = list(range(n_control, total_qubit))

    for k in range(n_control):
        controlled_U = U_gate.power(2**k).control(1)
        quantum_circuit.append(
            controlled_U,
            [k] + target_qubits
        )

    # Inverse QFT
    IQFT(quantum_circuit=quantum_circuit, n_control=n_control)
    quantum_circuit.barrier()


