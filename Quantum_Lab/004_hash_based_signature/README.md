# Hash-Based Signature Simulator (Project 043)

A high-assurance cryptographic prototype demonstrating the mechanics of Post-Quantum Cryptography (PQC) through hash-based signature primitives. Engineered as a software-level simulation of One-Time Signature (OTS) logic, this utility validates identity and data integrity without relying on vulnerable trapdoor mathematical problems, rendering it inherently resilient against Shor's algorithm.

## Technical Explanation

* **Preimage and Collision Resistance:** Unlike RSA or Elliptic Curve systems, which depend on the computational difficulty of integer factorization and discrete logarithms, this framework shifts the security boundary entirely to the preimage resistance of the SHA-256 hashing primitive. This structure ensures that a quantum adversary cannot reverse-engineer public verifiers.
* **Deterministic Bitstream Binding:** Constructs an immutable mathematical link between the data payload and a private entropy matrix. By digesting the input message into a standardized bitstream, the engine targets specific secret tokens to disclose, creating a unique validation proof that cannot be attached to a altered payload.
* **One-Time Signature (OTS) Mechanics:** Mimics the core structural behavior of the Lamport signature protocol. Security is derived from the strict structural constraint that a private key state vector must only be signed against a single payload lifecycle, as repeated signatures over varying data would expose the underlying secret matrices.

## Problems Solved

* **Asymmetric Infrastructure Collapse:** Mitigates the existential threat posed by scalable quantum hardware running Shor's algorithm, which will instantly compromise legacy PKI architectures (RSA, ECDSA).
* **Signature Malleability and Tampering:** Eradicates interception vectors where a malicious actor attempts to forge or alter transactional identities, ensuring total non-repudiation over unsecure channels.
* **Cryptographic Dependency Overheads:** Eliminates the need for complex, heavy mathematical big-integer libraries by leveraging native, highly optimized one-way compression algorithms, making the deployment highly performant.

## Design Decisions: "Why this instead of that?"

| Category | Decision | Why? |
| :--- | :--- | :--- |
| **Core Primitive** | SHA-256 Hashing | Offers a predictable 256-bit security margin classically and maintains a robust 128-bit preimage security margin against Grover-class quantum attacks. |
| **Key Architecture** | Matrix-Based State Setup | Adheres strictly to foundational OTS principles, ensuring that validation can be computed using simple sequential hash validations. |
| **State Validation** | Strict One-Time Usage | Essential to prevent key reuse exploitation. Sacrificing multi-message capability guarantees absolute cryptographic isolation per transaction block. |
| **Verification Loop** | Forward Compression Checking | Bypasses modular exponentiation traps; verification requires only the forward execution of the hash function, which is immune to quantum algorithmic shortcuts. |



## Usage

This simulator acts as the primary validation block for testing stateful hash-based identity tokens inside the lab. Ensure the file is saved as `hash_signature.py`.

### Programmatic Deployment

```python
from hash_signature import HashSignature

# 1. Initialize the post-quantum signature environment
# Generates the internal key state vectors and public matrix maps
pqc = HashSignature()

# 2. Sign a high-value or sensitive data packet
# Discloses the specific secret fragments tied to the payload digest
sig = pqc.sign_message("Auth Data")

# 3. Verify identity and payload structural integrity
# Returns a boolean validation matrix reflecting target authenticity
is_valid = pqc.verify("Auth Data", sig)

print(f"[+] Cryptographic Integrity Status: {is_valid}")
