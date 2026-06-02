from qiskit.circuit import Parameter
from qiskit import QuantumCircuit

class ParameterizedCircuit:
    """
    Constructs a tunable quantum circuit using Parameter objects,
    serving as an Ansatz for variational quantum algorithms (VQA).
    """
    def __init__(self):
        # Initialize the tunable parameter (theta)
        self.theta = Parameter('θ')
        self.qc = QuantumCircuit(1)
        self._build_circuit()

    def _build_circuit(self):
        """Constructs the circuit structure with the parameterized gate."""
        self.qc.h(0)           # Initialization into superposition
        self.qc.ry(self.theta, 0)  # Parametrized rotation (The optimization dial)

    def get_circuit(self) -> QuantumCircuit:
        return self.qc

    def assign_value(self, value: float) -> QuantumCircuit:
        """Binds a classical numeric value to the parameter for execution."""
        return self.qc.assign_parameters({self.theta: value})

if __name__ == "__main__":
    pqc = ParameterizedCircuit()
    circuit = pqc.get_circuit()

    print("[*] Parameterized Ansatz generated (Qiskit 1.x compliant).")
    print(f"[+] Active parameters: {circuit.parameters}")
    print("\nCircuit Architecture:")
    print(circuit.draw(output='text'))

    # Simulate binding a specific optimization state (theta = pi/4)
    bound_circuit = pqc.assign_value(3.14 / 4)
    print("\n[!] Circuit with θ assigned to π/4:")
    print(bound_circuit.draw(output='text'))
