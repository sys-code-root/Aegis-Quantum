# Sentinel File Integrity Watchdog (Project 016)

A real-time File Integrity Monitoring (FIM) system built to track
filesystem events and establish algorithmic data integrity chains.

## Technical Explanation

-   **Cryptographic Baselines:** Converts full directory trees into an
    analytical dictionary matrix mapped by SHA-256 signatures.
-   **Chunked Streaming Execution:** Streams binary files in strict
    4096-byte sequences to optimize CPU execution overhead and prevent
    Out-Of-Memory (OOM) crashing hazards.
-   **Delta Differentiation Analysis:** Evaluates state changes using
    continuous algorithmic polling to compute explicit delta paths
    (added, customized, or removed assets).

## Problems Solved

1.  **Webshell Injection Discovery:** Immediately intercepts background
    adversarial drop events, flagging hidden scripts (e.g., prefix
    scripts starting with *.*) the moment they land on disk.
2.  **Anti-Forensics Tracking:** Detects malicious attempts to erase
    system log trails or alter diagnostic tracking databases.
3.  **Improper System Alteration:** Provides clear data logs detailing
    exactly which configuration contexts were warped during an
    operational breach window.

## Design Decisions: \"Why this instead of that?\"

  --------------------- ---------------------- ------------------------------------------------------------------------------------------------------------------------
  **Analysis Mode**     SHA-256 Polling        Cryptographic evaluation is immune to advanced metadata forging techniques like timestamp modification (timestomping).
  **Memory Strategy**   *4096-byte Chunking*   Guarantees system stability when validating massive files, keeping memory utilization flat.
  **Parsing Tree**      Recursive *os.walk*    Ensures full observation coverage across nested application structures and subdirectories.
  --------------------- ---------------------- ------------------------------------------------------------------------------------------------------------------------

## Usage

from 016_sentinel_watchdog import SentinelWatchdog\
\
\# Initiate monitoring on critical server directories\
watchdog = SentinelWatchdog(\"/var/www/uploads\")\
watchdog.start_monitoring(interval=2)
