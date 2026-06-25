# Login Dictionary Brute Forcer (Project 028)

A high-performance security utility engineered for authentication auditing and credential strength validation. This tool enables security auditors to programmatically assess the resistance of login interfaces against dictionary-based credential attacks, providing a quantitative metric for password policy effectiveness.

## Technical Explanation

* **HTTP Payload Injection:** Programmatically crafts and submits authentication payloads (`username` / `password`) via HTTP POST requests. By bypassing the browser UI, the tool communicates directly with the authentication backend, allowing for high-frequency testing.
* **Auth-Status Heuristics:** Evaluates server responses using signature-based logic. By searching for specific "Invalid" or "Rejected" strings in the response body, the tool accurately differentiates between successful authentication events and failed attempts, regardless of HTTP status codes.
* **Stream-Based Dictionary Iteration:** Implements a file-streaming architecture to iterate through credential candidates. This approach ensures that even massive dictionary files are processed linearly, maintaining a minimal memory footprint during the audit execution.

## Problems Solved

* **Credential Policy Validation:** Exposes accounts that rely on weak or common passwords, providing empirical evidence needed to enforce stronger password complexity requirements.
* **Security Control Assessment:** Tests the efficacy of server-side rate-limiting and account lockout thresholds. By observing the server's response to rapid-fire requests, auditors can determine if security controls are actually functioning as expected.
* **Boundary Integrity Audit:** Confirms whether the authentication gateway correctly validates credentials before granting session tokens, identifying potential bypasses in the login logic.

## Design Decisions: "Why this instead of that?"

| Category | Decision | Why? |
| :--- | :--- | :--- |
| **I/O Strategy** | Streamed File Reading | Instead of loading entire wordlists into memory, streaming line-by-line allows for testing huge datasets on resource-constrained devices. |
| **Detection** | Signature Matching | Simple and robust. It ignores HTTP status codes (which can be unreliable, e.g., 200 OK on both success and fail) and focuses on the actual content body. |
| **Efficiency** | `requests` Library | Optimized for connection pooling. It is faster and easier to manage than low-level socket programming for HTTP operations. |
| **Safety** | Dictionary-Only Approach | Focuses on verifiable credential lists, preventing the tool from becoming a general-purpose "scanner" and keeping the scope strictly limited to authorized auditing. |

## Usage

This utility serves as the primary module for credential strength assessment. Ensure the file is saved as `login_brute_forcer.py`.

```python
from login_brute_forcer import LoginBruteForcer

# 1. Initialize the auditor for the specific target and account
# The tool encapsulates the request logic
auditor = LoginBruteForcer("[http://127.0.0.1/login](http://127.0.0.1/login)", "admin")

# 2. Execute the authentication strength sweep
# The tool returns True if credentials are found, False if dictionary exhausted
auditor.crack("passwords.txt")
