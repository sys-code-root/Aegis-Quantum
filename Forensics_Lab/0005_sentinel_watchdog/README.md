# Sentinel File Integrity Watchdog (Project 016)

A real-time File Integrity Monitoring (FIM) system built to track filesystem events and establish algorithmic data integrity chains.

## Technical Explanation

* **Cryptographic Baselines:** Converts full directory trees into an analytical dictionary matrix mapped by SHA-256 signatures.
* **Chunked Streaming Execution:** Streams binary files in strict 4096-byte sequences to optimize CPU execution overhead and prevent Out-Of-Memory (OOM) crashing hazards on massive files.
* **Delta Differentiation Analysis:** Evaluates state changes using continuous algorithmic polling to compute explicit delta paths (added, modified, or removed assets).
* **Concurrency State Guard:** Retains the last known cryptographic state if a file is temporarily locked or inaccessible during a polling cycle, preventing race condition noise and false deletion alerts.

## Problems Solved

* **Webshell Injection Discovery:** Immediately intercepts background adversarial drop events, flagging hidden scripts (e.g., files starting with `.`) the moment they land on disk.
* **Anti-Forensics Tracking:** Detects malicious attempts to erase system log trails, overwrite evidence, or alter diagnostic tracking databases.
* **Improper System Alteration:** Provides clear data logs detailing exactly which configuration contexts were warped or mutated during an operational breach window.

## Design Decisions: "Why this instead of that?"

| Category | Decision | Why? |
| :--- | :--- | :--- |
| **Analysis Mode** | SHA-256 Polling | Cryptographic evaluation is immune to advanced metadata forging techniques like timestamp modification (timestomping). |
| **Memory Strategy** | 4096-byte Chunking | Guarantees system stability when validating massive files, keeping memory utilization flat. |
| **State Resilience** | Historical Fallback | Retaining the last valid hash during transient read failures eliminates false positives caused by locked or busy system resources. |

## Usage

This tool is optimized for command-line interface (CLI) automation. Pass the target directory path directly as an argument:

```bash
python sentinel_watchdog.py /var/www/uploads
