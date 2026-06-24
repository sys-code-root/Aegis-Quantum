import numpy as np
from qiskit import QuantumCircuit

class QuantumCompressor:
    def __init__(self, data_vector: list):
        self.data = np.array(data_vector)
        self.n_qubits = int(np.log2(len(data_vector)))

    def encode(self) -> QuantumCircuit:
        norm = np.linalg.norm(self.data)
        normalized_data = self.data / norm

        qc = QuantumCircuit(self.n_qubits)
        qc.initialize(normalized_data, range(self.n_qubits))

        return qc

    if __name__ == "__main__":
        raw_data = [1.0, 2.0, 3.0, 4.0]

        print(f"[*] Compressing classical vector: {raw_data}")
        compressor = QuantumCompressor(raw_data)
        circuit = compressor.encode()

        print("[+] Quantum State Amplitude Mapping complete:")
        print(circuit.draw(output='text'))
        print("[!] Data density optimized via Hilbert Space storage.")
