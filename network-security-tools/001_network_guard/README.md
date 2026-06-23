# Network Guard (Project 001)

A professional, modular Python toolkit engineered for secure network communication, cryptographic integrity verification, and data obfuscation.

## Technical Explanation

* **Constant-Time Security:** Utilizes `hmac.compare_digest` for all integrity checks. Unlike standard string operators (`==`), this method is resilient against **Timing Attacks**, preventing adversaries from deducing signatures based on comparison duration.
* **RAII-Style Resource Management:** Implements context managers (`with` statements) for all socket operations, ensuring network file descriptors are released instantly, preventing memory leaks and handle exhaustion during long-running forensic audits.
* **Stateless Architecture:** Encapsulated via `@staticmethod` decorators. This eliminates the overhead of class instantiation, reducing memory footprint and enabling the library to be seamlessly integrated into high-throughput, asynchronous pipelines without state conflict.
* **Gateway-Safe Encoding:** Implements `base64` wrapping for binary data, ensuring payloads remain safe for transmission across text-based network gateways, email buffers, or legacy infrastructure that would otherwise corrupt raw byte streams.

## Problems Solved

* **Cryptographic Authenticity:** Bridges the gap between simple data transmission and secure verification using HMAC-SHA256, guaranteeing that received telemetry has not been tampered with in transit.
* **Fault-Tolerant Networking:** Wraps volatile network I/O in robust exception handling, ensuring scanners and monitors do not crash when encountering timeouts, unreachable hosts, or closed ports.
* **Primitive Abstraction:** Eliminates scattered, redundant code by providing a unified interface for repetitive security primitives (banner grabbing, hashing, encoding), adhering to DRY (Don't Repeat Yourself) engineering principles.
* **Payload Obfuscation:** Provides lightweight XOR-based masking primitives to protect sensitive configuration strings from casual inspection during field triage.

## Design Decisions: "Why this instead of that?"

| Category | Decision | Why? |
| :--- | :--- | :--- |
| **Integrity Check** | `hmac.compare_digest` | Prevents timing-based side-channel attacks by ensuring the comparison time is independent of the content. |
| **Resource Mgmt** | `with` (Context Manager) | Automatically closes sockets and releases memory handles, even when network exceptions or connection resets occur. |
| **Architecture** | `@staticmethod` | Improves execution performance by avoiding the initialization of object state, making the library "plug-and-play" for IR scripts. |
| **Transmission** | `base64` | Converts non-printable binary data into standard ASCII, preventing corruption by gateways or protocol-specific data filters. |

## Usage

This library is designed to be imported into your forensic or defensive automation scripts. Ensure the file is saved as `network_guard.py`.

```python
from network_guard import NetworkGuard

guard = NetworkGuard()

# 1. Obfuscation: Protect sensitive strings
original = "SECURE_DATA_2026"
obfuscated = guard.xor_obfuscate(original)
print(f"Obfuscated Payload: {obfuscated}")

# 2. Integrity: Verify packet authenticity
message = "AUTH_ACTION"
sig = guard.generate_hmac_signature(b"secret_key", message)
print(f"Cryptographic Signature: {sig}")

# 3. Reconnaissance: Fetch service fingerprints
fingerprint = guard.get_service_fingerprint('google.com', 80)
print(f"Service Fingerprint: {fingerprint}")
