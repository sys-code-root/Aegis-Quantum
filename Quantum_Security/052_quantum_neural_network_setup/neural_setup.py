from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from qiskit_machine_learning.neural_networks import EstimatorQNN

class QuantumNeuralNetworkSetup:
    def __init__(self, n_inputs: int = 2, n_weights: int = 2):
        self.n_inputs = n_inputs
        self.n_weights = n_weights
        self.inputs = ParameterVector('input', n_inputs)
        self.weights = ParameterVector('weight', n_weights)
        self.qc = self._build_circuit()

    def _build_circuit(self) -> QuantumCircuit:
        qc = QuantumCircuit(2)

        qc.ry(self.inputs[0], 0)
        qc.ry(self.inputs[1], 1)

        qc.rx(self.weights[0], 0)
        qc.rx(self.weights[1], 1)
        qc.cx(0, 1)

        return qc

    def get_qnn(self) -> EstimatorQNN:
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
