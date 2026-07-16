import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

class AngleEncoder:
    def __init__(self, features: list):
        self.features = features
        self.n_qubits = len(features)
        self.qc = QuantumCircuit(self.n_qubits)

    def encode(self) -> QuantumCircuit:
        for i, val in enumerate(self.features):
            self.qc.ry(val, i)

        self.qc.measure_all()
        return self.qc

    def run_simulation(self) -> dict:
        circuit = self.encode()
        backend = AerSimulator()
        compiled_qc = transpile(circuit, backend)

        job = backend.run(compiled_qc, shots=1024)
        return job.result().get_counts()

if __name__ == "__main__":
    sensor_features = [np.pi/4, np.pi/2, np.pi] 

    print(f"[*] Encoding classical features: {sensor_features}")
    encoder = AngleEncoder(sensor_features)

    counts = encoder.run_simulation()

    print(f"[+] Quantum State Probabilities: {counts}")
    print("[!] Feature vector mapped successfully to rotation angles.")
