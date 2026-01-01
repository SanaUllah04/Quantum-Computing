## Programming Quantum Computers
##   by Eric Johnston, Nic Harrigan and Mercedes Gimeno-Segovia
##   O'Reilly Media
##
## More samples like this can be found at http://oreilly-qc.github.io

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
import math

## Uncomment the next line to see diagrams when running in a notebook
#%matplotlib inline

## Example 2-4: Quantum Spy Hunter
## This program demonstrates quantum key distribution (QKD) using the BB84 protocol
## to detect if someone (a spy) is eavesdropping on quantum communication between Alice and Bob

# ============================================================================
# STEP 1: SET UP QUANTUM AND CLASSICAL REGISTERS
# ============================================================================

# Create quantum registers (qubits) for Alice, the fiber optic channel, and Bob
alice = QuantumRegister(1, name='alice')  # Alice's qubit for preparing quantum states
fiber = QuantumRegister(1, name='fiber')  # The communication channel (fiber optic cable)
bob   = QuantumRegister(1, name='bob')    # Bob's qubit for receiving quantum states

# Create classical registers (regular bits) to store measurement results
alice_had = ClassicalRegister(1, name='ahad')  # Alice's Hadamard basis choice (0 or 1)
alice_val = ClassicalRegister(1, name='aval')  # Alice's bit value to send (0 or 1)
fiber_val = ClassicalRegister(1, name='fval')  # Spy's measurement result (if present)
bob_had   = ClassicalRegister(1, name='bhad')  # Bob's Hadamard basis choice (0 or 1)
bob_val   = ClassicalRegister(1, name='bval')  # Bob's measurement result (0 or 1)

# Create the quantum circuit with all registers
qc = QuantumCircuit(alice, fiber, bob, alice_had, alice_val, fiber_val, bob_had, bob_val)

# ============================================================================
# STEP 2: ALICE GENERATES TWO RANDOM BITS
# ============================================================================

# Generate Alice's random basis choice (Hadamard basis: YES=1 or NO=0)
qc.reset(alice)              # Initialize Alice's qubit to |0⟩
qc.h(alice)                  # Apply Hadamard gate to create superposition (50/50 chance)
qc.measure(alice, alice_had) # Measure to get random bit for basis choice

# Generate Alice's random bit value to send (0 or 1)
qc.reset(alice)              # Reset Alice's qubit to |0⟩ again
qc.h(alice)                  # Apply Hadamard gate for another random bit
qc.measure(alice, alice_val) # Measure to get random bit value

# ============================================================================
# STEP 3: ALICE PREPARES HER QUBIT TO SEND
# ============================================================================

# Prepare the qubit in the state Alice wants to send
qc.reset(alice)  # Start with |0⟩

# If alice_val=1, flip to |1⟩ (X gate)
with qc.if_test((alice_val, 1)):
    qc.x(alice[0])

# If alice_had=1, apply Hadamard (diagonal basis)
with qc.if_test((alice_had, 1)):
    qc.h(alice[0])

# At this point:
# - If alice_had=0 and alice_val=0: qubit is |0⟩ (computational basis)
# - If alice_had=0 and alice_val=1: qubit is |1⟩ (computational basis)
# - If alice_had=1 and alice_val=0: qubit is |+⟩ (Hadamard/diagonal basis)
# - If alice_had=1 and alice_val=1: qubit is |-⟩ (Hadamard/diagonal basis)

# ============================================================================
# STEP 4: SEND THE QUBIT THROUGH THE FIBER
# ============================================================================

qc.swap(alice, fiber)  # Transfer Alice's qubit to the fiber optic channel

# ============================================================================
# STEP 5: SPY INTERCEPTS AND MEASURES (IF PRESENT)
# ============================================================================

spy_is_present = True  # Set to True to simulate a spy, False for no spy

if spy_is_present:
    qc.barrier()  # Visual separator in circuit diagram
    
    spy_had = True  # Spy's basis choice (True = Hadamard basis, False = computational)
    
    # Spy measures the qubit in their chosen basis
    if spy_had:
        qc.h(fiber)  # Apply Hadamard if measuring in diagonal basis
    
    qc.measure(fiber, fiber_val)  # Spy measures the qubit (COLLAPSES the state!)
    
    # Spy tries to restore the qubit to what they measured
    qc.reset(fiber)  # Reset to |0⟩
    
    # Set to measured value
    with qc.if_test((fiber_val, 1)):
        qc.x(fiber[0])
    
    if spy_had:
        qc.h(fiber)  # Apply Hadamard again if they used diagonal basis
    
    # PROBLEM: If spy chose wrong basis (different from Alice), the qubit state is DESTROYED!
    # This creates detectable errors when Bob measures.

qc.barrier()  # Visual separator

# ============================================================================
# STEP 6: BOB GENERATES A RANDOM BASIS CHOICE
# ============================================================================

# Bob randomly chooses which basis to measure in (independent of Alice)
qc.reset(bob)            # Initialize Bob's qubit to |0⟩
qc.h(bob)                # Apply Hadamard for random choice
qc.measure(bob, bob_had) # Measure to get random basis choice (0 or 1)

# ============================================================================
# STEP 7: BOB RECEIVES AND MEASURES THE QUBIT
# ============================================================================

qc.swap(fiber, bob)  # Transfer qubit from fiber to Bob

# If bob_had=1, measure in Hadamard basis
with qc.if_test((bob_had, 1)):
    qc.h(bob[0])

qc.measure(bob, bob_val)  # Measure to get final bit value

# ============================================================================
# STEP 8: EXECUTE THE QUANTUM CIRCUIT
# ============================================================================

