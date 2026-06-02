import time
from qiskit import QuantumCircuit
from qiskit_aer import Aer

class QuantumBenchmark:
    """
    Stress-tests classical hardware memory and processing limits by 
    simulating a 30-qubit GHZ state (Greenberger-Horne-Zeilinger).
    """
    def __init__(self, n_qubits: int = 30):
        self.n_qubits = n_qubits
        self.backend = Aer.get_backend('qasm_simulator')

    def run_benchmark(self):
        """Builds and executes the GHZ entanglement circuit."""
        print(f"[*] Initializing {self.n_qubits}-qubit entanglement circuit...")

        qc = QuantumCircuit(self.n_qubits)

        # Build GHZ state: Hadamard on 0, then cascade CNOTs for maximum entanglement
        qc.h(0)
        for i in range(self.n_qubits - 1):
            qc.cx(i, i + 1)

        qc.measure_all()

        print(f"[*] Launching simulation (Warning: Memory intensity may reach ~16GB RAM)...")
        start_time = time.time()

        # Execute simulation
        job = self.backend.run(qc, shots=100)
        result = job.result()
        counts = result.get_counts()

        end_time = time.time()

        print(f"[+] Simulation completed in: {end_time - start_time:.2f}s")
        print(f"[!] Sample result set: {list(counts.items())[:2]}")

if __name__ == "__main__":
    try:
        benchmark = QuantumBenchmark(30)
        benchmark.run_benchmark()
    except MemoryError:
        print("[!] CRITICAL: Insufficient RAM to complete 30-qubit state space simulation.")
    except Exception as e:
        print(f"[!] Execution exception: {e}")
