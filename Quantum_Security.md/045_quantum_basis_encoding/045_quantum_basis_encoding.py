from qiskit import QuantumCircuit
from qiskit_aer import Aer

class QuantumEncoder:
    """
    Maps classical binary data sequences into quantum register states
    using basis encoding primitives.
    """
    def __init__(self, binary_data: str):
        self.data = binary_data
        self.n_qubits = len(binary_data)
        self.qc = QuantumCircuit(self.n_qubits)

    def encode(self) -> QuantumCircuit:
        """
        Encodes binary strings into qubit states.
        Logic: '1' maps to state |1> via Pauli-X (NOT gate).
        """
        for i, bit in enumerate(self.data):
            if bit == '1':
                # Apply X gate to flip the qubit from ground state |0> to |1>
                self.qc.x(i)

        self.qc.measure_all()
        return self.qc

    def run_simulation(self) -> dict:
        """Executes the encoding mapping on a local quantum simulator."""
        circuit = self.encode()
        backend = Aer.get_backend('qasm_simulator')

        # Execution dispatch
        job = backend.run(circuit, shots=1024)
        result = job.result().get_counts()
        return result

if __name__ == "__main__":
    # Example data payload for Hilbert Space mapping
    my_data = "101"
    encoder = QuantumEncoder(my_data)

    print(f"[*] Mapping classical data to quantum register: {my_data}")
    counts = encoder.run_simulation()

    # Note: Qiskit utilizes Little-Endian ordering (qubit 0 is the rightmost bit)
    print(f"[+] Quantum State Output: {counts}")
    print("[!] Data successfully mapped to Hilbert Space.")
