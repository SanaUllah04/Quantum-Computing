# Import necessary Qiskit components
from qiskit import QuantumCircuit
from qiskit.providers.basic_provider import BasicSimulator

# Create a quantum circuit with 1 qubit and 1 classical bit
qc = QuantumCircuit(1, 1)

# Apply Hadamard gate to put the qubit in superposition
qc.h(0)

# Measure the qubit and store result in the classical bit
qc.measure(0, 0)

# Use the basic simulator
simulator = BasicSimulator()
job = simulator.run(qc, shots=1)
result = job.result()

# Extract the measured bit
counts = result.get_counts()
random_bit = int(list(counts.keys())[0])

# Print the result
print(f"Random bit: {random_bit}")