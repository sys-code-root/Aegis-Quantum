from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from qiskit_machine_learning.neural_networks import EstimatorQNN

class QuantumNeuralNetworkSetup:
    """
    Initializes a formal Quantum Neural Network (QNN) using the Qiskit 
    Estimator primitive for scalable quantum machine learning.
    """
    def __init__(self, n_inputs: int = 2, n_weights: int = 2):
        self.n_inputs = n_inputs
        self.n_weights = n_weights

        # ParameterVectors act as scalable arrays for inputs and trainable weights
        self.inputs = ParameterVector('input', n_inputs)
        self.weights = ParameterVector('weight', n_weights)
        self.qc = self._build_circuit()

    def _build_circuit(self) -> QuantumCircuit:
        """Constructs the variational quantum circuit layers."""
        qc = QuantumCircuit(2)

        # 1. Feature Map Layer: Encoding input data into quantum states
        qc.ry(self.inputs[0], 0)
        qc.ry(self.inputs[1], 1)

        # 2. Ansatz Layer: Learnable rotation weights and entanglement
        qc.rx(self.weights[0], 0)
        qc.rx(self.weights[1], 1)
        qc.cx(0, 1)  # Entangling gate to capture feature correlations

        return qc

    def get_qnn(self) -> EstimatorQNN:
        """Wraps the circuit into a trainabale QNN object."""
        return EstimatorQNN(
            circuit=self.qc,
            input_params=self.inputs,
            weight_params=self.weights
        )

if __name__ == "__main__":
    qnn_builder = QuantumNeuralNetworkSetup()
    qnn = qnn_builder.get_qnn()

    print("[*] Qiskit Machine Learning Network Initialized.")
    print(f"[+] Input parameters: {len(qnn.input_params)}")
    print(f"[+] Trainable weight parameters: {len(qnn.weight_params)}")
    print("\n[+] Circuit Architecture:")
    print(qnn_builder.qc.draw(output='text'))
