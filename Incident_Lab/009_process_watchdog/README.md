# Process Watchdog (Project 009)

An automated defense tool that enforces strict process whitelisting (Zero-Trust) by terminating any unauthorized background activities and rogue executables in real-time.

## Technical Explanation

* **Dynamic State Auditing:** Utilizes `psutil.process_iter` to poll the system's active process list continuously. Process objects are terminated directly from the iterator in memory, eliminating the overhead of redundant API calls.
* **Algorithmic Optimization ($O(1)$):** Casts the allowed application arrays into a Python hash-set structure. This upgrades the whitelist validation from a linear loop ($O(n)$) to constant-time lookup ($O(1)$), maximizing enforcement speed without spiking the CPU.
* **Targeted Kernel Shielding:** Replaces naive integer filters with absolute OS kernel protections. Explicitly isolates critical architecture processes (like `smss.exe`, `csrss.exe`, and static PIDs `0` and `4`), entirely removing the risk of triggering Kernel Panics or Blue Screens of Death (BSOD).
* **Automated CLI Fallbacks:** Features an intelligent argument parser that accepts dynamic allowed binaries via the terminal, seamlessly defaulting to a pre-hardened baseline configuration if no arguments are provided.

## Problems Solved

* **Malware Persistence (Zero-Trust):** Proactively slaughters unauthorized payloads, reverse shells, or droppers that attempt to spin up unseen processes in the background.
* **Environment Hardening:** Ensures that only explicitly approved forensic acquisition tools or incident response frameworks can execute on a compromised or highly secure host.
* **Compliance & Focus Enforcement:** Acts as an aggressive local policy manager to kill unauthorized entertainment apps, unapproved browsers, or distracting software during focused analysis sessions.

## Design Decisions: "Why this instead of that?"

| Category | Decision | Why? |
| :--- | :--- | :--- |
| **Logic Model** | Strict Whitelisting | Infinitely more secure than signature-based blacklisting. By defaulting to "deny all," it automatically neutralizes zero-day malware. |
| **Data Structure** | Python Hash-Sets (`set`) | Evaluating names against a list requires scanning every item. Sets use cryptographic hashing to verify authorization instantly. |
| **OS Safety** | Static PID & Name Isolation | Modern OS architectures often assign high PIDs to vital services. The old `PID < 100` rule is obsolete and dangerous. |
| **API Handling** | Direct Iteration Kill | Calling `psutil.Process(pid)` repeatedly leaks memory. Terminating the active object directly from the loop keeps the watchdog extremely lightweight. |

## Usage

This utility features a parameter-driven terminal interface. Execute the application by passing your authorized process names directly as arguments. 

*(Note: The script automatically protects its own Python interpreter and core Windows/Linux subsystems).*

```bash
# Example 1: Run the watchdog allowing only Firefox, VS Code, and standard terminal
python watchdog.py firefox.exe code.exe cmd.exe powershell.exe

# Example 2: Run with the built-in default safe-list
python watchdog.py
