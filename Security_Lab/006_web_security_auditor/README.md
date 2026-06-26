# Web Security Auditor (Project 030)

An automated configuration assessment utility engineered to audit web server security posture. This tool validates the implementation of critical HTTP security headers and analyzes cookie attributes to identify potential vulnerabilities before they can be exploited.

## Technical Explanation

* **Header Hardening Verification:** Compares the target server's response against a predefined security manifest. By auditing for the presence of headers like `Content-Security-Policy` (CSP) and `Strict-Transport-Security` (HSTS), the tool identifies the site's susceptibility to well-known attack vectors such as Clickjacking, MIME-sniffing, and Protocol Downgrade attacks.
* **Cookie Attribute Audit:** Inspects session tokens for the `HttpOnly` flag. This flag is the primary defense against XSS-based session hijacking, as it prevents client-side scripts from accessing sensitive session cookies.
* **HEAD-Request Efficiency:** Utilizes the HTTP `HEAD` method for all auditing tasks. This enables the tool to retrieve response metadata without downloading the full page body, drastically reducing bandwidth consumption and latency during bulk assessments.

## Problems Solved

* **Security Policy Gaps:** Rapidly identifies misconfigured servers that fail to implement industry-standard defenses, allowing security teams to address "low-hanging fruit" vulnerabilities immediately.
* **Session Hijacking Mitigation:** Detects weak cookie configurations that could allow an attacker to bypass authentication mechanisms if a user is subjected to a Cross-Site Scripting (XSS) attack.
* **Configuration Drift Detection:** Provides a programmatic way to ensure that production web servers remain compliant with organizational hardening standards over time.

## Design Decisions: "Why this instead of that?"

| Category | Decision | Why? |
| :--- | :--- | :--- |
| **Request Method** | `HEAD` vs `GET` | HEAD is optimized for metadata. It prevents the overhead of downloading multi-megabyte HTML payloads, making the audit extremely fast. |
| **Verification** | Manifest-based Audit | Using a list of "Mandatory Headers" ensures the audit is consistent. If a header is missing, it is flagged instantly as a configuration gap. |
| **Cookie Analysis** | Direct Attribute Checking | We don't just check if cookies *exist*; we programmatically inspect their attributes (`HttpOnly`, `Secure`). This is the only way to audit "hardening" rather than just existence. |
| **Framework** | `requests` | Standard library for HTTP. It abstracts away the complexity of socket-level programming while providing robust redirect and timeout handling out of the box. |

## Usage

This utility is designed to serve as the initial audit module for your reconnaissance pipeline. Ensure the file is saved as `web_auditor.py`.

```python
from web_auditor import SecurityHeaderAuditor

# 1. Initialize the audit on the target service
# The tool automatically manages the request state
target = "[https://example.com](https://example.com)"
auditor = SecurityHeaderAuditor(target)

# 2. Execute the security posture assessment
# Output provides a clear [SAFE] vs [VULNERABLE] status report
auditor.audit()
