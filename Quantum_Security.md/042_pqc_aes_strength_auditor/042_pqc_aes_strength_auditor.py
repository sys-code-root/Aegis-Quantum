import math

class PQCAnalyzer:
    """
    Audits the cryptographic strength of symmetric keys against quantum 
    brute-force attacks using Grover's Algorithm complexity metrics.
    """
    def __init__(self):
        # 10^18 represents 1 Exaflop (current hypothetical peak processing power)
        self.ops_per_sec = 10**18

    def calculate_resistance(self, key_bits: int) -> float:
        """
        Compares classical brute-force effort against quantum-accelerated 
        Grover's Algorithm effort (complexity reduction to square root).
        """
        # Classical: Full keyspace exploration (2^N)
        # Quantum: Grover's search optimization (sqrt(2^N) = 2^(N/2))
        classical_eff = 2**key_bits
        quantum_eff = 2**(key_bits / 2) 

        print(f"\n[+] Analysis for {key_bits}-bit Key:")
        print(f"    Classical Security: 2^{key_bits} operations")
        print(f"    Quantum Security (Grover): 2^{int(key_bits/2)} operations")

        # Time estimation in years based on theoretical exaflop processing speed
        seconds_in_year = 3600 * 24 * 365
        years_to_crack = (quantum_eff / self.ops_per_sec) / seconds_in_year
        return years_to_crack

if __name__ == "__main__":
    analyzer = PQCAnalyzer()
    print("--- POST-QUANTUM RESISTANCE AUDIT ---")

    for bits in [128, 256]:
        time_years = analyzer.calculate_resistance(bits)

        # Standard safety threshold: 100 years of computational effort
        if time_years < 100:
            print(f"    [VULNERABLE] Crackable in approx {time_years:.2e} years!")
        else:
            print(f"    [SAFE] Security threshold exceeded: {time_years:.2e} years to crack.")
