## Simplified Phase Kickback Example
## Demonstrates how phase information transfers between qubits

from qiskit import QuantumCircuit, execute, BasicAer
import math

# Create a quantum circuit with 3 qubits total
# 2 qubits for the main register (reg1) and 1 qubit for the target (reg2)
qc = QuantumCircuit(3)

# Apply Hadamard gates to the first 2 qubits
# This creates an equal superposition: |00⟩ + |01⟩ + |10⟩ + |11⟩
qc.h(0)  # Put qubit 0 in superposition: |0⟩ + |1⟩
qc.h(1)  # Put qubit 1 in superposition: |0⟩ + |1⟩

# Apply controlled phase rotations
# These add different phases based on the control qubit states
qc.cu1(math.pi/4, 0, 2)  # If qubit 0 is |1⟩, rotate qubit 2 by π/4
qc.cu1(math.pi/2, 1, 2)  # If qubit 1 is |1⟩, rotate qubit 2 by π/2

# Run the circuit on a simulator
backend = BasicAer.get_backend('statevector_simulator')
job = execute(qc, backend)
result = job.result()

# Get and print the final quantum state
outputstate = result.get_statevector(qc, decimals=3)
print(outputstate)

# Display the circuit diagram
qc.draw()