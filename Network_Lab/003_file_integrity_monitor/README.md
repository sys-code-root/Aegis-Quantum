# File Integrity Monitor (Project 003)

A high-performance security utility engineered to detect unauthorized modifications to system files or sensitive configurations by performing continuous cryptographic integrity verification.

## Technical Explanation

* **Memory-Efficient Streaming I/O:** Utilizes chunk-based reading (4096-byte blocks) to process files. By streaming the file into memory in small segments rather than loading it entirely, the monitor handles massive log files and system binaries without risking system RAM exhaustion.
* **Cryptographic Baseline Verification:** Implements the `SHA-256` hashing algorithm to generate a unique digital "fingerprint." Due to the "Avalanche Effect," even a single-bit modification in the target file results in a completely distinct hash, ensuring absolute tamper detection.
* **Stateless Utility Architecture:** Encapsulated via `@staticmethod` decorators. This design allows the integrity verification logic to be imported and executed instantly within larger Incident Response orchestrators without the memory overhead of class instantiation.

## Problems Solved

* **Rootkit/Backdoor Detection:** Instantly identifies if critical system configurations (e.g., `/etc/hosts`, `.ssh/authorized_keys`, or app settings) have been injected with malicious payloads or persistence mechanisms.
* **Forensic Audit Integrity:** Provides a programmatic, reproducible method to verify the state of a system during and after a security incident, creating a reliable chain of custody for log files.
* **Configuration Drift Prevention:** Monitors production environments for unauthorized "hot-patching," ensuring that deployed infrastructure remains aligned with defined security baselines.

## Design Decisions: "Why this instead of that?"

| Category | Decision | Why? |
| :--- | :--- | :--- |
| **Hashing Algorithm** | `SHA-256` | Offers the optimal balance between collision resistance and computational performance, making it the industry standard for integrity monitoring. |
| **I/O Strategy** | Chunked Reading | Reading in 4KB buffers is a systems-engineering best practice; it prevents the tool from crashing when auditing large binary logs or forensic images. |
| **Modularity** | `staticmethod` | Decoupling the hash calculation from the class instance state ensures the logic is pure, thread-safe, and easily reusable in other automation scripts. |
| **Loop Control** | `KeyboardInterrupt` | Provides a graceful exit path for forensic analysts to stop the monitoring cycle instantly without leaving orphaned processes or corrupted locks. |

## Usage

This utility is designed to be imported into your forensic automation pipelines. Ensure the file is saved as `integrity_monitor.py`.

```python
from integrity_monitor import IntegrityMonitor

monitor = IntegrityMonitor()

# 1. Establish the "Known Good" Baseline
baseline = monitor.calculate_hash("config_test.txt")
print(f"Cryptographic Baseline: {baseline}")

# 2. Start the Continuous Integrity Loop
# This will alert if the file content deviates from the baseline
monitor.monitor("config_test.txt", baseline, interval=5)
