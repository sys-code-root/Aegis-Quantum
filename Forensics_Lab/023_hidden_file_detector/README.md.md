# Hidden Artifact Detector (Project 023)

A forensic triage utility that bypasses standard shell visibility to
expose hidden configuration files, scripts, and persistent backdoors
masked by the dotfile (.) convention.

## Technical Explanation

-   **Dotfile Enumeration:** Performs direct filesystem listing to
    enumerate all directory entries, explicitly bypassing the standard
    shell\'s exclusion of dot-prefixed artifacts.
-   **Forensic Triage:** Automates the search for hidden configuration
    stores (*.bashrc*, *.profile*) or hidden malicious directories often
    used by threat actors to persist within the environment.

## Problems Solved

1.  **Backdoor Concealment:** Exposes malicious scripts or hidden
    directories created by attackers to maintain a foothold in the
    target system.
2.  **Persistence Discovery:** Locates modified shell environment
    configurations that automatically trigger malicious payloads upon
    user login.
3.  **Forensic Visibility:** Provides a quick audit of the directory\'s
    contents that may be invisible in typical GUI file browsers or
    standard CLI output.

## Design Decisions: \"Why this instead of that?\"

  ------------------ ------------------ -----------------------------------------------------------------------------------------------------------------------
  **Detection**      Dot-Prefix Logic   Uses native OS standards to ensure 100% detection coverage of hidden items without false positives.
  **I/O Strategy**   *os.listdir*       Queries the kernel filesystem index directly, preventing local aliases or environment settings from hiding real data.
  ------------------ ------------------ -----------------------------------------------------------------------------------------------------------------------

## Usage

from 023_hidden_file_detector import HiddenFileDetector\
\
\# Define the suspicious directory target\
detector = HiddenFileDetector(\"/home/user/.hidden_space\")\
\
\# Execute scan\
detector.scan()
