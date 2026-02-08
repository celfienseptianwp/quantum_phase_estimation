import numpy as np

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
def QuantumPhaseEstimation(quantum_circuit, unitary_matrix, n_control, n_target):
    total_qubit = n_control + n_target

    # Hadamard for control qubit
    for order in range(n_control):
        quantum_circuit.h(order)
    
    # Controlled-U for target qubit
    controlled_U = unitary_matrix.control(1)
    for order in range(n_control):
        for _ in range(2**order):
            quantum_circuit.append(controlled_U, [order, total_qubit - 1])

    # Apply the IQFT
    IQFT(quantum_circuit=quantum_circuit, n_control=n_control)
    quantum_circuit.barrier()


