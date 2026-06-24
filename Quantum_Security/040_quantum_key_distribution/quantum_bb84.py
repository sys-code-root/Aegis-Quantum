import random
    from qiskit import QuantumCircuit, transpile
    from qiskit_aer import AerSimulator

    class QuantumBB84:
        def __init__(self, num_bits: int):
            self.num_bits = num_bits
            self.backend = AerSimulator()

        def execute_exchange(self) -> list:
            alice_bits = [random.randint(0, 1) for _ in range(self.num_bits)]
            alice_bases = [random.randint(0, 1) for _ in range(self.num_bits)] 

            circuits = []
            for i in range(self.num_bits):
                qc = QuantumCircuit(1, 1)
                if alice_bits[i] == 1:
                    qc.x(0)
                if alice_bases[i] == 1:
                    qc.h(0)
                circuits.append(qc)

            bob_bases = [random.randint(0, 1) for _ in range(self.num_bits)]
            bob_results = []

            for i in range(self.num_bits):
                qc = circuits[i]
                if bob_bases[i] == 1: 
                    qc.h(0)

                qc.measure(0, 0)
                compiled_qc = transpile(qc, self.backend)
                result_dict = self.backend.run(compiled_qc, shots=1).result().get_counts()
                measured_bit = int(list(result_dict.keys())[0])
                bob_results.append(measured_bit)

            final_key = []
            for i in range(self.num_bits):
                if alice_bases[i] == bob_bases[i]:
                    final_key.append(alice_bits[i])

            return final_key

    if __name__ == "__main__":
        print("[!] Initiating Quantum Key Distribution (BB84) Engine...")
        qkd = QuantumBB84(num_bits=32)
        secret_key = qkd.execute_exchange()

        key_str = ''.join(map(str, secret_key))
        print(f"\n[+] Secure Key Established: {key_str}")
        print(f"[*] Key Length: {len(secret_key)} bits")
