# Process Watchdog (Project 009)

An automated defense tool that enforces process whitelisting by
terminating any unauthorized background activities in real-time.

## Technical Explanation

-   **Dynamic Auditing:** Uses *psutil.process_iter* to poll the
    system\'s active process list continuously.
-   **Whitelist Enforcement:** Matches process names against a
    pre-defined secure list, effectively creating an \"Allow-List\"
    environment.
-   **Safety Mechanisms:** Includes logic to ignore low-PID system
    processes (PID \< 100), preventing critical kernel/OS crashes.

## Problems Solved

1.  **Malware Persistence:** Prevents malicious background processes
    from running.
2.  **Distraction Management:** Can be used to kill games, social media
    apps, or unauthorized tools while the user is studying.
3.  **Environment Hardening:** Ensures that only authorized security
    tools run on a forensic host.

## Design Decisions: \"Why this instead of that?\"

  ------------- --------------------- --------------------------------------------------------------------------------------------------------
  **Logic**     Whitelisting          More secure than blacklisting, as it prevents all unknown software by default.
  **Safety**    *pid \< 100* filter   Essential protection to ensure the script doesn\'t accidentally trigger a Blue Screen of Death (BSOD).
  **Cleanup**   *try-except* block    Necessary to handle processes that die during the loop, ensuring the script keeps running.
  ------------- --------------------- --------------------------------------------------------------------------------------------------------

## Usage

from 009_process_watchdog import ProcessWatchdog\
\
\# Define apps you need to study\
watchdog = ProcessWatchdog(\[\"code.exe\", \"chrome.exe\"\])\
watchdog.start_protection(interval=10)
