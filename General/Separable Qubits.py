# Import QuantumCircuit to build quantum circuits
from qiskit import QuantumCircuit

# Import Aer simulator for statevector simulation
from qiskit_aer import Aer

# Import Statevector to explicitly access the wavefunction
from qiskit.quantum_info import Statevector


# Create a quantum circuit with 3 qubits
# (no classical bits needed since we are not measuring)
qc = QuantumCircuit(3)

# q0 is left untouched → remains in |0>
# Apply Hadamard gate to q1 to create |+> = (|0> + |1>) / √2
qc.h(1)

# Apply Hadamard gate to q2 to create |+> = (|0> + |1>) / √2
qc.h(2)

# Use the statevector simulator backend
backend = Aer.get_backend("statevector_simulator")

# Run the circuit on the simulator
job = backend.run(qc)

# Get the result of the simulation
result = job.result()

# Extract the full quantum state (wavefunction)
statevector = result.get_statevector(qc)

# Print the statevector (this is equivalent to DumpMachine() in Q#)
print("Quantum Statevector:")
print(statevector)
