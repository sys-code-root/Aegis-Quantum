from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

class QuantumEncoder:
    def __init__(self, binary_data: str):
        self.data = binary_data
        self.n_qubits = len(binary_data)
        self.qc = QuantumCircuit(self.n_qubits)

    def encode(self) -> QuantumCircuit:
        for i, bit in enumerate(self.data):
            if bit == '1':
                self.qc.x(i)

        self.qc.measure_all()
        return self.qc

    def run_simulation(self) -> dict:
        circuit = self.encode()
        backend = AerSimulator()
        compiled_qc = transpile(circuit, backend)
        
        job = backend.run(compiled_qc, shots=1024)
        result = job.result().get_counts()
        return result

if __name__ == "__main__":
    my_data = "101"
    encoder = QuantumEncoder(my_data)

    print(f"[*] Mapping classical data to quantum register: {my_data}")
    counts = encoder.run_simulation()

    print(f"[+] Quantum State Output: {counts}")
    print("[!] Data successfully mapped to Hilbert Space.")
