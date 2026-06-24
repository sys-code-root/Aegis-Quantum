from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import numpy as np

class E91ProtocolSimulator:
    def __init__(self):
        self.backend = AerSimulator()

    def create_entangled_pair(self) -> QuantumCircuit:
        qc = QuantumCircuit(2, 2)
        qc.h(0)
        qc.cx(0, 1)
        return qc

    def apply_measurement(self, qc: QuantumCircuit, alice_angle: float, bob_angle: float) -> QuantumCircuit:
        qc.ry(alice_angle, 0)
        qc.ry(bob_angle, 1)
        qc.measure([0, 1], [0, 1])
        return qc

    def run_simulation(self, shots: int = 1024) -> dict:
        qc = self.create_entangled_pair()
        qc = self.apply_measurement(qc, 0, np.pi/4)
        transpiled_qc = transpile(qc, self.backend)
        job = self.backend.run(transpiled_qc, shots=shots)
        result = job.result().get_counts()
        print(f"[+] Measurement Distribution Matrix (Counts): {result}")
        return result

if __name__ == "__main__":
    print("[*] TITAN CORE: Initializing E91 Quantum Protocol Deployment...")
    titan_e91 = E91ProtocolSimulator()
    titan_e91.run_simulation()
