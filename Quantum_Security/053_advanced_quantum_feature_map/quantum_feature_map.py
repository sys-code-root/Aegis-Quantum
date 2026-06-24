from qiskit.circuit.library import ZZFeatureMap
import numpy as np

class QuantumFeatureMap:
    def __init__(self, feature_dimension: int = 2, reps: int = 2):
        self.feature_dimension = feature_dimension
        self.reps = reps
        self.f_map = ZZFeatureMap(
            feature_dimension=feature_dimension, 
            reps=reps, 
            entanglement='linear'
        )

    def encode_data(self, classical_data: list):
        return self.f_map.assign_parameters(classical_data)

if __name__ == "__main__":
    print("[*] Initializing Advanced ZZFeatureMap Engine (Qiskit 1.x compliant)...")

    q_map = QuantumFeatureMap(feature_dimension=2, reps=2)
    sample_metrics = [0.5, 1.2]
    encoded_circuit = q_map.encode_data(sample_metrics)

    print(f"[+] Classical Input Vector: {sample_metrics}")
    print(f"[+] Symbolic Target Parameters: {q_map.f_map.parameters}")

    print("\n[+] Quantum Feature Map Architecture:")
    print(encoded_circuit.draw(output='text'))
    print("\n[!] Note: RZZ gates represent the calculated correlations between data points.")
