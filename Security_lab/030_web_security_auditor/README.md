# Web Security Auditor (Project 030)

An automated configuration assessment tool that audits web servers for
the presence of hardening headers and secure cookie attributes.

## Technical Explanation

-   **Header Hardening Verification:** Compares the target site's
    response against a predefined security manifest, flagging absent
    headers that expose the site to well-known attack vectors (e.g.,
    Clickjacking).
-   **Cookie Attribute Audit:** Inspects session tokens for the
    *HttpOnly* flag, a critical defense against XSS-based session
    hijacking.
-   **HEAD-Request Efficiency:** Utilizes HTTP HEAD requests to perform
    rapid audits without the overhead of downloading multi-megabyte HTML
    page bodies.

## Problems Solved

1.  **Security Policy Gaps:** Quickly identifies misconfigured servers
    that fail to implement industry-standard defenses like HSTS or CSP.
2.  **Session Token Exfiltration Risks:** Detects if cookies are
    susceptible to being stolen by malicious JavaScript due to missing
    browser protection flags.

## Usage

from 030_web_security_auditor import SecurityHeaderAuditor\
\
\# Perform a hardening audit on a target web service\
auditor =
SecurityHeaderAuditor(\"\[https://example.com\](https://example.com)\")\
auditor.audit()
