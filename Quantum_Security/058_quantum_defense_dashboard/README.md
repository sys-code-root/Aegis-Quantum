# Graphical Quantum Defense Dashboard (Project 058)

An advanced graphical interface (GUI) developed via *customtkinter* that
merges background host environment monitoring (Sentinel) with
post-quantum lattice signature pipelines.

## Technical Explanation

-   **CustomTkinter GUI Matrix:** Builds a modern multi-threaded console
    interaction grid, isolating backend computation tasks from interface
    processing rendering routines.
-   **Process Watchdog Integration:** Integrates system hooks using
    *psutil* to iterate over system processes, laying down the
    groundwork to block malicious distractions or non-whitelisted items
    during critical work blocks.
-   **Qiskit 1.x QRNG Harvesting:** Provisions high-entropy keys
    on-demand by resolving physical simulation states using randomized
    Hadamard register distribution models.

## Problems Solved

1.  **Tool Fragmentation:** Consolidates loose terminal scripts (process
    checkers, key-generators, cryptographic testing suites) into a
    single, cohesive executable hub.
2.  **Cognitive Overload & Environment Control:** Streamlines
    environment auditing through simple visual control panels, creating
    predictable workspaces tailored for focused engineering tasks.

## Usage

\# Run the application interface locally\
python 058_quantum_defense_dashboard.py
