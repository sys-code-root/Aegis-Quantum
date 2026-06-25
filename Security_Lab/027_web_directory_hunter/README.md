# Web Directory Hunter & Path Auditor (Project 027)

An automated reconnaissance utility engineered for directory enumeration and path auditing. This tool facilitates the identification of hidden resources, forgotten backup logs, and misconfigured administration endpoints, providing critical visibility into a target's attack surface.

## Technical Explanation

* **HTTP Response Mapping:** Inspects operational HTTP response codes (e.g., `200 OK` vs `403 Forbidden`) to map server-side directory structures. By distinguishing between "Found," "Restricted," and "Not Found," the auditor efficiently reconstructs the target's logical file structure.
* **Stream-Based Ingestion:** Implements memory-efficient I/O streaming. By processing dictionary wordlists line-by-line rather than loading them entirely into system RAM, the tool maintains a minimal memory footprint, allowing for the execution of massive wordlists on resource-constrained forensic hardware.
* **Network Exception Shielding:** Incorporates localized exception handling to maintain audit continuity. The scanner proactively intercepts network drops and timeout errors, ensuring that transient connectivity issues do not terminate the ongoing enumeration process.

## Problems Solved

* **Unprotected Artifact Exposure:** Identifies "Shadow IT" or forgotten diagnostic scripts (`info.php`, `test.php`), configuration backups (`.bak`, `.config`), and source code archives that are often left accessible in production environments.
* **Access Control Validation:** Validates whether restricted administrative paths are truly secure. If a path returns a `403 Forbidden`, the auditor confirms the existence of the directory while validating that the server’s authorization controls are functioning correctly.
* **Attack Surface Reduction:** By revealing non-indexed paths that are left reachable, the tool enables administrators to perform proactive hardening before these endpoints are exploited by malicious actors.

## Design Decisions: "Why this instead of that?"

| Category | Decision | Why? |
| :--- | :--- | :--- |
| **Request Strategy** | `requests.get` | Provides the most accurate simulation of a standard browser request, ensuring the server responds as it would to a legitimate user. |
| **Timeout Boundary** | 3-Second Rule | Optimized for speed. It is short enough to bypass slow "hanging" endpoints but long enough to allow a healthy server to process the request. |
| **Logic** | Dictionary-Based | Deterministic. It removes the guesswork of "guessing" names, ensuring that only the paths explicitly defined in the wordlist are tested. |
| **Performance** | Non-Persistent I/O | Operates directly against the target host without local state management, ensuring the tool remains ephemeral and leaves zero footprint on the forensic machine. |

## Usage

This utility serves as the primary enumeration module for your reconnaissance pipeline. Ensure the file is saved as `directory_hunter.py`.

```python
from directory_hunter import WebDirectoryHunter

# 1. Instantiate the auditor on the target service
# The tool automatically manages trailing slashes
auditor = WebDirectoryHunter("http://localhost:8080")

# 2. Run the discovery engine against a standard wordlist
# This performs the structural testing
auditor.scan("wordlist.txt")
