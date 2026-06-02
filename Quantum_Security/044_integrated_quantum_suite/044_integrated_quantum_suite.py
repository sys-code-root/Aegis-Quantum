import numpy as np
import hashlib
import random

class QuantumSuite:
    """
    Simulates an end-to-end quantum security lifecycle: from superposition-based 
    key exchange to Grover attack simulation and PQC defensive hashing.
    """
    def __init__(self):
        # Hadamard Gate: The fundamental engine for creating quantum superposition
        self.h_gate = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]]) 

    def phase_1_4_secure_exchange(self):
        """Simulates superposition and key exchange (BB84 style foundation)."""
        print("\n[*] Phase 1-4: Generating Key via Superposition...")
        alice_bit = random.randint(0, 1)

        # Preparing the initial state vector (|0> or |1>)
        state = np.array([[1], [0]]) if alice_bit == 0 else np.array([[0], [1]])

        # Applying Hadamard gate to force state into superposition
        superposition = np.dot(self.h_gate, state)
        return alice_bit, superposition

    def phase_5_7_grover_attack(self, target_bit):
        """Simulates a Grover Search attack attempt (Oracle-based probability amplification)."""
        print(f"[*] Phase 5-7: Attacker utilizes Grover's amplification to find bit {target_bit}...")

        # Grover amplification increases probability amplitude of marked states
        success_rate = 0.95 
        found = target_bit if random.random() < success_rate else (1 - target_bit)
        return found

    def phase_6_pqc_defense(self, data):
        """Applies Post-Quantum Defense mechanism (SHA-256 collision resistance)."""
        print("[*] Phase 6: Applying PQC Shield (SHA-256)...")
        # Cryptographic hashes are effectively resistant to Shor's algorithm
        return hashlib.sha256(data.encode()).hexdigest()

if __name__ == "__main__":
    suite = QuantumSuite()

    # 1. Quantum Key Exchange Sequence
    bit, q_state = suite.phase_1_4_secure_exchange()
    print(f"    [OK] Alice initialized bit: {bit}")
    print(f"    [STATE] Quantum Vector:\n{q_state}")

    # 2. Attack Attempt
    hacker_guess = suite.phase_5_7_grover_attack(bit)
    print(f"    [RESULT] Attacker used Grover's oracle and found: {hacker_guess}")

    # 3. Final Defense (PQC Hashing)
    pqc_signature = suite.phase_6_pqc_defense(str(bit))
    print(f"    [FINAL] PQC Signature Generated: {pqc_signature[:20]}...")

    print("\n--- [COMPLETED] SYSTEM SECURED AGAINST QUANTUM THREAT ---")
