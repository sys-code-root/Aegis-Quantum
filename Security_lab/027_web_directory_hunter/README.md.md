# Web Directory Hunter & Path Auditor (Project 027)

A web interface assessment utility designed to look for hidden directory
structures, forgotten backup logs, or unprotected administration
endpoints on a target web server.

## Technical Explanation

-   **HTTP Status Code Mapping:** Inspects operational HTTP response
    codes directly from the host (*200 OK* vs *403 Forbidden*) to map
    server directory structures.
-   **Wordlist Stream Ingestion:** Streams flat-text dictionary elements
    line-by-line to execute structural directory testing without
    creating large memory buffers.
-   **Network Exception Isolation:** Incorporates localized exception
    shielding to handle network connection issues cleanly without
    interrupting the ongoing scan.

## Problems Solved

1.  **Unprotected Artifact Exposure:** Helps web administrators locate
    exposed diagnostic scripts (*info.php*), configuration backups
    (*.bak*), or old source code zip archives.
2.  **Access Control Validation:** Validates whether restricted
    administrative paths actually block unauthenticated users with a
    proper *403 Forbidden* status code.
3.  **Information Leakage Triage:** Identifies non-indexed paths that
    are left reachable, reducing the attack surface before deployment.

## Design Decisions: \"Why this instead of that?\"

  ---------------------- ----------------------- -----------------------------------------------------------------------------------------------------------------
  **Protocol Method**    *requests.get* Method   Standard choice for simple path auditing, ensuring the application processes standard responses accurately.
  **Timeout Boundary**   3-Second Rule           Balances validation accuracy with execution speed, avoiding long delays from hanging scripts or slow endpoints.
  ---------------------- ----------------------- -----------------------------------------------------------------------------------------------------------------

## Usage

from 027_web_directory_hunter import WebDirectoryHunter\
\
\# Instantiate the auditor on a local development server\
auditor = WebDirectoryHunter(\"http://localhost:8080\")\
\
\# Run the discovery engine against a standard test list\
auditor.scan(\"wordlist.txt\")
