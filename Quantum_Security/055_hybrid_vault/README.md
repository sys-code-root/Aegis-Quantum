# Hybrid Post-Quantum Cryptographic Vault (Project 055)

A high-assurance hybrid cryptographic framework engineered to safeguard sensitive data assets against both classical and quantum adversarial capabilities. This architecture unifies the post-quantum resilience of Crystals-Kyber lattice-based Key Encapsulation Mechanisms (KEM) with direct-sampled Quantum Random Number Generation (QRNG) and high-throughput symmetric AES-256-CBC encryption.

## Technical Explanation

* **Lattice-Based Cryptography:** Integrates Crystals-Kyber (Kyber768), a quantum-safe primitive rooted in the mathematical hardness of the Module Learning With Errors (M-LWE) problem. This mathematical formulation provides structural immunity against Shor's algorithm, protecting asymmetric key exchanges from polynomial-time quantum factorization.
* **Direct Quantum Entropy Sampling:** Replaces deterministic Pseudo-Random Number Generators (PRNG) with a dynamic, multi-qubit Hadamard pipeline. By placing registers into a uniform superposition and measuring their state collapse, the system harvests true physical entropy directly into raw byte arrays, ensuring fundamentally unpredictable Initialization Vectors (IV).
* **Hybrid Structural Layer:** Employs a dual-engine architecture. It utilizes the asymmetric post-quantum mechanism exclusively for the secure distribution of a 256-bit shared secret (the key envelope), while offloading the heavy payload processing to hardware-optimized symmetric AES blocks to maximize throughput.

## Problems Solved

* **The "Harvest Now, Decrypt Later" Threat:** Neutralizes passive interception campaigns where adversaries capture encrypted traffic logs today with the intent of decrypting them retrospectively once fault-tolerant quantum computers become available.
* **Initialization Vector (IV) Predictability:** Eliminates the risk of pattern leakage and cipher-block correlation in CBC mode. By feeding the cipher's block requirements with true quantum randomness instead of seed-based software equations, it guarantees that identical plaintexts will never produce recognizable ciphertext structures.
* **Data Transport Latency:** Bridges the performance gap of asymmetric post-quantum algorithms. Splitting the logic into a hybrid topology ensures enterprise-level file processing speeds without compromising the post-quantum security boundary.

## Design Decisions: "Why this instead of that?"

| Category | Decision | Why? |
| :--- | :--- | :--- |
| **Entropy Strategy** | Direct Byte Assembly | Critical Upgrade: Instead of seeding a classical PRNG with a single quantum value, the system now streams state collapses directly into bytes, achieving true cryptographic randomness for the IV. |
| **KEM Standard** | Crystals-Kyber768 | Recognized by NIST as the global baseline for general encryption due to its optimal balance between ciphertext size, execution speed, and security margins. |
| **Cipher Block Mode** | AES-256-CBC + Padding | A time-tested standard for data-at-rest and bulk storage vaults. Combined with true quantum IV generation, its security profile is significantly hardened. |
| **Quantum Scaling** | Dynamic Qubit Allocation | Scalable layout generation. The system automatically provisions a matching register width (num_bits = length * 8) to build the requested data arrays in a single execution shot. |



## Usage

This framework serves as the primary secure storage utility for your sensitive intelligence archives. Ensure the file is saved as `hybrid_vault.py`.

```python
from hybrid_vault import HybridVault

# 1. Initialize the post-quantum hybrid cryptographic vault
vault = HybridVault()

# 2. Execute the verification and deployment pipeline
# This automates keypair generation, quantum IV harvesting, and payload wrapping
vault.run_deployment_test()
