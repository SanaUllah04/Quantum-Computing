# Import quantum computing library and math functions
from qiskit import QuantumCircuit, QuantumRegister, execute, BasicAer
import math

# Create a quantum register with 2 qubits named 'reg'
reg = QuantumRegister(2, name='reg')

# Create a quantum circuit using the register
qc = QuantumCircuit(reg)

# Set the rotation angle to 90 degrees (pi/2 radians)
theta = math.pi / 2

# Apply Hadamard gate to both qubits (creates superposition)
qc.h(reg)

# Rotate qubit 1 around z-axis by half the angle
qc.rz(theta/2, reg[1])

# Apply CNOT gate with qubit 0 as control and qubit 1 as target
qc.cx(reg[0], reg[1])

# Rotate qubit 1 around z-axis by negative half the angle
qc.rz(-theta/2, reg[1])

# Apply another CNOT gate with same control and target
qc.cx(reg[0], reg[1])

# Rotate qubit 0 around z-axis by negative half the angle
qc.rz(-theta/2, reg[0])

# Add a visual barrier to separate circuit sections
qc.barrier()

# Apply controlled rotation on qubit 1, controlled by qubit 0
qc.crz(theta, reg[0], reg[1])

# Get the statevector simulator backend
backend = BasicAer.get_backend('statevector_simulator')

# Execute the quantum circuit on the simulator
job = execute(qc, backend)

# Get the results from the job
result = job.result()

# Extract the final quantum state vector with 3 decimal places
outputstate = result.get_statevector(qc, decimals=3)

# Print the output state vector
print(outputstate)

# Draw the quantum circuit diagram
qc.draw()
