# Hidden Artifact Detector (Project 023)

A forensic triage utility that bypasses standard shell visibility to expose hidden configuration files, deep-nested scripts, and persistent backdoors masked by the dotfile (`.`) convention.

## Technical Explanation

* **Recursive Tree Traversal:** Utilizes `os.walk` to execute deep structural scans through target directory branches, eliminating the critical blind spots left behind by shallow, single-level inspection tools.
* **Dual-State Object Separation:** Tracks and evaluates filesystem entities using separate inner loops for directories and files. This allows the tool to isolate entire masked directories alongside isolated hidden script footprints.
* **CLI Parameter Standardization:** Implements automated command-line argument processing (`sys.argv`) featuring a graceful inline fallback to the active working directory (`"."`) if no explicit target scope is supplied by the operator.

## Problems Solved

* **Deep-Nested Backdoor Concealment:** Exposes malicious payloads, stagers, or tools hidden deep within legitimate application subdirectories (e.g., `.config/` or `.local/`) that easily deceive shallow directory lists.
* **Persistence Vector Discovery:** Locates modified shell profile structures (such as hidden `.bashrc` or `.profile` files) weaponized by threat actors to execute arbitrary commands upon user interaction.
* **Evasion Countermeasures:** Provides an absolute, configuration-agnostic view of storage media, ensuring local shell aliases (like a hijacked `ls` command) cannot hide malicious files from the forensic analyst.

## Design Decisions: "Why this instead of that?"

| Category | Decision | Why? |
| :--- | :--- | :--- |
| **Traversal Method** | Recursive `os.walk` | Shallow listing (`os.listdir`) completely misses persistent backdoors hidden inside sub-folders. True recursive sweeping maps the entire tree. |
| **Object Isolation** | Split `dirs` / `files` Loops | Attackers often hide tooling inside an entirely hidden folder structure. Distinguishing objects clarifies the target's forensic architecture. |
| **Execution Flow** | CLI Argument + Default Fallback | Bypasses slow interactive queries (`input()`), enabling rapid manual triage as well as automated multi-directory auditing via bash loops. |

## Usage

This tool is optimized for command-line interface (CLI) execution. Pass the target path as a terminal argument, or omit it to scan your current working directory:

```bash
# Scan a specific directory target
python hidden_detector.py /home/user/evidence_folder

# Scan the current directory automatically (Fallback mode)
python hidden_detector.py
