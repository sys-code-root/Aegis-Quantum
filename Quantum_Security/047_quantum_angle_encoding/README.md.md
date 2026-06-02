# Angle Encoding for Quantum Neural Networks (Project 047)

A data-mapping utility that translates continuous classical data into
quantum register rotations, enabling the input layer for variational
quantum circuits.

## Technical Explanation

-   **Rotation Encoding:** Utilizes \$R_y(\\theta)\$ gates, where the
    classical input \$\\theta\$ determines the probability amplitude
    \$cos(\\theta/2)\|0\\rangle + sin(\\theta/2)\|1\\rangle\$.
-   **Feature-to-Qubit Mapping:** Each feature in a dataset corresponds
    directly to an individual qubit, allowing for high-dimensional
    feature space representation.
-   **QNN Foundation:** This serves as the \"input layer\" for hybrid
    quantum-classical machine learning models.

## Problems Solved

1.  **Continuous Data Mapping:** Unlike basis encoding (which maps
    discrete bits), angle encoding allows for the direct ingestion of
    continuous, floating-point data points.
2.  **QNN Integration:** Provides the essential interface required for
    training variational quantum circuits using classical optimization
    loops.

## Usage

from 047_quantum_angle_encoding import AngleEncoder\
\
\# Map normalized features to 3 qubits\
features = \[np.pi/4, np.pi/2, np.pi\]\
encoder = AngleEncoder(features)\
probabilities = encoder.run_simulation()
