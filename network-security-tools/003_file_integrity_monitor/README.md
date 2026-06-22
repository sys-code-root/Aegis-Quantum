# File Integrity Monitor (Project 3)

A security utility designed to detect unauthorized modifications to
system files or sensitive configurations by performing continuous
cryptographic integrity checks.

## Purpose

In cybersecurity, an attacker\'s primary goal is often to alter system
configuration files to gain persistence. This tool provides a baseline
\"fingerprint\" of a file and alerts the administrator if the file\'s
content deviates from that fingerprint.

## Technical Explanation

-   **Chunk-based Hashing:** Uses 4096-byte blocks to read files,
    ensuring that the script can handle large files without exhausting
    system memory.
-   **Cryptographic Verification:** Uses *SHA-256* to create a secure
    hash. Even a change of a single character in the file will result in
    a completely different hash (Avalanche Effect).

## Problems Solved

1.  **Unauthorized Tampering:** Detects if configuration files (like
    *hosts*, *.ssh/authorized_keys*, or app settings) were modified.
2.  **Audit Trail:** Provides a programmatic way to verify system state
    during a security incident.
3.  **Persistence Detection:** Helps identify if a backdoor was injected
    into your script files.

## Design Decisions

  ----------------------- ----------------- -----------------------------------------------------------------------------------------------------------
  **Hashing Algorithm**   *SHA-256*         Provides an ideal balance between security and performance for integrity monitoring.
  **I/O Strategy**        Chunked Reading   Allows the tool to monitor large log files without loading them entirely into RAM.
  **Modularity**          *staticmethod*    The hash calculation logic is stateless, making it easy to import into other security automation scripts.
  ----------------------- ----------------- -----------------------------------------------------------------------------------------------------------

## Usage

from file_monitor import IntegrityMonitor\
\
monitor = IntegrityMonitor()\
\# Get original hash\
baseline = monitor.calculate_hash(\"my_config.conf\")\
\
\# Start monitor\
monitor.monitor(\"my_config.conf\", baseline)
