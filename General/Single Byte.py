# Programming Quantum Computers - Random Byte Generator
# Converted from O'Reilly QC JavaScript to Python using Qiskit
# This sample generates a single random byte using eight unentangled qubits

try:
    from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
    from qiskit_aer import AerSimulator
    QISKIT_AVAILABLE = True
except ImportError as e:
    print("Qiskit is not properly installed. Please install it using:")
    print("pip install qiskit qiskit-aer")
    print("\nFor a complete installation:")
    print("pip install 'qiskit[all]'")
    print(f"\nError: {e}")
    QISKIT_AVAILABLE = False

try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

def generate_random_byte():
    """
    Generate a random byte (0-255) using 8 quantum bits in superposition.
    Each qubit has equal probability of being 0 or 1 when measured.
    """
    
    # Create quantum circuit with 8 qubits and 8 classical bits
    qreg = QuantumRegister(8, 'q')
    creg = ClassicalRegister(8, 'c')
    qc = QuantumCircuit(qreg, creg)
    
    # Initialize qubits to |0⟩ state (this is automatic, but explicit for clarity)
    # qc.reset() is equivalent to qc.initialize([1, 0], qubit) for each qubit
    
    # Apply Hadamard gates to all qubits to create superposition
    # This puts each qubit in equal superposition of |0⟩ and |1⟩
    for i in range(8):
        qc.h(qreg[i])
    
    # Measure all qubits
    qc.measure(qreg, creg)
    
    return qc

def run_quantum_random():
    """
    Execute the quantum circuit and return the random byte value.
    """
    # Create the circuit
    circuit = generate_random_byte()
    
    # Use Aer simulator
    simulator = AerSimulator()
    
    # Transpile circuit for simulator
    compiled_circuit = transpile(circuit, simulator)
    
    # Execute the circuit once to get a single random result
    job = simulator.run(compiled_circuit, shots=1)
    result = job.result()
    counts = result.get_counts(compiled_circuit)
    
    # Get the measurement result (binary string)
    binary_result = list(counts.keys())[0]
    
    # Convert binary string to integer (byte value 0-255)
    byte_value = int(binary_result, 2)
    
    return byte_value, binary_result

def demonstrate_randomness(num_samples=100):
    """
    Generate multiple random bytes to demonstrate the randomness.
    """
    print("Generating random bytes using quantum superposition...\n")
    
    results = []
    for i in range(min(10, num_samples)):  # Show first 10 results
        byte_val, binary = run_quantum_random()
        results.append(byte_val)
        print(f"Sample {i+1:2d}: Binary: {binary} → Decimal: {byte_val:3d}")
    
    if num_samples > 10:
        # Generate remaining samples without printing each one
        for i in range(10, num_samples):
            byte_val, _ = run_quantum_random()
            results.append(byte_val)
    
    # Show statistics
    print(f"\nStatistics for {num_samples} samples:")
    print(f"Min: {min(results)}")
    print(f"Max: {max(results)}")
    print(f"Average: {sum(results)/len(results):.2f}")
    print(f"Expected average for uniform distribution: 127.5")
    
    return results

if __name__ == "__main__":
    if not QISKIT_AVAILABLE:
        exit(1)
    
    # Single random byte generation
    print("=== Quantum Random Byte Generator ===")
    byte_value, binary_string = run_quantum_random()
    print(f"Generated random byte:")
    print(f"Binary:  {binary_string}")
    print(f"Decimal: {byte_value}")
    print(f"Hex:     0x{byte_value:02X}")
    
    print("\n" + "="*50)
    
    # Demonstrate with multiple samples
    sample_results = demonstrate_randomness(100)
    
    # Optional: Create a simple histogram (requires matplotlib)
    if MATPLOTLIB_AVAILABLE:
        plt.figure(figsize=(10, 6))
        plt.hist(sample_results, bins=16, alpha=0.7, edgecolor='black')
        plt.xlabel('Byte Value')
        plt.ylabel('Frequency')
        plt.title('Distribution of Quantum Random Bytes (100 samples)')
        plt.grid(True, alpha=0.3)
        plt.show()
    else:
        print("\nNote: Install matplotlib to see histogram visualization:")