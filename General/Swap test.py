# Quantum Swap Test - measures similarity between two quantum states
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, BasicAer

# Create three single-qubit registers
input1 = QuantumRegister(1, name='input1')  # First input qubit
input2 = QuantumRegister(1, name='input2')  # Second input qubit
output = QuantumRegister(1, name='output')  # Ancilla qubit for test result

# Create classical register to store measurement result
output_c = ClassicalRegister(1, name='outputc')

# Initialize quantum circuit with all registers
qc = QuantumCircuit(input1, input2, output, output_c)

# Apply Hadamard gate to output qubit (creates superposition)
qc.h(output)

# Apply controlled-SWAP: swaps input1 and input2 if output is |1⟩
qc.cswap(output, input1, input2)

# Apply Hadamard gate again to output qubit (interference step)
qc.h(output)

# Apply X gate to flip the result (optional inversion)
qc.x(output)

# Measure the output qubit into classical register
qc.measure(output, output_c)

# Select the statevector simulator backend
backend = BasicAer.get_backend('statevector_simulator')

# Execute the quantum circuit on the simulator
job = execute(qc, backend)

# Get the results from the execution
result = job.result()

# Extract measurement counts from results
counts = result.get_counts(qc)
print('counts:', counts)

# Get the final statevector (quantum state amplitudes)
outputstate = result.get_statevector(qc, decimals=3)
print(outputstate)

# Draw the circuit diagram
qc.draw()