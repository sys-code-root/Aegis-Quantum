from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

class GroverSearch:
    def __init__(self):
        self.qc = QuantumCircuit(2, 2)
        print("[!] Grover's Search Engine Initialized (2-Qubits).")

    def run(self):
        print("[*] Phase 1: Creating Uniform Superposition...")
        self.qc.h([0, 1])
        self.qc.barrier()

        print("[*] Phase 2: Applying Oracle to mark state |11>...")
        self.qc.cz(0, 1)
        self.qc.barrier()

        print("[*] Phase 3: Amplitude Amplification (Diffusion)...")
        self.qc.h([0, 1])
        self.qc.z([0, 1])
        self.qc.cz(0, 1)
        self.qc.h([0, 1])
        self.qc.barrier()

        print("[*] Measuring state probabilities...")
        self.qc.measure([0, 1], [0, 1])

        backend = AerSimulator()
        compiled_qc = transpile(self.qc, backend)
        result = backend.run(compiled_qc, shots=1024).result()
        counts = result.get_counts()

        print(f"\n[+] Final Measurement Probabilities: {counts}")
        print("[!] The marked state '11' achieves peak probability.")

if __name__ == "__main__":
    grover = GroverSearch()
    grover.run()
