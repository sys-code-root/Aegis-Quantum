from qiskit import QuantumCircuit
from qiskit_aer import Aer
import numpy as np

class AngleEncoder:
    """
    Maps classical feature vectors into quantum states using rotation angle 
    encoding (RY gates), a prerequisite for Quantum Neural Networks (QNNs).
    """
    def __init__(self, features: list):
        self.features = features
        self.n_qubits = len(features)
        self.qc = QuantumCircuit(self.n_qubits)

    def encode(self) -> QuantumCircuit:
        """
        Encodes data by rotating each qubit along the Y-axis 
        proportionally to the feature value.
        """
        for i, val in enumerate(self.features):
            # RY rotation encodes continuous data as qubit state probability
            self.qc.ry(val, i)

        self.qc.measure_all()
        return self.qc

    def run_simulation(self) -> dict:
        """Executes the encoding circuit on the aer qasm_simulator."""
        circuit = self.encode()
        backend = Aer.get_backend('qasm_simulator')

        job = backend.run(circuit, shots=1024)
        return job.result().get_counts()

if __name__ == "__main__":
    # Simulated sensor inputs: [Humidity, Temperature, Pressure] normalized in radians
    sensor_features = [np.pi/4, np.pi/2, np.pi] 

    print(f"[*] Encoding classical features: {sensor_features}")
    encoder = AngleEncoder(sensor_features)

    counts = encoder.run_simulation()

    print(f"[+] Quantum State Probabilities: {counts}")
    print("[!] Feature vector mapped successfully to rotation angles.")
