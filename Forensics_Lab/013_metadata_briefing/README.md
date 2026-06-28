# Forensic Metadata Briefing Tool (Project 024)

A diagnostic tool designed to extract critical low-level file-system artifacts, enabling the rapid creation of timelines and permission audits during digital forensic triage.

## Technical Explanation

* **Atomic Kernel Inversion:** Invokes `os.stat` directly inside a targeted exception-handling engine rather than using superficial pre-checks. This explicitly neutralizes Time-of-Check to Time-of-Use (TOCTOU) race condition vulnerabilities.
* **Padded Octal Masking:** Bitmasks the structural file mode against `0o777` and applies a padded string conversion format (`:03o`). This strips messy default Python prefixes (like `0o`) to yield an isolated, industry-standard 3-digit POSIX permission index.
* **Chronological Suite Synchronization:** Converts the raw `st_mtime` floating-point token into a standardized international timestamp (`YYYY-MM-DD HH:MM:SS`) via the `datetime` engine, preserving chronological output uniformity across your forensic toolkit.

## Problems Solved

* **Timeline Reconstruction:** Fast-tracks the creation of incident timelines by extracting authentic modification timestamps directly from filesystem allocation metadata.
* **Privilege & Execution Auditing:** Instantly reveals if an adversary flagged hidden tools or scripts with execution parameters (`x`), establishing the exact vector for unauthorized code runtimes.
* **TOCTOU Defense during Triage:** Eliminates process hanging or state-tampering failures if an active threat actor or parallel process deletes/mutates the target artifact while the scanner is reading it.

## Design Decisions: "Why this instead of that?"

| Category | Decision | Why? |
| :--- | :--- | :--- |
| **Error Architecture** | Direct Call + Exception Catch | Checking paths via `os.path.exists` creates a structural race condition. Moving straight to execution with localized exceptions ensures absolute IO isolation. |
| **Data Formatting** | Formatted Octal (`:03o`) | Rejects raw legacy `oct()` string slices, providing clean, zero-padded 3-digit permissions (e.g., `644` instead of `0o644`) for swift visual evaluation. |
| **Temporal Layout** | `datetime` Serialization | Upgrades loose, regional terminal time strings (`time.ctime`) to structured ISO-like templates, ideal for downstream automated chronological sorting. |
| **Execution Path** | Native CLI Wrapper | Bypasses blockages from synchronous text queries (`input()`), turning the script into an automatable unit ready for deployment inside bulk execution pipelines. |

## Usage

This tool is engineered for seamless command-line interface (CLI) automation. Pass the targeted evidence file path directly as an argument:

```bash
python metadata_brief.py /path/to/evidence_artifact.bin
