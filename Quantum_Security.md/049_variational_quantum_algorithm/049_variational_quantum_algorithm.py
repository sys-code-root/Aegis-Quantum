from qiskit.circuit import Parameter
from qiskit import QuantumCircuit
from qiskit_aer import Aer
import numpy as np
from scipy.optimize import minimize

class VariationalOptimizer:
    """
    Implements a Variational Quantum Algorithm (VQA) to tune circuit 
    parameters using a classical optimizer (COBYLA) to minimize target costs.
    """
    def __init__(self):
        # The Parameter (theta) acts as the tunable dial for the quantum circuit
        self.theta = Parameter('θ')
        self.qc = QuantumCircuit(1)
        self.qc.ry(self.theta, 0)
        self.qc.measure_all()
        self.backend = Aer.get_backend('qasm_simulator')

    def objective_function(self, theta_value: list) -> float:
        """
        Cost function: Measures the probability of the qubit collapsing to state '0'.
        The goal is to minimize this to reach the target state |1>.
        """
        bound_circuit = self.qc.assign_parameters({self.theta: theta_value[0]})

        counts = self.backend.run(bound_circuit, shots=1024).result().get_counts()

        # Calculate failure rate: Prob(0) is the cost to be minimized
        prob_zero = counts.get('0', 0) / 1024
        return prob_zero

    def optimize(self):
        """Orchestrates the classical optimizer to tune the quantum parameter."""
        initial_theta = [0.0]
        # COBYLA is a derivative-free optimization method suitable for noisy quantum systems
        result = minimize(self.objective_function, initial_theta, method='COBYLA')
        return result

if __name__ == "__main__":
    print("[*] Launching Variational Quantum Optimizer...")

    optimizer = VariationalOptimizer()
    result = optimizer.optimize()

    print(f"\n[+] Optimization Cycle Completed.")
    print(f"[!] Optimal Rotation Angle (θ): {result.x[0]:.4f} radians")
    print(f"[!] Residual Cost (Error): {result.fun:.4f}")
