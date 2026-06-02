# Forensic Metadata Briefing Tool (Project 024)

A diagnostic tool designed to extract critical low-level file-system
artifacts, enabling the rapid creation of timelines and permission
audits during digital forensic triage.

## Technical Explanation

-   **System-Call Interface:** Utilizes *os.stat* to pull raw
    kernel-level metadata, bypassing higher-level abstractions that
    might hide file attributes.
-   **Octal Permission Masking:** Masks the file mode against *0o777* to
    isolate the standard POSIX permission structure, clarifying whether
    an artifact had read, write, or execute triggers.
-   **Temporal Mapping:** Maps *st_mtime* (Modification Time) to
    standard human-readable strings, allowing investigators to identify
    exactly when an evidence artifact was last tampered with.

## Problems Solved

1.  **Timeline Reconstruction:** Helps link specific files to the
    timeline of an incident by verifying exactly when they were last
    accessed or changed.
2.  **Permission Audit:** Identifies if malicious scripts or binaries
    were tagged as executable (*x*) by an attacker, confirming their
    potential for code execution.
3.  **Artifact Identification:** Quickly provides technical stats for
    triage when dealing with high volumes of unknown file dumps found in
    a compromised directory.

## Design Decisions: \"Why this instead of that?\"

  ----------------- ------------------- ---------------------------------------------------------------------------------------------------------------------------------
  **Data Source**   *os.stat*           The most direct way to query OS metadata; it\'s lightweight and works instantly without external dependencies.
  **Format**        Octal Permissions   The industry-standard representation for UNIX-like permissions, instantly recognizable to forensic investigators during triage.
  ----------------- ------------------- ---------------------------------------------------------------------------------------------------------------------------------

## Usage

To extract metadata and permission artifacts for a specific evidence
file, initialize the class and trigger the briefing method:

from 024_metadata_briefing import MetadataBrief\
\
\# Define the path to the suspected forensic artifact\
brief = MetadataBrief(\"/tmp/malicious_payload.sh\")\
\
\# Execute the forensic metadata extraction\
brief.get_brief()
