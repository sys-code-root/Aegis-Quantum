from qiskit import QuantumCircuit
from qiskit_aer import Aer
import random

class QuantumBB84:
    """
    Implements the BB84 Quantum Key Distribution (QKD) protocol.
    Simulates secure cryptographic key exchange using qubit polarization states.
    """
    def __init__(self, num_bits: int):
        self.num_bits = num_bits
        self.backend = Aer.get_backend('qasm_simulator')

    def execute_exchange(self) -> list:
        """
        Executes the quantum pipeline: state preparation, basis transformation, 
        and measurement sifting.
        """
        # Alice generates raw binary payload and random basis strings (0=Z, 1=X)
        alice_bits = [random.randint(0, 1) for _ in range(self.num_bits)]
        alice_bases = [random.randint(0, 1) for _ in range(self.num_bits)] 

        # 1. Quantum State Preparation
        circuits = []
        for i in range(self.num_bits):
            qc = QuantumCircuit(1, 1)
            # Apply Pauli-X (NOT) gate if the bit is 1
            if alice_bits[i] == 1:
                qc.x(0)
            # Apply Hadamard (H) gate if the basis is X (1) to enter superposition
            if alice_bases[i] == 1:
                qc.h(0)
            circuits.append(qc)

        # 2. Quantum Measurement
        bob_bases = [random.randint(0, 1) for _ in range(self.num_bits)]
        bob_results = []

        for i in range(self.num_bits):
            qc = circuits[i]
            # Bob applies H-gate before measurement if his basis is X (1)
            if bob_bases[i] == 1: 
                qc.h(0)

            qc.measure(0, 0)
            # Execute circuit in the quantum simulator
            result_dict = self.backend.run(qc, shots=1).result().get_counts()
            measured_bit = int(list(result_dict.keys())[0])
            bob_results.append(measured_bit)

        # 3. Sifting Stage
        # Key material is only preserved where Alice and Bob chose the same bases
        final_key = []
        for i in range(self.num_bits):
            if alice_bases[i] == bob_bases[i]:
                final_key.append(alice_bits[i])

        return final_key

if __name__ == "__main__":
    print("[!] Initiating Quantum Key Distribution (BB84) Engine...")

    # Configure the exchange with 32 bits for a robust key length
    qkd = QuantumBB84(num_bits=32)
    secret_key = qkd.execute_exchange()

    key_str = ''.join(map(str, secret_key))
    print(f"\n[+] Secure Key Established: {key_str}")
    print(f"[*] Key Length: {len(secret_key)} bits")
