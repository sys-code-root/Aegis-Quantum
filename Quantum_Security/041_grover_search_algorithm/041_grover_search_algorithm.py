from qiskit import QuantumCircuit
from qiskit_aer import Aer

class GroverSearch:
    """
    Implements Grover's Algorithm to search for a marked state |11> 
    within a 2-qubit system using amplitude amplification.
    """
    def __init__(self):
        self.qc = QuantumCircuit(2, 2)
        print("[!] Grover's Search Engine Initialized (2-Qubits).")

    def run(self):
        """Executes the three core phases of Grover's Algorithm."""

        # 1. Initialization Phase: Creating Uniform Superposition
        print("[*] Phase 1: Creating Uniform Superposition...")
        self.qc.h([0, 1])
        self.qc.barrier()

        # 2. Oracle Phase: Marking the target state |11>
        # The CZ gate inverts the phase of the |11> amplitude
        print("[*] Phase 2: Applying Oracle to mark state |11>...")
        self.qc.cz(0, 1)
        self.qc.barrier()

        # 3. Diffusion Operator Phase: Amplitude Amplification
        print("[*] Phase 3: Amplitude Amplification (Diffusion)...")
        self.qc.h([0, 1])
        self.qc.z([0, 1])
        self.qc.cz(0, 1)
        self.qc.h([0, 1])
        self.qc.barrier()

        # 4. Measurement Phase
        print("[*] Measuring state probabilities...")
        self.qc.measure([0, 1], [0, 1])

        # Execution on local Aer simulator
        backend = Aer.get_backend('qasm_simulator')
        result = backend.run(self.qc, shots=1024).result()
        counts = result.get_counts()

        print(f"\n[+] Final Measurement Probabilities: {counts}")
        print("[!] The marked state '11' achieves peak probability.")

if __name__ == "__main__":
    grover = GroverSearch()
    grover.run()
