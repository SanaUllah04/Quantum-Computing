# Import required Qiskit classes
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import Aer, execute

# -----------------------------
# Create quantum registers
# -----------------------------

# One qubit named 'a'
qubit_a = QuantumRegister(1, name='a')

# One qubit named 'b'
qubit_b = QuantumRegister(1, name='b')

# Classical bits to store measurement results
classical_a = ClassicalRegister(1, name='ca')
classical_b = ClassicalRegister(1, name='cb')

# Create the quantum circuit
qc = QuantumCircuit(qubit_a, qubit_b, classical_a, classical_b)

# -----------------------------
# Quantum operations
# -----------------------------

# Put qubit 'a' into superposition
qc.h(qubit_a)

# Entangle qubit 'a' with qubit 'b'
qc.cx(qubit_a, qubit_b)

# Measure both qubits
qc.measure(qubit_a, classical_a)
qc.measure(qubit_b, classical_b)

# -----------------------------
# Run the circuit
# -----------------------------

# Use simulator that supports measurements
backend = Aer.get_backend('qasm_simulator')

# Execute the circuit
job = execute(qc, backend, shots=1024)
result = job.result()

# Get measurement results
counts = result.get_counts(qc)
print("Measurement results:", counts)

# Draw the circuit
qc.draw()
