from qiskit.circuit import Parameter
from qiskit import QuantumCircuit

class ParameterizedCircuit:
    def __init__(self):
        self.theta = Parameter('θ')
        self.qc = QuantumCircuit(1)
        self._build_circuit()

    def _build_circuit(self):
        self.qc.h(0)
        self.qc.ry(self.theta, 0)

    def get_circuit(self) -> QuantumCircuit:
        return self.qc

    def assign_value(self, value: float) -> QuantumCircuit:
        return self.qc.assign_parameters({self.theta: value})

if __name__ == "__main__":
    pqc = ParameterizedCircuit()
    circuit = pqc.get_circuit()

    print("[*] Parameterized Ansatz generated (Qiskit 1.x compliant).")
    print(f"[+] Active parameters: {circuit.parameters}")
    print("\nCircuit Architecture:")
    print(circuit.draw(output='text'))

    bound_circuit = pqc.assign_value(3.14 / 4)
    print("\n[!] Circuit with θ assigned to π/4:")
    print(bound_circuit.draw(output='text'))
