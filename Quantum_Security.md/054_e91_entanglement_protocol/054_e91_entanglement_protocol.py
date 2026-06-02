from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
import numpy as np

class E91ProtocolSimulator:
    """
    Simulates the E91 Quantum Key Distribution protocol using entangled Bell pairs
    and dynamic basis measurement configurations.
    """
    def __init__(self):
        # Qiskit 1.x compliant Aer simulator backend resolution
        self.backend = Aer.get_backend('qasm_simulator')

    def create_entangled_pair(self) -> QuantumCircuit:
        """Generates a maximally entangled Bell state (|Phi+>) between Alice and Bob."""
        qc = QuantumCircuit(2, 2)
        qc.h(0)           # Puts qubit 0 into uniform superposition
        qc.cx(0, 1)       # Entangles qubit 1 with qubit 0 via CNOT
        return qc

    def apply_measurement(self, qc: QuantumCircuit, alice_angle: float, bob_angle: float) -> QuantumCircuit:
        """Applies directional base rotation transformations prior to register measurement."""
        # Alice rotates her observer interface (Qubit 0)
        qc.ry(alice_angle, 0)
        # Bob rotates his observer interface (Qubit 1)
        qc.ry(bob_angle, 1)

        qc.measure([0, 1], [0, 1])
        return qc

    def run_simulation(self, shots: int = 1024) -> dict:
        """Executes full quantum compilation pipeline: transpile followed by backend run."""
        qc = self.create_entangled_pair()

        # Define measurement orientation (e.g., standard Z-basis vs Pi/4 offset)
        qc = self.apply_measurement(qc, 0, np.pi/4)

        # Transpilation layer optimization tailored dynamically for the specific backend target
        transpiled_qc = transpile(qc, self.backend)

        # Dispatch job execution
        job = self.backend.run(transpiled_qc, shots=shots)
        result = job.result().get_counts()

        print(f"[+] Measurement Distribution Matrix (Counts): {result}")
        return result

if __name__ == "__main__":
    print("[*] TITAN CORE: Initializing E91 Quantum Protocol Deployment...")
    titan_e91 = E91ProtocolSimulator()
    titan_e91.run_simulation()
