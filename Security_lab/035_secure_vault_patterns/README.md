# Secure Vault Injection Patterns (Project 035)

A reference implementation demonstrating the implementation of
Parameterized Queries as a primary defense against SQL Injection (SQLi)
vulnerabilities.

## Technical Explanation

-   **String Concatenation (Vulnerability):** Shows how *f-strings* or
    direct concatenation allow attackers to escape SQL syntax and
    manipulate query logic (e.g., using *\' OR \'1\'=\'1*).
-   **Parameterization (Remediation):** Explains how *?* placeholders
    tell the database engine to prepare the query structure *before* the
    data is injected, ensuring inputs cannot modify the query execution
    path.

## Why this is critical

-   **Prevention vs. Detection:** While your other scanners *detect*
    vulnerabilities, this script shows how to *prevent* them during the
    design phase of any application you build.
-   **Defense in Depth:** Even if input sanitization fails at the
    frontend, parameterized queries act as a final \"sandbox\" inside
    the database layer, nullifying the attack.

## Usage

from 035_secure_vault_patterns import SecureVaultPatterns\
\
vault = SecureVaultPatterns()\
\
\# Demonstrating vulnerability:\
\# Result: Returns all database rows by bypassing logic\
vault.insecure_search(\"\' OR \'1\'=\'1\")\
\
\# Demonstrating protection:\
\# Result: Returns nothing (or an exact match), as the injected string
is treated as a literal URL\
vault.secure_search(\"\' OR \'1\'=\'1\")
