from qiskit.circuit import Parameter
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import numpy as np
from scipy.optimize import minimize

class VariationalOptimizer:
    def __init__(self):
        self.theta = Parameter('θ')
        self.qc = QuantumCircuit(1)
        self.qc.ry(self.theta, 0)
        self.qc.measure_all()
        self.backend = AerSimulator()

    def objective_function(self, theta_value: list) -> float:
        bound_circuit = self.qc.assign_parameters({self.theta: theta_value[0]})
        compiled_qc = transpile(bound_circuit, self.backend)
        counts = self.backend.run(compiled_qc, shots=1024).result().get_counts()
        
        prob_zero = counts.get('0', 0) / 1024
        return prob_zero

    def optimize(self):
        initial_theta = [0.0]
        result = minimize(self.objective_function, initial_theta, method='COBYLA')
        return result

if __name__ == "__main__":
    print("[*] Launching Variational Quantum Optimizer...")

    optimizer = VariationalOptimizer()
    result = optimizer.optimize()

    print(f"\n[+] Optimization Cycle Completed.")
    print(f"[!] Optimal Rotation Angle (θ): {result.x[0]:.4f} radians")
    print(f"[!] Residual Cost (Error): {result.fun:.4f}")
