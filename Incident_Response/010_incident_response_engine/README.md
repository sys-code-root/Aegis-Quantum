# Incident Response Engine (Project 010)

An automated cleanup and analysis engine designed to neutralize threats
and sanitize evidence during an incident.

## Technical Explanation

-   **Vaccine Logic:** Implements a blacklist-based cleanup to
    immediately remove known dangerous file extensions.
-   **Metadata Sanitization:** Uses *Pillow* to reconstruct image files,
    effectively stripping EXIF data that could track the user or expose
    sensitive information.
-   **PDF URI Extraction:** Leverages *pdfplumber* to inspect annotation
    layers of PDF documents, identifying hidden malicious redirect URLs.

## Problems Solved

1.  **Automated Cleanup:** Rapidly removes common malware vectors from a
    compromised folder.
2.  **Evidence Sanitization:** Prevents privacy leaks by stripping
    metadata from files before they are shared or stored.
3.  **Hidden Threat Discovery:** Exposes malicious links inside PDFs
    that aren\'t visible to the naked eye.

## Design Decisions: \"Why this instead of that?\"

  ----------------- ----------------- --------------------------------------------------------------------------------------------------------------
  **PDF Logic**     *pdfplumber*      More robust at extracting annotation metadata than standard PDF libraries.
  **Image Logic**   Data Rebuild      Rebuilding the image is safer than just deleting EXIF headers, as it guarantees no residual metadata exists.
  **Flow**          Modular Methods   Allows the engine to be easily extended as you add support for more file types.
  ----------------- ----------------- --------------------------------------------------------------------------------------------------------------

## Usage

from 010_incident_response_engine import IncidentResponseEngine\
\
\# Engine cleans and inspects target directory\
engine = IncidentResponseEngine(\"./data_to_clean\")\
engine.run_full_scan()
