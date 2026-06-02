# Login Dictionary Brute Forcer (Project 028)

A security utility designed for authentication auditing and credential
strength validation. It identifies vulnerabilities in login interfaces
by simulating dictionary-based credential attacks.

## Technical Explanation

-   **POST Request Injection:** Manually crafts authentication payloads
    (*username*/*password*) and submits them via HTTP POST to the
    backend server.
-   **Failure Pattern Matching:** Evaluates server responses against a
    predefined *error_message* string, allowing the tool to distinguish
    between authenticated sessions and rejected attempts.
-   **Payload Iteration:** Streams credential candidates from a
    flat-text dictionary to perform rapid testing without exhausting
    system memory.

## Problems Solved

1.  **Weak Credential Identification:** Exposes accounts that utilize
    passwords present in standard dictionary files (e.g.,
    \'password123\', \'admin\').
2.  **Brute-Force Policy Verification:** Tests whether the target server
    implements account lockout thresholds or rate-limiting strategies
    effectively.
3.  **Authentication Boundary Audit:** Confirms if the application
    correctly validates inputs before granting session cookies.

## Usage

from 028_login_brute_forcer import LoginBruteForcer\
\
\# Setup the auditor targeting a local development endpoint\
auditor =
LoginBruteForcer(\"\[http://127.0.0.1/login\](http://127.0.0.1/login)\",
\"admin\")\
\
\# Perform the authentication strength sweep\
auditor.crack(\"passwords.txt\")
