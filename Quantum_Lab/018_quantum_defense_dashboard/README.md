# Graphical Quantum Defense Dashboard (Project 058)

A modern, high-assurance orchestration interface engineered using `customtkinter`. This control plane unifies real-time host environment telemetry (Sentinel) with post-quantum cryptographic primitives and Quantum Random Number Generation (QRNG), transforming fragmented security scripts into a cohesive desktop security environment.

## Technical Explanation

* **Asynchronous GUI Matrix (`customtkinter`):** Implements a hardware-accelerated, modern user interface. By isolating the main interface rendering loop from backend computational tasks (such as quantum circuit execution and continuous polling), the dashboard ensures fluid responsiveness even during heavy cryptographic processing.
* **Proactive System Telemetry (`psutil`):** Integrates natively with host operating system hooks to monitor ongoing process lifecycles. This architectural design creates a system watchdog layer capable of identifying running processes and laying the groundwork to mitigate malicious execution vectors or unauthorized environmental drift.
* **Quantum Superposition Sampling (Qiskit 1.x):** Provisions high-entropy cryptographic seeds on-demand. By simulating pure uniform Hadamard superposition states $\frac{|0\rangle + |1\rangle}{\sqrt{2}}$ and triggering state collapses, the framework harvests true binary randomness, bypassing the vulnerabilities of classical pseudo-random algorithms.

## Problems Solved

* **Siloed Tooling Fragmentation:** Eliminates loose, independent terminal utilities (process checkers, key generators, and cryptographic scripts) by consolidating them into a single executable control hub.
* **Operator Cognitive Overload:** Mitigates operational configuration mistakes by abstracting complex command-line arguments behind an intuitive, human-centric visual management grid.
* **Environment Visibility Gaps:** Solves the lack of real-time monitoring during sensitive operations, allowing the operator to continuously audit the host machine's execution space for unrecognized background tasks.

## Design Decisions: "Why this instead of that?"

| Category | Decision | Why? |
| :--- | :--- | :--- |
| **UI Engine** | `customtkinter` | Enhances native Tkinter with a professional dark-themed appearance, native scaling, and hardware acceleration with zero complex distribution baggage. |
| **Threading Model** | Main Loop Decoupling | Long-running monitoring tasks and quantum simulations are offloaded to background threads to prevent the application window from freezing. |
| **Telemetry Hook** | `psutil` Core | Provides cross-platform access to system metrics and process tables without requiring unstable, OS-specific low-level assembly bindings. |
| **Entropy Source** | Hadamard Superposition | Utilizes fundamental quantum mechanics rather than predictable software equations, achieving true mathematical unpredictability for key generation. |

## Usage

This dashboard acts as the unified frontend wrapper for your local defense suite. Ensure your runtime environments are initialized properly.

### Execution

Launch the operational dashboard directly from your terminal workspace:

```bash
python quantum_defense.py
