# Network Heartbeat System (Project 2)

A robust utility for securing continuous device communication. This tool
prevents \"Replay Attacks\" by attaching a time-based hash to every
heartbeat packet.

## Purpose

In network monitoring, simply sending a \"ping\" is insecure because
anyone can intercept and spoof that signal. This tool ensures that each
heartbeat is unique, time-stamped, and cryptographically signed, making
captured packets useless to attackers after a few seconds.

## Technical Explanation

-   **Time-Synchronization:** Uses *time.time()* to generate a
    sliding-window authentication.
-   **Cryptographic Hashing:** Uses *SHA-256* to create a signature that
    binds the specific time to your secret key.
-   **Secure Comparison:** Uses *secrets.compare_digest* to perform
    constant-time comparisons, mitigating timing side-channel attacks.

## Problems Solved

1.  **Replay Attacks:** An attacker cannot reuse an old heartbeat
    because the server will reject packets outside the defined
    *window_seconds*.
2.  **Authentication:** Ensures that only devices possessing the
    *secret_key* can generate valid heartbeats.
3.  **Data Integrity:** If even one bit of the timestamp or key changes,
    the hash will fail to validate.

## Design Decisions

  --------------- ------------------- -------------------------------------------------------------------------------------------------
  **Integrity**   *SHA-256*           Provides a high-collision resistance hash, ideal for small security tokens.
  **Logic**       Time-based window   Prevents stale packets from being accepted, a core requirement for secure UDP streaming.
  **Security**    *secrets* module    Preferable over *random* or *hashlib* alone for constant-time comparisons in security contexts.
  --------------- ------------------- -------------------------------------------------------------------------------------------------

## Usage

from project_2_network_heartbeat import NetworkHeartbeat\
\
key = \"YOUR_SHARED_SECRET\"\
hb = NetworkHeartbeat(key)\
\
\# Generate a secure packet\
packet = hb.generate_heartbeat()\
\
\# Verify on receiver side\
is_valid, msg = NetworkHeartbeat.verify_heartbeat(packet, key)
