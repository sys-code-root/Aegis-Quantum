# Forensic File Hasher (Project 022)

A cryptographic integrity utility designed to generate immutable digital
fingerprints (SHA-256) for forensic artifacts, essential for maintaining
secure chain-of-custody records.

## Technical Explanation

-   **Collision-Resistant Fingerprinting:** Implements the SHA-256
    algorithm to create a unique signature, ensuring that even
    single-bit modifications are detected during re-verification.
-   **Buffered Binary Streaming:** Processes target files using *4KB*
    chunk streams, ensuring system-level performance remains fluid even
    when hashing massive forensic drive images (e.g., .E01 or .dd
    files).
-   **Immutable Baseline Creation:** Provides the foundational hash
    necessary for legal-grade evidence verification, allowing
    independent auditors to confirm the artifact has not been modified
    since collection.

## Problems Solved

1.  **Chain of Custody Verification:** Allows investigators to prove
    that an evidence file currently under analysis is identical to the
    file captured at the crime scene.
2.  **Metadata Forgery Detection:** Effectively detects \"timestomping\"
    or hidden payload injections, as any alteration to the binary data
    results in a total hash mismatch.
3.  **Data Integrity Assurance:** Validates that data transfer/copying
    operations during collection did not result in corruption or
    bit-rot.

## Design Decisions: \"Why this instead of that?\"

  ----------------- -------------------- ----------------------------------------------------------------------------------------------------------------------------------
  **Algorithm**     SHA-256              Offers superior collision resistance compared to MD5 or SHA-1, aligning with modern industrial standards for evidence integrity.
  **IO Strategy**   4KB Buffer Blocks    Prevents the operating system from loading massive binary files into memory, eliminating the risk of heap overflows.
  **Encoding**      *rb* (Read Binary)   Essential for forensic integrity; forces raw byte processing regardless of text-encoding or binary file headers.
  ----------------- -------------------- ----------------------------------------------------------------------------------------------------------------------------------

## Usage

from 022_file_hasher import ForensicFileHasher\
\
\# Instantiate the hasher with the path to your evidence file\
hasher = ForensicFileHasher(\"disk_image_evidence.dd\")\
\
\# Generate the cryptographic signature\
signature = hasher.generate_hash()\
print(f\"Artifact Fingerprint: {signature}\")
