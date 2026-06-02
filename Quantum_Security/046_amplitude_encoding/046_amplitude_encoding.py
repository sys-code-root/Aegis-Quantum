import numpy as np
from qiskit import QuantumCircuit

class QuantumCompressor:
    """
    Implements Amplitude Encoding to compress classical data vectors into 
    quantum states, mapping 2^n data points into n qubits.
    """
    def __init__(self, data_vector: list):
        self.data = np.array(data_vector)
        self.n_qubits = int(np.log2(len(data_vector)))

    def encode(self) -> QuantumCircuit:
        """
        Normalizes input data and initializes a quantum circuit 
        to store amplitudes in the quantum register.
        """
        # Data Normalization: The L2 norm of the state vector must equal 1
        norm = np.linalg.norm(self.data)
        normalized_data = self.data / norm

        # Initialize the circuit with the specified number of qubits
        qc = QuantumCircuit(self.n_qubits)

        # 'initialize' computes the gate operations needed to map data to amplitudes
        qc.initialize(normalized_data, range(self.n_qubits))

        return qc

if __name__ == "__main__":
    # Input vector: 4 data points compressed into 2 qubits (2^2 = 4)
    raw_data = [1.0, 2.0, 3.0, 4.0]

    print(f"[*] Compressing classical vector: {raw_data}")
    compressor = QuantumCompressor(raw_data)
    circuit = compressor.encode()

    print("[+] Quantum State Amplitude Mapping complete:")
    print(circuit.draw(output='text'))
    print("[!] Data density optimized via Hilbert Space storage.")
