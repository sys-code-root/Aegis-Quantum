# PQC AES Strength Auditor (Project 042)

A computational utility that audits symmetric key security by modeling
the impact of quantum speedups (Grover\'s Algorithm) on key entropy.

## Technical Explanation

-   **Complexity Modeling:** Demonstrates the degradation of security
    from \$2\^N\$ to \$2\^{N/2}\$ when applying Grover\'s algorithm to
    unstructured search spaces (like AES key spaces).
-   **Exaflop Thresholding:** Uses exaflop-scale computation rates
    (\$10\^{18}\$ ops/sec) to provide a realistic time-to-crack estimate
    for high-performance quantum hardware.
-   **Entropy Auditing:** Validates that 256-bit AES remains a standard
    for post-quantum resistance, as its quantum-effective security
    (128-bit) remains beyond feasible compute horizons.

## Problems Solved

1.  **Cryptographic Lifecycle Planning:** Helps determine when keys
    become vulnerable to future quantum advancements, allowing for
    proactive migration to higher bit-lengths.
2.  **Post-Quantum Strategy:** Confirms why AES-256 is currently
    considered the industry standard for remaining secure in the
    post-quantum era.

## Usage

from 042_pqc_aes_strength_auditor import PQCAnalyzer\
\
\# Initialize auditor\
audit = PQCAnalyzer()\
\
\# Compare security degradation between AES-128 and AES-256\
audit.calculate_resistance(128)\
audit.calculate_resistance(256)