# Use a simulator to run the quantum circuit
simulator = AerSimulator()
transpiled_circuit = transpile(qc, simulator)
job = simulator.run(transpiled_circuit, shots=1)
result = job.result()

# ============================================================================
# STEP 9: ANALYZE RESULTS TO DETECT SPY
# ============================================================================

# Alice and Bob compare their bases publicly (safe to reveal)
# If bases match AND values DON'T match, there was interference (spy detected!)

counts = result.get_counts()
print('counts:', counts)

caught = False

# Parse each measurement outcome
for key, val in counts.items():
    # Extract the classical bit values from the measurement string
    # Format is: bval bhad fval aval ahad (reversed order)
    bits = key.split(' ')
    bval = int(bits[0])
    bhad = int(bits[1])
    f = int(bits[2])
    aval = int(bits[3])
    ahad = int(bits[4])
    
    # Check if Alice and Bob used the SAME basis
    if ahad == bhad:
        # If same basis but DIFFERENT values, spy must have interfered!
        if aval != bval:
            print('Caught a spy!')
            caught = True

if not caught:
    print('No spies detected.')

# ============================================================================
# DISPLAY RESULTS
# ============================================================================

# Draw the circuit diagram
print("\nCircuit Diagram:")
print(qc.draw(output='text'))

# ============================================================================
# README DOCUMENTATION
# ============================================================================

"""
QUANTUM SPY HUNTER - BB84 PROTOCOL DEMONSTRATION
================================================

WHAT THIS CODE DOES:
-------------------
This program simulates quantum key distribution (QKD) using the BB84 protocol,
which is a method for two parties (Alice and Bob) to securely share encryption
keys while detecting any eavesdropping attempts.

WHY IT WORKS:
------------
The security is based on a fundamental principle of quantum mechanics:
measuring a quantum state CHANGES it (quantum measurement collapse). If a spy
intercepts and measures the qubit during transmission, they disturb its quantum
state. When Alice and Bob later compare their measurements, this disturbance
creates detectable errors.

HOW IT WORKS - STEP BY STEP:
---------------------------

1. ALICE PREPARES A QUBIT:
   - Alice randomly chooses a basis (computational or Hadamard/diagonal)
   - Alice randomly chooses a bit value (0 or 1)
   - She prepares her qubit in the corresponding quantum state:
     * |0⟩ or |1⟩ (computational basis)
     * |+⟩ or |-⟩ (Hadamard basis)

2. TRANSMISSION:
   - The qubit is sent through a quantum channel (fiber optic cable)

3. SPY INTERCEPTION (IF PRESENT):
   - The spy intercepts the qubit
   - The spy randomly guesses a measurement basis
   - The spy measures the qubit (this COLLAPSES the quantum state!)
   - The spy tries to recreate the qubit and send it forward
   - Problem: If the spy guessed the WRONG basis (50% chance), the qubit
     state is permanently altered in a detectable way

4. BOB RECEIVES THE QUBIT:
   - Bob randomly chooses his own measurement basis (independent of Alice)
   - Bob measures the qubit in his chosen basis

5. PUBLIC COMPARISON (AFTER TRANSMISSION):
   - Alice publicly announces her basis choices (safe to reveal)
   - Bob publicly announces his basis choices (safe to reveal)
   - They keep only the cases where they BOTH used the same basis
   - They compare a sample of these matching cases:
     * If NO spy: their values should ALWAYS match
     * If YES spy: about 25% of values will MISMATCH (this is the error rate)

THE MATHEMATICAL APPROACH:
-------------------------
When Alice and Bob use the SAME basis and there's NO interference:
- Their measurement results will be 100% correlated (identical values)

When a spy measures in the WRONG basis:
- The quantum state collapses to a state that's 50/50 between the two states
  in Alice's original basis
- This creates a 50% error rate in that particular transmission
- Across all transmissions, about 25% will show errors (50% wrong basis × 50% error)

SECURITY GUARANTEE:
------------------
If Alice and Bob detect an error rate above statistical noise, they know
someone intercepted the quantum channel. They can then:
1. Abort the key exchange
2. Use a different channel
3. Not use the compromised bits for encryption

This makes quantum key distribution provably secure - any eavesdropping
attempt is mathematically guaranteed to leave detectable traces.

REAL-WORLD APPLICATIONS:
-----------------------
- Secure government communications
- Banking and financial transactions
- Protecting classified information
- Future quantum-safe cryptography networks

KEY QUANTUM CONCEPTS DEMONSTRATED:
---------------------------------
1. Superposition: Qubits can be in multiple states simultaneously
2. Measurement collapse: Measuring a qubit forces it into a definite state
3. Basis choice: The same qubit can be measured in different ways
4. No-cloning theorem: You can't perfectly copy an unknown quantum state
5. Quantum uncertainty: You can't measure all properties simultaneously

PARAMETERS YOU CAN MODIFY:
-------------------------
- spy_is_present: Set to False to see perfect correlation without a spy
- spy_had: Change the spy's basis choice strategy
- Run multiple times to see statistical behavior

EXPECTED OUTPUT:
---------------
- With spy_is_present=True: You'll see "Caught a spy!" messages when basis
  choices match but values differ
- With spy_is_present=False: You'll see "No spies detected" and perfect
  correlation when bases match

This is a foundational demonstration of quantum cryptography and shows why
quantum mechanics provides security guarantees impossible with classical physics.

INSTALLATION REQUIREMENTS:
-------------------------
To run this code, you need to install qiskit-aer:
pip install qiskit-aer

This provides the quantum circuit simulator needed for the program.
"""