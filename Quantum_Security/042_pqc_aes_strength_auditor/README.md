# PQC AES Strength Auditor (Project 042)

A high-assurance cryptographic auditing framework engineered to simulate, calculate, and analyze the quantitative degradation of symmetric keyspaces under quantum cryptanalytic acceleration. This utility maps keyspace resistance profiles against next-generation compute bounds to provide hard empirical timelines for enterprise migration strategies.

## Technical Explanation

* **Quantum Entropy Erosion Modeling:** Quantifies the security margin reduction from a classical brute-force bound of $2^N$ states down to an effective quantum search space of $2^{N/2}$. This mathematical transformation models the exact impact of Grover's asymptotic speedup on unstructured keyspaces.
* **Exaflop-Scale Horizon Thresholding:** Simulates ultra-high-performance quantum compute capabilities utilizing exaflop-scale performance metrics ($10^{18}$ operations per second). This allows the engine to calculate realistic worst-case time-to-compromise horizons for legacy encryption standards.
* **Symmetric Margin Validation:** Evaluates and proves the structural viability of symmetric block ciphers in the post-quantum era. The analyzer isolates how Advanced Encryption Standard (AES) variants react, demonstrating why AES-128 collapses to an insecure 64 bits of effective entropy, while AES-256 preserves a rock-solid 128-bit defense margin.

## Problems Solved

* **Speculative Cryptographic Risk:** Replaces arbitrary timeline guesswork with rigid mathematical calculations regarding exactly when and how existing symmetric infrastructure fails against scalable quantum processors.
* **Migration Strategy Justification:** Provides chief information security officers (CISOs) with the empirical data needed to justify the computational and operational overhead of upgrading production endpoints from 128-bit to 256-bit encryption.
* **Compliance and Lifecycle Planning:** Directly aids risk assessment teams in building proactive asset-hardening roadmaps that comply with updated post-quantum security frameworks (such as NIST and BSI guidelines).

## Design Decisions: "Why this instead of that?"

| Category | Decision | Why? |
| :--- | :--- | :--- |
| **Analysis Model** | Asymptotic Complexity Mapping | Evaluates keyspaces based on the fundamental physics of Grover's algorithm rather than specific, volatile hardware configurations, making the predictions future-proof. |
| **Compute Metrics** | Exaflop Scaling ($10^{18}$ ops/sec) | Establishes an aggressive computational ceiling to simulate a well-funded, highly advanced adversarial nation-state threat vector. |
| **Scope Isolation** | Unstructured Attack Focus | Concentrates purely on key-exhaustion bounds, removing variable real-world networking factors to deliver a baseline measurement of mathematical structural integrity. |
| **Architecture** | Deterministic Math Engine | Utilizes direct analytical computation rather than resource-heavy iterative simulation loops, enabling instant multi-variant audits. |



## Usage

This utility acts as the primary analytical component for cryptographic life-cycle assessments within the lab. Ensure the file is saved as `pqc_aes_auditor.py`.

### Programmatic Integration

```python
from pqc_aes_auditor import PQCAnalyzer

# 1. Initialize the cryptographic strength auditor engine
audit = PQCAnalyzer()

# 2. Execute and compare keyspace resistance profiles
# Outputs the mathematical breakdown and time-to-crack projections
audit.calculate_resistance(128)
audit.calculate_resistance(256)
