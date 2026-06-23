# Secure Vault Injection Patterns (Project 035)

A reference implementation demonstrating the architectural implementation of Parameterized Queries as the primary defense mechanism against SQL Injection (SQLi) vulnerabilities.

## Technical Explanation

* **Execution Flow Separation:** Distinguishes between the *query structure* and the *data input*. In insecure implementations, these are merged, allowing the database engine to interpret user input as executable SQL commands.
* **Prepared Statement Logic:** Utilizing parameterization (`?` placeholders), the database engine compiles the query structure *before* the data is bound. This ensures that even if an input contains SQL syntax (e.g., `' OR '1'='1`), it is treated strictly as a literal value rather than an instruction, effectively nullifying the attack vector.
* **AST (Abstract Syntax Tree) Integrity:** By forcing data to be bound as literals, the system prevents the attacker from modifying the Abstract Syntax Tree of the SQL query, which is the root cause of logic bypasses in standard concatenation methods.

## Problems Solved

* **Input-Level Vulnerability Neutralization:** Acts as a final "sandbox" within the database layer. Even if frontend sanitization filters are bypassed or incorrectly implemented, the parameterized query remains secure.
* **Elimination of Logic Bypasses:** Prevents attackers from injecting tautologies (like `OR 1=1`) that force database engines to return unauthorized records.
* **Architectural Robustness:** Demonstrates the shift from "Detection-based Security" (scanning for hacks) to "Design-based Security" (building systems that are structurally immune to the attack).

## Design Decisions: "Why this instead of that?"

| Category | Decision | Why? |
| :--- | :--- | :--- |
| **Data Handling** | Parameterized Bindings | Decouples SQL logic from data input at the driver level, making injection logically impossible. |
| **Logic** | Prepared Statements | The database engine parses the query structure *before* input is injected, preventing the execution of unintended commands. |
| **Security Posture** | Defense-in-Depth | Provides a robust backend fail-safe; it is the industry standard for preventing SQLi in high-security applications. |
| **Coding Standard** | Placeholders (`?`) | Reduces code complexity by removing the need for manual escaping or quoting, which is highly prone to human error. |

## Usage

This library serves as a secure design pattern. Ensure the file is saved as `vault_patterns.py`.

```python
from vault_patterns import SecureVaultPatterns

vault = SecureVaultPatterns()

# 1. Demonstration of Vulnerability (For educational audit purposes)
# Result: Bypasses authentication/filters by manipulating query logic
vault.insecure_search("' OR '1'='1")

# 2. Demonstration of Remediation
# Result: Returns an exact match (literal search), treating the input as data only
vault.secure_search("' OR '1'='1")
