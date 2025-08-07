import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Create a quantum circuit with 1 qubit
def demonstrate_rootnot():
    # Initialize quantum circuit
    qc = QuantumCircuit(1, 1)
    
    # Start with |0⟩ state (default)
    print("Initial state: |0⟩")
    
    # Method 1: Manual ROOTNOT construction using H-Phase(-π/2)-H
    print("\n=== Manual ROOTNOT Construction ===")
    qc_manual = QuantumCircuit(1)
    
    # First ROOTNOT: H - Phase(-90°) - H
    qc_manual.h(0)           # Hadamard
    qc_manual.p(-np.pi/2, 0) # Phase(-90°) = Phase(-π/2)
    qc_manual.h(0)           # Hadamard
    qc_manual.barrier()
    
    # Second ROOTNOT: H - Phase(-90°) - H  
    qc_manual.h(0)           # Hadamard
    qc_manual.p(-np.pi/2, 0) # Phase(-90°) = Phase(-π/2)
    qc_manual.h(0)           # Hadamard
    qc_manual.barrier()
    
    # Measure
    qc_manual.measure_all()
    
    print("Manual circuit:")
    print(qc_manual.draw())
    
    # Method 2: Using built-in SX gate (square root of X, equivalent to ROOTNOT)
    print("\n=== Built-in ROOTNOT (SX gate) ===")
    qc_builtin = QuantumCircuit(1)
    
    # Apply SX gate twice (equivalent to X gate)
    qc_builtin.sx(0)  # First ROOTNOT
    qc_builtin.barrier()
    qc_builtin.sx(0)  # Second ROOTNOT
    qc_builtin.barrier()
    
    # Measure
    qc_builtin.measure_all()
    
    print("Built-in SX circuit:")
    print(qc_builtin.draw())
    
    # Simulate both circuits
    simulator = AerSimulator()
    
    # Run manual construction
    job_manual = simulator.run(qc_manual, shots=1000)
    result_manual = job_manual.result()
    counts_manual = result_manual.get_counts()
    
    # Run built-in version
    job_builtin = simulator.run(qc_builtin, shots=1000)
    result_builtin = job_builtin.result()
    counts_builtin = result_builtin.get_counts()
    
    print(f"\nManual ROOTNOT×2 results: {counts_manual}")
    print(f"Built-in SX×2 results: {counts_builtin}")
    
    # Demonstrate single ROOTNOT effect
    print("\n=== Single ROOTNOT Effect ===")
    qc_single = QuantumCircuit(1)
    qc_single.sx(0)  # Single ROOTNOT
    
    # Get statevector to show the complex amplitudes
    statevector = Statevector.from_instruction(qc_single)
    print(f"After single ROOTNOT: {statevector}")
    print(f"Probabilities: |0⟩: {abs(statevector[0])**2:.3f}, |1⟩: {abs(statevector[1])**2:.3f}")
    
    return qc_manual, qc_builtin

# Additional function to show the mathematical equivalence
def show_mathematical_equivalence():
    print("\n=== Mathematical Analysis ===")
    
    # Define gates as matrices
    H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)  # Hadamard
    P_neg90 = np.array([[1, 0], [0, -1j]])        # Phase(-90°)
    X = np.array([[0, 1], [1, 0]])                # NOT gate
    SX = np.array([[1+1j, 1-1j], [1-1j, 1+1j]]) / 2  # Square root of X
    
    # Manual ROOTNOT construction
    manual_rootnot = H @ P_neg90 @ H
    
    print("Manual ROOTNOT matrix:")
    print(manual_rootnot)
    print("\nBuilt-in SX (ROOTNOT) matrix:")
    print(SX)
    print(f"\nMatrices are equivalent: {np.allclose(manual_rootnot, SX)}")
    
    # Show that ROOTNOT² = X
    rootnot_squared_manual = manual_rootnot @ manual_rootnot
    rootnot_squared_builtin = SX @ SX
    
    print(f"\nManual ROOTNOT² ≈ X: {np.allclose(rootnot_squared_manual, X)}")
    print(f"Built-in SX² ≈ X: {np.allclose(rootnot_squared_builtin, X)}")
    
    # Show effect on |0⟩
    zero_state = np.array([1, 0])
    after_one_rootnot = SX @ zero_state
    after_two_rootnot = SX @ SX @ zero_state
    
    print(f"\n|0⟩ after one ROOTNOT: {after_one_rootnot}")
    print(f"|0⟩ after two ROOTNOT: {after_two_rootnot}")

# Run the demonstration
if __name__ == "__main__":
    # Demonstrate the circuits
    manual_circuit, builtin_circuit = demonstrate_rootnot()
    
    # Show mathematical equivalence
    show_mathematical_equivalence()
    
    print("\n=== Summary ===")
    print("• ROOTNOT is the square root of the NOT gate")
    print("• It can be constructed as: Hadamard → Phase(-90°) → Hadamard")
    print("• In Qiskit, it's implemented as the SX gate")
    print("• Applying ROOTNOT twice gives the same result as a single NOT gate")
    print("• Single ROOTNOT creates a superposition with complex phases")