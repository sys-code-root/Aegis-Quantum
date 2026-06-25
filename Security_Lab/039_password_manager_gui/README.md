# Full GUI Password Vault & Manager (Project 039)

An integrated credential-management dashboard that unifies a high-entropy generation engine, event-driven GUI inputs, and SQL-bound relational persistence into a singular, portable application.

## Technical Explanation

* **Event-Driven UI Integration:** Bridges synchronous backend data streams directly into an asynchronous `Tkinter` event loop. This ensures the dashboard remains responsive while handling relational database I/O.
* **Deterministic Entropy Engine:** Utilizes the `string` and `random` primitives to construct high-entropy character matrices. This generates cryptographically unpredictable credentials across customizable length parameters.
* **Input-Layer Sanitization:** Implements strict data-type trapping (`ValueError`) and parameter-bound SQL queries. This defensive architecture proactively sanitizes user inputs before they reach the memory buffer or the relational database layer, nullifying common injection vectors.

## Problems Solved

* **Credential Fragility:** Eliminates human bias in password selection by enforcing high-entropy generation, drastically reducing the success rate of dictionary or brute-force attacks on managed services.
* **Management Fragmentation:** Consolidates target service configurations, metadata, and authentication tokens into a unified, secure relational architecture rather than scattered text files.
* **Injection-Proof Persistence:** Uses parameterized SQL bindings, ensuring that even if malicious strings are entered into the GUI, they are treated as data, not as executable database commands.

## Design Decisions: "Why this instead of that?"

| Category | Decision | Why? |
| :--- | :--- | :--- |
| **Persistence** | `SQLite` | A file-based, serverless database that requires zero configuration, making it ideal for portable forensic toolkits. |
| **Security** | Parameterized Queries | Binding inputs (`?`) is the industry standard to neutralize SQL Injection vulnerabilities at the source. |
| **Interface** | `Tkinter` | Built into the Python standard library, it ensures the tool works on any system (Windows/Linux/macOS) without needing extra `pip install` dependencies. |
| **Validation** | Synchronous Trapping | Catching errors (like non-numeric entropy lengths) before the logic processes ensures the application never crashes in the field. |

## Usage

This dashboard is designed to be the primary interface for your secure credential vault. Ensure the file is saved as `password_manager.py`.

Launch the integrated vault directly from your terminal:

```bash
python password_manager.py
