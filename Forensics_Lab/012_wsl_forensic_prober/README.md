# WSL Forensic Prober (Project 012)

A specialized forensic audit tool designed for WSL (Windows Subsystem
for Linux) and native Linux environments.

## Technical Explanation

-   **Signature Analysis:** Uses hexadecimal \"Magic Numbers\" to verify
    if files have been renamed to disguise their true nature (e.g., an
    *.exe* disguised as a *.txt*).
-   **Persistence Detection:** Scans critical Linux initialization files
    (*.bashrc*, *.profile*) for common reverse shell signatures (*curl*,
    *nc*).
-   **Resource Auditing:** Correlates high CPU utilization with specific
    PIDs, aiding in the detection of hidden miners or malicious agents.

## Problems Solved

1.  **Disguised Malware:** Detects files that claim to be one type but
    have headers of another.
2.  **Persistence Discovery:** Identifies mechanisms attackers use to
    ensure their code runs every time the Linux shell opens.
3.  **Evidence Timeline:** Extracts creation/modification timestamps,
    forming the backbone of any forensic timeline analysis.

## Design Decisions: \"Why this instead of that?\"

  --------------- ------------------- --------------------------------------------------------------------------------------
  **Signature**   Magic Numbers       Metadata (file extensions) can be easily faked; binary signatures cannot.
  **Integrity**   *os.stat*           Provides hardware-level file timestamps that are harder for non-root users to spoof.
  **Detection**   Real-time Monitor   Captures file system events that logs might fail to record.
  --------------- ------------------- --------------------------------------------------------------------------------------

## Usage

from 012_wsl_forensic_prober import WSLForensicProber\
\
prober = WSLForensicProber()\
prober.analyze_file_integrity(\"/mnt/c/evidence.exe\")\
prober.check_persistence()
