# Grover\'s Search Algorithm Simulator (Project 041)

A quantum search implementation that utilizes amplitude amplification to
find a target state within a non-structured quantum database with
quadratic speedup.

## Technical Explanation

-   **Uniform Superposition:** Initializes all possible states in the
    Hilbert space equally using Hadamard gates, creating a parallel
    search environment.
-   **Oracle Phase:** Inverts the phase of the target state
    \$\|11\\rangle\$, effectively \"tagging\" the item the search engine
    intends to retrieve.
-   **Amplitude Amplification:** The diffusion operator reflects the
    amplitudes about the mean, boosting the probability amplitude of the
    marked state while suppressing others.

## Problems Solved

1.  **Unstructured Search Bottlenecks:** Provides a mathematical
    shortcut for searching unsorted lists where classical algorithms are
    constrained by linear time complexity.
2.  **Computational Efficiency:** Demonstrates how quantum interference
    can replace brute-force iterative checking with targeted probability
    reinforcement.

## Usage

from 041_grover_search_algorithm import GroverSearch\
\
\# Initialize and execute the Grover search pipeline\
grover = GroverSearch()\
grover.run()
