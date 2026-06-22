# Network Guard (Project 1)

A professional, modular Python toolkit designed for secure network
communication, data integrity verification, and simple obfuscation.

## Purpose

This tool serves as a utility library for developers working on network
security tasks. It abstracts common, repetitive network
operations---such as banner grabbing, integrity checks, and data
encoding---into a reusable, robust class structure.

## Technical Explanation

The core of this project is the *NetworkGuard* class, which utilizes
static methods to perform discrete tasks without maintaining complex
internal states.

-   **Network Interaction:** Uses the *socket* library with context
    managers (*with* statement) to ensure proper connection handling and
    resource cleanup.

-   **Cryptography & Integrity:**

    -   **HMAC-SHA256:** Used for message authentication to ensure data
        hasn\'t been tampered with.
    -   **SHA1/SHA256:** Used for fingerprinting services and verifying
        packet integrity.

-   **Data Handling:** Implements *base64* encoding for safe
    transmission of binary data over text-based network protocols.

## Problems Solved

1.  **Code Redundancy:** Instead of scattered scripts, all logic is
    encapsulated, promoting DRY (Don\'t Repeat Yourself) principles.
2.  **Unstable Connections:** Robust exception handling prevents scripts
    from crashing due to timeouts or blocked ports.
3.  **Data Corruption/Tampering:** Provides a clear path to verify if
    received data matches the original sender\'s hash.
4.  **Security Obfuscation:** Offers basic XOR-based masking to protect
    sensitive strings from casual inspection.

## Design Decisions: \"Why this instead of that?\"

  ------------------- -------------------------- -------------------------------------------------------------------------------------------------------------------
  **Comparisons**     *hmac.compare_digest*      Prevents **Timing Attacks**, which can occur with standard *==* operators.
  **Modularity**      *staticmethod*             Improves performance and memory usage by removing the need for class instantiation.
  **Encoding**        *base64*                   Unlike raw binary, Base64 ensures characters are printable and safe for transmission across all network gateways.
  **Resource Mgmt**   *with* (context manager)   Guarantees that network sockets are closed automatically, even if an error occurs.
  ------------------- -------------------------- -------------------------------------------------------------------------------------------------------------------

## Usage
This library is designed to be imported into your forensic or defensive automation scripts. Ensure the file is saved as network_guard.py

\
guard = NetworkGuard()\
\
\# Example: Verify if a message is intact\
message = \"SECURE_ACTION\"\
sig = guard.generate_hmac_signature(b\"secret_key\", message)\
print(f\"Signature: {sig}\")
