# Network Heartbeat System (Project 002)

A high-assurance utility designed to secure continuous device communication by preventing "Replay Attacks" and unauthorized signal spoofing through cryptographic time-based binding.

## Technical Explanation

* **Sliding-Window Authentication:** Utilizes `time.time()` to generate ephemeral, time-sensitive packets. By validating these against a defined temporal window, the system ensures that packets are only valid for a specific duration, rendering intercepted payloads useless to attackers seconds later.
* **Cryptographic Binding:** Binds the current timestamp to a pre-shared secret key using `SHA-256` hashing. This ensures that every heartbeat is cryptographically unique, even if the device state remains constant.
* **Constant-Time Verification:** Employs `secrets.compare_digest` for all hash validations. This is critical for security; standard comparison operators (`==`) can leak information about the secret via execution time (side-channel timing attacks), whereas `compare_digest` forces the operation to take the same amount of time regardless of whether the match is correct or incorrect.

## Problems Solved

* **Replay Attack Mitigation:** Effectively stops attackers from capturing and re-transmitting (looping) heartbeat packets. Since the server validates the timestamp, stale packets are rejected as expired.
* **Spoofing Prevention:** Ensures that only agents possessing the master `secret_key` can generate valid heartbeat signatures, authenticating the device source.
* **Data Tampering Detection:** Any modification to the timestamp or key results in a completely different hash, ensuring the integrity of the communication signal.

## Design Decisions: "Why this instead of that?"

| Category | Decision | Why? |
| :--- | :--- | :--- |
| **Comparison** | `secrets.compare_digest` | Essential for security; it prevents timing side-channel attacks, which can allow an attacker to brute-force a signature byte-by-byte. |
| **Logic** | Time-based Sliding Window | Prevents stale packet acceptance, a fundamental requirement for secure UDP streaming and authenticated network monitors. |
| **Integrity** | `SHA-256` | Provides high collision resistance and creates a robust cryptographic bond between the timestamp and the secret key. |
| **Standard** | `secrets` module | Designed specifically for cryptography, it is safer for security-critical comparisons than standard `hashlib` or `random` modules. |

## Usage

This utility is designed to be integrated into your network monitoring pipelines. Ensure the file is saved as `network_heartbeat.py`.

```python
from network_heartbeat import NetworkHeartbeat

